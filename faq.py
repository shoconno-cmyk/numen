"""
faq.py -- builds faq.html, the Numen site's Frequently Asked Questions page,
in the shared design (numen_theme.css: same tokens, fonts, light and dark
themes), with the wordmark and tagline at the top as on the walkthrough.

Deterministic: no API call, no generated prose. The questions and answers
are the author's text (2026-10-20), shown exactly. The one figure ("57 of
82") is computed from the data at build time with walkthrough.kept_as_made,
the same count the walkthrough shows; the text holds no typed digits.

These answers deny judgment, so they use words the report's lists catch
("good"). Every Q&A string is on the approved static list (APPROVED) and
exempt from the banned and grading word checks; the pipeline-term check,
the "model" check and the old-name check still apply to all of it.

Run from the repo root:  python faq.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report  # noqa: E402
import report_guard  # noqa: E402
import numen_theme  # noqa: E402
import walkthrough  # noqa: E402

OUT = os.path.join(ROOT, "faq.html")
TITLE = "Frequently Asked Questions"
LINKEDIN = "https://www.linkedin.com/in/shoconno"
# Link text in an answer -> its URL (the first occurrence is linked).
LINKS = {"LinkedIn": LINKEDIN}

# --- the author's text (2026-10-20), exactly ----------------------------------------
QA = [
    ("Why archetypes? Why The Big Seven and Jung, and not just a reader's coverage?",
     "Numen is designed to complement traditional coverage, not replace it. Jungian archetypes and arc "
     "analysis offer a unique lens on how a story is built and how it moves. Down the road, the goal is for "
     "Numen to work throughout the development process, tracking each draft and how its characters evolve."),
    ("Does Numen say whether a script is good?",
     "No. It shows where archetypes appear and how characters change, with evidence. Whether that makes a "
     "good story is for the people reading it to decide."),
    ("Does a high archetype count mean my script will be a hit?",
     "No. Archetypes are a lens on a script, not a predictor of box office or reviews."),
    ("Why not structure, pacing or coverage?",
     "Other tools already do those well. Numen focuses on something they don't cover: archetypes, moment by "
     "moment."),
    ("How accurate is it?",
     "On the demo script, {kept} of the AI's {ai_calls} archetype calls held up on human review. The Story "
     "Report shows the AI's output and the human-reviewed version side by side, so you can compare them "
     "yourself."),
    ("Which AI does it use?",
     "Claude, made by Anthropic. The pipeline is built so the AI can be swapped, including for one that runs "
     "on a studio's own machines."),
    ("Can I run it on my own script?",
     "Not yet on your own. It's a working prototype shown on one script. Get in touch through LinkedIn for "
     "a read."),
]


def numbers():
    kept, ai_calls = walkthrough.kept_as_made(walkthrough.load("model"))
    return {"kept": kept, "ai_calls": ai_calls}


def filled(N):
    """[(question, answer)] as shown."""
    return [(q, a.format(**N)) for q, a in QA]


def approved(N):
    """Approved static strings (author, 2026-10-20): every question and
    answer, whole and sentence by sentence (the final scan checks the page
    one sentence at a time)."""
    out = set()
    for q, a in filled(N):
        out |= {q, a, *report_guard.sentences(q), *report_guard.sentences(a)}
    return out


CSS = r"""
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.6 var(--font-body); }
main { max-width: 680px; margin: 0 auto; padding: 40px 16px 64px; }
.faq-head { margin: 8px 0 28px; }
.faq-head h1 { font-size: 30px; margin: 0 0 6px; }
.faq-head p.tagline { margin: 0 0 20px; color: var(--muted); }
.faq-head h2 { font-size: 24px; margin: 0; }
.faq { margin: 0; }
.faq dt { font-weight: 600; margin: 0 0 4px; }
.faq dd { margin: 0 0 22px; overflow-wrap: break-word; }
a { color: var(--ink); text-underline-offset: 2px; }
"""


def answer_html(a):
    out = report.e(a)
    for text, url in LINKS.items():
        out = out.replace(report.e(text), f'<a href="{report.e(url)}">{report.e(text)}</a>', 1)
    return out


def page(N):
    items = "\n".join(f"<dt>{report.e(q)}</dt>\n<dd>{answer_html(a)}</dd>" for q, a in filled(N))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numen FAQ</title>
<style>{numen_theme.css(ROOT)}{CSS}</style></head>
<body><main>
<header class="faq-head"><h1><span class="wordmark">{report.e(walkthrough.NAME)}</span></h1><p class="tagline">{report.e(walkthrough.TAGLINE)}</p>
<h2>{report.e(TITLE)}</h2></header>
<dl class="faq">
{items}
</dl>
</main>
{numen_theme.home_button(ROOT)}
</body></html>
"""


def check(html_out, N):
    """The build's checks; returns a list of problems (empty = pass)."""
    bad = []
    for _, a in QA:
        if re.search(r"\d", re.sub(r"\{\w+\}", "", a)):
            bad.append(f"typed digit in an answer: {a!r}")
    ok = approved(N)
    for s in [TITLE, *(x for qa in filled(N) for x in qa)]:
        graded = s
        for a in sorted(ok, key=len, reverse=True):
            graded = graded.replace(a, " ")
        for pat in report.FORBIDDEN:
            if re.search(pat, s, re.I):
                bad.append(f"report word check {pat!r}: {s!r}")
        for pat in report.GRADING:
            if re.search(pat, graded, re.I):
                bad.append(f"report grading check {pat!r}: {s!r}")
        bad += [f"model: {s!r}" for _ in report_guard.model_word_hits(s)]
    bad += [f"final scan: {x}" for x in report_guard.final_scan(html_out, [], ok)]
    bad += [f"model word: {h}" for h in report_guard.model_word_hits(report_guard.all_visible_text(html_out))]
    bad += [f"old name: {h}" for h in report_guard.old_name_hits(html_out)]
    return bad


def build():
    N = numbers()
    return page(N), N


def main():
    html_out, N = build()
    bad = check(html_out, N)
    if bad:
        for b in bad:
            print("  ", b)
        sys.exit(f"ABORT: {len(bad)} problem(s); page not written")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"checks pass; numbers: {N}")
    print(f"wrote {os.path.basename(OUT)} ({os.path.getsize(OUT) // 1024} KB)")


if __name__ == "__main__":
    main()
