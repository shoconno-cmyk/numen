"""
Tests for report_guard.py. Offline: no API call. Known-bad strings for each
check, and known-good strings that must pass, including quoted script lines
that contain banned words.

Run from the repo root:  python -m unittest test_report_guard -v
"""
import json
import os
import tempfile
import unittest

import report_guard as g

FULL = g.load_full_lines()
# Real beats, with lines pulled from fog_full.txt (checked in setUpClass):
#   scene60_beat4  (1980-1999): YOUNG CHEYENNE "John? I think you should slow down." (1984)
#   scene34_beat4  (1086-1108): TRUDY "Shit! You must be starving. Hey," (1107)
#   scene140_beat6 (4473-4485): YOUNG JOHN "You think I’m ever gonna play baseball after this?!"
#   scene172_beat1 (5376-5410): REGGIE "You’re way outta your jurisdiction, John."
EV = g.evidence_table(["scene60_beat4", "scene34_beat4", "scene140_beat6", "scene172_beat1"])


def checks(text, kind="observation", evidence=EV):
    return {v.check for v in g.check_text(text, kind, evidence, FULL)}


class SourceLines(unittest.TestCase):
    """The quotes the tests rely on really are in the script, at those lines."""

    def test_fixture_lines(self):
        self.assertIn("I think you should slow down.", FULL[1984 - 1])
        self.assertIn("You must be starving.", FULL[1107 - 1])
        self.assertEqual((EV["E1"].first_line, EV["E1"].last_line), (1980, 1999))
        self.assertEqual((EV["E3"].first_line, EV["E3"].last_line), (4473, 4485))


class Banned(unittest.TestCase):
    BAD = [
        "John's turn here is a problem [E3].",
        "There is a flaw in Mackie's logic [E3].",
        "The motivation feels weak [E3].",
        "A weakness of the sequence is its pacing [E3].",
        "This scene needs work [E3].",
        "Mackie's outburst is unearned [E3].",
        "The scene fails to set this up [E3].",
        "It's a failure of setup [E3].",
        "The chain of cause is broken here [E3].",
        "Having him grab John is a mistake [E3].",
        "The moment is poorly motivated [E3].",
        "We would grade this moment highly [E3].",
        "This beat would score low [E3].",
        "Our rating for this scene [E3].",
        "The writer should show more of Mackie's past [E3].",
        "Mackie must react more slowly [E3].",
        "The scene needs to slow down [E3].",
        "Fix the transition into the grab [E3].",
        "Cut the line before the grab [E3].",
        "Add a beat before the grab [E3].",
        "We recommend this script [E3].",
        "Verdict: Pass [E3].",
        "Recommend / Consider / Pass [E3]",
        "I'd pass on this one [E3].",
        "SHOULD Mackie grab him [E3]?",  # case-insensitive
    ]

    def test_bad(self):
        for s in self.BAD:
            with self.subTest(s=s):
                self.assertIn("banned", checks(s))

    def test_word_boundaries(self):
        # Words that merely contain a banned word must pass.
        for s in ["Mackie is shouldering the family's grief [E3].",
                  "Mackie added nothing [E3].",
                  "Mackie's grip tightens on his son's throat [E3].",
                  "Mackie passes the moment in silence [E3]."]:
            with self.subTest(s=s):
                self.assertNotIn("banned", checks(s))

    def test_quoted_script_with_banned_words_passes(self):
        good = [
            "Young Cheyenne asks John to ease off: “John? I think you should slow down.” [E1]",
            "Trudy greets him with “Shit! You must be starving.” before anything else is said [E2].",
            'Straight quotes work too: "I think you should slow down." [E1]',
        ]
        for s in good:
            with self.subTest(s=s):
                self.assertEqual(checks(s), set())

    def test_quotation_marks_alone_exempt_nothing(self):
        # Author ruling 2026-10-05: only a quote that verifies word for word
        # against fog_full.txt is exempt from the word checks.
        for kind in ("text", "summary"):
            with self.subTest(kind=kind):
                self.assertIn("banned", {v.check for v in g.check_text('"Why should I care?"', kind)})
                self.assertIn("banned", {v.check for v in g.check_text("He said “this needs work”.", kind)})
                self.assertIn("pipeline", {v.check for v in g.check_text('A "boundary_revealed" beat.', kind)})

    def test_verified_script_quote_is_still_exempt(self):
        # Line 1984: "John? I think you should slow down."
        self.assertNotIn("banned", {v.check for v in g.check_text(
            "Young Cheyenne: “John? I think you should slow down.”", "text")})

    def test_a_partial_script_quote_is_not_exempt(self):
        # "should slow dow" is not whole words in the script, so it is checked.
        self.assertIn("banned", {v.check for v in g.check_text("She says “should slow dow”.", "text")})

    def test_banned_word_outside_the_quote_still_fails(self):
        s = "“John? I think you should slow down.” The writer should cut this [E1]."
        self.assertIn("banned", checks(s))


class Questions(unittest.TestCase):
    BAD = [
        ("Does the audience need to see what Mackie knows", "no ?"),
        ("Consider whether Mackie's grab needs more setup?", "Consider"),
        ("Try showing Mackie's temper earlier?", "Try"),
        ("What if you gave Mackie an earlier outburst?", "What if you"),
        ("Show what Mackie is afraid of here?", "imperative"),
        ("Make the grab land harder?", "imperative"),
        ("Imagine the scene without the grab?", "imperative"),
    ]
    GOOD = [
        "What does Mackie know at this point that makes this choice possible?",
        "Is the grab something the audience is meant to see coming, or is it meant to shock?",
        "How much of Mackie's fear is visible before this moment [E3]?",
        "Where in the script does Mackie's temper first show, if anywhere?",
        "Does “You think I’m ever gonna play baseball after this?!” land as the trigger the scene intends [E3]?",
    ]

    def test_bad(self):
        for s, why in self.BAD:
            with self.subTest(s=s, why=why):
                self.assertIn("question", checks(s, "question"))

    def test_needs_to_allowed_in_questions(self):
        # Author ruling 2026-10-05: "needs to" is allowed inside questions only.
        self.assertEqual(checks("Does the audience need to see this, or does it need to stay hidden?", "question"), set())
        self.assertEqual(checks("What does the scene need to show before the grab [E3]?", "question"), set())

    def test_spec_example_question_passes(self):
        # STORY_REPORT_SPEC.md's own example question.
        self.assertEqual(checks("Is that something the audience needs to see, or is it meant to stay hidden?",
                                "question"), set())

    def test_needs_to_still_banned_in_statements(self):
        self.assertIn("banned", checks("The audience needs to see this [E3].", "observation"))
        self.assertIn("banned", checks("The audience needs to see this.", "text"))

    def test_other_directives_still_banned_in_questions(self):
        self.assertIn("banned", checks("Does the writer think the scene should slow down?", "question"))

    def test_imperative_opener_still_checked_with_needs_to(self):
        self.assertIn("question", checks("Show what the audience needs to see?", "question"))

    def test_good(self):
        for s in self.GOOD:
            with self.subTest(s=s):
                self.assertEqual(checks(s, "question"), set())


class Pipeline(unittest.TestCase):
    BAD = [
        "This is boundary_revealed for Mackie [E3].",
        "A THROUGHLINE_EVOLUTION moment [E3].",
        "Under Principle 8, this is new [E3].",
        "Principle 11 applies here [E3].",
        "Compare scene140_beat5 [E3].",
        "Earlier, in scene75, Mackie is calm [E3].",
        "The Pass 2 judgment differs [E3].",
        "Its weight_proportionality is off [E3].",
        "The CharacterizationConsistency value [E3].",
        "It matches trait 2 [E3].",
        "As finding 19 says [E3].",
        "Marked llm_human_corrected [E3].",
        "requires_second_pass for now [E3].",
        "no_confident_archetype here [E3].",
    ]

    def test_bad(self):
        for s in self.BAD:
            with self.subTest(s=s):
                self.assertIn("pipeline", checks(s))

    def test_schema_vocabulary_loaded(self):
        for v in ("boundary_revealed", "throughline_evolution", "requires_second_pass",
                  "no_confident_archetype", "functional_role_only", "weight_proportionality"):
            self.assertIn(v, g.ENUM_VALUES)
        self.assertIn("CharacterizationConsistency", g.ENUM_NAMES)

    def test_plain_words_pass(self):
        # Single-word enum values are ordinary English and are not banned.
        self.assertEqual(checks("Mackie's reaction is consistent with what came before [E3]."), set())


class Citations(unittest.TestCase):
    def test_observation_needs_a_citation(self):
        self.assertIn("citation", checks("Mackie grabs his son without warning."))

    def test_unknown_id(self):
        self.assertIn("citation", checks("Mackie grabs his son [E9]."))

    def test_one_unknown_among_good_still_fails(self):
        self.assertIn("citation", checks("Mackie grabs his son [E3], as before [E7]."))

    def test_loose_id(self):
        self.assertIn("citation", checks("Mackie grabs his son (E3)."))

    def test_model_writes_own_page_or_line(self):
        for s in ["Mackie grabs his son on page 83 [E3].", "See p. 84 [E3].", "Lines 4484-4485 show it [E3]."]:
            with self.subTest(s=s):
                self.assertIn("citation", checks(s))

    def test_resolves_to_code_built_pages(self):
        s = "Mackie grabs his son without warning [E3]."
        self.assertEqual(checks(s), set())
        self.assertEqual(g.resolve_citations(s, EV), "Mackie grabs his son without warning (pp. 83–84).")

    def test_text_kind_has_no_citation_rule(self):
        self.assertEqual(checks("Moments worth a second look.", "text"), set())


class Quotes(unittest.TestCase):
    def test_verbatim_quote_in_cited_lines_passes(self):
        self.assertEqual(checks("Reggie says “You’re way outta your jurisdiction, John.” [E4]"), set())

    def test_quote_wrapped_across_lines_passes(self):
        # 5383-5384 split this line across two script lines.
        self.assertEqual(checks("He tells John “way outta your jurisdiction, John” [E4]."), set())

    def test_straight_apostrophe_matches_curly(self):
        self.assertEqual(checks('Reggie: "You\'re way outta your jurisdiction, John." [E4]'), set())

    def test_trailing_punctuation_inside_quotes_passes(self):
        # Author ruling 2026-10-05: the comma in "El Vaquero," is the writer's
        # punctuation. The name is in E4 (line 5407: "This is not El Vaquero.").
        self.assertEqual(checks("John is told the man is not “El Vaquero,” and then disarmed [E4]."), set())
        self.assertEqual(checks('A lead called "El Vaquero," turns up.', "summary"), set())
        for q in ["El Vaquero.", "El Vaquero;", "El Vaquero:", "El Vaquero!", "El Vaquero?"]:
            with self.subTest(q=q):
                self.assertEqual(checks(f"A lead called “{q}” turns up.", "summary"), set())

    def test_stripping_punctuation_does_not_excuse_a_changed_word(self):
        self.assertIn("quote", checks('A lead called "El Vaqueros," turns up.', "summary"))

    def test_whole_words_only(self):
        # Author ruling 2026-10-05: the first development-read run quoted
        # "baptize", which passed as a substring of "baptized" (lines 5556, 5568).
        self.assertIn("quote", checks('Trudy wanted to "baptize" her.', "summary"))
        self.assertEqual(checks('Nobody even got "baptized." in time.', "summary"), set())

    def test_whole_words_in_cited_lines(self):
        # A quote cut off mid-word fails; the full words pass (E4, 5383-5384).
        self.assertIn("quote", checks("He says “outta your jurisdic” [E4]."))
        self.assertEqual(checks("He says “outta your jurisdiction” [E4]."), set())

    def test_possessive_still_matches_the_name(self):
        # "Holly" inside "Holly’s" is a whole word; the apostrophe ends it.
        self.assertEqual(checks('The name "Holly" recurs.', "summary"), set())

    def test_quote_of_only_punctuation_fails(self):
        self.assertIn("quote", checks('He says "?" and leaves [E4].'))

    def test_invented_quote_fails(self):
        self.assertIn("quote", checks("Reggie says “You handle the boat, Doug.” [E4]"))

    def test_paraphrase_in_quotes_fails(self):
        self.assertIn("quote", checks("Reggie says “You are way out of your jurisdiction, John.” [E4]"))

    def test_real_quote_but_wrong_citation_fails(self):
        # The line is real, but it is not in the cited beat (E3 is Mackie's).
        self.assertIn("quote", checks("Reggie says “You’re way outta your jurisdiction, John.” [E3]"))

    def test_quote_without_any_citation_fails(self):
        self.assertIn("quote", checks("He says “Your phone.”", "question"))


class RetryPolicy(unittest.TestCase):
    def setUp(self):
        fd, self.log = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)

    def tearDown(self):
        os.remove(self.log)

    def run_guard(self, outputs, fallback="Mackie grabs his son without warning [E3]."):
        calls = []

        def generate(violations):
            calls.append(violations)
            out = outputs[len(calls) - 1]
            if isinstance(out, Exception):
                raise out
            return out
        r = g.guard_generate("item1", generate, lambda: fallback, "observation", EV, FULL, self.log)
        return r, calls

    def logged(self):
        with open(self.log, encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]

    def test_first_attempt_passes(self):
        r, calls = self.run_guard(["Mackie grabs his son without warning [E3]."])
        self.assertEqual((r.source, len(calls), calls[0]), ("ai", 1, None))
        self.assertEqual(self.logged(), [])

    def test_retry_gets_the_violations_and_passes(self):
        r, calls = self.run_guard(["The grab is unearned [E3].", "Mackie grabs his son without warning [E3]."])
        self.assertEqual(r.source, "ai_retry")
        self.assertEqual(len(calls), 2)
        self.assertTrue(any("unearned" in v for v in calls[1]))
        self.assertEqual(self.logged(), [])

    def test_two_failures_fall_back_and_log(self):
        r, calls = self.run_guard(["The grab is unearned [E3].", "The writer should fix this [E3]."])
        self.assertEqual(r.source, "fallback")
        self.assertEqual(r.text, "Mackie grabs his son without warning [E3].")
        self.assertEqual(len(calls), 2)  # one retry only
        log = self.logged()
        self.assertEqual(len(log), 1)
        self.assertEqual([a["attempt"] for a in log[0]["rejected"]], [1, 2])

    def test_exception_counts_as_rejected(self):
        r, _ = self.run_guard([RuntimeError("timeout"), "Mackie grabs his son without warning [E3]."])
        self.assertEqual(r.source, "ai_retry")

    def test_non_string_is_rejected(self):
        r, _ = self.run_guard([{"text": "x"}, None])
        self.assertEqual(r.source, "fallback")

    def test_bad_fallback_raises(self):
        with self.assertRaises(ValueError):
            self.run_guard(["unearned [E3]", "unearned [E3]"], fallback="This is a problem [E3].")


class FinalScan(unittest.TestCase):
    PAGE = """<html><body><h1>Report</h1><p>John changes here.</p>
<details class="more hood"><summary>Under the hood</summary><p>boundary_revealed, scene140_beat6, should</p></details>
<script>const x = "should fix boundary_revealed";</script>
<p>Mackie’s reaction may be out of proportion.</p></body></html>"""

    def test_hood_and_scripts_are_not_scanned(self):
        self.assertEqual(g.final_scan(self.PAGE), [])

    def test_visible_problem_is_found(self):
        page = self.PAGE.replace("John changes here.", "John's arc is a problem. See scene140_beat6.")
        found = {f.violation.split(" ", 1)[0] for f in g.final_scan(page)}
        self.assertEqual(found, {"[banned]", "[pipeline]"})

    def test_reader_strings_are_scanned_with_quotes_masked(self):
        ok = [("panel", "Young Cheyenne: “John? I think you should slow down.”", "report_voice")]
        bad = [("panel", "The scene should slow down.", "report_voice")]
        self.assertEqual(g.final_scan(self.PAGE, ok), [])
        self.assertEqual(len(g.final_scan(self.PAGE, bad)), 1)


class OldName(unittest.TestCase):
    def test_old_name_in_visible_text_is_found(self):
        for text in ["a-score", "A-Score", "ascore", "ASCORE", "project_ascore"]:
            with self.subTest(text=text):
                page = f"<html><body><p>Built with {text}.</p></body></html>"
                self.assertEqual(len(g.old_name_hits(page)), 1)

    def test_under_the_hood_counts_as_visible(self):
        page = ('<html><body><details class="more hood"><summary>Under the hood</summary>'
                '<p>Made by a-score.</p></details></body></html>')
        self.assertEqual(len(g.old_name_hits(page)), 1)

    def test_internal_names_are_not_visible_text(self):
        page = ('<html><body><div data-mode="a-score-review-mode"><p>Numen</p></div>'
                "<script>const STORE = 'a-score-review-edits';</script></body></html>")
        self.assertEqual(g.old_name_hits(page), [])

    def test_ordinary_words_pass(self):
        self.assertEqual(g.old_name_hits("<html><body><p>A score of 12. A scoreboard.</p></body></html>"), [])


class ModelWord(unittest.TestCase):
    def test_framing_model_is_found(self):
        self.assertEqual(len(g.model_word_hits("The AI model does it in minutes.")), 1)
        self.assertEqual(len(g.model_word_hits("the fields the model stored")), 1)

    def test_model_id_line_is_the_exception(self):
        self.assertEqual(g.model_word_hits("Genre, logline and synopsis: model claude-sonnet-5 , written in one call"), [])

    def test_locked_text_is_not_framing(self):
        locked = ["Early model HONDA hatchback."]
        self.assertEqual(g.model_word_hits("Script: Early model HONDA hatchback. Idling.", locked), [])
        self.assertEqual(len(g.model_word_hits("Script: Early model HONDA hatchback. The model read it.", locked)), 1)

    def test_report_check_covers_hood_and_page_data(self):
        import report
        page = ('<html><body><details class="more hood"><summary>Under the hood</summary>'
                '<p>the fields the model stored</p></details></body></html>')
        with self.assertRaises(SystemExit):
            report.model_word_check("test page", page, [])
        with self.assertRaises(SystemExit):
            report.model_word_check("test page", "<html><body><p>AI</p></body></html>",
                                    [("TEXT[banner_p2_cold]", "AI Output: the model's judgments.", "static")])
        report.model_word_check("test page", "<html><body><p>The AI's read. model claude-sonnet-5</p></body></html>",
                                [("AI read x goal", "the model of a father", "ai_read")])


class QuotedStaticCopy(unittest.TestCase):
    PAGE = '<html><body><h2>"Why should I care?"</h2></body></html>'

    def test_heading_and_next_paragraph_are_checked_separately(self):
        # The heading ends in ?" with no space before the paragraph's text;
        # it must still match the approved string on its own.
        page = '<html><body><h2>"Why should I care?"</h2><p>When a script lands.</p></body></html>'
        self.assertEqual(g.final_scan(page, approved_static={'"Why should I care?"'}), [])
        self.assertEqual(g.sentences(g.visible_text(page)), ['"Why should I care?"', "When a script lands."])

    def test_quoted_heading_is_flagged_unless_approved(self):
        self.assertEqual([f.violation for f in g.final_scan(self.PAGE)], ["[banned] directive word 'should'"])
        self.assertEqual(g.final_scan(self.PAGE, approved_static={'"Why should I care?"'}), [])


class VerbatimClass(unittest.TestCase):
    """Author ruling 2026-10-05: the published definitions are exempt from the
    word checks only if they are on the page exactly and the label is there."""
    DEF = "The courage must be for another. Default to ordinary_reaction otherwise."
    LABEL = "These are the exact definitions given to the AI."
    V = {"label": [LABEL], "texts": [DEF]}

    def page(self, label=LABEL, text=DEF, extra=""):
        return f"<html><body><h2>Defs</h2><p>{label}</p><p>{text}</p>{extra}</body></html>"

    def test_exact_text_with_label_is_exempt(self):
        self.assertEqual(g.final_scan(self.page(), verbatim=self.V), [])

    def test_without_the_class_it_is_flagged(self):
        found = {f.violation for f in g.final_scan(self.page())}
        self.assertIn("[banned] directive word 'must'", found)
        self.assertIn("[pipeline] pipeline term 'ordinary_reaction'", found)

    def test_changed_text_stops_it(self):
        found = [f.violation for f in g.final_scan(self.page(text=self.DEF.replace("for another", "for others")),
                                                   verbatim=self.V)]
        self.assertIn("[verbatim] text not on the page exactly", found)
        self.assertIn("[banned] directive word 'must'", found)  # and the text is checked like any other

    def test_missing_label_stops_it(self):
        found = [f.violation for f in g.final_scan(self.page(label="Some other intro."), verbatim=self.V)]
        self.assertEqual(found, ["[verbatim] label not on the page exactly"])

    def test_other_text_on_the_page_is_still_checked(self):
        found = [f.violation for f in g.final_scan(self.page(extra="<p>This act needs work.</p>"), verbatim=self.V)]
        self.assertEqual(found, ["[banned] grading word 'needs work'"])


class TextClasses(unittest.TestCase):
    """Author ruling 2026-10-05: banned-word checks scoped by text type."""
    PAGE = "<html><body><h1>Why should I care?</h1><p>It gives no grade.</p></body></html>"
    APPROVED = {"Why should I care?", "It gives no grade."}

    def words(self, findings):
        return sorted(f.violation for f in findings)

    def test_static_copy_flagged_until_approved(self):
        self.assertEqual(len(g.final_scan(self.PAGE)), 2)
        self.assertEqual(g.final_scan(self.PAGE, approved_static=self.APPROVED), [])

    def test_approval_is_exact_string_only(self):
        page = self.PAGE.replace("It gives no grade.", "It gives no grade at all.")
        self.assertEqual(len(g.final_scan(page, approved_static=self.APPROVED)), 1)

    def test_new_static_text_still_checked(self):
        page = self.PAGE.replace("</body>", "<p>This act needs work.</p></body>")
        self.assertEqual(self.words(g.final_scan(page, approved_static=self.APPROVED)),
                         ["[banned] grading word 'needs work'"])

    def test_approved_static_still_checked_for_pipeline_terms(self):
        s = "It gives no grade, per boundary_revealed."
        found = g.final_scan("<body></body>", [("TEXT", s, "static")], approved_static={s})
        self.assertEqual(self.words(found), ["[pipeline] pipeline term 'boundary_revealed'"])

    def test_ai_read_exempt_from_banned_words(self):
        reads = [("AI read", "venting frustration at a failed physical challenge", "ai_read"),
                 ("AI read", "a woman reflecting honestly on her flawed past", "ai_read")]
        self.assertEqual(g.final_scan("<body></body>", reads), [])

    def test_ai_read_still_checked_for_pipeline_terms(self):
        reads = [("AI read", "a boundary_revealed moment in scene140_beat6", "ai_read")]
        self.assertEqual(len(g.final_scan("<body></body>", reads)), 2)

    def test_report_voice_gets_every_check(self):
        s = "venting frustration at a failed physical challenge"
        self.assertEqual(len(g.final_scan("<body></body>", [("observation", s, "report_voice")])), 1)
        # Approval does not extend to report-voice text.
        self.assertEqual(len(g.final_scan("<body></body>", [("observation", s, "report_voice")],
                                          approved_static={s})), 1)

    def test_unknown_class_is_rejected(self):
        with self.assertRaises(ValueError):
            g.final_scan("<body></body>", [("x", "text", "author")])


if __name__ == "__main__":
    unittest.main()
