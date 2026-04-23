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

OUTPUT = Path(__file__).resolve().parent / "KCLNLP_TreeYellow.pptx"


def rgb(tup):
    return RGBColor(*tup)


def _logo_width(path, height_emu):
    with Image.open(path) as im:
        w, h = im.size
    return int(height_emu * (w / h))


def add_logo_header(slide, with_rule=True):
    right = T.SLIDE_W - T.EDGE_PAD
    top = Inches(0.22)
    widths = [_logo_width(p, T.LOGO_H) for p in T.LOGOS]
    total = sum(widths) + T.LOGO_GAP * (len(T.LOGOS) - 1)
    x = right - total
    for i, path in enumerate(T.LOGOS):
        slide.shapes.add_picture(str(path), x, top, height=T.LOGO_H)
        x += widths[i] + (T.LOGO_GAP if i < len(T.LOGOS) - 1 else 0)

    if with_rule:
        rule_y = T.HEADER_H + Inches(0.20)
        rule = slide.shapes.add_connector(
            1, T.EDGE_PAD, rule_y, T.SLIDE_W - T.EDGE_PAD, rule_y
        )
        rule.line.color.rgb = rgb(T.GOLD)
        rule.line.width = Emu(9525)


def add_title_accent(slide, x, y, h):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(T.GOLD)
    bar.line.fill.background()


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
        run.font.color.rgb = rgb(T.INK)
    return box


def slide_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo_header(slide)

    left = T.EDGE_PAD + Inches(0.2)
    title_top = Inches(2.6)

    add_title_accent(slide, left, title_top + Inches(0.1), Inches(1.4))
    _add_text(slide, left + Inches(0.35), title_top,
              Inches(11), Inches(1.6),
              "Talk Title Goes Here",
              font=T.FONT_HEAD, size=T.SZ_TITLE, color=T.INK, bold=True)

    _add_text(slide, left + Inches(0.35), title_top + Inches(1.5),
              Inches(11), Inches(0.6),
              "A concise subtitle or one-line abstract",
              font=T.FONT_BODY, size=T.SZ_SUBTITLE, color=T.MUTED, italic=True)

    rule_y = title_top + Inches(2.3)
    rule = slide.shapes.add_connector(
        1, left + Inches(0.35), rule_y,
        left + Inches(2.2), rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(19050)

    _add_text(slide, left + Inches(0.35), rule_y + Inches(0.15),
              Inches(11), Inches(0.4),
              "Speaker Name  ·  Affiliation  ·  Month Year",
              font=T.FONT_BODY, size=Pt(14), color=T.INK)


def slide_section(prs, number="01", title="Section Heading"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo_header(slide)

    left = T.EDGE_PAD + Inches(0.5)
    y = Inches(3.0)

    _add_text(slide, left, y, Inches(1.8), Inches(1.2),
              number, font=T.FONT_HEAD, size=Pt(56), color=T.GOLD, bold=True)

    rule_x = left + Inches(1.9)
    rule = slide.shapes.add_connector(
        1, rule_x, y + Inches(0.25), rule_x, y + Inches(1.15)
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(12700)

    _add_text(slide, rule_x + Inches(0.3), y + Inches(0.2),
              Inches(8), Inches(1.0),
              title, font=T.FONT_HEAD, size=T.SZ_SECTION,
              color=T.INK, bold=True)

    _add_text(slide, rule_x + Inches(0.3), y + Inches(1.05),
              Inches(8), Inches(0.4),
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
    add_logo_header(slide)

    left = T.EDGE_PAD + Inches(0.1)
    title_top = T.HEADER_H + Inches(0.45)

    add_title_accent(slide, left, title_top + Inches(0.08), Inches(0.7))
    _add_text(slide, left + Inches(0.3), title_top,
              Inches(11), Inches(0.9),
              title, font=T.FONT_HEAD, size=T.SZ_SLIDE_TITLE,
              color=T.INK, bold=True)

    rule_y = title_top + Inches(0.95)
    rule = slide.shapes.add_connector(
        1, left + Inches(0.3), rule_y,
        T.SLIDE_W - T.EDGE_PAD, rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(6350)

    _add_bullets(slide, left + Inches(0.3), rule_y + Inches(0.3),
                 Inches(12.0), Inches(4.6), bullets)

    _add_text(slide, left + Inches(0.3),
              T.SLIDE_H - Inches(0.4),
              Inches(12.0), Inches(0.3),
              "Footer / citation / page note",
              font=T.FONT_BODY, size=T.SZ_CAPTION, color=T.MUTED, italic=True)


def slide_two_column(prs, title="Figure or image + text"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo_header(slide)

    left = T.EDGE_PAD + Inches(0.1)
    title_top = T.HEADER_H + Inches(0.45)

    add_title_accent(slide, left, title_top + Inches(0.08), Inches(0.7))
    _add_text(slide, left + Inches(0.3), title_top,
              Inches(11), Inches(0.9),
              title, font=T.FONT_HEAD, size=T.SZ_SLIDE_TITLE,
              color=T.INK, bold=True)

    rule_y = title_top + Inches(0.95)
    rule = slide.shapes.add_connector(
        1, left + Inches(0.3), rule_y,
        T.SLIDE_W - T.EDGE_PAD, rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(6350)

    col_x = left + Inches(0.3)
    col_top = rule_y + Inches(0.3)
    col_h = Inches(4.5)
    col_w = Inches(5.8)

    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, col_x, col_top, col_w, col_h
    )
    frame.fill.background()
    frame.line.color.rgb = rgb(T.MUTED)
    frame.line.width = Emu(6350)
    _add_text(slide, col_x, col_top, col_w, col_h,
              "[ figure / diagram ]",
              font=T.FONT_BODY, size=Pt(14), color=T.MUTED, italic=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    text_x = col_x + col_w + Inches(0.5)
    text_w = T.SLIDE_W - text_x - T.EDGE_PAD
    _add_text(slide, text_x, col_top,
              text_w, Inches(0.5),
              "Caption or claim",
              font=T.FONT_HEAD, size=Pt(20), color=T.INK, bold=True)
    _add_bullets(slide, text_x, col_top + Inches(0.7),
                 text_w, col_h - Inches(0.7),
                 ["Explain what the figure shows",
                  "Call out the one feature worth noting",
                  "Relate it back to the slide's main point"],
                 size=Pt(15))


def slide_thanks(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo_header(slide)

    left = T.EDGE_PAD + Inches(0.2)
    y = Inches(3.0)

    add_title_accent(slide, left, y + Inches(0.15), Inches(1.6))
    _add_text(slide, left + Inches(0.35), y,
              Inches(10), Inches(1.6),
              "Thank you",
              font=T.FONT_HEAD, size=Pt(56), color=T.INK, bold=True)

    rule_y = y + Inches(1.75)
    rule = slide.shapes.add_connector(
        1, left + Inches(0.35), rule_y,
        left + Inches(2.2), rule_y
    )
    rule.line.color.rgb = rgb(T.GOLD)
    rule.line.width = Emu(19050)

    _add_text(slide, left + Inches(0.35), rule_y + Inches(0.2),
              Inches(10), Inches(0.5),
              "Questions & discussion",
              font=T.FONT_BODY, size=Pt(20), color=T.MUTED, italic=True)

    _add_text(slide, left + Inches(0.35), rule_y + Inches(1.0),
              Inches(10), Inches(0.4),
              "speaker@kcl.ac.uk  ·  kclnlp.github.io",
              font=T.FONT_BODY, size=Pt(14), color=T.INK)


def build():
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
