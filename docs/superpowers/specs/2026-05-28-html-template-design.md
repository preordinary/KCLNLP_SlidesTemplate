# KCLNLP HTML Slide Template — Editorial Serif

**Date:** 2026-05-28
**Status:** Design approved, ready for implementation planning
**Scope:** A zero-dependency HTML deck template that mirrors the Editorial Serif visual language, distributed as a single `.html` file editable by hand.

---

## 1. Product Scope

### What we are building

A single-file HTML presentation template for KCL NLP research talks. The file opens in any modern browser, scales to any 16:9 display, and is edited as plain HTML (no build, no Markdown driver, no framework).

### MVP scope (this deliverable)

- **Deck only** — 16:9 talk slides. Poster, landing page, and tutorial article formats are explicitly out of scope.
- **One theme** — Editorial Serif (warm paper + brick red). No theme switcher.
- **Zero dependencies** — All CSS and JS inline. Runs offline. Runs from a USB stick. Runs from an email attachment.
- **Hand-edited HTML** — User edits the `.html` file directly. No content sources outside the file.

### Explicitly out of scope (YAGNI)

- A0 poster format — the existing pptx `poster.py` covers this.
- Landing page / academic article layouts — revisit only after deck adoption is proven.
- Multiple themes (deep-plum / sage-mist / etc.) — design tokens are themable, but only Editorial Serif ships.
- Markdown / YAML content drivers — contradicts "hand-edit HTML."
- Live-reload dev server, npm dependencies, any build step.
- Slide transition animations, autoplay, remote control, presenter mode (independent window), annotation pen, laser pointer.

### Deliverable layout

```
html-templates/editorial-serif/
  template.html         # Blank starter deck; opening comment explains usage
  example-talk.html     # Full example deck with realistic content (EMNLP fictional)
  README.md             # Quickstart, keyboard map, layout reference
  assets/logos/
    KCL.png
    KCLNLP.png
    Alan.png
```

`assets/logos/` is a **copy** of the existing pptx logos (not a symlink), so the `editorial-serif/` directory is self-contained and can be zipped or copied as a unit.

---

## 2. Design System

### Color tokens

```css
:root {
  /* paper & ink */
  --paper:    #f5efe6;   /* warm paper background */
  --ink:      #1a1a1a;   /* primary text */
  --muted:    #4a4a4a;   /* secondary text, italic captions */
  --hairline: #1a1a1a;   /* top/bottom rails */
  --faint:    #999999;   /* footer page numbers, figure captions */

  /* accent */
  --accent:   #8b3a2f;   /* brick red — the only accent */
  --accent-2: #c9b27c;   /* reserved gold (optional pull-quote / stat) */
}
```

### Font stacks

System-first fallbacks; templates must render correctly without any installed fonts.

```css
:root {
  --font-serif:
    'Source Serif Pro', 'Source Serif 4',
    Georgia, 'Times New Roman', serif;

  --font-sans:
    'Inter', -apple-system, BlinkMacSystemFont,
    'Segoe UI', 'Helvetica Neue', sans-serif;

  --font-mono:
    'JetBrains Mono', 'SF Mono', Menlo,
    Consolas, monospace;
}
```

Usage rules:
- **Serif** — body, headings, pull-quotes, references.
- **Sans (small caps, wide tracking)** — kickers, slide head/foot metadata, stat labels, button-like UI affordances.
- **Mono** — `slide-code` only.

### Type scale (at native 1920×1080 stage size)

```css
:root {
  --size-hero:      80px;    /* slide-title H1 */
  --size-section:   180px;   /* slide-section big numeral, e.g. "02" */
  --size-section-h: 68px;    /* slide-section heading */
  --size-h2:        56px;    /* slide-content / slide-two / slide-end H2 */
  --size-quote:     56px;    /* slide-quote text */
  --size-body:      34px;    /* paragraph body, bullet items */
  --size-sub:       36px;    /* italic subtitles */
  --size-stat:      100px;   /* big number on slide-two */
  --size-meta:      22px;    /* kicker, head, foot, stat-label */
  --size-tiny:      18px;    /* page number, figure caption */
}
```

Body 34px sits one notch below the pptx ≥30pt rule. This is intentional: HTML fit-to-screen is pixel-accurate (no projector squish), so 34px reads cleanly at projection distance.

### Spacing

```css
:root {
  --pad-x:       120px;   /* left/right slide padding */
  --pad-top:      90px;
  --pad-bottom:   70px;
  --rule-w:      100px;   /* brick-red rule width under H2 */
  --rule-h:        5px;
}
```

### Grid

- Fixed 1920×1080 stage.
- 120 px horizontal padding → 1680 px usable width.
- Top and bottom hairlines (0.5px, `--hairline`) inset to match `--pad-x`.

---

## 3. Layouts

Eight layouts. Each is a `<section class="slide slide-X">`. The class is the contract — users pick a layout by selecting the right class, never by writing CSS.

| # | Layout            | Class           | Purpose                              |
|---|-------------------|-----------------|--------------------------------------|
| 1 | Title             | `slide-title`   | Opening slide                        |
| 2 | Section divider   | `slide-section` | Chapter break                        |
| 3 | Content (bullets) | `slide-content` | Default information slide (~60% use) |
| 4 | Two-column        | `slide-two`     | Figure + text, or big-number + text  |
| 5 | Pull-quote        | `slide-quote`   | Headline result / quoted line        |
| 6 | Figure-full       | `slide-figure`  | Single dominant image with caption   |
| 7 | Code / table      | `slide-code`    | Mono code block or small table       |
| 8 | References / end  | `slide-end`     | Reference list, or thank-you + Q&A   |

### Modifiers

- `.slide-content.dense` — tighter line-height, smaller H2, for method-heavy pages.
- `.slide-title.cover-only` — hides the author meta, keynote-style.

### Shared chrome

Every slide carries the same head/foot:

```html
<section class="slide slide-content">
  <header class="slide-head">
    <span class="head-l">Method</span>          <!-- current part / chapter -->
    <span class="head-r">EMNLP 2026</span>      <!-- venue -->
  </header>

  <div class="slide-body">
    <!-- layout-specific content -->
  </div>

  <footer class="slide-foot">
    <span class="foot-l">KCL · NLP Group · Alan Turing</span>
    <span class="foot-r" data-auto-page></span>  <!-- auto-filled by JS -->
  </footer>
</section>
```

- `.slide-head` and `.slide-foot` render the top/bottom hairlines automatically.
- `data-auto-page` is opt-in: a span with the attribute gets filled with `currentIndex / total`. Users can hand-write the value instead (e.g. "intro / 32") and it will not be overwritten.

### Layouts that did NOT make the cut

- Agenda / TOC — `slide-content` is sufficient.
- Comparison (side-by-side) — fold into `slide-two` later if needed.
- Timeline — SVG-heavy; defer.
- Team grid — `slide-end` with author emails suffices.

---

## 4. Interaction & Keyboard Map

Implemented as a single `class SlidePresentation` (~150 lines) inlined in `<script>`. Auto-initializes on DOMContentLoaded.

### Navigation

| Action               | Keys / Gestures                                                                |
|----------------------|--------------------------------------------------------------------------------|
| Next                 | `→` / `↓` / `Space` / `PageDown` / right mouse / touch swipe left              |
| Previous             | `←` / `↑` / `Shift+Space` / `PageUp` / touch swipe right                       |
| First                | `Home`                                                                         |
| Last                 | `End`                                                                          |
| Jump to slide N      | Type digits, then `Enter` (corner shows input buffer)                          |
| Overview grid        | `Esc` / `O` — all slides shrink into a 4×N grid; click to jump                 |
| URL hash sync        | `#7` jumps to slide 7; hash updates as you advance                             |

### Power user

| Action               | Key            |
|----------------------|----------------|
| Black screen         | `B`            |
| White screen         | `W`            |
| Keyboard cheat sheet | `?` or `H`     |
| Fullscreen           | `F`            |
| Print / export PDF   | `Ctrl/Cmd+P`   |

### Presenter notes

Notes are embedded per slide:

```html
<aside class="notes">Remember: GSM8K is the only benchmark not matching 7B. Mention limitations.</aside>
```

- Hidden on the main screen (`display: none`).
- `?notes` URL parameter activates rehearsal mode: the current slide's notes render in a small box at the bottom-right of the screen.

### URL parameters (not in cheat sheet)

- `?print` — render print layout directly (for headless PDF generation).
- `?grid` — start in overview.
- `?notes` — rehearsal mode: notes for the current slide render in a small box at the bottom-right of the main screen.

### Explicitly NOT implemented

- Presenter mode (independent second window with timer + next-slide preview)
- Annotation pen / drawing tool
- Laser pointer
- Slide transition animations
- Autoplay / timed advance
- Phone-as-remote control
- Multi-language toggle

---

## 5. File Structure & Skeleton

### Repository layout

```
KCLNLP_SlidesTemplate/
└── html-templates/
    └── editorial-serif/
        ├── template.html
        ├── example-talk.html
        ├── README.md
        └── assets/
            └── logos/
                ├── KCL.png
                ├── KCLNLP.png
                └── Alan.png
```

### `template.html` skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Talk title</title>

  <!--
    KCLNLP Editorial Serif · HTML deck template
    ─────────────────────────────────────────
    HOW TO USE
    1. Change <title> above and the deck title in section 1.
    2. Add / remove / reorder <section class="slide ..."> blocks below.
    3. Open this file in any browser. No build step.

    LAYOUTS
      slide-title       slide-section     slide-content
      slide-two         slide-quote       slide-figure
      slide-code        slide-end

    KEYBOARD (press ? in the deck for the full list)
      → ←   Space   B / W   F   Esc (grid)   Ctrl+P
  -->

  <style>
    /* === DESIGN TOKENS === */
    :root { /* color, font, type-scale, spacing tokens — see §2 */ }

    /* === STAGE (1920×1080, JS-driven scale) === */
    html, body { margin: 0; background: #222; overflow: hidden; height: 100vh; }
    .stage {
      width: 1920px; height: 1080px;
      transform-origin: top left;
      position: absolute; top: 50%; left: 50%;
      /* JS sets --scale and translate offset to center the stage */
    }

    /* === SHARED SLIDE CHROME === */
    .slide { width: 1920px; height: 1080px; background: var(--paper); /* ... */ }
    .slide-head, .slide-foot { /* hairlines, padding, sans metadata */ }
    .accent-rule { width: var(--rule-w); height: var(--rule-h); background: var(--accent); }

    /* === PER-LAYOUT === */
    .slide-title h1     { font-size: var(--size-hero); /* ... */ }
    .slide-section .section-num { font-size: var(--size-section); /* ... */ }
    /* ... all 8 layouts ... */

    /* === MODES (toggled via body class) === */
    body.is-grid .stage { /* 4×N overview grid */ }
    body.is-black::after, body.is-white::after { /* full-bleed overlay */ }
    body.is-notes .slide.is-current .notes { /* rehearsal box bottom-right */ }

    /* === PRINT (PDF export) === */
    @page { size: 1920px 1080px; margin: 0; }
    @media print {
      html, body { background: #fff; overflow: visible; height: auto; }
      .stage { position: static; transform: none; }
      .slide { page-break-after: always; box-shadow: none; }
    }
  </style>
</head>

<body>
  <div class="stage">

    <section class="slide slide-title">
      <header class="slide-head">
        <span class="head-l">KCLNLP · Talk 01</span>
        <span class="head-r">EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <div class="kicker">No. 01 — Scaling</div>
        <h1>Smaller language models,<br>trained on the right data.</h1>
        <p class="sub">A look at where parameter efficiency stops paying its bills.</p>
        <div class="accent-rule"></div>
        <p class="meta">Jane Doe · King's College London · Dec 2026</p>
      </div>
      <footer class="slide-foot">
        <span class="foot-l">KCL · NLP Group · Alan Turing</span>
        <span class="foot-r" data-auto-page></span>
      </footer>
    </section>

    <!-- ... seven more layout examples ... -->

  </div>

  <script>
    /* SlidePresentation — ~150 LOC
       - Scans .slide elements on init
       - Binds keydown / touch / hashchange
       - Maintains currentIndex
       - Computes --scale on resize, applies to .stage
       - Fills [data-auto-page] spans
       - Toggles body.is-* classes for grid / black / white / notes
    */
    class SlidePresentation { /* ... */ }
    new SlidePresentation();
  </script>
</body>
</html>
```

### `example-talk.html`

Same skeleton, every layout populated with realistic (fictional EMNLP) content. ~700 lines. Serves as the live reference users copy from.

### `README.md`

~200 lines covering:
- Quickstart (copy → edit → open, three steps).
- Keyboard map.
- All 8 layouts with screenshots, class names, and "when to use."
- How to change the accent color (touch only `--accent` in `:root`).
- How to export PDF and where it might differ across browsers.

### Non-obvious design choices

1. **Stage in absolute pixels (1920×1080), scaled via `transform: scale()`.** JS computes `scale = min(window.w / 1920, window.h / 1080)` on resize, writes it to a `--scale` CSS variable. All design values stay in px; scaling is one knob.

2. **`data-auto-page` is opt-in.** The JS only fills spans that carry the attribute, so authors who want a custom footer (e.g. `intro / 32`) just omit the attribute.

3. **Single-responsibility CSS classes.** `slide-head` / `slide-foot` own the hairlines and chrome only; `slide-X` owns body layout only. Swapping a slide's layout never touches its head/foot.

4. **No build step.** CSS and JS are inline. Distributing the template is `cp template.html my-talk.html`.

---

## 6. Implementation Phasing

This section sketches what the writing-plans step will refine into a step-by-step plan.

### Phase 1 — Scaffolding
- Create `html-templates/editorial-serif/`.
- Copy three logos from `assets/logos/sage_mist/` into `html-templates/editorial-serif/assets/logos/`.
- Minimal `template.html`: DOCTYPE, one hello-world slide, JS class stub.

### Phase 2 — Design tokens & stage scaling
- Implement the full `:root` token set (color, font, type scale, spacing).
- Implement the 1920×1080 stage and `SlidePresentation._fit()` (resize observer → `--scale`).
- Manual verification: drag window, fullscreen, multiple monitors. Scale stays correct, no overflow, no letterbox bug.
- Implement `.slide-head` / `.slide-foot` shared chrome plus `data-auto-page`.

### Phase 3 — 8 layouts
- `slide-title` — title hero (scale mockup #4 to 1920×1080).
- `slide-section` — large numeral + heading + tagline.
- `slide-content` — H2 + brick-red rule + em-dash list.
- `slide-two` — two-column grid (figure / stat + text).
- `slide-quote` — large quote mark + italic body + attribution.
- `slide-figure` — full-bleed image (`object-fit: contain` so figures are never cropped) + caption below.
- `slide-code` — mono block, paper tinted one notch darker (`#ece5d7`), line numbers, accent-colored language tag in the corner.
- `slide-end` — references list, or thank-you + Q&A.

### Phase 4 — Interaction
- Keyboard / touch / right-mouse / hash navigation.
- Numeric jump (digits + Enter) with on-screen input buffer.
- `Esc`/`O` overview grid (`body.is-grid` + grid CSS).
- `B` / `W` / `F` / `?`/`H` cheat sheet overlay.
- `?notes` URL param → rehearsal box bottom-right.
- Print CSS (`@page` + `page-break-after`) for `Ctrl/Cmd+P`.

### Phase 5 — `example-talk.html`
- Copy the empty template, fill all 8 layouts with realistic EMNLP example content.
- Manual smoke test: walk every keyboard shortcut once; print to PDF; capture 8 screenshots for README.

### Phase 6 — Documentation
- `README.md`: quickstart, keyboard map, 8-layout reference, accent-color howto, PDF export howto.
- Update root `README.md` with a link to `html-templates/editorial-serif/`.
- Commit and push.

### Estimated effort

~4 focused days of single-developer work.

### Acceptance criteria (user-facing, not unit tests)

- `template.html` opens correctly in Chrome, Firefox, and Safari by double-click.
- Scales correctly to external 1080p and 4K displays.
- All 8 layouts in `example-talk.html` share a consistent visual rhythm.
- `Ctrl+P` produces a PDF with one slide per page, no clipping.
- Zipping the `editorial-serif/` directory and unzipping it elsewhere yields a working deck.

### Known risks

- Safari fullscreen uses `webkitRequestFullscreen` — fallback required.
- Source Serif / Inter not installed → fallback to Georgia / system sans is acceptable but visually weaker; README recommends installing the fonts but the template must run bare.
- Chrome and Firefox can render print CSS differently; both must be tested during Phase 4.
