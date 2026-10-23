"""
==============================================================================
03_observability.py — Observability & Tracing for Agentic RAG Systems
==============================================================================
Converted from notebooks/observability.ipynb.

Observability is critical in Agentic RAG systems because multi-agent loops,
query decomposition, tool routing, and context compression are non-deterministic.
Without tracing, debugging why an agent retrieved the wrong chunk or hallucinated
is nearly impossible.

This module covers:
  1. Telemetry Anatomy:
     • Sessions: Complete user conversational session (thread ID)
     • Traces: A single user query traversal through the LangGraph pipeline
     • Spans: Discrete sub-steps (e.g. rewrite_query, tool execution, compression)
     • Generations: Individual LLM calls capturing system prompt, inputs, outputs, tokens
  2. Langfuse Integration:
     • Tracing LangChain & LangGraph via Langfuse CallbackHandler
     • Auth and health verification
  3. Local Console Tracer:
     • Built-in console observer showing colorized live traces even without an external account!

Usage:
  python learning/03_observability.py --help
  python learning/03_observability.py --check          # Validate Langfuse credentials
  python learning/03_observability.py --demo-trace      # Run live trace with console feedback
==============================================================================
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure workspace root is in sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning import config


# ==============================================================================
# SECTION 1: Local Console Tracer (Fallback & Learning Mode)
# ==============================================================================

class LocalConsoleTracer:
    """
    A lightweight terminal telemetry observer that mimics Langfuse spans and generations
    directly in stdout with clear ASCII tree visualizations.
    """

    def __init__(self):
        self.step_counter = 0

    def start_trace(self, trace_name: str, input_query: str):
        self.step_counter = 1
        print("\n" + "═" * 70)
        print(f"📡 [TRACE START] {trace_name}")
        print(f"   Input: \"{input_query}\"")
        print("═" * 70)

    def log_span(self, name: str, details: str, duration_ms: float = None):
        dur_str = f" ({duration_ms:.1f}ms)" if duration_ms else ""
        print(f"  ├─ ⚙️ [SPAN {self.step_counter}] {name}{dur_str}")
        for line in details.strip().splitlines():
            print(f"  │    {line}")
        self.step_counter += 1

    def log_generation(self, model: str, prompt_summary: str, output_summary: str, tokens: int = None):
        tok_str = f" ~{tokens} tokens" if tokens else ""
        print(f"  ├─ 🧠 [GENERATION {self.step_counter}] Model: {model}{tok_str}")
        print(f"  │    Prompt: {prompt_summary}")
        print(f"  │    Output: {output_summary}")
        self.step_counter += 1

    def log_tool(self, tool_name: str, tool_args: dict, result_summary: str):
        print(f"  ├─ 🛠️ [TOOL CALL {self.step_counter}] {tool_name}")
        print(f"  │    Args: {tool_args}")
        print(f"  │    Result: {result_summary}")
        self.step_counter += 1

    def end_trace(self, final_output: str):
        print("  └─ 🏁 [TRACE COMPLETED]")
        print(f"     Final Output Summary: {final_output[:120]}...")
        print("═" * 70 + "\n")


# ==============================================================================
# SECTION 2: Langfuse Observability Client
# ==============================================================================

class LangfuseObservability:
    """Manages Langfuse tracing handler and authentication checks."""

    def __init__(self):
        self.enabled = config.LANGFUSE_ENABLED
        self.public_key = config.LANGFUSE_PUBLIC_KEY
        self.secret_key = config.LANGFUSE_SECRET_KEY
        self.base_url = config.LANGFUSE_BASE_URL
        self.handler = None
        self.client = None

        if self.enabled:
            self._init_langfuse()

    def _init_langfuse(self):
        try:
            from langfuse import get_client
            from langfuse.langchain import CallbackHandler

            self.client = get_client()
            if self.client.auth_check():
                self.handler = CallbackHandler()
                print("✓ Langfuse authenticated successfully. Telemetry active.")
            else:
                print("⚠️ Langfuse auth_check failed. Verify LANGFUSE_PUBLIC_KEY and SECRET_KEY.")
                self.enabled = False
        except ImportError:
            print("ℹ️ langfuse package not installed. Run: pip install langfuse")
            self.enabled = False
        except Exception as e:
            print(f"⚠️ Langfuse initialization error: {e}")
            self.enabled = False

    def get_callbacks(self) -> list:
        if self.enabled and self.handler:
            return [self.handler]
        return []

    def flush(self):
        if self.client and hasattr(self.client, "flush"):
            try:
                self.client.flush()
            except Exception:
                pass


def check_langfuse_status():
    """Diagnoses the Langfuse connection settings from .env."""
    print("=" * 70)
    print(" 🔍 LANGFUSE OBSERVABILITY STATUS")
    print("=" * 70)
    print(f"  • LANGFUSE_ENABLED    : {config.LANGFUSE_ENABLED}")
    print(f"  • LANGFUSE_BASE_URL   : {config.LANGFUSE_BASE_URL}")
    pk = config.LANGFUSE_PUBLIC_KEY
    sk = config.LANGFUSE_SECRET_KEY
    print(f"  • LANGFUSE_PUBLIC_KEY : {'***' + pk[-4:] if len(pk) > 4 else '(empty)'}")
    print(f"  • LANGFUSE_SECRET_KEY : {'***' + sk[-4:] if len(sk) > 4 else '(empty)'}")

    if not config.LANGFUSE_ENABLED:
        print("\nℹ️ Langfuse is currently disabled. To enable:")
        print("  1. Set LANGFUSE_ENABLED=true in .env")
        print("  2. Provide your keys from https://cloud.langfuse.com or your local instance")
        return

    try:
        from langfuse import get_client
        client = get_client()
        if client.auth_check():
            print("\n✅ Langfuse credentials are VALID and successfully verified!")
        else:
            print("\n❌ Langfuse authentication FAILED. Please double-check your API keys.")
    except Exception as e:
        print(f"\n❌ Error connecting to Langfuse: {e}")


def run_demo_trace():
    """Runs a simulated step-by-step trace showing telemetry anatomy."""
    tracer = LocalConsoleTracer()
    query = "What is blockchain and how does it prevent double spending?"

    tracer.start_trace(trace_name="Agentic_RAG_Query_Workflow", input_query=query)

    tracer.log_span("summarize_history", "Rolling summary evaluated (4 previous messages retained).")

    tracer.log_generation(
        model=config.LLM_MODEL,
        prompt_summary="Rewrite & decompose query into sub-queries",
        output_summary="Sub-query 1: 'What is blockchain definition?' | Sub-query 2: 'Bitcoin double spending prevention'",
        tokens=185
    )

    tracer.log_span("route_after_rewrite", "Fan-out: Spawned 2 parallel retrieval agent subgraphs.")

    tracer.log_tool(
        tool_name="search_child_chunks",
        tool_args={"query": "blockchain definition tamper-proof ledger", "limit": 7},
        result_summary="Found 3 matches. Top score: 0.812, Parent ID: blockchain_p000"
    )

    tracer.log_tool(
        tool_name="retrieve_parent_chunks",
        tool_args={"parent_ids": ["blockchain_p000"]},
        result_summary="Retrieved 1,450 characters of parent section context."
    )

    tracer.log_span("should_compress_context", "Context token count: 850 tokens (below 2000 threshold). No compression needed.")

    tracer.log_generation(
        model=config.LLM_MODEL,
        prompt_summary="Synthesize sub-query findings and aggregate answers",
        output_summary="Blockchain is a tamper-proof shared digital ledger that permanently stores asset exchanges...",
        tokens=340
    )

    tracer.end_trace(
        "Blockchain is a shared tamper-proof ledger that solves double spending using decentralized cryptographic consensus..."
    )

    print("💡 In production with Langfuse enabled, all of the above spans, tool calls,")
    print("   latencies, token counts, and cost metrics are transmitted automatically to your dashboard.")


def main():
    parser = argparse.ArgumentParser(description="Observability & Tracing for Agentic RAG")
    parser.add_argument("--check", action="store_true", help="Check Langfuse connection and credentials")
    parser.add_argument("--demo-trace", action="store_true", help="Run simulated telemetry trace demonstration")

    args = parser.parse_args()

    if args.check:
        check_langfuse_status()
    elif args.demo_trace:
        run_demo_trace()
    else:
        # Default: check status and run demo trace
        check_langfuse_status()
        print()
        run_demo_trace()


if __name__ == "__main__":
    main()
