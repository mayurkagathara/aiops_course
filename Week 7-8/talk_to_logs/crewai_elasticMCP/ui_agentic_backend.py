# log_analysis_crew.py
from crewai import Agent, Task, Crew, LLM
from textwrap import dedent
from typing import List, Dict, Tuple, Optional
import hashlib
import html

from langchain_openai import ChatOpenAI
from config import OPENROUTER_MODEL, OPENROUTER_API_KEY, USE_LOCAL_LLM

USE_LOCAL_LLM = False

if USE_LOCAL_LLM:
    llm = LLM(model="ollama/qwen2.5:1.5b", base_url="http://localhost:11434")
else:
    llm = ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
    )

class LogAnalysisCrew:
    """
    Crew wrapper that:
      - Maintains one Agent and one persistent Task (no tools).
      - Stores a context summary (filters + top-N results) and conversation history.
      - On each user query, updates the single task.description (not the tasks list),
        so the agent always receives the context + conversation history + new question.
      - Resets when reset_memory() is called or when filters/results change.
    """

    def __init__(self, max_preview_logs: int = 40, max_context_chars: int = 4000):
        self.crew: Optional[Crew] = None
        self.agent: Optional[Agent] = None
        self.persistent_task: Optional[Task] = None

        # textual context built from filters + results (persisted until filters/results change)
        self.context_text: str = ""
        self.context_signature: Optional[str] = None

        # conversation history: list of tuples ("user"|"assistant", message_str)
        self.history: List[Tuple[str, str]] = []

        # tuning: how many logs to show in the context, and max prompt size
        self.max_preview_logs = max_preview_logs
        self.max_context_chars = max_context_chars

    # ----------------------
    # Public API
    # ----------------------

    def reset_memory(self):
        """Completely clear crew, context and history (Start New Chat)."""
        self.crew = None
        self.agent = None
        self.persistent_task = None
        self.context_text = ""
        self.context_signature = None
        self.history = []

    def analyze(self, filters: Dict, results: List[Dict], user_query: str) -> str:
        """
        Main entrypoint:
          - ensures context is built (or rebuilt if filters/results changed),
          - updates a single persistent task description to include context + history + new question,
          - calls crew.kickoff() and returns the assistant's reply (string).
        """
        try:
            # Ensure we have context/crew for current filters+results
            self._ensure_context_and_crew(filters, results)

            # append the user query to history (so the conversation gets passed onwards)
            # we append before calling the agent so the agent sees the new user message
            self.history.append(("user", user_query))

            # Build the new task description in-place (do not replace crew.tasks list)
            new_description = self._compose_description(user_query)

            # Update persistent task description (modify the same Task object)
            if self.persistent_task is None:
                # fallback safety - shouldn't happen because _ensure_context_and_crew creates it
                raise RuntimeError("Persistent task missing; crew not initialized.")
            self.persistent_task.description = new_description

            # Call crew.kickoff() - should run the task and return a textual answer
            output = self.crew.kickoff()

            # store assistant response in history (so follow-ups remember it)
            assistant_reply = output if isinstance(output, str) else str(output)
            self.history.append(("assistant", assistant_reply))

            return assistant_reply

        except Exception as e:
            # keep trace for debugging but return a readable message
            import traceback
            tb = traceback.format_exc()
            return f"**Error in LogAnalysisCrew.analyze():** {html.escape(str(e))}\n\n```\n{html.escape(tb)}\n```"

    # ----------------------
    # Internal helpers
    # ----------------------

    def _ensure_context_and_crew(self, filters: Dict, results: List[Dict]):
        """
        Build or rebuild context & crew when necessary.
        If the filters+results signature matches the stored one, do nothing.
        Otherwise, rebuild context (and reset conversation history).
        """
        sig = self._make_signature(filters, results)
        if sig == self.context_signature and self.crew is not None:
            # same context as before — keep history and crew
            return

        # new context detected -> refresh
        self.context_signature = sig
        self.context_text = self._build_context_text(filters, results)
        # reset conversation history when context changes (new search results)
        self.history = []

        # (re)build crew and single persistent task
        self._build_crew_with_persistent_task()

    def _make_signature(self, filters: Dict, results: List[Dict]) -> str:
        """
        Create a small signature/hash for the filters+results to detect changes.
        We avoid hashing the entire results content if it's large: we use the IDs/timestamps/messages of top-N.
        """
        try:
            items = [
                (k, filters.get(k)) for k in sorted(filters.keys())
            ]
            # include a compact preview of top results (timestamp/id/message snippet)
            preview = []
            for r in (results or [])[: self.max_preview_logs]:
                # prefer an id-like field if present
                rid = r.get("_id") or r.get("id") or r.get("timestamp") or r.get("message", "")[:60]
                preview.append(str(rid))
            blob = repr(items) + "|" + "|".join(preview)
            return hashlib.sha256(blob.encode("utf-8")).hexdigest()
        except Exception:
            # fallback: very coarse signature
            return hashlib.sha256(repr(filters).encode("utf-8")).hexdigest()

    def _truncate_text(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        # naive truncation with ellipsis
        return text[: max_chars - 200] + "\n\n... (truncated context) ...\n"

    def _build_context_text(self, filters: Dict, results: List[Dict]) -> str:
        """
        Compose a human-friendly summary of the filters and a preview of the results.
        Keep it short: limit to max_preview_logs and to max_context_chars.
        """
        filters_part = ", ".join(f"{k}={v}" for k, v in (filters or {}).items() if v)
        if not filters_part:
            filters_part = "No filters (all data)."

        total_hits = len(results or [])
        top_n = min(self.max_preview_logs, total_hits)

        lines = [f"Filters applied: {filters_part}", f"Total results returned: {total_hits}", ""]
        if total_hits == 0:
            lines.append("No log lines in results.")
        else:
            lines.append(f"Showing a preview of up to {top_n} log lines (most recent first):")
            lines.append("Log format: timestamp | level | environment | application | customer | message")
            for r in (results or [])[:top_n]:
                # be defensive about missing fields in the log dict:
                ts = r.get("timestamp") or r.get("@timestamp") or ""
                app = r.get("application_name") or r.get("app") or ""
                cust = r.get("customer") or ""
                cust_name = r.get("customer_name") or ""
                env = r.get("environment_name") or ""
                level = r.get("log_level") or ""
                message = (r.get("message") or r.get("msg") or "")
                # keep message short
                message_preview = message.replace("\n", " ")[:250]
                lines.append(f"- [{ts}] [{level}] [{env}] {app} {f'({cust + ' ' + cust_name})' if cust else ''}: {message_preview}")

        context = "\n".join(lines)
        # final guard against huge prompts
        context = self._truncate_text(context, self.max_context_chars)
        print("=== Context ===\n", context)
        # instruct agent that this is background/context for follow-ups
        header = (
            "Context (filters + result preview) — keep this context available for all follow-up questions "
            "until the conversation is reset.\n\n"
        )
        return header + context

    def _build_crew_with_persistent_task(self):
        """
        Create the Crew, one Agent and one persistent Task.
        We do a single kickoff once to prime the crew (optional).
        """
        # Create an Agent (no tools). We manage "memory" ourselves via description/history.
        self.agent = Agent(
            role="Log Analyst",
            goal="Analyze filtered log data and answer user questions concisely (≤ 2 paragraphs).",
            backstory=(
                "You are an expert in reading and summarizing logs. Use the provided context + conversation "
                "history to answer the user's next question concisely and in Markdown. No external tools."
            ),
            llm = llm,
            allow_delegation=False,
            # Do not rely on internal memory: we pass context explicitly each time
            memory=False,
        )

        # Build a base task description that contains the context.
        # The description will be updated in-place for each user query.
        base_desc = dedent(
            f"""
            {self.context_text}

            Conversation history: (empty for now). Wait for the user's first question.
            
            Instructions for the Assistant:
            - Answer in Markdown.
            - Keep the answer to **no more than 2 short paragraphs**.
            - Be specific and reference the logs/context if relevant.
            """
        )

        # persistent Task (only one). We'll update persistent_task.description for each query.
        self.persistent_task = Task(
            description=base_desc,
            agent=self.agent,
            expected_output="Short Markdown answer (<= 2 paragraphs).",
        )

        # Build Crew with a single agent and single task
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.persistent_task],
            verbose=False,
        )

        # optional: kickoff once to prime (this may cause an initial ack). It's OK.
        try:
            self.crew.kickoff()
        except Exception:
            # ignore kickoff errors here — we'll rebuild description before real queries
            pass

    def _compose_description(self, user_query: str) -> str:
        """
        Compose the full description for the persistent task by combining:
          - context_text (filters + preview results),
          - conversation history (user & assistant turns),
          - the new user query,
          - final instructions (markdown, <= 2 paragraphs).
        """
        # Build conversation history block
        history_lines = []
        for role, msg in self.history:
            prefix = "User" if role == "user" else "Assistant"
            # escape newlines to keep layout compact
            history_lines.append(f"{prefix}: {msg}")

        history_block = "\n".join(history_lines) if history_lines else "No prior messages."

        desc = dedent(
            f"""
            {self.context_text}

            Conversation history:
            {history_block}

            NEW USER QUESTION:
            {user_query}

            Assistant instructions:
            - Use the context and conversation history above to answer the NEW USER QUESTION.
            - Answer in Markdown and be concise: **no more than two short paragraphs**.
            - If you rely on particular log lines, reference them briefly.
            """
        )

        # ensure we do not exceed max prompt size
        desc = self._truncate_text(desc, self.max_context_chars)
        return desc
