"""
Shared pieces for the demo cards: rendered Full of Grace PDF pages with
highlighted lines, the card stylesheet, and the checks every card runs.

Quote-verification rule (CLAUDE.md): every highlighted PDF line is matched
against its fog_full.txt line before drawing, and any mismatch aborts the
build. Script text on a card is either a rendered PDF page or pulled from
fog_full.txt by line range; nothing is typed in by hand.
"""
import base64
import html
import io
import os
import re
import sys

import pdfplumber
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import report_guard  # noqa: E402
import numen_theme  # noqa: E402
import review_mode  # noqa: E402

OUT_DIR = os.path.join(ROOT, "demo_prototype")
PDF_PATH = os.path.join(ROOT, "full_of_grace.pdf")
TXT_PATH = os.path.join(ROOT, "fog_full.txt")

DPI = 216  # 3x the PDF's 72pt grid
SCALE = DPI / 72

COLORS = {  # highlight fill on the page image, and the matching CSS swatch
    "beat": ((240, 178, 50, 70), "rgba(240,178,50,.45)"),     # amber: the moment
    "beat2": ((90, 140, 230, 62), "rgba(90,140,230,.40)"),    # blue: a second moment
    "context": ((150, 150, 150, 48), "rgba(150,150,150,.35)"),  # grey: lead-in, not part of the moment
}

e = html.escape
fog = open(TXT_PATH, encoding="utf-8").read().split("\n")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def fog_lines(a, b):
    """(line number, normalized text) for the non-blank fog_full.txt lines a..b."""
    return [(i, norm(fog[i - 1])) for i in range(a, b + 1) if fog[i - 1].strip()]


def locate(pdf, pdf_pages, a, b):
    """Find fog_full.txt lines a..b on the given PDF pages, in order, as one
    unbroken run per page. Returns {pdf page: [(fog line, pdf line dict)]}.
    Aborts if any line can't be matched word for word."""
    want, k, found = fog_lines(a, b), 0, {}
    for pno in pdf_pages:
        if k == len(want):
            break
        lines = pdf.pages[pno - 1].dedupe_chars().extract_text_lines()
        texts = [norm(l["text"]) for l in lines]
        best = None
        for s in range(len(texts)):
            j = 0
            while s + j < len(texts) and k + j < len(want) and texts[s + j] == want[k + j][1]:
                j += 1
            if j and (best is None or j > best[1]):
                best = (s, j)
        if best is None:
            if k:
                sys.exit(f"ABORT: fog_full.txt {want[k][0]} not found on PDF page {pno}")
            continue
        s, j = best
        if not k and k + j < len(want) and s + j != len(texts):
            continue   # a stray partial match (e.g. a bare cue) before the lines begin
        if k + j < len(want) and s + j != len(texts):
            sys.exit(f"ABORT: PDF page {pno}: fog_full.txt {want[k + j][0]} {want[k + j][1]!r} "
                     f"!= PDF {texts[s + j]!r}")
        found[pno] = [(want[k + i][0], lines[s + i]) for i in range(j)]
        k += j
    if k < len(want):
        sys.exit(f"ABORT: fog_full.txt {want[k][0]} {want[k][1]!r} not found on PDF pages {pdf_pages}")
    return found


def render_pages(pdf_pages, groups):
    """groups: [(color key, first fog line, last fog line)]. Every line is
    verified against the PDF before it is drawn. Returns page dicts."""
    pdf = pdfplumber.open(PDF_PATH)
    boxes = {p: [] for p in pdf_pages}
    for key, a, b in groups:
        for pno, hits in locate(pdf, pdf_pages, a, b).items():
            for n, l in hits:
                print(f"  verified  PDF p.{pno}  fog_full.txt {n}: {norm(l['text'])}")
                if is_page_number(l):
                    # Verified like every line, but a script page-number line is
                    # never highlighted, even inside a moment's line range.
                    print(f"  not highlighted (page number): PDF p.{pno} {norm(l['text'])}")
                    continue
                boxes[pno].append((key, l))
    out = []
    for pno in pdf_pages:
        page = pdf.pages[pno - 1].dedupe_chars()
        base = page.to_image(resolution=DPI).original.convert("RGBA")
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for key, l in boxes[pno]:
            box = [(l["x0"] - 3) * SCALE, (l["top"] - 1.5) * SCALE,
                   (l["x1"] + 3) * SCALE, (l["bottom"] + 0.5) * SCALE]
            draw.rounded_rectangle(box, radius=3 * SCALE, fill=COLORS[key][0])
        img = Image.alpha_composite(base, overlay).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        printed = printed_number(pdf, pno)
        out.append({"pdf": pno, "printed": printed, "size": img.size,
                    "b64": base64.b64encode(buf.getvalue()).decode("ascii")})
    return out


def is_page_number(line):
    """The script's "N." page-number header at the top of a PDF page."""
    return bool(re.fullmatch(r"\d+\.", norm(line["text"]))) and line["top"] < 100


def printed_number(pdf, pdf_no):
    """The script's own page number, read from the page itself: the "N."
    header line at the top of that PDF page. Captions use this, never a typed
    or computed number (author approval 2026-10-06, STORY_REPORT_SPEC.md)."""
    lines = pdf.pages[pdf_no - 1].dedupe_chars().extract_text_lines()
    nums = [l for l in lines if is_page_number(l)]
    if len(nums) != 1:
        sys.exit(f"ABORT: PDF page {pdf_no}: expected one page-number header, found {len(nums)}")
    return int(norm(nums[0]["text"])[:-1])


def pages_html(pages, uid):
    return "\n".join(
        f'''<figure class="page" data-pdf-page="{p["pdf"]}">
  <button class="zoom" data-src="{uid}p{p["pdf"]}" aria-label="Enlarge script page {p["printed"]}">
    <img id="{uid}p{p["pdf"]}" src="data:image/png;base64,{p["b64"]}" width="{p["size"][0]}" height="{p["size"][1]}"
         alt="Full of Grace, script page {p["printed"]}, with highlighted lines">
  </button>
  <figcaption>Full of Grace, page {p["printed"]}</figcaption>
</figure>''' for p in pages)


# --- review notes ------------------------------------------------------------

INTERNAL_RE = re.compile(r"`|\b[a-z]+_[a-z_]+\b|\bProvenance\b|\bfinding \d")


def note_sentences(note):
    """Split a review note into sentences, never inside quotation marks or
    parentheses. Text is not changed: the pieces join back to the note."""
    out, start, quote, depth = [], 0, False, 0
    for i, ch in enumerate(note):
        if ch == '"':
            quote = not quote
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch in ".!?" and not quote and depth == 0 and (i + 1 == len(note) or note[i + 1] == " "):
            out.append(note[start:i + 1].strip())
            start = i + 1
    if note[start:].strip():
        out.append(note[start:].strip())
    assert " ".join(out) == re.sub(r"\s+", " ", note).strip(), "note split changed the text"
    return out


def split_note(note):
    """(reader sentences, internal bookkeeping sentences), both verbatim."""
    s = note_sentences(note)
    return [x for x in s if not INTERNAL_RE.search(x)], [x for x in s if INTERNAL_RE.search(x)]


def verify_note_quotes(where, note):
    """Every quotation in a review note must be in fog_full.txt word for word."""
    src = report_guard.script_source()
    for _, _, q in report_guard.quoted_spans(note):
        if not report_guard._quote_found(q, src):
            sys.exit(f"ABORT: {where}: quote {q!r} is not verbatim in fog_full.txt")
        print(f"  quote verified ({where}): {q[:70]!r}")


# --- framing checks ------------------------------------------------------------

LOCKED = "\u27e8locked\u27e9"   # placeholder for a term taken from locked AI text


def check_framing(lines, locked_text="", locked_terms=()):
    """Framing text written for the cards (titles, captions, labels) must pass
    the report's checks: no pipeline terms or grading words (report.py), and
    report_guard's report-voice checks (praise, critique, verdict words,
    directives, citations, quotes).

    locked_terms: terms that belong to locked AI text shown verbatim on the
    card (e.g. a scene ID inside the model's stored claim). A framing line
    may name one when explaining it; the term is masked before the checks,
    but only if it really occurs in locked_text, so the exemption can't
    cover a term the framing introduced on its own."""
    import report
    for t in locked_terms:
        if t not in locked_text:
            sys.exit(f"ABORT: locked term {t!r} is not in the locked AI text")
    for where, s in lines:
        for t in locked_terms:
            s = s.replace(t, LOCKED)
        report.check_plain(where, s)
        v = report_guard.check_text(s, "summary")
        if v:
            sys.exit(f"ABORT: framing line {where!r} {s!r} fails report_guard: {[str(x) for x in v]}")
    print(f"framing: {len(lines)} lines pass report.check_plain and report_guard (summary)")


def check_card(path, required=(), forbidden_visible=(r"\breasoning\b", r"\brationale\b"),
               framing_forbidden=(r"\bmodel\b",)):
    """A built card: no old product name, no 'reasoning'/'rationale' labels in
    visible text, every required label present, and no "model" in framing
    (reader-facing text says "AI"; elements marked data-verbatim, which hold
    locked AI text or the author's verbatim review text, are left out)."""
    page = open(path, encoding="utf-8").read()
    hits = report_guard.old_name_hits(page)
    if hits:
        sys.exit(f"ABORT: {os.path.basename(path)}: old name in visible text: {hits}")
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", page.split("<body>", 1)[-1], flags=re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", body))
    for pat in forbidden_visible:
        if re.search(pat, visible, re.I):
            sys.exit(f"ABORT: {os.path.basename(path)}: visible text contains {pat!r}")
    framing = re.sub(r"<(\w+)[^>]*\bdata-verbatim\b[^>]*>.*?</\1>", " ", body, flags=re.S)
    framing = html.unescape(re.sub(r"<[^>]+>", " ", framing))
    for pat in framing_forbidden:
        m = re.search(pat, framing, re.I)
        if m:
            sys.exit(f"ABORT: {os.path.basename(path)}: framing contains {pat!r}: "
                     f"{framing[max(0, m.start() - 60):m.end() + 40]!r}")
    for label in required:
        if label not in visible:
            sys.exit(f"ABORT: {os.path.basename(path)}: label {label!r} missing")
    print(f"checked {os.path.basename(path)}: no old name, no reasoning/rationale label, no 'model' in framing, "
          f"{len(required)} required labels present")


# --- page shell -------------------------------------------------------------------

# Fonts and color tokens come from numen_theme.css (shared), inlined ahead of
# this; only the page-highlight swatches (COLORS) are card-specific.
CSS = """
:root { --beat: rgba(240,178,50,.45); --beat2: rgba(90,140,230,.40); --context: rgba(150,150,150,.35); }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.55 var(--font-body); }
header.top { max-width: 1240px; margin: 0 auto; padding: 32px 16px 0; }
header.top h1 { font-size: 28px; line-height: 1.25; font-weight: 500; margin: 0 0 6px; }
header.top p { margin: 0; color: var(--muted); font-size: 15px; max-width: 760px; }
.card { max-width: 1240px; margin: 0 auto; padding: 24px 16px 32px;
  display: grid; grid-template-columns: minmax(0, 1fr) 400px; gap: 36px; }
.panel-label { grid-column: 1 / -1; font-family: var(--font-body); font-size: 13px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); font-weight: 650; border-bottom: 1px solid var(--rule); padding-bottom: 6px; margin: 0; }
.pages { display: flex; flex-direction: column; gap: 22px; }
.page { margin: 0; }
.zoom { all: unset; display: block; cursor: zoom-in; border-radius: 2px; box-shadow: var(--shadow); }
.zoom:focus-visible { outline: 2px solid var(--muted); outline-offset: 3px; }
.page img { display: block; width: 100%; height: auto; background: #fff; }
.page figcaption { font-size: 12px; color: var(--muted); margin-top: 6px; text-align: right; }
aside { display: flex; flex-direction: column; gap: 24px; }
.who { font-size: 18px; font-weight: 650; margin: 0; }
.legend { display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: var(--muted); }
.sw { display: inline-block; width: 22px; height: 11px; border-radius: 3px; margin-right: 8px; vertical-align: -1px; }
section h2 { font-family: var(--font-body); font-size: 12px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); font-weight: 500; margin: 0 0 8px; }
section.claim h2, section.verdict h2 { margin: 0 0 10px; }
.value { font: 500 17px/1.3 var(--font-body); margin-bottom: 10px; }
.claim .value { color: var(--accent); } .verdict .value { color: var(--ink); }
dl.fields { margin: 0; display: grid; grid-template-columns: 9.5em 1fr; gap: 6px 10px; font-size: 14px; }
dl.fields dt { color: var(--muted); font-size: 12.5px; padding-top: 1px; }
dl.fields dd { margin: 0; }
.note { margin: 8px 0 0; padding-left: 12px; border-left: 2px solid var(--rule); }
/* Review outcome, gray (human review): outlined when upheld, filled when overturned. */
.badge { border: 1px solid var(--human-rule); color: var(--ink); border-radius: 6px;
  padding: 10px 12px; font-weight: 600; font-size: 15px; }
.badge.changed { background: var(--human-chip-bg); border-color: var(--human-chip-bg); color: var(--human-chip-ink); }
.author-label { color: var(--ink); font-weight: 600; margin-top: 14px; }
.author-note { border-left-color: var(--ink); }
ul.note { padding-left: 28px; } ul.note li { margin-bottom: 8px; }
.basis { font-size: 13.5px; color: var(--muted); margin: 10px 0 0; }
.link { grid-column: 1 / -1; font-size: 14px; margin: 0; }
.link a { color: inherit; }
.moment { display: flex; flex-direction: column; gap: 18px; padding-bottom: 22px; border-bottom: 1px solid var(--rule); }
.moment:last-of-type { border-bottom: 0; }
details { border-top: 1px solid var(--rule); padding-top: 14px; }
summary { cursor: pointer; font-size: 13px; font-weight: 600; color: var(--muted); }
summary:focus-visible { outline: 2px solid var(--muted); outline-offset: 3px; }
.hood { display: flex; flex-direction: column; gap: 14px; margin-top: 12px; font-size: 13px; }
.hood p { margin: 0; }
.hood .small { font-size: 12px; color: var(--muted); }
footer { max-width: 1240px; margin: 0 auto; padding: 12px 16px 40px; font-size: 12px; color: var(--muted);
  border-top: 1px solid var(--rule); }
dialog { padding: 0; border: 0; max-width: 100vw; max-height: 100vh; width: 100vw; height: 100vh;
  background: rgba(20,19,18,.92); }
dialog::backdrop { background: transparent; }
dialog .wrap { width: 100%; height: 100%; overflow: auto; cursor: zoom-out; }
dialog img { display: block; margin: 0 auto; width: min(1836px, 100%); height: auto; }
@media (max-width: 860px) {
  .card { grid-template-columns: minmax(0, 1fr); gap: 28px; padding-top: 20px; }
  dl.fields { grid-template-columns: 1fr; }
}
"""

SCRIPT = """
const box = document.getElementById("lightbox"), big = box.querySelector("img");
document.querySelectorAll(".zoom").forEach(b => b.addEventListener("click", () => {
  const src = document.getElementById(b.dataset.src);
  big.src = src.src; big.alt = src.alt; box.showModal();
}));
box.addEventListener("click", () => box.close());
"""


# Review mode (local only): the shared implementation in review_mode.py.
REVIEW_CAND = "h1, h2, p, li, dt, figcaption, .badge"
REVIEW_SKIP = "button, #review-bar, a, .who, dialog, summary, footer, .zoom"


def page_shell(title, body, review=None):
    """A card page. review: None for the public page, or
    {"page", "store", "sources"} for its local review page."""
    rv_css = review_mode.CSS if review else ""
    rv_bar = (review_mode.bar(review["page"], review["store"], REVIEW_CAND, REVIEW_SKIP, review["sources"],
                              "not in the source map: search demo_prototype/build_archetype_cards.py "
                              "for the original text") if review else "")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<style>{numen_theme.css(OUT_DIR)}{CSS}{rv_css}</style>
</head>
<body>
{body}
<footer>Tap a page to enlarge it.</footer>
{"" if review else numen_theme.home_button(OUT_DIR)}
<dialog id="lightbox" aria-label="Enlarged script page">
  <div class="wrap"><img alt=""></div>
</dialog>
<script>{SCRIPT}</script>
{rv_bar}
</body>
</html>
'''
