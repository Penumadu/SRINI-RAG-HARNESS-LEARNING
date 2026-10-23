custom_css = """
    /* ==========================================================================
       GLOBAL CONTAINER & BASE STYLING
       ========================================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-main: #0b0f19;
        --bg-card: #111827;
        --bg-card-subtle: #172033;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-accent: rgba(99, 102, 241, 0.3);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --primary-blue: #3b82f6;
        --primary-indigo: #6366f1;
        --accent-emerald: #10b981;
        --accent-amber: #f59e0b;
        --accent-rose: #f43f5e;
    }

    * {
        box-sizing: border-box;
    }

    .gradio-container {
        max-width: 100% !important;
        width: 100% !important;
        min-height: 100vh !important;
        margin: 0 auto !important;
        padding: 16px 24px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    footer {
        display: none !important;
    }

    /* ==========================================================================
       TOP HEADER BAR
       ========================================================================== */
    #top-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4) !important;
    }

    #top-header h1 {
        margin: 0 0 4px 0 !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    #top-header p {
        margin: 0 !important;
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
    }

    .status-badge-container {
        display: flex;
        gap: 8px;
        align-items: center;
        justify-content: flex-end;
        flex-wrap: wrap;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-subtle);
        color: #e2e8f0;
    }

    .pill-green {
        background: rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.35);
        color: #34d399;
    }

    .pill-purple {
        background: rgba(139, 92, 246, 0.12);
        border-color: rgba(139, 92, 246, 0.35);
        color: #a78bfa;
    }

    .pill-blue {
        background: rgba(59, 130, 246, 0.12);
        border-color: rgba(59, 130, 246, 0.35);
        color: #60a5fa;
    }

    /* ==========================================================================
       THREE COLUMN LAYOUT
       ========================================================================== */
    #main-3-col-layout {
        gap: 16px !important;
        align-items: stretch !important;
    }

    #left-col,
    #mid-col,
    #right-col {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.3) !important;
    }

    /* Section Titles */
    .column-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 10px;
        margin-bottom: 14px;
        border-bottom: 1px solid var(--border-subtle);
    }

    .column-header h2,
    .column-header h3 {
        margin: 0 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #f1f5f9 !important;
    }

    /* ==========================================================================
       LEFT COLUMN: UPLOAD & CHUNK METRICS
       ========================================================================== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin: 10px 0;
    }

    .metric-card {
        background: var(--bg-card-subtle);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 10px 12px;
        text-align: center;
    }

    .metric-num {
        font-size: 1.35rem;
        font-weight: 700;
        color: #60a5fa;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }

    .chunk-info-card {
        background: var(--bg-card-subtle);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
        font-size: 0.82rem;
        color: var(--text-secondary);
    }

    .chunk-info-item {
        margin-bottom: 8px;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .chunk-info-item:last-child {
        margin-bottom: 0;
    }

    .chunk-info-title {
        font-weight: 600;
        color: #cbd5e1;
        font-size: 0.78rem;
    }

    .chunk-info-badge {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }

    .doc-list-container {
        max-height: 160px;
        overflow-y: auto;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 8px;
        margin: 8px 0;
    }

    .doc-item-pill {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 10px;
        margin-bottom: 4px;
        background: var(--bg-card-subtle);
        border-radius: 6px;
        font-size: 0.8rem;
        color: #e2e8f0;
    }

    /* File drop upload styling */
    [data-testid="file-upload"],
    .file-preview {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px dashed rgba(99, 102, 241, 0.4) !important;
        border-radius: 10px !important;
        min-height: 110px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="file-upload"]:hover,
    .file-preview:hover {
        border-color: #6366f1 !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }

    /* ==========================================================================
       MIDDLE COLUMN: CHAT & SEARCH RESULTS
       ========================================================================== */
    .chatbot {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        overflow-y: auto !important;
    }

    .message.user {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border-radius: 14px 14px 2px 14px !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
        padding: 10px 14px !important;
    }

    .message.bot {
        background: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px 14px 14px 2px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    #chat-input-row {
        gap: 8px !important;
        align-items: center !important;
        margin-top: 10px !important;
    }

    #chat-input-box textarea {
        background: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        padding: 10px 14px !important;
        font-size: 0.92rem !important;
    }

    #chat-input-box textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    #search-results-panel {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        max-height: 280px !important;
        overflow-y: auto !important;
        font-size: 0.85rem !important;
    }

    /* ==========================================================================
       RIGHT COLUMN: OBSERVABILITY & MEMORY
       ========================================================================== */
    #observability-panel,
    #memory-panel {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        max-height: 640px !important;
        overflow-y: auto !important;
        font-size: 0.84rem !important;
    }

    /* Tables in Observability */
    table {
        width: 100% !important;
        border-collapse: collapse !important;
        margin: 8px 0 !important;
        font-size: 0.76rem !important;
    }

    th {
        background: #1e293b !important;
        color: #cbd5e1 !important;
        padding: 6px 8px !important;
        border: 1px solid var(--border-subtle) !important;
        text-align: left !important;
    }

    td {
        padding: 5px 8px !important;
        border: 1px solid var(--border-subtle) !important;
        color: #94a3b8 !important;
    }

    tr:nth-child(even) td {
        background: rgba(255, 255, 255, 0.02) !important;
    }

    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 4px !important;
        padding: 2px 5px !important;
        font-size: 0.78rem !important;
        color: #38bdf8 !important;
    }

    pre code {
        display: block !important;
        padding: 8px 12px !important;
        overflow-x: auto !important;
        white-space: pre-wrap !important;
    }

    /* ==========================================================================
       BUTTONS
       ========================================================================== */
    button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    }

    button:hover {
        transform: translateY(-1px) !important;
    }

    .primary,
    button[variant="primary"] {
        background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .primary:hover,
    button[variant="primary"]:hover {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    }

    .stop,
    button[variant="stop"] {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }

    .stop:hover,
    button[variant="stop"]:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        color: #fca5a5 !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.25);
    }
"""