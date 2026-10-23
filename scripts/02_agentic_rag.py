import sys
import importlib
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

module = importlib.import_module('learning.02_agentic_rag')

if __name__ == '__main__':
    module.main()
