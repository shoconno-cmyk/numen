"""Checks on review mode (review_mode.py) across the Story Report, the
walkthrough and the four demo cards: each review page builds, locked text
is never editable, edits export with the page and each line's source, and
no public page carries review mode.

The browser checks run headless Chrome with a throwaway profile, so test
edits never reach the browser storage of your own review pages.

Run: python -m unittest test_review_mode
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
import review_mode  # noqa: E402
import walkthrough  # noqa: E402
from test_report_timeline import CHROME, built as report_built  # noqa: E402

CARDS = ["holly_scene3_beat2_card", "mackie_scene140_beat6_card", "pete_scene122_beat1_card",
         "protected_protector_card"]
PUBLIC = ["fog_story_report.html", "numen_walkthrough.html"] + [f"demo_prototype/{c}.html" for c in CARDS]
REVIEW = {"fog_story_report.html": "fog_story_report_review.html",
          "numen_walkthrough.html": "numen_walkthrough_review.html",
          **{f"demo_prototype/{c}.html": f"demo_prototype/{c}_review.html" for c in CARDS}}
PAGE_NAME = {"fog_story_report_review.html": "story report", "numen_walkthrough_review.html": "walkthrough",
             **{f"demo_prototype/{c}_review.html": f"card {c}" for c in CARDS}}
_BUILT = {}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def build_all():
    """Build every review page fresh (the report and walkthrough in process,
    the cards through their builder with --review)."""
    if not _BUILT:
        import report
        b = report_built()
        _BUILT["report"] = report.page(b["data"], b["model"], b["stats"], review=True)
        with redirect_stdout(StringIO()):
            _BUILT["walkthrough"] = walkthrough.build_review()
        r = subprocess.run([sys.executable, os.path.join(ROOT, "demo_prototype", "build_archetype_cards.py"), "--review"],
                           capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        _BUILT["cards_rc"], _BUILT["cards_out"] = r.returncode, r.stdout + r.stderr
        with open(os.path.join(ROOT, "fog_story_report_review.html"), "w", encoding="utf-8") as f:
            f.write(_BUILT["report"])
        with open(walkthrough.REVIEW_OUT, "w", encoding="utf-8") as f:
            f.write(_BUILT["walkthrough"])
    return _BUILT


class Builds(unittest.TestCase):
    def test_each_review_page_builds(self):
        b = build_all()
        self.assertEqual(b["cards_rc"], 0, b["cards_out"][-800:])
        for rel in REVIEW.values():
            with self.subTest(page=rel):
                page = read(rel)
                self.assertIn(review_mode.MARKER, page)
                self.assertIn(f'data-page="{PAGE_NAME[rel]}"', page)
                self.assertIn('id="rv-sources"', page)

    def test_one_implementation(self):
        for rel in ("report.py", "walkthrough.py", "demo_prototype/card_kit.py"):
            src = read(rel)
            with self.subTest(builder=rel):
                self.assertIn("review_mode.bar(", src)
                self.assertNotIn("localStorage", src)
                self.assertNotIn("contenteditable", src)

    def test_storage_keys_differ(self):
        build_all()
        keys = [re.search(r'data-store="([^"]+)"', read(rel)).group(1) for rel in REVIEW.values()]
        self.assertEqual(len(set(keys)), len(keys), keys)
        self.assertEqual(keys[0], "a-score-review-edits", "the report keeps its key, so saved edits survive")

    def test_sources_name_constants_and_lines(self):
        build_all()
        wt = json.loads(re.search(r'<script type="application/json" id="rv-sources">(.*?)</script>',
                                  read("numen_walkthrough_review.html"), re.S).group(1))
        self.assertRegex(wt[walkthrough.OPENING], r"^OPENING \(walkthrough\.py:\d+\)$")
        self.assertRegex(wt[walkthrough.STAGES[1]["note"]], r"^STAGES\[1\]\['note'\] \(walkthrough\.py:\d+\)$")
        card = json.loads(re.search(r'id="rv-sources">(.*?)</script>',
                                    read("demo_prototype/holly_scene3_beat2_card_review.html"), re.S).group(1))
        self.assertRegex(card["Human review"], r"^f\('section heading'\) \(build_archetype_cards\.py:\d+\)$")


class PublicPages(unittest.TestCase):
    def test_public_pages_have_no_review_marker(self):
        build_all()
        for rel in PUBLIC:
            page = read(rel)
            with self.subTest(page=rel):
                self.assertNotIn(review_mode.MARKER, page)
                self.assertNotIn("review-bar", page)
                self.assertNotIn("rv-sources", page)
                self.assertNotIn("_review.html", page, "a public page never links a review page")

    def test_public_builders_refuse_review_mode(self):
        with self.assertRaises(SystemExit):
            review_mode.assert_public("<div id='review-bar' data-mode='%s'></div>" % review_mode.MARKER, "test")
        review_mode.assert_public(walkthrough.build()[0], "walkthrough")

    def test_review_pages_are_git_ignored(self):
        build_all()
        r = subprocess.run(["git", "check-ignore", *REVIEW.values()], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(sorted(r.stdout.split()), sorted(REVIEW.values()))


HOST_JS = r"""
const frames = [...document.querySelectorAll('iframe')], out = {};
let left = frames.length;
frames.forEach(f => f.addEventListener('load', () => setTimeout(() => {
  const w = f.contentWindow, d = f.contentDocument;
  const sw = d.getElementById('rv-on'); sw.checked = true; sw.dispatchEvent(new Event('change'));
  const LOCK = '[data-ai], [data-locked], [data-verbatim]';
  const ed = [...d.querySelectorAll('[contenteditable="true"]')];
  const bad = ed.filter(el => el.closest(LOCK) || el.querySelector(LOCK)).map(el => el.outerHTML.slice(0, 120));
  const locked = d.querySelectorAll(LOCK).length;
  // One edit, then the export.
  const target = ed.find(el => el.matches(f.dataset.target)) || ed[0];
  target.textContent = target.textContent + ' EDITED';
  target.dispatchEvent(new Event('input', {bubbles: true}));
  d.getElementById('rv-copy').click();
  out[f.dataset.k] = {editable: ed.length, locked: locked, bad: bad, export: d.querySelector('#review-bar textarea').value};
  if (--left === 0) document.getElementById('out').textContent = JSON.stringify(out);
}, 500)));
"""
TARGET = {"fog_story_report_review.html": "#why-h", "numen_walkthrough_review.html": "header.wt-head p",
          **{f"demo_prototype/{c}_review.html": "dt" for c in CARDS}}


@unittest.skipUnless(CHROME, "no headless Chrome/Edge found")
class InTheBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_all()
        cls.tmp = tempfile.mkdtemp()
        frames = "".join(
            f'<iframe data-k="{rel}" data-target="{TARGET[rel]}" src="file:///{os.path.join(ROOT, rel).replace(os.sep, "/")}" '
            f'style="border:0;width:1200px;height:800px"></iframe>' for rel in REVIEW.values())
        host = os.path.join(cls.tmp, "host.html")
        with open(host, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><body><pre id="out"></pre>{frames}<script>{HOST_JS}</script></body>')
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                            f"--user-data-dir={os.path.join(cls.tmp, 'profile')}", "--window-size=1300,900",
                            "--virtual-time-budget=15000", "--dump-dom", "file:///" + host.replace("\\", "/")],
                           capture_output=True, timeout=240, text=True, encoding="utf-8")
        m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
        cls.res = json.loads(html.unescape(m.group(1))) if m and m.group(1).strip() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_measured_every_page(self):
        self.assertIsNotNone(self.res)
        self.assertEqual(set(self.res), set(REVIEW.values()))

    def test_locked_text_is_not_editable(self):
        for rel, x in self.res.items():
            with self.subTest(page=rel):
                self.assertGreater(x["editable"], 3)
                self.assertGreater(x["locked"], 0)
                self.assertEqual(x["bad"], [])

    def test_export_names_page_and_source(self):
        for rel, x in self.res.items():
            with self.subTest(page=rel):
                self.assertTrue(x["export"].startswith(f"Numen review edits ({PAGE_NAME[rel]}): 1 change(s)\n"),
                                x["export"][:120])
                self.assertRegex(x["export"], r"\n   Source: .+\n   Original: .+\n   New: .+ EDITED\n")
        self.assertRegex(self.res["numen_walkthrough_review.html"]["export"],
                         r"Source: OPENING \(walkthrough\.py:\d+\)")
        self.assertRegex(self.res["fog_story_report_review.html"]["export"], r"Source: WHY_HEADING \(report\.py:\d+\)")


if __name__ == "__main__":
    unittest.main()
