"""Build the Tree Yellow Texture demo deck.

Run: python templates/tree_yellow_texture/build.py
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
from textures import ensure_textures

OUTPUT = Path(__file__).resolve().parent / "KCLNLP_TreeYellow.pptx"


def rgb(tup):
    return RGBColor(*tup)


def add_background(slide):
    pic = slide.shapes.add_picture(
        str(T.PARCHMENT_PNG), 0, 0, width=T.SLIDE_W, height=T.SLIDE_H
    )
    spTree = slide.shapes._spTree
    spTree.remove(pic._element)
    spTree.insert(2, pic._element)


def _logo_width(path, height_emu):
    with Image.open(path) as im:
        w, h = im.size
    return int(height_emu * (w / h))


def add_logo_header(slide):
    right = T.SLIDE_W - T.EDGE_PAD
    top = Inches(0.14)
    widths = [_logo_width(p, T.LOGO_H) for p in T.LOGOS]
    total = sum(widths) + T.LOGO_GAP * (len(T.LOGOS) - 1)
    x = right - total
    for i, path in enumerate(T.LOGOS):
        slide.shapes.add_picture(str(path), x, top, height=T.LOGO_H)
        x += widths[i]
        if i < len(T.LOGOS) - 1:
            sep_x = x + T.LOGO_GAP // 2
            sep = slide.shapes.add_connector(1, sep_x, top + Inches(0.06),
                                             sep_x, top + T.LOGO_H - Inches(0.06))
            sep.line.color.rgb = rgb(T.BRONZE)
            sep.line.width = Emu(4000)
            x += T.LOGO_GAP

    rule_y = T.HEADER_H + Inches(0.08)
    rule = slide.shapes.add_connector(
        1, T.EDGE_PAD, rule_y, T.SLIDE_W - T.EDGE_PAD, rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(9525)


def add_branch_accent(slide, scale=1.0, right=True, bottom=True):
    img_w = Inches(7.0 * scale)
    with Image.open(T.BRANCH_PNG) as im:
        ratio = im.size[1] / im.size[0]
    img_h = Emu(int(img_w * ratio))
    x = T.SLIDE_W - img_w - Inches(-0.3) if right else Inches(-0.3)
    y = T.SLIDE_H - img_h + Inches(0.2) if bottom else Inches(-0.2)
    pic = slide.shapes.add_picture(str(T.BRANCH_PNG), x, y, width=img_w, height=img_h)
    spTree = slide.shapes._spTree
    spTree.remove(pic._element)
    spTree.insert(3, pic._element)


def add_left_rule(slide):
    x = T.EDGE_PAD - Inches(0.12)
    top = T.HEADER_H + Inches(0.3)
    bot = T.SLIDE_H - Inches(0.5)
    rule = slide.shapes.add_connector(1, x, top, x, bot)
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(12700)

    mid = (top + bot) // 2
    leaf = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, x - Inches(0.08), mid - Inches(0.09),
        Inches(0.16), Inches(0.22)
    )
    leaf.rotation = 25
    leaf.fill.solid()
    leaf.fill.fore_color.rgb = rgb(T.OLIVE)
    leaf.line.color.rgb = rgb(T.BRONZE)
    leaf.line.width = Emu(4000)


def _add_text(slide, left, top, width, height, text, *, font, size, color,
              bold=False, italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
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


def _add_bullets(slide, left, top, width, height, items, *, size=T.SZ_BODY):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = f"•  {item}"
        run.font.name = T.FONT_BODY
        run.font.size = size
        run.font.color.rgb = rgb(T.ESPRESSO)
    return box


def slide_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_branch_accent(slide, scale=1.15, right=True, bottom=True)
    add_logo_header(slide)

    eyebrow_top = Inches(2.2)
    _add_text(slide, T.EDGE_PAD + Inches(0.2), eyebrow_top,
              Inches(8), Inches(0.4),
              "KCL NLP  ·  Research Talk",
              font=T.FONT_BODY, size=Pt(14), color=T.BRONZE,
              bold=True, italic=True)

    _add_text(slide, T.EDGE_PAD + Inches(0.2), eyebrow_top + Inches(0.5),
              Inches(10), Inches(1.6),
              "Talk Title Goes Here",
              font=T.FONT_HEAD, size=T.SZ_TITLE, color=T.ESPRESSO, bold=True)

    _add_text(slide, T.EDGE_PAD + Inches(0.2), eyebrow_top + Inches(2.0),
              Inches(10), Inches(0.6),
              "A concise subtitle or one-line abstract",
              font=T.FONT_HEAD, size=T.SZ_SUBTITLE, color=T.MUTED, italic=True)

    rule_y = eyebrow_top + Inches(2.9)
    rule = slide.shapes.add_connector(
        1, T.EDGE_PAD + Inches(0.2), rule_y,
        T.EDGE_PAD + Inches(2.0), rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(19050)

    _add_text(slide, T.EDGE_PAD + Inches(0.2), rule_y + Inches(0.1),
              Inches(10), Inches(0.4),
              "Speaker Name  ·  Affiliation  ·  Month Year",
              font=T.FONT_BODY, size=Pt(14), color=T.ESPRESSO)


def slide_section(prs, number="01", title="Section Heading"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_branch_accent(slide, scale=1.0, right=False, bottom=True)
    add_logo_header(slide)

    cx_left = Inches(4.3)
    _add_text(slide, cx_left, Inches(2.7), Inches(1.6), Inches(1.0),
              number, font=T.FONT_HEAD, size=Pt(64), color=T.GOLD, bold=True)

    rule_x = cx_left + Inches(1.7)
    rule = slide.shapes.add_connector(
        1, rule_x, Inches(3.15), rule_x, Inches(4.55)
    )
    rule.line.color.rgb = rgb(T.BRONZE)
    rule.line.width = Emu(12700)

    _add_text(slide, rule_x + Inches(0.3), Inches(2.95),
              Inches(7.5), Inches(1.3),
              title, font=T.FONT_HEAD, size=T.SZ_SECTION,
              color=T.ESPRESSO, bold=True)

    _add_text(slide, rule_x + Inches(0.3), Inches(4.0),
              Inches(7.5), Inches(0.5),
              "An optional one-line summary of this section",
              font=T.FONT_BODY, size=Pt(14), color=T.MUTED, italic=True)


def slide_content(prs, title="Slide title", bullets=None):
    bullets = bullets or [
        "Lead with the main claim — what the reader should take away",
        "Supporting detail, ideally a number or concrete example",
        "A second supporting point that extends the first",
        "Edge case, caveat, or the one thing not to forget",
    ]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_logo_header(slide)
    add_left_rule(slide)

    _add_text(slide, T.EDGE_PAD + Inches(0.3), T.HEADER_H + Inches(0.35),
              Inches(11), Inches(0.9),
              title, font=T.FONT_HEAD, size=T.SZ_SLIDE_TITLE,
              color=T.ESPRESSO, bold=True)

    under_y = T.HEADER_H + Inches(1.2)
    rule = slide.shapes.add_connector(
        1, T.EDGE_PAD + Inches(0.3), under_y,
        T.EDGE_PAD + Inches(1.2), under_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(12700)

    _add_bullets(slide, T.EDGE_PAD + Inches(0.3), under_y + Inches(0.3),
                 Inches(11.7), Inches(4.6), bullets)

    _add_text(slide, T.EDGE_PAD + Inches(0.3),
              T.SLIDE_H - Inches(0.45),
              Inches(11.7), Inches(0.3),
              "Footer / citation / page note",
              font=T.FONT_BODY, size=T.SZ_CAPTION, color=T.MUTED, italic=True)


def slide_two_column(prs, title="Figure or image + text"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_logo_header(slide)
    add_left_rule(slide)

    _add_text(slide, T.EDGE_PAD + Inches(0.3), T.HEADER_H + Inches(0.35),
              Inches(11), Inches(0.9),
              title, font=T.FONT_HEAD, size=T.SZ_SLIDE_TITLE,
              color=T.ESPRESSO, bold=True)

    under_y = T.HEADER_H + Inches(1.2)
    rule = slide.shapes.add_connector(
        1, T.EDGE_PAD + Inches(0.3), under_y,
        T.EDGE_PAD + Inches(1.2), under_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(12700)

    left_x = T.EDGE_PAD + Inches(0.3)
    col_top = under_y + Inches(0.35)
    col_h = Inches(4.6)
    col_w = Inches(5.6)

    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left_x, col_top, col_w, col_h
    )
    frame.fill.solid()
    frame.fill.fore_color.rgb = rgb((236, 223, 195))
    frame.line.color.rgb = rgb(T.BRONZE)
    frame.line.width = Emu(9525)
    _add_text(slide, left_x, col_top, col_w, col_h,
              "[ figure / diagram ]",
              font=T.FONT_BODY, size=Pt(14), color=T.MUTED, italic=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    divider_x = left_x + col_w + Inches(0.35)
    div = slide.shapes.add_connector(
        1, divider_x, col_top + Inches(0.2),
        divider_x, col_top + col_h - Inches(0.2)
    )
    div.line.color.rgb = rgb(T.OLIVE)
    div.line.width = Emu(9525)

    text_x = divider_x + Inches(0.35)
    text_w = T.SLIDE_W - text_x - T.EDGE_PAD
    _add_text(slide, text_x, col_top,
              text_w, Inches(0.5),
              "Caption or claim",
              font=T.FONT_HEAD, size=Pt(20), color=T.ESPRESSO, bold=True)
    _add_bullets(slide, text_x, col_top + Inches(0.7),
                 text_w, col_h - Inches(0.7),
                 ["Explain what the figure shows",
                  "Call out the one feature worth noting",
                  "Relate it back to the slide's main point"],
                 size=Pt(15))


def slide_thanks(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_branch_accent(slide, scale=1.2, right=True, bottom=True)
    add_logo_header(slide)

    cy = Inches(2.8)
    _add_text(slide, T.EDGE_PAD + Inches(0.2), cy,
              Inches(10), Inches(1.4),
              "Thank you",
              font=T.FONT_HEAD, size=Pt(60), color=T.ESPRESSO, bold=True)

    rule_y = cy + Inches(1.5)
    rule = slide.shapes.add_connector(
        1, T.EDGE_PAD + Inches(0.2), rule_y,
        T.EDGE_PAD + Inches(2.0), rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(19050)

    _add_text(slide, T.EDGE_PAD + Inches(0.2), rule_y + Inches(0.2),
              Inches(10), Inches(0.5),
              "Questions & discussion",
              font=T.FONT_HEAD, size=Pt(22), color=T.MUTED, italic=True)

    _add_text(slide, T.EDGE_PAD + Inches(0.2), rule_y + Inches(1.1),
              Inches(10), Inches(0.4),
              "speaker@kcl.ac.uk  ·  kclnlp.github.io",
              font=T.FONT_BODY, size=Pt(14), color=T.ESPRESSO)


def build():
    ensure_textures()
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H

    slide_title(prs)
    slide_section(prs, number="01", title="Motivation")
    slide_content(prs)
    slide_two_column(prs)
    slide_thanks(prs)

    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    build()
