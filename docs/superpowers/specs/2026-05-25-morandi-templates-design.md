# Sage Mist & Dusty Rose — Two Morandi-palette Templates

**Date:** 2026-05-25
**Status:** Design approved, ready for implementation
**Scope:** Add two new academic-presentation templates to `KCLNLP_SlidesTemplate`, sharing a new "Side Rail" skeleton and using Morandi-style palettes.

---

## 1. Goals

Add **two new templates** to the KCL NLP slide template repo:

- **Sage Mist** — sage-green Morandi palette, warm/natural feel.
- **Dusty Rose** — dusty-rose Morandi palette, humanist/considered feel.

Both target **academic talks** (seminars, conference talks, thesis-defence-style decks). Both ship with a matching A0 portrait poster, to stay consistent with the existing Royal Blue / Tree Yellow product line.

The two new templates **share a single skeleton** ("Side Rail"); only the palette differs. The existing Royal Blue and Tree Yellow templates are **not modified**.

## 2. Non-Goals

- Not refactoring existing Royal Blue / Tree Yellow code.
- Not extracting shared helpers into a common module — each template stays a self-contained folder, matching the repo's existing convention.
- Not adding more than 9 demo slide layouts.
- Not redesigning the logo set, the asset folder, or `README.md`'s overall structure.
- Not adding dark mode, icon libraries, or interactive elements.

## 3. Visual Decisions (Approved)

### 3.1 Palettes

**Sage Mist** (`templates/sage_mist/theme.py`):

| Token | Hex | Role |
|---|---|---|
| `RAIL` | `#5C7261` | Brand rail, title rule, section number — the primary accent |
| `ACCENT` | `#A7B5A0` | Lighter sage, decorative lines, pull-quote glyphs |
| `TINT` | `#EDEAE0` | Cream fill for callout boxes |
| `INK` | `#2B2F2A` | Primary text (warm near-black) |
| `MUTED` | `#6F756C` | Captions, footer, secondary text (warm grey-green) |

**Dusty Rose** (`templates/dusty_rose/theme.py`):

| Token | Hex | Role |
|---|---|---|
| `RAIL` | `#8A5E5A` | Brand rail and primary accent |
| `ACCENT` | `#C9A9A1` | Dusty rose, decorative |
| `TINT` | `#F2EBE6` | Warm beige fill |
| `INK` | `#2E2625` | Primary text (warm near-black brown) |
| `MUTED` | `#736A68` | Captions, footer (warm grey) |

Both palettes intentionally tint `MUTED` toward the brand hue (rather than the neutral `#555555` used in existing templates) — this is the small detail that keeps the Morandi flavour from drifting toward generic grey.

### 3.2 Skeleton — "Side Rail"

A single new skeleton, shared by both palettes. Layout:

```
 ┌──┬────────────────────────────────────────────────┐
 │██│                                                 │  Rail: full-bleed
 │██│   Talk Title Goes Here                          │  vertical brand-color
 │██│   ──                                            │  bar, 0.18" wide.
 │██│                                                 │
 │██│   •  Bullet content                             │  Slide title sits in
 │██│   •  Bullet content                             │  the body area with a
 │██│   •  Bullet content                             │  short brand-color
 │██│                                                 │  underline rule.
 │██│   King's College London · KCL NLP   [3 logos]   │
 └──┴────────────────────────────────────────────────┘
```

Key differences from existing Royal Blue / Tree Yellow:

- **No header band.** Logos move from the header band down to a single-line footer; the body gets the full slide height to breathe.
- **Vertical rail replaces the horizontal rule** as the primary brand marker.
- **Slide title sits in the body**, not the header — there is no header.
- **Footer line** carries `<institution>` on the left and three logos on the right.

### 3.3 Geometry (16:9 slide, 13.333" × 7.5")

| Constant | Value | Purpose |
|---|---|---|
| `RAIL_W` | `Inches(0.18)` | Left rail width |
| `EDGE_PAD_L` | `Inches(0.55)` | Padding between rail and content |
| `EDGE_PAD_R` | `Inches(0.45)` | Right edge padding (matches existing) |
| `TITLE_TOP` | `Inches(0.5)` | Slide-title top |
| `TITLE_RULE_W` | `Inches(0.6)` | Short brand-color underline below title |
| `TITLE_RULE_H` | `Inches(0.04)` | ~2pt thickness |
| `BODY_TOP` | `Inches(1.35)` | Body content top |
| `FOOTER_H` | `Inches(0.5)` | Footer band height |
| `LOGO_H` | `Inches(0.45)` | Logo height in footer |
| `LOGO_GAP` | `Inches(0.18)` | Gap between logos |

### 3.4 Typography

```python
FONT_HEAD  = "Calibri"   # Headings
FONT_BODY  = "Calibri"   # Body
FONT_SERIF = "Georgia"   # Pull-quote slide only (deliberate contrast)

SZ_TITLE_HERO  = Pt(44)  # Title slide hero
SZ_SUBTITLE    = Pt(22)  # Title slide subtitle
SZ_SECTION     = Pt(36)  # Section divider title
SZ_SLIDE_TITLE = Pt(26)  # Content slide title
SZ_BODY        = Pt(20)  # Body text
SZ_BULLET_NUM  = Pt(28)  # Numbered list "01 / 02 / 03"
SZ_PULLQUOTE   = Pt(36)  # Pull-quote text
SZ_CAPTION     = Pt(14)  # Captions, footer
SZ_LABEL       = Pt(11)  # Uppercase labels (CALLOUT, TAKEAWAY)
```

Fonts fall back automatically: PowerPoint / LibreOffice substitute Calibri with Carlito or Arial when unavailable.

## 4. Demo Deck Contents

Each `.pptx` contains **9 demo slides** to cover the common academic-talk progression:

| # | Layout | Notes |
|---|---|---|
| 1 | Title (left-aligned) | Rail + 44pt title + 22pt subtitle + short rule + author line |
| 2 | Title (centered) | Centered variant — matches existing templates' centered title option |
| 3 | Section divider | Big number "01" + section name + one-line summary |
| 4 | Content with bullets | The workhorse — 5 bullets, footer with logos |
| 5 | Content + callout box | Same as #4 but overlays a TAKEAWAY block on the cream `TINT` — demonstrates how the callout is a reusable overlay, not a separate layout |
| 6 | Numbered list | "01 / 02 / 03" with horizontal divider lines, max 5 items |
| 7 | Two-column | Figure placeholder on the left + caption + bullets on the right |
| 8 | Pull-quote | Single-slide highlight — large Georgia italic quote + attribution line |
| 9 | Thanks (centered) | Q&A slide, centered variant |

### 4.1 Per-layout function names (in `build.py`)

```python
slide_title(prs)
slide_title_centered(prs)
slide_section(prs, number="01", title="…")
slide_content(prs, title="…", bullets=[…])
slide_content_with_callout(prs, title="…", bullets=[…], callout_label="TAKEAWAY", callout_text="…")
slide_numbered_list(prs, title="…", items=[…])
slide_two_column(prs, title="…")
slide_pullquote(prs, quote="…", attribution="…")
slide_thanks_centered(prs)
```

### 4.2 Callout box — reusable overlay

The callout is **not a separate layout**. It's a helper:

```python
add_callout(slide, *, left, top, width, label="TAKEAWAY", text="…")
```

It draws a `TINT`-filled rectangle with a 3pt `RAIL`-colored left border, an uppercase 11pt `RAIL`-colored label, and the body text below in `INK`. Users can drop it anywhere on any content slide.

## 5. A0 Poster

Each template ships one A0 portrait poster (`KCLNLP_<Theme>_Poster.pptx`), matching the deck's visual language and the existing two-column poster structure.

### 5.1 Structure (carried over from existing posters)

- A0 portrait: 33.11" × 46.81"
- 2-column body
- Header: title + authors + affiliations on the left, KCL / KCLNLP / Alan logos on the right
- Footer: contact line + institution line, with a QR-code placeholder bottom-right
- Sections: Introduction, Method (left column) | Results + figure, Conclusion, References, Acknowledgements (right column)

### 5.2 Skeleton adaptation

- The vertical rail extends **full bleed** down the left edge of the entire A0 sheet (width scaled from 0.18" to ~0.7" for visual weight at A0 size).
- **Logos remain in the header** (top-right) rather than moving to the footer. Rationale: on an A0 sheet, the footer is too far from the viewer's eye-line; logos belong near the title so the affiliations are read together with the work.
- This is the only intentional skeleton difference between deck and poster.

## 6. File Layout

```
templates/
├── royal_blue/             (unchanged)
├── tree_yellow/            (unchanged)
├── sage_mist/              ← NEW
│   ├── theme.py
│   ├── build.py
│   ├── poster.py
│   ├── KCLNLP_SageMist.pptx          (generated)
│   └── KCLNLP_SageMist_Poster.pptx   (generated)
└── dusty_rose/             ← NEW
    ├── theme.py
    ├── build.py
    ├── poster.py
    ├── KCLNLP_DustyRose.pptx
    └── KCLNLP_DustyRose_Poster.pptx

assets/
├── logos/                  (unchanged — reuse KCL.png / KCLNLP.png / Alan.png)
└── images/
    ├── sage_mist_title.png       ← NEW preview
    ├── sage_mist_content.png     ← NEW preview
    ├── sage_mist_poster.png      ← NEW preview
    ├── dusty_rose_title.png      ← NEW preview
    ├── dusty_rose_content.png    ← NEW preview
    └── dusty_rose_poster.png     ← NEW preview
```

Folder names use `snake_case` (matching existing `royal_blue` / `tree_yellow`). `.pptx` filenames use `PascalCase` (matching existing `KCLNLP_RoyalBlue.pptx`).

## 7. Implementation Plan

The work splits naturally into 7 steps. Each step ends in a checkpoint that can be verified before moving on.

1. **Skeleton + theme files for both palettes.** Create `templates/sage_mist/` and `templates/dusty_rose/`, each with a `theme.py` carrying the palette + shared geometry/typography constants. The two `theme.py` files differ only in colour values.

2. **`build.py` — Side Rail skeleton + 9 layouts.** Implement the 9 `slide_*` functions and the `add_rail()` / `add_footer_with_logos()` / `add_callout()` helpers. Both palettes' `build.py` files are byte-for-byte identical except for the module they import (`import theme as T`).

3. **`poster.py` — A0 poster.** Adapt `templates/royal_blue/poster.py` to the Side Rail skeleton (full-bleed rail, logos in header, two-column body). Both palettes' `poster.py` are again identical except for `theme`.

4. **Generate 4 `.pptx` files** by running the four scripts.

5. **Generate 6 preview PNGs.** Convert the `.pptx` files to PNG previews matching the naming convention in `assets/images/`. Preferred toolchain: `libreoffice --headless --convert-to pdf` followed by `pdftoppm`. If `libreoffice` is unavailable in the environment, fall back to rendering an approximation directly with `python-pptx` + `Pillow` (lower fidelity but unblocks the README).

6. **Update `README.md`.** Add a "Sage Mist" and "Dusty Rose" subsection under "Slides Templates"; add the matching posters under "Posters Templates". Each subsection follows the exact structure of the existing Royal Blue / Tree Yellow entries (preview table, download link, layouts-included note, hex colour list). Replace any wording that says "two templates" with "four templates".

7. **Commit and push** in logical batches:
   - One commit for the Sage Mist deck + theme.
   - One commit for the Sage Mist poster.
   - One commit for the Dusty Rose deck + theme.
   - One commit for the Dusty Rose poster.
   - One commit for the preview images.
   - One commit for the README update.

   No PR is opened — per user instruction (`feedback_pr_approval.md`), `gh pr create` requires explicit user request.

## 8. Verification Checklist

For each generated `.pptx`:

- File opens without error in LibreOffice Impress.
- File size is within the ~1 MB range of the existing templates.
- All 9 demo slides render with correct layout and the correct palette.
- Calibri falls back cleanly to Carlito / Arial when Calibri is unavailable.
- Logos appear in the expected positions (footer for decks, header for posters).

For each preview PNG:

- Resolution ≥ 1280 × 720 for deck previews, ≥ 1200 px wide for posters.
- Colour fidelity — the rail and tint match the spec hex values to the eye (not over-saturated, not washed out).

For the README:

- Each of the four templates has matching information depth (title + preview table + download + layouts + hex colours).
- Style descriptions distinguish the two new palettes clearly (green vs. rose, both Morandi).

## 9. Open Questions

None. All visual decisions were resolved during brainstorming:

- ✓ Palettes: Sage Mist + Dusty Rose
- ✓ Skeleton: Side Rail (shared, full-bleed rail, logos in footer for decks, header for posters)
- ✓ Extras: Pull-quote layout + Callout overlay + Numbered list layout — all three included
- ✓ Deliverables: deck + A0 poster per palette
- ✓ Existing templates unchanged

## 10. Out-of-Scope (YAGNI)

- Shared `_common.py` helper module across templates.
- Any modification to `royal_blue` or `tree_yellow`.
- Additional slide layouts beyond the 9 listed.
- Refactoring the existing poster code.
- Dark-mode variants.
- Icon library or graphic asset library.
- Changes to the logo layout rules.
