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
        <div class="chat-item" style="justify-content: center; text-align: center; color: #94a3b8; padding: 24px 8px;">
            <div>
                <p class="sender" style="color: #64748b; font-size: 0.82rem;">No documents uploaded</p>
                <p class="preview" style="font-size: 0.72rem;">Drop PDF or Markdown above</p>
            </div>
        </div>
        """
    
    rows = []
    for d in docs:
        ext = Path(d).suffix.lower()
        count = source_counts.get(d, 0)
        chunks_info = f"{count} parent chunks" if count else "Indexed"
        badge_text = ext.replace('.', '').upper()[:3] or "DOC"
        
        rows.append(f"""
        <div class="chat-item">
            <div class="avatar">{badge_text}</div>
            <div class="chat-item-text">
                <p class="sender" title="{d}">{d}</p>
                <p class="preview">{chunks_info} • Ready</p>
            </div>
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
        <div class="stat-card">
            <div class="stat-value">{total_docs}</div>
            <div class="stat-label">Total Docs</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{parent_chunks}</div>
            <div class="stat-label">Parents</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{child_chunks}</div>
            <div class="stat-label">Children</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{avg_child}</div>
            <div class="stat-label">Avg / Doc</div>
        </div>
    </div>

    <div class="strategy-box">
        <div class="strategy-row">
            <span class="strategy-label">Strategy</span>
            <div class="strategy-content">
                <span class="badge-tag badge-chunks">{analytics.get('strategy', 'Hierarchical Parent-Child')}</span>
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Parent Chunker</span>
            <div class="strategy-content">
                {analytics.get('parent_type', 'Markdown Header Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Child Chunker</span>
            <div class="strategy-content">
                {analytics.get('child_type', 'Recursive Character Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Embeddings</span>
            <div class="strategy-content" style="font-family: -apple-system, monospace; font-size: 0.70rem;">
                Dense: <span style="color: #4C426D; font-weight: 600;">{analytics.get('dense_model', '')}</span><br>
                Sparse: <span style="color: #64748b;">{analytics.get('sparse_model', '')}</span>
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

    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="slate",
        neutral_hue="slate",
    ).set(
        body_background_fill="#ffffff",
        body_background_fill_dark="#ffffff",
        block_background_fill="#ffffff",
        block_background_fill_dark="#ffffff",
        block_border_width="1px",
        block_border_color="#edf2f7",
        button_primary_background_fill="#4C426D",
        button_primary_background_fill_hover="#3b3256",
        button_primary_text_color="#ffffff",
        button_secondary_background_fill="#F6F7FB",
        button_secondary_text_color="#1e293b",
        input_background_fill="#ffffff",
        input_background_fill_dark="#ffffff",
    )

    with gr.Blocks(title="Srini RAG Harness Learning", fill_width=True, fill_height=True, theme=theme) as demo:

        # =====================================================================
        # TOP APP HEADER BAR (Fixed 56px height)
        # =====================================================================
        with gr.Row(elem_id="app-header"):
            provider = getattr(config, 'LLM_PROVIDER', 'ollama')
            model_name = getattr(config, 'LLM_MODEL', 'qwen3.5:9b')
            langfuse_on = getattr(config, 'LANGFUSE_ENABLED', False)

            gr.HTML(
                f"""
                <div class="app-brand">
                    <span class="app-brand-badge">PROD</span>
                    <h1 class="app-brand-title">⚡ Srini RAG Harness Learning</h1>
                </div>
                <div class="app-status-bar">
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

        # =====================================================================
        # MAIN 3-COLUMN SEAMLESS CONTAINER (height: calc(100vh - 56px))
        # =====================================================================
        with gr.Row(elem_id="app-3-columns", equal_height=True):
            
            # -----------------------------------------------------------------
            # COLUMN 1: LEFT SIDEBAR (DOCUMENTS & CHUNKS)
            # -----------------------------------------------------------------
            with gr.Column(scale=3, min_width=280, elem_id="col-sidebar"):
                
                # 1. Upload Feature
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title">
                        <span>📥 Ingest Documents</span>
                        <span style="font-size: 0.68rem; color: #64748b;">PDF / MD</span>
                    </div>
                    """)
                    files_input = gr.File(
                        label="Drop PDF or Markdown files",
                        file_count="multiple",
                        type="filepath",
                        height=90,
                        show_label=False
                    )
                    upload_btn = gr.Button("⚡ Ingest & Process Chunks", variant="primary", size="sm")

                # 2. Uploaded Documents List
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title" style="margin-top: 10px;">
                        <span>📚 Knowledge Base Docs</span>
                        <span style="color: #34d399; font-size: 0.68rem;">Live</span>
                    </div>
                    """)
                    doc_list_display = gr.HTML(value=format_doc_list_html(initial_analytics))
                    
                    with gr.Row():
                        refresh_docs_btn = gr.Button("🔄 Refresh", variant="secondary", size="sm")
                        clear_docs_btn = gr.Button("🗑️ Clear All", variant="stop", size="sm")

                # 3. Chunking Strategy & Processed Count
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title" style="margin-top: 10px;">
                        <span>🧩 Chunk Strategy & Stats</span>
                        <span style="color: #60a5fa; font-size: 0.68rem;">Hierarchy</span>
                    </div>
                    """)
                    chunk_analytics_display = gr.HTML(value=format_chunk_analytics_html(initial_analytics))

            # -----------------------------------------------------------------
            # COLUMN 2: MIDDLE MAIN CHAT & RETRIEVED SEARCH RESULTS
            # -----------------------------------------------------------------
            with gr.Column(scale=6, min_width=460, elem_id="col-chat"):
                
                gr.HTML("""
                <div class="chat-column-header">
                    <span style="font-weight: 700; font-size: 0.88rem; color: #1e293b; display: flex; align-items: center; gap: 6px;">
                        Conversation & Agent Reasoning
                    </span>
                    <span style="font-size: 0.72rem; color: #4C426D; background: rgba(76, 66, 109, 0.08); padding: 2px 8px; border-radius: 4px; font-weight: 600;">
                        Hybrid Qdrant + BM25
                    </span>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    placeholder="<strong>Ask anything about your ingested documents!</strong><br><span style='color: #64748b;'>The agent will analyze the query, execute hybrid retrieval, and synthesize an answer.</span>",
                    show_label=False,
                    avatar_images=(None, BOT_AVATAR),
                    layout="bubble",
                )

                # Search Results Drawer directly in the middle column
                with gr.Accordion("🔍 Retrieved Search Results & Excerpts", open=False, elem_id="search-accordion"):
                    search_results_display = gr.HTML(
                        value=chat_interface.get_search_results_markdown(),
                        elem_id="search-results-panel"
                    )

                with gr.Row(elem_id="chat-input-row"):
                    msg_input = gr.Textbox(
                        placeholder="Type a message or question...",
                        show_label=False,
                        scale=8,
                        elem_id="chat-input-box",
                        container=False,
                        autofocus=False
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=2, min_width=75)
                    clear_chat_btn = gr.Button("🧹 Clear", variant="secondary", scale=1, min_width=65)

            # -----------------------------------------------------------------
            # COLUMN 3: RIGHT INSPECTOR PANEL (OBSERVABILITY & MEMORY)
            # -----------------------------------------------------------------
            with gr.Column(scale=3, min_width=290, elem_id="col-inspector"):
                
                gr.HTML(
                    f"""
                    <div class="inspector-profile">
                        <div class="info-avatar">🤖</div>
                        <p class="info-name">Srini RAG Agent</p>
                        <p class="info-description">
                            Hierarchical hybrid retrieval agent with LangGraph pipeline orchestration, Qdrant vector memory, and {provider}:{model_name} reasoning.
                        </p>
                    </div>
                    """
                )
                
                with gr.Tabs(elem_id="observability-tabs"):
                    with gr.Tab("📡 Agent Traces"):
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
                    reset_session_btn = gr.Button("🗑️ Reset Session", variant="stop", size="sm")

        # =====================================================================
        # EVENT HANDLERS & WIRING
        # =====================================================================
        
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
                gr.Info("🗑️ Cleared all documents and vector chunks")
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

            user_msg = {"role": "user", "content": msg_str}
            current_history = history + [user_msg]
            
            yield (
                "",
                current_history,
                '<div style="padding: 12px; text-align: center; color: #a5b4fc; font-size: 0.82rem; background: rgba(99, 102, 241, 0.08); border-radius: 6px;">⏳ <em>Agent analyzing query and executing hybrid retrieval...</em></div>',
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
