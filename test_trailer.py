"""Checks on the trailer page (trailer.py -> trailer.html).

Run: python -m unittest test_trailer
"""
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import numen_theme  # noqa: E402
import report_guard as g  # noqa: E402
import trailer as t  # noqa: E402
import walkthrough as w  # noqa: E402


def page():
    return t.page()


class Video(unittest.TestCase):
    def test_file_is_an_mp4_under_the_limit(self):
        n = t.video_bytes()
        self.assertGreater(n, 0)
        self.assertLessEqual(n, 100 * 1024 * 1024)
        with open(os.path.join(ROOT, t.VIDEO), "rb") as f:
            self.assertEqual(f.read(12)[4:8], b"ftyp")

    def test_video_tag(self):
        h = page()
        self.assertRegex(h, r'<video class="video" controls playsinline preload="metadata"[^>]*>')
        self.assertIn('<source src="numen_trailer.mp4#t=2" type="video/mp4">', h)
        self.assertIn("aspect-ratio: 16 / 9", h)
        self.assertIn(".video { display: block; width: 100%;", h)

    def test_poster_only_if_present(self):
        has = os.path.exists(os.path.join(ROOT, t.POSTER))
        self.assertEqual(f'poster="{t.POSTER}"' in page(), has)


class Page(unittest.TestCase):
    def test_header_and_text(self):
        h = page()
        self.assertEqual(re.search(r"<h1>(.*?)</h1>", h, re.S).group(1), '<span class="wordmark">Numen</span>')
        self.assertIn(f'<p class="tagline">{w.TAGLINE}</p>', h)
        self.assertIn("<h2>Watch the Trailer</h2>", h)
        self.assertIn("Numen in about a minute: one screenplay, from PDF to Story Report.", g.all_visible_text(h))

    def test_links(self):
        h = page()
        self.assertIn('<a href="numen_walkthrough.html">', h)
        self.assertTrue(os.path.exists(os.path.join(ROOT, "numen_walkthrough.html")))
        self.assertIn(numen_theme.home_button(ROOT), h)

    def test_passes_every_check(self):
        self.assertEqual(t.check(page()), [])

    def test_checks_catch_model_and_old_name(self):
        bad = page().replace("one screenplay", "one model, a-score")
        problems = t.check(bad)
        self.assertTrue(any(p.startswith("model word") for p in problems))
        self.assertTrue(any(p.startswith("old name") for p in problems))

    def test_built_page_is_current(self):
        with open(t.OUT, encoding="utf-8") as f:
            self.assertEqual(f.read(), page())


if __name__ == "__main__":
    unittest.main()
