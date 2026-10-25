import json
import re
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk, ToolMessage
from core.execution_logger import log_chat_end, log_chat_start, log_error

SYSTEM_NODES = {"summarize_history", "rewrite_query"}
FINAL_RESPONSE_NODES = {"aggregate_answers"}

SYSTEM_NODE_CONFIG = {
    "rewrite_query":     {"title": "🔍 Query Analysis & Rewriting"},
    "summarize_history": {"title": "📋 Chat History Summary"},
}

# --- Helpers ---

def make_message(content, *, title=None, node=None):
    msg = {"role": "assistant", "content": content}
    if title or node:
        msg["metadata"] = {k: v for k, v in {"title": title, "node": node}.items() if v}
    return msg


def find_msg_idx(messages, node):
    return next(
        (i for i, m in enumerate(messages) if m.get("metadata", {}).get("node") == node),
        None,
    )


def parse_rewrite_json(buffer):
    match = re.search(r"\{.*\}", buffer, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except Exception:
        return None


def format_rewrite_content(buffer):
    data = parse_rewrite_json(buffer)
    if not data:
        return "⏳ Analyzing query..."
    if data.get("is_clear"):
        lines = ["✅ **Query is clear**"]
        if data.get("questions"):
            lines += ["\n**Rewritten queries:**"] + [f"- {q}" for q in data["questions"]]
    else:
        lines = ["❓ **Query is unclear**"]
        clarification = data.get("clarification_needed", "")
        if clarification and clarification.strip().lower() != "no":
            lines.append(f"\nClarification needed: *{clarification}*")
    return "\n".join(lines)

# --- End of Helpers ---

from datetime import datetime

class ChatInterface:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.last_query = ""
        self.events_log = []
        self.search_results = []
        self.rewritten_questions = []
        self.working_memory_summary = ""
        self.session_metrics = {
            "tool_calls": 0,
            "queries_processed": 0,
            "clarification_needed": False,
            "status": "Ready",
            "active_node": "Idle",
        }

    def _log_event(self, node: str, event_type: str, detail: str = ""):
        now_str = datetime.now().strftime("%H:%M:%S")
        self.events_log.append({
            "time": now_str,
            "node": node,
            "type": event_type,
            "detail": detail,
        })
        # Keep last 50 events
        if len(self.events_log) > 50:
            self.events_log.pop(0)

    def _extract_search_results(self, content_str: str, tool_name: str = "search"):
        """Extract child and parent chunk details from tool outputs."""
        if not content_str or "NO_RELEVANT_CHUNKS" in content_str or "RETRIEVAL_ERROR" in content_str:
            return
        
        # Check if content has chunks separated by CHILD_CHUNK_SEPARATOR
        import config
        chunks = content_str.split(config.CHILD_CHUNK_SEPARATOR) if hasattr(config, "CHILD_CHUNK_SEPARATOR") else [content_str]
        for c in chunks:
            text = c.strip()
            if not text:
                continue
            parent_id = ""
            file_name = ""
            snippet = text
            for line in text.splitlines():
                if line.startswith("Parent ID:"):
                    parent_id = line.replace("Parent ID:", "").strip()
                elif line.startswith("File Name:"):
                    file_name = line.replace("File Name:", "").strip()
                elif line.startswith("Content:"):
                    snippet = text.split("Content:", 1)[-1].strip()
            self.search_results.append({
                "parent_id": parent_id or "N/A",
                "file_name": file_name or "Unknown Source",
                "tool": tool_name,
                "content": snippet[:400] + ("..." if len(snippet) > 400 else "")
            })

    def _handle_system_node(self, chunk, node, response_messages, system_node_buffer):
        """Update (or create) the collapsible system-node message and surface any clarification."""
        system_node_buffer[node] = system_node_buffer.get(node, "") + chunk.content
        buffer = system_node_buffer[node]
        title  = SYSTEM_NODE_CONFIG[node]["title"]
        content = format_rewrite_content(buffer) if node == "rewrite_query" else buffer

        if node == "summarize_history":
            self.working_memory_summary = buffer
            self._log_event(node, "Memory Updated", f"History summarized ({len(buffer)} chars)")

        if node == "rewrite_query":
            parsed = parse_rewrite_json(buffer)
            if parsed and parsed.get("questions"):
                self.rewritten_questions = parsed.get("questions", [])
                self._log_event(node, "Query Rewritten", f"{len(self.rewritten_questions)} sub-queries generated")

        idx = find_msg_idx(response_messages, node)
        if idx is None:
            response_messages.append(make_message(content, title=title, node=node))
        else:
            response_messages[idx]["content"] = content

        if node == "rewrite_query":
            self._surface_clarification(buffer, response_messages)

    def _surface_clarification(self, buffer, response_messages):
        """If the query is unclear, add/update a plain clarification message."""
        data          = parse_rewrite_json(buffer) or {}
        clarification = data.get("clarification_needed", "")
        if not data.get("is_clear") and clarification.strip().lower() not in ("", "no"):
            self.session_metrics["clarification_needed"] = True
            self._log_event("main.rewrite_query", "Clarification Requested", clarification[:60])
            cidx = find_msg_idx(response_messages, "clarification")
            if cidx is None:
                response_messages.append(make_message(clarification, node="clarification"))
            else:
                response_messages[cidx]["content"] = clarification

    def _handle_tool_call(self, chunk, response_messages, active_tool_calls):
        """Register new tool calls as collapsible messages."""
        for tc in chunk.tool_calls:
            if tc.get("id") and tc["id"] not in active_tool_calls:
                tname = tc.get("name", "tool")
                self.session_metrics["tool_calls"] += 1
                self._log_event("agent.tools", f"Calling `{tname}`", f"Args: {str(tc.get('args', {}))[:80]}")
                response_messages.append(
                    make_message(f"Running `{tname}`...", title=f"🛠️ {tname}")
                )
                active_tool_calls[tc["id"]] = len(response_messages) - 1

    def _handle_tool_result(self, chunk, response_messages, active_tool_calls):
        """Fill in the tool result inside the matching collapsible message."""
        idx = active_tool_calls.get(chunk.tool_call_id)
        if idx is not None:
            content_str = str(chunk.content)
            self._extract_search_results(content_str, tool_name=getattr(chunk, "name", "tool") or "tool")
            self._log_event("agent.tools", "Tool Output Received", f"{len(content_str)} chars returned")
            preview = content_str[:300]
            suffix  = "\n..." if len(content_str) > 300 else ""
            response_messages[idx]["content"] = f"```\n{preview}{suffix}\n```"

    def _handle_llm_token(self, chunk, node, response_messages):
        """Append streaming LLM tokens to the last plain assistant message."""
        last = response_messages[-1] if response_messages else None
        if not (last and last.get("role") == "assistant" and "metadata" not in last):
            response_messages.append(make_message(""))
        response_messages[-1]["content"] += chunk.content

    def get_search_results_markdown(self) -> str:
        """Render the latest search results and query rewrites in clean rich cards."""
        if not self.last_query:
            return """
            <div style="padding: 20px; text-align: center; color: var(--ink-muted); font-size: 0.82rem;">
                <div style="font-size: 1.3rem; margin-bottom: 4px;">🔍</div>
                <strong style="color: var(--ink-secondary);">No search queries yet</strong><br>
                Ask a question in the chat to see real-time hybrid retrieval (Qdrant + BM25) and extracted excerpts here.
            </div>
            """

        html_blocks = [
            f"""
            <div style="margin-bottom: 8px; padding: 6px 10px; background: var(--surface-subtle); border: 1px solid var(--border-subtle); border-radius: 6px;">
                <div style="font-size: 0.66rem; font-weight: 600; color: var(--ink-muted);">Active search query</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: var(--ink-primary); margin-top: 1px;">{self.last_query}</div>
            </div>
            """
        ]

        if self.rewritten_questions:
            questions_html = "".join([f'<li style="margin-bottom: 2px; color: var(--ink-secondary);"><code style="background: var(--surface-subtle); padding: 2px 6px; border-radius: 4px; font-size: 0.72rem; font-family: var(--font-mono);">{q}</code></li>' for q in self.rewritten_questions])
            html_blocks.append(f"""
            <div style="margin-bottom: 8px;">
                <div style="font-size: 0.68rem; font-weight: 600; color: var(--brand-primary); margin-bottom: 3px;">Rewritten sub-queries</div>
                <ul style="margin: 0; padding-left: 16px; font-size: 0.74rem;">{questions_html}</ul>
            </div>
            """)

        if not self.search_results:
            html_blocks.append("""
            <div style="padding: 8px; background: var(--surface-subtle); border: 1px dashed var(--border-subtle); border-radius: 6px; color: var(--ink-muted); font-size: 0.74rem;">
                ℹ️ No child chunks retrieved for this turn. The agent answered directly from context or conversation history.
            </div>
            """)
        else:
            cards = []
            for i, r in enumerate(self.search_results, 1):
                parent_badge = f'<span class="badge-tag badge-chunks">Parent: {r["parent_id"]}</span>' if r['parent_id'] != 'N/A' else ''
                cards.append(f"""
                <div class="search-chunk-card">
                    <div class="search-chunk-header">
                        <span style="font-weight: 600; color: var(--ink-primary); display: flex; align-items: center; gap: 6px;">
                            <span style="color: var(--brand-primary); font-family: var(--font-mono);">#{i}</span> 📄 {r['file_name']}
                        </span>
                        {parent_badge}
                    </div>
                    <div class="search-chunk-content">{r['content']}</div>
                </div>
                """)
            html_blocks.append("".join(cards))

        return "\n".join(html_blocks)

    def get_observability_markdown(self) -> str:
        """Render live agent call traces, active steps, and system diagnostics with rich styling."""
        active = self.session_metrics.get("active_node", "Idle")
        status = self.session_metrics.get("status", "Ready")
        tool_count = self.session_metrics.get("tool_calls", 0)

        pipeline_nodes = [
            ("1", "main.summarize_history", "Context compaction & rolling summary"),
            ("2", "main.rewrite_query", "Intent analysis & multi-query expansion"),
            ("3", "agent.orchestrator", "Agent reasoning & tool decision node"),
            ("4", "agent.tools", "Hybrid Qdrant & BM25 retrieval"),
            ("5", "agent.compress_context", "Token budget compression & optimization"),
            ("6", "main.aggregate_answers", "Final answer aggregation & synthesis"),
        ]

        stepper_items = []
        for num, node_name, desc in pipeline_nodes:
            is_active = (node_name == active) or (node_name in active)
            active_class = "active" if is_active else ""
            dot_color = "var(--status-live)" if is_active else ("var(--brand-primary)" if status == "Completed" else "var(--border-focus)")
            stepper_items.append(f"""
            <div class="stepper-item {active_class}">
                <div class="stepper-num">{num}</div>
                <div style="flex: 1;">
                    <div class="stepper-title" style="display: flex; align-items: center; justify-content: space-between;">
                        <span>{node_name}</span>
                        <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {dot_color};"></span>
                    </div>
                    <div class="stepper-desc">{desc}</div>
                </div>
            </div>
            """)

        event_rows = []
        if not self.events_log:
            event_rows.append("""
            <tr>
                <td colspan="4" style="text-align: center; color: var(--ink-muted); padding: 10px;">
                    No execution events recorded yet. Send a query to observe live agent calls.
                </td>
            </tr>
            """)
        else:
            for ev in reversed(self.events_log[-10:]):
                event_rows.append(f"""
                <tr>
                    <td style="font-family: var(--font-mono); color: var(--brand-primary); font-weight: 600;">{ev['time']}</td>
                    <td style="font-family: var(--font-mono); font-weight: 600; color: var(--ink-primary);">{ev['node']}</td>
                    <td><strong style="color: var(--ink-secondary);">{ev['type']}</strong></td>
                    <td style="color: var(--ink-muted);">{ev['detail']}</td>
                </tr>
                """)

        return f"""
        <div class="obs-stat-row">
            <div class="obs-stat-card">
                <div class="obs-stat-label">Status</div>
                <div class="obs-stat-val" style="color: {'var(--status-live)' if status in ('Ready', 'Completed') else 'var(--brand-primary)'};">{status}</div>
            </div>
            <div class="obs-stat-card">
                <div class="obs-stat-label">Active Node</div>
                <div class="obs-stat-val" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: var(--font-mono); font-size: 0.74rem;">{active}</div>
            </div>
            <div class="obs-stat-card">
                <div class="obs-stat-label">Tools Invoked</div>
                <div class="obs-stat-val" style="font-family: var(--font-mono);">{tool_count}</div>
            </div>
        </div>

        <div style="font-size: 0.70rem; font-weight: 700; color: var(--ink-primary); margin: 8px 0 4px 0; letter-spacing: -0.01em;">
            State Machine Pipeline
        </div>
        <div class="stepper-list">
            {''.join(stepper_items)}
        </div>

        <div style="font-size: 0.70rem; font-weight: 700; color: var(--ink-primary); margin: 10px 0 4px 0; letter-spacing: -0.01em;">
            Execution Event Log (Latest First)
        </div>
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Node</th>
                    <th>Event</th>
                    <th>Detail</th>
                </tr>
            </thead>
            <tbody>
                {''.join(event_rows)}
            </tbody>
        </table>
        """

    def get_memory_markdown(self) -> str:
        """Render thread ID, working memory summary, and conversation state in rich cards."""
        tid = self.rag_system.thread_id
        summary = self.working_memory_summary.strip() or "No conversation summary generated yet. The agent automatically compresses previous turns into working memory as dialogue length increases."
        clarification = "⚠️ Clarification needed from user" if self.session_metrics.get("clarification_needed") else "✅ Query is unambiguous & clear"
        
        import config
        return f"""
        <div style="display: flex; flex-direction: column; gap: 7px;">
            <div style="background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: 7px; padding: 9px 10px;">
                <div style="font-size: 0.65rem; font-weight: 600; color: var(--ink-muted);">Session Thread ID</div>
                <div style="font-family: var(--font-mono); font-size: 0.72rem; color: #4F46E5; font-weight: 600; word-break: break-all; margin-top: 2px;">
                    {tid}
                </div>
            </div>

            <div style="background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: 7px; padding: 9px 10px;">
                <div style="font-size: 0.65rem; font-weight: 600; color: var(--ink-muted);">Dialogue State</div>
                <div style="font-size: 0.76rem; font-weight: 600; color: {'var(--status-amber)' if self.session_metrics.get('clarification_needed') else 'var(--status-live)'}; margin-top: 2px;">
                    {clarification}
                </div>
            </div>

            <div style="background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: 7px; padding: 9px 10px;">
                <div style="font-size: 0.65rem; font-weight: 600; color: var(--ink-muted);">Active LLM Runtime</div>
                <div style="font-size: 0.74rem; color: var(--ink-secondary); margin-top: 2px; font-family: var(--font-mono);">
                    Provider: <strong style="color: #4F46E5;">{getattr(config, 'LLM_PROVIDER', 'ollama')}</strong> | 
                    Model: <strong style="color: #4F46E5;">{getattr(config, 'LLM_MODEL', 'qwen3.5:9b')}</strong>
                </div>
            </div>

            <div style="background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: 7px; padding: 9px 10px;">
                <div style="font-size: 0.65rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 5px;">Working Memory Summary</div>
                <div style="font-size: 0.74rem; color: var(--ink-secondary); line-height: 1.5; background: var(--surface-subtle); border: 1px solid var(--border-subtle); border-left: 3px solid var(--brand-primary); padding: 7px 10px; border-radius: 5px;">
                    {summary}
                </div>
            </div>
        </div>
        """


    def chat_stream_full(self, message, history):
        """Generator yielding (messages, search_results_md, observability_md, memory_md)."""
        if not self.rag_system.agent_graph:
            yield (
                [{"role": "assistant", "content": "⚠️ System not initialized!"}],
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )
            return

        self.last_query = message.strip()
        self.search_results = []
        self.rewritten_questions = []
        self.session_metrics["status"] = "Executing"
        self.session_metrics["clarification_needed"] = False
        self.session_metrics["queries_processed"] += 1

        self._log_event("chat.start", "Query Received", message.strip()[:60])

        config = self.rag_system.get_config()
        current_state = self.rag_system.agent_graph.get_state(config)
        log_chat_start(message.strip(), self.rag_system.thread_id, bool(current_state.next))

        try:
            if current_state.next:
                self.rag_system.agent_graph.update_state(config, {"messages": [HumanMessage(content=message.strip())]})
                stream_input = None
            else:
                stream_input = {"messages": [HumanMessage(content=message.strip())]}

            response_messages  = []
            active_tool_calls  = {}
            system_node_buffer = {}

            for chunk, metadata in self.rag_system.agent_graph.stream(stream_input, config=config, stream_mode="messages"):
                node = metadata.get("langgraph_node", "")
                if node:
                    self.session_metrics["active_node"] = node

                if node in SYSTEM_NODES and isinstance(chunk, (AIMessageChunk, AIMessage)) and chunk.content:
                    self._handle_system_node(chunk, node, response_messages, system_node_buffer)

                elif hasattr(chunk, "tool_calls") and chunk.tool_calls:
                    self._handle_tool_call(chunk, response_messages, active_tool_calls)

                elif isinstance(chunk, ToolMessage):
                    self._handle_tool_result(chunk, response_messages, active_tool_calls)

                elif isinstance(chunk, (AIMessageChunk, AIMessage)) and chunk.content and node in FINAL_RESPONSE_NODES:
                    self._handle_llm_token(chunk, node, response_messages)

                else:
                    continue

                yield (
                    response_messages,
                    self.get_search_results_markdown(),
                    self.get_observability_markdown(),
                    self.get_memory_markdown(),
                )

            final_state = self.rag_system.agent_graph.get_state(config)
            log_chat_end(getattr(final_state, "values", final_state))
            
            # Post-execution state & message extraction
            if hasattr(final_state, "values") and isinstance(final_state.values, dict):
                conv_sum = final_state.values.get("conversation_summary", "")
                if conv_sum:
                    self.working_memory_summary = conv_sum

                rewritten = final_state.values.get("rewrittenQuestions", [])
                if rewritten:
                    self.rewritten_questions = rewritten

                # Handle clarification interrupt
                if getattr(final_state, "next", None) and "request_clarification" in final_state.next:
                    clarification = final_state.values.get("clarification", "") or "Could you please provide a bit more context for your question?"
                    self.session_metrics["clarification_needed"] = True
                    self.session_metrics["status"] = "Needs Clarification"
                    plain_idx = next((i for i, m in enumerate(response_messages) if m.get("role") == "assistant" and "metadata" not in m), None)
                    if plain_idx is not None:
                        response_messages[plain_idx]["content"] = clarification
                    else:
                        response_messages.append(make_message(clarification))
                else:
                    # Ensure final synthesized answer is surfaced from state
                    msgs = final_state.values.get("messages", [])
                    if msgs:
                        last_ai = next((m for m in reversed(msgs) if isinstance(m, (AIMessage, AIMessageChunk)) and m.content and not getattr(m, "tool_calls", None)), None)
                        if last_ai and last_ai.content:
                            plain_idx = next((i for i, m in enumerate(response_messages) if m.get("role") == "assistant" and "metadata" not in m), None)
                            if plain_idx is not None:
                                response_messages[plain_idx]["content"] = last_ai.content
                            else:
                                response_messages.append(make_message(last_ai.content))

            self.session_metrics["status"] = "Completed" if not self.session_metrics.get("clarification_needed") else "Needs Clarification"
            self.session_metrics["active_node"] = "Idle"
            self._log_event("chat.end", "Execution Finished", "Synthesized response delivered")

            yield (
                response_messages,
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )

        except Exception as e:
            log_error("chat", e)
            self.session_metrics["status"] = "Error"
            self.session_metrics["active_node"] = "Idle"
            self._log_event("chat.error", "Execution Failed", str(e)[:80])
            err_msg = [{"role": "assistant", "content": f"❌ Error: {str(e)}"}]
            yield (
                err_msg,
                self.get_search_results_markdown(),
                self.get_observability_markdown(),
                self.get_memory_markdown(),
            )

    def chat(self, message, history):
        """Original generator streaming only message list for backward compatibility."""
        for messages, _, _, _ in self.chat_stream_full(message, history):
            yield messages

    def clear_session(self):
        self.rag_system.reset_thread()
        self.rag_system.observability.flush()
        self.last_query = ""
        self.search_results = []
        self.rewritten_questions = []
        self.working_memory_summary = ""
        self.events_log = []
        self.session_metrics = {
            "tool_calls": 0,
            "queries_processed": 0,
            "clarification_needed": False,
            "status": "Ready",
            "active_node": "Idle",
        }

