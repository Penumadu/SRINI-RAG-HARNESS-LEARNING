"""
==============================================================================
run_learning.py — Interactive Runner & Learning Navigator
==============================================================================
Provides a guided terminal dashboard to explore, test, and run all components
of the Agentic RAG system with zero guesswork.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure workspace root is in sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning import config


def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AGENTIC RAG FOR DUMMIES RUNNER                         ║
║         Hierarchical Indexing • LangGraph Agents • Human-in-the-Loop         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_environment():
    """Validates python packages, environment variables, and Ollama/API status."""
    print("\n🔍 Checking Local Environment & Dependencies:")
    print("─" * 60)
    print(f"  • Python Version  : {sys.version.split()[0]}")
    print(f"  • Workspace Root  : {_ROOT}")
    print(f"  • LLM Provider    : {config.LLM_PROVIDER}")
    print(f"  • LLM Model       : {config.LLM_MODEL}")
    print(f"  • Ollama Base URL : {config.OLLAMA_BASE_URL}")

    packages = [
        ("langchain_ollama", "Ollama LLM integration"),
        ("langgraph", "Multi-Agent Graph Orchestration"),
        ("qdrant_client", "Vector Database"),
        ("fastembed", "Sparse BM25 Embeddings"),
        ("pymupdf4llm", "PDF to Markdown Parser"),
        ("gradio", "Interactive Web UI"),
        ("langfuse", "Telemetry Observability"),
    ]

    print("\n📦 Dependency Status:")
    all_ok = True
    for pkg, desc in packages:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg:<18}: Installed ({desc})")
        except ImportError:
            print(f"  ✗ {pkg:<18}: MISSING ({desc})")
            all_ok = False

    if not all_ok:
        print("\n💡 To install all required dependencies, run:")
        print("   pip install -r requirements.txt")

    # Generate sample docs if missing
    md_files = list(Path(config.MARKDOWN_DIR).glob("*.md"))
    if not md_files:
        print("\n📄 Generating initial sample documents in markdown_docs/...")
        from learning.sample_docs import create_sample_documents
        create_sample_documents()
    else:
        print(f"\n✓ Found {len(md_files)} markdown documents ready in '{config.MARKDOWN_DIR}'.")

    print("─" * 60 + "\n")


def run_menu():
    while True:
        print_banner()
        print("  [1] 📄 PDF to Markdown (Inspect & Validate Documents)")
        print("  [2] 🤖 Agentic RAG Pipeline (Index, Terminal Chat, or Web UI)")
        print("  [3] 🔍 Observability & Live Telemetry Tracing")
        print("  [4] 📊 Benchmark Evaluation (RAGAS Metrics on QA dataset)")
        print("  [5] 🚀 Launch Production Gradio App (project/app.py)")
        print("  [6] 🛠️ Run Diagnostics & Check Dependencies")
        print("  [0] ❌ Exit")
        print()

        try:
            choice = input("Select an option [0-6]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if choice == "0":
            print("Happy learning! Goodbye 👋")
            break

        elif choice == "1":
            print("\n--- PDF to Markdown Menu ---")
            print("  [1] Run demonstration and audit existing markdown quality")
            print("  [2] Validate a specific markdown file")
            sub = input("Choose [1-2]: ").strip()
            if sub == "2":
                f = input("Enter path to markdown file: ").strip()
                subprocess.run([sys.executable, str(_ROOT / "learning" / "01_pdf_to_markdown.py"), "--validate", f])
            else:
                subprocess.run([sys.executable, str(_ROOT / "learning" / "01_pdf_to_markdown.py"), "--demo"])

        elif choice == "2":
            print("\n--- Agentic RAG Menu ---")
            print("  [1] Index documents into Qdrant & Parent store")
            print("  [2] Start interactive Terminal Chat with memory")
            print("  [3] Ask a single query")
            print("  [4] Launch Gradio Web UI")
            sub = input("Choose [1-4]: ").strip()
            rag_script = str(_ROOT / "learning" / "02_agentic_rag.py")
            if sub == "1":
                subprocess.run([sys.executable, rag_script, "--index"])
            elif sub == "2":
                subprocess.run([sys.executable, rag_script, "--chat"])
            elif sub == "3":
                q = input("Enter your question: ").strip()
                subprocess.run([sys.executable, rag_script, "--query", q])
            elif sub == "4":
                subprocess.run([sys.executable, rag_script, "--ui"])

        elif choice == "3":
            obs_script = str(_ROOT / "learning" / "03_observability.py")
            subprocess.run([sys.executable, obs_script, "--demo-trace"])

        elif choice == "4":
            print("\n--- Benchmark Evaluation Menu ---")
            print("  [1] Quick test run (first 3 questions)")
            print("  [2] Full evaluation on entire benchmark (30 questions)")
            sub = input("Choose [1-2]: ").strip()
            eval_script = str(_ROOT / "learning" / "04_evaluation.py")
            if sub == "1":
                subprocess.run([sys.executable, eval_script, "--sample-size", "3"])
            else:
                subprocess.run([sys.executable, eval_script])

        elif choice == "5":
            app_script = str(_ROOT / "project" / "app.py")
            print("\nLaunching Project App...")
            subprocess.run([sys.executable, app_script])

        elif choice == "6":
            check_environment()

        else:
            print("⚠️ Invalid choice. Please enter a number between 0 and 6.")

        input("\nPress [Enter] to return to main menu...")


if __name__ == "__main__":
    run_menu()
