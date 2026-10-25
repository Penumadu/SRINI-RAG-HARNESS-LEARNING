custom_css = """
/* ==========================================================================
   SRINI RAG HARNESS - MODERN PROFESSIONAL STUDIO LIGHT THEME
   Linear / Stripe / Vercel Pro Light Architecture
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root, body, .gradio-container, .light {
    /* Foundation Palette Tokens - Modern Professional Studio Light */
    --canvas-bg: #F8FAFC;          /* Clean soft slate canvas */
    --surface-sidebar: #FFFFFF;    /* Pristine white sidebar panels */
    --surface-card: #FFFFFF;       /* Crisp white surface cards */
    --surface-card-hover: #F1F5F9; /* Subtle slate 100 hover */
    --surface-subtle: #F1F5F9;     /* Soft slate 100 inset */
    --surface-input: #FFFFFF;      /* Clean white input surfaces */
    --surface-overlay: rgba(255, 255, 255, 0.90); /* Frosted header glass */

    /* Hairline Precision Borders */
    --border-subtle: #E2E8F0;      /* Slate 200 border */
    --border-card: #CBD5E1;        /* Slate 300 border */
    --border-focus: #4F46E5;       /* Focus ring indigo */

    /* Typographic Ink Tokens - High Contrast & Sharp Legibility */
    --ink-primary: #0F172A;        /* Slate 900 - ultra-sharp primary text */
    --ink-secondary: #334155;      /* Slate 700 - structured secondary text */
    --ink-muted: #64748B;          /* Slate 500 - meta & descriptions */
    --ink-subtle: #94A3B8;         /* Slate 400 - placeholders & hints */

    /* Brand Accent Colors */
    --brand-primary: #4F46E5;      /* Electric Indigo 600 */
    --brand-hover: #4338CA;        /* Indigo 700 */
    --brand-gradient: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
    --brand-light: #EEF2FF;        /* Indigo 50 */
    --brand-border: #C7D2FE;       /* Indigo 200 */
    --brand-glow: 0 4px 14px rgba(79, 70, 229, 0.18);

    /* Purpose-driven Status Accents */
    --status-live: #059669;        /* Emerald 600 */
    --status-live-bg: #ECFDF5;     /* Emerald 50 */
    --status-live-border: #A7F3D0; /* Emerald 200 */
    --status-trace: #0284C7;       /* Sky 600 */
    --status-trace-bg: #F0F9FF;    /* Sky 50 */
    --status-trace-border: #BAE6FD;/* Sky 200 */
    --status-alert: #E11D48;       /* Rose 600 */
    --status-alert-bg: #FFF1F2;    /* Rose 50 */
    --status-alert-border: #FECDD3;/* Rose 200 */
    --status-amber: #D97706;       /* Amber 600 */
    --status-amber-bg: #FFFBEB;    /* Amber 50 */
    --status-amber-border: #FDE68A;/* Amber 200 */

    /* Font Families */
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

    /* Override Gradio Internal Theme Variables */
    --body-background-fill: var(--canvas-bg) !important;
    --body-text-color: var(--ink-primary) !important;
    --body-text-color-subdued: var(--ink-muted) !important;
    --block-background-fill: var(--surface-card) !important;
    --block-border-color: var(--border-subtle) !important;
    --block-border-width: 1px !important;
    --block-label-text-color: var(--ink-secondary) !important;
    --input-background-fill: var(--surface-input) !important;
    --input-border-color: var(--border-card) !important;
    --input-placeholder-color: var(--ink-subtle) !important;
    --input-text-color: var(--ink-primary) !important;
    --button-primary-background-fill: var(--brand-primary) !important;
    --button-primary-background-fill-hover: var(--brand-hover) !important;
    --button-primary-text-color: #FFFFFF !important;
    --button-secondary-background-fill: var(--surface-card) !important;
    --button-secondary-border-color: var(--border-card) !important;
    --button-secondary-text-color: var(--ink-secondary) !important;
    --panel-background-fill: var(--surface-card) !important;
    --panel-border-color: var(--border-subtle) !important;
    --background-fill-primary: var(--canvas-bg) !important;
    --background-fill-secondary: var(--surface-sidebar) !important;
    --border-color-primary: var(--border-subtle) !important;
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

/* Reset Gradio nested container borders */
.gr-group,
.gr-box,
.block,
.form,
fieldset,
.wrap {
    background: transparent !important;
    border-color: var(--border-subtle) !important;
    color: var(--ink-primary) !important;
}

/* ==========================================================================
   TOP APPLICATION BAR (50px High-Precision Glass Header)
   ========================================================================== */
#app-header {
    height: 50px !important;
    min-height: 50px !important;
    max-height: 50px !important;
    flex-shrink: 0 !important;
    background: var(--surface-overlay) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 0 18px !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    z-index: 100 !important;
    box-sizing: border-box !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.app-brand-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #4F46E5 0%, #0284C7 100%);
    border-radius: 8px;
    font-size: 0.90rem;
    color: #FFFFFF;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}

.app-brand-text {
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.app-brand-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin: 0;
    letter-spacing: -0.02em;
    font-family: var(--font-sans);
}

.app-brand-version {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--ink-muted);
    font-family: var(--font-mono);
    background: var(--surface-subtle);
    padding: 1px 7px;
    border-radius: 4px;
    border: 1px solid var(--border-subtle);
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
    border-radius: 6px;
    font-size: 0.70rem;
    font-weight: 600;
    border: 1px solid var(--border-subtle);
    background: var(--surface-card);
    color: var(--ink-secondary);
    white-space: nowrap;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    transition: all 0.15s ease;
}

.status-pill:hover {
    border-color: var(--border-card);
}

.pill-green {
    background: var(--status-live-bg) !important;
    border-color: var(--status-live-border) !important;
    color: var(--status-live) !important;
}

.pill-purple {
    background: var(--brand-light) !important;
    border-color: var(--brand-border) !important;
    color: #4338CA !important;
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
    box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.6);
    animation: dotPulse 2s infinite;
}

@keyframes dotPulse {
    0% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.6); }
    70% { box-shadow: 0 0 0 6px rgba(5, 150, 105, 0); }
    100% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0); }
}

/* ==========================================================================
   3-COLUMN MAIN WORKBENCH CONTAINER
   ========================================================================== */
#app-3-columns {
    display: flex !important;
    flex-direction: row !important;
    flex: 1 1 0% !important;
    height: calc(100vh - 50px) !important;
    max-height: calc(100vh - 50px) !important;
    width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    overflow: hidden !important;
    background-color: var(--canvas-bg) !important;
}

/* Draggable Vertical Splitter Handles */
.col-splitter {
    width: 6px !important;
    min-width: 6px !important;
    max-width: 6px !important;
    height: 100% !important;
    background: transparent !important;
    cursor: col-resize !important;
    position: relative !important;
    z-index: 25 !important;
    flex-shrink: 0 !important;
    margin: 0 -3px !important;
}

.col-splitter::after {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 2px !important;
    width: 2px !important;
    background: transparent !important;
    transition: background 0.15s ease !important;
}

.col-splitter:hover::after,
.col-splitter:active::after {
    background: var(--brand-primary) !important;
    box-shadow: 0 0 6px rgba(79, 70, 229, 0.5) !important;
}

#sidebar-width-control,
#inspector-width-control {
    display: none !important;
}

/* ==========================================================================
   LEFT COLUMN: SIDEBAR (KNOWLEDGE BASE & CHUNKING)
   ========================================================================== */
#col-sidebar {
    flex: 0 0 310px !important;
    width: 310px !important;
    min-width: 220px !important;
    max-width: 550px !important;
    height: 100% !important;
    max-height: 100% !important;
    border-right: 1px solid var(--border-subtle) !important;
    background: var(--surface-sidebar) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding: 12px 10px !important;
    box-sizing: border-box !important;
}

.sidebar-section-card {
    background: var(--surface-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 9px !important;
    padding: 11px 10px !important;
    margin: 0 0 2px 0 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
}

.sidebar-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin-bottom: 6px;
    padding-bottom: 5px;
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
    border: 1px solid var(--border-subtle);
}

.sidebar-badge.live {
    background: var(--status-live-bg);
    color: var(--status-live);
    border-color: var(--status-live-border);
}

/* Ingest Documents Upload Box UI */
[data-testid="file-upload"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: unset !important;
    max-height: unset !important;
    width: 100% !important;
}

button.upload-container,
.upload-container {
    background: var(--surface-subtle) !important;
    border: 1.5px dashed var(--border-card) !important;
    border-radius: 9px !important;
    min-height: 80px !important;
    height: 80px !important;
    max-height: 88px !important;
    width: 100% !important;
    padding: 8px 12px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 2px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    text-align: center !important;
}

button.upload-container:hover {
    border-color: var(--brand-primary) !important;
    background: var(--brand-light) !important;
    box-shadow: 0 0 12px rgba(79, 70, 229, 0.12) !important;
}

button.upload-container::before {
    content: '' !important;
    width: 20px !important;
    height: 20px !important;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234F46E5'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12'%3E%3C/path%3E%3C/svg%3E") no-repeat center center !important;
    background-size: contain !important;
    display: block !important;
    margin-bottom: 2px !important;
}

button.upload-container > div {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: var(--ink-primary) !important;
    line-height: 1.25 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    white-space: normal !important;
    text-align: center !important;
}

button.upload-container > span {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    color: var(--brand-primary) !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}

#col-sidebar button.primary,
#col-sidebar button[variant="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 7px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    height: 33px !important;
    min-height: 33px !important;
    margin-top: 4px !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25) !important;
    transition: all 0.15s ease !important;
}

#col-sidebar button.primary:hover,
#col-sidebar button[variant="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.40) !important;
    transform: translateY(-1px) !important;
}

/* ==========================================================================
   INDEXED DOCUMENTS SECTION
   ========================================================================== */
.indexed-docs-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-top: 14px !important;
    margin-bottom: 7px !important;
    padding: 0 1px !important;
}

.section-title-left {
    display: flex !important;
    align-items: center !important;
    gap: 7px !important;
}

.section-title-text {
    font-size: 0.80rem !important;
    font-weight: 700 !important;
    color: var(--ink-primary) !important;
    letter-spacing: -0.01em !important;
}

.sidebar-counter-pill {
    background: var(--brand-light) !important;
    border: 1px solid var(--brand-border) !important;
    color: #4338CA !important;
    font-size: 0.64rem !important;
    font-weight: 600 !important;
    font-family: var(--font-mono) !important;
    padding: 1px 7px !important;
    border-radius: 9999px !important;
    line-height: 1.2 !important;
}

.status-dot-pulse {
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    background: var(--status-live) !important;
    display: inline-block !important;
    margin-right: 4px !important;
    box-shadow: 0 0 6px var(--status-live) !important;
}

.doc-list-scroll {
    max-height: 185px !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding: 2px !important;
}

.doc-list-scroll::-webkit-scrollbar {
    width: 4px !important;
}

.doc-list-scroll::-webkit-scrollbar-track {
    background: transparent !important;
}

.doc-list-scroll::-webkit-scrollbar-thumb {
    background: #CBD5E1 !important;
    border-radius: 4px !important;
}

.doc-list-scroll::-webkit-scrollbar-thumb:hover {
    background: #94A3B8 !important;
}

.doc-card {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 7px 9px !important;
    display: flex !important;
    align-items: center !important;
    gap: 9px !important;
    cursor: default !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

.doc-card:hover {
    background: var(--surface-subtle) !important;
    border-color: #A5B4FC !important;
    transform: translateX(2px) !important;
    box-shadow: 0 3px 8px rgba(79, 70, 229, 0.08) !important;
}

.doc-badge {
    width: 28px !important;
    height: 28px !important;
    border-radius: 6px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    transition: transform 0.15s ease !important;
}

.doc-badge.pdf {
    background: var(--status-alert-bg) !important;
    border: 1px solid var(--status-alert-border) !important;
    color: var(--status-alert) !important;
}

.doc-badge.md {
    background: var(--status-trace-bg) !important;
    border: 1px solid var(--status-trace-border) !important;
    color: var(--status-trace) !important;
}

.doc-badge.generic {
    background: #FAF5FF !important;
    border: 1px solid #E9D5FF !important;
    color: #7C3AED !important;
}

.doc-card-body {
    flex: 1 !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 3px !important;
}

.doc-card-title-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 6px !important;
}

.doc-card-filename {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: var(--ink-primary) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.2 !important;
}

.doc-badge-pill {
    font-size: 0.60rem !important;
    font-weight: 700 !important;
    font-family: var(--font-mono) !important;
    padding: 1px 5px !important;
    border-radius: 4px !important;
    line-height: 1.1 !important;
    flex-shrink: 0 !important;
}

.doc-badge-pill.pdf {
    background: #FFE4E6 !important;
    color: #BE123C !important;
}

.doc-badge-pill.md {
    background: #E0F2FE !important;
    color: #0369A1 !important;
}

.doc-badge-pill.generic {
    background: #F3E8FF !important;
    color: #6D28D9 !important;
}

.doc-card-meta-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    font-size: 0.66rem !important;
    font-family: var(--font-mono) !important;
}

.doc-chunk-count {
    color: var(--brand-primary) !important;
    font-weight: 600 !important;
    display: flex !important;
    align-items: center !important;
    gap: 3px !important;
}

.doc-meta-icon {
    font-size: 0.62rem !important;
    color: var(--brand-primary) !important;
}

.doc-status-synced {
    color: var(--status-live) !important;
    font-weight: 600 !important;
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
}

.synced-dot {
    width: 5px !important;
    height: 5px !important;
    border-radius: 50% !important;
    background: var(--status-live) !important;
    display: inline-block !important;
    box-shadow: 0 0 4px var(--status-live) !important;
}

.doc-empty-state {
    padding: 22px 14px !important;
    text-align: center !important;
    border: 1.5px dashed var(--border-card) !important;
    border-radius: 8px !important;
    background: var(--surface-subtle) !important;
    margin: 4px 0 !important;
}

.doc-empty-icon {
    color: var(--ink-muted) !important;
    margin-bottom: 6px !important;
    display: flex !important;
    justify-content: center !important;
}

.doc-empty-title {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: var(--ink-secondary) !important;
}

.doc-empty-hint {
    font-size: 0.67rem !important;
    color: var(--ink-muted) !important;
    margin-top: 3px !important;
}

/* Document Action Buttons */
.doc-actions-row {
    margin-top: 7px !important;
    margin-bottom: 3px !important;
    gap: 7px !important;
}

#btn-refresh-docs {
    background: #FFFFFF !important;
    border: 1px solid var(--border-card) !important;
    color: var(--ink-secondary) !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    height: 31px !important;
    min-height: 31px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.15s ease !important;
}

#btn-refresh-docs:hover {
    background: var(--surface-subtle) !important;
    border-color: var(--brand-primary) !important;
    color: var(--ink-primary) !important;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.15) !important;
}

#btn-clear-docs {
    background: var(--status-alert-bg) !important;
    border: 1px solid var(--status-alert-border) !important;
    color: var(--status-alert) !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    height: 31px !important;
    min-height: 31px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.15s ease !important;
}

#btn-clear-docs:hover {
    background: #FFE4E6 !important;
    border-color: #FDA4AF !important;
    color: #BE123C !important;
    box-shadow: 0 2px 6px rgba(225, 29, 72, 0.18) !important;
}

/* Chunk Analytics Bento Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    margin: 4px 0;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    border-radius: 7px;
    padding: 6px 8px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.stat-card:hover {
    border-color: var(--border-card);
    transform: translateY(-1px);
    background: var(--surface-subtle);
}

.stat-value {
    font-family: var(--font-mono);
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--brand-primary);
}

.stat-value.val-docs { color: #0284C7 !important; }
.stat-value.val-parents { color: #4F46E5 !important; }
.stat-value.val-children { color: #7C3AED !important; }
.stat-value.val-avg { color: #059669 !important; }

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
    border-radius: 7px;
    padding: 8px 10px;
    font-size: 0.72rem;
}

.strategy-row {
    margin-bottom: 4px;
    display: flex;
    flex-direction: column;
}

.strategy-row:last-child { margin-bottom: 0; }
.strategy-label { font-size: 0.63rem; font-weight: 600; color: var(--ink-muted); }
.strategy-content { font-size: 0.70rem; color: var(--ink-secondary); margin-top: 1px; }

/* ==========================================================================
   MIDDLE COLUMN: MAIN CHAT & CONVERSATIONAL WORKBENCH
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
    padding: 14px 20px 10px 20px !important;
    box-sizing: border-box !important;
}

.chat-column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 8px;
    margin-bottom: 6px;
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

/* Empty Hero Card inside Chat */
.empty-chat-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 44px 16px;
    max-width: 540px;
    margin: auto;
}

.hero-icon-badge {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #EEF2FF 0%, #E0F2FE 100%);
    border: 1px solid #C7D2FE;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    color: #4F46E5;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.12);
}

.hero-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin: 0 0 8px 0;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 0.84rem;
    color: var(--ink-secondary);
    line-height: 1.6;
    margin: 0;
}

/* Chat Message Bubbles */
.message.user,
[data-testid="user"] .message,
div[class*="user"] > .message {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border-radius: 14px 14px 2px 14px !important;
    padding: 10px 16px !important;
    font-size: 13.5px !important;
    line-height: 1.55 !important;
    max-width: 78% !important;
    margin-left: auto !important;
    box-shadow: 0 3px 10px rgba(79, 70, 229, 0.25) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.message.user * {
    color: #FFFFFF !important;
}

.message.bot,
[data-testid="bot"] .message,
div[class*="bot"] > .message {
    background: #FFFFFF !important;
    color: var(--ink-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px 14px 14px 2px !important;
    padding: 14px 18px !important;
    font-size: 13.5px !important;
    line-height: 1.6 !important;
    max-width: 84% !important;
    margin-right: auto !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.message.bot * {
    color: var(--ink-primary) !important;
}

.message.bot pre,
.message.bot code {
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    background: var(--surface-subtle) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 5px !important;
    padding: 2px 6px !important;
    color: var(--ink-primary) !important;
}

.message.bot pre code {
    padding: 10px 14px !important;
    display: block !important;
    background: #0F172A !important;
    color: #F8FAFC !important;
}

.chatbot details {
    background: var(--surface-subtle) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 7px !important;
    margin: 6px 0 !important;
    padding: 6px 10px !important;
}

.chatbot summary {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: var(--brand-primary) !important;
    cursor: pointer !important;
}

/* Quick Prompts Row */
#quick-prompts-row {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    margin-bottom: 8px !important;
    margin-top: 4px !important;
    flex-shrink: 0 !important;
    overflow-x: auto !important;
    padding-bottom: 2px !important;
}

.quick-prompt-btn,
#quick-prompts-row button {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    padding: 4px 12px !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: var(--ink-secondary) !important;
    white-space: nowrap !important;
    height: 28px !important;
    min-height: 28px !important;
    line-height: 1 !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.15s ease !important;
}

.quick-prompt-btn:hover,
#quick-prompts-row button:hover {
    border-color: var(--brand-primary) !important;
    color: var(--brand-primary) !important;
    background: var(--brand-light) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.15) !important;
}

/* Search Accordion Drawer */
#search-accordion {
    margin-top: 4px !important;
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    flex-shrink: 0 !important;
}

#search-accordion summary {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    color: #0284C7 !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
    background: var(--surface-subtle) !important;
}

#search-results-panel {
    max-height: 150px !important;
    overflow-y: auto !important;
    padding: 10px 12px !important;
    font-size: 0.78rem !important;
    background: #FFFFFF !important;
}

.search-chunk-card {
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 7px;
    padding: 8px 10px;
    margin-bottom: 6px;
    transition: all 0.15s ease;
}

.search-chunk-card:hover {
    border-color: var(--brand-border);
    background: #FFFFFF;
}

.search-chunk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 5px;
    font-size: 0.74rem;
    color: #0284C7;
    font-weight: 600;
}

.search-chunk-content {
    font-family: var(--font-sans);
    font-size: 0.74rem;
    color: var(--ink-secondary);
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    padding: 7px 10px;
    border-radius: 5px;
    white-space: pre-wrap;
    line-height: 1.45;
}

/* Chat Input Bar Pinned at Bottom */
#chat-input-row {
    flex-shrink: 0 !important;
    gap: 8px !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
    padding-top: 6px !important;
    border-top: 1px solid var(--border-subtle) !important;
}

#chat-input-box textarea {
    background: #FFFFFF !important;
    border: 1.5px solid var(--border-card) !important;
    border-radius: 8px !important;
    color: var(--ink-primary) !important;
    font-size: 13.5px !important;
    font-family: var(--font-sans) !important;
    padding: 9px 14px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.15s ease !important;
}

#chat-input-box textarea:focus {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
    background: #FFFFFF !important;
}

/* ==========================================================================
   RIGHT COLUMN: AGENT INSPECTOR & TELEMETRY PANEL
   ========================================================================== */
#col-inspector {
    flex: 0 0 330px !important;
    width: 330px !important;
    min-width: 220px !important;
    max-width: 600px !important;
    height: 100% !important;
    max-height: 100% !important;
    background: var(--surface-sidebar) !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding: 12px 10px !important;
    box-sizing: border-box !important;
    border-left: 1px solid var(--border-subtle) !important;
}

.compact-agent-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    margin-bottom: 2px;
}

.compact-agent-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.compact-avatar {
    width: 24px;
    height: 24px;
    border-radius: 6px;
    background-color: var(--brand-light);
    border: 1px solid var(--brand-border);
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
    color: #4338CA;
    background: var(--brand-light);
    border: 1px solid var(--brand-border);
    padding: 2px 7px;
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
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    border-radius: 7px;
    padding: 6px 5px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
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
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 7px !important;
    padding: 10px !important;
    max-height: calc(100vh - 195px) !important;
    overflow-y: auto !important;
}

/* Segmented Tabs */
#observability-tabs [role="tablist"] {
    background: var(--surface-subtle) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 7px !important;
    padding: 3px !important;
    gap: 3px !important;
}

button[role="tab"] {
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    color: var(--ink-muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 5px 12px !important;
    border-radius: 5px !important;
    transition: all 0.15s ease !important;
}

button[role="tab"][aria-selected="true"] {
    color: var(--ink-primary) !important;
    background: #FFFFFF !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid var(--border-card) !important;
}

/* State Machine Stepper */
.stepper-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin: 5px 0;
}

.stepper-item {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 9px;
    background: var(--surface-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: 7px;
    font-size: 0.74rem;
    transition: all 0.15s ease;
}

.stepper-item.active {
    background: var(--brand-light);
    border-color: var(--brand-primary);
    box-shadow: 0 0 8px rgba(79, 70, 229, 0.15);
}

.stepper-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    color: var(--ink-muted);
    font-weight: 700;
    font-size: 0.65rem;
    flex-shrink: 0;
}

.stepper-item.active .stepper-num {
    background: var(--brand-primary);
    color: #FFFFFF;
    border-color: var(--brand-primary);
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
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 7px !important;
    overflow: hidden !important;
}

th {
    background: var(--surface-subtle) !important;
    color: var(--ink-secondary) !important;
    padding: 6px 8px !important;
    font-weight: 600 !important;
    border: 1px solid var(--border-subtle) !important;
    font-size: 0.65rem !important;
}

td {
    padding: 5px 8px !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--ink-secondary) !important;
}

/* Universal Button Styling */
button {
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    font-family: var(--font-sans) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

.primary, button[variant="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 1px 6px rgba(79, 70, 229, 0.25) !important;
}

.primary:hover, button[variant="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
    box-shadow: 0 3px 12px rgba(79, 70, 229, 0.35) !important;
}

.secondary, button[variant="secondary"] {
    background: #FFFFFF !important;
    color: var(--ink-secondary) !important;
    border: 1px solid var(--border-card) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

.secondary:hover, button[variant="secondary"]:hover {
    background: var(--surface-subtle) !important;
    color: var(--ink-primary) !important;
    border-color: var(--brand-primary) !important;
}

.stop, button[variant="stop"] {
    background: var(--status-alert-bg) !important;
    color: var(--status-alert) !important;
    border: 1px solid var(--status-alert-border) !important;
}

.stop:hover, button[variant="stop"]:hover {
    background: #FFE4E6 !important;
    border-color: #FDA4AF !important;
    color: #BE123C !important;
}

button:active {
    transform: scale(0.98) !important;
}

.badge-tag {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.64rem;
    font-weight: 600;
    font-family: var(--font-mono);
}

.badge-pdf { background: var(--status-alert-bg); color: var(--status-alert); border: 1px solid var(--status-alert-border); }
.badge-md { background: var(--status-trace-bg); color: var(--status-trace); border: 1px solid var(--status-trace-border); }
.badge-chunks { background: var(--brand-light); color: var(--brand-primary); border: 1px solid var(--brand-border); }

/* Sleek Light Scrollbars */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
"""