# Sage Mist & Dusty Rose Templates — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two Morandi-palette academic templates (Sage Mist green, Dusty Rose red) sharing a new "Side Rail" skeleton, each with a 16:9 deck and an A0 poster, plus preview images and README updates.

**Architecture:** Each template lives in its own folder under `templates/` with `theme.py`, `build.py`, `poster.py` — matching the repo's existing per-template convention. The two new templates share byte-for-byte identical `build.py` / `poster.py` files; only `theme.py` differs. Existing Royal Blue / Tree Yellow templates are untouched.

**Tech Stack:** Python 3, `python-pptx>=1.0.2`, `Pillow>=10.0`, `libreoffice --headless` + `pdftoppm` for PNG previews.

**Spec:** `docs/superpowers/specs/2026-05-25-morandi-templates-design.md`

---

## File Structure

**Created:**
- `templates/sage_mist/theme.py` — Sage Mist palette + shared geometry/typography
- `templates/sage_mist/build.py` — 9-slide deck builder
- `templates/sage_mist/poster.py` — A0 poster builder
- `templates/dusty_rose/theme.py` — Dusty Rose palette + shared geometry/typography
- `templates/dusty_rose/build.py` — identical to Sage Mist's `build.py` except `import theme`
- `templates/dusty_rose/poster.py` — identical to Sage Mist's `poster.py` except `import theme`
- `templates/sage_mist/KCLNLP_SageMist.pptx` (generated)
- `templates/sage_mist/KCLNLP_SageMist_Poster.pptx` (generated)
- `templates/dusty_rose/KCLNLP_DustyRose.pptx` (generated)
- `templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx` (generated)
- `assets/images/sage_mist_title.png` (generated)
- `assets/images/sage_mist_content.png` (generated)
- `assets/images/sage_mist_poster.png` (generated)
- `assets/images/dusty_rose_title.png` (generated)
- `assets/images/dusty_rose_content.png` (generated)
- `assets/images/dusty_rose_poster.png` (generated)
- `scripts/render_previews.sh` — helper for converting pptx → png (kept in repo for future regeneration)

**Modified:**
- `README.md` — add Sage Mist + Dusty Rose sections under Slides Templates and Posters Templates; reword overview from "two templates" to "four templates"
- `.gitignore` — already includes `.superpowers/`; no further changes needed

**Untouched:**
- `templates/royal_blue/` (all files)
- `templates/tree_yellow/` (all files)
- `assets/logos/` (KCL.png / KCLNLP.png / Alan.png reused)
- `CLAUDE.md`, `requirements.txt`

---

## Notes for the Engineer

**Repo conventions you must match:**
- Geometry constants use `pptx.util.Inches` / `Emu` / `Pt` — never raw integers.
- Each template folder is self-contained. **Do not extract shared helpers.** The repo deliberately keeps templates as siblings even when there's duplication.
- `theme.py` is the single source of truth for colours, fonts, sizes, and geometry per template. `build.py` and `poster.py` only call `import theme as T`.
- Slide layouts use `prs.slide_layouts[6]` (the blank layout) — shapes are drawn programmatically, not via PPTX placeholders.
- Logo widths are computed from image aspect ratio via PIL (`Image.open(p).size`).

**Verification commands you'll run repeatedly:**
- `python templates/<theme>/build.py` — generates the deck `.pptx`
- `python templates/<theme>/poster.py` — generates the poster `.pptx`
- `libreoffice --headless --convert-to pdf <file>.pptx --outdir <dir>` — converts to PDF for preview
- `pdftoppm -png -r 150 <file>.pdf <prefix>` — converts PDF pages to PNG

**No test framework needed.** This repo has no tests; verification is visual + structural (file opens, slide count correct, colours match). Each generation step ends in opening the resulting `.pptx` headlessly and confirming page count.

---

## Task 1: Sage Mist theme.py

**Files:**
- Create: `templates/sage_mist/theme.py`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p templates/sage_mist
```

- [ ] **Step 2: Write `templates/sage_mist/theme.py`**

```python
"""Design tokens for the Sage Mist template.

A sage-green Morandi palette for academic talks. Shares the Side Rail
skeleton with Dusty Rose; only the palette differs.
"""
from pathlib import Path

from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logos"

LOGOS = [
    LOGO_DIR / "KCL.png",
    LOGO_DIR / "KCLNLP.png",
    LOGO_DIR / "Alan.png",
]

# 16:9 slide
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Side Rail geometry
RAIL_W = Inches(0.18)
EDGE_PAD_L = Inches(0.55)   # gap between rail and content
EDGE_PAD_R = Inches(0.45)
TITLE_TOP = Inches(0.5)
TITLE_RULE_W = Inches(0.6)
TITLE_RULE_H = Inches(0.04)
BODY_TOP = Inches(1.35)
FOOTER_H = Inches(0.5)
LOGO_H = Inches(0.45)
LOGO_GAP = Inches(0.18)

# Palette — Sage Mist
RAIL   = (0x5C, 0x72, 0x61)
ACCENT = (0xA7, 0xB5, 0xA0)
TINT   = (0xED, 0xEA, 0xE0)
INK    = (0x2B, 0x2F, 0x2A)
MUTED  = (0x6F, 0x75, 0x6C)
WHITE  = (0xFF, 0xFF, 0xFF)

# Typography
FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"
FONT_SERIF = "Georgia"

SZ_TITLE_HERO  = Pt(44)
SZ_SUBTITLE    = Pt(22)
SZ_SECTION     = Pt(36)
SZ_SLIDE_TITLE = Pt(26)
SZ_BODY        = Pt(20)
SZ_BULLET_NUM  = Pt(28)
SZ_PULLQUOTE   = Pt(36)
SZ_CAPTION     = Pt(14)
SZ_LABEL       = Pt(11)
```

- [ ] **Step 3: Verify it imports**

Run: `python -c "import sys; sys.path.insert(0, 'templates/sage_mist'); import theme; print(theme.RAIL, theme.SLIDE_W)"`
Expected: `(92, 114, 97) 12192000`

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/theme.py
git commit -m "$(cat <<'EOF'
add Sage Mist theme (sage-green Morandi palette)

Geometry and typography tokens for the new Side Rail skeleton.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Sage Mist build.py — scaffold + helpers

**Files:**
- Create: `templates/sage_mist/build.py`

This task writes the file with the imports, helper functions, and a stub `build()` that produces an empty `.pptx`. Each subsequent task adds one slide layout.

- [ ] **Step 1: Write `templates/sage_mist/build.py`**

```python
"""Build the Sage Mist demo deck.

Run: python templates/sage_mist/build.py

A sage-green Morandi deck with the new Side Rail skeleton — a vertical
brand-color rail on the left, slide title in the body, logos in the footer.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))

import theme as T

OUTPUT = Path(__file__).resolve().parent / "KCLNLP_SageMist.pptx"


def rgb(tup):
    return RGBColor(*tup)


def _logo_width(path, height_emu):
    with Image.open(path) as im:
        w, h = im.size
    return int(height_emu * (w / h))


def _add_text(slide, left, top, width, height, text, *, font, size, color,
              bold=False, italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = size
    run.font.color.rgb = rgb(color)
    run.font.bold = bold
    run.font.italic = italic
    return box


def _add_bullets(slide, left, top, width, height, items, *, size=None, color=None):
    size = size or T.SZ_BODY
    color = color or T.INK
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(10)
        run = p.add_run()
        run.text = f"•  {item}"
        run.font.name = T.FONT_BODY
        run.font.size = size
        run.font.color.rgb = rgb(color)
    return box


def add_rail(slide):
    """Full-bleed vertical brand-color rail on the left edge."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, T.RAIL_W, T.SLIDE_H
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(T.RAIL)
    bar.line.fill.background()


def add_title_rule(slide, left, top, width=None):
    """Short brand-color rule under a slide title."""
    width = width or T.TITLE_RULE_W
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, T.TITLE_RULE_H
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(T.RAIL)
    rule.line.fill.background()


def add_footer_with_logos(slide, *, institution_text="King's College London  ·  KCL NLP"):
    """Single-line footer: institution on the left, three logos on the right."""
    footer_top = T.SLIDE_H - T.FOOTER_H
    body_left = T.RAIL_W + T.EDGE_PAD_L
    right = T.SLIDE_W - T.EDGE_PAD_R

    # Logos, right-aligned
    widths = [_logo_width(p, T.LOGO_H) for p in T.LOGOS]
    total = sum(widths) + T.LOGO_GAP * (len(T.LOGOS) - 1)
    x = right - total
    logo_top = footer_top + (T.FOOTER_H - T.LOGO_H) // 2
    for i, path in enumerate(T.LOGOS):
        slide.shapes.add_picture(str(path), x, logo_top, height=T.LOGO_H)
        x += widths[i] + (T.LOGO_GAP if i < len(T.LOGOS) - 1 else 0)

    # Institution text, left-aligned, vertically centered
    text_w = (right - total) - body_left - Inches(0.2)
    _add_text(
        slide, body_left, footer_top, text_w, T.FOOTER_H,
        institution_text,
        font=T.FONT_BODY, size=T.SZ_CAPTION, color=T.MUTED, italic=True,
        anchor=MSO_ANCHOR.MIDDLE,
    )


def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H
    # Slide functions will be added in subsequent tasks.
    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    build()
```

- [ ] **Step 2: Run it to confirm the scaffold works**

Run: `python templates/sage_mist/build.py`
Expected: prints `wrote .../KCLNLP_SageMist.pptx` and creates the file.

- [ ] **Step 3: Verify the file is a valid empty pptx**

Run: `python -c "from pptx import Presentation; p = Presentation('templates/sage_mist/KCLNLP_SageMist.pptx'); print(f'{len(p.slides)} slides, {p.slide_width}x{p.slide_height}')"`
Expected: `0 slides, 12192000x6858000`

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
scaffold Sage Mist build.py with Side Rail helpers

add_rail / add_title_rule / add_footer_with_logos plus the
text/bullet utilities. Slide layouts will be added in subsequent
commits.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Sage Mist build.py — title slides (left + centered)

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add `slide_title` and `slide_title_centered` functions before `def build():`**

Insert just above `def build():`:

```python
def slide_title(prs):
    """Title slide, left-aligned."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)

    left = T.RAIL_W + T.EDGE_PAD_L
    title_top = Inches(2.7)
    text_w = T.SLIDE_W - left - T.EDGE_PAD_R

    _add_text(
        slide, left, title_top, text_w, Inches(1.4),
        "Talk Title Goes Here",
        font=T.FONT_HEAD, size=T.SZ_TITLE_HERO, color=T.INK, bold=True,
    )

    _add_text(
        slide, left, title_top + Inches(1.3), text_w, Inches(0.6),
        "A concise subtitle or one-line abstract",
        font=T.FONT_BODY, size=T.SZ_SUBTITLE, color=T.MUTED, italic=True,
    )

    rule_y = title_top + Inches(2.05)
    add_title_rule(slide, left, rule_y, width=Inches(1.6))

    _add_text(
        slide, left, rule_y + Inches(0.2), text_w, Inches(0.5),
        "Speaker Name  ·  Affiliation  ·  Month Year",
        font=T.FONT_BODY, size=Pt(16), color=T.INK,
    )

    add_footer_with_logos(slide)


def slide_title_centered(prs):
    """Title slide, centered variant."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)

    body_h = T.SLIDE_H - T.FOOTER_H
    block_h = Inches(3.6)
    block_top = (body_h - block_h) // 2

    # centered top accent line
    accent_w = Inches(1.6)
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        (T.SLIDE_W - accent_w) // 2, block_top,
        accent_w, T.TITLE_RULE_H,
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = rgb(T.RAIL)
    accent.line.fill.background()

    _add_text(
        slide, Inches(0), block_top + Inches(0.35),
        T.SLIDE_W, Inches(1.4),
        "Talk Title Goes Here",
        font=T.FONT_HEAD, size=T.SZ_TITLE_HERO, color=T.INK, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    _add_text(
        slide, Inches(0), block_top + Inches(1.85),
        T.SLIDE_W, Inches(0.7),
        "A concise subtitle or one-line abstract",
        font=T.FONT_BODY, size=T.SZ_SUBTITLE, color=T.MUTED, italic=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    _add_text(
        slide, Inches(0), block_top + Inches(2.85),
        T.SLIDE_W, Inches(0.5),
        "Speaker Name  ·  Affiliation  ·  Month Year",
        font=T.FONT_BODY, size=Pt(16), color=T.INK,
        align=PP_ALIGN.CENTER,
    )

    add_footer_with_logos(slide)
```

- [ ] **Step 2: Wire them into `build()`**

Replace the body of `def build():` with:

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 3: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `2`.

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add title-slide layouts to Sage Mist deck

slide_title (left-aligned) and slide_title_centered (centered).

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Sage Mist build.py — section divider

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add `slide_section` function before `def build():`**

```python
def slide_section(prs, number="01", title="Section Heading"):
    """Section divider with large numeral and section name."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)

    left = T.RAIL_W + T.EDGE_PAD_L
    row_top = Inches(2.7)
    row_h = Inches(1.6)

    _add_text(
        slide, left, row_top, Inches(2.0), row_h,
        number,
        font=T.FONT_HEAD, size=Pt(72), color=T.RAIL, bold=True,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    # Vertical divider between number and title
    rule_x = left + Inches(2.2)
    rule = slide.shapes.add_connector(
        1, rule_x, row_top + Inches(0.3),
        rule_x, row_top + row_h - Inches(0.3),
    )
    rule.line.color.rgb = rgb(T.RAIL)
    rule.line.width = Emu(12700)

    _add_text(
        slide, rule_x + Inches(0.3), row_top,
        Inches(9.0), row_h,
        title,
        font=T.FONT_HEAD, size=T.SZ_SECTION, color=T.INK, bold=True,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    _add_text(
        slide, rule_x + Inches(0.3), row_top + row_h + Inches(0.1),
        Inches(9.0), Inches(0.5),
        "An optional one-line summary of this section",
        font=T.FONT_BODY, size=Pt(18), color=T.MUTED, italic=True,
    )

    add_footer_with_logos(slide)
```

- [ ] **Step 2: Add `slide_section(prs, number="01", title="Background")` to `build()`**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 3: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `3`.

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add section-divider layout to Sage Mist deck

Big numeral + vertical rule + section title + one-line summary.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Sage Mist build.py — standard content slide

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add a slide-title helper at the top of the file (after `_add_bullets`)**

Add this helper just below `_add_bullets`:

```python
def add_slide_title(slide, title):
    """Slide title in the body area, with a short brand-color rule beneath."""
    left = T.RAIL_W + T.EDGE_PAD_L
    text_w = T.SLIDE_W - left - T.EDGE_PAD_R
    _add_text(
        slide, left, T.TITLE_TOP, text_w, Inches(0.55),
        title,
        font=T.FONT_HEAD, size=T.SZ_SLIDE_TITLE, color=T.INK, bold=True,
    )
    add_title_rule(slide, left, T.TITLE_TOP + Inches(0.65))
```

- [ ] **Step 2: Add `slide_content` function before `def build():`**

```python
def slide_content(prs, title="Slide title", bullets=None):
    bullets = bullets or [
        "Lead with the main claim — what the reader should take away",
        "Supporting detail, ideally a number or concrete example",
        "A second supporting point that extends the first",
        "A fourth line of room — the body has the full slide to breathe",
        "Edge case, caveat, or the one thing not to forget",
    ]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)
    add_slide_title(slide, title)

    body_left = T.RAIL_W + T.EDGE_PAD_L
    body_w = T.SLIDE_W - body_left - T.EDGE_PAD_R
    body_h = T.SLIDE_H - T.BODY_TOP - T.FOOTER_H - Inches(0.2)

    _add_bullets(slide, body_left, T.BODY_TOP, body_w, body_h, bullets)
    add_footer_with_logos(slide)
```

- [ ] **Step 3: Add `slide_content(prs, title="Slide title")` to `build()`**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")
    slide_content(prs, title="Slide title")

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 4: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `4`.

- [ ] **Step 5: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add standard content layout to Sage Mist deck

Slide title in the body, 5-bullet workhorse layout.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Sage Mist build.py — callout overlay + content+callout slide

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add the `add_callout` helper after `add_slide_title`**

```python
def add_callout(slide, *, left, top, width,
                label="TAKEAWAY", text="The single point worth remembering."):
    """Tinted callout box with a brand-color left border and uppercase label.

    Reusable overlay — can be dropped on any content slide.
    """
    # Height is computed from text length, but for the demo we fix it.
    box_h = Inches(1.2)

    fill_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, box_h
    )
    fill_box.fill.solid()
    fill_box.fill.fore_color.rgb = rgb(T.TINT)
    fill_box.line.fill.background()

    border = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, Inches(0.08), box_h
    )
    border.fill.solid()
    border.fill.fore_color.rgb = rgb(T.RAIL)
    border.line.fill.background()

    text_left = left + Inches(0.25)
    text_w = width - Inches(0.4)

    _add_text(
        slide, text_left, top + Inches(0.18), text_w, Inches(0.3),
        label,
        font=T.FONT_HEAD, size=T.SZ_LABEL, color=T.RAIL, bold=True,
    )

    _add_text(
        slide, text_left, top + Inches(0.5), text_w, box_h - Inches(0.6),
        text,
        font=T.FONT_BODY, size=Pt(18), color=T.INK,
    )
```

- [ ] **Step 2: Add `slide_content_with_callout` function before `def build():`**

```python
def slide_content_with_callout(prs, title="Slide title"):
    """Content slide that demonstrates the callout overlay."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)
    add_slide_title(slide, title)

    body_left = T.RAIL_W + T.EDGE_PAD_L
    body_w = T.SLIDE_W - body_left - T.EDGE_PAD_R

    _add_bullets(
        slide, body_left, T.BODY_TOP, body_w, Inches(2.6),
        [
            "Set up the experimental finding",
            "Note the comparison or baseline",
            "Quantify the effect with one or two numbers",
        ],
    )

    add_callout(
        slide,
        left=body_left, top=T.BODY_TOP + Inches(3.0), width=body_w,
        label="TAKEAWAY",
        text="Across 5 benchmarks, our 1.3B model matches a 7B baseline at 18% of the inference cost.",
    )

    add_footer_with_logos(slide)
```

- [ ] **Step 3: Add to `build()`**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")
    slide_content(prs, title="Slide title")
    slide_content_with_callout(prs, title="Headline finding")

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 4: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `5`.

- [ ] **Step 5: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add callout overlay and content+callout layout to Sage Mist

add_callout is a reusable overlay; slide_content_with_callout
demonstrates the intended usage on a standard content slide.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Sage Mist build.py — numbered list slide

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add `slide_numbered_list` function before `def build():`**

```python
def slide_numbered_list(prs, title="Three contributions", items=None):
    """01 / 02 / 03 numbered list with horizontal divider lines."""
    items = items or [
        "Lead with the main claim worth remembering",
        "Supporting detail, a number or concrete example",
        "A second supporting point that extends the first",
    ]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)
    add_slide_title(slide, title)

    body_left = T.RAIL_W + T.EDGE_PAD_L
    body_w = T.SLIDE_W - body_left - T.EDGE_PAD_R

    row_h = Inches(0.85)
    num_w = Inches(0.9)
    text_left = body_left + num_w + Inches(0.15)
    text_w = body_w - num_w - Inches(0.15)

    for i, item in enumerate(items):
        y = T.BODY_TOP + Inches(0.15) + row_h * i
        _add_text(
            slide, body_left, y, num_w, row_h,
            f"{i + 1:02d}",
            font=T.FONT_HEAD, size=T.SZ_BULLET_NUM, color=T.RAIL, bold=True,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        _add_text(
            slide, text_left, y, text_w, row_h,
            item,
            font=T.FONT_BODY, size=T.SZ_BODY, color=T.INK,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        # Divider line under each row, full width
        div_y = y + row_h
        div = slide.shapes.add_connector(
            1, body_left, div_y, body_left + body_w, div_y
        )
        div.line.color.rgb = rgb(T.ACCENT)
        div.line.width = Emu(6350)

    add_footer_with_logos(slide)
```

- [ ] **Step 2: Add to `build()`**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")
    slide_content(prs, title="Slide title")
    slide_content_with_callout(prs, title="Headline finding")
    slide_numbered_list(prs, title="Three contributions")

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 3: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `6`.

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add numbered-list layout to Sage Mist deck

01/02/03 with horizontal divider lines; max 5 items.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Sage Mist build.py — two-column slide

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add `slide_two_column` function before `def build():`**

```python
def slide_two_column(prs, title="Result"):
    """Two-column: figure placeholder on the left, caption + bullets on the right."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)
    add_slide_title(slide, title)

    body_left = T.RAIL_W + T.EDGE_PAD_L
    body_w = T.SLIDE_W - body_left - T.EDGE_PAD_R
    body_h = T.SLIDE_H - T.BODY_TOP - T.FOOTER_H - Inches(0.2)

    col_gap = Inches(0.45)
    col_w = (body_w - col_gap) // 2

    # Left column — figure placeholder
    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, body_left, T.BODY_TOP, col_w, body_h
    )
    frame.fill.background()
    frame.line.color.rgb = rgb(T.ACCENT)
    frame.line.width = Emu(6350)
    _add_text(
        slide, body_left, T.BODY_TOP, col_w, body_h,
        "[ figure / diagram ]",
        font=T.FONT_BODY, size=Pt(18), color=T.MUTED, italic=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    # Right column — caption + bullets
    text_x = body_left + col_w + col_gap
    _add_text(
        slide, text_x, T.BODY_TOP, col_w, Inches(0.5),
        "Caption or claim",
        font=T.FONT_HEAD, size=Pt(22), color=T.INK, bold=True,
    )
    _add_bullets(
        slide, text_x, T.BODY_TOP + Inches(0.8),
        col_w, body_h - Inches(0.8),
        [
            "Explain what the figure shows",
            "Call out the one feature worth noting",
            "Relate it back to the slide's main point",
        ],
        size=Pt(18),
    )

    add_footer_with_logos(slide)
```

- [ ] **Step 2: Add to `build()`**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")
    slide_content(prs, title="Slide title")
    slide_content_with_callout(prs, title="Headline finding")
    slide_numbered_list(prs, title="Three contributions")
    slide_two_column(prs, title="Result")

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 3: Generate and verify**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; print(len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides))"`
Expected: prints `wrote ...` then `7`.

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/build.py
git commit -m "$(cat <<'EOF'
add two-column layout to Sage Mist deck

Figure placeholder on the left, caption + bullets on the right.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Sage Mist build.py — pull-quote and thanks slides

**Files:**
- Modify: `templates/sage_mist/build.py`

- [ ] **Step 1: Add `slide_pullquote` and `slide_thanks_centered` before `def build():`**

```python
def slide_pullquote(prs, quote=None, attribution="Main result"):
    """Single-slide highlight — large Georgia italic quote."""
    quote = quote or "Smaller models, trained on the right data, beat larger ones."
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)

    body_h = T.SLIDE_H - T.FOOTER_H
    block_h = Inches(3.4)
    block_top = (body_h - block_h) // 2

    # Large decorative opening quote glyph in ACCENT
    _add_text(
        slide, T.RAIL_W + T.EDGE_PAD_L, block_top - Inches(0.4),
        Inches(1.6), Inches(1.4),
        "“",  # left double quotation mark
        font=T.FONT_SERIF, size=Pt(120), color=T.ACCENT, bold=True,
    )

    # Quote text — Georgia italic, large
    text_left = T.RAIL_W + T.EDGE_PAD_L + Inches(0.1)
    text_w = T.SLIDE_W - text_left - T.EDGE_PAD_R
    _add_text(
        slide, text_left, block_top + Inches(0.9), text_w, Inches(2.0),
        quote,
        font=T.FONT_SERIF, size=T.SZ_PULLQUOTE, color=T.INK, italic=True,
    )

    # Attribution line, small uppercase
    rule_y = block_top + block_h
    add_title_rule(slide, text_left, rule_y, width=Inches(0.5))
    _add_text(
        slide, text_left, rule_y + Inches(0.15), text_w, Inches(0.4),
        attribution.upper(),
        font=T.FONT_HEAD, size=T.SZ_LABEL, color=T.RAIL, bold=True,
    )

    add_footer_with_logos(slide)


def slide_thanks_centered(prs):
    """Centered Thank-you / Q&A slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rail(slide)

    body_h = T.SLIDE_H - T.FOOTER_H
    block_h = Inches(3.4)
    block_top = (body_h - block_h) // 2

    accent_w = Inches(1.8)
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        (T.SLIDE_W - accent_w) // 2, block_top,
        accent_w, T.TITLE_RULE_H,
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = rgb(T.RAIL)
    accent.line.fill.background()

    _add_text(
        slide, Inches(0), block_top + Inches(0.35),
        T.SLIDE_W, Inches(1.6),
        "Thank you",
        font=T.FONT_HEAD, size=Pt(56), color=T.INK, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    _add_text(
        slide, Inches(0), block_top + Inches(2.1),
        T.SLIDE_W, Inches(0.6),
        "Questions & discussion",
        font=T.FONT_BODY, size=Pt(22), color=T.MUTED, italic=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    _add_text(
        slide, Inches(0), block_top + Inches(2.85),
        T.SLIDE_W, Inches(0.45),
        "speaker@kcl.ac.uk  ·  kclnlp.github.io",
        font=T.FONT_BODY, size=Pt(16), color=T.INK,
        align=PP_ALIGN.CENTER,
    )

    add_footer_with_logos(slide)
```

- [ ] **Step 2: Wire them into `build()` (final order)**

```python
def build():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_title_centered(prs)
    slide_section(prs, number="01", title="Background")
    slide_content(prs, title="Slide title")
    slide_content_with_callout(prs, title="Headline finding")
    slide_numbered_list(prs, title="Three contributions")
    slide_two_column(prs, title="Result")
    slide_pullquote(prs)
    slide_thanks_centered(prs)

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")
```

- [ ] **Step 3: Generate and verify final slide count**

Run: `python templates/sage_mist/build.py && python -c "from pptx import Presentation; p = Presentation('templates/sage_mist/KCLNLP_SageMist.pptx'); print(f'{len(p.slides)} slides')"`
Expected: prints `wrote ...` then `9 slides`.

- [ ] **Step 4: Open the file in LibreOffice headlessly and confirm no errors**

Run: `libreoffice --headless --convert-to pdf templates/sage_mist/KCLNLP_SageMist.pptx --outdir /tmp/ 2>&1 | tail -5`
Expected: prints `convert ... -> /tmp/KCLNLP_SageMist.pdf using filter ...` with no errors.

- [ ] **Step 5: Commit**

```bash
git add templates/sage_mist/build.py templates/sage_mist/KCLNLP_SageMist.pptx
git commit -m "$(cat <<'EOF'
complete Sage Mist deck: add pull-quote and thanks layouts

Final 9-slide demo deck:
  title, title-centered, section, content, content+callout,
  numbered-list, two-column, pull-quote, thanks-centered.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Sage Mist poster.py — full A0 poster

**Files:**
- Create: `templates/sage_mist/poster.py`

This task creates the entire poster in one file. It's longer than a typical task, but it's a single coherent unit and there are no intermediate verifiable states.

- [ ] **Step 1: Write `templates/sage_mist/poster.py`**

```python
"""Build the Sage Mist A0 poster.

Run: python templates/sage_mist/poster.py

A0 portrait (841 x 1189 mm) single-page poster. Side Rail extends full
bleed down the left edge; logos are in the header (not the footer —
on A0 the footer is too far from the eye-line). Body laid out in two
columns. Matches the deck's Sage Mist palette and visual language.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))

import theme as T

OUTPUT = Path(__file__).resolve().parent / "KCLNLP_SageMist_Poster.pptx"

# A0 portrait: 841 x 1189 mm
SLIDE_W = Inches(33.1102)
SLIDE_H = Inches(46.8110)

# Scaled-up Side Rail for A0
RAIL_W = Inches(0.7)
EDGE_PAD = Inches(1.0)
HEADER_H = Inches(6.5)
LOGO_H = Inches(1.5)
LOGO_GAP = Inches(0.55)
FOOTER_H = Inches(1.5)
COL_GAP = Inches(1.2)
N_COLS = 2

SZ_POSTER_TITLE   = Pt(88)
SZ_AUTHORS        = Pt(36)
SZ_AFFIL          = Pt(26)
SZ_SECTION_HEAD   = Pt(48)
SZ_POSTER_BODY    = Pt(26)
SZ_POSTER_CAPTION = Pt(20)
SZ_FOOTER         = Pt(24)


def rgb(tup):
    return RGBColor(*tup)


def _logo_width(path, height_emu):
    with Image.open(path) as im:
        w, h = im.size
    return int(height_emu * (w / h))


def _add_text(slide, left, top, width, height, text, *, font, size, color,
              bold=False, italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = size
    run.font.color.rgb = rgb(color)
    run.font.bold = bold
    run.font.italic = italic
    return box


def _add_bullets(slide, left, top, width, height, items, *, size=SZ_POSTER_BODY,
                 color=None):
    color = color if color is not None else T.INK
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(14)
        run = p.add_run()
        run.text = f"•  {item}"
        run.font.name = T.FONT_BODY
        run.font.size = size
        run.font.color.rgb = rgb(color)
    return box


def add_rail(slide):
    """Full-bleed brand-color rail on the left edge."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, RAIL_W, SLIDE_H
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(T.RAIL)
    bar.line.fill.background()


def add_poster_header(slide, *, title, authors, affiliations):
    """Header: title + authors + affiliations on the left, logos on the right."""
    text_left = RAIL_W + EDGE_PAD
    right = SLIDE_W - EDGE_PAD

    widths = [_logo_width(p, LOGO_H) for p in T.LOGOS]
    total = sum(widths) + LOGO_GAP * (len(T.LOGOS) - 1)
    logos_left = right - total
    logo_top = Inches(1.0)

    x = logos_left
    for i, path in enumerate(T.LOGOS):
        slide.shapes.add_picture(str(path), x, logo_top, height=LOGO_H)
        x += widths[i] + (LOGO_GAP if i < len(T.LOGOS) - 1 else 0)

    text_w = logos_left - text_left - Inches(0.5)

    _add_text(slide, text_left, Inches(0.8),
              text_w, Inches(3.6),
              title,
              font=T.FONT_HEAD, size=SZ_POSTER_TITLE, color=T.INK, bold=True)

    _add_text(slide, text_left, Inches(4.6),
              text_w, Inches(0.9),
              authors,
              font=T.FONT_HEAD, size=SZ_AUTHORS, color=T.INK)

    _add_text(slide, text_left, Inches(5.6),
              text_w, Inches(0.7),
              affiliations,
              font=T.FONT_BODY, size=SZ_AFFIL, color=T.MUTED, italic=True)

    # Short brand-color rule under the header block
    rule_y = HEADER_H
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, text_left, rule_y, Inches(2.5), Inches(0.08)
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(T.RAIL)
    rule.line.fill.background()


def add_section(slide, left, top, width, text):
    """Section heading with a short brand-color underline."""
    _add_text(slide, left, top, width, Inches(0.95),
              text, font=T.FONT_HEAD, size=SZ_SECTION_HEAD,
              color=T.INK, bold=True)
    rule_y = top + Inches(1.0)
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, rule_y, Inches(2.0), Inches(0.06)
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(T.RAIL)
    rule.line.fill.background()
    return rule_y + Inches(0.3)


def add_figure_placeholder(slide, left, top, width, height, caption):
    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    frame.fill.background()
    frame.line.color.rgb = rgb(T.ACCENT)
    frame.line.width = Emu(12700)
    _add_text(slide, left, top, width, height,
              "[ figure / diagram ]",
              font=T.FONT_BODY, size=Pt(28), color=T.MUTED, italic=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_text(slide, left, top + height + Inches(0.2),
              width, Inches(0.5),
              caption,
              font=T.FONT_BODY, size=SZ_POSTER_CAPTION,
              color=T.MUTED, italic=True)


def add_footer(slide):
    rule_y = SLIDE_H - FOOTER_H
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, EDGE_PAD + RAIL_W, rule_y,
        SLIDE_W - 2 * EDGE_PAD - RAIL_W, Inches(0.05)
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(T.RAIL)
    rule.line.fill.background()

    _add_text(slide, RAIL_W + EDGE_PAD, rule_y + Inches(0.25),
              SLIDE_W - 2 * EDGE_PAD - RAIL_W, Inches(0.6),
              "speaker@kcl.ac.uk  ·  kclnlp.github.io  ·  @kclnlp",
              font=T.FONT_BODY, size=SZ_FOOTER, color=T.INK)

    _add_text(slide, RAIL_W + EDGE_PAD, rule_y + Inches(0.75),
              SLIDE_W - 2 * EDGE_PAD - RAIL_W, Inches(0.5),
              "King's College London  ·  NLP Group  ·  Conference Year",
              font=T.FONT_BODY, size=SZ_POSTER_CAPTION,
              color=T.MUTED, italic=True)


def build_poster():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_rail(slide)
    add_poster_header(
        slide,
        title="Your Poster Title Goes Here",
        authors="First Author · Second Author · Third Author",
        affiliations="King's College London  ·  KCL NLP  ·  The Alan Turing Institute",
    )

    # Two-column body
    body_top = HEADER_H + Inches(0.8)
    body_bottom = SLIDE_H - FOOTER_H - Inches(0.4)
    body_h = body_bottom - body_top
    usable_w = SLIDE_W - 2 * EDGE_PAD - RAIL_W
    col_w = (usable_w - COL_GAP * (N_COLS - 1)) // N_COLS
    col_xs = [RAIL_W + EDGE_PAD + (col_w + COL_GAP) * i for i in range(N_COLS)]

    # Column 1: Introduction + Method
    y = body_top
    y = add_section(slide, col_xs[0], y, col_w, "Introduction")
    intro = _add_text(
        slide, col_xs[0], y, col_w, Inches(5.5),
        "Open with the problem and why it matters. Frame the gap in "
        "prior work and state the contribution in one sentence. Use "
        "this wider column to set up the context the reader needs to "
        "understand the method and results.",
        font=T.FONT_BODY, size=SZ_POSTER_BODY, color=T.INK,
    )
    y = y + Inches(5.5)

    y = add_section(slide, col_xs[0], y + Inches(0.4), col_w, "Method")
    _add_bullets(
        slide, col_xs[0], y, col_w, Inches(20.0),
        [
            "Dataset — what you used and how it was collected",
            "Model / algorithm — architecture, training regime, hyper-parameters",
            "Evaluation — metrics, baselines, held-out sets",
            "Implementation — reproducibility notes, compute budget",
            "Ablation — what you varied to isolate each effect",
        ],
    )

    # Column 2: Results + Conclusion + References + Acknowledgements
    y = body_top
    y = add_section(slide, col_xs[1], y, col_w, "Results")
    fig_h = Inches(10.0)
    add_figure_placeholder(
        slide, col_xs[1], y, col_w, fig_h,
        "Figure 1. Main result — replace this box with your chart.",
    )
    y = y + fig_h + Inches(1.0)
    _add_bullets(
        slide, col_xs[1], y, col_w, Inches(6.5),
        [
            "Headline number — the single result the reader must remember",
            "Second finding — what changed when you varied X",
            "Error analysis — where the method still fails",
            "Comparison — how this relates to the strongest baseline",
        ],
    )
    y = y + Inches(6.5)

    y = add_section(slide, col_xs[1], y + Inches(0.4), col_w, "Conclusion")
    _add_text(
        slide, col_xs[1], y, col_w, Inches(4.0),
        "Restate the contribution in the terms of the result. Note the "
        "one limitation that most shapes when to use (or not use) this "
        "approach, and point to the next question it opens up.",
        font=T.FONT_BODY, size=SZ_POSTER_BODY, color=T.INK,
    )
    y = y + Inches(4.0)

    y = add_section(slide, col_xs[1], y + Inches(0.3), col_w, "References")
    _add_bullets(
        slide, col_xs[1], y, col_w, Inches(3.8),
        [
            "Author, A. et al. (Year). Title. Venue.",
            "Author, B. & Author, C. (Year). Title. Venue.",
            "Author, D. (Year). Title. Venue.",
        ],
        size=SZ_POSTER_CAPTION, color=T.MUTED,
    )
    y = y + Inches(4.0)

    y = add_section(slide, col_xs[1], y, col_w, "Acknowledgements")
    _add_text(
        slide, col_xs[1], y, col_w, Inches(2.0),
        "Funding, collaborators, and compute providers who made this work possible.",
        font=T.FONT_BODY, size=SZ_POSTER_CAPTION, color=T.MUTED, italic=True,
    )

    add_footer(slide)

    # QR placeholder, bottom-right above the footer rule
    qr_side = Inches(2.4)
    qr_x = SLIDE_W - EDGE_PAD - qr_side
    qr_y = SLIDE_H - FOOTER_H - qr_side - Inches(0.5)
    qr = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, qr_x, qr_y, qr_side, qr_side
    )
    qr.fill.background()
    qr.line.color.rgb = rgb(T.ACCENT)
    qr.line.width = Emu(19050)
    _add_text(slide, qr_x, qr_y, qr_side, qr_side,
              "[ QR ]",
              font=T.FONT_BODY, size=Pt(24), color=T.MUTED, italic=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    build_poster()
```

- [ ] **Step 2: Generate and verify**

Run: `python templates/sage_mist/poster.py && python -c "from pptx import Presentation; p = Presentation('templates/sage_mist/KCLNLP_SageMist_Poster.pptx'); print(f'{len(p.slides)} slide, {p.slide_width/914400:.2f}x{p.slide_height/914400:.2f} in')"`
Expected: prints `wrote ...` then `1 slide, 33.11x46.81 in`.

- [ ] **Step 3: Headless render to PDF to confirm no errors**

Run: `libreoffice --headless --convert-to pdf templates/sage_mist/KCLNLP_SageMist_Poster.pptx --outdir /tmp/ 2>&1 | tail -3`
Expected: prints `convert ... -> /tmp/KCLNLP_SageMist_Poster.pdf using filter ...`

- [ ] **Step 4: Commit**

```bash
git add templates/sage_mist/poster.py templates/sage_mist/KCLNLP_SageMist_Poster.pptx
git commit -m "$(cat <<'EOF'
add Sage Mist A0 poster

A0 portrait with full-bleed Side Rail, two-column body, logos in the
header (not footer — A0 footer is too far from the eye-line).

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: Dusty Rose theme.py

**Files:**
- Create: `templates/dusty_rose/theme.py`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p templates/dusty_rose
```

- [ ] **Step 2: Write `templates/dusty_rose/theme.py`**

Same geometry/typography as Sage Mist, only the palette block changes.

```python
"""Design tokens for the Dusty Rose template.

A dusty-rose Morandi palette for academic talks. Shares the Side Rail
skeleton with Sage Mist; only the palette differs.
"""
from pathlib import Path

from pptx.util import Inches, Pt

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logos"

LOGOS = [
    LOGO_DIR / "KCL.png",
    LOGO_DIR / "KCLNLP.png",
    LOGO_DIR / "Alan.png",
]

# 16:9 slide
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Side Rail geometry
RAIL_W = Inches(0.18)
EDGE_PAD_L = Inches(0.55)
EDGE_PAD_R = Inches(0.45)
TITLE_TOP = Inches(0.5)
TITLE_RULE_W = Inches(0.6)
TITLE_RULE_H = Inches(0.04)
BODY_TOP = Inches(1.35)
FOOTER_H = Inches(0.5)
LOGO_H = Inches(0.45)
LOGO_GAP = Inches(0.18)

# Palette — Dusty Rose
RAIL   = (0x8A, 0x5E, 0x5A)
ACCENT = (0xC9, 0xA9, 0xA1)
TINT   = (0xF2, 0xEB, 0xE6)
INK    = (0x2E, 0x26, 0x25)
MUTED  = (0x73, 0x6A, 0x68)
WHITE  = (0xFF, 0xFF, 0xFF)

# Typography
FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"
FONT_SERIF = "Georgia"

SZ_TITLE_HERO  = Pt(44)
SZ_SUBTITLE    = Pt(22)
SZ_SECTION     = Pt(36)
SZ_SLIDE_TITLE = Pt(26)
SZ_BODY        = Pt(20)
SZ_BULLET_NUM  = Pt(28)
SZ_PULLQUOTE   = Pt(36)
SZ_CAPTION     = Pt(14)
SZ_LABEL       = Pt(11)
```

- [ ] **Step 3: Verify it imports**

Run: `python -c "import sys; sys.path.insert(0, 'templates/dusty_rose'); import theme; print(theme.RAIL, theme.TINT)"`
Expected: `(138, 94, 90) (242, 235, 230)`

- [ ] **Step 4: Commit**

```bash
git add templates/dusty_rose/theme.py
git commit -m "$(cat <<'EOF'
add Dusty Rose theme (dusty-rose Morandi palette)

Same geometry/typography as Sage Mist; only the palette differs.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: Dusty Rose build.py — copy Sage Mist's build.py

The two templates share the same Side Rail skeleton, so `build.py` is byte-for-byte identical except for the output filename string.

**Files:**
- Create: `templates/dusty_rose/build.py`

- [ ] **Step 1: Copy the Sage Mist build.py**

```bash
cp templates/sage_mist/build.py templates/dusty_rose/build.py
```

- [ ] **Step 2: Update the OUTPUT path and the docstring**

In `templates/dusty_rose/build.py`, change the docstring (top of file) and the `OUTPUT` line:

Replace the docstring:
```python
"""Build the Sage Mist demo deck.

Run: python templates/sage_mist/build.py

A sage-green Morandi deck with the new Side Rail skeleton — a vertical
brand-color rail on the left, slide title in the body, logos in the footer.
"""
```
with:
```python
"""Build the Dusty Rose demo deck.

Run: python templates/dusty_rose/build.py

A dusty-rose Morandi deck with the Side Rail skeleton — a vertical
brand-color rail on the left, slide title in the body, logos in the footer.
"""
```

Replace:
```python
OUTPUT = Path(__file__).resolve().parent / "KCLNLP_SageMist.pptx"
```
with:
```python
OUTPUT = Path(__file__).resolve().parent / "KCLNLP_DustyRose.pptx"
```

The `import theme as T` line is unchanged — Python's path manipulation ensures it picks up `templates/dusty_rose/theme.py` because of the `sys.path.insert(0, ...)` line.

- [ ] **Step 3: Generate the Dusty Rose deck and verify**

Run: `python templates/dusty_rose/build.py && python -c "from pptx import Presentation; p = Presentation('templates/dusty_rose/KCLNLP_DustyRose.pptx'); print(f'{len(p.slides)} slides')"`
Expected: prints `wrote ...` then `9 slides`.

- [ ] **Step 4: Headless render to verify it opens cleanly**

Run: `libreoffice --headless --convert-to pdf templates/dusty_rose/KCLNLP_DustyRose.pptx --outdir /tmp/ 2>&1 | tail -3`
Expected: prints `convert ... -> /tmp/KCLNLP_DustyRose.pdf using filter ...`

- [ ] **Step 5: Commit**

```bash
git add templates/dusty_rose/build.py templates/dusty_rose/KCLNLP_DustyRose.pptx
git commit -m "$(cat <<'EOF'
add Dusty Rose deck (same skeleton as Sage Mist)

build.py is byte-identical to Sage Mist except for the output
filename and docstring. The palette switch comes entirely from the
sibling theme.py.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: Dusty Rose poster.py

**Files:**
- Create: `templates/dusty_rose/poster.py`

- [ ] **Step 1: Copy the Sage Mist poster.py**

```bash
cp templates/sage_mist/poster.py templates/dusty_rose/poster.py
```

- [ ] **Step 2: Update the docstring and OUTPUT path**

Replace the docstring:
```python
"""Build the Sage Mist A0 poster.

Run: python templates/sage_mist/poster.py

A0 portrait (841 x 1189 mm) single-page poster. Side Rail extends full
bleed down the left edge; logos are in the header (not the footer —
on A0 the footer is too far from the eye-line). Body laid out in two
columns. Matches the deck's Sage Mist palette and visual language.
"""
```
with:
```python
"""Build the Dusty Rose A0 poster.

Run: python templates/dusty_rose/poster.py

A0 portrait (841 x 1189 mm) single-page poster. Side Rail extends full
bleed down the left edge; logos are in the header (not the footer —
on A0 the footer is too far from the eye-line). Body laid out in two
columns. Matches the deck's Dusty Rose palette and visual language.
"""
```

Replace:
```python
OUTPUT = Path(__file__).resolve().parent / "KCLNLP_SageMist_Poster.pptx"
```
with:
```python
OUTPUT = Path(__file__).resolve().parent / "KCLNLP_DustyRose_Poster.pptx"
```

- [ ] **Step 3: Generate the Dusty Rose poster**

Run: `python templates/dusty_rose/poster.py && python -c "from pptx import Presentation; p = Presentation('templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx'); print(f'{len(p.slides)} slide, {p.slide_width/914400:.2f}x{p.slide_height/914400:.2f} in')"`
Expected: prints `wrote ...` then `1 slide, 33.11x46.81 in`.

- [ ] **Step 4: Headless render to verify**

Run: `libreoffice --headless --convert-to pdf templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx --outdir /tmp/ 2>&1 | tail -3`
Expected: prints `convert ... -> /tmp/KCLNLP_DustyRose_Poster.pdf using filter ...`

- [ ] **Step 5: Commit**

```bash
git add templates/dusty_rose/poster.py templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx
git commit -m "$(cat <<'EOF'
add Dusty Rose A0 poster

poster.py is byte-identical to Sage Mist except for the output
filename and docstring.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: Preview rendering script

**Files:**
- Create: `scripts/render_previews.sh`

A reusable shell script that converts all four `.pptx` files into the 6 preview PNGs we need for the README. Keeping the script in the repo means future maintainers can regenerate previews after any palette tweak.

- [ ] **Step 1: Create scripts directory and write the script**

```bash
mkdir -p scripts
```

Write `scripts/render_previews.sh`:

```bash
#!/usr/bin/env bash
# Render preview PNGs for the Sage Mist and Dusty Rose templates.
#
# Strategy: convert .pptx -> PDF with LibreOffice, then PDF page -> PNG with
# pdftoppm. PNGs are written to assets/images/ with the naming convention
# used by README.md.
#
# Decks: page 1 = title slide -> *_title.png
#        page 4 = content slide -> *_content.png
# Poster: page 1 -> *_poster.png

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT_DIR="$REPO_ROOT/assets/images"
mkdir -p "$OUT_DIR"

render() {
  local pptx_path="$1"
  local prefix="$2"
  local title_page="$3"
  local content_page="$4"
  local out_kind="$5"   # "deck" or "poster"

  local stem
  stem="$(basename "$pptx_path" .pptx)"

  libreoffice --headless --convert-to pdf "$pptx_path" \
    --outdir "$TMP_DIR" >/dev/null

  if [[ "$out_kind" == "deck" ]]; then
    pdftoppm -png -r 150 -f "$title_page" -l "$title_page" \
      "$TMP_DIR/$stem.pdf" "$TMP_DIR/${prefix}_title_tmp"
    pdftoppm -png -r 150 -f "$content_page" -l "$content_page" \
      "$TMP_DIR/$stem.pdf" "$TMP_DIR/${prefix}_content_tmp"
    # pdftoppm appends "-N" suffixes; find them and rename.
    mv "$TMP_DIR/${prefix}_title_tmp"-*.png "$OUT_DIR/${prefix}_title.png"
    mv "$TMP_DIR/${prefix}_content_tmp"-*.png "$OUT_DIR/${prefix}_content.png"
  else
    pdftoppm -png -r 100 -f 1 -l 1 \
      "$TMP_DIR/$stem.pdf" "$TMP_DIR/${prefix}_poster_tmp"
    mv "$TMP_DIR/${prefix}_poster_tmp"-*.png "$OUT_DIR/${prefix}_poster.png"
  fi

  echo "rendered $prefix from $stem"
}

# Decks: page 1 = title (left), page 4 = content (standard bullets)
render "$REPO_ROOT/templates/sage_mist/KCLNLP_SageMist.pptx"    sage_mist  1 4 deck
render "$REPO_ROOT/templates/dusty_rose/KCLNLP_DustyRose.pptx"  dusty_rose 1 4 deck

# Posters: single page
render "$REPO_ROOT/templates/sage_mist/KCLNLP_SageMist_Poster.pptx"    sage_mist  0 0 poster
render "$REPO_ROOT/templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx"  dusty_rose 0 0 poster

echo "all previews written to $OUT_DIR"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x scripts/render_previews.sh
```

- [ ] **Step 3: Run it**

Run: `scripts/render_previews.sh`
Expected: prints 4 `rendered ...` lines and `all previews written to .../assets/images`.

- [ ] **Step 4: Verify all 6 PNGs exist with reasonable size**

Run: `ls -la assets/images/sage_mist_*.png assets/images/dusty_rose_*.png`
Expected: 6 files listed, each ≥ 20 KB.

- [ ] **Step 5: Spot-check one PNG can be opened**

Run: `python -c "from PIL import Image; im = Image.open('assets/images/sage_mist_title.png'); print(im.size, im.mode)"`
Expected: a tuple like `(1920, 1080) RGB` (size depends on render resolution).

- [ ] **Step 6: Commit**

```bash
git add scripts/render_previews.sh assets/images/sage_mist_title.png \
        assets/images/sage_mist_content.png assets/images/sage_mist_poster.png \
        assets/images/dusty_rose_title.png assets/images/dusty_rose_content.png \
        assets/images/dusty_rose_poster.png
git commit -m "$(cat <<'EOF'
add preview rendering script and 6 PNG previews

scripts/render_previews.sh uses LibreOffice + pdftoppm to regenerate
all template previews. Run it after any palette tweak.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: README — add Sage Mist + Dusty Rose sections

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the introductory paragraph**

In `README.md`, find this line at the top of the file:

```markdown
# KCLNLP_SlidesTemplate

PowerPoint templates for the **KCL NLP** research group, designed for consistent outreach and presentation of our research work (talks, posters, seminars, reading groups, etc.).

## Slides Templates
```

Replace with:

```markdown
# KCLNLP_SlidesTemplate

PowerPoint templates for the **KCL NLP** research group, designed for consistent outreach and presentation of our research work (talks, posters, seminars, reading groups, etc.). Four 16:9 decks and four matching A0 posters are included, covering classic accent colours (Royal Blue, Tree Yellow) and Morandi-style palettes for a more understated look (Sage Mist, Dusty Rose).

## Slides Templates
```

- [ ] **Step 2: Add Sage Mist section under Slides Templates**

Find this line in `README.md`:

```markdown
### Royal Blue
```

Just **before** that line, insert:

````markdown
### Sage Mist

A sage-green Morandi 16:9 deck with the new **Side Rail** skeleton — a thin vertical brand-color bar on the left, slide title in the body area with a short underline rule, and the KCL / KCLNLP / Alan Turing logos collected in a single-line footer. The body has the full slide height to breathe. Typography: Calibri throughout, with Georgia for the pull-quote slide.

| Title page | Content page |
| --- | --- |
| ![Sage Mist title page](assets/images/sage_mist_title.png) | ![Sage Mist content page](assets/images/sage_mist_content.png) |

- Download: [`templates/sage_mist/KCLNLP_SageMist.pptx`](templates/sage_mist/KCLNLP_SageMist.pptx)
- Layouts included: title (left + centered), section divider, content (bullets), content + callout overlay, numbered list (01 / 02 / 03), two-column (figure + text), pull-quote, thanks / Q&A.
- Main colors:
  - `#5C7261` — brand sage; rail, title rules, section number, callout border
  - `#A7B5A0` — lighter sage; decorative lines, pull-quote glyphs
  - `#EDEAE0` — cream tint for callout fills
  - `#2B2F2A` — slide titles and primary body text (warm near-black)
  - `#6F756C` — secondary / italic text (captions, footer)

### Dusty Rose

A dusty-rose Morandi 16:9 deck sharing the **Side Rail** skeleton with Sage Mist — same layout grammar, warmer earth-tone palette. Good for humanities-leaning talks or any setting where the cool Royal Blue and Tree Yellow feel too formal. Typography: Calibri throughout, with Georgia for the pull-quote slide.

| Title page | Content page |
| --- | --- |
| ![Dusty Rose title page](assets/images/dusty_rose_title.png) | ![Dusty Rose content page](assets/images/dusty_rose_content.png) |

- Download: [`templates/dusty_rose/KCLNLP_DustyRose.pptx`](templates/dusty_rose/KCLNLP_DustyRose.pptx)
- Layouts included: title (left + centered), section divider, content (bullets), content + callout overlay, numbered list (01 / 02 / 03), two-column (figure + text), pull-quote, thanks / Q&A.
- Main colors:
  - `#8A5E5A` — brand rose; rail, title rules, section number, callout border
  - `#C9A9A1` — lighter rose; decorative lines, pull-quote glyphs
  - `#F2EBE6` — warm beige tint for callout fills
  - `#2E2625` — slide titles and primary body text (warm near-black brown)
  - `#736A68` — secondary / italic text (captions, footer)

````

- [ ] **Step 3: Add Sage Mist and Dusty Rose posters under Posters Templates**

Find this line in `README.md`:

```markdown
### Tree Yellow poster
```

Just **before** that line, insert:

````markdown
### Sage Mist poster

<p align="center">
  <img src="assets/images/sage_mist_poster.png" alt="Sage Mist A0 poster" width="360">
</p>

- Download: [`templates/sage_mist/KCLNLP_SageMist_Poster.pptx`](templates/sage_mist/KCLNLP_SageMist_Poster.pptx)

### Dusty Rose poster

<p align="center">
  <img src="assets/images/dusty_rose_poster.png" alt="Dusty Rose A0 poster" width="360">
</p>

- Download: [`templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx`](templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx)

````

- [ ] **Step 4: Verify the file structure**

Run: `grep -n "^### " README.md`
Expected: 8 section headings in this order:
```
### Sage Mist
### Dusty Rose
### Royal Blue
### Tree Yellow
### Sage Mist poster
### Dusty Rose poster
### Tree Yellow poster
### Royal Blue poster
```

(Sage Mist and Dusty Rose lead because they're the latest additions — readers see new content first; the older templates are still right below.)

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "$(cat <<'EOF'
document Sage Mist and Dusty Rose templates in README

Add sections under Slides Templates and Posters Templates with
preview tables, download links, layout lists, and hex colour
references — matching the structure of the existing Royal Blue and
Tree Yellow entries.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Task 16: Final verification and push

**Files:** none modified — just final checks and push.

- [ ] **Step 1: Re-generate all four .pptx files from scratch to confirm reproducibility**

Run:
```bash
python templates/sage_mist/build.py && \
python templates/sage_mist/poster.py && \
python templates/dusty_rose/build.py && \
python templates/dusty_rose/poster.py
```
Expected: 4 `wrote ...` lines, no errors.

- [ ] **Step 2: Verify file structure matches the spec**

Run: `ls templates/sage_mist/ templates/dusty_rose/`
Expected, in each folder:
- `theme.py`
- `build.py`
- `poster.py`
- `KCLNLP_<Theme>.pptx`
- `KCLNLP_<Theme>_Poster.pptx`

- [ ] **Step 3: Verify all 6 preview PNGs exist**

Run: `ls assets/images/*.png | wc -l`
Expected: `10` (4 existing + 6 new).

- [ ] **Step 4: Verify slide counts**

Run:
```bash
python -c "from pptx import Presentation; \
print('sage_mist deck:', len(Presentation('templates/sage_mist/KCLNLP_SageMist.pptx').slides)); \
print('sage_mist poster:', len(Presentation('templates/sage_mist/KCLNLP_SageMist_Poster.pptx').slides)); \
print('dusty_rose deck:', len(Presentation('templates/dusty_rose/KCLNLP_DustyRose.pptx').slides)); \
print('dusty_rose poster:', len(Presentation('templates/dusty_rose/KCLNLP_DustyRose_Poster.pptx').slides))"
```
Expected:
```
sage_mist deck: 9
sage_mist poster: 1
dusty_rose deck: 9
dusty_rose poster: 1
```

- [ ] **Step 5: Verify the existing templates are untouched**

Run: `git log --oneline templates/royal_blue/ templates/tree_yellow/ | head -5 | diff - <(git log --oneline templates/royal_blue/ templates/tree_yellow/ origin/main..HEAD 2>/dev/null)`

Better check: confirm no changes since this branch started in those folders:

Run: `git diff origin/main --stat -- templates/royal_blue/ templates/tree_yellow/`
Expected: empty output (no changes to those folders).

- [ ] **Step 6: Push to remote (current branch only — no PR)**

Per CLAUDE.md, commit + push is fine; per `feedback_pr_approval.md`, do **not** open a PR.

Run: `git push`
Expected: `To <remote-url>` followed by the pushed commits.

- [ ] **Step 7: Final summary**

Print a summary to the conversation:
- Files added: 4 templates × 3 source files + 4 .pptx + 6 PNGs + 1 spec + 1 plan + 1 render script
- Commits added: ~14
- Existing templates: untouched ✓
- README: updated ✓
- PR: **not opened** (per user preference)
