"""Checks on the walkthrough page (walkthrough.py -> numen_walkthrough.html)
and the section 2 honesty fix in the Story Report.

The expected numbers below are fixed on purpose: if the data drifts, the
page's numbers change and these tests fail until someone looks.

Run: python -m unittest test_walkthrough
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report  # noqa: E402
import report_guard as g  # noqa: E402
import walkthrough as w  # noqa: E402
from test_report_timeline import CHROME, built as report_built  # noqa: E402

EXPECTED = {
    "printed_first": 1, "printed_last": 125, "lines": 6665, "scenes": 223, "beats": 460,
    "calls": 470, "kept": 57, "ai_calls": 82, "ordinary_cold": 0, "ordinary_reviewed": 19,
    "pass2_before": 196, "drafts": 524, "pass2_chars": 29, "min_beats": 3, "sections": 4, "cards": 4,
    "scream_page": 4, "scream_line": 198, "scream_pdf": 5, "scream_printed": 4, "holly_page": 2,
    "mackie_page": 84, "garbled_page": 123, "plot_facts": 3, "corrections": 847,
}
_B = {}


def page():
    if not _B:
        with redirect_stdout(StringIO()):
            _B["html"], _B["N"] = w.build()
            _B["excerpts"] = list(w.EXCERPTS)
    return _B


def visible():
    return g.all_visible_text(page()["html"])


class Numbers(unittest.TestCase):
    def test_numbers_have_not_drifted(self):
        self.assertEqual(page()["N"], EXPECTED)

    def test_each_shown_number_is_on_the_page(self):
        v = visible()
        for k in ("scenes", "beats", "calls", "kept", "ai_calls", "ordinary_reviewed", "pass2_before",
                  "drafts", "pass2_chars", "min_beats", "sections", "scream_page", "mackie_page", "garbled_page",
                  "plot_facts", "corrections", "lines", "cards"):
            self.assertRegex(v, rf"(?<![\d.]){EXPECTED[k]}(?![\d])", k)

    def test_the_figure_is_exact(self):
        self.assertIn("57 of the AI’s 82 archetype calls were kept as made.", visible())

    def test_kept_as_made_matches_the_accuracy_record(self):
        self.assertEqual(w.kept_as_made(w.load("model")), (57, 82))

    def test_framing_has_no_typed_digits(self):
        for t in w.framing_templates():
            self.assertNotRegex(re.sub(r"\{\w+\}", "", t), r"\d", t)

    def test_never_the_inflated_figure(self):
        self.assertNotIn("95.1", page()["html"])


class Excerpts(unittest.TestCase):
    def test_every_excerpt_is_word_for_word_in_its_file(self):
        ex = page()["excerpts"]
        self.assertGreater(len(ex), 20)
        self.assertEqual(w.verify_excerpts(ex), [])

    def test_every_excerpt_is_on_the_page(self):
        h = page()["html"]
        for _, t in page()["excerpts"]:
            self.assertIn(report.e(t), h)

    def test_a_changed_excerpt_fails(self):
        self.assertTrue(w.verify_excerpts([("full", "A SCREAM. A boy’s scream.")]))
        self.assertTrue(w.verify_excerpts([("calls", "an impish child")]))

    def test_threads(self):
        v = visible()
        for s in ("A SCREAM. A girl’s scream. Holly.", "Hey! Not fair!", "Trickster",
                  "Without warning, Mackie’s big powerful hand grabs John’s throat, squeezing.",
                  "Crime Drama / Thriller"):
            self.assertIn(s, v)


class Framing(unittest.TestCase):
    def test_opening(self):
        h = page()["html"]
        h1 = re.search(r"<h1>(.*?)</h1>", h, re.S).group(1)
        self.assertEqual(html.unescape(re.sub(r"<[^>]+>", "", h1)), w.TAGLINE)
        self.assertIn('<span class="wordmark">Numen</span>', h1)
        self.assertEqual(w.TAGLINE, "Numen: Archetype and Character-Arc Analysis for Screenplays")
        self.assertIn("Full of Grace", w.OPENING)
        self.assertIn("from the script’s PDF to its final Story Report", w.OPENING)

    def test_five_stages_in_order(self):
        self.assertEqual([s["title"] for s in w.STAGES], [
            "The Script Read", "Finding the Moments", "The AI Labels the Archetypes",
            "The AI Tracks Character Changes", "The Story Report"])
        self.assertEqual([s["steps"] for s in w.STAGES], [[1, 2], [3], [4], [6], [8, 9, 10]])
        self.assertEqual(len(w.STEPS), 10)

    def test_stage_one_goes_in(self):
        self.assertEqual(w.STAGES[0]["in"], "The script PDF.")

    def test_stage_four_says_it_plainly(self):
        s = w.STAGES[3]["plain"].format(**EXPECTED)
        self.assertIn("whole arc is in view", s)
        self.assertIn("human-reviewed archetype calls", s)

    def test_track_says_ai_only(self):
        self.assertIn("AI-only, with no human review", w.TRACK["lead"])
        self.assertIn("how close the AI currently gets", w.TRACK["lead"])

    def test_framing_passes_every_check(self):
        self.assertEqual(w.check(page()["html"], page()["N"]), [])

    def test_script_pdf_never_named_by_file(self):
        v = visible()
        self.assertNotIn(".pdf", v)
        self.assertNotRegex(v, r"(?i)a-?score")
        self.assertIn("the script PDF", v)

    def test_links(self):
        h = page()["html"]
        self.assertIn(f'href="{w.REPORT_HTML}"', h)
        for c in w.CARDS:
            self.assertIn(f'href="demo_prototype/{c}"', h)
            self.assertTrue(os.path.exists(os.path.join(ROOT, "demo_prototype", c)))

    def test_hood_holds_the_real_steps(self):
        h = page()["html"]
        hood = h[h.index("<details"):h.index("</details>")]
        for s in ("fog_full.txt", "fog_plot_facts_runner.py", "nothing in the report uses them",
                  "printed pages only", "YOUNG JOHN", "the human review track"):
            self.assertIn(s, hood)


class Section2Fix(unittest.TestCase):
    def test_banner(self):
        self.assertEqual(report_built()["data"]["text"]["banner_p2_cold"],
                         "AI Output: the AI's character-change judgments, unedited. "
                         "They were made after human review of its archetype calls.")

    def test_hood_line_and_its_numbers(self):
        po = report_built()["stats"]["pass2_order"]
        self.assertEqual((po["n"], po["first"], po["before"], po["partial"], po["complete"], po["drafts"]),
                         (196, "1fe11c8", "d294e1c", "e26724d", "8079f93", 524))
        self.assertIn("196 human corrections (corrections-log entries 1–196, commits <code>1fe11c8</code> to "
                      "<code>d294e1c</code>)", report_built()["page"])

    def test_banner_passes_the_checks(self):
        s = report_built()["data"]["text"]["banner_p2_cold"]
        report.check_plain("test", s)
        self.assertEqual([v for v in g.check_text(s, "text") if v.check in ("banned", "pipeline")], [])
        self.assertEqual(g.model_word_hits(s), [])


HOST_JS = r"""
const f = document.querySelector('iframe');
f.addEventListener('load', () => setTimeout(() => {
  const w = f.contentWindow, d = f.contentDocument, de = d.documentElement;
  d.querySelectorAll('details').forEach(x => x.open = true);
  const wide = [...d.querySelectorAll('body *')].filter(el => {
    const r = el.getBoundingClientRect(); return r.width && (r.left < -0.5 || r.right > w.innerWidth + 0.5); });
  document.getElementById('out').textContent = JSON.stringify({inner: w.innerWidth, client: de.clientWidth,
    scroll: de.scrollWidth, body: d.body.scrollWidth, outside: wide.slice(0, 5).map(e => e.tagName + '.' + e.className)});
}, 300));
"""


@unittest.skipUnless(CHROME, "no headless Chrome/Edge found")
class PhoneWidth(unittest.TestCase):
    def test_no_sideways_scroll_at_390px(self):
        tmp = tempfile.mkdtemp()
        try:
            with open(os.path.join(tmp, "page.html"), "w", encoding="utf-8") as f:
                f.write(page()["html"])
            host = os.path.join(tmp, "host.html")
            with open(host, "w", encoding="utf-8") as f:
                f.write('<!doctype html><body style="margin:0"><pre id="out"></pre><iframe src="page.html" '
                        f'style="border:0;width:390px;height:844px"></iframe><script>{HOST_JS}</script></body>')
            r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                                "--window-size=540,900", "--virtual-time-budget=6000", "--dump-dom",
                                "file:///" + host.replace("\\", "/")], capture_output=True, timeout=120,
                               text=True, encoding="utf-8")
            res = json.loads(html.unescape(re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S).group(1)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(res["inner"], 390)
        self.assertLessEqual(res["scroll"], res["client"])
        self.assertLessEqual(res["body"], res["client"])
        self.assertEqual(res["outside"], [])


if __name__ == "__main__":
    unittest.main()
