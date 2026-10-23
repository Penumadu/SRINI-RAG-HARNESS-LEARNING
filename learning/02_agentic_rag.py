"""
==============================================================================
02_agentic_rag.py — End-to-End Agentic RAG System with LangGraph
==============================================================================
Converted from notebooks/agentic_rag.ipynb.

This module is a complete, self-contained educational implementation of an
Agentic RAG system featuring:
  • Hierarchical Indexing (Small Child chunks for search, Large Parent chunks for context)
  • Hybrid Search (Dense embeddings + BM25 sparse vectors via Qdrant)
  • Conversation Memory & Rolling Summarization
  • Query Decomposition & Human-in-the-Loop Clarification
  • Multi-Agent Map-Reduce (Parallel sub-question retrieval)
  • Dynamic Context Compression & Self-Correction Loops
  • Flexible Model Support (Local Ollama, OpenAI, Anthropic, or Google Gemini)

Usage:
  # 1. Index sample documents into Qdrant & Parent Store:
  python learning/02_agentic_rag.py --index

  # 2. Ask a question via CLI:
  python learning/02_agentic_rag.py --query "What are the advantages of client-side JavaScript?"

  # 3. Start an interactive terminal conversation:
  python learning/02_agentic_rag.py --chat

  # 4. Launch the local Gradio Web UI:
  python learning/02_agentic_rag.py --ui
==============================================================================
"""

import os
import sys
import glob
import json
import uuid
import argparse
from pathlib import Path
from functools import lru_cache
from typing import List, Literal, Set, Dict, Any, Annotated
import operator

# Ensure workspace root is in sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning import config


# ==============================================================================
# SECTION 1: Token Management & Utilities
# ==============================================================================

@lru_cache(maxsize=1)
def _get_token_encoding():
    """Lazily loads tiktoken cl100k_base encoding with character fallback."""
    try:
        import tiktoken
        return tiktoken.encoding_for_model("gpt-4")
    except Exception:
        try:
            import tiktoken
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None


def count_tokens(text: str) -> int:
    """Estimates tokens using tiktoken, falling back to 4 chars/token."""
    if not text:
        return 0
    enc = _get_token_encoding()
    if enc:
        try:
            return len(enc.encode(text))
        except Exception:
            pass
    return max(1, len(text) // 4)


def estimate_context_tokens(messages: list) -> int:
    """Estimates total tokens across a list of LangChain messages."""
    total = 0
    for msg in messages:
        content = getattr(msg, "content", "")
        if isinstance(content, str):
            total += count_tokens(content)
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for tc in tool_calls:
                total += count_tokens(json.dumps(tc))
    return total


# ==============================================================================
# SECTION 2: System Prompts
# ==============================================================================

def get_conversation_summary_prompt() -> str:
    return """## Role
You are a compact memory manager for a retrieval-augmented chat assistant.

## Context
The input contains an existing rolling summary plus older user/assistant messages that will be removed from raw chat history.

## Instructions
- Produce an updated, dense rolling summary combining prior context and new messages.
- Preserve core user intent, preferences, constraints, entities, and answers already given.
- Do NOT include filler; keep it concise and factual.
- Return ONLY the updated summary text.
"""


def get_query_rewriter_prompt() -> str:
    return """## Role
You are an intelligent query analysis agent for an enterprise documentation RAG system.

## Task
Analyze the user's latest query in the context of recent chat history and rolling summary.
Determine whether the query needs clarification, or if it can be broken into 1 to 3 targeted retrieval sub-queries.

## Rules
1. If the user query is excessively vague, ambiguous, or lacks key context needed to search (e.g. "tell me more", "how does it work?"), flag need_clarification=True and formulate a polite, specific clarification question.
2. If the user query is clear, decompose it into 1 to 3 distinct, self-contained sub-queries (sub_queries) suitable for semantic keyword search.
3. If the query is a simple greeting or general acknowledgement not requiring document search, output empty sub_queries and need_clarification=False.
"""


def get_clarification_prompt() -> str:
    return """## Role
You are a helpful AI assistant politely requesting clarification from the user.
Explain what specific details are needed to provide an accurate answer based on the knowledge base.
"""


def get_orchestrator_prompt() -> str:
    return """## Role
You are an expert retrieval reasoning agent specializing in technical documentation.

## Instructions
1. Review the assigned sub-question and existing retrieved evidence (if any).
2. If you need more evidence, call `search_child_chunks(query=...)` with targeted keywords.
3. When `search_child_chunks` returns relevant parent chunk IDs, call `retrieve_parent_chunks(parent_ids=[...])` to inspect the full surrounding context.
4. Once you have sufficient factual information to answer the question, formulate a clear, complete, cited answer.
5. If the documentation does not contain the answer after reasonable searches, state what was found and what is missing.
"""


def get_context_compression_prompt() -> str:
    return """## Role
You are a working memory compressor for a RAG retrieval agent.

## Task
Summarize the search queries executed, documents consulted, and key factual findings gathered so far.
Discard raw text repetition while preserving exact names, numbers, parameters, and findings.
Return a structured, dense bulleted briefing for the next reasoning step.
"""


def get_fallback_response_prompt() -> str:
    return """## Role
You are a synthesis agent providing the best possible factual answer using only the retrieved evidence collected so far.
If the retrieved evidence is partial, answer what is supported and acknowledge limitations honestly.
"""


def get_aggregation_prompt() -> str:
    return """## Role
You are the lead synthesis agent for an Agentic RAG system.

## Task
Combine the answers from individual sub-query agents into a cohesive, well-structured, comprehensive response addressing the original user question.
Ensure consistent tone, remove duplicate points, and preserve accurate technical details.
"""


# ==============================================================================
# SECTION 3: Hierarchical Document Chunking
# ==============================================================================

class HierarchicalChunker:
    """
    Implements Hierarchical Chunking:
      - Markdown Header splitting creates large Parent Chunks (preserving section context)
      - Recursive Character splitting derives small Child Chunks (indexed in Vector DB)
    """

    def __init__(self):
        from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
        self.parent_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=config.HEADERS_TO_SPLIT_ON,
            strip_headers=False
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHILD_CHUNK_SIZE,
            chunk_overlap=config.CHILD_CHUNK_OVERLAP
        )

    def process_file(self, file_path: Path):
        content = file_path.read_text(encoding="utf-8")
        raw_parents = self.parent_splitter.split_text(content)

        merged_parents = self._merge_small_parents(raw_parents)
        parent_records = []
        child_records = []

        for p_idx, p_doc in enumerate(merged_parents):
            p_id = f"{file_path.stem}_p{p_idx:03d}"
            p_text = p_doc.page_content

            parent_records.append({
                "parent_id": p_id,
                "source": file_path.name,
                "content": p_text,
                "metadata": p_doc.metadata
            })

            # Create child chunks
            child_docs = self.child_splitter.create_documents([p_text])
            for c_idx, c_doc in enumerate(child_docs):
                c_id = f"{p_id}_c{c_idx:03d}"
                c_meta = dict(p_doc.metadata)
                c_meta.update({
                    "parent_id": p_id,
                    "child_id": c_id,
                    "source": file_path.name,
                })
                child_records.append({
                    "child_id": c_id,
                    "parent_id": p_id,
                    "source": file_path.name,
                    "content": c_doc.page_content,
                    "metadata": c_meta
                })

        return parent_records, child_records

    def _merge_small_parents(self, chunks):
        if not chunks:
            return []
        merged, current = [], None
        for chunk in chunks:
            if current is None:
                current = chunk
            else:
                current.page_content += "\n\n" + chunk.page_content
                current.metadata.update(chunk.metadata)

            if len(current.page_content) >= config.MIN_PARENT_SIZE:
                merged.append(current)
                current = None
        if current:
            if merged:
                merged[-1].page_content += "\n\n" + current.page_content
                merged[-1].metadata.update(current.metadata)
            else:
                merged.append(current)
        return merged


# ==============================================================================
# SECTION 4: Storage Managers (Qdrant & Parent Store)
# ==============================================================================

class StorageManager:
    """Manages Qdrant Vector DB (Dense + Sparse) and Local Parent Store."""

    def __init__(self):
        self.qdrant_path = config.QDRANT_DB_PATH
        self.parent_store_dir = Path(config.PARENT_STORE_PATH)
        self.parent_store_dir.mkdir(parents=True, exist_ok=True)
        self.client = None
        self.vector_store = None
        self.dense_embeddings = None
        self.sparse_embeddings = None

    def initialize(self):
        from qdrant_client import QdrantClient
        from qdrant_client.http import models as qmodels
        from langchain_qdrant import QdrantVectorStore, RetrievalMode
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_qdrant.fastembed_sparse import FastEmbedSparse

        print("📦 Initializing Qdrant client and Embeddings...")
        self.client = QdrantClient(path=self.qdrant_path)
        self.dense_embeddings = config.get_dense_embeddings()
        self.sparse_embeddings = FastEmbedSparse(model_name=config.SPARSE_MODEL)

        # Check or create collection with matching dimension
        dense_dim = len(self.dense_embeddings.embed_query("warmup"))
        if self.client.collection_exists(config.CHILD_COLLECTION):
            c_info = self.client.get_collection(config.CHILD_COLLECTION)
            v_cfg = c_info.config.params.vectors
            curr_size = getattr(v_cfg, "size", None)
            if curr_size and curr_size != dense_dim:
                print(f"⚠️ Dimension change detected ({curr_size} -> {dense_dim}). Recreating collection...")
                self.client.delete_collection(config.CHILD_COLLECTION)

        if not self.client.collection_exists(config.CHILD_COLLECTION):
            print(f"Creating Qdrant collection: {config.CHILD_COLLECTION} (dim: {dense_dim})")
            self.client.create_collection(
                collection_name=config.CHILD_COLLECTION,
                vectors_config=qmodels.VectorParams(
                    size=dense_dim,
                    distance=qmodels.Distance.COSINE
                ),
                sparse_vectors_config={
                    config.SPARSE_VECTOR_NAME: qmodels.SparseVectorParams()
                }
            )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=config.CHILD_COLLECTION,
            embedding=self.dense_embeddings,
            sparse_embedding=self.sparse_embeddings,
            sparse_vector_name=config.SPARSE_VECTOR_NAME,
            retrieval_mode=RetrievalMode.HYBRID
        )
        print("✓ Storage Manager initialized.")

    def save_parent(self, parent_id: str, data: dict):
        p_file = self.parent_store_dir / f"{parent_id}.json"
        p_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_parent(self, parent_id: str) -> dict | None:
        p_file = self.parent_store_dir / f"{parent_id}.json"
        if p_file.exists():
            return json.loads(p_file.read_text(encoding="utf-8"))
        return None

    def index_all(self, markdown_dir: str = None):
        """Indexes all markdown documents into Qdrant & Parent store."""
        from langchain_core.documents import Document

        m_dir = Path(markdown_dir or config.MARKDOWN_DIR)
        md_files = sorted(m_dir.glob("*.md"))
        if not md_files:
            print(f"⚠️ No markdown files found in {m_dir}. Generating sample docs...")
            from learning.sample_docs import create_sample_documents
            create_sample_documents(str(m_dir))
            md_files = sorted(m_dir.glob("*.md"))

        print(f"\n🚀 Indexing {len(md_files)} documents from '{m_dir}'...")
        chunker = HierarchicalChunker()

        total_parents = 0
        all_child_docs = []

        for f in md_files:
            parents, children = chunker.process_file(f)
            for p in parents:
                self.save_parent(p["parent_id"], p)
            total_parents += len(parents)

            for c in children:
                all_child_docs.append(Document(
                    page_content=c["content"],
                    metadata=c["metadata"]
                ))

        if all_child_docs:
            print(f"Embedding {len(all_child_docs)} child chunks into Qdrant...")
            self.vector_store.add_documents(all_child_docs)

        print(f"✅ Indexing complete: {total_parents} Parent chunks stored, {len(all_child_docs)} Child chunks indexed.")


# ==============================================================================
# SECTION 5: Agent Tools
# ==============================================================================

def create_rag_tools(storage: StorageManager):
    """Factory creating LangChain tools wired to storage."""
    from langchain_core.tools import tool

    @tool
    def search_child_chunks(query: str, limit: int = config.DEFAULT_RETRIEVAL_K) -> str:
        """Search document excerpts for evidence related to the user question.
        Returns matching child chunk excerpts with parent IDs and scores.
        """
        results = storage.vector_store.similarity_search_with_score(query=query, k=limit)
        if not results:
            return "No matching excerpts found for query."

        output = []
        for doc, score in results:
            if score < config.RETRIEVAL_SCORE_THRESHOLD:
                continue
            parent_id = doc.metadata.get("parent_id", "unknown")
            source = doc.metadata.get("source", "unknown")
            output.append(
                f"[Score: {score:.3f} | Source: {source} | Parent ID: {parent_id}]\n{doc.page_content}"
            )
        return "\n\n---\n\n".join(output) if output else "No results passed score threshold."

    @tool
    def retrieve_parent_chunks(parent_ids: list[str]) -> str:
        """Retrieve the full, detailed parent context sections using their parent IDs."""
        if isinstance(parent_ids, str):
            parent_ids = [parent_ids]

        sections = []
        for pid in parent_ids:
            p_data = storage.get_parent(pid)
            if p_data:
                source = p_data.get("source", "unknown")
                sections.append(f"### [Parent: {pid} | Source: {source}]\n{p_data.get('content', '')}")
            else:
                sections.append(f"### [Parent: {pid}] Not found.")
        return "\n\n" + ("=" * 40) + "\n\n".join(sections)

    return [search_child_chunks, retrieve_parent_chunks]


# ==============================================================================
# SECTION 6: LangGraph State Definitions & Reducers
# ==============================================================================

from pydantic import BaseModel, Field
from langgraph.graph import MessagesState


class SubQuery(BaseModel):
    sub_query: str = Field(description="Self-contained retrieval sub-query")


class QueryDecomposition(BaseModel):
    need_clarification: bool = Field(description="True if query is too ambiguous to answer")
    clarification_question: str = Field(default="", description="Question to ask user if clarification is needed")
    sub_queries: List[SubQuery] = Field(default_factory=list, description="1 to 3 targeted search queries")


def accumulate_or_reset(existing: List[dict], new: List[dict]) -> List[dict]:
    if new and any(item.get("__reset__") for item in new):
        return []
    return (existing or []) + (new or [])


class State(MessagesState):
    context_summary: str
    originalQuery: str
    clarificationQuery: str
    agent_answers: Annotated[List[dict], accumulate_or_reset]


class AgentState(MessagesState):
    context_summary: str
    question: str
    question_index: int
    retrieval_keys: Set[str]
    retrieved_contexts: List[str]
    final_answer: str


# ==============================================================================
# SECTION 7: LangGraph Nodes & Routing Logic
# ==============================================================================

def build_agent_graph(llm, tools, storage: StorageManager):
    """Constructs and compiles the complete multi-agent LangGraph workflow."""
    from langgraph.graph import START, END, StateGraph
    from langgraph.prebuilt import ToolNode
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import Send, Command
    from langchain_core.messages import (
        HumanMessage, AIMessage, SystemMessage, RemoveMessage, ToolMessage
    )

    llm_with_tools = llm.bind_tools(tools)
    tool_node = ToolNode(tools)

    # ── Subgraph Nodes ────────────────────────────────────────────────────────
    def orchestrator(state: AgentState):
        messages = state["messages"]
        summary = state.get("context_summary", "").strip()

        sys_prompt = get_orchestrator_prompt()
        if summary:
            sys_prompt += f"\n\n## Prior Investigation Findings:\n{summary}"

        full_prompt = [SystemMessage(content=sys_prompt)] + messages
        response = llm_with_tools.invoke(full_prompt)
        return {"messages": [response]}

    def route_after_orchestrator(state: AgentState) -> Literal["tools", "fallback_response", "collect_answer"]:
        last_msg = state["messages"][-1]
        tool_calls = getattr(last_msg, "tool_calls", None)

        if not tool_calls:
            return "collect_answer"

        # Check recursion limits
        tool_count = sum(1 for m in state["messages"] if isinstance(m, ToolMessage))
        if tool_count >= config.MAX_TOOL_CALLS:
            return "fallback_response"

        return "tools"

    def should_compress_context(state: AgentState) -> Command[Literal["compress_context", "orchestrator"]]:
        messages = state["messages"]
        tokens = estimate_context_tokens(messages)
        goto = "compress_context" if tokens > config.BASE_TOKEN_THRESHOLD else "orchestrator"
        return Command(goto=goto)

    def compress_context(state: AgentState):
        messages = state["messages"]
        summary_prompt = get_context_compression_prompt()
        text_to_compress = "\n\n".join(
            f"{m.__class__.__name__}: {getattr(m, 'content', '')}"
            for m in messages[1:]
        )
        compressed = llm.invoke([
            SystemMessage(content=summary_prompt),
            HumanMessage(content=text_to_compress)
        ])
        # Keep initial user question, remove tool noise
        return {
            "context_summary": compressed.content,
            "messages": [RemoveMessage(id=m.id) for m in messages[1:] if hasattr(m, "id")]
        }

    def fallback_response(state: AgentState):
        prompt = (
            f"User Question: {state.get('question')}\n"
            f"Collected Findings: {state.get('context_summary', '')}\n"
            f"Please synthesize the best answer possible with the evidence gathered."
        )
        resp = llm.invoke([SystemMessage(content=get_fallback_response_prompt()), HumanMessage(content=prompt)])
        return {"messages": [resp]}

    def collect_answer(state: AgentState):
        last_msg = state["messages"][-1]
        answer = last_msg.content if isinstance(last_msg, AIMessage) else "No answer generated."
        return {
            "final_answer": answer,
            "agent_answers": [{
                "index": state.get("question_index", 0),
                "question": state.get("question", ""),
                "answer": answer,
            }]
        }

    # Assemble Subgraph
    sub_builder = StateGraph(AgentState)
    sub_builder.add_node("orchestrator", orchestrator)
    sub_builder.add_node("tools", tool_node)
    sub_builder.add_node("compress_context", compress_context)
    sub_builder.add_node("fallback_response", fallback_response)
    sub_builder.add_node("should_compress_context", should_compress_context)
    sub_builder.add_node("collect_answer", collect_answer)

    sub_builder.add_edge(START, "orchestrator")
    sub_builder.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {"tools": "tools", "fallback_response": "fallback_response", "collect_answer": "collect_answer"}
    )
    sub_builder.add_edge("tools", "should_compress_context")
    sub_builder.add_edge("compress_context", "orchestrator")
    sub_builder.add_edge("fallback_response", "collect_answer")
    sub_builder.add_edge("collect_answer", END)
    agent_subgraph = sub_builder.compile()

    # ── Main Graph Nodes ──────────────────────────────────────────────────────
    def summarize_history(state: State):
        messages = state.get("messages", [])
        if len(messages) <= config.MAIN_HISTORY_MESSAGES_TO_KEEP:
            return {}
        old_msgs = messages[:-config.MAIN_HISTORY_MESSAGES_TO_KEEP]
        existing = state.get("context_summary", "")
        prompt = f"Existing Summary:\n{existing}\n\nMessages to summarize:\n"
        for m in old_msgs:
            prompt += f"{m.__class__.__name__}: {getattr(m, 'content', '')}\n"

        summary_resp = llm.invoke([
            SystemMessage(content=get_conversation_summary_prompt()),
            HumanMessage(content=prompt)
        ])
        return {
            "context_summary": summary_resp.content,
            "messages": [RemoveMessage(id=m.id) for m in old_msgs if hasattr(m, "id")]
        }

    def rewrite_query(state: State):
        last_msg = state["messages"][-1]
        user_query = last_msg.content if isinstance(last_msg, HumanMessage) else ""
        structured_llm = llm.with_structured_output(QueryDecomposition)
        
        prompt = f"User Question: {user_query}\nSummary: {state.get('context_summary', '')}"
        try:
            decomp = structured_llm.invoke([
                SystemMessage(content=get_query_rewriter_prompt()),
                HumanMessage(content=prompt)
            ])
        except Exception:
            # Fallback if model doesn't support structured output
            decomp = QueryDecomposition(
                need_clarification=False,
                sub_queries=[SubQuery(sub_query=user_query)]
            )

        return {
            "originalQuery": user_query,
            "clarificationQuery": decomp.clarification_question,
            "agent_answers": [{"__reset__": True}],
            "_decomp": decomp
        }

    def route_after_rewrite(state: State):
        decomp: QueryDecomposition = state.get("_decomp")
        if decomp and decomp.need_clarification:
            return "request_clarification"

        sub_queries = decomp.sub_queries if decomp else []
        if not sub_queries:
            sub_queries = [SubQuery(sub_query=state.get("originalQuery", ""))]

        # Fan-out to parallel agent subgraphs via Send API
        return [
            Send("agent", {
                "messages": [HumanMessage(content=sq.sub_query)],
                "question": sq.sub_query,
                "question_index": idx,
                "context_summary": state.get("context_summary", ""),
                "retrieval_keys": set(),
                "retrieved_contexts": [],
                "final_answer": ""
            })
            for idx, sq in enumerate(sub_queries)
        ]

    def request_clarification(state: State):
        q = state.get("clarificationQuery") or "Could you please provide more specific details?"
        return {"messages": [AIMessage(content=q)]}

    def aggregate_answers(state: State):
        answers = state.get("agent_answers", [])
        if not answers:
            return {"messages": [AIMessage(content="I could not find relevant information in the documents.")]}

        formatted = "\n\n".join(
            f"Sub-Query {ans.get('index', 0) + 1} ({ans.get('question')}):\n{ans.get('answer')}"
            for ans in answers
        )
        prompt = (
            f"Original User Question: {state.get('originalQuery')}\n\n"
            f"Findings from Retrieval Agents:\n{formatted}"
        )
        resp = llm.invoke([SystemMessage(content=get_aggregation_prompt()), HumanMessage(content=prompt)])
        return {"messages": [resp]}

    # Assemble Main Graph
    main_builder = StateGraph(State)
    main_builder.add_node("summarize_history", summarize_history)
    main_builder.add_node("rewrite_query", rewrite_query)
    main_builder.add_node("request_clarification", request_clarification)
    main_builder.add_node("agent", agent_subgraph)
    main_builder.add_node("aggregate_answers", aggregate_answers)

    main_builder.add_edge(START, "summarize_history")
    main_builder.add_edge("summarize_history", "rewrite_query")
    main_builder.add_conditional_edges(
        "rewrite_query",
        route_after_rewrite,
        {"request_clarification": "request_clarification", "agent": "agent"}
    )
    main_builder.add_edge("request_clarification", "rewrite_query")
    main_builder.add_edge("agent", "aggregate_answers")
    main_builder.add_edge("aggregate_answers", END)

    checkpointer = InMemorySaver()
    compiled_graph = main_builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["request_clarification"]
    )
    return compiled_graph


# ==============================================================================
# SECTION 8: Interactive Modes (CLI & Gradio UI)
# ==============================================================================

def run_chat_loop(agent_graph):
    """Interactive terminal conversation loop with conversation memory."""
    from langchain_core.messages import HumanMessage

    thread_id = str(uuid.uuid4())
    print("\n" + "=" * 70)
    print(" 🤖 AGENTIC RAG INTERACTIVE CHAT (Type 'exit' to quit, 'clear' to reset)")
    print("=" * 70 + "\n")

    while True:
        try:
            user_input = input("User 👤: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            thread_id = str(uuid.uuid4())
            print("🧹 Conversation memory cleared.\n")
            continue

        print("\nThinking 🧠...")
        run_config = {"configurable": {"thread_id": thread_id}}
        result = agent_graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=run_config
        )

        last_msg = result["messages"][-1]
        print(f"\nAssistant 🤖:\n{last_msg.content}\n" + "-" * 70 + "\n")


def launch_ui(agent_graph):
    """Launches a sleek local Gradio interface."""
    try:
        import gradio as gr
    except ImportError:
        raise ImportError("Gradio is required for UI. Run: pip install gradio")

    from langchain_core.messages import HumanMessage

    thread_id = str(uuid.uuid4())

    def respond(message, chat_history):
        nonlocal thread_id
        run_config = {"configurable": {"thread_id": thread_id}}
        result = agent_graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=run_config
        )
        bot_response = result["messages"][-1].content
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_response})
        return "", chat_history

    with gr.Blocks(title="Agentic RAG Assistant") as demo:
        gr.Markdown("# 🤖 Agentic RAG Assistant\n*Hierarchical Retrieval + LangGraph Reasoning*")
        chatbot = gr.Chatbot(type="messages", height=500)
        with gr.Row():
            msg_input = gr.Textbox(placeholder="Ask a question about the indexed documents...", scale=8)
            send_btn = gr.Button("Send", variant="primary", scale=2)
        clear_btn = gr.Button("Clear Session")

        send_btn.click(respond, [msg_input, chatbot], [msg_input, chatbot])
        msg_input.submit(respond, [msg_input, chatbot], [msg_input, chatbot])

        def clear_session():
            nonlocal thread_id
            thread_id = str(uuid.uuid4())
            return []

        clear_btn.click(clear_session, None, chatbot)

    print("\n🚀 Launching Gradio UI on http://127.0.0.1:7860...")
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Agentic RAG System: Complete Learning and Execution Module"
    )
    parser.add_argument("--index", action="store_true", help="Index markdown files into Qdrant & Parent store")
    parser.add_argument("--query", "-q", type=str, help="Run a single question query")
    parser.add_argument("--chat", action="store_true", help="Start interactive terminal conversation")
    parser.add_argument("--ui", action="store_true", help="Launch Gradio web interface")
    parser.add_argument("--provider", type=str, choices=["ollama", "openai", "anthropic", "google"], help="Override LLM provider")
    parser.add_argument("--model", type=str, help="Override model name")

    args = parser.parse_args()

    # Initialize Storage and LLM
    storage = StorageManager()
    storage.initialize()

    if args.index:
        storage.index_all()
        if not (args.query or args.chat or args.ui):
            return

    # Initialize LLM & Graph
    print(f"🧠 Initializing LLM ({args.provider or config.LLM_PROVIDER})...")
    llm = config.get_llm(provider=args.provider, model=args.model)
    tools = create_rag_tools(storage)
    agent_graph = build_agent_graph(llm, tools, storage)

    if args.query:
        from langchain_core.messages import HumanMessage
        print(f"\n❓ Query: {args.query}\nExecuting Agentic RAG pipeline...")
        cfg = {"configurable": {"thread_id": str(uuid.uuid4())}}
        res = agent_graph.invoke({"messages": [HumanMessage(content=args.query)]}, config=cfg)
        print("\n💡 Final Answer:\n" + res["messages"][-1].content + "\n")
    elif args.ui:
        launch_ui(agent_graph)
    elif args.chat:
        run_chat_loop(agent_graph)
    else:
        # If no action specified, show help and run interactive chat
        print("\nNo specific flag passed. Starting interactive chat session...")
        run_chat_loop(agent_graph)


if __name__ == "__main__":
    main()
