custom_css = """
/* ==========================================================================
   SRINI RAG HARNESS - LIGHT MINIMALIST 3-COLUMN CHAT LAYOUT
   Inspired by dom-the-dev.github.io/three-columns-chat-layout
   ========================================================================== */

:root {
    --background-color: #F6F7FB;
    --primary-color: #4C426D;
    --primary-hover: #3b3256;
    --text-primary: #1e293b;
    --text-secondary: #475569;
    --text-muted: #64748b;
    --border-color: #edf2f7;
    --border-card: #e2e8f0;
    --avatar-bg: #9ca3af;
    --card-bg: #ffffff;
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
    background-color: #ffffff !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    font-size: 13px !important;
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
    background-color: #ffffff !important;
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
    background-color: #ffffff !important;
}

footer {
    display: none !important;
}

/* ==========================================================================
   TOP APPLICATION BAR (Clean White Header)
   ========================================================================== */
#app-header {
    height: 48px !important;
    min-height: 48px !important;
    max-height: 48px !important;
    flex-shrink: 0 !important;
    background: #ffffff !important;
    border-bottom: 1px solid var(--border-color) !important;
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
    background: rgba(76, 66, 109, 0.08);
    border: 1px solid rgba(76, 66, 109, 0.2);
    color: var(--primary-color);
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.app-brand-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.2px;
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
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    border: 1px solid var(--border-card);
    background: var(--background-color);
    color: var(--text-secondary);
}

.pill-green {
    background: #ecfdf5 !important;
    border-color: #a7f3d0 !important;
    color: #065f46 !important;
}

.pill-purple {
    background: #f5f3ff !important;
    border-color: #ddd6fe !important;
    color: #5b21b6 !important;
}

.pill-blue {
    background: #eff6ff !important;
    border-color: #bfdbfe !important;
    color: #1e40af !important;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

/* ==========================================================================
   3-COLUMN MAIN LAYOUT
   ========================================================================== */
#app-3-columns {
    display: flex !important;
    flex-direction: row !important;
    flex: 1 1 0% !important;
    height: calc(100vh - 48px) !important;
    max-height: calc(100vh - 48px) !important;
    width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    overflow: hidden !important;
    background-color: #ffffff !important;
}

/* ==========================================================================
   LEFT COLUMN: SIDEBAR (DOCUMENTS & CHUNKS)
   ========================================================================== */
#col-sidebar {
    flex: 0 0 290px !important;
    max-width: 320px !important;
    min-width: 270px !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-color) !important;
    background: #ffffff !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    padding: 12px 14px !important;
    box-sizing: border-box !important;
}

.section-box {
    background: #ffffff;
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 12px;
}

.sidebar-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.80rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--primary-color);
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border-color);
}

/* dom-the-dev Chat Item Style for Documents */
.doc-list-scroll {
    max-height: 160px;
    overflow-y: auto;
}

.chat-item {
    padding: 10px 8px;
    border-bottom: 1px solid var(--background-color);
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: default;
    border-radius: 6px;
    transition: background-color 0.15s ease;
}

.chat-item:hover {
    background-color: var(--background-color);
}

.chat-item:last-child {
    border-bottom: none;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 9999px;
    background-color: var(--avatar-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 0.70rem;
    font-weight: 700;
    flex-shrink: 0;
}

.chat-item-text {
    flex: 1;
    overflow: hidden;
}

.sender {
    font-weight: bold;
    font-size: 0.82rem;
    color: var(--text-primary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.preview {
    color: var(--text-muted);
    font-size: 0.70rem;
    margin: 2px 0 0 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Upload Drop Area */
[data-testid="file-upload"],
.file-preview,
.upload-container {
    background: var(--background-color) !important;
    border: 1.5px dashed #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 80px !important;
    color: var(--text-secondary) !important;
    transition: all 0.2s ease !important;
}

[data-testid="file-upload"]:hover {
    border-color: var(--primary-color) !important;
    background: rgba(76, 66, 109, 0.04) !important;
}

/* Stats Grid in Light Theme */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    margin: 6px 0;
}

.stat-card {
    background: var(--background-color);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 8px 10px;
    text-align: center;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.1;
    color: var(--primary-color);
}

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
    background: var(--background-color);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 10px;
    font-size: 0.76rem;
}

.strategy-row {
    margin-bottom: 5px;
    display: flex;
    flex-direction: column;
}

.strategy-row:last-child { margin-bottom: 0; }
.strategy-label { font-size: 0.68rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
.strategy-content { font-size: 0.74rem; color: var(--text-secondary); }

/* ==========================================================================
   MIDDLE COLUMN: MAIN CHAT & SPEECH BUBBLES
   Matching dom-the-dev purple user bubble & light bot bubble
   ========================================================================== */
#col-chat {
    flex: 1 1 0% !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-color) !important;
    background: #ffffff !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    padding: 14px 20px !important;
    box-sizing: border-box !important;
}

.chat-column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 6px;
    margin-bottom: 6px;
    border-bottom: 1px solid var(--border-color);
    min-height: 28px;
    flex-shrink: 0 !important;
}

.chatbot,
[data-testid="chatbot"] {
    flex: 1 1 0% !important;
    min-height: 180px !important;
    height: auto !important;
    background: #ffffff !important;
    border: none !important;
    overflow-y: auto !important;
    padding: 10px 0 !important;
}

.chatbot * {
    background-color: transparent;
}

/* dom-the-dev Chat Bubbles:
   User Message: Deep Purple #4C426D with white text
   Bot Message: Soft Light Grey #F6F7FB with dark text */
.message.user,
[data-testid="user"] .message,
div[class*="user"] > .message {
    background-color: var(--primary-color) !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
    max-width: 74% !important;
    margin-left: auto !important;
    box-shadow: 0 1px 3px rgba(76, 66, 109, 0.15) !important;
}

.message.user * {
    color: #ffffff !important;
}

.message.bot,
[data-testid="bot"] .message,
div[class*="bot"] > .message {
    background-color: var(--background-color) !important;
    color: var(--text-primary) !important;
    border: 1px solid #e9ecef !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 12px 18px !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
    max-width: 78% !important;
    margin-right: auto !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
}

.message.bot * {
    color: var(--text-primary) !important;
}

/* Chat Input Row Pinned at Bottom */
#chat-input-row {
    flex-shrink: 0 !important;
    gap: 8px !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
    padding-top: 6px !important;
    border-top: 1px solid var(--border-color) !important;
}

#chat-input-box textarea {
    background: #ffffff !important;
    border: 1.5px solid var(--border-card) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 13px !important;
    padding: 9px 12px !important;
    box-shadow: none !important;
}

#chat-input-box textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(76, 66, 109, 0.12) !important;
}

/* Search Accordion */
#search-accordion {
    margin-top: 6px !important;
    background: var(--background-color) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    flex-shrink: 0 !important;
}

#search-accordion summary {
    font-size: 0.80rem !important;
    font-weight: 700 !important;
    color: var(--primary-color) !important;
    padding: 6px 10px !important;
}

#search-results-panel {
    max-height: 160px !important;
    overflow-y: auto !important;
    padding: 8px 10px !important;
    font-size: 0.80rem !important;
    background: #ffffff !important;
}

.search-chunk-card {
    background: var(--background-color);
    border: 1px solid var(--border-card);
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
    color: var(--primary-color);
    font-weight: 600;
}

.search-chunk-content {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 0.72rem;
    color: var(--text-secondary);
    background: #ffffff;
    border: 1px solid var(--border-card);
    padding: 6px 8px;
    border-radius: 4px;
    white-space: pre-wrap;
    line-height: 1.4;
}

/* ==========================================================================
   RIGHT COLUMN: INSPECTOR PANEL (dom-the-dev info style)
   ========================================================================== */
#col-inspector {
    flex: 0 0 310px !important;
    max-width: 350px !important;
    min-width: 280px !important;
    height: 100% !important;
    max-height: 100% !important;
    background: #ffffff !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    padding: 14px !important;
    box-sizing: border-box !important;
}

/* dom-the-dev exact info classes */
.info-avatar {
    width: 86px;
    height: 86px;
    border-radius: 9999px;
    background-color: var(--avatar-bg);
    margin: 15px auto 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    color: #ffffff;
}

.info-name {
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    margin-top: 12px;
    margin-bottom: 0;
    color: var(--text-primary);
}

.info-description {
    margin: 8px 12px 14px;
    text-align: center;
    color: var(--text-muted);
    font-size: 12px;
    line-height: 1.5;
}

/* Boxes inside Right Column */
.obs-stat-row {
    display: flex;
    gap: 6px;
    margin-bottom: 10px;
}

.obs-stat-card {
    flex: 1;
    background: var(--background-color);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 6px 4px;
    text-align: center;
}

.obs-stat-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
}

.obs-stat-val {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-top: 2px;
}

#observability-panel,
#memory-panel {
    background: #ffffff !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 8px !important;
    padding: 10px !important;
    max-height: 380px !important;
    overflow-y: auto !important;
}

/* Tab Headers */
button[role="tab"] {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 6px 10px !important;
    border-radius: 0 !important;
}

button[role="tab"][aria-selected="true"] {
    color: var(--primary-color) !important;
    border-bottom-color: var(--primary-color) !important;
    background: rgba(76, 66, 109, 0.05) !important;
}

/* Stepper */
.stepper-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin: 6px 0;
}

.stepper-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    background: var(--background-color);
    border: 1px solid var(--border-card);
    border-radius: 6px;
    font-size: 0.76rem;
    transition: all 0.15s ease;
}

.stepper-item.active {
    background: #ffffff;
    border-color: var(--primary-color);
    box-shadow: 0 1px 3px rgba(76, 66, 109, 0.12);
}

.stepper-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #e2e8f0;
    color: var(--primary-color);
    font-weight: 700;
    font-size: 0.68rem;
    flex-shrink: 0;
}

.stepper-item.active .stepper-num {
    background: var(--primary-color);
    color: #ffffff;
}

.stepper-title { font-weight: 600; color: var(--text-primary); }
.stepper-desc { font-size: 0.68rem; color: var(--text-muted); }

/* Table */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 6px 0 !important;
    font-size: 0.72rem !important;
    background: #ffffff !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

th {
    background: var(--background-color) !important;
    color: var(--text-secondary) !important;
    padding: 5px 6px !important;
    font-weight: 700 !important;
    border: 1px solid var(--border-card) !important;
    text-transform: uppercase !important;
    font-size: 0.66rem !important;
}

td {
    padding: 5px 6px !important;
    border: 1px solid var(--border-card) !important;
    color: var(--text-secondary) !important;
}

/* Buttons in dom-the-dev Style */
button {
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

button:hover { opacity: 0.9 !important; }

.primary, button[variant="primary"] {
    background: var(--primary-color) !important;
    color: #ffffff !important;
    border: 1px solid var(--primary-color) !important;
}

.secondary, button[variant="secondary"] {
    background: var(--background-color) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-card) !important;
}

.stop, button[variant="stop"] {
    background: #fef2f2 !important;
    color: #b91c1c !important;
    border: 1px solid #fecaca !important;
}

/* Badge Tags */
.badge-tag {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 700;
}

.badge-pdf { background: #fee2e2; color: #b91c1c; }
.badge-md { background: #e0f2fe; color: #0369a1; }
.badge-chunks { background: #ede9fe; color: var(--primary-color); }

/* Scrollbars */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--background-color); }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
"""