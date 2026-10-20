"""
trailer.py -- builds trailer.html, the Numen site's trailer page, in the
shared design (numen_theme.css: same tokens, fonts, light and dark themes),
with the wordmark and tagline at the top as on the walkthrough.

The video is numen_trailer.mp4 (repo root), shown with native controls at
full content width in a 16:9 box. A poster frame is used only if
numen_trailer_poster.jpg exists (ffmpeg, about 2 seconds in: the title
card); without it the page has no poster. The build stops if the video is
missing or over GitHub's 100 MB file limit.

No API call. The page's text passes the "model" check, the old-name check
and report_guard's final scan.

Run from the repo root:  python trailer.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report  # noqa: E402
import report_guard  # noqa: E402
import numen_theme  # noqa: E402
import walkthrough  # noqa: E402

OUT = os.path.join(ROOT, "trailer.html")
VIDEO = "numen_trailer.mp4"
POSTER = "numen_trailer_poster.jpg"
# Media fragment: browsers show the frame at 2 seconds (the title card) as the preview.
START = "#t=2"
MAX_BYTES = 100 * 1024 * 1024   # GitHub's per-file limit
TITLE = "Watch the Trailer"
LINE = "Numen in about a minute: one screenplay, from PDF to Story Report."
WALKTHROUGH_HTML = "numen_walkthrough.html"
WALKTHROUGH_LINK = "The Walkthrough: From PDF to Story Report"   # as on index.html

CSS = r"""
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.6 var(--font-body); }
main { max-width: 760px; margin: 0 auto; padding: 40px 16px 64px; }
.tr-head { margin: 8px 0 20px; }
.tr-head h1 { font-size: 30px; margin: 0 0 6px; }
.tr-head p.tagline { margin: 0 0 20px; color: var(--muted); }
.tr-head h2 { font-size: 24px; margin: 0; }
.video { display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; background: #000;
  border-radius: 6px; }
.tr-line { margin: 14px 0 8px; }
a { color: var(--ink); text-underline-offset: 2px; }
"""


def video_bytes():
    path = os.path.join(ROOT, VIDEO)
    if not os.path.exists(path):
        sys.exit(f"ABORT: {VIDEO} is missing")
    n = os.path.getsize(path)
    if n > MAX_BYTES:
        sys.exit(f"ABORT: {VIDEO} is {n / 1e6:.1f} MB, over GitHub's 100 MB file limit")
    return n


def page():
    video_bytes()
    poster = f' poster="{POSTER}"' if os.path.exists(os.path.join(ROOT, POSTER)) else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numen Trailer</title>
<style>{numen_theme.css(ROOT)}{CSS}</style></head>
<body><main>
<header class="tr-head"><h1><span class="wordmark">{report.e(walkthrough.NAME)}</span></h1><p class="tagline">{report.e(walkthrough.TAGLINE)}</p>
<h2>{report.e(TITLE)}</h2></header>
<video class="video" controls playsinline preload="metadata"{poster}>
<source src="{VIDEO}{START}" type="video/mp4">
</video>
<p class="tr-line">{report.e(LINE)}</p>
<p><a href="{WALKTHROUGH_HTML}">{report.e(WALKTHROUGH_LINK)}</a></p>
</main>
{numen_theme.home_button(ROOT)}
</body></html>
"""


def check(html_out):
    """The build's checks; returns a list of problems (empty = pass)."""
    bad = [f"final scan: {x}" for x in report_guard.final_scan(html_out)]
    bad += [f"model word: {h}" for h in report_guard.model_word_hits(report_guard.all_visible_text(html_out))]
    bad += [f"old name: {h}" for h in report_guard.old_name_hits(html_out)]
    return bad


def main():
    html_out = page()
    bad = check(html_out)
    if bad:
        for b in bad:
            print("  ", b)
        sys.exit(f"ABORT: {len(bad)} problem(s); page not written")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"checks pass; video {video_bytes() / 1e6:.1f} MB")
    print(f"wrote {os.path.basename(OUT)} ({os.path.getsize(OUT) // 1024} KB)")


if __name__ == "__main__":
    main()
