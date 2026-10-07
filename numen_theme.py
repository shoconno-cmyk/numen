"""
numen_theme.py -- the shared stylesheet (numen_theme.css) for a page
written to a given folder: the CSS text with its font URLs rewritten
relative to that folder. Every page builder (report.py, walkthrough.py,
demo_prototype/card_kit.py) inlines css(out_dir) ahead of its own CSS, so
fonts, color tokens and the AI / human review chips change in one place.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(ROOT, "numen_theme.css")
FONTS = os.path.join(ROOT, "fonts")
FONT_URL_RE = re.compile(r'url\("fonts/([^"]+)"\)')


def css(out_dir=ROOT):
    """numen_theme.css with font URLs relative to out_dir. Stops if a font
    file it names is missing."""
    with open(THEME, encoding="utf-8") as f:
        text = f.read()
    rel = os.path.relpath(FONTS, out_dir).replace(os.sep, "/")

    def fix(m):
        if not os.path.exists(os.path.join(FONTS, m.group(1))):
            raise SystemExit(f"ABORT: numen_theme.css names fonts/{m.group(1)}, which is missing")
        return f'url("{rel}/{m.group(1)}")'
    return FONT_URL_RE.sub(fix, text)


def font_files():
    """The font files the stylesheet loads."""
    with open(THEME, encoding="utf-8") as f:
        return FONT_URL_RE.findall(f.read())


HOME_TEXT = "Back to Main Page"


def home_button(out_dir=ROOT):
    """The "Back to Main Page" link for a public page written to out_dir:
    it points at the site's index.html (the repo root). Styled by .home-btn
    in numen_theme.css. Never on index.html itself or on a review page."""
    href = os.path.relpath(os.path.join(ROOT, "index.html"), out_dir).replace(os.sep, "/")
    return f'<a class="home-btn" href="{href}">{HOME_TEXT}</a>'
