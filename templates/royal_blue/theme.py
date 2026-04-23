"""Design tokens for the Royal Blue template."""
from pathlib import Path

from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logos"

LOGOS = [
    LOGO_DIR / "KCL.png",
    LOGO_DIR / "KCLNLP.png",
    LOGO_DIR / "Alan.png",
]

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

HEADER_H = Inches(1.05)
LOGO_H = Inches(0.6)
LOGO_GAP = Inches(0.22)
EDGE_PAD = Inches(0.45)

WHITE = (0xFF, 0xFF, 0xFF)
BLUE = (0x1F, 0x3A, 0x93)
BLUE_DEEP = (0x15, 0x29, 0x6B)
INK = (0x1F, 0x1F, 0x1F)
MUTED = (0x55, 0x55, 0x55)

FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"

SZ_TITLE = Pt(44)
SZ_SUBTITLE = Pt(22)
SZ_SECTION = Pt(36)
SZ_HEADER_TITLE = Pt(26)
SZ_HEADER_NOW = Pt(16)
SZ_BODY = Pt(20)
SZ_CAPTION = Pt(14)
