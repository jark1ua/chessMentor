"""
Board position extraction from a screenshot via Claude vision.

Sends the image to Claude and asks it to return the FEN of the visible
position.  Falls back gracefully when the image doesn't show a chess board.
"""
import re
from typing import Optional, Tuple
import chess
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

_client: Optional[anthropic.Anthropic] = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


_VISION_PROMPT = """\
You are a chess position recognizer. The user has provided a screenshot that
may contain a chess board.

Your task:
1. Identify whether a chess board is visible in the image.
2. If yes, determine the position of all pieces and return the FEN string for
   that position (piece placement only — you may omit castling/en-passant/clocks
   if you cannot reliably determine them, but include the active color if you
   can tell whose turn it is).
3. Also identify the player color at the bottom of the board (white or black).
4. If no board is visible or the position is unclear, respond with: NO_BOARD

Respond ONLY in this JSON format (no markdown, no explanation):
{"fen": "<FEN or NO_BOARD>", "bottom_color": "<white|black|unknown>"}
"""


def extract_position(image_b64: str) -> Tuple[Optional[chess.Board], str]:
    """
    Returns (board, bottom_color) or (None, 'unknown') if no board found.
    bottom_color is 'white' or 'black'.
    """
    client = _get_client()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_b64,
                        },
                    },
                    {"type": "text", "text": _VISION_PROMPT},
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()

    # extract JSON even if model wraps it
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        return None, "unknown"

    import json
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None, "unknown"

    fen = data.get("fen", "NO_BOARD")
    bottom_color = data.get("bottom_color", "unknown")

    if fen == "NO_BOARD" or not fen:
        return None, bottom_color

    # validate / parse FEN
    try:
        # If only piece placement was returned, add defaults
        parts = fen.split()
        if len(parts) == 1:
            fen = fen + " w - - 0 1"
        board = chess.Board(fen)
        return board, bottom_color
    except ValueError:
        return None, bottom_color
