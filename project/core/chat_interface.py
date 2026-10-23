import json
import re
from langchain_core.messages import HumanMessage, AIMessageChunk, ToolMessage
from core.execution_logger import log_chat_end, log_chat_start, log_error

SYSTEM_NODES = {"summarize_history", "rewrite_query"}
FINAL_RESPONSE_NODES = {"aggregate_answers"}

SYSTEM_NODE_CONFIG = {
    "rewrite_query":     {"title": "🔍 Query Analysis & Rewriting"},
    "summarize_history": {"title": "📋 Chat History Summary"},
}

# --- Helpers ---

def make_message(content, *, title=None, node=None):
    msg = {"role": "assistant", "content": content}
    if title or node:
        msg["metadata"] = {k: v for k, v in {"title": title, "node": node}.items() if v}
    return msg


def find_msg_idx(messages, node):
    return next(
        (i for i, m in enumerate(messages) if m.get("metadata", {}).get("node") == node),
        None,
    )


def parse_rewrite_json(buffer):
    match = re.search(r"\{.*\}", buffer, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except Exception:
        return None


def format_rewrite_content(buffer):
    data = parse_rewrite_json(buffer)
    if not data:
        return "⏳ Analyzing query..."
    if data.get("is_clear"):
        lines = ["✅ **Query is clear**"]
        if data.get("questions"):
            lines += ["\n**Rewritten queries:**"] + [f"- {q}" for q in data["questions"]]
    else:
        lines = ["❓ **Query is unclear**"]
        clarification = data.get("clarification_needed", "")
        if clarification and clarification.strip().lower() != "no":
            lines.append(f"\nClarification needed: *{clarification}*")
    return "\n".join(lines)

# --- End of Helpers ---

from datetime import datetime

class ChatInterface:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.last_query = ""
        self.events_log = []
        self.search_results = []
        self.rewritten_questions = []
        self.working_memory_summary = ""
        self.session_metrics = {
            "tool_calls": 0,
            "queries_processed": 0,
            "clarification_needed": False,
            "status": "Ready",
            "active_node": "Idle",
        }

    def _log_event(self, node: str, event_type: str, detail: str = ""):
        now_str = datetime.now().strftime("%H:%M:%S")
        self.events_log.append({
            "time": now_str,
            "node": node,
            "type": event_type,
            "detail": detail,
        })
        # Keep last 50 events
        if len(self.events_log) > 50:
            self.events_log.pop(0)

    def _extract_search_results(self, content_str: str, tool_name: str = "search"):
        """Extract child and parent chunk details from tool outputs."""
        if not content_str or "NO_RELEVANT_CHUNKS" in content_str or "RETRIEVAL_ERROR" in content_str:
            return
        
        # Check if content has chunks separated by CHILD_CHUNK_SEPARATOR
        import config
        chunks = content_str.split(config.CHILD_CHUNK_SEPARATOR) if hasattr(config, "CHILD_CHUNK_SEPARATOR") else [content_str]
        for c in chunks:
            text = c.strip()
            if not text:
                continue
            parent_id = ""
            file_name = ""
            snippet = text
            for line in text.splitlines():
                if line.startswith("Parent ID:"):
                    parent_id = line.replace("Parent ID:", "").strip()
                elif line.startswith("File Name:"):
                    file_name = line.replace("File Name:", "").strip()
                elif line.startswith("Content:"):
                    snippet = text.split("Content:", 1)[-1].strip()
            self.search_results.append({
                "parent_id": parent_id or "N/A",
                "file_name": file_name or "Unknown Source",
                "tool": tool_name,
                "content": snippet[:400] + ("..." if len(snippet) > 400 else "")
            })

    def _handle_system_node(self, chunk, node, response_messages, system_node_buffer):
        """Update (or create) the collapsible system-node message and surface any clarification."""
        system_node_buffer[node] = system_node_buffer.get(node, "") + chunk.content
        buffer = system_node_buffer[node]
        title  = SYSTEM_NODE_CONFIG[node]["title"]
        content = format_rewrite_content(buffer) if node == "rewrite_query" else buffer

        if node == "summarize_history":
            self.working_memory_summary = buffer
            self._log_event(node, "Memory Updated", f"History summarized ({len(buffer)} chars)")

        if node == "rewrite_query":
            parsed = parse_rewrite_json(buffer)
            if parsed and parsed.get("questions"):
                self.rewritten_questions = parsed.get("questions", [])
                self._log_event(node, "Query Rewritten", f"{len(self.rewritten_questions)} sub-queries generated")

        idx = find_msg_idx(response_messages, node)
        if idx is None:
            response_messages.append(make_message(content, title=title, node=node))
        else:
            response_messages[idx]["content"] = content

        if node == "rewrite_query":
            self._surface_clarification(buffer, response_messages)

    def _surface_clarification(self, buffer, response_messages):
        """If the query is unclear, add/update a plain clarification message."""
        data          = parse_rewrite_json(buffer) or {}
        clarification = data.get("clarification_needed", "")
        if not data.get("is_clear") and clarification.strip().lower() not in ("", "no"):
            self.session_metrics["clarification_needed"] = True
            self._log_event("main.rewrite_query", "Clarification Requested", clarification[:60])
            cidx = find_msg_idx(response_messages, "clarification")
            if cidx is None:
                response_messages.append(make_message(clarification, node="clarification"))
            else:
                response_messages[cidx]["content"] = clarification

    def _handle_tool_call(self, chunk, response_messages, active_tool_calls):
        """Register new tool calls as collapsible messages."""
        for tc in chunk.tool_calls:
            if tc.get("id") and tc["id"] not in active_tool_calls:
                tname = tc.get("name", "tool")
                self.session_metrics["tool_calls"] += 1
                self._log_event("agent.tools", f"Calling `{tname}`", f"Args: {str(tc.get('args', {}))[:80]}")
                response_messages.append(
                    make_message(f"Running `{tname}`...", title=f"🛠️ {tname}")
                )
                active_tool_calls[tc["id"]] = len(response_messages) - 1

    def _handle_tool_result(self, chunk, response_messages, active_tool_calls):
        """Fill in the tool result inside the matching collapsible message."""
        idx = active_tool_calls.get(chunk.tool_call_id)
        if idx is not None:
            content_str = str(chunk.content)
            self._extract_search_results(content_str, tool_name=getattr(chunk, "name", "tool") or "tool")
            self._log_event("agent.tools", "Tool Output Received", f"{len(content_str)} chars returned")
            preview = content_str[:300]
            suffix  = "\n..." if len(content_str) > 300 else ""
            response_messages[idx]["content"] = f"```\n{preview}{suffix}\n```"

    def _handle_llm_token(self, chunk, node, response_messages):
        """Append streaming LLM tokens to the last plain assistant message."""
        last = response_messages[-1] if response_messages else None
        if not (last and last.get("role") == "assistant" and "metadata" not in last):
            response_messages.append(make_message(""))
        response_messages[-1]["content"] += chunk.content

    def get_search_results_markdown(self) -> str:
        """Render the latest search results and query rewrites in clean GitHub-flavored markdown."""
        if not self.last_query:
            return (
                "### 🔍 No Search Queries Yet\n"
                "_Ask a question in the chat to see real-time hybrid search results and retrieved context here._"
            )

        md = [f"### 🔍 Search & Retrieval Results\n**Active Question:** `{self.last_query}`\n"]

        if self.rewritten_questions:
            md.append("#### 🔄 Rewritten Sub-Queries")
            for q in self.rewritten_questions:
                md.append(f"- 🔎 `{q}`")
            md.append("")

        if not self.search_results:
            md.append("\n> [!NOTE]\n> No child chunks were retrieved yet for this turn. The agent may be analyzing history or responding directly.")
        else:
            md.append(f"\n#### 📑 Retrieved Chunks ({len(self.search_results)} excerpts found)\n")
            for i, r in enumerate(self.search_results, 1):
                parent_badge = f"`{r['parent_id']}`" if r['parent_id'] != 'N/A' else "_N/A_"
                md.append(
                    f"**{i}. 📄 {r['file_name']}** | Parent ID: {parent_badge}\n"
                    f"```text\n{r['content']}\n```\n"
                )

        return "\n".join(md)

    def get_observability_markdown(self) -> str:
        """Render live agent call traces, active steps, and system diagnostics."""
        active = self.session_metrics.get("active_node", "Idle")
        status = self.session_metrics.get("status", "Ready")
        tool_count = self.session_metrics.get("tool_calls", 0)
        
        md = [
            "### 🛰️ Live Agent Execution Trace\n",
            f"**Workflow State:** `{status}` | **Active Node:** `{active}` | **Tools Invoked:** `{tool_count}`\n",
            "#### 🔄 Agent State Machine Pipeline",
            "1. `[+] main.summarize_history` — Context compaction",
            "2. `[+] main.rewrite_query` — Intent analysis & query expansion",
            "3. `[+] agent.orchestrator` — Reasoning & decision node",
            "4. `[+] agent.tools` — Hybrid Qdrant & BM25 search",
            "5. `[+] agent.compress_context` — Token optimization",
            "6. `[+] main.aggregate_answers` — Final answer synthesis\n",
            "#### 📋 Recent Execution Log (Latest First)",
        ]

        if not self.events_log:
            md.append("_No execution events recorded yet. Send a query to observe live agent calls._")
        else:
            md.append("| Time | Node | Event | Detail |")
            md.append("| :--- | :--- | :--- | :--- |")
            for ev in reversed(self.events_log[-12:]):
                detail_clean = ev['detail'].replace("|", "\\|")
                md.append(f"| `{ev['time']}` | `{ev['node']}` | **{ev['type']}** | {detail_clean} |")

        return "\n".join(md)

    def get_memory_markdown(self) -> str:
        """Render thread ID, working memory summary, and conversation state."""
        tid = self.rag_system.thread_id
        summary = self.working_memory_summary.strip() or "_No conversation summary generated yet. The agent will summarize previous turns automatically as context grows._"
        clarification = "⚠️ Clarification needed from user" if self.session_metrics.get("clarification_needed") else "✅ Query is clear"
        
        import config
        return (
            "### 🧠 Agent Memory & Session State\n\n"
            f"- **Thread ID:** `{tid}`\n"
            f"- **Dialogue Status:** {clarification}\n"
            f"- **LLM Provider:** `{getattr(config, 'LLM_PROVIDER', 'ollama')}` ({getattr(config, 'LLM_MODEL', 'qwen3.5:9b')})\n"
            f"- **Langfuse Observability:** `{'🟢 Active' if getattr(config, 'LANGFUSE_ENABLED', False) else '⚪ Disabled'}`\n\n"
            "#### 📝 Working Memory Summary\n"
            f"> {summary}\n"
        )

    def chat_stream_full(self, message, history):
        """Generator yielding (messages, search_results_md, observability_md, memory_md)."""
        if not self.rag_system.agent_graph:
            yield (
                [{"role": "assistant", "content": "⚠️ System not initialized!"}],
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )
            return

        self.last_query = message.strip()
        self.search_results = []
        self.rewritten_questions = []
        self.session_metrics["status"] = "Executing"
        self.session_metrics["clarification_needed"] = False
        self.session_metrics["queries_processed"] += 1

        self._log_event("chat.start", "Query Received", message.strip()[:60])

        config = self.rag_system.get_config()
        current_state = self.rag_system.agent_graph.get_state(config)
        log_chat_start(message.strip(), self.rag_system.thread_id, bool(current_state.next))

        try:
            if current_state.next:
                self.rag_system.agent_graph.update_state(config, {"messages": [HumanMessage(content=message.strip())]})
                stream_input = None
            else:
                stream_input = {"messages": [HumanMessage(content=message.strip())]}

            response_messages  = []
            active_tool_calls  = {}
            system_node_buffer = {}

            for chunk, metadata in self.rag_system.agent_graph.stream(stream_input, config=config, stream_mode="messages"):
                node = metadata.get("langgraph_node", "")
                if node:
                    self.session_metrics["active_node"] = node

                if node in SYSTEM_NODES and isinstance(chunk, AIMessageChunk) and chunk.content:
                    self._handle_system_node(chunk, node, response_messages, system_node_buffer)

                elif hasattr(chunk, "tool_calls") and chunk.tool_calls:
                    self._handle_tool_call(chunk, response_messages, active_tool_calls)

                elif isinstance(chunk, ToolMessage):
                    self._handle_tool_result(chunk, response_messages, active_tool_calls)

                elif isinstance(chunk, AIMessageChunk) and chunk.content and node in FINAL_RESPONSE_NODES:
                    self._handle_llm_token(chunk, node, response_messages)

                else:
                    continue

                yield (
                    response_messages,
                    self.get_search_results_markdown(),
                    self.get_observability_markdown(),
                    self.get_memory_markdown(),
                )

            final_state = self.rag_system.agent_graph.get_state(config)
            log_chat_end(getattr(final_state, "values", final_state))
            
            # Post-execution summary extraction
            if hasattr(final_state, "values") and isinstance(final_state.values, dict):
                conv_sum = final_state.values.get("conversation_summary", "")
                if conv_sum:
                    self.working_memory_summary = conv_sum

            self.session_metrics["status"] = "Completed"
            self.session_metrics["active_node"] = "Idle"
            self._log_event("chat.end", "Execution Finished", "Synthesized response delivered")

            yield (
                response_messages,
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )

        except Exception as e:
            log_error("chat", e)
            self.session_metrics["status"] = "Error"
            self.session_metrics["active_node"] = "Idle"
            self._log_event("chat.error", "Execution Failed", str(e)[:80])
            err_msg = [{"role": "assistant", "content": f"❌ Error: {str(e)}"}]
            yield (
                err_msg,
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )

    def chat(self, message, history):
        """Original generator streaming only message list for backward compatibility."""
        for messages, _, _, _ in self.chat_stream_full(message, history):
            yield messages

    def clear_session(self):
        self.rag_system.reset_thread()
        self.rag_system.observability.flush()
        self.last_query = ""
        self.search_results = []
        self.rewritten_questions = []
        self.working_memory_summary = ""
        self.events_log = []
        self.session_metrics = {
            "tool_calls": 0,
            "queries_processed": 0,
            "clarification_needed": False,
            "status": "Ready",
            "active_node": "Idle",
        }

