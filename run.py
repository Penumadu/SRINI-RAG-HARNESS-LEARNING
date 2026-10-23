"""
Top-level entry point for running the Agentic RAG Learning and Runner dashboard.
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning.run_learning import run_menu

if __name__ == "__main__":
    run_menu()
