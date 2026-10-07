"""
Offline tests for fog_dev_read_runner.py (section 1, the development read:
genre, logline and full synopsis, prompt version 5) and its rendering in
report.py. No API call: --run is exercised against a fake client, with
every output path redirected to a temp directory.

Run from the repo root:  python -m unittest test_fog_dev_read_runner -v
"""
import json
import os
import shutil
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

import fog_dev_read_runner as r
import report_guard as g

LINES = r.read_script().split("\n")
# Test fixtures only, not a description of the script. No evaluation words,
# no quotations; the synopsis is three paragraphs of about 300 words.
LOGLINE = ("Test fixture. When a detective returns to his hometown for his father's funeral, he is drawn into "
           "the search for a missing girl, and what he finds puts his own family at risk.")
SYNOPSIS = "\n\n".join([
    "Test fixture. A man returns to the small town where he grew up after a death in his family. He has not "
    "been back in many years. At the funeral he sees old friends, a sister who stayed in town, and a woman he "
    "once knew well. A child from the town has been missing for several weeks, and the local police have no "
    "leads. The woman asks him to look into the case, and he agrees to stay for a few days. He moves into his "
    "late father's house and begins to read the old case notes he finds there.",
    "He talks to neighbors, to the police, and to a family friend who runs a shop near the river. Each person "
    "tells him a different part of the story. He finds a set of old files that point to a man outside the "
    "town, and he drives there to find him. The man tells him what he saw on the day the child went missing. "
    "On his way back, the family friend stops him on the road and takes his phone. The two men argue, and "
    "the friend leaves him there. He walks back to town along the road. That night he reads the files again "
    "and writes down the names of everyone who saw the child on the last day.",
    "A few days later the police find the child's body near the lake. They arrest a man who lives alone at "
    "the edge of town, and he answers their questions for many hours. What he tells them leads back to the "
    "detective's own sister. In the last scene of the story, she tells him what she did, and he gives her the "
    "keys to his car. He then drives to the house of a family he has known since childhood, knocks on the "
    "door, and tells them there is something he has to tell them.",
])


def resp(genre="Drama", logline=LOGLINE, synopsis=SYNOPSIS, **extra):
    return json.dumps({"genre": genre, "logline": logline, "synopsis": synopsis, **extra})


GOOD = resp()


def check(raw, stop="end_turn"):
    return r.check_response(raw, stop, LINES)


def violations(raw, stop="end_turn"):
    return check(raw, stop)[1]


def n_words(n):
    """A neutral text of exactly n words."""
    words = (SYNOPSIS.replace("\n\n", " ")).split()
    return " ".join((words * (n // len(words) + 1))[:n])


class Title(unittest.TestCase):
    def test_title_from_title_page(self):
        self.assertEqual(r.extract_title(), ("FULL OF GRACE", "Full of Grace"))

    def test_title_page_not_sent(self):
        body = r.script_body()
        self.assertNotIn("Written by", body[:2000])
        self.assertNotIn("@", body[:2000])
        self.assertTrue(body.lstrip().startswith("OVER BLACK:"))

    def test_unexpected_title_page_raises(self):
        with self.assertRaises(ValueError):
            r.extract_title("Some Script\nby nobody\n\fpage two")


class Checks(unittest.TestCase):
    def test_fixtures_are_in_range(self):
        self.assertTrue(r.LOGLINE_BOUNDS[0] <= len(LOGLINE.split()) <= r.LOGLINE_BOUNDS[1])
        self.assertTrue(300 <= len(SYNOPSIS.split()) <= 380)
        self.assertEqual(len(r.paragraphs(SYNOPSIS)), 3)

    def test_good_passes(self):
        self.assertEqual(violations(GOOD), [])

    def test_praise_rejected_in_each_part(self):
        for kw in [dict(synopsis=SYNOPSIS.replace("Test fixture.", "A gripping story.")),
                   dict(logline=LOGLINE.replace("Test fixture.", "A gripping story.")),
                   dict(genre="Powerful drama")]:
            part = next(iter(kw))
            with self.subTest(part=part):
                parsed, v, per = check(resp(**kw))
                self.assertTrue(per[part])
                self.assertTrue(any("praise word" in x for x in per[part]))

    def test_critique_rejected(self):
        bad = resp(synopsis=SYNOPSIS.replace("Test fixture.", "A predictable story."))
        self.assertTrue(any("critique word" in v for v in violations(bad)))

    def test_invented_quote_rejected(self):
        bad = resp(synopsis=SYNOPSIS + " He says, “I always knew it was you.”")
        self.assertTrue(any("[quote]" in v for v in violations(bad)))

    def test_verbatim_quote_is_not_rejected(self):
        # Short quotations are allowed (prompt v6); each is checked word for
        # word. This one is a real line (wrapped in the text).
        ok = resp(synopsis=SYNOPSIS + " He says, “There’s something I have to tell you.”")
        self.assertEqual(violations(ok), [])

    def test_directive_rejected(self):
        bad = resp(synopsis=SYNOPSIS + " The ending should be clearer.")
        self.assertTrue(any("should" in v for v in violations(bad)))

    def test_page_reference_rejected(self):
        bad = resp(logline=LOGLINE.replace("When a detective", "On page 2 a detective"))
        self.assertTrue(any("[citation]" in v for v in violations(bad)))

    def test_pipeline_term_rejected(self):
        bad = resp(synopsis=SYNOPSIS + " It is a boundary_revealed moment.")
        self.assertTrue(any("[pipeline]" in v for v in violations(bad)))

    def test_logline_malfunction_bound_8_to_120(self):
        self.assertEqual(r.LOGLINE_BOUNDS, (8, 120))
        for n, rejected in [(7, True), (8, False), (61, False), (120, False), (121, True)]:
            with self.subTest(n=n):
                per = check(resp(logline=n_words(n)))[2]
                self.assertEqual(any("[length]" in x for x in per["logline"]), rejected)

    def test_synopsis_malfunction_bound_100_to_1000(self):
        self.assertEqual(r.SYNOPSIS_BOUNDS, (100, 1000))
        for n, rejected in [(99, True), (100, False), (462, False), (1000, False), (1001, True)]:
            with self.subTest(n=n):
                per = check(resp(synopsis=n_words(n)))[2]
                self.assertEqual(any("[length]" in x for x in per["synopsis"]), rejected)

    def test_over_target_is_a_note_not_a_rejection(self):
        long_syn = SYNOPSIS + "\n\n" + n_words(150)
        three = LOGLINE + " A third sentence follows here."
        parsed, v, per = check(resp(logline=three, synopsis=long_syn))
        self.assertEqual(v, [])
        notes = r.length_notes(parsed)
        self.assertEqual(len(notes), 2)
        self.assertTrue(all("length over target" in x for x in notes))
        self.assertEqual(r.length_notes(check(GOOD)[0]), [])

    def test_sentence_count(self):
        self.assertEqual(r.sentence_count(LOGLINE), 2)
        self.assertEqual(r.sentence_count("He says, \u201cGo home.\u201d She stays."), 2)
        self.assertEqual(r.sentence_count("One sentence with El Vaquero in it."), 1)


class Repair(unittest.TestCase):
    ORIG = "He was told to keep silent.a While he waits, nothing happens."

    def test_stray_character_and_paragraph_break(self):
        out = r.check_repair(self.ORIG, "silent.a While", "silent.\n\nWhile")
        self.assertEqual(out, "He was told to keep silent.\n\nWhile he waits, nothing happens.")

    def test_refuses_word_changes(self):
        for old, new in [("silent.a While", "silent. Then"),       # a word changed
                         ("silent.a While", "quiet.\n\nWhile"),   # a word changed
                         ("silent.a While", "silent\n\nWhile"),   # two characters removed
                         ("keep", "kep"),                          # a real letter removed from a word
                         ("absent", "absnt")]:                     # not in the text
            with self.subTest(new=new):
                with self.assertRaises(ValueError):
                    r.check_repair(self.ORIG, old, new)

    def test_logline_must_be_one_paragraph(self):
        per = check(resp(logline=LOGLINE.replace(", he is", ".\n\nHe is")))[2]
        self.assertTrue(any("[shape]" in x for x in per["logline"]))

    def test_long_genre(self):
        per = check(resp(genre="A small town family drama about grief and secrets"))[2]
        self.assertTrue(any("[shape]" in x for x in per["genre"]))

    def test_malformed(self):
        for raw in ["Here is the read: " + GOOD, "```json\n" + GOOD + "\n```",
                    json.dumps({"genre": "Drama", "synopsis": SYNOPSIS}), resp(notes="x")]:
            with self.subTest(raw=raw[:30]):
                parsed, v, per = check(raw)
                self.assertIsNone(parsed)
                self.assertTrue(v[0].startswith("[malformed]"))
                self.assertTrue(all(per[k] for k in r.FIELDS))

    def test_truncated_response_rejected(self):
        self.assertTrue(violations(GOOD, stop="max_tokens")[0].startswith("[malformed]"))


class FakeClient:
    """Returns the queued texts in order (an Exception is raised instead);
    records each request."""

    def __init__(self, texts, stops=None):
        self.texts, self.stops, self.requests = list(texts), list(stops or []), []
        self.messages = SimpleNamespace(create=self.create, count_tokens=self.count_tokens)

    def count_tokens(self, **kw):
        return SimpleNamespace(input_tokens=60000)

    def create(self, **kw):
        self.requests.append(kw)
        text = self.texts.pop(0)
        if isinstance(text, Exception):
            raise text
        stop = self.stops.pop(0) if self.stops else "end_turn"
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop,
                               model=kw["model"], _request_id="req_fake",
                               usage=SimpleNamespace(input_tokens=60000, output_tokens=1500))


class Run(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.patches = [
            mock.patch.object(r, "CALL_PATH", os.path.join(self.tmp, "call.json")),
            mock.patch.object(r, "NEW_CALL_PATH", os.path.join(self.tmp, "call.new.json")),
            mock.patch.object(r, "OUT_PATH", os.path.join(self.tmp, "out.json")),
            mock.patch.object(r, "ARCHIVE_DIR", os.path.join(self.tmp, "archive")),
            mock.patch.object(g, "GUARD_LOG", os.path.join(self.tmp, "guard.jsonl")),
            mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-not-a-key"}),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def go(self, texts, stops=None, rerun=False):
        client = FakeClient(texts, stops)
        with mock.patch("anthropic.Anthropic", lambda **kw: client):
            r.run(rerun=rerun)
        with open(r.OUT_PATH, encoding="utf-8") as f:
            out = json.load(f)
        with open(r.CALL_PATH, encoding="utf-8") as f:
            calls = json.load(f)
        return out, calls, self.log(), client

    def log(self):
        if not os.path.exists(g.GUARD_LOG):
            return []
        with open(g.GUARD_LOG, encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]

    def test_first_attempt_accepted(self):
        out, calls, log, client = self.go([GOOD])
        self.assertEqual((out["source"], out["genre"], out["logline"], out["synopsis"], out["title"]),
                         ("ai", "Drama", LOGLINE, SYNOPSIS, "Full of Grace"))
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(calls["attempts"][0]["raw_text"], GOOD)  # saved raw
        self.assertEqual(log, [])
        self.assertFalse(os.path.exists(r.NEW_CALL_PATH))         # moved into place
        req = client.requests[0]
        self.assertEqual((req["model"], req["max_tokens"]), ("claude-sonnet-5", 16000))
        schema = req["output_config"]["format"]["schema"]
        self.assertEqual(req["output_config"]["format"]["type"], "json_schema")
        self.assertEqual((sorted(schema["required"]), schema["additionalProperties"]),
                         (["genre", "logline", "synopsis"], False))
        self.assertEqual((out["prompt_version"], calls["prompt_version"]), (6, 6))
        self.assertEqual(out["generated_by_prompt_version"], 6)
        with open(out["generating_prompt_file"], encoding="utf-8") as f:   # the exact prompt sent, saved
            pf = json.load(f)
        self.assertEqual((pf["prompt_version"], pf["system"]), (6, req["system"]))
        self.assertTrue(req["messages"][0]["content"].startswith(pf["user_head"]))
        r.check_generating_prompt(out)   # and it matches the record and the call file
        self.assertNotIn("length_notes", out)
        for rule in ["One or two sentences.",
                     "Give the premise, the protagonist, and the stakes. Do not reveal the ending.",
                     "Three or four paragraphs, about 300 to 380 words in all.",
                     "Include the ending.",
                     "Describe actions exactly as the page shows them.",
                     "Do not characterize an act as accidental, intentional, mistaken, or justified unless the "
                     "script states it or unmistakably shows it through action.",
                     "Do not state what a character believes or intends unless the script states it or "
                     "unmistakably shows it through action.",
                     "No evaluation in either direction",
                     "You may quote the script briefly. Keep each quotation short and copy it word for word.",
                     "Write complete, grammatical sentences."]:
            self.assertIn(rule, req["system"])
        self.assertNotIn("Written by", req["messages"][0]["content"][:3000])
        self.assertNotIn("Use no quotation marks", req["system"])
        self.assertNotIn("Do not quote the script", req["system"])

    def test_over_target_is_stored_and_logged(self):
        out, calls, log, client = self.go([resp(synopsis=SYNOPSIS + "\n\n" + n_words(150))])
        self.assertEqual(out["source"], "ai")
        self.assertEqual(len(client.requests), 1)       # no retry for length
        self.assertTrue(out["length_notes"][0].startswith("[synopsis] length over target"))
        self.assertEqual((log[-1]["event"], log[-1]["notes"]), ("length over target", out["length_notes"]))

    def test_retry_carries_violations(self):
        bad = resp(synopsis=SYNOPSIS.replace("Test fixture.", "A riveting story."))
        out, calls, log, client = self.go([bad, GOOD])
        self.assertEqual(out["source"], "ai_retry")
        self.assertIn("riveting", client.requests[1]["messages"][0]["content"][-800:])
        self.assertEqual(len(calls["attempts"]), 2)

    def test_fallback_keeps_the_parts_that_passed(self):
        bad = resp(synopsis=SYNOPSIS.replace("Test fixture.", "A riveting story."))
        out, calls, log, client = self.go([bad, bad])
        self.assertEqual((out["source"], out["genre"], out["logline"], out["synopsis"], out["missing"]),
                         ("fallback", "Drama", LOGLINE, None, ["synopsis"]))
        self.assertEqual(len(client.requests), 2)  # one retry only
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["fallback"], {"kept": ["genre", "logline"], "missing": ["synopsis"]})

    def test_fallback_without_logline(self):
        bad = resp(logline="Too short to pass.", synopsis=SYNOPSIS.replace("Test fixture.", "A riveting story."))
        out = self.go([bad, bad])[0]
        self.assertEqual((out["genre"], out["logline"], out["missing"]), ("Drama", None, ["logline", "synopsis"]))

    def test_two_malformed_fall_back_to_title_only(self):
        out = self.go(["not json", "still not json"])[0]
        self.assertEqual((out["source"], out["genre"], out["missing"]), ("fallback", None, list(r.FIELDS)))

    def test_refuses_to_overwrite(self):
        self.go([GOOD])
        with self.assertRaises(SystemExit):
            self.go([GOOD])

    def test_rerun_archives_the_earlier_result_when_storing(self):
        self.go([GOOD])  # the earlier, accepted result
        with open(r.OUT_PATH, encoding="utf-8") as f:
            old_out = f.read()
        with open(r.CALL_PATH, encoding="utf-8") as f:
            old_call = f.read()
        new = resp(genre="Crime drama")
        out, calls, log, client = self.go([new], rerun=True)
        self.assertEqual(out["genre"], "Crime drama")
        archived = sorted(n for n in os.listdir(r.ARCHIVE_DIR) if not n.startswith("fog_dev_read_prompt."))
        self.assertEqual(len(archived), 2)
        contents = {n.split(".")[0]: open(os.path.join(r.ARCHIVE_DIR, n), encoding="utf-8").read() for n in archived}
        self.assertEqual(contents, {"call": old_call, "out": old_out})  # kept byte for byte

    def test_a_run_that_stops_partway_leaves_the_earlier_result_live(self):
        self.go([GOOD])
        with open(r.OUT_PATH, encoding="utf-8") as f:
            old_out = f.read()
        bad = resp(synopsis=SYNOPSIS.replace("Test fixture.", "A riveting story."))
        with self.assertRaises(RuntimeError):
            self.go([bad, RuntimeError("connection lost")], rerun=True)
        with open(r.OUT_PATH, encoding="utf-8") as f:
            self.assertEqual(f.read(), old_out)              # still live
        self.assertEqual([n for n in os.listdir(r.ARCHIVE_DIR)  # no earlier result archived yet
                          if not n.startswith("fog_dev_read_prompt.")], [])
        with open(r.NEW_CALL_PATH, encoding="utf-8") as f:   # the billed attempt is kept
            self.assertEqual(json.load(f)["attempts"][0]["raw_text"], bad)
        with self.assertRaises(SystemExit):                  # and must be looked at first
            self.go([GOOD], rerun=True)

    def test_rerun_needs_an_earlier_result(self):
        with self.assertRaises(SystemExit):
            self.go([GOOD], rerun=True)

    def test_cap_aborts_before_any_call(self):
        client = FakeClient([GOOD])
        with mock.patch.object(r, "COST_CAP", 0.01), mock.patch("anthropic.Anthropic", lambda **kw: client):
            with self.assertRaises(SystemExit):
                r.run()
        self.assertEqual(client.requests, [])

    def saved(self, attempt2_text, source="fallback"):
        """Write a call record and result as an earlier run would have."""
        with open(r.CALL_PATH, "w", encoding="utf-8") as f:
            json.dump({"prompt_version": 5, "attempts": [
                {"attempt": 1, "raw_text": "not json", "stop_reason": "end_turn"},
                {"attempt": 2, "raw_text": attempt2_text, "stop_reason": "end_turn"}]}, f)
        with open(r.OUT_PATH, "w", encoding="utf-8") as f:
            json.dump({"title": "Full of Grace", "title_printed": "FULL OF GRACE", "genre": "Drama",
                       "logline": LOGLINE, "synopsis": None, "source": source, "missing": ["synopsis"]}, f)

    def test_accept_saved_passing_attempt(self):
        self.saved(GOOD)
        r.accept_saved(2, "limit changed")
        with open(r.OUT_PATH, encoding="utf-8") as f:
            out = json.load(f)
        self.assertEqual((out["source"], out["accepted_attempt"], out["synopsis"], "missing" in out),
                         ("ai_accepted_after_rule_change", 2, SYNOPSIS, False))
        self.assertEqual((self.log()[-1]["attempt"], self.log()[-1]["reason"]), (2, "limit changed"))

    def test_accept_saved_failing_attempt_changes_nothing(self):
        self.saved(resp(synopsis=SYNOPSIS.replace("Test fixture.", "A riveting story.")))
        with open(r.OUT_PATH, encoding="utf-8") as f:
            before = f.read()
        with self.assertRaises(SystemExit):
            r.accept_saved(2, "limit changed")
        with open(r.OUT_PATH, encoding="utf-8") as f:
            self.assertEqual(f.read(), before)
        self.assertEqual(self.log(), [])

    def test_accept_saved_never_replaces_an_accepted_result(self):
        self.saved(GOOD, source="ai")
        with self.assertRaises(SystemExit):
            r.accept_saved(2, "x")


class Render(unittest.TestCase):
    """report.py shows section 1 from fog_dev_read.json and re-checks it."""

    def setUp(self):
        import report
        self.report = report
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "dev.json")
        self.base = {"title": "Full of Grace", "title_printed": "FULL OF GRACE", "genre": "Drama",
                     "logline": LOGLINE, "synopsis": SYNOPSIS, "source": "ai", "model": "claude-sonnet-5",
                     "call_file": "fog_dev_read_call.json", "attempts": 1, "total_cost_usd": 0.15,
                     "prompt_version": 5, "title_source": "code", "inputs": "fog_full.txt page 2 on only"}

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def html(self, **kw):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({**self.base, **kw}, f)
        with mock.patch.object(self.report, "DEV_READ", self.path):
            return self.report.dev_read_html(self.report.load_dev_read())

    def test_layered_section(self):
        h = self.html()
        self.assertIn("Section 1. Development Read", h)
        self.assertIn("Written by the AI", h)
        self.assertIn("<dt>Logline</dt>", h)
        self.assertIn('<details class="dr-syn"><summary>Read the full synopsis</summary>', h)
        self.assertEqual(h.count("<p>Test fixture.") + h.count("<p>He talks") + h.count("<p>A few days"), 3)
        self.assertIn('<div data-ai="1">', h)
        self.assertNotIn("toggle", h)

    def test_earlier_one_paragraph_result_still_renders(self):
        h = self.html(prompt_version=3, logline=None, synopsis=SYNOPSIS.split("\n\n")[0])
        self.assertIn("<dt>Synopsis</dt>", h)
        self.assertNotIn("Read the full synopsis", h)

    def test_fallback_note_names_the_missing_parts(self):
        h = self.html(synopsis=None, source="fallback", missing=["synopsis"])
        self.assertIn("are not shown: the full synopsis.", h)
        self.assertIn("<dt>Logline</dt>", h)

    def test_build_rejects_text_that_fails_the_guard(self):
        for kw in [dict(logline=LOGLINE.replace("Test fixture.", "A masterful story.")),
                   dict(synopsis=SYNOPSIS.replace("Test fixture.", "A masterful story."))]:
            with self.subTest(part=next(iter(kw))):
                with self.assertRaises(SystemExit):
                    self.html(**kw)

    def test_build_rejects_a_changed_title(self):
        with self.assertRaises(SystemExit):
            self.html(title="Full Of Grace!")

    def test_build_rejects_hand_edited_text(self):
        call = os.path.join(self.tmp, "call.json")
        with open(call, "w", encoding="utf-8") as f:
            json.dump({"attempts": [{"attempt": 1, "raw_text": GOOD}]}, f)
        import fog_dev_read_runner
        with mock.patch.object(fog_dev_read_runner, "CALL_PATH", call):
            self.html(accepted_attempt=1)  # matches the saved response
            with self.assertRaises(SystemExit):
                self.html(accepted_attempt=1, logline=LOGLINE.replace("missing girl", "missing child"))

    def repaired(self, **kw):
        call = os.path.join(self.tmp, "call.json")
        orig = SYNOPSIS.replace("Each person tells", "Each person.a Tells", 1)
        with open(call, "w", encoding="utf-8") as f:
            json.dump({"attempts": [{"attempt": 1, "raw_text": resp(synopsis=orig)}]}, f)
        fix = {"field": "synopsis", "date": "2026-10-06", "old": "person.a Tells", "new": "person.\n\nTells",
               "note": "Formatting repair: one stray character removed and one paragraph break restored; "
                       "no words changed.", "ai_original": orig}
        shown = orig.replace("person.a Tells", "person.\n\nTells")
        import fog_dev_read_runner
        with mock.patch.object(fog_dev_read_runner, "CALL_PATH", call):
            return self.html(**{"accepted_attempt": 1, "synopsis": shown, "formatting_repair": fix, **kw})

    def test_formatting_repair_shown_and_checked(self):
        h = self.repaired()
        self.assertIn("Formatting repair: one stray character removed and one paragraph break restored; "
                      "no words changed.", h)
        self.assertIn("<p>Tells him a different part", h)

    def test_build_rejects_display_beyond_the_logged_repair(self):
        with self.assertRaises(SystemExit):
            self.repaired(synopsis=SYNOPSIS.replace("Each person tells", "Each person.\n\nTells").replace(
                "old friends", "old pals"))

    def test_build_rejects_a_repair_that_changes_words(self):
        with self.assertRaises(SystemExit):
            self.repaired(formatting_repair={"field": "synopsis", "date": "x", "old": "person.a Tells",
                                             "new": "people.\n\nTells", "note": "x",
                                             "ai_original": SYNOPSIS.replace("Each person tells",
                                                                             "Each person.a Tells", 1)},
                          synopsis=SYNOPSIS.replace("Each person tells", "Each people.\n\nTells"))

    def test_author_check_shown_and_cited_text_must_exist(self):
        check = {"date": "2026-10-06", "by": "author", "note": "Checked against the script.",
                 "issues": [{"field": "logline", "text": "his father's funeral", "issue": "Example point."}],
                 "closing": "Otherwise confirmed accurate by the author."}
        h = self.html(author_check=check)
        self.assertIn("Logline: “his father&#x27;s funeral”. Example point.", h)
        self.assertIn("Otherwise confirmed accurate by the author.", h)
        bad = {**check, "issues": [{"field": "logline", "text": "not in the logline", "issue": "x"}]}
        with self.assertRaises(SystemExit):
            self.html(author_check=bad)

    def with_prompt(self, file_version=5, record_version=5, call_version=5):
        pf = os.path.join(self.tmp, "prompt.json")
        system = "Exact prompt text."
        sha = __import__("hashlib").sha256(system.encode("utf-8")).hexdigest()
        with open(pf, "w", encoding="utf-8") as f:
            json.dump({"prompt_version": file_version, "system": system, "system_sha256": sha}, f)
        call = os.path.join(self.tmp, "call.json")
        with open(call, "w", encoding="utf-8") as f:
            json.dump({"prompt_version": call_version, "system_sha256": sha, "attempts": []}, f)
        import fog_dev_read_runner
        with mock.patch.object(fog_dev_read_runner, "CALL_PATH", call):
            return self.html(prompt_version=record_version, generated_by_prompt_version=record_version,
                             generating_prompt_file=pf)

    def test_generating_prompt_version_shown_apart_from_current(self):
        h = self.with_prompt()
        self.assertIn("The text shown was produced by prompt v5", h)
        self.assertIn(f"v{r.PROMPT_VERSION} is the current prompt, for future runs.", h)

    def test_build_rejects_a_generating_prompt_mismatch(self):
        for kw in [dict(file_version=6), dict(record_version=6), dict(call_version=6)]:
            with self.subTest(**kw):
                with self.assertRaises(SystemExit):
                    self.with_prompt(**kw)
        with self.assertRaises(SystemExit):   # a named file that is missing
            self.html(generated_by_prompt_version=5, generating_prompt_file=os.path.join(self.tmp, "no.json"))

    def test_absent_file_means_no_section(self):
        with mock.patch.object(self.report, "DEV_READ", os.path.join(self.tmp, "missing.json")):
            self.assertIsNone(self.report.load_dev_read())
        self.assertEqual(self.report.dev_read_html(None), "")


class GuardLists(unittest.TestCase):
    def test_praise_list_requested_words(self):
        for w in ["compelling", "gripping", "powerful", "masterful", "brilliant", "stunning", "riveting",
                  "must-read", "beautifully"]:
            with self.subTest(w=w):
                self.assertIn("banned", {v.check for v in g.check_text(f"A {w} story.", "summary")})

    def test_evaluation_words_only_in_report_voice(self):
        self.assertEqual(g.check_text("A gripping story.", "text"), [])

    def test_plot_words_not_banned(self):
        for s in ["He is moving to Boston.", "A slow drive at night.", "She feels thinner than before."]:
            with self.subTest(s=s):
                self.assertEqual([v for v in g.check_text(s, "summary") if v.check == "banned"], [])


if __name__ == "__main__":
    unittest.main()
