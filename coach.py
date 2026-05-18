"""
LLM-powered chess coach.

Maintains a rolling conversation per session and calls Claude to give
contextual guidance, update the user profile, and persist lessons.
"""
from typing import Optional, List, Dict, Any
import json
import chess
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from profile import (
    profile_summary_text,
    append_lesson,
    append_coach_note,
    add_weakness,
    add_strength,
    record_opening,
    save_profile,
)

_SYSTEM_PROMPT = """\
You are ChessMentor, an expert chess coach.  You have been following this
player across multiple sessions.  Your role is to:

1. Analyse the current position and the move just played.
2. Give concise, actionable coaching tailored to the player's level and history.
3. Identify patterns: praise consistent strengths, flag recurring mistakes,
   suggest targeted improvements, and name relevant openings or tactical themes.
4. After your coaching message, emit a JSON block on its own line (no markdown
   fences) in this exact format so the system can update the player profile:

PROFILE_UPDATE:{"lessons":["..."],"weaknesses":["..."],"strengths":["..."],
"opening":{"color":"<white|black>","name":"<opening name or empty>"},
"coach_note":"<one-sentence persistent note or empty>"}

   All fields are optional — omit or leave empty if nothing new to record.
   Only include lessons/weaknesses/strengths that are genuinely new insights.

Keep your coaching reply under 120 words.  Be encouraging but honest.

--- Player Profile ---
{profile}
"""

_client: Optional[anthropic.Anthropic] = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


class CoachSession:
    def __init__(self, profile: dict):
        self.profile = profile
        self.messages: List[Dict[str, Any]] = []
        self.system = _SYSTEM_PROMPT.replace("{profile}", profile_summary_text(profile))

    def _system_with_updated_profile(self) -> str:
        return _SYSTEM_PROMPT.replace("{profile}", profile_summary_text(self.profile))

    def coach(
        self,
        board: chess.Board,
        engine_result: Dict[str, Any],
        last_move_san: Optional[str],
        delta_cp: Optional[int],
        player_color: str,
    ) -> str:
        """
        Send current position context to Claude and return coaching text.
        Also parses PROFILE_UPDATE and mutates self.profile accordingly.
        """
        context = _build_context(board, engine_result, last_move_san, delta_cp, player_color)
        self.messages.append({"role": "user", "content": context})

        response = _get_client().messages.create(
            model=CLAUDE_MODEL,
            max_tokens=512,
            system=self._system_with_updated_profile(),
            messages=self.messages,
        )

        reply = response.content[0].text.strip()
        self.messages.append({"role": "assistant", "content": reply})

        # parse and apply profile updates
        coaching_text = _apply_profile_update(reply, self.profile)
        save_profile(self.profile)

        return coaching_text

    def end_game_summary(self, result: str) -> str:
        """Ask the coach for a post-game summary and profile update."""
        prompt = (
            f"The game just ended: {result}. "
            "Please give a brief post-game summary (strengths, key mistakes, "
            "one concrete improvement goal) and emit a PROFILE_UPDATE as usual."
        )
        self.messages.append({"role": "user", "content": prompt})

        response = _get_client().messages.create(
            model=CLAUDE_MODEL,
            max_tokens=600,
            system=self._system_with_updated_profile(),
            messages=self.messages,
        )

        reply = response.content[0].text.strip()
        self.messages.append({"role": "assistant", "content": reply})

        coaching_text = _apply_profile_update(reply, self.profile)
        self.profile["total_games_analyzed"] = self.profile.get("total_games_analyzed", 0) + 1
        save_profile(self.profile)
        return coaching_text


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
    if mate is not None:
        lines.append(f"Engine evaluation: Mate in {abs(mate)}")
    elif cp is not None:
        lines.append(f"Engine evaluation: {cp/100:+.2f} pawns (white perspective)")

    top = engine_result.get("top_moves", [])
    if top:
        moves_str = ", ".join(m["san"] for m in top[:3])
        lines.append(f"Engine top moves: {moves_str}")

    return "\n".join(lines)


def _apply_profile_update(reply: str, profile: dict) -> str:
    """Strip PROFILE_UPDATE line from reply, apply changes, return clean text."""
    update_marker = "PROFILE_UPDATE:"
    if update_marker not in reply:
        return reply

    parts = reply.split(update_marker, 1)
    coaching_text = parts[0].strip()
    json_str = parts[1].strip().split("\n")[0]

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return coaching_text

    for lesson in data.get("lessons", []):
        if lesson:
            append_lesson(profile, lesson)
    for w in data.get("weaknesses", []):
        if w:
            add_weakness(profile, w)
    for s in data.get("strengths", []):
        if s:
            add_strength(profile, s)
    opening = data.get("opening", {})
    if opening.get("name") and opening.get("color"):
        record_opening(profile, opening["color"], opening["name"])
    note = data.get("coach_note", "")
    if note:
        append_coach_note(profile, note)

    return coaching_text
