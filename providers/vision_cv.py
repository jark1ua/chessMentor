"""
Computer-vision board recognition — no LLM vision tokens required.

Two-tier approach:
  Tier 1 (default): Pure OpenCV heuristics.  Works well for clean screenshots
    of digital chess boards (chess.com, lichess, any flat UI).  No model file.
  Tier 2 (optional): PyTorch CNN for piece classification.  Drop a
    torchscript model at CV_MODEL_PATH for full accuracy on any screenshot.

Algorithm overview
------------------
1. Locate the chess board: find the largest near-square contour in the image.
2. Perspective-warp to a canonical 512×512 flat view.
3. Split into 64 equal squares.
4. For each square:
     a. Compare pixel statistics against expected empty-square colour.
     b. Classify empty vs occupied.
     c. If occupied: infer colour (white/black piece) from relative brightness.
     d. Infer piece type from CNN (Tier 2) or edge/shape heuristics (Tier 1).
5. Assemble FEN placement string.
6. Infer active colour from move context if possible (defaults to white).
"""

from __future__ import annotations

import base64
import io
import math
from typing import Optional, Tuple, List

import chess

try:
    import cv2
    import numpy as np
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

try:
    import torch
    import torchvision.transforms as T
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

from providers.vision import VisionProvider

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

BOARD_SIZE = 512          # canonical warped-board side length in pixels
SQUARE_SIZE = BOARD_SIZE // 8

# Piece-type labels matching the 13-class convention used by most chess
# piece classifiers (index 0 = empty):
#   0:empty 1:wP 2:wN 3:wB 4:wR 5:wQ 6:wK 7:bP 8:bN 9:bB 10:bR 11:bQ 12:bK
_IDX_TO_PIECE = {
    1: (chess.PAWN,   chess.WHITE),
    2: (chess.KNIGHT, chess.WHITE),
    3: (chess.BISHOP, chess.WHITE),
    4: (chess.ROOK,   chess.WHITE),
    5: (chess.QUEEN,  chess.WHITE),
    6: (chess.KING,   chess.WHITE),
    7: (chess.PAWN,   chess.BLACK),
    8: (chess.KNIGHT, chess.BLACK),
    9: (chess.BISHOP, chess.BLACK),
    10:(chess.ROOK,   chess.BLACK),
    11:(chess.QUEEN,  chess.BLACK),
    12:(chess.KING,   chess.BLACK),
}


# -------------------------------------------------------------------
# Tier-1 helpers: OpenCV-only heuristics
# -------------------------------------------------------------------

def _pil_to_cv(img: "Image.Image") -> "np.ndarray":
    arr = np.array(img.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _b64_to_pil(b64: str) -> "Image.Image":
    data = base64.b64decode(b64)
    return Image.open(io.BytesIO(data)).convert("RGB")


def _find_board_contour(gray: "np.ndarray") -> Optional["np.ndarray"]:
    """
    Return the four-corner contour of the chess board, or None if not found.
    Strategy: find the largest near-square quadrilateral contour.
    """
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 120)
    # dilate slightly to close gaps
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    best = None
    best_area = 0
    h, w = gray.shape
    min_area = (min(h, w) * 0.3) ** 2

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) != 4:
            continue
        # Aspect ratio check: board should be roughly square
        x, y, cw, ch = cv2.boundingRect(approx)
        ratio = cw / ch if ch > 0 else 0
        if not (0.7 < ratio < 1.3):
            continue
        if area > best_area:
            best_area = area
            best = approx

    return best


def _order_corners(pts: "np.ndarray") -> "np.ndarray":
    """Order [top-left, top-right, bottom-right, bottom-left]."""
    pts = pts.reshape(4, 2).astype(np.float32)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).flatten()
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]
    return np.array([tl, tr, br, bl], dtype=np.float32)


def _warp_board(img_bgr: "np.ndarray", corners: "np.ndarray") -> "np.ndarray":
    """Perspective-warp *img_bgr* so the board fills a BOARD_SIZE×BOARD_SIZE square."""
    dst = np.array([
        [0, 0],
        [BOARD_SIZE - 1, 0],
        [BOARD_SIZE - 1, BOARD_SIZE - 1],
        [0, BOARD_SIZE - 1],
    ], dtype=np.float32)
    M = cv2.getPerspectiveTransform(corners, dst)
    return cv2.warpPerspective(img_bgr, M, (BOARD_SIZE, BOARD_SIZE))


def _extract_squares(board_bgr: "np.ndarray") -> List["np.ndarray"]:
    """
    Return a list of 64 BGR square images in chess order:
    index 0 = a8 (top-left from white's perspective),
    index 63 = h1 (bottom-right).
    """
    squares = []
    for row in range(8):
        for col in range(8):
            y0 = row * SQUARE_SIZE
            y1 = y0 + SQUARE_SIZE
            x0 = col * SQUARE_SIZE
            x1 = x0 + SQUARE_SIZE
            squares.append(board_bgr[y0:y1, x0:x1])
    return squares


def _estimate_empty_colours(squares: List["np.ndarray"]) -> Tuple[float, float]:
    """
    Estimate the mean brightness of empty light and dark squares by taking
    the lightest and darkest quartiles of per-square mean brightness.
    Returns (light_mean, dark_mean) in [0, 255].
    """
    means = [float(np.mean(sq)) for sq in squares]
    means_sorted = sorted(means)
    n = len(means_sorted)
    # lightest quartile → light empty squares
    light = float(np.mean(means_sorted[3 * n // 4:]))
    # darkest quartile → dark empty squares
    dark = float(np.mean(means_sorted[:n // 4]))
    return light, dark


def _is_light_square(row: int, col: int) -> bool:
    """True if the square at (row, col) is a light square (a8=row0,col0)."""
    # a8 is a dark square in standard chess
    return (row + col) % 2 == 1


def _classify_heuristic(
    sq: "np.ndarray",
    row: int,
    col: int,
    light_empty: float,
    dark_empty: float,
) -> int:
    """
    Return a 0-12 class index using colour/edge heuristics.
    0 = empty, 1-6 = white pieces, 7-12 = black pieces.
    Piece type accuracy is approximate: uses edge density to rank types.
    """
    mean_brightness = float(np.mean(sq))
    is_light = _is_light_square(row, col)
    expected_empty = light_empty if is_light else dark_empty

    # Occupation threshold: if brightness deviates more than 15 % from expected
    deviation = abs(mean_brightness - expected_empty)
    threshold = 0.12 * 255
    if deviation < threshold:
        return 0  # empty

    # Determine piece colour from brightness relative to board background
    # White pieces on dark squares → brighter than expected dark square
    # Black pieces on light squares → darker than expected light square
    piece_is_white: bool
    if is_light:
        piece_is_white = mean_brightness < (expected_empty - 20)
        # counterintuitive? white piece on light square is hard;
        # use edge density instead
        gray_sq = cv2.cvtColor(sq, cv2.COLOR_BGR2GRAY)
        edge_density = float(np.mean(cv2.Canny(gray_sq, 30, 100))) / 255.0
        # If piece is very light on a light square, edge density helps
        if mean_brightness > expected_empty * 0.95:
            piece_is_white = edge_density < 0.08
        else:
            piece_is_white = mean_brightness > expected_empty * 0.5
    else:
        piece_is_white = mean_brightness > expected_empty + 20

    # Rough piece-type estimation from edge density
    gray_sq = cv2.cvtColor(sq, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_sq, 40, 120)
    edge_density = float(np.mean(edges)) / 255.0

    # Map edge density to piece type (very rough heuristic)
    # Pawns: compact, low edge density
    # Knights/Bishops: moderate
    # Rooks: blocky, moderate-high
    # Queen/King: tallest, high edge density
    if edge_density < 0.04:
        ptype = chess.PAWN
    elif edge_density < 0.07:
        ptype = chess.ROOK
    elif edge_density < 0.10:
        ptype = chess.KNIGHT
    elif edge_density < 0.14:
        ptype = chess.BISHOP
    elif edge_density < 0.18:
        ptype = chess.QUEEN
    else:
        ptype = chess.KING

    # Map back to 1-12 index
    offset = 0 if piece_is_white else 6
    ptype_to_base = {
        chess.PAWN: 1, chess.KNIGHT: 2, chess.BISHOP: 3,
        chess.ROOK: 4, chess.QUEEN: 5, chess.KING: 6,
    }
    return ptype_to_base[ptype] + offset


def _squares_to_board(classes: List[int], bottom_is_white: bool) -> chess.Board:
    """
    Construct a chess.Board from 64 class indices.
    classes[0] = square at top-left of the image.
    """
    board = chess.Board(None)  # empty board
    for idx, cls in enumerate(classes):
        if cls == 0:
            continue
        row = idx // 8
        col = idx % 8
        if bottom_is_white:
            # top-left of image = a8, so rank = 7-row, file = col
            rank = 7 - row
            file_ = col
        else:
            # board is flipped: top-left = h1
            rank = row
            file_ = 7 - col
        sq = chess.square(file_, rank)
        piece_type, color = _IDX_TO_PIECE[cls]
        board.set_piece_at(sq, chess.Piece(piece_type, color))
    return board


def _infer_bottom_color(board: chess.Board) -> str:
    """
    Guess which side is at the bottom from where the kings are.
    If white king is in ranks 1-2 and black in ranks 7-8 → white at bottom.
    """
    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)
    if wk is not None and bk is not None:
        if chess.square_rank(wk) < chess.square_rank(bk):
            return "white"
        return "black"
    return "unknown"


# -------------------------------------------------------------------
# Tier-2: Optional PyTorch CNN
# -------------------------------------------------------------------

def _load_torch_model(model_path: str) -> Optional[object]:
    if not _TORCH_AVAILABLE:
        return None
    try:
        model = torch.jit.load(model_path, map_location="cpu")
        model.eval()
        return model
    except Exception:
        return None


def _classify_cnn(model: object, squares: List["np.ndarray"]) -> List[int]:
    """Run CNN model (TorchScript) over all 64 squares at once."""
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize((64, 64)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    tensors = []
    for sq in squares:
        rgb = cv2.cvtColor(sq, cv2.COLOR_BGR2RGB)
        tensors.append(transform(rgb))
    batch = torch.stack(tensors)  # [64, 3, 64, 64]
    with torch.no_grad():
        logits = model(batch)
    return logits.argmax(dim=1).tolist()


# -------------------------------------------------------------------
# Public provider
# -------------------------------------------------------------------

class CVVisionProvider(VisionProvider):
    """
    Board recognition via OpenCV (+ optional PyTorch CNN).
    No LLM vision API calls — zero vision tokens consumed.
    """

    def __init__(self, model_path: Optional[str] = None):
        if not _CV2_AVAILABLE:
            raise ImportError(
                "opencv-python is required for CVVisionProvider. "
                "Install with: pip install opencv-python-headless"
            )
        self._model = _load_torch_model(model_path) if model_path else None
        self._tier = "CNN" if self._model else "heuristic"

    def extract_position(
        self, image_b64: str
    ) -> Tuple[Optional[chess.Board], str]:
        try:
            pil_img = _b64_to_pil(image_b64)
            img_bgr = _pil_to_cv(pil_img)
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            corners = _find_board_contour(gray)
            if corners is None:
                return None, "unknown"

            ordered = _order_corners(corners)
            warped = _warp_board(img_bgr, ordered)
            squares = _extract_squares(warped)

            if self._model is not None:
                classes = _classify_cnn(self._model, squares)
            else:
                light_e, dark_e = _estimate_empty_colours(squares)
                classes = [
                    _classify_heuristic(sq, r, c, light_e, dark_e)
                    for r in range(8)
                    for c, sq in enumerate(squares[r * 8:(r + 1) * 8])
                ]

            # Try white-at-bottom first, then flip if kings are misplaced
            board = _squares_to_board(classes, bottom_is_white=True)
            bottom_color = _infer_bottom_color(board)
            if bottom_color == "black":
                board = _squares_to_board(classes, bottom_is_white=False)

            # Basic sanity: both kings must be present
            if board.king(chess.WHITE) is None or board.king(chess.BLACK) is None:
                return None, "unknown"

            return board, bottom_color

        except Exception:
            return None, "unknown"

    @property
    def tier(self) -> str:
        return self._tier
