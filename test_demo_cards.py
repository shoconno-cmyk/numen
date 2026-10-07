"""Checks on the built demo cards in demo_prototype/ (no PDF rendering).

Run: python -m unittest test_demo_cards
"""
import html
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "demo_prototype"))
import card_kit as K  # noqa: E402
import report_guard as g  # noqa: E402
from tagging_schema import BIG_SEVEN_DEFINITIONS  # noqa: E402

CARDS = {name: os.path.join(ROOT, "demo_prototype", name) for name in (
    "pete_scene122_beat1_card.html", "mackie_scene140_beat6_card.html",
    "holly_scene3_beat2_card.html", "protected_protector_card.html")}


def visible(path):
    page = open(path, encoding="utf-8").read()
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", page.split("<body>", 1)[-1], flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))


class Cards(unittest.TestCase):
    def test_every_card_uses_the_two_labels(self):
        for name, path in CARDS.items():
            with self.subTest(card=name):
                v = visible(path)
                self.assertIn("The AI's read", v)
                self.assertIn("Human review", v)
                self.assertNotRegex(v, r"(?i)\breasoning\b|\brationale\b|The AI said|Human verdict|The model's read")

    def test_framing_says_ai_not_model(self):
        # check_card strips locked AI text and verbatim review text (data-verbatim)
        # and fails on "model" anywhere else.
        for name, path in CARDS.items():
            with self.subTest(card=name):
                K.check_card(path)

    def test_model_check_catches_framing(self):
        import tempfile
        page = open(CARDS["holly_scene3_beat2_card.html"], encoding="utf-8").read()
        bad = page.replace("The AI read Holly", "The model read Holly")
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
            fh.write(bad)
        try:
            with self.assertRaises(SystemExit):
                K.check_card(fh.name)
        finally:
            os.remove(fh.name)

    def test_no_old_name(self):
        for name, path in CARDS.items():
            with self.subTest(card=name):
                with open(path, encoding="utf-8") as fh:
                    self.assertEqual(g.old_name_hits(fh.read()), [])

    def test_archetype_names_are_the_big_seven(self):
        names = "|".join(map(re.escape, BIG_SEVEN_DEFINITIONS))
        for name in ("mackie_scene140_beat6_card.html", "holly_scene3_beat2_card.html",
                     "protected_protector_card.html"):
            page = open(CARDS[name], encoding="utf-8").read()
            values = re.findall(r'<div class="value">([^<]+)</div>', page)
            self.assertTrue(values)
            for v in values:
                for part in html.unescape(v).split(" + "):
                    self.assertRegex(part, f"^({names})$")

    def test_card_three_has_one_amber_legend_line(self):
        v = visible(CARDS["protected_protector_card.html"])
        self.assertEqual(v.count("Amber:"), 1)

    def test_pete_model_read_is_the_stored_claim(self):
        import json
        syn = json.load(open(os.path.join(ROOT, "fog_pass2_calls", "synthesis_PETE.json"), encoding="utf-8"))
        claim = next(t for t in syn["turning_points"] if t["beat_id"] == "scene122_beat1")["what_changes"]
        page = open(CARDS["pete_scene122_beat1_card.html"], encoding="utf-8").read()
        said = re.search(r'<p class="note claimtext" data-verbatim="1">(.*?)</p>', page, re.S).group(1)
        self.assertEqual(html.unescape(said), claim)
        self.assertIn('<h2><span class="chip-ai">The AI&#x27;s read</span></h2>', page)

    def test_ai_labels_teal_review_labels_gray(self):
        for name, path in CARDS.items():
            page = open(path, encoding="utf-8").read()
            with self.subTest(card=name):
                self.assertNotRegex(page, r"<h2>The AI&#x27;s read</h2>|<h2>Human review</h2>")
                self.assertIn('<span class="chip-human">Human review</span>', page)
                self.assertIn('url("../fonts/inter-latin-400-normal.woff2")', page)

    def test_pete_review_is_the_record_verbatim(self):
        text = open(os.path.join(ROOT, "FOG_PETE_REVIEW.md"), encoding="utf-8").read()
        v = visible(CARDS["pete_scene122_beat1_card.html"])
        for bullet in ["The punch is not in this beat.", "What 122_1 holds is the aftermath.",
                       "The punch would be an origin, not a turning point."]:
            self.assertIn(bullet, text)
            self.assertIn(bullet, v)

    def test_mackie_author_note(self):
        v = visible(CARDS["mackie_scene140_beat6_card.html"])
        self.assertIn("Author's note (Oct 6, 2026) This moment could also be read as Great Mother, dark pole. "
                      "I judged Shadow the better fit.", v)

    def test_mackie_cards_link_to_each_other(self):
        a = open(CARDS["mackie_scene140_beat6_card.html"], encoding="utf-8").read()
        b = open(CARDS["protected_protector_card.html"], encoding="utf-8").read()
        self.assertIn('href="protected_protector_card.html"', a)
        self.assertIn('href="mackie_scene140_beat6_card.html"', b)
        self.assertIn("Mackie also appears in the card", visible(CARDS["mackie_scene140_beat6_card.html"]))
        self.assertIn("Mackie also appears in the card", visible(CARDS["protected_protector_card.html"]))

    def test_card_three_states_each_review_outcome(self):
        v = visible(CARDS["protected_protector_card.html"])
        for s in ["In a flashback scene, the AI read Mackie as Great Mother over his son and Young John as Hero. "
                  "Then, near the end of the script, the AI read John as Great Mother over his sister Trudy. "
                  "The human review kept all three calls.",
                  "Amber: the Great Mother moments, Mackie then and John now.",
                  "Upheld: Great Mother, marked dark pole.", "Upheld: Hero.",
                  "Upheld: Great Mother, with fields corrected; not marked dark pole.", "Then", "Now"]:
            self.assertIn(s, v)


def figures(path):
    """(pdf page, caption number, PNG bytes) for each rendered page on a card."""
    import base64
    page = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<figure class="page" data-pdf-page="(\d+)">(.*?)</figure>', page, re.S):
        img = re.search(r'src="data:image/png;base64,([^"]+)"', m.group(2)).group(1)
        cap = re.search(r"<figcaption>Full of Grace, page (\d+)</figcaption>", m.group(2))
        out.append((int(m.group(1)), int(cap.group(1)) if cap else None, base64.b64decode(img)))
    return out


def dark_mask(png_bytes):
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert("L")
    return {i for i, v in enumerate(im.getdata()) if v < 100}


def strip_is_white(png_bytes, line):
    """True if the 2pt strip left of a text line (where highlight padding
    would sit) is white paper."""
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    x0, x1 = int((line["x0"] - 2.5) * K.SCALE), int((line["x0"] - 0.5) * K.SCALE)
    y0, y1 = int(line["top"] * K.SCALE), int(line["bottom"] * K.SCALE)
    px = [im.getpixel((x, y)) for x in range(x0, x1) for y in range(y0, y1)]
    return all(min(p) >= 250 for p in px)


def header_is_plain(pdf, pno, png_bytes):
    head = next(l for l in pdf.pages[pno - 1].dedupe_chars().extract_text_lines() if K.is_page_number(l))
    return strip_is_white(png_bytes, head)


class Captions(unittest.TestCase):
    """Approved exemption (2026-10-06): "Full of Grace, page N" captions,
    where N must come from the page under it, never typed."""

    @classmethod
    def setUpClass(cls):
        import pdfplumber
        cls.pdf = pdfplumber.open(K.PDF_PATH)
        cls.renders = {}

    @classmethod
    def tearDownClass(cls):
        cls.pdf.close()

    def render(self, pno):
        if pno not in self.renders:
            import io
            img = self.pdf.pages[pno - 1].dedupe_chars().to_image(resolution=K.DPI).original.convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            self.renders[pno] = dark_mask(buf.getvalue())
        return self.renders[pno]

    def test_every_caption_matches_the_page_it_sits_under(self):
        seen = 0
        for name, path in CARDS.items():
            for pno, n, png in figures(path):
                with self.subTest(card=name, pdf_page=pno):
                    self.assertIsNotNone(n, "page caption missing")
                    # the number is the page's own header number ...
                    self.assertEqual(n, K.printed_number(self.pdf, pno))
                    # ... and the image above it really is that PDF page (its text pixels)
                    a, b = dark_mask(png), self.render(pno)
                    self.assertGreater(len(a & b) / len(a | b), 0.95)
                    seen += 1
        self.assertEqual(seen, 9)

    def test_page_number_lines_are_never_highlighted(self):
        # Sample the strip just left of each page's "N." header, inside where a
        # highlight's padding would fall: it must be plain white paper.
        import io
        from PIL import Image
        for name, path in CARDS.items():
            for pno, n, png in figures(path):
                with self.subTest(card=name, pdf_page=pno):
                    self.assertTrue(header_is_plain(self.pdf, pno, png))

    def test_header_check_sees_a_highlight(self):
        # Control: the same strip check fails on a moment line that is highlighted.
        png = next(p for pno, _, p in figures(CARDS["mackie_scene140_beat6_card.html"]) if pno == 85)
        line = next(l for l in self.pdf.pages[84].dedupe_chars().extract_text_lines()
                    if K.norm(l["text"]).startswith("Without warning"))
        self.assertFalse(strip_is_white(png, line))

    def test_the_image_check_tells_pages_apart(self):
        png = figures(CARDS["holly_scene3_beat2_card.html"])[0][2]
        a, b = dark_mask(png), self.render(4)
        self.assertLess(len(a & b) / len(a | b), 0.5)


class LockedTerms(unittest.TestCase):
    NOTE = "scene121_beat2 is the system's ID for an earlier moment, in scene 121, that the AI is pointing back to."
    CLAIM = "escalates from shouting at officers who restrain him (scene121_beat2) to actually decking a cop"

    def test_id_from_locked_text_is_allowed_in_framing(self):
        K.check_framing([("note", self.NOTE)], locked_text=self.CLAIM, locked_terms=["scene121_beat2"])

    def test_without_the_lock_the_id_is_a_pipeline_term(self):
        with self.assertRaises(SystemExit):
            K.check_framing([("note", self.NOTE)])

    def test_lock_only_covers_terms_really_in_the_locked_text(self):
        with self.assertRaises(SystemExit):
            K.check_framing([("note", self.NOTE.replace("121_beat2", "140_beat6"))],
                            locked_text=self.CLAIM, locked_terms=["scene140_beat6"])

    def test_lock_does_not_exempt_the_rest_of_the_line(self):
        with self.assertRaises(SystemExit):
            K.check_framing([("note", self.NOTE + " A powerful moment.")],
                            locked_text=self.CLAIM, locked_terms=["scene121_beat2"])

    def test_cards_carry_the_hood_notes(self):
        self.assertIn(self.NOTE, visible(CARDS["pete_scene122_beat1_card.html"]))
        self.assertIn("The 75_3 review note refers to an earlier note; the author confirmed which one.",
                      visible(CARDS["protected_protector_card.html"]))


class NoteSplit(unittest.TestCase):
    def test_split_keeps_quotes_and_parentheses_whole(self):
        note = ('A real act (shielding Andy: "But I was the one. Don\'t put it on him.") at cost. '
                'No field changes. weight_proportionality was `matched`.')
        shown, internal = K.split_note(note)
        self.assertEqual(shown, ['A real act (shielding Andy: "But I was the one. Don\'t put it on him.") at cost.',
                                 "No field changes."])
        self.assertEqual(internal, ["weight_proportionality was `matched`."])

    def test_split_never_changes_the_text(self):
        note = 'One. Two "three. four" five. self_perceived rewritten; goal_status stays.'
        self.assertEqual(" ".join(K.note_sentences(note)), note)


if __name__ == "__main__":
    unittest.main()
