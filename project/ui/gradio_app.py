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
        <div style="padding: 18px; text-align: center; color: #64748b; font-size: 0.82rem; background: rgba(7, 10, 19, 0.5); border-radius: 8px;">
            📭 No documents ingested yet.<br>Drop PDF or Markdown files above to begin.
        </div>
        """
    
    rows = []
    for d in docs:
        ext = Path(d).suffix.lower()
        badge_class = "badge-pdf" if ext == ".pdf" else "badge-md"
        count = source_counts.get(d, 0)
        chunks_badge = f'<span class="badge-tag badge-chunks">{count} parents</span>' if count else ''
        
        rows.append(f"""
        <div class="doc-row">
            <div class="doc-row-title">
                <span class="badge-tag {badge_class}">{ext.replace('.', '').upper() or 'DOC'}</span>
                <span title="{d}">{d}</span>
            </div>
            {chunks_badge}
        </div>
        """)
    
    return f"""
    <div class="doc-list-scroll">
        {''.join(rows)}
    </div>
    """


def format_chunk_analytics_html(analytics: dict) -> str:
    total_docs = analytics.get("total_docs", 0)
    parent_chunks = analytics.get("parent_chunks", 0)
    child_chunks = analytics.get("child_chunks", 0)
    avg_child = analytics.get("avg_child_per_doc", 0)
    
    return f"""
    <div class="stats-grid">
        <div class="stat-card stat-card-blue">
            <div class="stat-value">{total_docs}</div>
            <div class="stat-label">Total Documents</div>
        </div>
        <div class="stat-card stat-card-purple">
            <div class="stat-value">{parent_chunks}</div>
            <div class="stat-label">Parent Chunks</div>
        </div>
        <div class="stat-card stat-card-emerald">
            <div class="stat-value">{child_chunks}</div>
            <div class="stat-label">Child Chunks (Indexed)</div>
        </div>
        <div class="stat-card stat-card-amber">
            <div class="stat-value">{avg_child}</div>
            <div class="stat-label">Avg Chunks / Doc</div>
        </div>
    </div>

    <div class="strategy-box">
        <div class="strategy-row">
            <span class="strategy-label">⚡ Chunking Strategy</span>
            <div class="strategy-content">
                <span class="badge-tag badge-chunks" style="font-size: 0.74rem;">{analytics.get('strategy', 'Hierarchical Parent-Child')}</span>
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 6px;">
            <span class="strategy-label">🧱 Parent Chunker (Contextual)</span>
            <div class="strategy-content" style="color: #cbd5e1;">
                {analytics.get('parent_type', 'Markdown Header Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 6px;">
            <span class="strategy-label">🎯 Child Chunker (Vector Retrieval)</span>
            <div class="strategy-content" style="color: #cbd5e1;">
                {analytics.get('child_type', 'Recursive Character Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 6px;">
            <span class="strategy-label">🧬 Embeddings (Hybrid Search)</span>
            <div class="strategy-content" style="font-family: 'JetBrains Mono', monospace; font-size: 0.73rem;">
                Dense: <span style="color: #38bdf8;">{analytics.get('dense_model', '')}</span><br>
                Sparse: <span style="color: #c084fc;">{analytics.get('sparse_model', '')}</span>
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

    # Premium dark theme configuration
    theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="slate",
        neutral_hue="slate",
    ).set(
        body_background_fill="#070a13",
        body_background_fill_dark="#070a13",
        block_background_fill="#0e1424",
        block_background_fill_dark="#0e1424",
        block_border_width="1px",
        block_border_color="rgba(255, 255, 255, 0.08)",
        block_border_color_dark="rgba(255, 255, 255, 0.08)",
        border_color_primary="rgba(99, 102, 241, 0.4)",
        button_primary_background_fill="linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)",
        button_primary_text_color="#ffffff",
        button_secondary_background_fill="rgba(255, 255, 255, 0.06)",
        button_secondary_text_color="#e2e8f0",
        input_background_fill="#0e1424",
        input_background_fill_dark="#0e1424",
        input_border_color="rgba(255, 255, 255, 0.12)",
    )

    with gr.Blocks(title="Srini RAG Harness Learning", fill_width=True, fill_height=True, theme=theme) as demo:
        
        # Inject custom CSS directly for 100% reliable rendering
        gr.HTML(f"<style>{custom_css}</style>")

        # --- Top Header ---
        with gr.Row(elem_id="top-header"):
            with gr.Column(scale=8):
                provider = getattr(config, 'LLM_PROVIDER', 'ollama')
                model_name = getattr(config, 'LLM_MODEL', 'qwen3.5:9b')
                gr.HTML(
                    f"""
                    <div>
                        <div class="brand-badge">⚡ PRODUCTION ARCHITECTURE</div>
                        <h1 class="main-title">Srini RAG Harness Learning</h1>
                        <p class="sub-title">Hierarchical Parent-Child Chunking • Hybrid Retrieval (Qdrant + BM25) • LangGraph Multi-Agent • Telemetry</p>
                    </div>
                    """
                )
            with gr.Column(scale=4):
                langfuse_on = getattr(config, 'LANGFUSE_ENABLED', False)
                gr.HTML(
                    f"""
                    <div style="display: flex; gap: 8px; justify-content: flex-end; align-items: center; flex-wrap: wrap; height: 100%;">
                        <span class="status-pill pill-green">
                            <span class="status-dot" style="background: #34d399;"></span> Qdrant Hybrid
                        </span>
                        <span class="status-pill pill-purple">
                            <span class="status-dot" style="background: #c084fc;"></span> {provider}:{model_name}
                        </span>
                        <span class="status-pill {'pill-blue' if langfuse_on else ''}">
                            <span class="status-dot" style="background: {'#60a5fa' if langfuse_on else '#64748b'};"></span>
                            {'Langfuse Active' if langfuse_on else 'Langfuse Off'}
                        </span>
                    </div>
                    """
                )

        # --- Main 3-Column Layout ---
        with gr.Row(elem_id="main-3-col-layout", equal_height=False):
            
            # =================================================================
            # LEFT COLUMN: Upload, Documents, Chunk Analytics
            # =================================================================
            with gr.Column(scale=3, min_width=320, elem_id="left-col"):
                
                # 1. Upload Feature
                with gr.Group():
                    gr.HTML("""
                    <div class="panel-header">
                        <h3 class="panel-header-title">📥 Upload Documents</h3>
                        <span class="panel-header-badge">PDF / MD</span>
                    </div>
                    """)
                    files_input = gr.File(
                        label="Drop PDF or Markdown files here",
                        file_count="multiple",
                        type="filepath",
                        height=100,
                        show_label=False
                    )
                    upload_btn = gr.Button("⚡ Ingest & Process Chunks", variant="primary", size="md")

                # 2. Uploaded Documents List
                with gr.Group():
                    gr.HTML("""
                    <div class="panel-header" style="margin-top: 14px;">
                        <h3 class="panel-header-title">📚 Uploaded Documents</h3>
                        <span class="panel-header-badge" style="color: #34d399; border-color: rgba(52, 211, 153, 0.3);">Knowledge Base</span>
                    </div>
                    """)
                    doc_list_display = gr.HTML(value=format_doc_list_html(initial_analytics))
                    
                    with gr.Row():
                        refresh_docs_btn = gr.Button("🔄 Refresh", variant="secondary", size="sm")
                        clear_docs_btn = gr.Button("🗑️ Clear All", variant="stop", size="sm")

                # 3. Chunking Strategy & Processed Count
                with gr.Group():
                    gr.HTML("""
                    <div class="panel-header" style="margin-top: 14px;">
                        <h3 class="panel-header-title">🧩 Chunking Strategy & Analytics</h3>
                        <span class="panel-header-badge" style="color: #60a5fa; border-color: rgba(96, 165, 250, 0.3);">Hierarchy</span>
                    </div>
                    """)
                    chunk_analytics_display = gr.HTML(value=format_chunk_analytics_html(initial_analytics))

            # =================================================================
            # MIDDLE LAYER: Chat Box & Search Results
            # =================================================================
            with gr.Column(scale=5, min_width=480, elem_id="mid-col"):
                
                gr.HTML("""
                <div class="panel-header">
                    <h3 class="panel-header-title">💬 Agent Assistant Conversation</h3>
                    <span class="panel-header-badge" style="color: #c084fc; border-color: rgba(192, 132, 252, 0.3);">Autonomous Reasoning</span>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    height=480,
                    placeholder="<strong>Ask me anything about your documents!</strong><br><em style='color: #94a3b8;'>I will analyze your query, execute hybrid search across child/parent chunks, and reason through the answer.</em>",
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
                    search_results_display = gr.HTML(
                        value=chat_interface.get_search_results_markdown(),
                        elem_id="search-results-panel"
                    )

            # =================================================================
            # RIGHT HAND SIDE: Observability of Agent Calls, Memory Calls, etc.
            # =================================================================
            with gr.Column(scale=4, min_width=340, elem_id="right-col"):
                
                gr.HTML("""
                <div class="panel-header">
                    <h3 class="panel-header-title">🛰️ Observability & Agent Traces</h3>
                    <span class="panel-header-badge" style="color: #38bdf8; border-color: rgba(56, 189, 248, 0.3);">Real-Time Diagnostics</span>
                </div>
                """)
                
                with gr.Tabs(elem_id="observability-tabs"):
                    with gr.Tab("📡 Agent Calls & Trace"):
                        observability_display = gr.HTML(
                            value=chat_interface.get_observability_markdown(),
                            elem_id="observability-panel"
                        )
                    with gr.Tab("🧠 Memory & State"):
                        memory_display = gr.HTML(
                            value=chat_interface.get_memory_markdown(),
                            elem_id="memory-panel"
                        )

                with gr.Row():
                    refresh_obs_btn = gr.Button("🔄 Refresh", variant="secondary", size="sm")
                    flush_traces_btn = gr.Button("⚡ Flush Traces", variant="secondary", size="sm")
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
                '<div style="padding: 16px; text-align: center; color: #a5b4fc; font-size: 0.88rem; background: rgba(99, 102, 241, 0.08); border: 1px dashed rgba(99, 102, 241, 0.3); border-radius: 8px;">⏳ <em>Agent analyzing query and executing hybrid retrieval across chunks...</em></div>',
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
