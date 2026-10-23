import os
from pathlib import Path
import gradio as gr
from core.chat_interface import ChatInterface
from core.document_manager import DocumentManager
from core.rag_system import RAGSystem
from ui.css import custom_css
import config

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
AVATAR_PATH = os.path.join(ASSETS_DIR, "chatbot_avatar.png")
BOT_AVATAR = AVATAR_PATH if os.path.exists(AVATAR_PATH) else None


def format_doc_list_html(analytics: dict) -> str:
    docs = analytics.get("doc_list", [])
    source_counts = analytics.get("source_counts", {})
    if not docs:
        return """
        <div style="padding: 16px; text-align: center; color: #64748b; font-size: 0.85rem;">
            📭 No documents in knowledge base.<br>Upload PDF or Markdown files above to begin.
        </div>
        """
    
    items = []
    for d in docs:
        count = source_counts.get(d, 0)
        count_badge = f'<span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 2px 6px; border-radius: 4px; font-size: 0.72rem; font-weight: 600;">{count} parents</span>' if count else ''
        items.append(f"""
        <div class="doc-item-pill">
            <span style="display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                📄 <strong style="color: #e2e8f0;">{d}</strong>
            </span>
            {count_badge}
        </div>
        """)
    
    return f"""
    <div class="doc-list-container">
        {''.join(items)}
    </div>
    """


def format_chunk_analytics_html(analytics: dict) -> str:
    total_docs = analytics.get("total_docs", 0)
    parent_chunks = analytics.get("parent_chunks", 0)
    child_chunks = analytics.get("child_chunks", 0)
    avg_child = analytics.get("avg_child_per_doc", 0)
    
    return f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-num">{total_docs}</div>
            <div class="metric-label">Total Documents</div>
        </div>
        <div class="metric-card">
            <div class="metric-num" style="color: #a78bfa;">{parent_chunks}</div>
            <div class="metric-label">Parent Chunks</div>
        </div>
        <div class="metric-card">
            <div class="metric-num" style="color: #34d399;">{child_chunks}</div>
            <div class="metric-label">Child Chunks (Indexed)</div>
        </div>
        <div class="metric-card">
            <div class="metric-num" style="color: #f59e0b;">{avg_child}</div>
            <div class="metric-label">Avg Chunks / Doc</div>
        </div>
    </div>

    <div class="chunk-info-card">
        <div class="chunk-info-item">
            <span class="chunk-info-title">Chunking Strategy</span>
            <span class="chunk-info-badge">{analytics.get('strategy', 'Hierarchical Parent-Child')}</span>
        </div>
        <div class="chunk-info-item" style="margin-top: 6px;">
            <span class="chunk-info-title">Parent Chunker (Contextual)</span>
            <div style="font-size: 0.76rem; color: #94a3b8; margin-top: 2px;">
                {analytics.get('parent_type', 'Markdown Header Splitter')}
            </div>
        </div>
        <div class="chunk-info-item" style="margin-top: 6px;">
            <span class="chunk-info-title">Child Chunker (Vector Retrieval)</span>
            <div style="font-size: 0.76rem; color: #94a3b8; margin-top: 2px;">
                {analytics.get('child_type', 'Recursive Character Splitter')}
            </div>
        </div>
        <div class="chunk-info-item" style="margin-top: 6px;">
            <span class="chunk-info-title">Embeddings (Hybrid)</span>
            <div style="font-size: 0.74rem; color: #94a3b8; font-family: monospace; margin-top: 2px;">
                Dense: <span style="color: #38bdf8;">{analytics.get('dense_model', '')}</span><br>
                Sparse: <span style="color: #f472b6;">{analytics.get('sparse_model', '')}</span>
            </div>
        </div>
    </div>
    """


def create_gradio_ui():
    rag_system = RAGSystem()
    rag_system.initialize()
    
    doc_manager = DocumentManager(rag_system)
    chat_interface = ChatInterface(rag_system)
    
    initial_analytics = doc_manager.get_chunk_analytics()

    with gr.Blocks(title="Srini RAG Harness Learning", fill_height=True) as demo:
        
        # --- Top Header ---
        with gr.Row(elem_id="top-header"):
            with gr.Column(scale=8):
                gr.Markdown(
                    """
                    # ⚡ Srini RAG Harness Learning
                    **Hybrid Retrieval (Dense + BM25) • Hierarchical Chunking • LangGraph Multi-Agent • Full Observability**
                    """
                )
            with gr.Column(scale=4, elem_classes=["status-badge-container"]):
                provider = getattr(config, 'LLM_PROVIDER', 'ollama')
                model_name = getattr(config, 'LLM_MODEL', 'qwen3.5:9b')
                langfuse_on = getattr(config, 'LANGFUSE_ENABLED', False)
                gr.HTML(
                    f"""
                    <div style="display: flex; gap: 8px; justify-content: flex-end; flex-wrap: wrap;">
                        <span class="status-pill pill-green">🟢 Qdrant Hybrid DB</span>
                        <span class="status-pill pill-purple">🤖 {provider}: {model_name}</span>
                        <span class="status-pill {'pill-blue' if langfuse_on else ''}">
                            {'🟢 Langfuse Connected' if langfuse_on else '⚪ Langfuse Off'}
                        </span>
                    </div>
                    """
                )

        # --- Main 3-Column Layout ---
        with gr.Row(elem_id="main-3-col-layout", equal_height=False):
            
            # =================================================================
            # LEFT COLUMN: Upload, Document List, Chunk Type & Processed Count
            # =================================================================
            with gr.Column(scale=3, min_width=320, elem_id="left-col"):
                
                # 1. Upload Feature
                with gr.Group():
                    gr.HTML("""
                    <div class="column-header">
                        <h3>📥 Upload Documents</h3>
                        <span style="font-size: 0.74rem; color: #94a3b8;">PDF / Markdown</span>
                    </div>
                    """)
                    files_input = gr.File(
                        label="Drop PDF or Markdown files here",
                        file_count="multiple",
                        type="filepath",
                        height=120,
                        show_label=False
                    )
                    upload_btn = gr.Button("⚡ Ingest & Process Chunks", variant="primary", size="md")

                # 2. Uploaded Documents List
                with gr.Group():
                    gr.HTML("""
                    <div class="column-header" style="margin-top: 14px;">
                        <h3>📚 Uploaded Documents</h3>
                        <span style="font-size: 0.74rem; color: #34d399;">Knowledge Base</span>
                    </div>
                    """)
                    doc_list_display = gr.HTML(value=format_doc_list_html(initial_analytics))
                    
                    with gr.Row():
                        refresh_docs_btn = gr.Button("🔄 Refresh", size="sm")
                        clear_docs_btn = gr.Button("🗑️ Clear All", variant="stop", size="sm")

                # 3. Type of Chunk Used & How Many Chunks Processed
                with gr.Group():
                    gr.HTML("""
                    <div class="column-header" style="margin-top: 14px;">
                        <h3>🧩 Chunking Strategy & Analytics</h3>
                        <span style="font-size: 0.74rem; color: #60a5fa;">Hierarchy</span>
                    </div>
                    """)
                    chunk_analytics_display = gr.HTML(value=format_chunk_analytics_html(initial_analytics))

            # =================================================================
            # MIDDLE LAYER: Chat Box & Search Results
            # =================================================================
            with gr.Column(scale=5, min_width=480, elem_id="mid-col"):
                
                gr.HTML("""
                <div class="column-header">
                    <h3>💬 RAG Assistant Chat</h3>
                    <span style="font-size: 0.74rem; color: #a78bfa;">Interactive Reasoning</span>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    height=500,
                    placeholder="<strong>Ask me anything!</strong><br><em>I will analyze your query, execute hybrid search across child/parent chunks, and reason through the answer.</em>",
                    show_label=False,
                    avatar_images=(None, BOT_AVATAR),
                    layout="bubble",
                )

                with gr.Row(elem_id="chat-input-row"):
                    msg_input = gr.Textbox(
                        placeholder="Ask a question about your documents...",
                        show_label=False,
                        scale=8,
                        elem_id="chat-input-box",
                        container=False,
                        autofocus=True
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=2, min_width=80)
                    clear_chat_btn = gr.Button("🧹 Clear", variant="secondary", scale=1, min_width=70)

                # Middle Layer: Search Results section directly below the chat
                with gr.Accordion("🔍 Retrieved Search Results & Excerpts", open=True, elem_id="search-accordion"):
                    search_results_display = gr.Markdown(
                        value=chat_interface.get_search_results_markdown(),
                        elem_id="search-results-panel"
                    )

            # =================================================================
            # RIGHT HAND SIDE: Observability of Agent Calls, Memory Calls, etc.
            # =================================================================
            with gr.Column(scale=4, min_width=340, elem_id="right-col"):
                
                gr.HTML("""
                <div class="column-header">
                    <h3>🛰️ Observability & Agent Traces</h3>
                    <span style="font-size: 0.74rem; color: #38bdf8;">Real-Time Diagnostics</span>
                </div>
                """)
                
                with gr.Tabs(elem_id="observability-tabs"):
                    with gr.Tab("📡 Agent Calls & Trace"):
                        observability_display = gr.Markdown(
                            value=chat_interface.get_observability_markdown(),
                            elem_id="observability-panel"
                        )
                    with gr.Tab("🧠 Memory & State"):
                        memory_display = gr.Markdown(
                            value=chat_interface.get_memory_markdown(),
                            elem_id="memory-panel"
                        )

                with gr.Row():
                    refresh_obs_btn = gr.Button("🔄 Refresh Observability", size="sm")
                    flush_traces_btn = gr.Button("⚡ Flush Traces", size="sm")
                    reset_session_btn = gr.Button("🗑️ Reset Thread", variant="stop", size="sm")

        # =====================================================================
        # EVENT HANDLERS & WIRING
        # =====================================================================
        
        # --- Document Upload & Management Handlers ---
        def upload_handler(files, progress=gr.Progress()):
            if not files:
                analytics = doc_manager.get_chunk_analytics()
                return None, format_doc_list_html(analytics), format_chunk_analytics_html(analytics)
                
            added, skipped = doc_manager.add_documents(
                files, 
                progress_callback=lambda p, desc: progress(p, desc=desc)
            )
            gr.Info(f"✅ Ingested: {added} new documents | Skipped: {skipped}")
            analytics = doc_manager.get_chunk_analytics()
            return None, format_doc_list_html(analytics), format_chunk_analytics_html(analytics)

        def refresh_docs_handler():
            analytics = doc_manager.get_chunk_analytics()
            return format_doc_list_html(analytics), format_chunk_analytics_html(analytics)

        def clear_docs_handler():
            try:
                doc_manager.clear_all()
                gr.Info("🗑️ Removed all documents & cleared vector chunks")
            except Exception as exc:
                gr.Error(f"Unable to clear documents: {exc}")
            analytics = doc_manager.get_chunk_analytics()
            return format_doc_list_html(analytics), format_chunk_analytics_html(analytics)

        upload_btn.click(
            upload_handler,
            inputs=[files_input],
            outputs=[files_input, doc_list_display, chunk_analytics_display],
            show_progress="corner"
        )
        refresh_docs_btn.click(
            refresh_docs_handler,
            inputs=None,
            outputs=[doc_list_display, chunk_analytics_display]
        )
        clear_docs_btn.click(
            clear_docs_handler,
            inputs=None,
            outputs=[doc_list_display, chunk_analytics_display]
        )

        # --- Chat & Real-Time Observability Streaming ---
        def user_submit(message, history):
            msg_str = (message or "").strip()
            if not msg_str:
                yield (
                    "",
                    history,
                    chat_interface.get_search_results_markdown(),
                    chat_interface.get_observability_markdown(),
                    chat_interface.get_memory_markdown(),
                )
                return

            # Append user message
            user_msg = {"role": "user", "content": msg_str}
            current_history = history + [user_msg]
            
            yield (
                "",
                current_history,
                "⏳ *Agent analyzing query and executing hybrid retrieval...*",
                chat_interface.get_observability_markdown(),
                chat_interface.get_memory_markdown(),
            )

            for (
                resp_messages,
                search_md,
                obs_md,
                mem_md,
            ) in chat_interface.chat_stream_full(msg_str, history):
                full_history = current_history + resp_messages
                yield (
                    "",
                    full_history,
                    search_md,
                    obs_md,
                    mem_md,
                )

        def clear_chat_handler():
            chat_interface.clear_session()
            gr.Info("🧹 Session & memory reset")
            return (
                [],
                chat_interface.get_search_results_markdown(),
                chat_interface.get_observability_markdown(),
                chat_interface.get_memory_markdown(),
            )

        def refresh_observability_handler():
            return (
                chat_interface.get_search_results_markdown(),
                chat_interface.get_observability_markdown(),
                chat_interface.get_memory_markdown(),
            )

        def flush_traces_handler():
            rag_system.observability.flush()
            gr.Info("⚡ Langfuse traces flushed")
            return chat_interface.get_observability_markdown()

        # Connect Chat Inputs
        submit_event = msg_input.submit(
            user_submit,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot, search_results_display, observability_display, memory_display]
        )
        send_btn.click(
            user_submit,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot, search_results_display, observability_display, memory_display]
        )
        clear_chat_btn.click(
            clear_chat_handler,
            inputs=None,
            outputs=[chatbot, search_results_display, observability_display, memory_display]
        )
        
        # Connect Observability buttons
        refresh_obs_btn.click(
            refresh_observability_handler,
            inputs=None,
            outputs=[search_results_display, observability_display, memory_display]
        )
        flush_traces_btn.click(
            flush_traces_handler,
            inputs=None,
            outputs=[observability_display]
        )
        reset_session_btn.click(
            clear_chat_handler,
            inputs=None,
            outputs=[chatbot, search_results_display, observability_display, memory_display]
        )

    return demo
