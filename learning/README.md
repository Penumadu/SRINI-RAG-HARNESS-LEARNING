# 🎓 Agentic RAG for Dummies — Learning Path (Local Python Files)

This folder contains the complete conversion of the interactive Jupyter notebooks into **clean, well-commented, standalone, and executable Python files**. You can read them to learn every concept in detail and run them directly from your local terminal or IDE.

---

## 🗂️ Converted Modules Overview

| Original Notebook | Local Python Script | Description |
|---|---|---|
| `notebooks/pdf_to_markdown.ipynb` | [`learning/01_pdf_to_markdown.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/01_pdf_to_markdown.py) | **3-Tier PDF Parsing & Quality Audit**: Demonstrates Category 1 (PyMuPDF4LLM), Category 2 (Docling OCR), Category 3 (VLM / Gemini Vision), plus smart routing and quality metrics. |
| `notebooks/agentic_rag.ipynb` | [`learning/02_agentic_rag.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/02_agentic_rag.py) | **Complete Agentic RAG System**: Hierarchical chunking (Parent/Child), Qdrant hybrid vector store, LangGraph agents, rolling memory, query clarification, map-reduce, and interactive chat / Gradio UI. |
| `notebooks/observability.ipynb` | [`learning/03_observability.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/03_observability.py) | **Telemetry & Tracing**: Explains sessions, traces, spans, and generations with Langfuse. Includes live console trace visualization. |
| `notebooks/evaluation.ipynb` | [`learning/04_evaluation.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/04_evaluation.py) | **Benchmark Evaluation**: Evaluates RAG performance across 30 curated questions with RAGAS metrics (accuracy, relevance, groundedness, precision, recall), generates summary charts and CSV reports. |
| *Runner* | [`run.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/run.py) / [`learning/run_learning.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/run_learning.py) | **Interactive Terminal Dashboard**: Guided terminal menu to run any module, inspect dependencies, and launch tests. |
| *Sample Docs* | [`learning/sample_docs.py`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/learning/sample_docs.py) | Generates initial sample reference documents (`javascript_tutorial.md`, `blockchain.md`, `fortinet.md`) in `markdown_docs/` for immediate out-of-the-box testing. |

---

## ⚙️ Configuration (`.env`)

A root [`.env`](file:///Users/srinivasulu/Documents/Srini%20Learning/agentic-rag-for-dummies/.env) file is provided and pre-configured.

### 1. Local Ollama (Default)
Runs 100% locally with zero external API calls:
```env
LLM_PROVIDER=ollama
LLM_MODEL=granite4.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```
Ensure Ollama is running and you have pulled the model:
```bash
ollama run granite4.1:8b
# or: ollama run qwen2.5:7b / ollama run llama3.1:8b
```

### 2. Cloud Providers (Optional)
Switch providers anytime by changing `LLM_PROVIDER`:
- **OpenAI**:
  ```env
  LLM_PROVIDER=openai
  LLM_MODEL=gpt-4o-mini
  OPENAI_API_KEY=sk-...
  ```
- **Anthropic**:
  ```env
  LLM_PROVIDER=anthropic
  LLM_MODEL=claude-3-5-haiku-20241022
  ANTHROPIC_API_KEY=sk-ant-...
  ```
- **Google Gemini**:
  ```env
  LLM_PROVIDER=google
  LLM_MODEL=gemini-1.5-flash
  GOOGLE_API_KEY=AIza...
  ```

---

## 🚀 Quick Start Guide

### 1. Launch the Interactive Dashboard
The simplest way to explore and run the project:
```bash
python run.py
```
You will see the guided menu:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AGENTIC RAG FOR DUMMIES RUNNER                         ║
║         Hierarchical Indexing • LangGraph Agents • Human-in-the-Loop         ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📄 PDF to Markdown (Inspect & Validate Documents)
  [2] 🤖 Agentic RAG Pipeline (Index, Terminal Chat, or Web UI)
  [3] 🔍 Observability & Live Telemetry Tracing
  [4] 📊 Benchmark Evaluation (RAGAS Metrics on QA dataset)
  [5] 🚀 Launch Production Gradio App (project/app.py)
  [6] 🛠️ Run Diagnostics & Check Dependencies
  [0] ❌ Exit
```

---

### 2. Running Individual Modules Directly via CLI

#### Module 1: PDF to Markdown & Quality Audit
```bash
# Run demonstration auditing existing markdown files
python learning/01_pdf_to_markdown.py --demo

# Validate a specific markdown file
python learning/01_pdf_to_markdown.py --validate markdown_docs/javascript_tutorial.md

# Convert a PDF with smart routing (simple, scanned, or complex)
python learning/01_pdf_to_markdown.py --input path/to/doc.pdf --method smart
```

#### Module 2: Agentic RAG (Index, Chat, UI)
```bash
# Step 1: Index markdown files into Qdrant & Parent store
python learning/02_agentic_rag.py --index

# Step 2: Ask a single question via CLI
python learning/02_agentic_rag.py --query "What are the main advantages of client-side JavaScript?"

# Step 3: Start an interactive terminal conversation with memory
python learning/02_agentic_rag.py --chat

# Step 4: Launch local Gradio Web UI
python learning/02_agentic_rag.py --ui
```

#### Module 3: Observability & Tracing
```bash
# Validate Langfuse configuration and credentials
python learning/03_observability.py --check

# Run simulated live telemetry trace in console
python learning/03_observability.py --demo-trace
```

#### Module 4: Evaluation with Benchmark QA
```bash
# Quick test on first 3 benchmark questions
python learning/04_evaluation.py --sample-size 3

# Full benchmark evaluation across all 30 questions
python learning/04_evaluation.py
```

---

## 🏗️ How the Agentic RAG Workflow Works

```
                       ┌────────────────────────────┐
                       │   User Query Received      │
                       └─────────────┬──────────────┘
                                     │
                                     ▼
                       ┌────────────────────────────┐
                       │  Rolling Summary Pruning   │
                       └─────────────┬──────────────┘
                                     │
                                     ▼
                       ┌────────────────────────────┐
                       │  Query Analysis & Rewrite  │
                       └───────┬──────────────┬─────┘
                               │              │
                   Need Clarification?    Clear Query
                               │              │
                               ▼              ▼
                     ┌──────────────────┐   ┌─────────────────────────────┐
                     │ Pause & Ask User │   │ Fan-Out: Parallel Sub-Agents│
                     │(Human-in-the-Loop│   └──────────────┬──────────────┘
                     └──────────────────┘                  │
                                           ┌───────────────┴───────────────┐
                                           │                               │
                                           ▼                               ▼
                                   ┌───────────────┐               ┌───────────────┐
                                   │ Sub-Agent 1   │               │ Sub-Agent 2   │
                                   │ - Search Child│               │ - Search Child│
                                   │ - Get Parent  │               │ - Get Parent  │
                                   │ - Compress Ctx│               │ - Compress Ctx│
                                   └───────┬───────┘               └───────┬───────┘
                                           │                               │
                                           └───────────────┬───────────────┘
                                                           │
                                                           ▼
                                            ┌─────────────────────────────┐
                                            │ Final Answer Aggregation    │
                                            └─────────────────────────────┘
```

Enjoy learning and running Agentic RAG locally!
