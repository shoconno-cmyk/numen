"""Checks on the FAQ page (faq.py -> faq.html).

Run: python -m unittest test_faq
"""
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import faq  # noqa: E402
import numen_theme  # noqa: E402
import report  # noqa: E402
import report_guard as g  # noqa: E402
import walkthrough as w  # noqa: E402

_B = {}


def page():
    if not _B:
        _B["html"], _B["N"] = faq.build()
    return _B


def visible():
    return g.all_visible_text(page()["html"])


class Figure(unittest.TestCase):
    def test_computed_like_the_walkthrough(self):
        self.assertEqual(page()["N"], {"kept": 57, "ai_calls": 82})
        self.assertEqual((page()["N"]["kept"], page()["N"]["ai_calls"]), w.kept_as_made(w.load("model")))

    def test_the_figure_is_exact(self):
        self.assertIn("On the demo script, 57 of the AI's 82 archetype calls held up on human review.", visible())

    def test_no_typed_digits_in_the_text(self):
        for q, a in faq.QA:
            self.assertNotRegex(q + re.sub(r"\{\w+\}", "", a), r"\d")


class Page(unittest.TestCase):
    def test_header(self):
        h = page()["html"]
        self.assertEqual(re.search(r"<h1>(.*?)</h1>", h, re.S).group(1), '<span class="wordmark">Numen</span>')
        self.assertIn(f'<p class="tagline">{w.TAGLINE}</p>', h)
        self.assertIn("<h2>Frequently Asked Questions</h2>", h)

    def test_questions_bold_answers_beneath_in_order(self):
        h = page()["html"]
        pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", h, re.S)
        self.assertEqual(len(pairs), 7)
        self.assertEqual([report.e(q) for q, _ in faq.QA], [q for q, _ in pairs])
        self.assertIn(".faq dt { font-weight: 600;", h)

    def test_text_exactly(self):
        v = visible()
        for s in ("Why archetypes? Why The Big Seven and Jung, and not just a reader's coverage?",
                  "Does Numen say whether a script is good?",
                  "Whether that makes a good story is for the people reading it to decide.",
                  "Does a high archetype count mean my script will be a hit?",
                  "Other tools already do those well.",
                  "Claude, made by Anthropic.",
                  "Get in touch through LinkedIn for a read."):
            self.assertIn(s, v)

    def test_links(self):
        h = page()["html"]
        self.assertIn('<a href="https://www.linkedin.com/in/shoconno">LinkedIn</a>', h)
        self.assertIn(numen_theme.home_button(ROOT), h)
        self.assertIn('href="index.html">Back to Main Page</a>', h)

    def test_built_page_is_current(self):
        with open(faq.OUT, encoding="utf-8") as f:
            self.assertEqual(f.read(), page()["html"])


class Guard(unittest.TestCase):
    def test_passes_every_check(self):
        self.assertEqual(faq.check(page()["html"], page()["N"]), [])

    def test_good_is_caught_without_approval(self):
        s = "Does Numen say whether a script is good?"
        self.assertTrue(any(re.search(p, s, re.I) for p in report.GRADING))
        self.assertIn(s, faq.approved(page()["N"]))

    def test_approval_does_not_cover_model_or_old_name(self):
        bad = page()["html"].replace("Claude, made by Anthropic.", "Claude, a model made by Anthropic. a-score")
        problems = faq.check(bad, page()["N"])
        self.assertTrue(any(p.startswith("model word") for p in problems))
        self.assertTrue(any(p.startswith("old name") for p in problems))

    def test_unapproved_text_is_still_checked(self):
        bad = page()["html"].replace("Other tools already do those well.", "Other tools have a flaw.")
        self.assertTrue(faq.check(bad, page()["N"]))


if __name__ == "__main__":
    unittest.main()
