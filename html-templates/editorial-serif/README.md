# KCLNLP HTML Slide Template — Editorial Serif

A single-file, zero-dependency HTML deck template for KCL NLP talks.
Open it in any modern browser, scale to any 16:9 display, edit as plain HTML.

| Title page | Content page |
| --- | --- |
| ![Editorial Serif title page](../../assets/images/editorial_serif_title.png) | ![Editorial Serif content page](../../assets/images/editorial_serif_content.png) |

## Quickstart

1. Copy `template.html` to a new file:
   ```bash
   cp template.html my-talk.html
   ```
2. Open `my-talk.html` in your editor. Change the `<title>` and the
   first `<section>`. Add, remove, or reorder further `<section>`
   blocks using the layouts listed below.
3. Double-click `my-talk.html` to open it in your browser. Done.
   No build step, no install, no server.

## Keyboard shortcuts

| Action               | Keys                                                         |
|----------------------|--------------------------------------------------------------|
| Next                 | `→` `↓` `Space` `PageDown` · right mouse · touch swipe left  |
| Previous             | `←` `↑` `Shift+Space` `PageUp` · touch swipe right            |
| First / Last         | `Home` / `End`                                               |
| Jump to slide N      | type digits then `Enter`                                     |
| Overview grid        | `O` / `Esc` (toggle)                                         |
| Black / white screen | `B` / `W`                                                    |
| Fullscreen           | `F`                                                          |
| Cheat sheet          | `?` or `H`                                                   |
| Print / export PDF   | `Ctrl/Cmd + P`                                               |

## Layouts

Pick a layout by setting the second class on a `<section>`. Eight options:

| Class            | Purpose                                          |
|------------------|--------------------------------------------------|
| `slide-title`    | Opening slide (kicker + hero title + meta)       |
| `slide-section`  | Chapter break (huge "02" numeral + heading)      |
| `slide-content`  | Default information slide with em-dash bullets   |
| `slide-two`      | Two columns: figure + text, or stat + text       |
| `slide-quote`    | Pull-quote (large italic, brick-red attribution) |
| `slide-figure`   | One dominant image with caption beneath          |
| `slide-code`     | Monospace code block with line numbers           |
| `slide-end`      | References list — or add `.thanks` for Q&A page  |

Modifiers:
- `.slide-content.dense` — tighter line-height, smaller H2 for info-heavy pages.
- `.slide-title.cover-only` — hide the author meta for a pure keynote opener.
- `.slide-end.thanks` — switch the end slide to "Thank you" + Q&A line.

See `example-talk.html` for one complete worked example of every layout.

## Presenter notes

Embed a note inside any slide:

```html
<section class="slide slide-content">
  ...
  <aside class="notes">Mention the GSM8K gap; have the limitations slide queued.</aside>
</section>
```

By default notes are hidden. For rehearsal, open the deck with `?notes`
appended to the URL — the current slide's note appears as a small box
bottom-right.

## Page numbers

Any `<span data-auto-page></span>` in the footer is auto-filled with
`current / total`. To use a custom value (e.g. `intro / 32`), drop the
attribute and write the text by hand — the script never overwrites
non-empty spans.

## Theming

All design values are CSS variables in `:root` at the top of the file's
`<style>` block. Change the accent color by touching one line:

```css
--accent: #8b3a2f;   /* brick red */
```

Other tokens worth knowing:
- `--paper` / `--ink` — background and body text colors.
- `--font-serif` / `--font-sans` / `--font-mono` — type stacks (system-fallback safe).
- `--size-hero` / `--size-h2` / `--size-body` — type scale.
- `--pad-x` / `--pad-top` / `--pad-bottom` — slide padding.

The template ships with no web fonts. Source Serif Pro and Inter will
be used if installed; otherwise it falls back to Georgia and the
system sans. The design works at both ends.

## Exporting to PDF

Press `Ctrl/Cmd + P`. In the print dialog set **Margins: None** and
**Background graphics: on**. The output has one slide per page at
1920×1080. Chrome and Firefox both work; Safari may render slightly
differently — Chrome is the recommended exporter.

## File anatomy

| File                | What it is                                                    |
|---------------------|---------------------------------------------------------------|
| `template.html`     | The blank starter. Copy this to begin a new talk.             |
| `example-talk.html` | A populated example with all 8 layouts and a notes example.   |
| `README.md`         | This file.                                                    |
| `assets/logos/`     | Original full-resolution KCL / KCLNLP / Alan Turing PNGs. The HTML files don't need them — institutional logos are inlined as base64 data URIs inside `<style>`, so `template.html` is genuinely a single file you can email or drop anywhere. The folder is kept for reference and for regenerating the inlined copies if you re-theme. |

The CSS and JS are duplicated between `template.html` and
`example-talk.html`. This is intentional — it preserves the
"single-file, drop-anywhere" property. When upstream tokens change,
apply the diff to both files.

## Browser support

Chrome, Firefox, Safari, Edge — all recent versions. The template uses
no experimental features; only `transform`, `aspect-ratio`, `flex`,
`grid`, `@page`, and standard event APIs.
