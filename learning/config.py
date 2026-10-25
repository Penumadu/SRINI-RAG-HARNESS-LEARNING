"""
Configuration module for Agentic RAG Learning and Production runs.
Supports local Ollama by default, with optional switches for OpenAI, Anthropic, and Google Gemini.
"""

import os
from pathlib import Path
# Locate base directories
_CURRENT_DIR = Path(__file__).resolve().parent
_WORKSPACE_ROOT = _CURRENT_DIR.parent

# Load environment variables from workspace root or current dir
try:
    from dotenv import load_dotenv
    load_dotenv(_WORKSPACE_ROOT / ".env")
    load_dotenv(_CURRENT_DIR / ".env")
except ImportError:
    def _parse_env_file(path: Path):
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("\"'")
                    if k not in os.environ:
                        os.environ[k] = v
    _parse_env_file(_WORKSPACE_ROOT / ".env")
    _parse_env_file(_CURRENT_DIR / ".env")

# --- Directory Configuration ---
BASE_DIR = _WORKSPACE_ROOT
MARKDOWN_DIR = os.environ.get("MARKDOWN_DIR", str(BASE_DIR / "markdown_docs"))
DOCS_DIR = os.environ.get("DOCS_DIR", str(BASE_DIR / "docs"))
PARENT_STORE_PATH = os.environ.get("PARENT_STORE_PATH", str(BASE_DIR / "parent_store"))
QDRANT_DB_PATH = os.environ.get("QDRANT_DB_PATH", str(BASE_DIR / "qdrant_db"))
QA_DATASET_PATH = os.environ.get(
    "QA_DATASET_PATH", 
    str(BASE_DIR / "notebooks" / "data" / "curated_ragas_qa.json")
)

# Ensure required directories exist
for _p in [MARKDOWN_DIR, DOCS_DIR, PARENT_STORE_PATH, QDRANT_DB_PATH]:
    os.makedirs(_p, exist_ok=True)

# --- Qdrant Vector DB Configuration ---
CHILD_COLLECTION = os.environ.get("CHILD_COLLECTION", "document_child_chunks")
SPARSE_VECTOR_NAME = os.environ.get("SPARSE_VECTOR_NAME", "sparse")

# --- Model Configuration ---
# Provider options: "ollama", "openai", "anthropic", "google"
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama").lower()

# Default model names per provider
DEFAULT_MODELS = {
    "ollama": "granite4.1:8b",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "google": "gemini-1.5-flash",
}

DEFAULT_JUDGE_MODELS = {
    "ollama": "ministral-3:3b-instruct-2512-q8_0",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "google": "gemini-1.5-flash",
}

LLM_MODEL = os.environ.get("LLM_MODEL", DEFAULT_MODELS.get(LLM_PROVIDER, "granite4.1:8b"))
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", DEFAULT_JUDGE_MODELS.get(LLM_PROVIDER, "ministral-3:3b-instruct-2512-q8_0"))
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0"))
LLM_SEED = int(os.environ.get("LLM_SEED", "42"))
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

# Embeddings
DENSE_MODEL = os.environ.get("DENSE_MODEL", "Qwen/Qwen3-Embedding-0.6B")
SPARSE_MODEL = os.environ.get("SPARSE_MODEL", "Qdrant/bm25")

# --- Retrieval Configuration ---
RETRIEVAL_SCORE_THRESHOLD = float(os.environ.get("RETRIEVAL_SCORE_THRESHOLD", "0.4"))
DEFAULT_RETRIEVAL_K = int(os.environ.get("DEFAULT_RETRIEVAL_K", "7"))
CHILD_CHUNK_SEPARATOR = "\n\n<CHILD_CHUNK_BOUNDARY>\n\n"

# --- Agent Configuration ---
MAX_TOOL_CALLS = int(os.environ.get("MAX_TOOL_CALLS", "8"))
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "10"))
GRAPH_RECURSION_LIMIT = int(os.environ.get("GRAPH_RECURSION_LIMIT", "50"))
MAIN_HISTORY_MESSAGES_TO_KEEP = int(os.environ.get("MAIN_HISTORY_MESSAGES_TO_KEEP", "4"))
BASE_TOKEN_THRESHOLD = int(os.environ.get("BASE_TOKEN_THRESHOLD", "2000"))
TOKEN_GROWTH_FACTOR = float(os.environ.get("TOKEN_GROWTH_FACTOR", "0.9"))

# --- Text Splitter Configuration ---
CHILD_CHUNK_SIZE = int(os.environ.get("CHILD_CHUNK_SIZE", "500"))
CHILD_CHUNK_OVERLAP = int(os.environ.get("CHILD_CHUNK_OVERLAP", "100"))
MIN_PARENT_SIZE = int(os.environ.get("MIN_PARENT_SIZE", "2000"))
MAX_PARENT_SIZE = int(os.environ.get("MAX_PARENT_SIZE", "4000"))
HEADERS_TO_SPLIT_ON = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3"),
]

# --- Observability ---
LANGFUSE_ENABLED = os.environ.get("LANGFUSE_ENABLED", "false").lower() == "true"
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGFUSE_BASE_URL = os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000")


def get_llm(provider: str = None, model: str = None, temperature: float = None, seed: int = None):
    """
    Factory function to initialize the LLM based on provider configuration.
    
    Args:
        provider: "ollama", "openai", "anthropic", or "google" (defaults to LLM_PROVIDER)
        model: Specific model name to override the default
        temperature: Temperature setting (defaults to LLM_TEMPERATURE)
        seed: Random seed for reproducibility (defaults to LLM_SEED)
        
    Returns:
        A LangChain-compatible BaseChatModel instance.
    """
    prov = (provider or LLM_PROVIDER).lower()
    temp = LLM_TEMPERATURE if temperature is None else temperature
    sd = LLM_SEED if seed is None else seed
    mdl = model or LLM_MODEL

    if prov == "ollama":
        try:
            from langchain_ollama import ChatOllama
            return ChatOllama(
                model=mdl,
                temperature=temp,
                seed=sd,
                base_url=OLLAMA_BASE_URL,
                think=False,
            )
        except ImportError:
            raise ImportError(
                "langchain-ollama is required for Ollama. Run: pip install langchain-ollama"
            )

    elif prov == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment or .env file.")
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=mdl or "gpt-4o-mini",
                temperature=temp,
                api_key=api_key
            )
        except ImportError:
            raise ImportError(
                "langchain-openai is required for OpenAI. Run: pip install langchain-openai"
            )

    elif prov == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment or .env file.")
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=mdl or "claude-3-5-haiku-20241022",
                temperature=temp,
                api_key=api_key
            )
        except ImportError:
            raise ImportError(
                "langchain-anthropic is required for Anthropic. Run: pip install langchain-anthropic"
            )

    elif prov in ("google", "gemini"):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment or .env file.")
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=mdl or "gemini-1.5-flash",
                temperature=temp,
                google_api_key=api_key
            )
        except ImportError:
            raise ImportError(
                "langchain-google-genai is required for Google Gemini. Run: pip install langchain-google-genai"
            )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{prov}'. Supported: 'ollama', 'openai', 'anthropic', 'google'."
        )


def get_dense_embeddings(model_name: str = None):
    """
    Returns dense embeddings model.
    1. If nomic or an Ollama embedding model is configured, uses local OllamaEmbeddings.
    2. Otherwise attempts HuggingFaceEmbeddings.
    3. Falls back gracefully to local Ollama nomic-embed-text or FastEmbed.
    """
    model = model_name or DENSE_MODEL
    if "nomic" in model.lower() or model.startswith("ollama/") or (":" in model and "/" not in model):
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=model, base_url=OLLAMA_BASE_URL)

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=model)
    except Exception as e:
        try:
            from langchain_ollama import OllamaEmbeddings
            print("ℹ️ Using local Ollama nomic-embed-text:latest for dense embeddings...")
            return OllamaEmbeddings(model="nomic-embed-text:latest", base_url=OLLAMA_BASE_URL)
        except Exception:
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
            return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")


