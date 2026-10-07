"""Checks on section 4 of the Story Report, the archetype timeline.

Data checks run on report.build(); the layout checks open the built page in
headless Chrome (skipped if Chrome isn't installed). Headless Chrome won't
make a window narrower than 500px, so the page is loaded in an iframe of
the exact width and measured from the host page.

Run: python -m unittest test_report_timeline
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
from io import StringIO
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report  # noqa: E402
import report_guard as g  # noqa: E402

CHROME = next((p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                           shutil.which("google-chrome") or "", shutil.which("chromium") or "")
               if p and os.path.exists(p)), None)
EXPECTED = {"cold": 83, "reviewed": 71}

_BUILT = {}


def built():
    if not _BUILT:
        with redirect_stdout(StringIO()):
            data, model, stats = report.build()
            _BUILT.update(data=data, model=model, stats=stats, page=report.page(data, model, stats))
    return _BUILT


def framing():
    """Every reader-facing framing line section 4 adds."""
    return ([report.TL_HEADING.format(n=report.TIMELINE_SECTION)]
            + [x.format(map=report.MAP_SECTION) for x in report.TL_INTRO]
            + list(report.TL_TEXT.values())
            + [x for x in report.NOT_MEASURED if "timeline" in x])


class TimelineData(unittest.TestCase):
    def test_mark_count_per_view(self):
        tl = built()["data"]["timeline"]
        self.assertEqual({v: len(tl[v]) for v in tl}, EXPECTED)

    def test_same_calls_as_the_map(self):
        d = built()["data"]
        for v in ("cold", "reviewed"):
            mapped = sorted((m[0], ch["name"], a) for ch in d["top"] + d["rest"]
                            for m in ch["marks"][v] if not m[2] for a in m[1])
            self.assertEqual(sorted((x["b"], x["c"], x["a"]) for x in d["timeline"][v]), mapped)

    def test_positions_within_pages_1_to_125(self):
        d = built()["data"]
        self.assertEqual(d["tlPages"], [1, 125])
        for v in ("cold", "reviewed"):
            for x in d["timeline"][v]:
                b = d["beats"][x["b"]]
                with self.subTest(view=v, beat=x["b"], character=x["c"]):
                    self.assertGreaterEqual(b["x"], 1)
                    self.assertLess(b["x"], 126)
                    self.assertTrue(all(1 <= p <= 125 for p in b["pages"]))
                    self.assertEqual(int(b["x"]), b["pages"][0], "a mark sits on its first line's page")

    def test_john_and_young_john_are_one_label(self):
        names = {x["c"] for v in ("cold", "reviewed") for x in built()["data"]["timeline"][v]}
        self.assertIn("JOHN", names)
        self.assertNotIn("YOUNG JOHN", names)
        self.assertNotIn("YOUNG CHEYENNE", names)

    def test_pole_only_in_human_reviewed_great_mother(self):
        tl = built()["data"]["timeline"]
        self.assertFalse([x for x in tl["cold"] if "pole" in x])
        self.assertFalse([x for x in tl["reviewed"] if "pole" in x and x["a"] != "Great Mother"])
        gm = [x for x in tl["reviewed"] if x["a"] == "Great Mother"]
        self.assertTrue(all("pole" in x for x in gm))
        self.assertEqual(sum(x["pole"] == "dark" for x in gm), 15)
        self.assertEqual(sum(x["pole"] is None for x in gm), 9)

    def test_mackie_140_11_pole_comes_from_the_author_ruling(self):
        poles = built()["stats"]["timeline"]["poles"]
        p = next(x for x in poles if x["b"] == "scene140_beat11" and x["c"] == "MACKIE")
        self.assertEqual((p["pole"], p["source"]), ("dark", "author ruling (Oct 6, 2026)"))
        rec = report.review_row("MACKIE", "scene140_beat11")
        self.assertEqual(rec["verdict"], "Great Mother + Persona (confirmed)", "the verdict text is unchanged")

    def test_one_approximate_position(self):
        approx = built()["stats"]["timeline"]["approx"]
        self.assertEqual([(x["b"], x["c"]) for x in approx], [("scene216_beat6", "TRUDY")])
        self.assertIn("One approximate position", built()["page"])


class PoleParser(unittest.TestCase):
    def rec(self, verdict, notes=""):
        row = f"| scene1_beat1 | {verdict} | {notes} | applied |"
        return {"file": "x", "verdict": verdict, "rulings": report.RULING_RE.findall(row)}

    def test_verdict(self):
        self.assertEqual(report.great_mother_pole(self.rec("Great Mother (confirmed, dark pole)")), ("dark", "verdict"))
        self.assertEqual(report.great_mother_pole(self.rec("Great Mother (confirmed)")), (None, None))

    def test_ruling_is_read_and_takes_precedence(self):
        r = self.rec("Great Mother (confirmed)", "Basis. Author ruling (Oct 6, 2026): Great Mother, dark pole.")
        self.assertEqual(report.great_mother_pole(r), ("dark", "author ruling (Oct 6, 2026)"))
        r = self.rec("Great Mother (confirmed, dark pole)", "Author ruling (Oct 7, 2026): Great Mother, light pole.")
        self.assertEqual(report.great_mother_pole(r), ("light", "author ruling (Oct 7, 2026)"))

    def test_ruling_on_another_archetype_is_ignored(self):
        r = self.rec("Great Mother (confirmed)", "Author ruling (Oct 6, 2026): Shadow, not a dark pole call.")
        self.assertEqual(report.great_mother_pole(r), (None, None))


class TimelinePage(unittest.TestCase):
    def test_section_order_and_number(self):
        page = built()["page"]
        i_map, i_tl = page.index('id="map-h"'), page.index('id="tl-h"')
        i_not = page.index('aria-label="What this report doesn\'t measure"')
        self.assertLess(i_map, i_tl)
        self.assertLess(i_tl, i_not)
        self.assertIn(">Section 4. Archetype Timeline</h2>", page)
        self.assertEqual(report.toggled_sections(), "Sections 2, 3 and 4")
        self.assertIn('data-sec="tl"', page)

    def test_framing_passes_the_checks(self):
        for s in framing():
            with self.subTest(s=s):
                report.check_plain("test", s)  # exits on a finding
                self.assertEqual([v for v in g.check_text(s, "text") if v.check in ("banned", "pipeline")], [])
                self.assertEqual(g.model_word_hits(s), [])
                self.assertNotRegex(s, r"\d+ (marks?|calls?|moments?|times)\b", "no counts in framing")

    def test_intro_is_the_approved_wording(self):
        # Author-approved 2026-10-06; the first line is the author's wording.
        self.assertEqual(report.TL_INTRO, [
            "Where each of The Big Seven is called across the script. Each lane is one archetype; each mark is a "
            "moment, placed at the page where it begins and labelled with the character.",
            "Tap or click a mark for the character, archetype and page, and a link to that character in the "
            "character map (section {map}).",
        ])
        page = built()["page"]
        for s in report.TL_INTRO:
            self.assertIn(f"<p>{report.e(s.format(map=report.MAP_SECTION))}</p>", page)

    def test_no_ai_read_text_in_the_timeline(self):
        js = report.JS
        tl = js[js.index("// --- section 4"):js.index("const RENDER")]
        for k in ("audience_perceived", "self_perceived", "D.ai", "emotion", "oneLine"):
            self.assertNotIn(k, tl)

    def test_hood_names_its_sources(self):
        page = built()["page"]
        hood = page[page.index('id="tl-h"'):page.index('aria-label="What this report doesn\'t measure"')]
        for s in ("first line", "Young John", "Author ruling", "not a stored value", "scene216_beat6"):
            self.assertIn(s, hood)


HOST_JS = r"""
const f = document.querySelector('iframe');
f.addEventListener('load', () => setTimeout(() => {
  const w = f.contentWindow, d = f.contentDocument, out = {};
  for (const v of ['cold', 'reviewed']) {
    d.querySelector(`.toggle[data-sec="tl"] button[data-v="${v}"]`).click();
    const tl = d.getElementById('tl'), de = d.documentElement;
    const outside = [...tl.querySelectorAll('.tlm, .tl-lab, .tl-vlab')].filter(el => {
      const r = el.getBoundingClientRect(); return r.left < -0.5 || r.right > w.innerWidth + 0.5; }).length;
    out[v] = {marks: tl.querySelectorAll('.tlm').length, hollow: tl.querySelectorAll('.tlm.hollow').length,
              layout: tl.dataset.layout, inner: w.innerWidth, client: de.clientWidth, scroll: de.scrollWidth,
              bodyScroll: d.body.scrollWidth, outside: outside};
  }
  const mk = d.querySelector('#tl .tlm[data-a="Great Mother"][data-c="MACKIE"]');
  mk.click();
  const pop = d.getElementById('tl-pop');
  out.pop = {open: pop.classList.contains('open'), text: pop.textContent};
  pop.querySelector('a').click();
  const sh = d.getElementById('sheet');
  out.sheet = {open: sh.classList.contains('open'), title: (sh.querySelector('h3') || {}).textContent || ''};
  document.getElementById('out').textContent = JSON.stringify(out);
}, 300));
"""


@unittest.skipUnless(CHROME, "no headless Chrome/Edge found")
class TimelineLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        with open(os.path.join(cls.tmp, "page.html"), "w", encoding="utf-8") as f:
            f.write(built()["page"])
        cls.results = {w: cls.measure(w) for w in (390, 1280)}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def measure(cls, width):
        host = os.path.join(cls.tmp, f"host{width}.html")
        with open(host, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><body style="margin:0"><pre id="out"></pre><iframe src="page.html" '
                    f'style="border:0;width:{width}px;height:844px"></iframe><script>{HOST_JS}</script></body>')
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                            f"--window-size={max(width, 500) + 40},900", "--virtual-time-budget=8000",
                            "--dump-dom", "file:///" + host.replace("\\", "/")],
                           capture_output=True, timeout=120, text=True, encoding="utf-8")
        m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
        if not m or not m.group(1).strip():
            raise AssertionError(f"no measurement at {width}px: {r.stderr[-400:]}")
        return json.loads(html.unescape(m.group(1)))

    def test_mark_count_per_view_in_the_browser(self):
        for w, res in self.results.items():
            for v, n in EXPECTED.items():
                with self.subTest(width=w, view=v):
                    self.assertEqual(res[v]["marks"], n)
            self.assertEqual(res["cold"]["hollow"], 0, "AI Output shows no pole")
            self.assertEqual(res["reviewed"]["hollow"], 9)

    def test_layout_by_width(self):
        self.assertEqual(self.results[390]["cold"]["inner"], 390)
        self.assertEqual(self.results[390]["cold"]["layout"], "narrow")
        self.assertEqual(self.results[1280]["cold"]["layout"], "wide")

    def test_no_horizontal_overflow_at_390px(self):
        for v in EXPECTED:
            res = self.results[390][v]
            with self.subTest(view=v):
                self.assertLessEqual(res["scroll"], res["client"])
                self.assertLessEqual(res["bodyScroll"], res["client"])
                self.assertEqual(res["outside"], 0, "every mark and label inside the viewport")

    def test_tap_shows_the_moment_and_links_to_the_map(self):
        for w, res in self.results.items():
            with self.subTest(width=w):
                self.assertTrue(res["pop"]["open"])
                self.assertIn("Mackie · Great Mother", res["pop"]["text"])
                self.assertIn("Page", res["pop"]["text"])
                self.assertIn("See Mackie in the character map (section 3)", res["pop"]["text"])
                self.assertNotIn("The AI", res["pop"]["text"])
                self.assertTrue(res["sheet"]["open"])
                self.assertIn("Mackie · Great Mother", res["sheet"]["title"])


if __name__ == "__main__":
    unittest.main()
