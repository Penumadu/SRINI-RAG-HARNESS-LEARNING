custom_css = """
/* ==========================================================================
   SRINI RAG HARNESS - HIGH PRECISION AGENTIC WORKBENCH
   Designed following intentional visual principles & technical aesthetics
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    /* 6 Deliberate Palette Tokens */
    --canvas-bg: #F8FAFC;
    --surface-card: #FFFFFF;
    --surface-subtle: #F1F5F9;
    --ink-primary: #0F172A;
    --ink-secondary: #475569;
    --ink-muted: #64748B;
    --ink-subtle: #94A3B8;
    --border-subtle: #E2E8F0;
    --border-card: #E2E8F0;
    --border-focus: #CBD5E1;

    /* Technical Brand Accent - Electric Indigo */
    --brand-primary: #4F46E5;
    --brand-hover: #4338CA;
    --brand-light: rgba(79, 70, 229, 0.07);
    --brand-border: rgba(79, 70, 229, 0.18);

    /* Purpose-driven Status Accents */
    --status-live: #059669;
    --status-live-bg: #ECFDF5;
    --status-live-border: #A7F3D0;
    --status-trace: #2563EB;
    --status-trace-bg: #EFF6FF;
    --status-trace-border: #BFDBFE;
    --status-alert: #DC2626;
    --status-alert-bg: #FEF2F2;
    --status-alert-border: #FECACA;

    /* Distinct Typography Roles */
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
}

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
    background-color: var(--canvas-bg) !important;
    color: var(--ink-primary) !important;
    font-family: var(--font-sans) !important;
    font-size: 13px !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
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
    background-color: var(--canvas-bg) !important;
    font-family: var(--font-sans) !important;
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
    background-color: var(--canvas-bg) !important;
}

footer {
    display: none !important;
}

/* ==========================================================================
   TOP APPLICATION BAR (46px Precision Instrument Header)
   ========================================================================== */
#app-header {
    height: 46px !important;
    min-height: 46px !important;
    max-height: 46px !important;
    flex-shrink: 0 !important;
    background: var(--surface-card) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 0 16px !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    z-index: 100 !important;
    box-sizing: border-box !important;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.app-brand-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: var(--brand-light);
    border: 1px solid var(--brand-border);
    border-radius: 6px;
    font-size: 0.85rem;
    color: var(--brand-primary);
    flex-shrink: 0;
}

.app-brand-text {
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.app-brand-title {
    font-size: 0.94rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin: 0;
    letter-spacing: -0.015em;
    font-family: var(--font-sans);
}

.app-brand-version {
    font-size: 0.70rem;
    font-weight: 500;
    color: var(--ink-muted);
    font-family: var(--font-mono);
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
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 0.70rem;
    font-weight: 600;
    border: 1px solid var(--border-subtle);
    background: var(--surface-card);
    color: var(--ink-secondary);
    white-space: nowrap;
    transition: all 0.15s ease;
}

.status-pill:hover {
    border-color: var(--border-focus);
}

.pill-green {
    background: var(--status-live-bg) !important;
    border-color: var(--status-live-border) !important;
    color: var(--status-live) !important;
}

.pill-purple {
    background: var(--brand-light) !important;
    border-color: var(--brand-border) !important;
    color: var(--brand-primary) !important;
    font-family: var(--font-mono);
}

.pill-blue {
    background: var(--status-trace-bg) !important;
    border-color: var(--status-trace-border) !important;
    color: var(--status-trace) !important;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.status-dot.pulse {
    box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4);
    animation: dotPulse 2s infinite;
}

@keyframes dotPulse {
    0% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4); }
    70% { box-shadow: 0 0 0 5px rgba(5, 150, 105, 0); }
    100% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0); }
}

/* ==========================================================================
   3-COLUMN MAIN LAYOUT CONTAINER
   ========================================================================== */
#app-3-columns {
    display: flex !important;
    flex-direction: row !important;
    flex: 1 1 0% !important;
    height: calc(100vh - 46px) !important;
    max-height: calc(100vh - 46px) !important;
    width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    overflow: hidden !important;
    background-color: var(--canvas-bg) !important;
}

/* Draggable Vertical Splitter Handles */
.col-splitter {
    width: 5px !important;
    min-width: 5px !important;
    max-width: 5px !important;
    height: 100% !important;
    background: transparent !important;
    cursor: col-resize !important;
    position: relative !important;
    z-index: 20 !important;
    transition: background 0.15s ease !important;
    flex-shrink: 0 !important;
    margin: 0 -2px !important;
}

.col-splitter:hover,
.col-splitter:active {
    background: var(--brand-primary) !important;
}

/* ==========================================================================
   SLIM INLINE COLUMN WIDTH CONTROLS (Low-profile, Zero Waste)
   ========================================================================== */
#sidebar-width-control,
#inspector-width-control {
    background: var(--surface-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    padding: 5px 9px !important;
    margin: 0 0 8px 0 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 3px !important;
    box-sizing: border-box !important;
    width: 100% !important;
}

#sidebar-width-control .wrap,
#inspector-width-control .wrap {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
}

#sidebar-width-control .head,
#inspector-width-control .head {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}

.col-slider-label {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--ink-secondary) !important;
    margin: 0 !important;
}

.col-slider-val {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--brand-primary) !important;
    background: var(--brand-light) !important;
    border: 1px solid var(--brand-border) !important;
    border-radius: 4px !important;
    padding: 0 5px !important;
}

#sidebar-width-control input[type="range"],
#inspector-width-control input[type="range"] {
    height: 3px !important;
    margin: 2px 0 0 0 !important;
    width: 100% !important;
    accent-color: var(--brand-primary) !important;
    cursor: pointer !important;
}

#sidebar-width-control input[type="number"],
#inspector-width-control input[type="number"],
#sidebar-width-control button,
#inspector-width-control button {
    display: none !important;
}

/* ==========================================================================
   LEFT COLUMN: SIDEBAR (KNOWLEDGE BASE & CHUNKING)
   ========================================================================== */
#col-sidebar {
    flex: 0 0 290px !important;
    width: 290px !important;
    min-width: 180px !important;
    max-width: 550px !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-subtle) !important;
    background: var(--surface-card) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding: 12px !important;
    box-sizing: border-box !important;
}

.sidebar-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin-bottom: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border-subtle);
    letter-spacing: -0.01em;
}

.sidebar-section-title span:first-child {
    display: flex;
    align-items: center;
    gap: 6px;
}

.sidebar-badge {
    font-size: 0.64rem;
    font-weight: 600;
    font-family: var(--font-mono);
    padding: 1px 6px;
    border-radius: 4px;
    background: var(--surface-subtle);
    color: var(--ink-muted);
}

.sidebar-badge.live {
    background: var(--status-live-bg);
    color: var(--status-live);
    border: 1px solid var(--status-live-border);
}

/* Polished File Drop Area */
[data-testid="file-upload"],
.file-preview,
.upload-container {
    background: var(--surface-subtle) !important;
    border: 1.5px dashed var(--border-focus) !important;
    border-radius: 8px !important;
    min-height: 72px !important;
    max-height: 80px !important;
    color: var(--ink-secondary) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 6px !important;
    transition: all 0.15s ease !important;
}

[data-testid="file-upload"]:hover {
    border-color: var(--brand-primary) !important;
    background: var(--brand-light) !important;
}

[data-testid="file-upload"] button {
    font-size: 0.72rem !important;
}

/* Document Item List */
.doc-list-scroll {
    max-height: 150px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.chat-item {
    padding: 7px 9px;
    background: var(--canvas-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: default;
    transition: all 0.15s ease;
}

.chat-item:hover {
    border-color: var(--border-focus);
    transform: translateX(2px);
    background: #ffffff;
}

.avatar {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--ink-secondary);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 700;
    flex-shrink: 0;
}

.avatar.pdf {
    background: var(--status-alert-bg);
    color: var(--status-alert);
    border-color: var(--status-alert-border);
}

.avatar.md {
    background: var(--status-trace-bg);
    color: var(--status-trace);
    border-color: var(--status-trace-border);
}

.chat-item-text {
    flex: 1;
    overflow: hidden;
}

.sender {
    font-weight: 600;
    font-size: 0.78rem;
    color: var(--ink-primary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.preview {
    color: var(--ink-muted);
    font-size: 0.68rem;
    font-family: var(--font-mono);
    margin: 1px 0 0 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    margin: 6px 0;
}

.stat-card {
    background: var(--surface-card);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 6px 8px;
    text-align: center;
    transition: transform 0.12s ease, border-color 0.12s ease;
}

.stat-card:hover {
    border-color: var(--border-focus);
    transform: translateY(-1px);
}

.stat-value {
    font-family: var(--font-mono);
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--brand-primary);
}

.stat-label {
    font-size: 0.64rem;
    font-weight: 600;
    color: var(--ink-muted);
    margin-top: 2px;
}

/* Strategy Box */
.strategy-box {
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 0.72rem;
}

.strategy-row {
    margin-bottom: 5px;
    display: flex;
    flex-direction: column;
}

.strategy-row:last-child { margin-bottom: 0; }
.strategy-label { font-size: 0.65rem; font-weight: 600; color: var(--ink-muted); }
.strategy-content { font-size: 0.72rem; color: var(--ink-secondary); margin-top: 1px; }

/* ==========================================================================
   MIDDLE COLUMN: MAIN CHAT & SUGGESTIONS
   ========================================================================== */
#col-chat {
    flex: 1 1 0% !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-subtle) !important;
    background: var(--canvas-bg) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    padding: 10px 16px !important;
    box-sizing: border-box !important;
}

.chat-column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 6px;
    margin-bottom: 4px;
    border-bottom: 1px solid var(--border-subtle);
    min-height: 28px;
    flex-shrink: 0 !important;
}

.chatbot,
[data-testid="chatbot"] {
    flex: 1 1 0% !important;
    min-height: 160px !important;
    height: auto !important;
    background: transparent !important;
    border: none !important;
    overflow-y: auto !important;
    padding: 8px 0 !important;
}

.chatbot * {
    background-color: transparent;
}

/* Chat Bubbles */
.message.user,
[data-testid="user"] .message,
div[class*="user"] > .message {
    background-color: var(--brand-primary) !important;
    color: #ffffff !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 10px 14px !important;
    font-size: 13.5px !important;
    line-height: 1.5 !important;
    max-width: 76% !important;
    margin-left: auto !important;
    box-shadow: 0 1px 3px rgba(79, 70, 229, 0.16) !important;
}

.message.user * {
    color: #ffffff !important;
}

.message.bot,
[data-testid="bot"] .message,
div[class*="bot"] > .message {
    background-color: var(--surface-card) !important;
    color: var(--ink-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px 16px 16px 4px !important;
    padding: 12px 16px !important;
    font-size: 13.5px !important;
    line-height: 1.55 !important;
    max-width: 82% !important;
    margin-right: auto !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

.message.bot * {
    color: var(--ink-primary) !important;
}

.message.bot pre,
.message.bot code {
    font-family: var(--font-mono) !important;
    font-size: 11.5px !important;
    background: var(--surface-subtle) !important;
    border-radius: 4px !important;
}

/* Quick Prompts Row */
#quick-prompts-row {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 6px !important;
    margin-bottom: 6px !important;
    margin-top: 2px !important;
    flex-shrink: 0 !important;
    overflow-x: auto !important;
    padding-bottom: 2px !important;
}

.quick-prompt-btn,
#quick-prompts-row button {
    background: var(--surface-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    padding: 3px 10px !important;
    font-size: 0.70rem !important;
    font-weight: 500 !important;
    color: var(--ink-secondary) !important;
    white-space: nowrap !important;
    height: 26px !important;
    min-height: 26px !important;
    line-height: 1 !important;
    transition: all 0.15s ease !important;
}

.quick-prompt-btn:hover,
#quick-prompts-row button:hover {
    border-color: var(--brand-primary) !important;
    color: var(--brand-primary) !important;
    background: var(--brand-light) !important;
    transform: translateY(-1px) !important;
}

/* Search Accordion Drawer */
#search-accordion {
    margin-top: 4px !important;
    background: var(--surface-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    flex-shrink: 0 !important;
}

#search-accordion summary {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: var(--brand-primary) !important;
    padding: 6px 10px !important;
    cursor: pointer !important;
}

#search-results-panel {
    max-height: 140px !important;
    overflow-y: auto !important;
    padding: 8px 10px !important;
    font-size: 0.78rem !important;
    background: var(--surface-card) !important;
}

.search-chunk-card {
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 7px 9px;
    margin-bottom: 6px;
    transition: all 0.15s ease;
}

.search-chunk-card:hover {
    border-color: var(--brand-border);
    background: #ffffff;
}

.search-chunk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 0.72rem;
    color: var(--brand-primary);
    font-weight: 600;
}

.search-chunk-content {
    font-family: var(--font-sans);
    font-size: 0.72rem;
    color: var(--ink-secondary);
    background: #ffffff;
    border: 1px solid var(--border-subtle);
    padding: 6px 8px;
    border-radius: 4px;
    white-space: pre-wrap;
    line-height: 1.4;
}

/* Chat Input Bar Pinned at Bottom */
#chat-input-row {
    flex-shrink: 0 !important;
    gap: 6px !important;
    margin-top: 4px !important;
    margin-bottom: 0 !important;
    padding-top: 4px !important;
    border-top: 1px solid var(--border-subtle) !important;
}

#chat-input-box textarea {
    background: var(--surface-card) !important;
    border: 1.5px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--ink-primary) !important;
    font-size: 13px !important;
    font-family: var(--font-sans) !important;
    padding: 8px 12px !important;
    box-shadow: none !important;
    transition: all 0.15s ease !important;
}

#chat-input-box textarea:focus {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 0 0 3px var(--brand-light) !important;
}

/* ==========================================================================
   RIGHT COLUMN: AGENT INSPECTOR PANEL
   ========================================================================== */
#col-inspector {
    flex: 0 0 320px !important;
    width: 320px !important;
    min-width: 220px !important;
    max-width: 600px !important;
    height: 100% !important;
    max-height: 100% !important;
    background: var(--surface-card) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
    padding: 10px !important;
    box-sizing: border-box !important;
}

.compact-agent-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 10px;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    margin-bottom: 2px;
}

.compact-agent-left {
    display: flex;
    align-items: center;
    gap: 6px;
}

.compact-avatar {
    width: 24px;
    height: 24px;
    border-radius: 6px;
    background-color: var(--surface-card);
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}

.compact-title {
    font-weight: 700;
    font-size: 0.80rem;
    color: var(--ink-primary);
}

.compact-badge {
    font-size: 0.65rem;
    font-family: var(--font-mono);
    font-weight: 600;
    color: var(--brand-primary);
    background: var(--brand-light);
    border: 1px solid var(--brand-border);
    padding: 1px 6px;
    border-radius: 4px;
}

/* Observability Status Tiles */
.obs-stat-row {
    display: flex;
    gap: 6px;
    margin-bottom: 8px;
}

.obs-stat-card {
    flex: 1;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 5px 4px;
    text-align: center;
}

.obs-stat-label {
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--ink-muted);
}

.obs-stat-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--brand-primary);
    margin-top: 1px;
}

#observability-panel,
#memory-panel {
    background: var(--surface-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    padding: 8px !important;
    max-height: calc(100vh - 190px) !important;
    overflow-y: auto !important;
}

/* Segmented Tabs */
#observability-tabs [role="tablist"] {
    background: var(--surface-subtle) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    padding: 2px !important;
    gap: 2px !important;
}

button[role="tab"] {
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    color: var(--ink-muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 4px 10px !important;
    border-radius: 4px !important;
    transition: all 0.15s ease !important;
}

button[role="tab"][aria-selected="true"] {
    color: var(--ink-primary) !important;
    background: var(--surface-card) !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
}

/* State Machine Stepper */
.stepper-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin: 4px 0;
}

.stepper-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 8px;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    font-size: 0.74rem;
    transition: all 0.15s ease;
}

.stepper-item.active {
    background: #ffffff;
    border-color: var(--brand-primary);
    box-shadow: 0 1px 4px var(--brand-light);
}

.stepper-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--border-subtle);
    color: var(--ink-secondary);
    font-weight: 700;
    font-size: 0.65rem;
    flex-shrink: 0;
}

.stepper-item.active .stepper-num {
    background: var(--brand-primary);
    color: #ffffff;
}

.stepper-title {
    font-weight: 600;
    color: var(--ink-primary);
    font-family: var(--font-mono);
    font-size: 0.72rem;
}

.stepper-desc {
    font-size: 0.66rem;
    color: var(--ink-muted);
}

/* Tables */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 4px 0 !important;
    font-size: 0.70rem !important;
    background: #ffffff !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

th {
    background: var(--surface-subtle) !important;
    color: var(--ink-secondary) !important;
    padding: 4px 6px !important;
    font-weight: 600 !important;
    border: 1px solid var(--border-subtle) !important;
    font-size: 0.65rem !important;
}

td {
    padding: 4px 6px !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--ink-secondary) !important;
}

/* Buttons */
button {
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    font-family: var(--font-sans) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

.primary, button[variant="primary"] {
    background: var(--brand-primary) !important;
    color: #ffffff !important;
    border: 1px solid var(--brand-primary) !important;
}

.primary:hover, button[variant="primary"]:hover {
    background: var(--brand-hover) !important;
    border-color: var(--brand-hover) !important;
}

.secondary, button[variant="secondary"] {
    background: var(--surface-card) !important;
    color: var(--ink-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
}

.secondary:hover, button[variant="secondary"]:hover {
    background: var(--surface-subtle) !important;
    color: var(--ink-primary) !important;
    border-color: var(--border-focus) !important;
}

.stop, button[variant="stop"] {
    background: var(--status-alert-bg) !important;
    color: var(--status-alert) !important;
    border: 1px solid var(--status-alert-border) !important;
}

.stop:hover, button[variant="stop"]:hover {
    background: #FEE2E2 !important;
}

button:active {
    transform: scale(0.98) !important;
}

/* Tag Badges */
.badge-tag {
    display: inline-block;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.64rem;
    font-weight: 600;
    font-family: var(--font-mono);
}

.badge-pdf { background: var(--status-alert-bg); color: var(--status-alert); border: 1px solid var(--status-alert-border); }
.badge-md { background: var(--status-trace-bg); color: var(--status-trace); border: 1px solid var(--status-trace-border); }
.badge-chunks { background: var(--brand-light); color: var(--brand-primary); border: 1px solid var(--brand-border); }

/* Scrollbars */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
"""