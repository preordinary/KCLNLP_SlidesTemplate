# Paper Yellow — Palette & Typography

Reference swatches and fonts for the `paper-yellow` template. Keep this in sync with `scripts/build_paper_yellow.py`.

## Colours

| Role | Hex | Where it's used |
|---|---|---|
| Paper yellow (primary) | `#F6BD60` | Title-slide background, section-divider left third, closing-slide background, left accent bar on content slides |
| Cream (surface) | `#F7EDE2` | Default background for content / TOC slides, "paper" cards on title & closing slides |
| Sage (secondary) | `#84A59D` | Thin title underlines, footer wordmark + slide number, small accent squares |
| Terracotta (emphasis) | `#F07167` | Section numbers, bullet markers, "Thank You", column heading on "ours" side of comparisons, title-slide accent square |
| Blush (soft accent) | `#FCD5CE` | Vertical separator between columns on two-column layout |
| Ink (body text) | `#2B2B2B` | Titles, body text |
| Muted (captions) | `#6B6B6B` | Speaker name, section lead-in, low-priority captions |
| White | `#FFFFFF` | — |

Palette origins: derived from the "Peach · Terracotta · Sand · Sage · Honey" family used in the reference deck (`20250911.pptx`), re-weighted so paper-yellow dominates (~60% visual weight on feature slides) with sage + terracotta as the two-accent system.

## Typography

| Slot | Latin | East Asian (Hans) |
|---|---|---|
| Major (titles, section numbers) | Aptos Display | 等线 Light |
| Minor (body, captions, footers) | Aptos | 等线 |

Declared in the theme under `<a:fontScheme>` with additional `<a:font script="Hant/Jpan/Hang">` entries (新細明體 / 游ゴシック / 맑은 고딕) so Traditional Chinese, Japanese, and Korean fall back sensibly.

> **Font availability.** Aptos ships with Microsoft 365 (2023+). 等线 ships with Windows. macOS users without 等线 will see PowerPoint's auto-substitute (typically 苹方 or Songti SC) — this is acceptable for v1.

## Size scale

| Element | Size (pt) |
|---|---|
| Title-slide main title | 40 – 54 |
| Section-number numeral | 140 – 150 |
| Closing "Thank You" | 72 |
| Slide title (content) | 32 |
| Section title | 44 – 48 |
| Body (single column) | 20 – 22 |
| Body (two-column) | 18 |
| TOC entry | 24 (number 28 bold) |
| Footer wordmark / slide number | 10 |
