"""Checks on the shared type and color system (numen_theme.css, fonts/):
the Story Report, the walkthrough and all four demo cards use the same
stylesheet, the bundled fonts load in a real browser, and nothing asks
Google Fonts for anything.

Run: python -m unittest test_theme
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

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import numen_theme  # noqa: E402
from test_report_timeline import CHROME  # noqa: E402

PAGES = {
    "fog_story_report.html": ROOT,
    "numen_walkthrough.html": ROOT,
    **{f"demo_prototype/{c}": os.path.join(ROOT, "demo_prototype") for c in (
        "holly_scene3_beat2_card.html", "mackie_scene140_beat6_card.html",
        "pete_scene122_beat1_card.html", "protected_protector_card.html")},
}
FONTS = {"fraunces-latin-400-normal.woff2": "Fraunces-OFL.txt", "fraunces-latin-500-normal.woff2": "Fraunces-OFL.txt",
         "inter-latin-400-normal.woff2": "Inter-OFL.txt", "inter-latin-500-normal.woff2": "Inter-OFL.txt",
         "inter-latin-600-normal.woff2": "Inter-OFL.txt",
         "courier-prime-latin-400-normal.woff2": "CourierPrime-OFL.txt"}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class Fonts(unittest.TestCase):
    def test_font_files_are_woff2_with_licenses(self):
        self.assertEqual(sorted(numen_theme.font_files()), sorted(FONTS))
        for font, lic in FONTS.items():
            with open(os.path.join(ROOT, "fonts", font), "rb") as f:
                self.assertEqual(f.read(4), b"wOF2", font)
            text = read(f"fonts/{lic}")
            self.assertIn("SIL OPEN FONT LICENSE Version 1.1", text)
            self.assertIn("Copyright", text)

    def test_only_the_bundled_weights(self):
        faces = re.findall(r'font-family: "([^"]+)"; font-style: normal; font-weight: (\d+)', read("numen_theme.css"))
        self.assertEqual(sorted(faces), sorted([("Fraunces", "400"), ("Fraunces", "500"), ("Inter", "400"),
                                                ("Inter", "500"), ("Inter", "600"), ("Courier Prime", "400")]))


class SharedStylesheet(unittest.TestCase):
    def test_every_page_inlines_the_same_theme(self):
        for rel, out_dir in PAGES.items():
            with self.subTest(page=rel):
                self.assertIn(numen_theme.css(out_dir), read(rel))

    def test_font_urls_resolve_from_each_page(self):
        for rel, out_dir in PAGES.items():
            for url in re.findall(r'url\("([^"]+\.woff2)"\)', read(rel)):
                with self.subTest(page=rel, url=url):
                    self.assertTrue(os.path.exists(os.path.normpath(os.path.join(out_dir, url))))

    def test_no_google_fonts_and_no_second_copy_of_the_tokens(self):
        for rel in PAGES:
            page = read(rel)
            with self.subTest(page=rel):
                self.assertNotRegex(page, r"fonts\.(googleapis|gstatic)\.com")
                self.assertEqual(page.count("--ai-chip-bg: #E1F5EE"), 1)
                self.assertEqual(page.count("--bg: #f4f2ee"), 1, "color tokens defined once, in the theme")

    def test_builders_hold_no_color_tokens(self):
        for rel in ("report.py", "walkthrough.py", "demo_prototype/card_kit.py"):
            with self.subTest(builder=rel):
                self.assertNotRegex(read(rel), r"--(bg|panel|ink|claim|verdict|accent|s\d): #")

    def test_ai_teal_human_gray_values(self):
        css = read("numen_theme.css")
        light = css[:css.index("@media (prefers-color-scheme: dark)")]
        for v in ("--accent: #0F6E56", "--ai-chip-bg: #E1F5EE", "--ai-chip-ink: #085041"):
            self.assertIn(v, light)
        for block in (css[css.index("@media (prefers-color-scheme: dark)"):css.index(':root[data-theme="dark"]')],
                      css[css.index(':root[data-theme="dark"]'):]):
            for v in ("--accent: #5DCAA5", "--ai-chip-bg: #085041", "--ai-chip-ink: #9FE1CB"):
                self.assertIn(v, block)


def _lab(h):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    x, y, z = ((0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b,
               (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883)

    def t(v):
        return v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return 116 * t(y) - 16, 500 * (t(x) - t(y)), 200 * (t(y) - t(z))


def _blocks():
    css = read("numen_theme.css")
    d1, d2 = css.index("@media (prefers-color-scheme: dark)"), css.index(':root[data-theme="dark"]')
    return {"light": css[:d1], "dark (preference)": css[d1:d2], "dark (data-theme)": css[d2:]}


def _tok(block, name):
    return re.search(rf"--{name}: (#[0-9A-Fa-f]{{6}})", block).group(1)


class ColorMapping(unittest.TestCase):
    """The author-approved mapping (2026-10-06)."""

    def test_trickster_and_chorus_clear_of_the_teal_accent(self):
        import math
        for mode, block in _blocks().items():
            arch = [_tok(block, f"s{i}") for i in range(1, 8)]
            for name, i in (("Trickster", 2), ("Chorus", 5)):
                with self.subTest(mode=mode, archetype=name):
                    for a in ("accent", "ai-chip-bg", "ai-chip-ink"):
                        self.assertGreater(math.dist(_lab(arch[i]), _lab(_tok(block, a))), 35)
            for i in range(7):
                for j in range(i + 1, 7):
                    with self.subTest(mode=mode, pair=(i + 1, j + 1)):
                        self.assertGreater(math.dist(_lab(arch[i]), _lab(arch[j])), 20)

    def test_new_values(self):
        b = _blocks()
        self.assertEqual((_tok(b["light"], "s3"), _tok(b["light"], "s6")), ("#87a400", "#3d7d0f"))
        for k in ("dark (preference)", "dark (data-theme)"):
            self.assertEqual((_tok(b[k], "s3"), _tok(b[k], "s6")), ("#a6c21a", "#5c9a2a"))

    def test_ai_teal_human_gray_on_the_pages(self):
        rpt, wt, card = read("report.py"), read("walkthrough.py"), read("demo_prototype/card_kit.py")
        self.assertIn("border-left: 4px solid var(--accent); background: var(--lane); }", rpt)
        self.assertIn(".banner.reviewed { border-left-color: var(--human-rule); }", rpt)
        self.assertIn(".changed { margin: 0; border-left: 4px solid var(--human-rule);", rpt)
        self.assertIn(".defs h3:target { color: var(--accent); }", rpt)
        self.assertNotRegex(rpt, r"\.chip\.(ev|br) \{")
        self.assertIn(".plain { border-left: 4px solid var(--ink);", wt)
        self.assertIn("border: 2px dashed var(--human-rule)", wt)
        self.assertIn(".wnote { margin: 14px 0 0; font-size: 14px; border-left: 4px solid var(--claim);", wt)
        self.assertIn(".badge { border: 1px solid var(--human-rule);", card)
        self.assertIn(".badge.changed { background: var(--human-chip-bg);", card)
        self.assertIn(".author-note { border-left-color: var(--ink); }", card)
        for src in (rpt.split("REVIEW_CSS")[0], wt, card):
            self.assertNotIn("var(--verdict)", src)

    def test_bold_is_inter_600_and_script_never_bold(self):
        css = read("numen_theme.css")
        self.assertIn("b, strong { font-weight: 600; }", css)
        self.assertNotRegex(css, r'"Courier Prime"; font-style: normal; font-weight: [5-9]00')


HOST_JS = r"""
const frames = [...document.querySelectorAll('iframe')], out = {};
let left = frames.length;
frames.forEach(f => f.addEventListener('load', () => setTimeout(async () => {
  const w = f.contentWindow, d = f.contentDocument, de = d.documentElement;
  await d.fonts.ready;
  const fam = sel => { const el = d.querySelector(sel); return el ? w.getComputedStyle(el).fontFamily : null; };
  // The report shows script text only inside an opened panel: probe the class itself.
  if (!d.querySelector('.script') && f.dataset.k === 'fog_story_report.html') {
    const p = d.createElement('div'); p.className = 'script'; p.textContent = 'TRUDY'; d.body.appendChild(p); }
  const loaded = [...d.fonts].filter(x => x.status === 'loaded').map(x => x.family.replace(/"/g, '') + ' ' + x.weight);
  out[f.dataset.k] = {inner: w.innerWidth, scroll: de.scrollWidth, client: de.clientWidth, loaded: [...new Set(loaded)].sort(),
    h1: fam('h1'), body: fam('body'), script: fam('.script')};
  if (--left === 0) document.getElementById('out').textContent = JSON.stringify(out);
}, 400)));
"""


@unittest.skipUnless(CHROME, "no headless Chrome/Edge found")
class InTheBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        frames = "".join(
            f'<iframe data-k="{rel}" src="{"file:///" + os.path.join(ROOT, rel).replace(os.sep, "/")}" '
            f'style="border:0;width:390px;height:844px"></iframe>' for rel in PAGES)
        host = os.path.join(cls.tmp, "host.html")
        with open(host, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><body style="margin:0"><pre id="out"></pre>{frames}<script>{HOST_JS}</script></body>')
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                            "--window-size=540,900", "--virtual-time-budget=10000", "--dump-dom",
                            "file:///" + host.replace("\\", "/")], capture_output=True, timeout=180,
                           text=True, encoding="utf-8")
        m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
        cls.res = json.loads(html.unescape(m.group(1))) if m and m.group(1).strip() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_measured(self):
        self.assertIsNotNone(self.res)
        self.assertEqual(set(self.res), set(PAGES))

    def test_fonts_load_and_apply(self):
        for rel, x in self.res.items():
            with self.subTest(page=rel):
                self.assertTrue(x["h1"].startswith('"Fraunces"') or x["h1"].startswith("Fraunces"), x["h1"])
                self.assertTrue(x["body"].startswith('"Inter"') or x["body"].startswith("Inter"), x["body"])
                self.assertIn("Fraunces 500", x["loaded"])
                self.assertTrue({"Inter 400", "Inter 500"} & set(x["loaded"]))
        for rel in ("fog_story_report.html", "numen_walkthrough.html"):
            self.assertIn("Courier Prime", self.res[rel]["script"] or "", rel)

    def test_no_sideways_scroll_at_390px(self):
        for rel, x in self.res.items():
            with self.subTest(page=rel):
                self.assertEqual(x["inner"], 390)
                self.assertLessEqual(x["scroll"], x["client"])


if __name__ == "__main__":
    unittest.main()
