custom_css = """
/* ==========================================================================
   SRINI RAG HARNESS LEARNING - EXECUTIVE DARK THEME
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #070a13;
    --bg-surface: #0e1424;
    --bg-surface-elevated: #151d33;
    --bg-surface-hover: #1c2744;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(99, 102, 241, 0.35);
    
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    --primary-gradient-hover: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
    --card-gradient: linear-gradient(180deg, rgba(22, 32, 53, 0.85) 0%, rgba(14, 20, 36, 0.95) 100%);
    
    --accent-cyan: #38bdf8;
    --accent-emerald: #10b981;
    --accent-purple: #c084fc;
    --accent-amber: #fbbf24;
    --accent-rose: #f43f5e;
}

/* Force dark mode canvas and wipe any default white backgrounds */
html, body {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    min-height: 100vh !important;
}

.gradio-container,
.gradio-container-6-29-0,
[class*="gradio-container"],
.contain,
.wrap,
#root,
#root > div {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    margin: 0 auto !important;
    padding: 10px 16px !important;
    max-width: 100% !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* Eliminate all white backgrounds that Gradio defaults to */
.gradio-container *,
.gradio-container *:before,
.gradio-container *:after {
    border-color: var(--border-subtle) !important;
}

div[class*="block"],
div[class*="panel"],
div[class*="group"],
div[class*="form"],
.gr-box,
.gr-panel,
.gr-group {
    background-color: transparent !important;
    border: none !important;
}

footer {
    display: none !important;
}

/* ==========================================================================
   TOP HEADER BANNER
   ========================================================================== */
#top-header {
    background: linear-gradient(135deg, rgba(22, 32, 53, 0.95) 0%, rgba(14, 20, 36, 0.98) 100%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 18px 24px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

.main-title {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    font-size: 0.84rem;
    color: var(--text-muted);
    margin: 3px 0 0 0;
    font-weight: 500;
}

/* Status Chips */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}

.pill-green {
    background: rgba(16, 185, 129, 0.12) !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
    color: #34d399 !important;
}

.pill-purple {
    background: rgba(168, 85, 247, 0.12) !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    color: #c084fc !important;
}

.pill-blue {
    background: rgba(59, 130, 246, 0.12) !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
    color: #60a5fa !important;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.7; }
    50% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.7; }
}

/* ==========================================================================
   THREE COLUMN LAYOUT CARDS
   ========================================================================== */
#main-3-col-layout {
    gap: 14px !important;
    width: 100% !important;
    max-width: 100% !important;
}

#left-col,
#mid-col,
#right-col {
    background: var(--card-gradient) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

/* Card Section Headers */
.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
}

.panel-header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1.02rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}

.panel-header-badge {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
}

/* ==========================================================================
   LEFT COLUMN: UPLOAD, DOCUMENTS, CHUNK ANALYTICS
   ========================================================================== */
/* Drag and Drop Box */
[data-testid="file-upload"],
.file-preview,
.upload-container,
div:has(> [data-testid="file-upload"]) {
    background: rgba(14, 20, 36, 0.7) !important;
    border: 1.5px dashed rgba(99, 102, 241, 0.4) !important;
    border-radius: 12px !important;
    min-height: 110px !important;
    color: #ffffff !important;
    transition: all 0.25s ease !important;
}

[data-testid="file-upload"]:hover,
.file-preview:hover {
    border-color: #818cf8 !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

[data-testid="file-upload"] *,
.file-preview * {
    color: var(--text-secondary) !important;
    background: transparent !important;
}

/* Document List */
.doc-list-scroll {
    max-height: 150px;
    overflow-y: auto;
    background: rgba(7, 10, 19, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 8px;
    margin: 8px 0;
}

.doc-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 10px;
    margin-bottom: 5px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    font-size: 0.82rem;
    transition: background 0.15s ease;
}

.doc-row:last-child {
    margin-bottom: 0;
}

.doc-row:hover {
    background: rgba(255, 255, 255, 0.06);
}

.doc-row-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #f1f5f9;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.badge-tag {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.70rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.badge-pdf {
    background: rgba(244, 63, 94, 0.15);
    color: #fb7185;
    border: 1px solid rgba(244, 63, 94, 0.3);
}

.badge-md {
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}

.badge-chunks {
    background: rgba(168, 85, 247, 0.15);
    color: #d8b4fe;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

/* Metric Tiles */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 10px 0;
}

.stat-card {
    background: rgba(7, 10, 19, 0.55);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 10px 12px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.stat-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
}

.stat-card-blue::after { background: var(--accent-cyan); }
.stat-card-purple::after { background: var(--accent-purple); }
.stat-card-emerald::after { background: var(--accent-emerald); }
.stat-card-amber::after { background: var(--accent-amber); }

.stat-value {
    font-size: 1.45rem;
    font-weight: 800;
    line-height: 1.2;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stat-card-blue .stat-value { color: var(--accent-cyan); }
.stat-card-purple .stat-value { color: var(--accent-purple); }
.stat-card-emerald .stat-value { color: var(--accent-emerald); }
.stat-card-amber .stat-value { color: var(--accent-amber); }

.stat-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 3px;
}

/* Chunk Strategy Card */
.strategy-box {
    background: rgba(7, 10, 19, 0.55);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 12px;
    margin-top: 8px;
    font-size: 0.8rem;
}

.strategy-row {
    margin-bottom: 8px;
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.strategy-row:last-child {
    margin-bottom: 0;
}

.strategy-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.strategy-content {
    font-size: 0.78rem;
    color: #e2e8f0;
    line-height: 1.4;
}

/* ==========================================================================
   MIDDLE COLUMN: CHAT & RETRIEVED SEARCH RESULTS
   ========================================================================== */
/* Chatbot Box */
.chatbot,
[data-testid="chatbot"],
div[class*="chatbot"] {
    background: #090e1c !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4) !important;
}

.chatbot * {
    background-color: transparent !important;
}

/* Message bubbles */
.message-row {
    padding: 8px 12px !important;
}

.message.user {
    background: var(--primary-gradient) !important;
    color: #ffffff !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 10px 16px !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    max-width: 85% !important;
}

.message.bot {
    background: rgba(22, 32, 53, 0.95) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px 16px 16px 4px !important;
    padding: 12px 18px !important;
    font-size: 0.90rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
    max-width: 90% !important;
}

.message.bot code {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #38bdf8 !important;
    padding: 2px 5px !important;
    border-radius: 4px !important;
}

/* Chat Input Bar */
#chat-input-row {
    gap: 8px !important;
    margin-top: 10px !important;
}

#chat-input-box textarea {
    background: rgba(14, 20, 36, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.92rem !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}

#chat-input-box textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    background: rgba(20, 29, 51, 0.95) !important;
}

/* Search Results Accordion */
#search-accordion {
    margin-top: 10px !important;
    background: rgba(7, 10, 19, 0.6) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

#search-accordion summary {
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    color: #cbd5e1 !important;
    padding: 10px 14px !important;
    background: rgba(255, 255, 255, 0.02) !important;
}

#search-results-panel {
    max-height: 250px !important;
    overflow-y: auto !important;
    padding: 12px 14px !important;
    font-size: 0.84rem !important;
    color: var(--text-secondary) !important;
}

/* Search results cards */
.search-chunk-card {
    background: rgba(22, 32, 53, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
}

.search-chunk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 0.76rem;
}

.search-chunk-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: #94a3b8;
    background: rgba(0, 0, 0, 0.3);
    padding: 8px;
    border-radius: 6px;
    white-space: pre-wrap;
}

/* ==========================================================================
   RIGHT COLUMN: OBSERVABILITY, AGENT CALLS & MEMORY
   ========================================================================== */
#observability-panel,
#memory-panel {
    background: rgba(7, 10, 19, 0.6) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    max-height: 580px !important;
    overflow-y: auto !important;
    font-size: 0.84rem !important;
    color: var(--text-secondary) !important;
}

/* Tab Headers inside right column */
button[role="tab"] {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #94a3b8 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 8px 14px !important;
    border-radius: 0 !important;
    transition: all 0.2s ease !important;
}

button[role="tab"]:hover {
    color: #ffffff !important;
}

button[role="tab"][aria-selected="true"] {
    color: #818cf8 !important;
    border-bottom-color: #6366f1 !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

/* Stepper timeline */
.stepper-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 12px 0;
}

.stepper-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    font-size: 0.80rem;
    transition: background 0.15s ease;
}

.stepper-item.active {
    background: rgba(99, 102, 241, 0.12);
    border-color: rgba(99, 102, 241, 0.35);
}

.stepper-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: rgba(99, 102, 241, 0.25);
    color: #c7d2fe;
    font-weight: 700;
    font-size: 0.72rem;
}

.stepper-title {
    font-weight: 600;
    color: #f1f5f9;
}

.stepper-desc {
    font-size: 0.72rem;
    color: var(--text-muted);
}

/* Event Log Table */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 10px 0 !important;
    font-size: 0.76rem !important;
}

th {
    background: rgba(22, 32, 53, 0.9) !important;
    color: #cbd5e1 !important;
    padding: 7px 10px !important;
    font-weight: 700 !important;
    border: 1px solid var(--border-subtle) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

td {
    padding: 6px 10px !important;
    border: 1px solid var(--border-subtle) !important;
    color: #94a3b8 !important;
}

tr:nth-child(even) td {
    background: rgba(255, 255, 255, 0.015) !important;
}

/* ==========================================================================
   BUTTONS
   ========================================================================== */
button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

button:hover {
    transform: translateY(-1px) !important;
}

button:active {
    transform: translateY(0) !important;
}

/* Primary Button */
.primary,
button[variant="primary"] {
    background: var(--primary-gradient) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
}

.primary:hover,
button[variant="primary"]:hover {
    background: var(--primary-gradient-hover) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
}

/* Secondary Button */
.secondary,
button[variant="secondary"] {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #e2e8f0 !important;
    border: 1px solid var(--border-subtle) !important;
}

.secondary:hover,
button[variant="secondary"]:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
}

/* Danger / Stop Button */
.stop,
button[variant="stop"] {
    background: rgba(244, 63, 94, 0.12) !important;
    color: #fb7185 !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
}

.stop:hover,
button[variant="stop"]:hover {
    background: rgba(244, 63, 94, 0.22) !important;
    color: #ffffff !important;
    border-color: rgba(244, 63, 94, 0.5) !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.18);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}
"""