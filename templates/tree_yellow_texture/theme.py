"""Design tokens for the Tree Yellow Texture template."""
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

HEADER_H = Inches(0.65)
LOGO_H = Inches(0.45)
LOGO_GAP = Inches(0.20)
EDGE_PAD = Inches(0.5)

WHITE = (0xFF, 0xFF, 0xFF)
GOLD = (0xC8, 0x96, 0x3E)
INK = (0x1F, 0x1F, 0x1F)
MUTED = (0x70, 0x70, 0x70)

FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"

SZ_TITLE = Pt(40)
SZ_SUBTITLE = Pt(18)
SZ_SECTION = Pt(34)
SZ_SLIDE_TITLE = Pt(26)
SZ_BODY = Pt(18)
SZ_CAPTION = Pt(11)
