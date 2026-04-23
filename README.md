# KCLNLP_SlidesTemplate

PowerPoint templates for the **KCL NLP** research group, designed for consistent outreach and presentation of our research work (talks, posters, seminars, reading groups, etc.).

## Templates

### Tree Yellow Texture

A minimal 16:9 deck. A cream header band carries the slide title on the left (as **"Now: <title>"**) and the KCL, KCLNLP, and Alan Turing Institute logos on the right, separated from the body by a thick orange rule. Titles live in the header so the body has the full slide to breathe. Typography: **Calibri** throughout (bold + italic for the header title, regular for body).

- Built deck: [`templates/tree_yellow_texture/KCLNLP_TreeYellow.pptx`](templates/tree_yellow_texture/KCLNLP_TreeYellow.pptx)
- Layouts included: title (left-aligned + centered variants), section divider, content (title + bullets), two-column (figure + text), thank-you / Q&A (left-aligned + centered variants).

Regenerate from source:

```bash
pip install -r requirements.txt
python templates/tree_yellow_texture/build.py
```

### Royal Blue

A formal academic 16:9 deck. White background, with a thick royal-blue rule framing the header; the slide title sits on the left as **"Now: <title>"** and the three logos on the right. Monochromatic blue-and-white palette — conference-poster / journal-house feel. Typography: Calibri throughout.

- Built deck: [`templates/royal_blue/KCLNLP_RoyalBlue.pptx`](templates/royal_blue/KCLNLP_RoyalBlue.pptx)
- Same layouts as Tree Yellow: title (+ centered variant), section divider, content, two-column, thank-you / Q&A (+ centered variant).

Regenerate from source:

```bash
python templates/royal_blue/build.py
```

Planned template categories:

- **Conference / paper talk** — for presenting accepted papers at venues like ACL, EMNLP, NAACL.
- **Group meeting** — lightweight template for reading groups and internal updates.
- **Poster** — A0 poster template for conference poster sessions.
- **General outreach** — for keynotes, public talks, and lab introductions.

## Usage

1. Open the template `.pptx` in PowerPoint / Keynote / LibreOffice Impress.
2. Replace the placeholder content with your own, keeping the logo header intact.
3. Put the slide title in the cream header (not the body) so the body has room for content.
4. Use Calibri throughout; reserve the orange accent (`#D94A1C`) for the "Now:" label, rules, and small accents.

## Contributing

Contributions from lab members are welcome:

- Open a pull request with new templates or refinements.
- Keep fonts, colours, and the KCL NLP logo consistent with existing templates.
- Preview slides (PNG exports of representative pages) are encouraged for quick browsing.

## License

TBD.
