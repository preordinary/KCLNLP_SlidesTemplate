"""Design tokens for the Tree Yellow Texture template."""
from pathlib import Path

from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logos"
GENERATED_DIR = REPO_ROOT / "assets" / "generated"

PARCHMENT_PNG = GENERATED_DIR / "parchment_bg.png"
BRANCH_PNG = GENERATED_DIR / "tree_branch.png"

LOGOS = [
    LOGO_DIR / "KCL.png",
    LOGO_DIR / "KCLNLP.png",
    LOGO_DIR / "Alan.png",
]

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

HEADER_H = Inches(0.65)
LOGO_H = Inches(0.42)
LOGO_GAP = Inches(0.18)
EDGE_PAD = Inches(0.5)

PARCHMENT = (0xF4, 0xEC, 0xD8)
GOLD = (0xC8, 0x96, 0x3E)
BRONZE = (0x8A, 0x6A, 0x2E)
ESPRESSO = (0x2B, 0x1F, 0x12)
OLIVE = (0x6B, 0x7A, 0x3E)
MUTED = (0x6E, 0x5A, 0x3C)

FONT_HEAD = "Georgia"
FONT_BODY = "Calibri"

SZ_TITLE = Pt(44)
SZ_SUBTITLE = Pt(20)
SZ_SECTION = Pt(36)
SZ_SLIDE_TITLE = Pt(28)
SZ_BODY = Pt(18)
SZ_CAPTION = Pt(11)
