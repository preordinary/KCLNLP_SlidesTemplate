# KCLNLP_SlidesTemplate

PowerPoint templates for the **KCL NLP** research group, designed for consistent outreach and presentation of our research work (talks, posters, seminars, reading groups, etc.).

## Templates

### Tree Yellow Texture

A minimal 16:9 deck. A cream header band carries the slide title on the left (as **"Now: <title>"**) and the KCL, KCLNLP, and Alan Turing Institute logos on the right, separated from the body by a thick orange rule. Titles live in the header so the body has the full slide to breathe. Typography: **Georgia Bold** for titles, **Cambria** (Roman serif) for body.

- Built deck: [`templates/tree_yellow_texture/KCLNLP_TreeYellow.pptx`](templates/tree_yellow_texture/KCLNLP_TreeYellow.pptx)
- Layouts included: title, section divider, content (title + bullets), two-column (figure + text), thank-you / Q&A.

Regenerate from source:

```bash
pip install -r requirements.txt
python templates/tree_yellow_texture/build.py
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
4. Body text is Cambria; headings are Georgia Bold. Use the orange accent (`#D94A1C`) sparingly.

## Contributing

Contributions from lab members are welcome:

- Open a pull request with new templates or refinements.
- Keep fonts, colours, and the KCL NLP logo consistent with existing templates.
- Preview slides (PNG exports of representative pages) are encouraged for quick browsing.

## License

TBD.
