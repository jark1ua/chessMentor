"""
Screen region capture.  Returns PIL Images.
"""
import time
import base64
import io
from typing import Optional, Tuple

try:
    import mss
    import mss.tools
    _MSS_AVAILABLE = True
except ImportError:
    _MSS_AVAILABLE = False

try:
    from PIL import Image, ImageGrab
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


Region = Tuple[int, int, int, int]  # left, top, width, height


def select_region_interactively() -> Region:
    """
    Print instructions and read region coords from stdin.
    Returns (left, top, width, height).
    """
    print("\nEnter the screen region to monitor for the chess board.")
    print("You can use a tool like xrandr / your OS snipping tool to find pixel coords.")
    left  = int(input("  left   (x): "))
    top   = int(input("  top    (y): "))
    width = int(input("  width     : "))
    height= int(input("  height    : "))
    return (left, top, width, height)


def capture(region: Region) -> "Image.Image":
    """Capture *region* and return a PIL Image."""
    left, top, width, height = region
    if _MSS_AVAILABLE:
        with mss.mss() as sct:
            monitor = {"left": left, "top": top, "width": width, "height": height}
            raw = sct.grab(monitor)
            img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
            return img
    elif _PIL_AVAILABLE:
        return ImageGrab.grab(bbox=(left, top, left + width, top + height))
    else:
        raise RuntimeError("Neither mss nor Pillow ImageGrab is available.")


def image_to_base64(img: "Image.Image", fmt: str = "PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode()


def save_debug_image(img: "Image.Image", path: str = "/tmp/chess_capture.png"):
    img.save(path)
