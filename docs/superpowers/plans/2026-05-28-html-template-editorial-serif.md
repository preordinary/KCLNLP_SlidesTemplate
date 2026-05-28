# HTML Deck Template (Editorial Serif) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file, zero-dependency HTML talk deck template with 8 layouts in the Editorial Serif visual language, plus a populated example deck and README.

**Architecture:** Each deck is one self-contained HTML file. The body holds a `.stage` containing `<section class="slide slide-X">` elements. CSS variables in `:root` carry all design tokens (color, type, spacing). A ~150-line `SlidePresentation` JS class scales the 1920×1080 stage to viewport, handles keyboard / touch / hash navigation, and toggles mode classes on `<body>`. No build step; no framework; no external assets except logo PNGs.

**Tech Stack:** Plain HTML5 / CSS3 / ES2020 JavaScript. Tested in Chrome, Firefox, Safari. Logos as PNG.

**Spec:** `docs/superpowers/specs/2026-05-28-html-template-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `html-templates/editorial-serif/template.html` | Blank starter deck. Single source of truth for CSS + JS. ~600 lines. Users `cp` it to start a new talk. |
| `html-templates/editorial-serif/example-talk.html` | Same CSS/JS, body populated with realistic content across all 8 layouts. ~800 lines. Living reference. |
| `html-templates/editorial-serif/README.md` | Quickstart, keyboard map, 8-layout reference, theming howto, PDF export howto. |
| `html-templates/editorial-serif/assets/logos/{KCL,KCLNLP,Alan}.png` | Self-contained copy of the logos so `editorial-serif/` zips cleanly. |
| `README.md` (root, modify) | Add a section linking to the HTML template. |

**Decomposition rationale:** Because spec mandates "completely single-file" and "no build step", `template.html` is intentionally large. All CSS and JS live inline in that file. `example-talk.html` is a *copy* — duplicating the CSS/JS block is the deliberate cost of zero-dep distribution. To avoid drift, this plan generates `example-talk.html` by copying `template.html` and replacing only the slide body content.

**Testing approach:** This project has no automated test framework (it's an HTML template for humans). Verification is **manual browser smoke tests** at each step, with explicit pass/fail criteria. Steps describe exactly what to look for in the browser. Where logic is testable in isolation (the `SlidePresentation` JS class), we add small **inline assertion blocks** in the dev console — no test runner.

---

## Task 1: Create directory scaffold and copy logos

**Files:**
- Create dir: `html-templates/editorial-serif/`
- Create dir: `html-templates/editorial-serif/assets/logos/`
- Copy: `assets/logos/sage_mist/{KCL,KCLNLP,Alan}.png` → `html-templates/editorial-serif/assets/logos/`

- [ ] **Step 1: Create directories**

```bash
mkdir -p html-templates/editorial-serif/assets/logos
```

- [ ] **Step 2: Copy logos**

```bash
cp assets/logos/sage_mist/KCL.png    html-templates/editorial-serif/assets/logos/
cp assets/logos/sage_mist/KCLNLP.png html-templates/editorial-serif/assets/logos/
cp assets/logos/sage_mist/Alan.png   html-templates/editorial-serif/assets/logos/
```

- [ ] **Step 3: Verify the three files exist**

```bash
ls -la html-templates/editorial-serif/assets/logos/
```

Expected output includes `KCL.png`, `KCLNLP.png`, `Alan.png` — each non-zero size.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/assets/
git commit -m "scaffold editorial-serif HTML template directory with logos"
```

---

## Task 2: Create minimal `template.html` with one hello-world slide

**Files:**
- Create: `html-templates/editorial-serif/template.html`

This step establishes the file shell so subsequent steps modify rather than create. Tokens, layouts, and the real JS class come in later tasks; the JS here is a no-op stub.

- [ ] **Step 1: Write the file**

Create `html-templates/editorial-serif/template.html`:

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
    1. Change <title> above and the deck title in the first <section>.
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
    /* Tokens, chrome, layouts, modes, print CSS — added in later tasks */
    html, body { margin: 0; padding: 0; }
    .stage { width: 1920px; height: 1080px; background: #f5efe6; }
    .slide { width: 1920px; height: 1080px; padding: 80px; box-sizing: border-box; }
    h1 { font-family: Georgia, serif; font-size: 80px; }
  </style>
</head>

<body>
  <div class="stage">

    <section class="slide slide-title">
      <h1>Hello, editorial serif.</h1>
    </section>

  </div>

  <script>
    /* SlidePresentation — full implementation added in later tasks */
    class SlidePresentation {
      constructor() { /* stub */ }
    }
    new SlidePresentation();
  </script>
</body>
</html>
```

- [ ] **Step 2: Open in a browser to verify**

Open `html-templates/editorial-serif/template.html` in Chrome.

Expected: warm beige rectangle in the top-left, large serif "Hello, editorial serif." text. No console errors (open DevTools → Console tab).

- [ ] **Step 3: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add minimal template.html shell with one hello-world slide"
```

---

## Task 3: Add full design token set in `:root`

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (replace the `<style>` block)

- [ ] **Step 1: Replace the `<style>` block**

In `template.html`, find:

```html
  <style>
    /* Tokens, chrome, layouts, modes, print CSS — added in later tasks */
    html, body { margin: 0; padding: 0; }
    .stage { width: 1920px; height: 1080px; background: #f5efe6; }
    .slide { width: 1920px; height: 1080px; padding: 80px; box-sizing: border-box; }
    h1 { font-family: Georgia, serif; font-size: 80px; }
  </style>
```

Replace with:

```html
  <style>
    /* ============================================================
       DESIGN TOKENS  —  edit these to retheme.
       ============================================================ */
    :root {
      /* Color */
      --paper:    #f5efe6;
      --ink:      #1a1a1a;
      --muted:    #4a4a4a;
      --hairline: #1a1a1a;
      --faint:    #999999;
      --accent:   #8b3a2f;
      --accent-2: #c9b27c;

      /* Fonts */
      --font-serif:
        'Source Serif Pro', 'Source Serif 4',
        Georgia, 'Times New Roman', serif;
      --font-sans:
        'Inter', -apple-system, BlinkMacSystemFont,
        'Segoe UI', 'Helvetica Neue', sans-serif;
      --font-mono:
        'JetBrains Mono', 'SF Mono', Menlo,
        Consolas, monospace;

      /* Type scale (px @ native 1920×1080) */
      --size-hero:      80px;
      --size-section:   180px;
      --size-section-h: 68px;
      --size-h2:        56px;
      --size-quote:     56px;
      --size-body:      34px;
      --size-sub:       36px;
      --size-stat:      100px;
      --size-meta:      22px;
      --size-tiny:      18px;

      /* Spacing */
      --pad-x:       120px;
      --pad-top:      90px;
      --pad-bottom:   70px;
      --rule-w:      100px;
      --rule-h:        5px;

      /* Stage scale — overwritten by JS on resize */
      --scale: 1;
    }

    /* ============================================================
       STAGE  —  1920×1080 absolute canvas, JS-driven scale.
       ============================================================ */
    html, body {
      margin: 0; padding: 0;
      background: #222;
      height: 100vh; overflow: hidden;
      font-family: var(--font-serif);
      color: var(--ink);
    }
    .stage {
      width: 1920px; height: 1080px;
      transform-origin: top left;
      transform: scale(var(--scale));
      position: absolute; top: 0; left: 0;
    }

    /* ============================================================
       SLIDE  —  every layout starts here.
       ============================================================ */
    .slide {
      width: 1920px; height: 1080px;
      background: var(--paper);
      color: var(--ink);
      box-sizing: border-box;
      position: relative;
      display: none;   /* SlidePresentation toggles .is-current */
    }
    .slide.is-current { display: block; }
    h1, h2, p { margin: 0; }
  </style>
```

- [ ] **Step 2: Reload the browser**

Expected: page is **mostly black** with no visible slide content. (The new CSS hides slides until `.is-current` is set by JS, and the JS is still a stub. This is the correct state for this step.)

- [ ] **Step 3: Verify tokens in DevTools**

Open DevTools → Elements → click on `<html>` → Styles panel. Confirm `:root` shows `--paper: #f5efe6`, `--accent: #8b3a2f`, `--size-body: 34px`, etc.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add design tokens, stage canvas, base slide CSS"
```

---

## Task 4: Implement `SlidePresentation` core (scale + currentIndex + auto-page)

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (replace the `<script>` block and add a second hello slide for testing)

The class is built in slices — this task covers scaling, current-slide tracking, hash sync, and `[data-auto-page]` filling. Navigation comes in Task 5.

- [ ] **Step 1: Add a second slide so navigation has somewhere to go**

In `template.html`, find:

```html
    <section class="slide slide-title">
      <h1>Hello, editorial serif.</h1>
    </section>
```

Replace with:

```html
    <section class="slide slide-title">
      <h1>Hello, editorial serif.</h1>
      <p style="font-family: var(--font-sans); font-size: var(--size-meta); margin-top:40px;">
        Page <span data-auto-page></span>
      </p>
    </section>

    <section class="slide slide-content">
      <h1>Slide two.</h1>
      <p style="font-family: var(--font-sans); font-size: var(--size-meta); margin-top:40px;">
        Page <span data-auto-page></span>
      </p>
    </section>
```

- [ ] **Step 2: Replace the `<script>` block**

Find:

```html
  <script>
    /* SlidePresentation — full implementation added in later tasks */
    class SlidePresentation {
      constructor() { /* stub */ }
    }
    new SlidePresentation();
  </script>
```

Replace with:

```html
  <script>
    /* ============================================================
       SlidePresentation
       Core responsibilities (this task):
         - fit() : compute --scale on every resize
         - currentIndex tracking, .is-current class management
         - hashchange sync (#7 jumps to slide 7)
         - [data-auto-page] auto-fill with "n / total"
       Navigation, modes, and overlays come in later tasks.
       ============================================================ */
    class SlidePresentation {
      constructor() {
        this.stage  = document.querySelector('.stage');
        this.slides = Array.from(document.querySelectorAll('.slide'));
        this.total  = this.slides.length;
        this.currentIndex = this._readHash();

        this._fillAutoPage();
        this._fit();
        this._show(this.currentIndex);

        window.addEventListener('resize',     () => this._fit());
        window.addEventListener('hashchange', () => this._onHash());
      }

      /* ---- scaling ---- */
      _fit() {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const scale = Math.min(w / 1920, h / 1080);
        document.documentElement.style.setProperty('--scale', scale);
        // Center the scaled stage in the viewport.
        const offsetX = (w - 1920 * scale) / 2;
        const offsetY = (h - 1080 * scale) / 2;
        this.stage.style.left = offsetX + 'px';
        this.stage.style.top  = offsetY + 'px';
      }

      /* ---- current slide ---- */
      _show(i) {
        i = Math.max(0, Math.min(this.total - 1, i));
        this.slides.forEach((s, n) => s.classList.toggle('is-current', n === i));
        this.currentIndex = i;
        // Update hash without re-triggering hashchange.
        const want = '#' + (i + 1);
        if (location.hash !== want) {
          history.replaceState(null, '', want);
        }
      }

      /* ---- hash sync ---- */
      _readHash() {
        const m = (location.hash || '').match(/^#(\d+)$/);
        if (!m) return 0;
        return Math.max(0, Math.min(this.total - 1, parseInt(m[1], 10) - 1));
      }
      _onHash() {
        const i = this._readHash();
        if (i !== this.currentIndex) this._show(i);
      }

      /* ---- auto page numbers ---- */
      _fillAutoPage() {
        this.slides.forEach((slide, n) => {
          slide.querySelectorAll('[data-auto-page]').forEach(el => {
            // Only fill if empty so authors can hand-write a custom value.
            if (el.textContent.trim() === '') {
              el.textContent = (n + 1) + ' / ' + this.total;
            }
          });
        });
      }
    }

    new SlidePresentation();
  </script>
```

- [ ] **Step 3: Reload the browser**

Expected:
- Beige slide visible, centered, scaled to viewport.
- Text reads `Hello, editorial serif.` and `Page 1 / 2`.
- No console errors.

- [ ] **Step 4: Verify scaling**

Resize the browser window — both narrower and shorter. The beige stage must scale proportionally with no overflow, no scrollbars, no letterboxing bug.

- [ ] **Step 5: Verify hash jump**

In the address bar change the URL to end with `#2` and press Enter. Page should now show `Hello, editorial serif. Slide two. Page 2 / 2`. (Both slides briefly show because nav isn't built yet — actually only slide 2 should show because `.is-current` is exclusive.)

Wait — verify only slide 2 is visible after `#2`. If both are visible, check `.slide { display: none; }` rule from Task 3 is still present.

- [ ] **Step 6: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "implement SlidePresentation core: scaling, currentIndex, hash sync, auto-page"
```

---

## Task 5: Add keyboard, touch, and mouse navigation

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (extend the `SlidePresentation` class)

- [ ] **Step 1: Extend the class constructor and add navigation methods**

In `template.html`, find this block in the constructor:

```js
        window.addEventListener('resize',     () => this._fit());
        window.addEventListener('hashchange', () => this._onHash());
      }
```

Replace with:

```js
        window.addEventListener('resize',     () => this._fit());
        window.addEventListener('hashchange', () => this._onHash());
        window.addEventListener('keydown',    (e) => this._onKey(e));
        window.addEventListener('contextmenu',(e) => { e.preventDefault(); this.next(); });

        // Touch swipe
        this._touchStartX = null;
        window.addEventListener('touchstart', (e) => {
          if (e.touches.length === 1) this._touchStartX = e.touches[0].clientX;
        }, { passive: true });
        window.addEventListener('touchend', (e) => {
          if (this._touchStartX === null) return;
          const dx = e.changedTouches[0].clientX - this._touchStartX;
          if (Math.abs(dx) > 50) (dx < 0 ? this.next() : this.prev());
          this._touchStartX = null;
        }, { passive: true });

        // Numeric jump buffer
        this._numBuffer = '';
      }

      /* ---- public navigation ---- */
      next() { this._show(this.currentIndex + 1); }
      prev() { this._show(this.currentIndex - 1); }
      first() { this._show(0); }
      last() { this._show(this.total - 1); }
      goTo(n1) { this._show(n1 - 1); }  // 1-indexed for humans

      /* ---- keyboard ---- */
      _onKey(e) {
        if (e.metaKey || e.ctrlKey || e.altKey) return;   // leave shortcuts alone

        // Numeric buffer: digits accumulate, Enter commits, Esc clears.
        if (/^[0-9]$/.test(e.key)) {
          this._numBuffer += e.key;
          this._renderNumBuffer();
          return;
        }
        if (e.key === 'Enter' && this._numBuffer) {
          const n = parseInt(this._numBuffer, 10);
          this._numBuffer = '';
          this._renderNumBuffer();
          this.goTo(n);
          return;
        }
        if (e.key === 'Escape' && this._numBuffer) {
          this._numBuffer = '';
          this._renderNumBuffer();
          return;
        }

        switch (e.key) {
          case 'ArrowRight':
          case 'ArrowDown':
          case 'PageDown':
          case ' ':
            if (e.shiftKey) this.prev(); else this.next();
            e.preventDefault();
            break;
          case 'ArrowLeft':
          case 'ArrowUp':
          case 'PageUp':
            this.prev();
            e.preventDefault();
            break;
          case 'Home':
            this.first();
            e.preventDefault();
            break;
          case 'End':
            this.last();
            e.preventDefault();
            break;
        }
      }

      _renderNumBuffer() {
        let el = document.getElementById('num-buffer');
        if (!this._numBuffer) {
          if (el) el.remove();
          return;
        }
        if (!el) {
          el = document.createElement('div');
          el.id = 'num-buffer';
          el.style.cssText =
            'position:fixed;bottom:24px;right:24px;background:rgba(0,0,0,0.7);' +
            'color:#fff;font-family:monospace;font-size:20px;padding:8px 14px;' +
            'border-radius:4px;z-index:99999;';
          document.body.appendChild(el);
        }
        el.textContent = '→ ' + this._numBuffer;
      }
```

- [ ] **Step 2: Reload the browser**

Test each navigation method:
- Press `→` — should advance to slide 2.
- Press `←` — should go back to slide 1.
- Press `Space` — advance.
- Press `Shift+Space` — back.
- Press `Home` — slide 1; press `End` — slide 2.
- Press right mouse button on the deck — advances (and no context menu appears).
- Type `2` then `Enter` — jumps to slide 2; the "→ 2" badge appears bottom-right while typing.

- [ ] **Step 3: Verify hash updates**

Watch the address bar while pressing arrow keys. Hash should change between `#1` and `#2` in sync with the current slide.

- [ ] **Step 4: Touch verification (skip if no touchscreen)**

If you have a touchscreen / can use Chrome DevTools' Device Mode: swipe left advances, swipe right goes back.

- [ ] **Step 5: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add keyboard, touch, mouse, numeric-jump navigation"
```

---

## Task 6: Add B/W/F/grid/cheat-sheet modes + notes rehearsal

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (extend `<style>` and `<script>`)

- [ ] **Step 1: Add mode CSS**

In `template.html`, find the end of the `<style>` block (just before `</style>`). Add **before** `</style>`:

```css
    /* ============================================================
       MODES  —  body classes toggled by JS.
       ============================================================ */
    /* Overview grid: shrink the stage and re-flow slides as a grid. */
    body.is-grid {
      overflow: auto;
    }
    body.is-grid .stage {
      position: static;
      width: 100%; height: auto;
      transform: none;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
      padding: 32px;
      box-sizing: border-box;
      background: #222;
    }
    body.is-grid .slide {
      display: block !important;          /* override .is-current exclusivity */
      width: 100%; height: auto;
      aspect-ratio: 16 / 9;
      transform: scale(0.25); transform-origin: top left;
      /* Use a wrapper trick: scale the slide and reserve space for it */
      position: relative;
    }
    /* Wrap each slide in a grid cell that reserves the post-scale footprint. */
    body.is-grid .slide-wrap {
      width: 100%; aspect-ratio: 16 / 9;
      overflow: hidden;
      background: var(--paper);
      cursor: pointer;
      outline: 2px solid transparent;
      transition: outline-color 0.15s;
    }
    body.is-grid .slide-wrap:hover { outline-color: var(--accent); }
    body.is-grid .slide-wrap.is-current-thumb { outline-color: var(--accent); }
    body.is-grid .slide-wrap .slide {
      width: 1920px; height: 1080px;
      transform: scale(calc(100% / 1920 * var(--thumb-w, 320)));
      /* Fallback: use a known scale rather than a calc that JS sets per cell */
    }

    /* Black / white screens */
    body.is-black::after,
    body.is-white::after {
      content: ""; position: fixed; inset: 0; z-index: 10000;
    }
    body.is-black::after { background: #000; }
    body.is-white::after { background: #fff; }

    /* Cheat sheet overlay */
    .cheat-overlay {
      position: fixed; inset: 0; z-index: 10001;
      background: rgba(0, 0, 0, 0.85);
      color: #fff; font-family: var(--font-sans);
      display: flex; align-items: center; justify-content: center;
    }
    .cheat-overlay .cheat-box {
      max-width: 600px; padding: 40px 56px;
      background: #111; border: 1px solid #333;
      font-size: 16px; line-height: 1.7;
    }
    .cheat-overlay h3 {
      margin: 0 0 20px; font-family: var(--font-serif);
      font-size: 24px; font-weight: 400; letter-spacing: -0.5px;
    }
    .cheat-overlay table { border-collapse: collapse; width: 100%; }
    .cheat-overlay td { padding: 4px 0; vertical-align: top; }
    .cheat-overlay td:first-child {
      width: 220px; color: #c9b27c;
      font-family: monospace; font-size: 14px;
    }
    .cheat-overlay .cheat-dismiss {
      margin-top: 20px; font-size: 13px; color: #999;
    }

    /* Rehearsal notes box */
    .notes { display: none; }
    body.is-notes .slide.is-current .notes {
      display: block;
      position: fixed; bottom: 24px; right: 24px;
      max-width: 380px; padding: 18px 22px;
      background: rgba(255, 255, 255, 0.95);
      border-left: 3px solid var(--accent);
      font-family: var(--font-sans); font-size: 16px;
      line-height: 1.5; color: var(--ink);
      z-index: 9998;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
    }
```

> The overview grid CSS above takes a simpler approach than fully scaling each thumbnail: when `body.is-grid`, each slide is wrapped in a `.slide-wrap` cell, scaling is handled via `aspect-ratio` + CSS scaling. The JS in the next step adds those wrappers when entering grid mode and removes them on exit.

- [ ] **Step 2: Extend the constructor to handle new keys and modes**

In the `_onKey(e)` method, find the closing `}` of the `switch (e.key)` block, then immediately after the `case 'End':` block add the following new cases inside the same switch (right before the closing `}` of the switch):

Find:

```js
          case 'End':
            this.last();
            e.preventDefault();
            break;
        }
      }
```

Replace with:

```js
          case 'End':
            this.last();
            e.preventDefault();
            break;
          case 'b': case 'B':
            this._toggleBody('is-black');
            e.preventDefault();
            break;
          case 'w': case 'W':
            this._toggleBody('is-white');
            e.preventDefault();
            break;
          case 'f': case 'F':
            this._toggleFullscreen();
            e.preventDefault();
            break;
          case 'o': case 'O':
            this._toggleGrid();
            e.preventDefault();
            break;
          case 'Escape':
            if (document.body.classList.contains('is-grid')) {
              this._toggleGrid();
              e.preventDefault();
            } else if (document.body.classList.contains('is-black') ||
                       document.body.classList.contains('is-white')) {
              document.body.classList.remove('is-black', 'is-white');
              e.preventDefault();
            } else if (this._cheatOpen) {
              this._toggleCheat();
              e.preventDefault();
            }
            break;
          case '?': case 'h': case 'H':
            this._toggleCheat();
            e.preventDefault();
            break;
        }
      }

      /* ---- modes ---- */
      _toggleBody(cls) {
        // Mutually exclusive between black and white.
        if (cls === 'is-black') document.body.classList.remove('is-white');
        if (cls === 'is-white') document.body.classList.remove('is-black');
        document.body.classList.toggle(cls);
      }

      _toggleFullscreen() {
        const doc = document;
        const el  = doc.documentElement;
        const isFs = doc.fullscreenElement || doc.webkitFullscreenElement;
        if (isFs) {
          (doc.exitFullscreen || doc.webkitExitFullscreen).call(doc);
        } else {
          (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
        }
      }

      _toggleGrid() {
        const on = document.body.classList.toggle('is-grid');
        if (on) {
          // Wrap each slide in a .slide-wrap cell that handles click-to-jump.
          this.slides.forEach((slide, n) => {
            if (slide.parentElement.classList.contains('slide-wrap')) return;
            const wrap = document.createElement('div');
            wrap.className = 'slide-wrap';
            if (n === this.currentIndex) wrap.classList.add('is-current-thumb');
            slide.parentNode.insertBefore(wrap, slide);
            wrap.appendChild(slide);
            wrap.addEventListener('click', () => {
              this._toggleGrid();
              this._show(n);
            });
          });
          // In grid mode every slide must render, regardless of .is-current.
          this.slides.forEach(s => s.classList.add('is-current'));
        } else {
          // Unwrap and restore single-slide display.
          this.slides.forEach((slide) => {
            const wrap = slide.parentElement;
            if (wrap.classList.contains('slide-wrap')) {
              wrap.parentNode.insertBefore(slide, wrap);
              wrap.remove();
            }
          });
          // Restore exclusive .is-current.
          this._show(this.currentIndex);
        }
      }

      _toggleCheat() {
        let el = document.getElementById('cheat-overlay');
        if (el) {
          el.remove();
          this._cheatOpen = false;
        } else {
          el = document.createElement('div');
          el.id = 'cheat-overlay';
          el.className = 'cheat-overlay';
          el.innerHTML = `
            <div class="cheat-box">
              <h3>Keyboard shortcuts</h3>
              <table>
                <tr><td>→ ↓ Space PageDn</td><td>Next slide</td></tr>
                <tr><td>← ↑ Shift+Space PageUp</td><td>Previous slide</td></tr>
                <tr><td>Home / End</td><td>First / Last slide</td></tr>
                <tr><td>digits + Enter</td><td>Jump to slide N</td></tr>
                <tr><td>O / Esc</td><td>Toggle overview grid</td></tr>
                <tr><td>B</td><td>Black screen</td></tr>
                <tr><td>W</td><td>White screen</td></tr>
                <tr><td>F</td><td>Fullscreen</td></tr>
                <tr><td>Ctrl/Cmd + P</td><td>Print / export PDF</td></tr>
                <tr><td>? / H</td><td>This cheat sheet</td></tr>
              </table>
              <div class="cheat-dismiss">Press ? or Esc to dismiss.</div>
            </div>`;
          el.addEventListener('click', () => this._toggleCheat());
          document.body.appendChild(el);
          this._cheatOpen = true;
        }
      }
```

- [ ] **Step 3: Add notes mode + URL param activation**

In the constructor, find:

```js
        this._numBuffer = '';
      }
```

Replace with:

```js
        this._numBuffer = '';

        // URL param activation.
        const params = new URLSearchParams(location.search);
        if (params.has('notes')) document.body.classList.add('is-notes');
        if (params.has('grid'))  this._toggleGrid();
        // ?print is handled by CSS @media print + an immediate window.print() would
        // be hostile; leave the param as documentation only.
      }
```

- [ ] **Step 4: Reload and test each mode**

- Press `B` — entire screen turns black. Press `B` again or `Esc` — back to slide.
- Press `W` — white. `W` or `Esc` to dismiss.
- Press `F` — browser enters fullscreen. `F` or browser ESC to exit.
- Press `?` — keyboard cheat sheet overlay. `?`, `Esc`, or click to dismiss.
- Press `O` — overview grid with both slides as thumbnails. Click slide 2 — exits grid, shows slide 2.
- Add `<aside class="notes">Remember to mention X.</aside>` inside the first `<section>`, then reload with `?notes` in the URL. A note box appears bottom-right. Remove `?notes` for the next steps.

- [ ] **Step 5: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add B/W/F/grid/cheat-sheet modes and ?notes rehearsal box"
```

---

## Task 7: Add print CSS for PDF export

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (append to `<style>`)

- [ ] **Step 1: Add print CSS at the end of `<style>`**

Find the closing `</style>` tag and add **immediately before** it:

```css
    /* ============================================================
       PRINT  —  Ctrl/Cmd + P exports one slide per page.
       ============================================================ */
    @page { size: 1920px 1080px; margin: 0; }
    @media print {
      html, body {
        background: #fff !important;
        height: auto !important;
        overflow: visible !important;
      }
      .stage {
        position: static !important;
        transform: none !important;
        width: 1920px; height: auto;
        left: 0 !important; top: 0 !important;
        display: block !important;
      }
      .slide {
        display: block !important;
        width: 1920px; height: 1080px;
        page-break-after: always;
        page-break-inside: avoid;
        box-shadow: none !important;
      }
      .slide:last-child { page-break-after: auto; }
      /* Hide UI overlays in print. */
      #num-buffer, #cheat-overlay, .notes { display: none !important; }
    }
```

- [ ] **Step 2: Test print preview**

In Chrome press `Ctrl/Cmd + P`. The preview should show **2 pages**, each a full 16:9 slide with the beige background, no clipping, no overlapping UI. Margins set to "None" (the browser may default to Default; switch to None to see the design as intended). Cancel out of the dialog.

- [ ] **Step 3: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add print CSS so Ctrl/Cmd+P exports one slide per page"
```

---

## Task 8: Implement `slide-title` layout CSS + HTML

**Files:**
- Modify: `html-templates/editorial-serif/template.html` (add CSS, replace slide 1 markup)

From here through Task 15 each layout follows the same shape: add the layout's CSS in a clearly labeled block, then replace the matching placeholder slide with a real example so it's visible in the browser.

- [ ] **Step 1: Add `slide-title` CSS**

In `<style>`, find the section that ends with the `h1, h2, p { margin: 0; }` rule:

```css
    .slide { /* ... */ }
    .slide.is-current { display: block; }
    h1, h2, p { margin: 0; }
```

Add **immediately after** that block:

```css
    /* ============================================================
       SHARED CHROME  —  head + foot are identical across all layouts.
       ============================================================ */
    .slide-head, .slide-foot {
      position: absolute; left: var(--pad-x); right: var(--pad-x);
      display: flex; justify-content: space-between; align-items: center;
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: var(--faint);
    }
    .slide-head {
      top: var(--pad-top);
      padding-bottom: 24px;
      border-bottom: 0.5px solid var(--hairline);
      color: var(--accent);
    }
    .slide-foot {
      bottom: var(--pad-bottom);
      padding-top: 24px;
      border-top: 0.5px solid var(--hairline);
      font-size: var(--size-tiny);
    }
    .slide-body {
      position: absolute;
      left: var(--pad-x); right: var(--pad-x);
      top: calc(var(--pad-top) + 90px);
      bottom: calc(var(--pad-bottom) + 70px);
      display: flex; flex-direction: column;
    }

    /* Common element: brick-red rule + sans kicker. */
    .accent-rule {
      width: var(--rule-w); height: var(--rule-h);
      background: var(--accent);
      margin: 28px 0;
    }
    .kicker {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 40px;
    }

    /* ============================================================
       LAYOUT 1: slide-title
       ============================================================ */
    .slide-title .slide-body { justify-content: center; }
    .slide-title h1 {
      font-family: var(--font-serif);
      font-size: var(--size-hero);
      font-weight: 400;
      line-height: 1.06;
      letter-spacing: -1px;
      margin: 0 0 32px;
    }
    .slide-title .sub {
      font-family: var(--font-serif);
      font-style: italic;
      font-size: var(--size-sub);
      color: var(--muted);
      line-height: 1.4;
      max-width: 80%;
      margin: 0;
    }
    .slide-title .meta {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--muted);
      margin: 28px 0 0;
    }
    .slide-title.cover-only .meta { display: none; }
```

- [ ] **Step 2: Replace the placeholder slide 1 with a real title slide**

Find the existing `<section class="slide slide-title">...` block and replace it with:

```html
    <section class="slide slide-title">
      <header class="slide-head">
        <span>KCLNLP · Talk 01</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <div class="kicker">No. 01 — Scaling</div>
        <h1>Smaller language models,<br>trained on the right data.</h1>
        <p class="sub">A look at where parameter efficiency stops paying its bills, and where curated data starts.</p>
        <div class="accent-rule"></div>
        <p class="meta">Jane Doe · King's College London · Dec 2026</p>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and inspect**

Expected: beige slide with a thin black line near the top, brick-red "NO. 01 — SCALING" kicker in small sans uppercase, large serif title across two lines, italic subtitle below, brick-red rule, then meta line. Footer at bottom with another thin line, "KCL · NLP GROUP · ALAN TURING" left, "1 / 2" right.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-title layout with shared head/foot chrome"
```

---

## Task 9: Implement `slide-section` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-section` CSS**

In `<style>`, after the `slide-title .meta` rules, add:

```css
    /* ============================================================
       LAYOUT 2: slide-section
       ============================================================ */
    .slide-section .slide-body {
      flex-direction: row;
      align-items: center;
      gap: 80px;
    }
    .slide-section .section-num {
      font-family: var(--font-serif);
      font-size: var(--size-section);
      font-weight: 400;
      color: var(--accent);
      line-height: 1;
      letter-spacing: -6px;
    }
    .slide-section .section-rule {
      width: 1px; align-self: stretch;
      background: var(--accent); opacity: 0.5;
    }
    .slide-section .section-text h2 {
      font-family: var(--font-serif);
      font-size: var(--size-section-h);
      font-weight: 400;
      line-height: 1.1;
      letter-spacing: -1px;
      margin: 0 0 24px;
    }
    .slide-section .section-text p {
      font-family: var(--font-serif);
      font-style: italic;
      font-size: var(--size-sub);
      color: var(--muted);
      line-height: 1.4;
      margin: 0; max-width: 90%;
    }
```

- [ ] **Step 2: Replace slide 2 with a section divider**

Find the existing `<section class="slide slide-content">...` (currently the placeholder "Slide two.") and replace with:

```html
    <section class="slide slide-section">
      <header class="slide-head">
        <span>Part Two</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <div class="section-num">02</div>
        <div class="section-rule"></div>
        <div class="section-text">
          <h2>The data curation premium</h2>
          <p>What we mean by "right data" — three quantitative axes.</p>
        </div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and press `→`**

Expected: section divider page. A huge brick-red "02" on the left, a thin vertical rule, then heading "The data curation premium" with an italic tagline beneath.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-section layout"
```

---

## Task 10: Implement `slide-content` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-content` CSS**

```css
    /* ============================================================
       LAYOUT 3: slide-content
       ============================================================ */
    .slide-content h2 {
      font-family: var(--font-serif);
      font-size: var(--size-h2);
      font-weight: 500;
      letter-spacing: -0.5px;
      margin: 0;
    }
    .slide-content .accent-rule { margin: 20px 0 40px; }
    .slide-content ul {
      list-style: none;
      padding: 0; margin: 0;
      font-family: var(--font-serif);
      font-size: var(--size-body);
      line-height: 1.55;
      color: var(--ink);
    }
    .slide-content ul li {
      position: relative;
      padding-left: 36px;
      margin-bottom: 22px;
    }
    .slide-content ul li::before {
      content: "—";
      position: absolute; left: 0;
      color: var(--accent);
      font-weight: 600;
    }
    .slide-content.dense h2 { font-size: 44px; }
    .slide-content.dense ul { font-size: 28px; line-height: 1.5; }
    .slide-content.dense ul li { margin-bottom: 14px; }
```

- [ ] **Step 2: Add a new `slide-content` slide after the section slide**

Find the closing `</section>` of the `slide-section` block. Add **immediately after** it:

```html
    <section class="slide slide-content">
      <header class="slide-head">
        <span>Method</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <h2>Three properties of "right data"</h2>
        <div class="accent-rule"></div>
        <ul>
          <li>Coverage — every reasoning skill seen at least 50× during training.</li>
          <li>De-duplication at the document level, not just the n-gram level.</li>
          <li>A held-out test split drawn from a different time period entirely.</li>
          <li>Sampled at 1.3B params, then re-verified at 350M and 7B scale.</li>
        </ul>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and navigate to slide 3**

Expected: H2 "Three properties of ...", brick-red rule below it, then four bullets each prefixed with a brick-red em-dash. Footer reads `3 / 3`.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-content layout with em-dash bullets"
```

---

## Task 11: Implement `slide-two` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-two` CSS**

```css
    /* ============================================================
       LAYOUT 4: slide-two   (figure / stat + text)
       ============================================================ */
    .slide-two h2 {
      font-family: var(--font-serif);
      font-size: var(--size-h2);
      font-weight: 500;
      letter-spacing: -0.5px;
      margin: 0;
    }
    .slide-two .accent-rule { margin: 20px 0 32px; }
    .slide-two .two-cols {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 60px;
      flex: 1;
    }
    .slide-two .figure {
      background: #ffffff;
      border: 1px solid #d8d2c8;
      display: flex; flex-direction: column;
      justify-content: center; align-items: center;
      padding: 32px;
    }
    .slide-two .figure img {
      max-width: 100%; max-height: 100%;
      object-fit: contain;
    }
    .slide-two .figure-cap {
      font-family: var(--font-serif);
      font-style: italic;
      font-size: var(--size-tiny);
      color: var(--muted);
      margin-top: 16px;
      text-align: center;
    }
    .slide-two .text-col {
      display: flex; flex-direction: column;
      justify-content: center;
    }
    .slide-two .stat {
      font-family: var(--font-serif);
      font-size: var(--size-stat);
      font-weight: 400;
      color: var(--accent);
      letter-spacing: -3px;
      line-height: 1;
    }
    .slide-two .stat-label {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 12px;
    }
    .slide-two .text-col p {
      font-family: var(--font-serif);
      font-size: var(--size-body);
      line-height: 1.55;
      color: var(--ink);
      margin: 32px 0 0;
    }
```

- [ ] **Step 2: Add a `slide-two` slide**

After the `slide-content` block, add:

```html
    <section class="slide slide-two">
      <header class="slide-head">
        <span>Result</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <h2>Five benchmarks, one finding</h2>
        <div class="accent-rule"></div>
        <div class="two-cols">
          <div class="figure">
            <!-- Placeholder figure: an inline SVG bar chart. -->
            <svg viewBox="0 0 200 120" width="100%" height="320">
              <rect x="10"  y="80" width="28" height="40"  fill="#8b3a2f" opacity="0.65"/>
              <rect x="48"  y="60" width="28" height="60"  fill="#8b3a2f" opacity="0.75"/>
              <rect x="86"  y="40" width="28" height="80"  fill="#8b3a2f"/>
              <rect x="124" y="20" width="28" height="100" fill="#8b3a2f" opacity="0.85"/>
              <rect x="162" y="10" width="28" height="110" fill="#8b3a2f" opacity="0.95"/>
            </svg>
            <div class="figure-cap">Fig 1 · Accuracy across MMLU, ARC-c, GSM8K, HellaSwag, TruthfulQA.</div>
          </div>
          <div class="text-col">
            <div class="stat">−82%</div>
            <div class="stat-label">Inference cost vs. 7B baseline</div>
            <p>At 1.3B parameters our model matches the 7B baseline on four of five benchmarks at 18% of the cost.</p>
          </div>
        </div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and navigate to slide 4**

Expected: H2, brick-red rule, then a two-column grid. Left: a small bar chart in a white card with italic caption. Right: large brick-red "−82%" with sans uppercase label below and a serif paragraph beneath.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-two layout with figure + stat + text"
```

---

## Task 12: Implement `slide-quote` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-quote` CSS**

```css
    /* ============================================================
       LAYOUT 5: slide-quote
       ============================================================ */
    .slide-quote .slide-body {
      justify-content: center;
      align-items: flex-start;
      padding-left: 80px; padding-right: 80px;
    }
    .slide-quote .quote-mark {
      font-family: var(--font-serif);
      font-size: 160px;
      line-height: 0.4;
      color: var(--accent);
      margin-bottom: 36px;
    }
    .slide-quote .quote {
      font-family: var(--font-serif);
      font-style: italic;
      font-size: var(--size-quote);
      line-height: 1.35;
      letter-spacing: -0.5px;
      color: var(--ink);
      margin: 0;
      max-width: 88%;
    }
    .slide-quote .attr {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: var(--accent);
      margin-top: 40px;
    }
```

- [ ] **Step 2: Add a `slide-quote` slide**

After the `slide-two` block, add:

```html
    <section class="slide slide-quote">
      <header class="slide-head">
        <span>Main result</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <div class="quote-mark">&ldquo;</div>
        <p class="quote">Smaller models, trained on the right data, beat larger ones — and they keep beating them as you scale.</p>
        <div class="attr">— Main result · Section 4</div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and navigate to slide 5**

Expected: a large brick-red opening quote glyph, then an italic serif sentence ~3 lines long, then small uppercase brick-red attribution.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-quote layout"
```

---

## Task 13: Implement `slide-figure` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-figure` CSS**

```css
    /* ============================================================
       LAYOUT 6: slide-figure   (one dominant image)
       ============================================================ */
    .slide-figure .slide-body {
      gap: 24px;
    }
    .slide-figure .figure-area {
      flex: 1;
      background: #fff;
      border: 1px solid #d8d2c8;
      display: flex; align-items: center; justify-content: center;
      overflow: hidden;
      padding: 28px;
    }
    .slide-figure .figure-area img,
    .slide-figure .figure-area svg {
      max-width: 100%; max-height: 100%;
      object-fit: contain;
    }
    .slide-figure .figure-cap {
      font-family: var(--font-serif);
      font-style: italic;
      font-size: var(--size-sub);
      color: var(--muted);
      line-height: 1.4;
      margin: 0;
      max-width: 90%;
    }
    .slide-figure .figure-cap b {
      font-style: normal;
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--accent);
      margin-right: 14px;
    }
```

- [ ] **Step 2: Add a `slide-figure` slide**

After the `slide-quote` block, add:

```html
    <section class="slide slide-figure">
      <header class="slide-head">
        <span>Figure</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <div class="figure-area">
          <svg viewBox="0 0 600 320" width="100%" height="100%">
            <line x1="60"  y1="280" x2="560" y2="280" stroke="#1a1a1a" stroke-width="1"/>
            <line x1="60"  y1="40"  x2="60"  y2="280" stroke="#1a1a1a" stroke-width="1"/>
            <polyline points="60,260 160,220 260,180 360,130 460,90 560,70"
                      fill="none" stroke="#8b3a2f" stroke-width="3"/>
            <polyline points="60,250 160,240 260,225 360,200 460,180 560,170"
                      fill="none" stroke="#1a1a1a" stroke-width="2" stroke-dasharray="6,4"/>
          </svg>
        </div>
        <p class="figure-cap"><b>Fig 2</b>Held-out accuracy vs. training tokens. Solid: ours (1.3B + curated). Dashed: 7B baseline (uncurated web).</p>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and navigate to slide 6**

Expected: large white panel filling most of the slide with two line plots (brick-red solid above black dashed). Below: italic caption with a small brick-red "FIG 2" label and the description.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-figure layout"
```

---

## Task 14: Implement `slide-code` layout

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-code` CSS**

```css
    /* ============================================================
       LAYOUT 7: slide-code
       ============================================================ */
    .slide-code h2 {
      font-family: var(--font-serif);
      font-size: var(--size-h2);
      font-weight: 500;
      letter-spacing: -0.5px;
      margin: 0;
    }
    .slide-code .accent-rule { margin: 20px 0 28px; }
    .slide-code .code-block {
      background: #ece5d7;          /* paper, one notch darker */
      border: 1px solid #d8d2c8;
      padding: 32px 40px;
      flex: 1;
      overflow: hidden;
      position: relative;
      display: flex;
    }
    .slide-code .code-lang {
      position: absolute;
      top: 16px; right: 20px;
      font-family: var(--font-sans);
      font-size: var(--size-tiny);
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--accent);
    }
    .slide-code .lines {
      font-family: var(--font-mono);
      font-size: 26px; line-height: 1.55;
      color: #999;
      text-align: right;
      padding-right: 24px;
      border-right: 1px solid #c8c2b6;
      margin-right: 24px;
      user-select: none;
    }
    .slide-code .code {
      font-family: var(--font-mono);
      font-size: 26px; line-height: 1.55;
      color: var(--ink);
      white-space: pre;
      flex: 1;
    }
    .slide-code .code .k { color: var(--accent); }   /* keyword */
    .slide-code .code .s { color: #6f8a4b; }         /* string  */
    .slide-code .code .c { color: var(--faint); }    /* comment */
```

- [ ] **Step 2: Add a `slide-code` slide**

After the `slide-figure` block, add:

```html
    <section class="slide slide-code">
      <header class="slide-head">
        <span>Implementation</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <h2>Curation pipeline (sketch)</h2>
        <div class="accent-rule"></div>
        <div class="code-block">
          <div class="code-lang">Python</div>
          <pre class="lines">1
2
3
4
5
6
7</pre><pre class="code"><span class="k">def</span> curate(docs):
    docs = dedupe(docs, level=<span class="s">"document"</span>)
    docs = filter_by_quality(docs, threshold=<span class="s">"high"</span>)
    docs = balance_skills(docs, target=<span class="s">"uniform"</span>)
    <span class="c"># 50× minimum exposure per reasoning skill</span>
    docs = upsample_rare(docs, factor=<span class="s">50</span>)
    <span class="k">return</span> docs</pre>
        </div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Reload and navigate to slide 7**

Expected: H2, brick-red rule, then a darker-beige code panel with line numbers on the left and monospace code on the right. Keywords brick-red, strings olive, comments grey. Small brick-red "PYTHON" label top-right of the panel.

- [ ] **Step 4: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-code layout with line numbers and minimal syntax tinting"
```

---

## Task 15: Implement `slide-end` layout (references + thank-you variants)

**Files:**
- Modify: `html-templates/editorial-serif/template.html`

- [ ] **Step 1: Append `slide-end` CSS**

```css
    /* ============================================================
       LAYOUT 8: slide-end   (references or thank-you / Q&A)
       ============================================================ */
    .slide-end h2 {
      font-family: var(--font-serif);
      font-size: var(--size-h2);
      font-weight: 500;
      letter-spacing: -0.5px;
      margin: 0;
    }
    .slide-end .accent-rule { margin: 20px 0 32px; }
    .slide-end .refs {
      display: grid;
      grid-template-columns: 60px 1fr;
      column-gap: 24px;
      row-gap: 22px;
      font-family: var(--font-serif);
      font-size: var(--size-body);
      line-height: 1.5;
      color: var(--ink);
    }
    .slide-end .refs .n {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 1px;
      color: var(--accent);
      text-align: right;
      padding-top: 6px;
    }
    .slide-end .refs em { color: var(--muted); }

    /* "Thanks" variant: center massive serif + sans Q&A line. */
    .slide-end.thanks .slide-body {
      justify-content: center; align-items: flex-start;
    }
    .slide-end.thanks h2 {
      font-size: 140px; font-weight: 400; letter-spacing: -3px;
      line-height: 1;
    }
    .slide-end.thanks .qa {
      font-family: var(--font-sans);
      font-size: var(--size-meta);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 48px;
    }
```

- [ ] **Step 2: Add a `slide-end` references slide**

After the `slide-code` block, add:

```html
    <section class="slide slide-end">
      <header class="slide-head">
        <span>Appendix</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <h2>References</h2>
        <div class="accent-rule"></div>
        <div class="refs">
          <div class="n">[1]</div><div>Hoffmann et al. <em>Training compute-optimal large language models.</em> NeurIPS 2022.</div>
          <div class="n">[2]</div><div>Penedo et al. <em>The RefinedWeb dataset for Falcon LLM.</em> arXiv 2023.</div>
          <div class="n">[3]</div><div>Sorscher et al. <em>Beyond neural scaling laws.</em> NeurIPS 2022.</div>
          <div class="n">[4]</div><div>Lee et al. <em>Deduplicating training data makes language models better.</em> ACL 2022.</div>
        </div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 3: Add a `slide-end.thanks` slide as the very last one**

After the references slide, add:

```html
    <section class="slide slide-end thanks">
      <header class="slide-head">
        <span>Q & A</span>
        <span>EMNLP 2026</span>
      </header>
      <div class="slide-body">
        <h2>Thank you.</h2>
        <div class="accent-rule"></div>
        <div class="qa">jane.doe@kcl.ac.uk · @kclnlp</div>
      </div>
      <footer class="slide-foot">
        <span>KCL · NLP Group · Alan Turing</span>
        <span data-auto-page></span>
      </footer>
    </section>
```

- [ ] **Step 4: Reload and navigate to slides 8 and 9**

Expected (slide 8): H2 "References", brick-red rule, then a 4-row grid: each row has a small brick-red `[N]` label and a serif citation with italic title.

Expected (slide 9): a huge serif "Thank you.", a brick-red rule, then a tiny sans email + handle line below.

- [ ] **Step 5: Commit**

```bash
git add html-templates/editorial-serif/template.html
git commit -m "add slide-end layout with references and thanks variants"
```

---

## Task 16: Smoke-test the whole template

**Files:**
- (no edits; verification only)

- [ ] **Step 1: Visual walkthrough**

In Chrome, open `template.html`. Press `→` 8 times, advancing through all 9 slides (slide-title, slide-section, slide-content, slide-two, slide-quote, slide-figure, slide-code, references, thanks). Each should look polished and the design rhythm consistent.

- [ ] **Step 2: Keyboard test**

From the first slide:
- `End` → last slide
- `Home` → first slide
- Type `5` then `Enter` → slide 5
- `O` → overview grid with 9 thumbnails
- click slide 3 → exits grid, shows slide 3
- `B` → black; `B` → restore
- `W` → white; `Esc` → restore
- `?` → cheat sheet shown; `Esc` → dismissed
- `F` → fullscreen; `F` → exit

- [ ] **Step 3: Resize test**

Drag the window to extreme proportions (very narrow tall window, then very wide short window). Stage scales without breaking, hairlines stay aligned, footer never overlaps body.

- [ ] **Step 4: Print test**

`Ctrl/Cmd + P` → preview shows exactly 9 pages, each a complete slide, no clipping. Cancel.

- [ ] **Step 5: Cross-browser sanity check**

Open the same file in Firefox. Walk through all 9 slides; print preview. Repeat in Safari if available. Note any visual differences in a scratch buffer; we'll address them inline.

- [ ] **Step 6: Commit any inline fixes that arose**

If you fixed issues (e.g. Safari rendering quirk):

```bash
git add html-templates/editorial-serif/template.html
git commit -m "fix cross-browser rendering issues found during smoke test"
```

If no fixes were needed, skip the commit.

---

## Task 17: Create `example-talk.html` by copying `template.html`

**Files:**
- Create: `html-templates/editorial-serif/example-talk.html` (copy of template.html)

Because the file is single-source-of-truth for CSS/JS, the example deck is the same file with richer body content. Future CSS or JS updates need to be applied to both files; this is the deliberate cost of zero-build distribution. README will note this in Task 18.

- [ ] **Step 1: Copy the file**

```bash
cp html-templates/editorial-serif/template.html html-templates/editorial-serif/example-talk.html
```

- [ ] **Step 2: Change the `<title>`**

In `example-talk.html`, find:

```html
  <title>Talk title</title>
```

Replace with:

```html
  <title>Smaller language models, trained on the right data</title>
```

- [ ] **Step 3: Add a presenter notes example to one slide**

In `example-talk.html`, inside the existing `<section class="slide slide-content">` (the "Three properties of right data" slide), add **just before** its closing `</section>`:

```html
      <aside class="notes">
        Spend extra time on point 3 — reviewers always ask about temporal contamination.
        Have the Sept-2024 cutoff date ready.
      </aside>
```

- [ ] **Step 4: Verify**

Open `example-talk.html` in Chrome:
- Browser tab title should read the new title.
- Walk through all 9 slides — they render identically to template.html (intentional; the example *is* the template with notes added).
- Reload with `?notes` appended to the URL. On the "Three properties" slide a small rehearsal box should appear bottom-right.

- [ ] **Step 5: Commit**

```bash
git add html-templates/editorial-serif/example-talk.html
git commit -m "add example-talk.html with presenter notes example"
```

---

## Task 18: Write `README.md`

**Files:**
- Create: `html-templates/editorial-serif/README.md`

- [ ] **Step 1: Write the README**

Create `html-templates/editorial-serif/README.md`:

````markdown
# KCLNLP HTML Slide Template — Editorial Serif

A single-file, zero-dependency HTML deck template for KCL NLP talks.
Open it in any modern browser, scale to any 16:9 display, edit as plain HTML.

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
| `assets/logos/`     | KCL / KCLNLP / Alan Turing PNGs you may reference in slides.  |

The CSS and JS are duplicated between `template.html` and
`example-talk.html`. This is intentional — it preserves the
"single-file, drop-anywhere" property. When upstream tokens change,
apply the diff to both files.

## Browser support

Chrome, Firefox, Safari, Edge — all recent versions. The template uses
no experimental features; only `transform`, `aspect-ratio`, `flex`,
`grid`, `@page`, and standard event APIs.
````

- [ ] **Step 2: Render the README in your editor or `grip`-style preview to sanity check formatting**

Visually skim the rendered markdown. Tables align, code blocks render, no dangling backticks.

- [ ] **Step 3: Commit**

```bash
git add html-templates/editorial-serif/README.md
git commit -m "add README with quickstart, keyboard map, layouts, theming guide"
```

---

## Task 19: Link the HTML template from the root README

**Files:**
- Modify: `README.md` (root)

- [ ] **Step 1: Inspect the current root README**

```bash
head -60 README.md
```

Look for an obvious place to add a new section — typically near where the pptx templates are mentioned.

- [ ] **Step 2: Add an HTML template section**

In `README.md` find a logical location (e.g. after the templates table or after the "Templates" heading). Insert a new section:

```markdown
## HTML deck template

A browser-based, single-file alternative to the pptx decks lives at
[`html-templates/editorial-serif/`](html-templates/editorial-serif/).
Copy `template.html`, edit the slides inline, open in any browser —
no build step. See the directory's own README for the full keyboard
map and layout reference.
```

> If the root README has no template section yet, append the block at the bottom under a new top-level `## HTML deck template` heading.

- [ ] **Step 3: Verify the link**

```bash
grep -c 'html-templates/editorial-serif' README.md
```

Expected: at least `1`.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "link HTML deck template from root README"
```

---

## Task 20: Final acceptance test

**Files:**
- (no edits; user-facing acceptance)

- [ ] **Step 1: Zip-and-extract test**

```bash
cd /tmp
rm -rf editorial-serif-test
cp -r /cephfs/volumes/hpc_data_prj/cllm/a25d4624-b5df-42a8-beb9-b8da3d7ff79b/yizhen/prj08_KCLNLP_PPT/KCLNLP_SlidesTemplate/html-templates/editorial-serif editorial-serif-test
zip -r editorial-serif-test.zip editorial-serif-test
rm -rf editorial-serif-test
unzip editorial-serif-test.zip
```

Open `/tmp/editorial-serif-test/example-talk.html` in Chrome. Expected: deck renders identically to the in-repo version. Logos resolvable (if any slide referenced them).

- [ ] **Step 2: Multi-display test (best-effort)**

If you have an external display, drag the browser to it and toggle fullscreen with `F`. Stage scales correctly without overflow or letterbox bug at any aspect ratio.

- [ ] **Step 3: Final cross-browser sanity**

Open `example-talk.html` once in Chrome, Firefox, and (if available) Safari. Walk slides; print preview. Note: small typographic differences are acceptable; broken layouts are not.

- [ ] **Step 4: Clean up the scratch test files**

```bash
rm -rf /tmp/editorial-serif-test /tmp/editorial-serif-test.zip
```

- [ ] **Step 5: Update the project memory (optional but recommended)**

If the work is complete and you intend to push:

```bash
git log --oneline -25
```

Confirm a clean chain of commits from Task 1 through Task 19. Push only after explicit user approval (per project memory: "Do not open PRs without explicit approval").

---

## Self-Review Notes

- **Spec coverage:** §1 Scope → Task 1 (scaffolding), Task 17 (example deck), Task 18-19 (docs). §2 Design tokens → Task 3. §3 Layouts → Tasks 8-15. §4 Interaction → Tasks 5-6. §5 File structure & skeleton → Tasks 1-2, 17. §6 Implementation phasing matches Tasks 1-19. Acceptance criteria → Task 20.
- **Risks from spec §6:**
  - Safari `webkitRequestFullscreen` — handled in Task 6 (`_toggleFullscreen` falls back).
  - Source Serif / Inter not installed — all font declarations end in system fallbacks (Task 3); README explains (Task 18).
  - Chrome vs. Firefox print CSS — both covered in Task 16 step 5 and Task 20 step 3.
- **Placeholder scan:** No "TBD"/"TODO"/etc. in actionable steps. Every CSS, HTML, and JS step shows the literal code to write.
- **Type consistency:** `SlidePresentation` class methods (`_fit`, `_show`, `_readHash`, `_onHash`, `_fillAutoPage`, `next`/`prev`/`first`/`last`/`goTo`, `_onKey`, `_renderNumBuffer`, `_toggleBody`, `_toggleFullscreen`, `_toggleGrid`, `_toggleCheat`) introduced in Tasks 4-6 and referenced consistently. CSS class names (`slide`, `slide-X`, `slide-head`, `slide-foot`, `slide-body`, `accent-rule`, `kicker`, `is-current`, `is-grid`, `is-black`, `is-white`, `is-notes`, `cheat-overlay`, `slide-wrap`) are consistent across CSS and JS.
