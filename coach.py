"""
LLM-powered chess coach.

Architecture
------------
* Tool use — profile updates are structured function calls, not fragile text
  parsing.  Both Claude (tool_use) and OpenAI (function_calling) support this
  natively.  Ollama falls back to JSON text extraction.

* Persistent conversation — the message history is serialised to
  ~/.chessMentor/conversation.json and reloaded on the next session so the
  coach retains full memory of everything discussed.  The history is trimmed
  to CONVERSATION_MAX_MESSAGES to bound token cost.

* Prompt caching — the large system prompt (profile + 100+ principles block)
  is marked with cache_control so Anthropic's API serves it from cache on
  repeated calls within a session, cutting input token cost significantly.
"""

from __future__ import annotations

import json
from typing import Optional, List, Dict, Any

import chess

from providers.llm import LLMProvider, get_llm_provider
from knowledge.retrieval import get_relevant_principles, format_principles_for_prompt
from profile import (
    profile_summary_text,
    append_lesson,
    append_coach_note,
    add_weakness,
    add_strength,
    record_opening,
    save_profile,
    load_conversation,
    save_conversation,
)

# ---------------------------------------------------------------------------
# Conversation settings
# ---------------------------------------------------------------------------

CONVERSATION_MAX_MESSAGES = 60   # keep last 60 messages (~30 exchanges)

# ---------------------------------------------------------------------------
# Tool definition: update_player_profile
# ---------------------------------------------------------------------------

# Anthropic / OpenAI compatible tool schema
PROFILE_TOOL = {
    "name": "update_player_profile",
    "description": (
        "Persist coaching insights to the player's profile. "
        "Call this at the end of every coaching response to record any new "
        "lessons, weaknesses, strengths, openings, or notes discovered. "
        "Omit fields that have nothing new to record."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lessons": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Concrete, reusable lessons to remember across sessions.",
            },
            "weaknesses": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Recurring mistakes or patterns to improve.",
            },
            "strengths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Consistent good habits or skills shown.",
            },
            "opening": {
                "type": "object",
                "description": "Opening played in this game (if identifiable).",
                "properties": {
                    "color": {
                        "type": "string",
                        "enum": ["white", "black"],
                    },
                    "name": {
                        "type": "string",
                        "description": "Opening name, e.g. 'Sicilian Najdorf'.",
                    },
                },
                "required": ["color", "name"],
            },
            "coach_note": {
                "type": "string",
                "description": "One-sentence persistent observation about this player.",
            },
        },
        "required": [],
    },
}

# ---------------------------------------------------------------------------
# System prompt template
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are ChessMentor, an expert chess coach with full memory of this player's \
history across all sessions.

Your role each turn:
1. Analyse the current position and the move just played.
2. Give concise, actionable coaching tailored to the player's level and history.
3. Reference their known weaknesses and strengths where relevant.
4. Cite a relevant principle from the Relevant Chess Principles section when \
   it directly applies.
5. ALWAYS call the `update_player_profile` tool at the end of your response \
   to persist any new insights — even if there is nothing new, call it with \
   empty arrays so the system knows the turn completed.

Keep your coaching reply under 120 words.  Be encouraging but honest.

--- Player Profile ---
{profile}

{principles}
"""

# ---------------------------------------------------------------------------
# Helper: apply a tool call result to the profile
# ---------------------------------------------------------------------------

def _apply_tool_input(data: dict, profile: dict) -> None:
    for lesson in data.get("lessons") or []:
        if lesson:
            append_lesson(profile, lesson)
    for w in data.get("weaknesses") or []:
        if w:
            add_weakness(profile, w)
    for s in data.get("strengths") or []:
        if s:
            add_strength(profile, s)
    opening = data.get("opening") or {}
    if opening.get("name") and opening.get("color"):
        record_opening(profile, opening["color"], opening["name"])
    note = data.get("coach_note", "")
    if note:
        append_coach_note(profile, note)


# ---------------------------------------------------------------------------
# Helper: fallback JSON extraction for providers without tool use (Ollama)
# ---------------------------------------------------------------------------

def _extract_json_fallback(text: str) -> Optional[dict]:
    """
    Try to parse a JSON object from anywhere in *text*.
    Used when the LLM provider doesn't support tool use.
    """
    import re
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# CoachSession
# ---------------------------------------------------------------------------

class CoachSession:
    """
    Manages a multi-turn coaching conversation that persists across sessions.

    Message history is loaded from disk on init and saved on every turn.
    Profile updates arrive via structured tool calls (Claude/OpenAI) or JSON
    fallback (Ollama/other).
    """

    def __init__(
        self,
        profile: dict,
        llm_provider: Optional[LLMProvider] = None,
        debug: bool = False,
    ):
        self.profile = profile
        self._llm = llm_provider
        self._debug = debug
        # Load persisted conversation; trim to max length
        self.messages: List[Dict[str, Any]] = load_conversation()
        if len(self.messages) > CONVERSATION_MAX_MESSAGES:
            self.messages = self.messages[-CONVERSATION_MAX_MESSAGES:]

    def _get_llm(self) -> LLMProvider:
        if self._llm is None:
            from config import (
                ANTHROPIC_API_KEY, CLAUDE_MODEL,
                OPENAI_API_KEY, OPENAI_LLM_MODEL,
                OLLAMA_BASE_URL, OLLAMA_MODEL,
                LLM_PROVIDER,
            )
            self._llm = get_llm_provider({
                "llm_provider": LLM_PROVIDER,
                "anthropic_api_key": ANTHROPIC_API_KEY,
                "claude_model": CLAUDE_MODEL,
                "openai_api_key": OPENAI_API_KEY,
                "openai_llm_model": OPENAI_LLM_MODEL,
                "ollama_base_url": OLLAMA_BASE_URL,
                "ollama_model": OLLAMA_MODEL,
            })
        return self._llm

    def _build_system(self, board: chess.Board) -> str:
        principles = get_relevant_principles(board, self.profile, n=3)
        if self._debug:
            print(f"[DEBUG] Injecting principles: {[p['id'] for p in principles]}")
        return _SYSTEM_PROMPT.format(
            profile=profile_summary_text(self.profile),
            principles=format_principles_for_prompt(principles),
        )

    def _persist(self) -> None:
        """Save conversation + profile to disk."""
        save_conversation(self.messages[-CONVERSATION_MAX_MESSAGES:])
        save_profile(self.profile)

    def coach(
        self,
        board: chess.Board,
        engine_result: Dict[str, Any],
        last_move_san: Optional[str],
        delta_cp: Optional[int],
        player_color: str,
    ) -> str:
        system = self._build_system(board)
        context = _build_context(board, engine_result, last_move_san, delta_cp, player_color)
        self.messages.append({"role": "user", "content": context})

        llm = self._get_llm()
        coaching_text, tool_input = llm.chat_with_tools(
            system=system,
            messages=self.messages,
            tools=[PROFILE_TOOL],
        )

        # Record assistant turn (text only — tool result handled internally)
        self.messages.append({"role": "assistant", "content": coaching_text})

        if tool_input:
            _apply_tool_input(tool_input, self.profile)
        else:
            # Fallback: try to find JSON in the text (Ollama, unconfigured models)
            data = _extract_json_fallback(coaching_text)
            if data:
                _apply_tool_input(data, self.profile)

        self._persist()
        return coaching_text

    def end_game_summary(self, result: str) -> str:
        prompt = (
            f"The game just ended: {result}. "
            "Please give a brief post-game summary covering strengths, key mistakes, "
            "and one concrete improvement goal for next time. "
            "Then call update_player_profile to persist the insights."
        )
        self.messages.append({"role": "user", "content": prompt})

        board = chess.Board()  # use starting position for principle selection
        system = self._build_system(board)
        llm = self._get_llm()
        summary_text, tool_input = llm.chat_with_tools(
            system=system,
            messages=self.messages,
            tools=[PROFILE_TOOL],
        )

        self.messages.append({"role": "assistant", "content": summary_text})

        if tool_input:
            _apply_tool_input(tool_input, self.profile)

        self.profile["total_games_analyzed"] = self.profile.get("total_games_analyzed", 0) + 1
        self._persist()
        return summary_text


# ---------------------------------------------------------------------------
# Context builder
# ---------------------------------------------------------------------------

def _build_context(
    board: chess.Board,
    engine_result: Dict[str, Any],
    last_move_san: Optional[str],
    delta_cp: Optional[int],
    player_color: str,
) -> str:
    lines = [
        f"Current FEN: {board.fen()}",
        f"Player color: {player_color}",
        f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}",
    ]
    if last_move_san:
        lines.append(f"Last move played: {last_move_san}")
    if delta_cp is not None:
        if delta_cp > 200:
            lines.append(f"Evaluation shift: -{delta_cp} cp (blunder)")
        elif delta_cp > 80:
            lines.append(f"Evaluation shift: -{delta_cp} cp (mistake)")
        elif delta_cp > 30:
            lines.append(f"Evaluation shift: -{delta_cp} cp (inaccuracy)")
        else:
            lines.append(f"Evaluation shift: {-delta_cp} cp")

    cp = engine_result.get("score_cp")
    mate = engine_result.get("mate_in")
    source = engine_result.get("source", "local")
    if mate is not None:
        lines.append(f"Engine evaluation: Mate in {abs(mate)} (source: {source})")
    elif cp is not None:
        lines.append(f"Engine evaluation: {cp/100:+.2f} pawns (white, source: {source})")

    top = engine_result.get("top_moves", [])
    if top:
        lines.append(f"Engine top moves: {', '.join(m['san'] for m in top[:3])}")

    return "\n".join(lines)
