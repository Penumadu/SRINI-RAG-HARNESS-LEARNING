custom_css = """
/* ==========================================================================
   SRINI RAG HARNESS LEARNING - 3-COLUMN SEAMLESS APPLICATION LAYOUT
   Inspired by dom-the-dev three-columns-chat-layout
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #080c16;
    --bg-sidebar: #0b101d;
    --bg-surface: #10172a;
    --bg-surface-elevated: #162038;
    --border-divider: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(99, 102, 241, 0.35);
    
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    --primary-gradient-hover: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
    
    --accent-cyan: #38bdf8;
    --accent-emerald: #10b981;
    --accent-purple: #c084fc;
    --accent-amber: #fbbf24;
    --accent-rose: #f43f5e;
}

/* ==========================================================================
   FULL VIEWPORT SEAMLESS APP CANVAS (100vw x 100vh)
   ========================================================================== */
*, *::before, *::after {
    box-sizing: border-box !important;
}

html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.gradio-container {
    max-width: 100vw !important;
    width: 100vw !important;
    height: 100vh !important;
    max-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background-color: var(--bg-base) !important;
}

.gradio-container > .main,
.gradio-container > .main > .wrap {
    height: 100% !important;
    max-height: 100% !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    gap: 0 !important;
}

footer {
    display: none !important;
}

/* ==========================================================================
   TOP APPLICATION BAR
   ========================================================================== */
#app-header {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    flex-shrink: 0 !important;
    background: #0d1322 !important;
    border-bottom: 1px solid var(--border-divider) !important;
    padding: 0 20px !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    z-index: 10;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.app-brand-badge {
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: #a5b4fc;
    font-size: 0.70rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

.app-brand-title {
    font-size: 1.10rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.3px;
    margin: 0;
}

.app-status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--border-divider);
    background: rgba(255, 255, 255, 0.04);
    color: #e2e8f0;
}

.pill-green {
    background: rgba(16, 185, 129, 0.12) !important;
    border-color: rgba(16, 185, 129, 0.35) !important;
    color: #34d399 !important;
}

.pill-purple {
    background: rgba(168, 85, 247, 0.12) !important;
    border-color: rgba(168, 85, 247, 0.35) !important;
    color: #c084fc !important;
}

.pill-blue {
    background: rgba(59, 130, 246, 0.12) !important;
    border-color: rgba(59, 130, 246, 0.35) !important;
    color: #60a5fa !important;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

/* ==========================================================================
   3-COLUMN MAIN LAYOUT (FULL HEIGHT SPLIT)
   ========================================================================== */
#app-3-columns {
    display: flex !important;
    flex-direction: row !important;
    flex: 1 1 0% !important;
    height: calc(100vh - 52px) !important;
    max-height: calc(100vh - 52px) !important;
    width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    overflow: hidden !important;
}

/* Remove default gradio padding on columns */
#col-sidebar {
    flex: 0 0 320px !important;
    max-width: 340px !important;
    min-width: 290px !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-divider) !important;
    background: var(--bg-sidebar) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding: 12px 14px !important;
    box-sizing: border-box !important;
}

#col-chat {
    flex: 1 1 0% !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-divider) !important;
    background: var(--bg-base) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    padding: 12px 16px !important;
    box-sizing: border-box !important;
}

#col-inspector {
    flex: 0 0 360px !important;
    max-width: 380px !important;
    min-width: 310px !important;
    height: 100% !important;
    max-height: 100% !important;
    background: var(--bg-sidebar) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding: 12px 14px !important;
    box-sizing: border-box !important;
}

.sidebar-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #94a3b8;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

/* Drag & Drop */
[data-testid="file-upload"],
.file-preview,
.upload-container {
    background: rgba(16, 23, 42, 0.6) !important;
    border: 1.5px dashed rgba(99, 102, 241, 0.4) !important;
    border-radius: 10px !important;
    min-height: 90px !important;
    color: #ffffff !important;
    transition: all 0.2s ease !important;
}

[data-testid="file-upload"]:hover,
.file-preview:hover {
    border-color: #818cf8 !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

/* Document List */
.doc-list-scroll {
    max-height: 140px;
    overflow-y: auto;
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid var(--border-divider);
    border-radius: 8px;
    padding: 6px;
}

.doc-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 9px;
    margin-bottom: 4px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 6px;
    font-size: 0.80rem;
}

.doc-row:last-child {
    margin-bottom: 0;
}

.doc-row-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    color: #f1f5f9;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.badge-tag {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.badge-pdf { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
.badge-md { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
.badge-chunks { background: rgba(168, 85, 247, 0.15); color: #d8b4fe; }

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    margin: 6px 0;
}

.stat-card {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-divider);
    border-radius: 8px;
    padding: 8px 10px;
    text-align: center;
}

.stat-value {
    font-size: 1.35rem;
    font-weight: 800;
    line-height: 1.1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stat-card-blue .stat-value { color: var(--accent-cyan); }
.stat-card-purple .stat-value { color: var(--accent-purple); }
.stat-card-emerald .stat-value { color: var(--accent-emerald); }
.stat-card-amber .stat-value { color: var(--accent-amber); }

.stat-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 2px;
}

/* Strategy Box */
.strategy-box {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid var(--border-divider);
    border-radius: 8px;
    padding: 10px;
    font-size: 0.78rem;
}

.strategy-row {
    margin-bottom: 6px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.strategy-row:last-child { margin-bottom: 0; }
.strategy-label { font-size: 0.68rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.strategy-content { font-size: 0.76rem; color: #cbd5e1; }

/* ==========================================================================
   MIDDLE COLUMN: MAIN CHAT & RETRIEVED SEARCH RESULTS
   ========================================================================== */
.chat-column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 6px;
    margin-bottom: 6px;
    border-bottom: 1px solid var(--border-divider);
    min-height: 28px;
    flex-shrink: 0 !important;
}

.chatbot,
[data-testid="chatbot"] {
    flex: 1 1 0% !important;
    min-height: 180px !important;
    height: auto !important;
    background: #090e1c !important;
    border: 1px solid var(--border-divider) !important;
    border-radius: 12px !important;
    overflow-y: auto !important;
}

.chatbot * {
    background-color: transparent !important;
}

.message.user {
    background: var(--primary-gradient) !important;
    color: #ffffff !important;
    border-radius: 14px 14px 3px 14px !important;
    padding: 9px 14px !important;
    font-size: 0.90rem !important;
    max-width: 82% !important;
}

.message.bot {
    background: #141c2e !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px 14px 14px 3px !important;
    padding: 10px 16px !important;
    font-size: 0.88rem !important;
    max-width: 88% !important;
}

#chat-input-row {
    flex-shrink: 0 !important;
    gap: 8px !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
}

#chat-input-box textarea {
    background: #10172a !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.90rem !important;
    padding: 9px 12px !important;
}

#chat-input-box textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

/* Search Accordion */
#search-accordion {
    margin-top: 8px !important;
    background: rgba(11, 16, 29, 0.8) !important;
    border: 1px solid var(--border-divider) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

#search-accordion summary {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #cbd5e1 !important;
    padding: 7px 12px !important;
}

#search-results-panel {
    max-height: 180px !important;
    overflow-y: auto !important;
    padding: 10px 12px !important;
    font-size: 0.82rem !important;
}

.search-chunk-card {
    background: rgba(22, 32, 53, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 8px 10px;
    margin-bottom: 6px;
}

.search-chunk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 0.74rem;
}

.search-chunk-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #94a3b8;
    background: rgba(0, 0, 0, 0.35);
    padding: 6px 8px;
    border-radius: 4px;
    white-space: pre-wrap;
}

/* ==========================================================================
   RIGHT COLUMN: INSPECTOR PANEL (OBSERVABILITY & MEMORY)
   ========================================================================== */

.inspector-profile {
    text-align: center;
    padding: 14px 10px;
    border-bottom: 1px solid var(--border-divider);
    background: rgba(255, 255, 255, 0.015);
    border-radius: 10px;
}

.inspector-avatar {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    margin: 0 auto 8px auto;
    background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
}

.inspector-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}

.inspector-desc {
    font-size: 0.76rem;
    color: var(--text-muted);
    margin-top: 2px;
}

#observability-panel,
#memory-panel {
    background: rgba(0, 0, 0, 0.25) !important;
    border: 1px solid var(--border-divider) !important;
    border-radius: 10px !important;
    padding: 12px !important;
    max-height: 480px !important;
    overflow-y: auto !important;
}

/* Tab Headers */
button[role="tab"] {
    font-size: 0.80rem !important;
    font-weight: 700 !important;
    color: #94a3b8 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 6px 12px !important;
    border-radius: 0 !important;
}

button[role="tab"][aria-selected="true"] {
    color: #818cf8 !important;
    border-bottom-color: #6366f1 !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

/* Stepper */
.stepper-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 8px 0;
}

.stepper-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 6px;
    font-size: 0.78rem;
}

.stepper-item.active {
    background: rgba(99, 102, 241, 0.12);
    border-color: rgba(99, 102, 241, 0.35);
}

.stepper-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    color: #c7d2fe;
    font-weight: 700;
    font-size: 0.70rem;
}

.stepper-title { font-weight: 600; color: #f1f5f9; }
.stepper-desc { font-size: 0.70rem; color: var(--text-muted); }

/* Table */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 8px 0 !important;
    font-size: 0.74rem !important;
}

th {
    background: rgba(22, 32, 53, 0.9) !important;
    color: #cbd5e1 !important;
    padding: 6px 8px !important;
    font-weight: 700 !important;
    border: 1px solid var(--border-divider) !important;
    text-transform: uppercase !important;
}

td {
    padding: 5px 8px !important;
    border: 1px solid var(--border-divider) !important;
    color: #94a3b8 !important;
}

/* Buttons */
button {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

button:hover { transform: translateY(-1px) !important; }

.primary, button[variant="primary"] {
    background: var(--primary-gradient) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}

.secondary, button[variant="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #e2e8f0 !important;
    border: 1px solid var(--border-divider) !important;
}

.stop, button[variant="stop"] {
    background: rgba(244, 63, 94, 0.12) !important;
    color: #fb7185 !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
}

/* Scrollbars */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 3px; }
"""