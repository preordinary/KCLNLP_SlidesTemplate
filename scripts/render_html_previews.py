"""Render PNG previews of the editorial-serif HTML deck for the README.

One-shot, locally-run script. Requires:
  pip install --user playwright
  python3 -m playwright install chromium

Renders the 1920x1080 stage at native resolution, crops to the slide, then
downscales to README-friendly width.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

REPO = Path(__file__).resolve().parent.parent
DECK = REPO / "html-templates" / "editorial-serif" / "example-talk.html"
OUT_DIR = REPO / "assets" / "images"

# (slide-number-in-deck, output-name)
SHOTS = [
    (1, "editorial_serif_title.png"),    # slide-title
    (3, "editorial_serif_content.png"),  # slide-content
]

STAGE_W = 1920
STAGE_H = 1080


async def render():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Native-resolution viewport so the deck stage doesn't have to scale
        # down. The deck's _fit() reads viewport size, picks --scale, and centers
        # the 1920x1080 stage.
        ctx = await browser.new_context(viewport={"width": STAGE_W, "height": STAGE_H})
        page = await ctx.new_page()

        for slide_idx, out_name in SHOTS:
            url = f"file://{DECK}#{slide_idx}"
            await page.goto(url, wait_until="networkidle")
            # Let _fit() finish a frame
            await page.wait_for_timeout(200)
            target = OUT_DIR / out_name
            # Capture the .stage element itself, which is always 1920x1080
            stage = page.locator(".stage")
            await stage.screenshot(path=str(target), type="png")
            print(f"wrote {target.relative_to(REPO)}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(render())
