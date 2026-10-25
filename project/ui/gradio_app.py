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
        <div class="chat-item" style="justify-content: center; text-align: center; color: var(--ink-muted); padding: 18px 8px;">
            <div>
                <p class="sender" style="color: var(--ink-secondary); font-size: 0.78rem;">No documents uploaded</p>
                <p class="preview" style="font-size: 0.68rem;">Drop PDF or Markdown files above</p>
            </div>
        </div>
        """
    
    rows = []
    for d in docs:
        ext = Path(d).suffix.lower()
        count = source_counts.get(d, 0)
        chunks_info = f"{count} parents" if count else "Indexed"
        badge_cls = "pdf" if "pdf" in ext else ("md" if "md" in ext else "")
        badge_text = ext.replace('.', '').upper()[:3] or "DOC"
        
        rows.append(f"""
        <div class="chat-item">
            <div class="avatar {badge_cls}">{badge_text}</div>
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
            <div class="stat-label">Total docs</div>
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
            <div class="stat-label">Avg / doc</div>
        </div>
    </div>

    <div class="strategy-box">
        <div class="strategy-row">
            <span class="strategy-label">Chunk strategy</span>
            <div class="strategy-content">
                <span class="badge-tag badge-chunks">{analytics.get('strategy', 'Hierarchical Parent-Child')}</span>
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Parent chunker</span>
            <div class="strategy-content">
                {analytics.get('parent_type', 'Markdown Header Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Child chunker</span>
            <div class="strategy-content">
                {analytics.get('child_type', 'Recursive Character Splitter')}
            </div>
        </div>
        <div class="strategy-row" style="margin-top: 4px;">
            <span class="strategy-label">Embedding models</span>
            <div class="strategy-content" style="font-family: var(--font-mono); font-size: 0.68rem;">
                Dense: <span style="color: var(--brand-primary); font-weight: 600;">{analytics.get('dense_model', '')}</span><br>
                Sparse: <span style="color: var(--ink-muted);">{analytics.get('sparse_model', '')}</span>
            </div>
        </div>
    </div>
    """


SPLITTER_JS = """
() => {
    function setupSplitters() {
        const leftCol = document.getElementById('col-sidebar');
        const midCol = document.getElementById('col-chat');
        const rightCol = document.getElementById('col-inspector');
        if (!leftCol || !midCol || !rightCol) {
            setTimeout(setupSplitters, 200);
            return;
        }

        const sliderLeftInput = document.querySelector('#slider-left input[type="range"]');
        const sliderRightInput = document.querySelector('#slider-right input[type="range"]');

        // Direct Range input listeners for buttery-smooth instant column resizing
        if (sliderLeftInput && !sliderLeftInput.dataset.bound) {
            sliderLeftInput.dataset.bound = 'true';
            sliderLeftInput.addEventListener('input', (e) => {
                const val = e.target.value;
                leftCol.style.setProperty('flex', `0 0 ${val}px`, 'important');
                leftCol.style.setProperty('max-width', `${val}px`, 'important');
                leftCol.style.setProperty('min-width', `${val}px`, 'important');
                leftCol.style.setProperty('width', `${val}px`, 'important');
                const badge = document.getElementById('left-col-val');
                if (badge) badge.textContent = `${val}px`;
            });
        }

        if (sliderRightInput && !sliderRightInput.dataset.bound) {
            sliderRightInput.dataset.bound = 'true';
            sliderRightInput.addEventListener('input', (e) => {
                const val = e.target.value;
                rightCol.style.setProperty('flex', `0 0 ${val}px`, 'important');
                rightCol.style.setProperty('max-width', `${val}px`, 'important');
                rightCol.style.setProperty('min-width', `${val}px`, 'important');
                rightCol.style.setProperty('width', `${val}px`, 'important');
                const badge = document.getElementById('right-col-val');
                if (badge) badge.textContent = `${val}px`;
            });
        }
        
        // Draggable vertical divider 1 (Left sidebar <-> Center chat)
        if (!document.getElementById('splitter-left')) {
            const splitL = document.createElement('div');
            splitL.id = 'splitter-left';
            splitL.className = 'col-splitter';
            splitL.title = 'Drag to resize Left Column';
            leftCol.parentNode.insertBefore(splitL, midCol);

            let isDraggingL = false;
            splitL.addEventListener('mousedown', (e) => {
                isDraggingL = true;
                document.body.style.cursor = 'col-resize';
                document.body.style.userSelect = 'none';
            });
            document.addEventListener('mousemove', (e) => {
                if (!isDraggingL) return;
                const newWidth = Math.max(180, Math.min(520, e.clientX));
                leftCol.style.setProperty('flex', `0 0 ${newWidth}px`, 'important');
                leftCol.style.setProperty('max-width', `${newWidth}px`, 'important');
                leftCol.style.setProperty('min-width', `${newWidth}px`, 'important');
                leftCol.style.setProperty('width', `${newWidth}px`, 'important');
                if (sliderLeftInput) sliderLeftInput.value = newWidth;
                const badge = document.getElementById('left-col-val');
                if (badge) badge.textContent = `${newWidth}px`;
            });
            document.addEventListener('mouseup', () => {
                if (isDraggingL) {
                    isDraggingL = false;
                    document.body.style.cursor = '';
                    document.body.style.userSelect = '';
                }
            });
        }

        // Draggable vertical divider 2 (Center chat <-> Right inspector)
        if (!document.getElementById('splitter-right')) {
            const splitR = document.createElement('div');
            splitR.id = 'splitter-right';
            splitR.className = 'col-splitter';
            splitR.title = 'Drag to resize Right Column';
            midCol.parentNode.insertBefore(splitR, rightCol);

            let isDraggingR = false;
            splitR.addEventListener('mousedown', (e) => {
                isDraggingR = true;
                document.body.style.cursor = 'col-resize';
                document.body.style.userSelect = 'none';
            });
            document.addEventListener('mousemove', (e) => {
                if (!isDraggingR) return;
                const newWidth = Math.max(220, Math.min(580, window.innerWidth - e.clientX));
                rightCol.style.setProperty('flex', `0 0 ${newWidth}px`, 'important');
                rightCol.style.setProperty('max-width', `${newWidth}px`, 'important');
                rightCol.style.setProperty('min-width', `${newWidth}px`, 'important');
                rightCol.style.setProperty('width', `${newWidth}px`, 'important');
                if (sliderRightInput) sliderRightInput.value = newWidth;
                const badge = document.getElementById('right-col-val');
                if (badge) badge.textContent = `${newWidth}px`;
            });
            document.addEventListener('mouseup', () => {
                if (isDraggingR) {
                    isDraggingR = false;
                    document.body.style.cursor = '';
                    document.body.style.userSelect = '';
                }
            });
        }
    }
    setupSplitters();
}
"""


def create_gradio_ui():
    rag_system = RAGSystem()
    rag_system.initialize()
    
    doc_manager = DocumentManager(rag_system)
    chat_interface = ChatInterface(rag_system)
    
    initial_analytics = doc_manager.get_chunk_analytics()

    theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="slate",
        neutral_hue="slate",
    ).set(
        body_background_fill="#F8FAFC",
        body_background_fill_dark="#F8FAFC",
        block_background_fill="#FFFFFF",
        block_background_fill_dark="#FFFFFF",
        block_border_width="1px",
        block_border_color="#E2E8F0",
        button_primary_background_fill="#4F46E5",
        button_primary_background_fill_hover="#4338CA",
        button_primary_text_color="#FFFFFF",
        button_secondary_background_fill="#FFFFFF",
        button_secondary_text_color="#0F172A",
        input_background_fill="#FFFFFF",
        input_background_fill_dark="#FFFFFF",
    )

    with gr.Blocks(title="Srini RAG Harness Learning", fill_width=True, fill_height=True) as demo:

        # =====================================================================
        # TOP APP HEADER BAR (Fixed 46px height, Precision Instrument Header)
        # =====================================================================
        with gr.Row(elem_id="app-header"):
            provider = getattr(config, 'LLM_PROVIDER', 'ollama')
            model_name = getattr(config, 'LLM_MODEL', 'qwen3.5:9b')
            langfuse_on = getattr(config, 'LANGFUSE_ENABLED', False)

            gr.HTML(
                """
                <div class="app-brand">
                    <span class="app-brand-logo">⚡</span>
                    <div class="app-brand-text">
                        <span class="app-brand-title">Srini RAG Harness</span>
                        <span class="app-brand-version">v2.4 • Agentic Workbench</span>
                    </div>
                </div>
                """
            )

            gr.HTML(
                f"""
                <div class="app-status-bar">
                    <span class="status-pill pill-green">
                        <span class="status-dot pulse" style="background: #059669;"></span> Qdrant Live
                    </span>
                    <span class="status-pill pill-purple">
                        {provider}:{model_name}
                    </span>
                    <span class="status-pill {'pill-blue' if langfuse_on else ''}">
                        <span class="status-dot" style="background: {'#2563EB' if langfuse_on else '#94a3b8'};"></span>
                        {'Langfuse Active' if langfuse_on else 'No Tracing'}
                    </span>
                </div>
                """
            )

        # =====================================================================
        # MAIN 3-COLUMN SEAMLESS CONTAINER (height: calc(100vh - 46px))
        # =====================================================================
        with gr.Row(elem_id="app-3-columns", equal_height=True):
            
            # -----------------------------------------------------------------
            # COLUMN 1: LEFT SIDEBAR (KNOWLEDGE BASE & CHUNKING)
            # -----------------------------------------------------------------
            with gr.Column(scale=3, min_width=180, elem_id="col-sidebar"):
                
                # Low-profile Column Width Slider
                with gr.Group(elem_id="sidebar-width-control"):
                    gr.HTML('<div class="col-slider-label"><span>Column width</span><span id="left-col-val" class="col-slider-val">290px</span></div>')
                    left_slider = gr.Slider(
                        minimum=180,
                        maximum=520,
                        value=290,
                        step=10,
                        show_label=False,
                        container=False,
                        elem_id="slider-left"
                    )

                # 1. Ingest Documents
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title">
                        <span>📥 Ingest documents</span>
                        <span class="sidebar-badge">PDF / MD</span>
                    </div>
                    """)
                    files_input = gr.File(
                        label="Drop PDF or Markdown files",
                        file_count="multiple",
                        type="filepath",
                        height=76,
                        show_label=False
                    )
                    upload_btn = gr.Button("⚡ Ingest & Process Chunks", variant="primary", size="sm")

                # 2. Indexed Documents List
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title" style="margin-top: 8px;">
                        <span>📚 Indexed documents</span>
                        <span class="sidebar-badge live">Live</span>
                    </div>
                    """)
                    doc_list_display = gr.HTML(value=format_doc_list_html(initial_analytics))
                    
                    with gr.Row():
                        refresh_docs_btn = gr.Button("🔄 Refresh", variant="secondary", size="sm")
                        clear_docs_btn = gr.Button("🗑️ Clear All", variant="stop", size="sm")

                # 3. Chunking Strategy & Processed Count
                with gr.Group():
                    gr.HTML("""
                    <div class="sidebar-section-title" style="margin-top: 8px;">
                        <span>🧩 Chunk strategy & metrics</span>
                        <span class="sidebar-badge">Hierarchy</span>
                    </div>
                    """)
                    chunk_analytics_display = gr.HTML(value=format_chunk_analytics_html(initial_analytics))

            # -----------------------------------------------------------------
            # COLUMN 2: MIDDLE MAIN CHAT & RETRIEVED SEARCH RESULTS
            # -----------------------------------------------------------------
            with gr.Column(scale=6, min_width=440, elem_id="col-chat"):
                
                gr.HTML("""
                <div class="chat-column-header">
                    <span style="font-weight: 700; font-size: 0.84rem; color: var(--ink-primary); display: flex; align-items: center; gap: 6px;">
                        Conversation & agent reasoning
                    </span>
                    <span style="font-size: 0.70rem; color: var(--brand-primary); background: var(--brand-light); border: 1px solid var(--brand-border); padding: 2px 7px; border-radius: 4px; font-weight: 600; font-family: var(--font-mono);">
                        Hybrid Qdrant + BM25
                    </span>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    placeholder="<strong>Ask anything about your ingested documents!</strong><br><span style='color: var(--ink-muted);'>The agent analyzes queries, executes hybrid retrieval across hierarchical parent/child chunks, and synthesizes answers.</span>",
                    show_label=False,
                    avatar_images=(None, BOT_AVATAR),
                    layout="bubble",
                )

                # Search Results Drawer directly in the middle column
                with gr.Accordion("🔍 Retrieved search excerpts", open=False, elem_id="search-accordion"):
                    search_results_display = gr.HTML(
                        value=chat_interface.get_search_results_markdown(),
                        elem_id="search-results-panel"
                    )

                # Quick Starter Prompts Row
                with gr.Row(elem_id="quick-prompts-row"):
                    quick_1 = gr.Button("💡 What are the key concepts in 137notes?", variant="secondary", size="sm", elem_classes=["quick-prompt-btn"])
                    quick_2 = gr.Button("⚡ Compare notes 217a & 217c", variant="secondary", size="sm", elem_classes=["quick-prompt-btn"])
                    quick_3 = gr.Button("🔬 Explain retrieval & chunk hierarchy", variant="secondary", size="sm", elem_classes=["quick-prompt-btn"])

                with gr.Row(elem_id="chat-input-row"):
                    msg_input = gr.Textbox(
                        placeholder="Type a message or question...",
                        show_label=False,
                        scale=8,
                        elem_id="chat-input-box",
                        container=False,
                        autofocus=False
                    )
                    send_btn = gr.Button("Send ↵", variant="primary", scale=2, min_width=75)
                    clear_chat_btn = gr.Button("🧹 Clear", variant="secondary", scale=1, min_width=65)

            # -----------------------------------------------------------------
            # COLUMN 3: RIGHT INSPECTOR PANEL (AGENT TRACES & STATE)
            # -----------------------------------------------------------------
            with gr.Column(scale=3, min_width=240, elem_id="col-inspector"):
                
                gr.HTML(
                    f"""
                    <div class="compact-agent-header">
                        <div class="compact-agent-left">
                            <span class="compact-avatar">🤖</span>
                            <span class="compact-title">Srini RAG Agent</span>
                        </div>
                        <span class="compact-badge">{provider}:{model_name}</span>
                    </div>
                    """
                )

                # Low-profile Column Width Slider
                with gr.Group(elem_id="inspector-width-control"):
                    gr.HTML('<div class="col-slider-label"><span>Column width</span><span id="right-col-val" class="col-slider-val">320px</span></div>')
                    right_slider = gr.Slider(
                        minimum=220,
                        maximum=580,
                        value=320,
                        step=10,
                        show_label=False,
                        container=False,
                        elem_id="slider-right"
                    )
                
                with gr.Tabs(elem_id="observability-tabs"):
                    with gr.Tab("📡 Agent traces"):
                        observability_display = gr.HTML(
                            value=chat_interface.get_observability_markdown(),
                            elem_id="observability-panel"
                        )
                    with gr.Tab("🧠 Memory & state"):
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

        # Quick Starter Prompt Buttons
        quick_1.click(lambda: "What are the key concepts in 137notes?", outputs=[msg_input])
        quick_2.click(lambda: "Compare notes 217a and 217c", outputs=[msg_input])
        quick_3.click(lambda: "Explain the hierarchical retrieval pipeline and chunking strategy", outputs=[msg_input])
        
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

        # Real-time column resizing via Sliders
        left_resize_js = """(val) => {
            const col = document.getElementById('col-sidebar');
            if (col) {
                col.style.setProperty('flex', `0 0 ${val}px`, 'important');
                col.style.setProperty('max-width', `${val}px`, 'important');
                col.style.setProperty('min-width', `${val}px`, 'important');
                col.style.setProperty('width', `${val}px`, 'important');
            }
            const badge = document.getElementById('left-col-val');
            if (badge) badge.textContent = `${val}px`;
        }"""
        right_resize_js = """(val) => {
            const col = document.getElementById('col-inspector');
            if (col) {
                col.style.setProperty('flex', `0 0 ${val}px`, 'important');
                col.style.setProperty('max-width', `${val}px`, 'important');
                col.style.setProperty('min-width', `${val}px`, 'important');
                col.style.setProperty('width', `${val}px`, 'important');
            }
            const badge = document.getElementById('right-col-val');
            if (badge) badge.textContent = `${val}px`;
        }"""
        left_slider.input(fn=None, inputs=[left_slider], js=left_resize_js)
        left_slider.change(fn=None, inputs=[left_slider], js=left_resize_js)
        right_slider.input(fn=None, inputs=[right_slider], js=right_resize_js)
        right_slider.change(fn=None, inputs=[right_slider], js=right_resize_js)

    return demo, theme

