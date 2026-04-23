"""Generate the parchment background and tree-branch motif PNGs."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from theme import BRONZE, GENERATED_DIR, MUTED, OLIVE, PARCHMENT


def _radial_gradient(size, inner, outer):
    w, h = size
    img = Image.new("RGB", size, outer)
    px = img.load()
    cx, cy = w / 2, h / 2
    max_d = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            t = math.hypot(x - cx, y - cy) / max_d
            t = min(1.0, t ** 1.25)
            r = int(inner[0] * (1 - t) + outer[0] * t)
            g = int(inner[1] * (1 - t) + outer[1] * t)
            b = int(inner[2] * (1 - t) + outer[2] * t)
            px[x, y] = (r, g, b)
    return img


def _add_noise(img, amp=8, seed=7):
    rng = random.Random(seed)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            n = rng.randint(-amp, amp)
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n - 1)),
            )
    return img


def make_parchment(path: Path, size=(1333, 750)):
    inner = (246, 238, 218)
    outer = (228, 214, 182)
    img = _radial_gradient(size, inner, outer)
    img = _add_noise(img, amp=6)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img = _add_noise(img, amp=3, seed=42)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


def _branch_segment(draw, p0, p1, width, color_rgba):
    x0, y0 = p0
    x1, y1 = p1
    steps = max(2, int(math.hypot(x1 - x0, y1 - y0) / 4))
    for i in range(steps + 1):
        t = i / steps
        x = x0 * (1 - t) + x1 * t
        y = y0 * (1 - t) + y1 * t
        w = width * (1 - t * 0.55)
        r = max(0.5, w / 2)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color_rgba)


def _leaf(draw, cx, cy, length, angle, color_rgba):
    pts = []
    for t in [i / 20 for i in range(21)]:
        u = t - 0.5
        width = (1 - 4 * u * u) * length * 0.28
        x = (t - 0.5) * length
        y = width
        ca, sa = math.cos(angle), math.sin(angle)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    for t in [i / 20 for i in range(21)]:
        u = t - 0.5
        width = -(1 - 4 * u * u) * length * 0.28
        x = (t - 0.5) * length
        y = width
        ca, sa = math.cos(angle), math.sin(angle)
        pts.append((cx + (length / 2 - x + (-length / 2)) * ca - y * sa,
                    cy + (length / 2 - x + (-length / 2)) * sa + y * ca))
    simple = []
    for t in [i / 24 for i in range(25)]:
        u = t - 0.5
        width = (1 - 4 * u * u) * length * 0.25
        x = (t - 0.5) * length
        y = width
        ca, sa = math.cos(angle), math.sin(angle)
        simple.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    for t in [i / 24 for i in range(25)]:
        u = 0.5 - t
        width = -(1 - 4 * u * u) * length * 0.25
        x = (0.5 - t) * length
        y = width
        ca, sa = math.cos(angle), math.sin(angle)
        simple.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    draw.polygon(simple, fill=color_rgba)


def make_branch(path: Path, size=(1600, 1200)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    bronze_rgba = (*BRONZE, 95)
    muted_rgba = (*MUTED, 75)
    olive_rgba = (*OLIVE, 105)

    start = (w * 0.05, h * 0.95)
    anchor = (w * 0.55, h * 0.40)
    tip = (w * 0.92, h * 0.12)

    trunk_pts = []
    for i in range(61):
        t = i / 60
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * anchor[0] + t ** 2 * tip[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * anchor[1] + t ** 2 * tip[1]
        trunk_pts.append((x, y))
    for i in range(len(trunk_pts) - 1):
        thickness = 22 - (i / len(trunk_pts)) * 17
        _branch_segment(draw, trunk_pts[i], trunk_pts[i + 1], thickness, bronze_rgba)

    branch_specs = [
        (0.25, (-0.35, -0.55), 0.28),
        (0.40, (0.20, -0.45), 0.22),
        (0.55, (-0.45, -0.30), 0.30),
        (0.72, (0.30, -0.55), 0.22),
        (0.88, (-0.20, -0.35), 0.18),
    ]
    for anchor_t, (dx_mul, dy_mul), scale in branch_specs:
        idx = int(anchor_t * (len(trunk_pts) - 1))
        bx, by = trunk_pts[idx]
        end = (bx + w * scale * dx_mul, by + h * scale * dy_mul)
        ctrl = ((bx + end[0]) / 2, by + h * scale * (dy_mul - 0.15))
        prev = (bx, by)
        for i in range(1, 31):
            t = i / 30
            x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * ctrl[0] + t ** 2 * end[0]
            y = (1 - t) ** 2 * by + 2 * (1 - t) * t * ctrl[1] + t ** 2 * end[1]
            _branch_segment(draw, prev, (x, y), 8 * (1 - t * 0.6), muted_rgba)
            prev = (x, y)

    leaf_specs = [
        (0.30, 160, 0.6),
        (0.46, 150, -0.4),
        (0.60, 180, 0.8),
        (0.68, 140, -0.2),
        (0.78, 170, 1.0),
        (0.86, 150, -0.5),
        (0.93, 130, 0.3),
    ]
    for anchor_t, length, angle in leaf_specs:
        idx = int(anchor_t * (len(trunk_pts) - 1))
        bx, by = trunk_pts[idx]
        offx = math.cos(angle) * length * 0.6
        offy = math.sin(angle) * length * 0.6 - 20
        _leaf(draw, bx + offx, by + offy, length, angle, olive_rgba)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


def ensure_textures(force: bool = False):
    from theme import BRANCH_PNG, PARCHMENT_PNG
    if force or not PARCHMENT_PNG.exists():
        make_parchment(PARCHMENT_PNG)
    if force or not BRANCH_PNG.exists():
        make_branch(BRANCH_PNG)


if __name__ == "__main__":
    import sys
    ensure_textures(force="--force" in sys.argv)
    print(f"parchment: {GENERATED_DIR / 'parchment_bg.png'}")
    print(f"branch:    {GENERATED_DIR / 'tree_branch.png'}")
