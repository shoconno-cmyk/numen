# Full of Grace -- fully-cold pipeline test: findings

Findings from the fully-cold run on Full of Grace (the flagship validation
milestone; see `OCEANS11_OPEN_ITEMS.md` item 21). Each finding records the
raw, unreviewed behaviour as observed, before any fix it prompted, so the
cold numbers stay on record even after the pipeline changes.

## 1. Out-of-schema agency_alignment value on 3 of 12 pilot beats (logged 2026-09-26)

**Run:** `python fog_tagging_harness.py --pilot` (12 beats, `PILOT_BEAT_IDS`),
code at HEAD `93c9590`, model `claude-sonnet-5`, `max_tokens=4500`. First
contact between the model and the schema on this script; no beat reviewed.
Per-call raw responses are in `fog_tagging_calls.jsonl`.

**Finding:** on 3 of 12 pilot beats (25%) the model returned
`"agency_alignment": "requires_second_pass"`. That value does not exist.
`AgencyAlignment` has only `aligned` / `displaced`, since agency_alignment
is resolved in Pass 1. The prompt listed only `"aligned"|"displaced"` for
the field. Validation rejected all 3 responses and they were discarded
whole:

| Beat | Characters given the invalid value | Request ID |
|---|---|---|
| `scene14_beat12` | JOHN, SARGE | `req_011CfT6rJtCP97UEtToMtygk` |
| `scene172_beat1` | JOHN, REGGIE | `req_011CfT6v4tSZtHseWmKATrep` |
| `scene205_beat1` | DR. SHEPHARD | `req_011CfT6wMyNVtCJNkgNMDVv8` |

In each of the 3, every character that carried a `causal_integrity` block
used the invalid value. None of them mixed it with `aligned`. Two of the
discarded responses included real archetype tags (SARGE Mentor on
`scene14_beat12`, DR. SHEPHARD Great Mother on `scene205_beat1`), which
were lost along with the rest of the response.

**Raw cold compliance rate for this field: 9/12 beats (75%).** The other 9
responses either used a valid value or omitted `causal_integrity`, which
is allowed. One of the 9 (`scene143_beat7`) failed for a different reason:
it hit `max_tokens`. That makes 8/12 accepted overall.

**Response:** the prompt is being clarified to say explicitly that
agency_alignment must be resolved to `aligned` or `displaced` in this pass
and that no `requires_second_pass` option exists. No automatic
retry-on-validation-failure is being added: the cold run's real
compliance rate is part of what this test measures. Beats tagged after
that change are no longer a cold measurement of this prompt behaviour.

## 2. RAYMOND tagged on scene205_beat1 but absent from characters_present: coverage gap, not fabrication (logged 2026-09-26)

**Run:** pilot re-run of the 4 failed beats, code at `3401879`
(`max_tokens=8000`), request for `scene205_beat1` logged in
`fog_tagging_calls.jsonl`. The response tagged four characters: RAYMOND
(Shadow), DR. SHEPHARD (Great Mother), FEDERAL AGENT
(functional_role_only), LAWYER (no_confident_archetype).

**Stored `characters_present`:** `["DR. SHEPHARD", "FEDERAL AGENT", "LAWYER"]`.

**Stored turns** (`fog_tagged.json`, checked against `fog_full.txt`
lines 6196-6221, INT. INTERROGATION ROOM - CONTINUOUS): RAYMOND is named
in four of the beat's eight turns and is the physical centre of the
scene. He has no dialogue.

- turn 0 (action): "Raymond begins to cry. Dr. Shephard goes to him."
- turn 2 (action): "Raymond, more upset, beings to wail. Dr. Shephard
  tries to calm him. Raymond pushes Dr. Shephard away."
- turn 5 (action): "Raymond starts to thrash his head against the metal
  tabletop. Over and over. Blood comes out."
- turn 6 (DR. SHEPHARD dialogue): "Raymond!"

**Verdict: a coverage gap in `characters_present`, not a model
fabrication.** `characters_present` is built from speakers only
(`beat_detector.py:305`: `sorted({t['speaker'] for t in seg['turns'] if
t['speaker']})`), so a character who acts on the page without speaking is
never listed. RAYMOND is on the harness's canonical-name list. The prompt's
name rules tell the model to tag a canonical character "when that
character is physically present and doing something in the beat's own
turns", and that describes RAYMOND here. The model followed its
instructions. The field's name promises more than it computes.

**Scope:** this is by design, not specific to Full of Grace. Across
existing tagged files, `per_character` entries naming someone outside
`characters_present` are common: Ocean's Eleven 220/881, Babadook
127/470, LMS 105/624, GWH 58/626. The most frequent names are principal
characters (LINUS, DANNY, AMELIA, SAMUEL, WILL, RICHARD). Individual
entries were not inspected, so some could be misattributions rather than
silent presence. LOTB/WHTBD files store no `source_evidence`.

**Status:** documented only. Tag not changed or removed. The Shadow tag
itself is unreviewed like every other cold tag.

## 3. agency_alignment="displaced" rejected for missing displacement_mechanism: a prompt/schema gap (logged 2026-09-26)

**Run:** full pass (`python fog_tagging_harness.py`), code at `32a9936`,
`max_tokens=8000`. Request `req_011CfTAnrYoZtBuL3JCd7P9V`
(`stop_reason=end_turn`, 1701 output tokens), logged in
`fog_tagging_calls.jsonl`.

**Finding:** `scene7_beat3` was rejected with `agency_alignment=DISPLACED
requires displacement_mechanism to be set.` The response had one
character, HOLLY (`no_confident_archetype`), with `causal_integrity`
`{"weight_proportionality": "requires_second_pass", "agency_alignment":
"displaced", "characterization_consistency": "requires_second_pass"}` and
no `displacement_mechanism` key. `chain_soundness` was `undetermined`.

**Distinct from finding 1.** Here the model chose a valid enum value
(`displaced`) but left out a field that the schema requires only when that
value is used (`CausalIntegrityTag.validate()`, `tagging_schema.py:1095`).

**The prompt never asks for the field.** `displacement_mechanism` appears
nowhere in `llm_orchestration.py`. The response template offers
`"agency_alignment": "aligned"|"displaced"` with no mention of a required
companion field or its shape (`{"enabling_character": ...,
"convenient_capability": ...}`, `tagging_schema.py:1090`). So this is a gap
between what the prompt asks for and what the schema enforces, not the
model ignoring an instruction.

**Consequence:** every `displaced` judgment in this run will be rejected
unless the model happens to invent the field on its own. Accepted data
will therefore lean systematically toward `aligned`. Rejected beats are
not in the progress file, so they are re-run, not lost; but any read of
agency_alignment rates must wait until they are.

**Final count (full run complete, 448 calls):** 6 of 448 rejected, all for
this reason and no other: `scene7_beat3`, `scene77_beat1`, `scene170_beat7`,
`scene196_beat2`, `scene206_beat1`, `scene213_beat5`. The model never
supplied `displacement_mechanism` unprompted, so every `displaced`
judgment was rejected. Across all 454 accepted beats (pilot + full run),
agency_alignment is `aligned` on 521 of 521 `causal_integrity` entries
and `displaced` on 0. The predicted bias is total: until the 6 are re-run,
the accepted data contains no `displaced` judgments at all.

**Status:** documented only. No prompt fix, no retry. Rejected beats from
the whole run will be handled together at the end, as with the pilot's 4.

**Re-run after the prompt fix (2026-09-26, code at `aff52e1`):** the
template now shows `displacement_mechanism` inside `causal_integrity`,
with its shape, and states that it is required whenever agency_alignment
is `displaced`. The 6 rejected beats were re-run with
`python fog_tagging_harness.py`, which billed only those 6 (~$0.15). All 6
succeeded. **These 6 beats are no longer part of the pure cold
measurement**, as with the pilot's 4 re-run beats (finding 1).

None of the re-run beats came back `displaced`. Per character, cold
response vs. re-run (from `fog_tagging_calls.jsonl`):

| Beat | Cold: displaced | Re-run |
|---|---|---|
| `scene7_beat3` | HOLLY | HOLLY: causal_integrity omitted |
| `scene77_beat1` | ANGIE (JOHN aligned) | ANGIE: omitted; JOHN aligned |
| `scene170_beat7` | ALBERTO | ALBERTO aligned |
| `scene196_beat2` | RAYMOND | RAYMOND aligned |
| `scene206_beat1` | JOHN (MARCHAND aligned) | JOHN aligned; MARCHAND aligned |
| `scene213_beat5` | TRUDY (JOHN aligned) | TRUDY: omitted; JOHN: omitted |

Across all 460 beats, agency_alignment is now `aligned` on 526 of 526
entries, `displaced` on 0.

**Reading:** this is not evidence that the script has no displaced
agency. Each of the 6 cold `displaced` judgments flipped on a single
re-sample: 3 to `aligned`, 3 to omitting causal_integrity entirely. So the
model's displaced/aligned call on these beats is unstable, and it looks
especially fragile under an added requirement. The new "is rejected"
wording may also discourage choosing `displaced`. With n=6 and one sample
each, the two explanations cannot be separated. Whether Full of Grace has
any displaced cases is open and needs human review of these 6 beats (the
cold `displaced` responses, with their reasoning fields, are preserved in
the call log).

## 4. weight_proportionality resolved in Pass 1 on 21 of 526 entries (logged 2026-09-26)

**Finding:** 21 of the 526 `causal_integrity` entries in the cold Pass 1
output (all 460 beats, including the 10 post-fix re-run beats) have
`weight_proportionality` resolved to `matched` (20) or `mismatch` (1).
CLAUDE.md's two-pass discipline defers that field to Pass 2 so hindsight
can't contaminate early-beat judgment. The other 505 are
`requires_second_pass`.

**Distinct from findings 1-3.** Nothing here is invalid or missing: the
values are legal, and the validator accepts them. The problem is
premature resolution, and it goes against an explicit prompt instruction.
The Pass 1 prompt offers `"matched"|"mismatch"|"requires_second_pass"`
for the field, but also says both deferred fields "can ONLY be resolved
... if you have been given the FULL script's later beats for THAT
CHARACTER specifically ... default both to "requires_second_pass" for
every character -- do not guess" (`llm_orchestration.py`, after the
response template). The validator does not enforce it.

**The 21 entries (13 beats):**

| beat_id | character | value |
|---|---|---|
| `scene3_beat2` | KRISTA | matched |
| `scene3_beat2` | BETH | matched |
| `scene3_beat2` | HOLLY | matched |
| `scene19_beat1` | JOHN | matched |
| `scene64_beat7` | CHEYENNE | matched |
| `scene75_beat5` | MACKIE | matched |
| `scene75_beat5` | YOUNG JOHN | matched |
| `scene77_beat1` | JOHN | matched |
| `scene115_beat1` | JOHN | matched |
| `scene115_beat1` | RICARDO | matched |
| `scene140_beat1` | MACKIE | matched |
| `scene155_beat1` | JOHN | matched |
| `scene155_beat1` | O’SHEA | matched |
| `scene155_beat3` | CHEYENNE | matched |
| `scene155_beat3` | O’SHEA | matched |
| `scene155_beat10` | O’SHEA | matched |
| `scene155_beat11` | CHEYENNE | matched |
| `scene155_beat11` | JOHN | matched |
| `scene155_beat11` | O’SHEA | matched |
| `scene213_beat7` | TRUDY | matched |
| `scene216_beat4` | TRUDY | mismatch |

`scene77_beat1` is one of finding 3's post-fix re-run beats. Its JOHN
entry was resolved early in the re-run response, so it is not a pure cold
data point. The other 20 entries are from cold responses. The cold
response for that beat had JOHN at `requires_second_pass` (compliant).
`matched` appeared only in the re-run, in the same response that tagged
JOHN Persona. That Persona tag was later corrected to ordinary_reaction
(`FOG_JOHN_REVIEW.md`). Responses carry no rationale field and reasoning
is not returned, so whether `matched` rested on the Persona reading can't
be established from the data. Either way it is a Pass 1 value that
shouldn't exist.

**Status:** reset complete (2026-09-28, after the full character review).
All 21 entries were re-checked against `fog_tagged.json` first. They
still matched this table, and no other entry anywhere in the script had
weight_proportionality resolved. All 21 are now `requires_second_pass`,
each logged as a `weight_proportionality` correction citing this finding.
Pass 2 will resolve them fresh, the same as every other character's
beats. A re-scan finds 0 entries with weight_proportionality resolved
(and 0 with characterization_consistency resolved). Still no prompt or
validator change. The validator does not enforce the Pass 1 default, so
a future cold run could repeat this.

## 5. scene119_beat2: JOHN's continuing speech parsed as unattributed action, leaving characters_present empty (logged 2026-09-27)

**Found during:** JOHN review chunk 2 (`FOG_JOHN_REVIEW.md`), checked
against a fresh `pdftotext -layout -enc UTF-8` pull (byte-identical to
`fog_full.txt`), lines 3644-3655.

**Raw source:** one continuous JOHN speech under a single `JOHN` cue:
"You like it here? You like America? You can support your kids with that
pay check?", then the parenthetical "(without giving Ricardo a
chance--)" (wrapped across two lines), then "Oh, that's right, you don't
have any kids. You're here all alone. You're a loner. Guess what?"

**Stored:** the first line is correctly JOHN dialogue, the last turn of
`scene119_beat1`. The parenthetical and the line after it are stored as
two separate `action` turns with `speaker: null`. They make up all of
`scene119_beat2`, whose `characters_present` is therefore `[]`. The loss
already happens at Stage 1: `fog_parsed_scenes.json` scene 119 stores both
as `{"type": "action", "speaker": null}`, so the beat detector and
integration only passed it along. The cold response still tagged JOHN on
the beat (Shadow, since corrected to ordinary_reaction), so the model
recovered the speaker from context. Finding 2's gap is the same shape on
the output side: a tagged character absent from `characters_present`.

**Same class as** the speaker-loss and parenthetical-handling bugs found
on other scripts (`PARSING_BUG_IMPACT_REPORT.md`, `OPEN_ITEMS.md` item 1):
a parenthetical inside a speech breaks the speaker attribution of the
dialogue that follows it, with no visible error.

**Status:** documented only. No parser fix, no re-parse, and not checked
for other occurrences in Full of Grace.

## 6. O'SHEA split across three labels (HISPANIC, DRIVER, O'SHEA): identity fragmentation (logged 2026-09-27)

**Found during:** JOHN review chunk 3 (`FOG_JOHN_REVIEW.md`), while
checking scene154_beat2 against a fresh `pdftotext -layout -enc UTF-8`
pull (byte-identical to `fog_full.txt`).

**Raw source:** the script brings one man in under a description and names
him only mid-confrontation. The Chrysler 300's driver is "Hispanic, 30's,
hoodie and a Boston Celtics ball cap" (line 3174), "The driver is the
Hispanic and we're in the Chrysler 300" (4877), the gun line is cued
`HISPANIC (O.S.)` (4918), and Cheyenne's very next line is "O'Shea. Baby.
Don't." (4924). John then "disarms O'Shea of his weapon" (4943), and
"Cheyenne is led to the Chrysler 300 by O'Shea" (5741). No scene shows
two separately present people. "Hispanic" also describes Ricardo at
3335-3429 ("young Hispanic man, 20's"), a different person, who is always
tagged RICARDO.

**Stored (cold output):** 13 beats under 3 labels. DRIVER on
scene151_beat1 and scene153_beat1, HISPANIC on scene154_beat2, and O'SHEA
on scene154_beat2, scene155_beat1/3/6/7/8/9/10/11/12 and scene181_beat1.
scene154_beat2 carried two entries for the same man (HISPANIC
functional_role_only + O'SHEA no_confident_archetype) with conflicting
goals and goal_status. The harness's canonical-name list
(`fog_tagging_harness.py:33`) has `O'SHEA` only. The model has no way to
link an unnamed descriptor to a name introduced later, and the cue text
`HISPANIC` becomes a speaker name directly.

**Same class as** findings 2 and 5 (coverage/attribution gaps between
the parser's speaker labels and the real cast): a label the pipeline
treats as an identity is not one.

**Status: merged (author-confirmed).** All three labels are now O'SHEA:
scene153_beat1 on the beat's own naming, scene151_beat1 on scene
continuity only (same unbroken INT. CAR scene running into scene153; its
text says only "unseen driver"). The two scene154_beat2 entries are
merged into one provisional ordinary_reaction entry (`FOG_JOHN_REVIEW.md`
chunk 3 note). `source_evidence` is left as the parser produced it:
scene154_beat2's `characters_present` and turn 8's speaker still read
`HISPANIC`, matching the script's cue. No parser or harness change.

O'SHEA now has 13 beats as one character, including real dramatic
material (the scene155 dialogue sequence in John's car, the scene181
wake beat), so he's added to the review queue below.

## 7. scene185_beat2: MARCHAND's line split by a blank line, second half stored as unattributed action (logged 2026-09-28)

**Found during:** JOHN review chunk 4 (`FOG_JOHN_REVIEW.md`), checked
against a fresh `pdftotext -layout -enc UTF-8` pull (byte-identical to
`fog_full.txt`), lines 5780-5783.

**Raw source:** one line of speech under a single `CAPTAIN MARCHAND
(CONT'D)` cue, "Your father would be very proud of", then a blank line,
then "you, John. Understand me?". There's no page break between them. Both
dialogue lines sit flush-left in the layout pull, not at the usual
dialogue indent, even though the cue above them is indented normally.

**Stored:** turn 17 of `scene185_beat2` is MARCHAND dialogue ending "...very
proud of". Turn 18, "you, John. Understand me?", is stored as an `action`
turn with `speaker: null`. The words are intact but no longer attributed
to MARCHAND.

**Same class as** finding 5: a break inside one speech (there a
parenthetical, here a blank line) cuts off the speaker attribution for
what follows, with no visible error.

**Status:** documented only. No parser fix, no re-parse, and not checked
for other occurrences in Full of Grace.

**Additional occurrence (logged 2026-09-29):** scene64_beat8, CHEYENNE. Found
during the finding 20 scan (TRUDY Pass 2 review batch 2). In
`fog_full.txt` lines 2138-2141, a `CHEYENNE (CONT'D)` cue is followed by "I
understand if you don't want to", then a blank line, then "help.". As here,
the dialogue lines sit flush-left. Stored turn 25 of `scene64_beat8`, "help.",
is an `action` turn with `speaker: null`, and the dialogue turn before it ends
"...don't want to". Same mechanism as the MARCHAND case, and also documented
only.

**Third occurrence (logged 2026-09-29):** scene56_beat3, DOUG. Found while
checking the scene56 porch scene during TRUDY's final Pass 2 batch. In a
fresh `-layout` pull, a `DOUG (CONT'D)` cue is followed by "Yeah. Got our own
problems here in", then a blank line, then "Dover, I guess, right?". Stored
turn 21 is DOUG dialogue ending "...here in", and turn 22, "Dover, I guess,
right?", is an `action` turn with `speaker: null`. Documented only.

**Fourth and fifth occurrences (logged 2026-09-30):** scene175_beat1 and
scene175_beat2, REGGIE. Found while assembling JOHN Pass 2 batch 3's
material, checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). Pages 104-105 print dialogue flush-left
under normally indented cues.
- scene175_beat1: after the page-break `REGGIE (CONT'D)` cue (line 5541),
  "Christmas gifts, birthday", then a blank line, then "parties... Days at
  the beach." (5542-5544). Stored turn 5 is REGGIE dialogue ending
  "...birthday", and turn 6, "parties... Days at the beach.", is an `action`
  turn with `speaker: null`.
- scene175_beat2: after `REGGIE (CONT'D)` (5576), "In this topsy-turvy
  world... you", then a blank line, then "gotta have God on your team..."
  (5577-5579). Stored turn 16 is REGGIE dialogue ending "...you", and turn
  17 is an `action` turn with `speaker: null`. This one was missed in the
  first batch 3 report and caught while writing up the scene175_beat1
  occurrence.

Documented only. No verdict depends on either occurrence: both are Reggie's
lines, and JOHN's queued scene175_beat1 verdict rests on "Let me make a
call." (5562), which is stored intact.

**Minor gap, same scene (noted 2026-09-30, not urgent):** Reggie's
"(smiles)" parenthetical (line 5537, after "...like she was his own..." and
before the page-break `(MORE)`) is absent from the stored turns. Stored
turn 4 has `paren: null`. This is the dropped-parenthetical side of the
family (findings 5 and 16). The batch 3 reverse check didn't catch it: that
check stripped parentheses and matched the bare word anywhere in the stored
text, and "smiles" occurs elsewhere. It was caught by reading the raw pull
directly.

**Sixth occurrence (logged 2026-09-30):** scene14_beat4, OFFICER. Found
while assembling JOHN Pass 2 batch 4's material, checked against a fresh
`pdftotext -layout -enc UTF-8` pull. After an `OFFICER (O.S.) (CONT'D)` cue
(line 384), "Streets are blind as usual. Buncha", then a blank line, then
"amnesiacs." (385-387), on a flush-left page. Stored turn 11 is OFFICER
dialogue ending "...Buncha", and turn 12, "amnesiacs.", is an `action` turn
with `speaker: null`. Documented only. No verdict depends on it: John's own
"See no evil, hear no evil, and you will survive." (392-393, turn 14) is
stored intact. But this beat is the first-shown beat of JOHN's
willful-blindness trait and the comparison anchor for scene185_beat2 and
scene223_beat1. It's another comparison-edge defect of the kind finding
20's 2026-09-30 update describes.

**Seventh occurrence (logged 2026-10-02):** scene94_beat2, REGGIE. Found
while assembling REGGIE Pass 2 batch 1's material, checked against a fresh
`pdftotext -layout -enc UTF-8` pull (byte-identical to `fog_full.txt`).
After a `REGGIE (O.S.) (CONT'D)` cue (line 3000), "But you were good, John.
Real good." (3001), then a blank line, then "You had tremendous talent."
(3003), on a flush-left page. Unlike the earlier occurrences, the split
also falls on a **beat boundary**. "But you were good..." is the last
REGGIE dialogue turn of scene94_beat1 (turn 11). "You had tremendous
talent." opens scene94_beat2 as turn 12, an `action` turn with `speaker:
null`. Documented only. No verdict depends on it. scene94_beat2 is the
first-shown beat of REGGIE's trait 6, and its trait-6 lines (3008-3022)
are stored intact. Caught by reading the raw pull directly, not by either
automated check (see the detection gap below).

**Detection gap, to fix in the check itself, not just note as another
instance:** this occurrence was caught only by reading stored turns directly.
Neither automated check caught it:

- **Finding 16's reverse-coverage check** compares parsed text against stored
  turns for *missing* text. A blank-line split loses no words, only the
  speaker, so this check can't see it.
- **The action-in-speech check** used in the TRUDY Pass 2 review (flag a stored
  `action` turn whose raw line sits under a speaker cue) walks upward from the
  action line and **stops at the first blank line**. A blank-line split puts a
  blank line exactly between the cue's dialogue and the split-off text, so
  the check misses this whole class by design, anywhere in the script.

A future parser-hardening pass should change that check to continue past a
single blank line when the line above it is dialogue under an open cue and
no new cue, slugline or action paragraph intervenes. Then re-run it
script-wide. It is part of the finding 20 family search.

## 8. Reggie described as John's "partner" in scene172: an invented relationship (logged 2026-09-28)

**Found during:** JOHN review chunk 4.

**Stored (cold output):** the JOHN fields on two scene172 beats call
Reggie John's partner:

- `scene172_beat2` self_perceived: "confronting his partner's corruption".
  audience_perceived: "a lawman risking his partner's wrath to protect an
  innocent victim".
- `scene172_beat8` audience_perceived: "a partner instinctively running
  toward danger to save his friend". The self_perceived and goal on this
  beat ("rushing to protect Reggie", "reach and protect Reggie") rest on
  the same premise.

**Raw source:** the text never calls Reggie John's partner. What it gives is
Reggie's own "Your father was my buddy. My man!" (scene172_beat5).
Author-confirmed: Reggie is a close friend of John's late father Mackie,
not John's partner. So the model invented a relationship. This is not a
parse error: the stored turns are complete and correctly attributed.

**Scope check:** a search for "partner" across every per_character
field for JOHN and REGGIE, and every character in scene172, found only
two other hits: JOHN on `scene101_beat1` ("dismissing his partner's
legitimate warnings") and `scene199_beat1` ("managing a partner's
emotional outburst"). Both refer to Doug, not Reggie.
O'SHEA/CHEYENNE uses (romantic partner) were excluded from the search.

**Scope extended to Doug (chunk 4 follow-up, 2026-09-28):** `fog_full.txt`
never uses the word "partner" (0 hits, any case). Author-confirmed: Doug
is a Dover PD officer in a relationship with Trudy. He and John are both
working the Holly Roberts case, but they are not official partners. So
the Doug uses are the same invented relationship. JOHN's
audience_perceived on `scene101_beat1` and `scene199_beat1` now says
"Doug" instead of "partner" (wording only, no tag change).

**Wider scan (report only, nothing changed):** on beats where DOUG is
present, "partner" also appears in other characters' fields, all in
DOUG's own entries: `scene83_beat1` ("a cooperative partner"),
`scene86_beat2` ("a partner trying to keep the investigation moving
despite doubts"), `scene86_beat3` ("a steady, unbothered partner
absorbing a dig without escalation"), `scene101_beat1` self_perceived
("trying to steer his partner away from a reckless,
jurisdiction-violating move..."), `scene123_beat3` ("a partner calmly
reporting information, unfazed by John's reaction") and `scene175_beat2`
self_perceived ("delivering hard news to a partner as gently as he
can"). So the error is wider than JOHN's fields. These are left for
DOUG's own review.

**See also** finding 14: the same scene's REGGIE fields invented an occupation for him ("a cop", a "professional front").

**Status:** fixed on the four JOHN beats in JOHN review chunk 4.

**Sweep complete (2026-09-28):** all 6 DOUG instances from the wider scan
are now fixed. scene101_beat1 was fixed in DOUG's review, where its
fields were rewritten along with the Mentor -> Chorus change. The other 5
are untagged beats and got a wording-only fix ("partner" -> "colleague"),
logged: scene83_beat1, scene86_beat2, scene86_beat3 and scene123_beat3
(audience_perceived) and scene175_beat2 (self_perceived). A re-scan of
every DOUG entry finds no "partner" left. The O'SHEA/CHEYENNE uses
(romantic partner) are correct and stay.
scene172_beat2: fields rewritten, and in the chunk 4 follow-up its Hero
went to ordinary_reaction (see finding 10). scene172_beat8: Hero ->
ordinary_reaction, fields rewritten to pursuit. scene101_beat1 and
scene199_beat1: wording only.

## 9. scene206_beat1: fields asserted a goal and emotions the beat doesn't show (logged 2026-09-28)

**Found during:** JOHN review chunk 4. This is a post-fix re-run beat
(finding 3).

**Stored:** JOHN's goal is "Continue pursuing Trudy himself" (violated).
audience_perceived is "a man swallowing rage and desperation to avoid
further consequences" and "compliance masking real anguish over Trudy",
and emotion includes "suppressed anger" and "desperation".

**Raw source:** the beat is four turns: "John's had enough. He goes to
leave. Captain stops him." / "I've issued an APB." / "I understand." / "All
due respect, John, just so we're clear: you had your shot at this. Let us
handle Trudy." It shows no pursuit of Trudy, rage or anguish. Before this
beat, the script never has John state or show suspicion of Trudy. The
fields appear to have been inferred from later events in the story.

**Status:** documented only. The planned scene206_beat1 field changes
were held at the step-2 check (`FOG_JOHN_REVIEW.md` chunk 4). The stored
fields are unchanged.

**Update (chunk 4 follow-up, 2026-09-28):** the author confirms that at
this point John wants to get to the bottom of Trudy's involvement, so the
goal isn't invented. But "Continue pursuing Trudy himself" overstates
it, since the pursuit happens in later beats, and "rage" and "anguish"
aren't shown. Fields replaced (goal "get to the bottom of Trudy's
involvement", still violated; emotion frustration, determination).
scene206_beat1 is applied, Persona confirmed (`FOG_JOHN_REVIEW.md` chunk 4).

## 10. Hero placed on the wrong beat of a confrontation, twice (logged 2026-09-28)

**Found during:** JOHN review chunks 3 and 4.

**Stored (cold output):** in two confrontations the cold run put JOHN's
Hero tag on a beat next to the act rather than on the act itself.

- **scene154:** Hero landed on the aftermath beat (scene154_beat3),
  not on the disarming (scene154_beat2). Both are now ordinary_reaction
  on the collusion plot fact (chunk 3), but the placement was wrong
  independently of that.
- **scene172:** Hero landed on the argument beat (scene172_beat2), not
  on the acts: raising the rifle (beat 3), levelling it (beat 4),
  shielding with the door and returning fire (beat 6), and ducking back
  to check on Alberto (beat 7). Corrected in the chunk 4 follow-up: beat
  2 is now ordinary_reaction and beats 3, 4, 6 and 7 are Hero.

**Related to** the Hero definition's rule that declared intent is not the
act (`tagging_schema.py`, "DECLARED INTENT IS NOT THE ACT ITSELF ... The
tag belongs on the beat where the courageous action is actually
taken"). The cold output tagged the beat where resolve is voiced or its
result is felt, not the beat where the action happens.

**Status:** documented only. No prompt change.

## 11. scene30_beat1: Trudy recognizes a man at the soup kitchen, and no later scene pays it off (logged 2026-09-28)

**Found during:** TRUDY review chunk 1. This is a continuity note on the
script, not an archetype or pipeline finding.

**Source (p. 19):** "Trudy hands a bowl to the next man in line. A look of
recognition on her face." Then: "The man's face goes unseen to us, as he
sheepishly takes the bowl of soup, turns, and walks off. / Trudy watches
after the man for a beat." Author-confirmed: the man is Raymond, and the
recognition is deliberate setup.

**Payoff check (fresh `pdftotext -layout` pull):** the soup kitchen
appears only in this scene. No later scene returns to it, shows Trudy and
Raymond meeting, or explains the recognition. Trudy's confession ("I
hired Raymond to take her") doesn't say how she knew him. The closest
later lines:

- p. 108, Captain Marchand on Raymond: "with no known fixed address, we
  just haven't had any promising leads, aside from occasional sightings
  at homeless shelters, churches."
- Raymond's interrogation, Federal Agent: "Yeah, we know Trudy was
  helping you, Raymond." and "You came to Trudy for help. You came to
  the church for help."

Neither line refers back to the soup kitchen or the recognition.

**Status:** documented only. Nothing applied.

## 12. scene216_beat6: TRUDY's Creed line garbled by a two-column `-layout` extraction and stored as unattributed action (logged 2026-09-28, repaired)

**Found during:** TRUDY review chunk 2.

**Stored (cold output):** turn 11 of scene216_beat6 was `kind: action`,
`speaker: null`, with the text
`"TRUDY (CONT'D)  the -- the holy Catholic Church,     life communion of saints, the forgiveness of sins, the resurrection of the body, and everlasting?"`.
The character cue was folded into the text, and "the" and "life" were
out of place.

**Cause:** at the top of p. 123, `pdftotext -layout` splits the speech
into two columns: "the" and "life" land at the right of the cue and first
lines. `fog_full.txt` has the same garbling, so the parser never saw a
clean cue. A `pdftotext -raw` pull of the same page reads in order:
"TRUDY (CONT'D) / -- the holy Catholic Church, the / communion of saints,
the / forgiveness of sins, the / resurrection of the body, and life /
everlasting?". pdftotext -layout can garble text near page-corner
artifacts like this, which is the same risk the parser notes flag for
`-layout`, in a different form.

**Repair applied (Ocean's Eleven convention, `OCEANS11_OPEN_ITEMS.md`
findings 1 and 6):** turn 11 is now `kind: dialogue`, `speaker: TRUDY`,
text "-- the holy Catholic Church, the communion of saints, the
forgiveness of sins, the resurrection of the body, and life
everlasting?", matching the `-raw` pull. No turns were inserted or
re-indexed. This is a text-completeness fix only, applied to
`source_evidence`, with no corrections-log entry. The beat's archetype
correction (Shadow -> Great Mother, `FOG_TRUDY_REVIEW.md` chunk 2) is
logged separately. `fog_full.txt` and `fog_parsed_scenes.json` are
unchanged.

## 13. scene140_beat8: YOUNG JOHN labeled "JOHN" inside a flashback (logged 2026-09-28, fixed)

**Found during:** MACKIE review.

**Stored (cold output):** scene140_beat8's second per-character entry was
labeled `JOHN`. Every other beat in this flashback (all of scene 75 and
the rest of scene 140) uses `YOUNG JOHN`. The beat is one action line,
"John struggles, but can't break free. Mackie's grip hardens.", with no
character cue. That leaves `characters_present` empty, so the model took
the name from the action text.

**Same class as** finding 6 (O'SHEA split across HISPANIC, DRIVER and
O'SHEA): the same person stored under more than one label.

**Fix applied:** the entry is relabeled `YOUNG JOHN`, logged as a
`character` correction (`JOHN` -> `YOUNG JOHN`), the same way as finding
6's merge. This is data consistency, not a judgment call, and no other
field on the entry changed. `characters_present` stays empty (FUTURE_WORK
item 1).

## 14. Reggie described as a cop with a "professional front" in scene172: an invented occupation (logged 2026-09-28, fixed)

**Found during:** REGGIE review.

**Stored (cold output):** REGGIE's own fields:

- `scene172_beat2` audience_perceived: "a cop's brutal, racist vigilante
  cruelty breaking through his professional front".
- `scene172_beat1` audience_perceived: "... break through whatever
  professional or personal facade he once had".

**Raw source (fresh `pdftotext -layout` pull):** no line makes Reggie a
cop. He is introduced as "a man, 60's, in a U.S. Marines uniform. He's
REGGIE." O'Shea calls him "that old Army cat" and "Him and his cop
buddy", where the buddy is Mackie. Captain Marchand calls him "Mr.
Reginald Lund." So the model invented an occupation. This is not a parse
error.

**Same class as** finding 8, where the model invented Reggie as John's
"partner" in the same scene: a relationship or role the text never
states, inferred from context and then used as the frame for the tag.

**Scope check:** a search of every REGGIE field for cop, cops, officer,
police, policeman, lawman, professional, badge and detective found only
the two scene172 entries above. In other characters' fields, the only hit
that describes Reggie is scene155_beat9's O'SHEA audience_perceived
("fear of corrupt cops"). That is a plural covering Mackie and Reggie,
drawn from O'Shea's own "Him and his cop buddy" / "Pullin' me over", and
it is left as stored. The other hits (scene94_beat3, scene95_beat1,
scene165_beat1 and scene172_beat2, all JOHN) describe John.

**Status:** fixed. Both scene172 entries changed from Shadow to
ordinary_reaction, with fields rewritten (`FOG_REGGIE_REVIEW.md`). The
"cop" and "professional" wording is gone.

**Recurrence in an instruction (noted 2026-10-02, no data change).** The
author's pasted instruction for REGGIE Pass 2 batch 2 described Reggie's
established pattern as "local cop". It was caught against this finding
before anything was applied: the log 766 note and `FOG_REGGIE_REVIEW.md`
Batch 2 both record the correction. This is the occupation's second
appearance overall: first in the cold model output (this finding), then
in an instruction. The repo has no record of an earlier instruction
occurrence. Flagged only, so the pattern is visible if it recurs a third
time.

## 15. scene123_beat5: DOUG's line garbled by a two-column `-layout` extraction, and his next line lost (logged 2026-09-28, not fixed)

**Found during:** CHEYENNE/ANGIE/DOUG enumeration.

**Stored (cold output):** two separate problems on the same beat.

1. **Garbling (same class as finding 12).** At the top of p. 77,
   `pdftotext -layout` splits DOUG's speech into two columns. Stored turn
   14 is `kind: action`, `speaker: null`:
   `"DOUG          got John. Guy's a nobody. OK? He's  take nothing to do with Holly. Just  ya? a damn break for a while, will"`.
   A `pdftotext -raw` pull reads, in order: "DOUG / John. Guy's a nobody.
   OK? He's got / nothing to do with Holly. Just take / a damn break for
   a while, will ya? / (pause) / You gave it your best shot."
2. **Content loss.** DOUG's next line, "(pause) You gave it your best
   shot.", is missing from the beat's stored turns entirely.
   `fog_parsed_scenes.json` has it with speaker JOHN (a JOHN parenthetical
   followed by JOHN dialogue), because the cue was folded into the
   garbled action above. It never reached `source_evidence`. So John's
   stored reply, "Excuse me? My best shot?", reacts to a line the record
   doesn't contain, and DOUG has no entry on the beat.

**Detection gap:** the verification used in the character reviews checks
that each stored turn's text exists in the fresh PDF pull. It does not
check the reverse, that the PDF text for a beat's span exists in the
stored turns. Garbled text still passed (the stored text matched the
equally garbled `-layout` pull), and the dropped line was invisible to
it. It was caught only because the printed passage showed the line.
Future checks should also compare the PDF span against the stored turns
(a reverse coverage check), and should not treat a `-layout` match as
proof when that pull is garbled.

**Status:** repaired 2026-09-28, before Pass 2, following finding 12's
convention (text-completeness fix to `source_evidence` only, no
corrections-log entry; `fog_full.txt` and `fog_parsed_scenes.json`
unchanged). Turn 14 is now `kind: dialogue`, `speaker: DOUG`, with the
text "John. Guy's a nobody. OK? He's got nothing to do with Holly. Just
take a damn break for a while, will ya? (pause) You gave it your best
shot.", taken from the `-raw` pull. The mid-speech parenthetical is
inlined, following the beat detector's convention. `characters_present`
now includes DOUG. No turns were inserted or re-indexed. A reverse check
of scene 123 now finds no PDF text missing. **Still open:** DOUG has no
`per_character` entry on this beat. Adding one is a tagging judgment,
not part of this repair. Until then, Pass 2's DOUG arc doesn't include
this beat.

## 16. scene19_beat2: a two-line parenthetical drops JOHN's coaching line (logged 2026-09-28, not fixed)

**Found during:** the reverse check (PDF text against stored turns, per
finding 15) on the 8-character batch.

**Stored (cold output):** on p. 14, JOHN's dialogue is interrupted by a
parenthetical that wraps onto two lines, "(hands Latino Kid the / ball)".
The parser stores that parenthetical as action, then stores JOHN's next
line, "Tuck your thumb and finger together, like a circle.", as an
unattributed action. `fog_parsed_scenes.json` does have the chunk after
it under JOHN: "(Latino Kid does it) That's it. Now, when you release the
ball, keep your back leg solid, don't be jumping off too much. This'll
control the speed of the pitch and it'll fool him into thinking it's a
fastball." But without a cue in front of it, that chunk never reached the
beat's stored turns. Same drop mechanism as finding 15.

**Impact:** it sits on JOHN's scene19_beat2, where Mentor was already
confirmed in chunk 1. Author's call: enough coaching content survives
elsewhere in the beat ("So here's your grip...", the grip demonstration,
"Tuck your thumb and finger together, like a circle.", "As hard as you
can.") that the Mentor verdict is unaffected.

**Scope check:** a script-wide comparison of every parsed dialogue and
action element against the stored turns found only 3 missing: this one,
finding 15's line, and finding 12's garbled original (replaced by its
repair, so expected). A script-wide scan of the layout pull for
two-column lines found only finding 12's and finding 15's lines and the
two hand-patched dual-dialogue blocks (scenes 120 and 143).

**Status:** repaired 2026-09-28, before Pass 2, following finding 12's
convention (`source_evidence` only, no corrections-log entry, parsed
scenes unchanged). The `-raw` pull of p. 14 confirms all of it is one
JOHN (CONT'D) speech. Turn 22 now holds it in full, with the two
parentheticals inlined: "See? Now you do it. (hands Latino Kid the ball)
Tuck your thumb and finger together, like a circle. (Latino Kid does it)
That's it. Now, when you release the ball, ... fool him into thinking
it's a fastball." Turns 23 (the parenthetical stored as action) and 24
(JOHN's line stored as unattributed action) duplicated text now in turn
22, so they were removed. The other turns keep their indices, so 22 is
followed by 25. No evidence signal referenced turns 23 or 24. A reverse
check of scene 19 now finds no PDF text missing.

**Rollup: one systemic bug class, five documented occurrences.** Findings
5, 7, 12, 15 and 16 are the same kind of failure. Dialogue is interrupted
by something between the cue and the rest of the speech: a page break
(5), a blank line (7), a two-column layout split (12, 15) or a wrapped
parenthetical (16). The text after the interruption is then dropped or
stored as unattributed action. Flag this as one systemic finding with
five occurrences when the full character review closes.

**Update (2026-09-29):** the interrupted-dialogue class now has six
documented occurrences, with scene64_beat8 added under finding 7. Finding
20 is a related but separate failure. It splits *uninterrupted* dialogue,
so it isn't a seventh occurrence of this class. See finding 20 for why the
two should still be searched for together.

## 17. Pass 2 synthesis validator silently forced "escalation" onto 13 turning points the model never claimed as escalations (logged 2026-09-29, validator fixed, drafts not corrected)

**Run:** the completed FOG Pass 2 run (commit `8079f93`; synthesis
outputs in `fog_pass2_calls/synthesis_*.json`, raw model text in
`synthesis_raw_*.json`, log in `fog_pass2_run.log`). Found from saved
data only. No API calls were made for this finding.

**Mechanism:** `synthesize_character_arc()` in `pass2_orchestration.py`
had two repair paths, both added so that one bad entry would not
discard a whole paid synthesis call (one $0.29 call had been lost to a
hard rejection):

- **AUTO-DOWNGRADE:** `if tp_type == "continuation" and comparison not in tp_beat_ids: tp["turning_point_type"] = "escalation"`.
  This fires on a continuation whose comparison beat is not itself in
  the turning_points list.
- **AUTO-HEAL:** `if tp_type in category_values: ... tp["turning_point_type"] = "escalation"`.
  This fires when the model wrote a likely_category value
  (`boundary_revealed` etc.) into turning_point_type. Moving that value
  into likely_category is a legitimate repair: in all 8 cases the model
  had also written the same value there. Defaulting the type to
  "escalation" is not.

Both paths overwrote the field in place. The only trace was a printed
log line. The code comment called the downgrade "a strictly WEAKER
version of the model's own claim." It isn't. Escalation asserts
*clearly greater scale, cost or risk*, which is a different claim that
none of these 13 entries makes. The resolution prompt then showed the
resolver `[escalation vs. X]`.

**AUTO-DOWNGRADE, 5 entries.** Every `what_changes` text describes an
unbroken sequence, not a magnitude increase:

| Character / beat | vs. | Stored what_changes (excerpt) | Draft outcome |
|---|---|---|---|
| TRUDY scene57_beat3 | scene57_beat2 (adjacent) | "silent evasion ... continues unbroken ... extending the same unresolved evasion" | consistent |
| JOHN scene103_beat1 | scene101_beat1 | "the immediate follow-through of the same choice" | **throughline_evolution**, "extending the trait via continuation (Principle 7)" |
| REGGIE scene94_beat3 | scene94_beat2 (adjacent) | "immediately continues ... the same exchange without a break" | consistent |
| O'SHEA scene155_beat7 | scene155_beat6 (adjacent) | "In the same unbroken exchange ... extending the same moment" | consistent |
| YOUNG JOHN scene75_beat2 | scene75_beat1 (adjacent) | "The same conversation continues unbroken ... directly extending" | consistent |

TRUDY's synthesis predates raw-output saving, so its original
"continuation" label survives nowhere on disk. JOHN, REGGIE, O'SHEA and
YOUNG JOHN are confirmed "continuation" in their `synthesis_raw_*.json`.

**AUTO-HEAL, 8 entries across 4 characters.** Every one was
`boundary_revealed`, and every `what_changes` describes a limit
exposed, not a bigger version of the same trait. MANAGEMENT's text
explicitly says "a previously untested limit rather than a new capacity
or escalation of the same behavior."

| Character / beat | vs. | Draft outcome |
|---|---|---|
| JOHN scene108_beat1 | scene103_beat1 | boundary_revealed / mismatch |
| JOHN scene175_beat1 | scene172_beat7 | boundary_revealed / matched |
| JOHN scene138_beat2 | scene13_beat1 | boundary_revealed / matched |
| JOHN scene213_beat3 | scene37_beat5 | boundary_revealed / matched |
| DOUG scene101_beat1 | scene57_beat3 | throughline_evolution / matched (resolved on DOUG's *other*, genuine escalation entry for this beat, vs. scene71_beat1; the healed boundary claim appears only as a secondary note) |
| DOUG scene197_beat2 | scene123_beat14 | boundary_revealed / matched |
| RAYMOND scene201_beat5 | scene196_beat1 | boundary_revealed / matched |
| MANAGEMENT scene107_beat2 | scene103_beat1 | no draft. That entry has no causal_integrity block, so it was not a resolution target |

An earlier Claude Code session summary miscounted these as 9. The run
log records 8: JOHN 4, DOUG 2, RAYMOND 1, MANAGEMENT 1.

**Impact:** the resolver mostly read through the forced label. It
rejected 4 of 5 downgraded entries as consistent, and it judged 6
healed entries on likely_category. **One confirmed leak:** JOHN
scene103_beat1 was drafted `throughline_evolution` on continuation
grounds, but continuation requires scene101_beat1 to be a turning
point, and the validator had already found that it isn't.

A pattern worth noting, not acted on: all 8 heals are
`boundary_revealed`. The three types (escalation / continuation / echo)
have no shape for "the trait held at X and breaks here." The model may
be reaching for the category because no type fits, rather than making a
random field mix-up.

**Fix (2026-09-29, uncommitted at time of writing):** validation now
lives in `validate_turning_points(analysis, turning_points)`, a pure
function that makes no calls. Neither slip is relabeled any more:

- If the comparison beat is the immediately preceding beat in the same
  scene, the entry is dropped from turning_points (the trait continuing
  to operate) and kept in `dropped_turning_points` with `dropped_reason`.
- Otherwise the entry is kept with its original claim. A dangling
  continuation stays "continuation". A healed entry gets
  `turning_point_type: None`, because no type was claimed. Both get
  `validation: "unverified -- ..."` and `requires_human_review: true`.
  The resolution prompt renders these as UNVERIFIED and tells the
  resolver not to treat them as any of the three types.
  `fog_pass2_runner.py` prefixes those beats' draft notes with
  "MANDATORY HUMAN REVIEW".
- Every entry records `model_turning_point_type`.

The fix was re-run offline against all saved raw synthesis outputs. It
drops REGGIE scene94_beat3, O'SHEA scene155_beat7 and YOUNG JOHN
scene75_beat2, and flags JOHN scene103_beat1 plus all 8 healed entries.
TRUDY cannot be re-run (no raw output), but its comparison beat is
adjacent, so it would drop. The saved `synthesis_*.json` files and
`fog_tagged.json` drafts from this run are **not** rewritten. They stay
the cold record.

**Mandatory human Pass 2 review. Correct via `log_correction()` during
the review, not before:**

1. **JOHN scene103_beat1**: the confirmed leak. The drafted
   throughline_evolution rests on an invalidated continuation claim.
2. TRUDY scene57_beat3, REGGIE scene94_beat3, O'SHEA scene155_beat7,
   YOUNG JOHN scene75_beat2: drafted consistent after the resolver
   rejected an escalation the model never claimed. The outcome is
   likely right, but confirm it.
   **Status (2026-10-03): all four confirmed consistent** (no-op, no log
   entries): TRUDY in `FOG_TRUDY_REVIEW.md`, REGGIE in
   `FOG_REGGIE_REVIEW.md`, O'SHEA in `FOG_OSHEA_REVIEW.md`, YOUNG JOHN in
   `FOG_YOUNGJOHN_REVIEW.md`.
3. JOHN scene108_beat1, scene175_beat1, scene138_beat2, scene213_beat3;
   DOUG scene197_beat2; RAYMOND scene201_beat5: drafted
   boundary_revealed with a forced type. Check each on its own evidence.
   JOHN scene213_beat3 reads more like an echo (a callback to the
   scene37_beat5 "No") than any magnitude change.
   **JOHN status (2026-10-01): all four reviewed.**
   - scene108_beat1 -> consistent (WP -> matched).
   - scene175_beat1: boundary_revealed confirmed.
   - scene138_beat2: boundary_revealed confirmed, reasoning corrected.
   - scene213_beat3 -> consistent. It is neither an echo nor a boundary:
     it is the first showing of a separate reciprocal-honesty trait, and
     the scene37_beat5 comparison is the wrong trait.

   See `FOG_JOHN_REVIEW.md`.
   **RAYMOND status (2026-10-03): reviewed.** scene201_beat5 -> consistent
   (log 839). The forced escalation doesn't hold on its own evidence: it is
   trait 6's plea ("Stop it!") under the agent's slurs, not trait 4
   cracking. See `FOG_RAYMOND_REVIEW.md`.
   **DOUG status (2026-10-02): reviewed.** scene197_beat2 -> consistent
   (log 779), the first showing of a new trait. See `FOG_DOUG_REVIEW.md`.
4. DOUG scene101_beat1: two synthesis entries, one of them healed. Check
   that the draft addresses the boundary claim (vs. scene57_beat3), not
   only the escalation.
   **Status (2026-10-02): reviewed.** throughline_evolution confirmed on
   claim (a); the healed boundary claim (b, trait 4) does not hold
   (no-op, notes). See `FOG_DOUG_REVIEW.md`.
5. MANAGEMENT scene107_beat2: an orphaned turning point with no
   causal_integrity block to draft into. Decide whether it needs one.
   **CLOSED (2026-10-03, author-confirmed): no block needed.** The
   orphaned turning point fails: "What's going on?" (3454) and "Hey!"
   (3460) are a reaction to John racing out (3456), something that
   happens TO the character and a universal reaction. scene107_beat2
   stays without a causal_integrity block. See `FOG_MANAGEMENT_REVIEW.md`.

**All five items are now reviewed (2026-10-03).**

Quoted lines inside model text in these entries ("I ain't proud to say
it", "Let me make a call", "Stop it!") have not been checked against the
script. Verify them against source before using them to justify any
correction. **Update (2026-10-03):** "Mr. Matthews" is cleared from this
list (verbatim at 3292, 3361, 3366; see `FOG_MANAGEMENT_REVIEW.md`). The
other three were also found verbatim in `fog_full.txt` during the same
check: "Crickets. I ain't proud to say it," (5032), "Let me make a call."
(5562), "Stop it!" (6148, already verified in `FOG_RAYMOND_REVIEW.md`).

Finding 18 covers the same class of defect at resolution time, with a
worked example of its cost on TRUDY.

## 18. Pass 2 resolver declares "continuation of X" in free text with no validation, and continuations inherit boundary_revealed without a Principle 8 retest (logged 2026-09-29, not fixed)

**Run:** the same completed FOG Pass 2 run as finding 17 (`8079f93`).
Found from saved data only (`fog_pass2_calls/resolution_*.json`,
`synthesis_*.json`, `fog_tagged.json`). No API calls were made.

**Mechanism:** the resolution output has no structured turning-point
type or comparison field. "Continuation of X" appears only in the
free-text `checked_against` field, whose spec is "which established
trait or turning point you compared this beat to"
(`pass2_orchestration.py`, `PASS2_VOCABULARY_INSTRUCTIONS`).
`parse_pass2_response()` checks only the enum values and the set of
beat IDs, and stores `checked_against` unread. Two principles legitimize
the move. Principle 7 makes continuation a real shape, and Principle 9
offers "(or a continuation of an already-identified turning point)" as
an outcome. Nothing checks that X is:

- (a) a real synthesis turning point,
- (b) itself resolved, meaning drafted, or
- (c) itself non-consistent.

`validate_turning_points()` (finding 17) runs on the synthesis output
before resolution, so it never sees these claims.

**All 9 instances** found by a scan of `checked_against` for
"continuation ... sceneN_beatM" on beats that are not synthesis turning
points for that character. Phrasings that name no beat are not caught
by this scan.

| Character / beat | Continuation of | X is | Draft outcome |
|---|---|---|---|
| JOHN scene119_beat11 | scene119_beat3 | drafted synthesis TP | consistent |
| TRUDY scene189_beat1 | scene188_beat1 | drafted synthesis TP | consistent |
| TRUDY scene190_beat1 | scene188_beat1 | drafted synthesis TP | consistent |
| TRUDY scene192_beat1 | scene188_beat1 | drafted synthesis TP | consistent |
| TRUDY scene215_beat1 | scene214_beat4 | drafted synthesis TP (itself a continuation link) | boundary_revealed |
| TRUDY scene194_beat1 | scene193_beat1 | synthesis TP **never resolved** (no causal_integrity block; worklist `arc_claim_check_no_draft`) | boundary_revealed |
| TRUDY scene195_beat1 | scene193_beat1 / scene194_beat1 | same, never resolved | boundary_revealed |
| TRUDY scene195_beat2 | scene195_beat1 | **the resolver's own earlier, unverified claim** | boundary_revealed |
| TRUDY scene195_beat4 | scene195_beat2 | **the resolver's own earlier, unverified claim** | boundary_revealed |

The 4 consistent drafts are harmless, since consistent is the default.
The 5 boundary_revealed drafts carry a notable verdict whose only
support is the chain. scene195_beat2's own rationale says the sequence
continues "without new development."

**Same underlying defect as finding 17, at a different stage:** a
category is inherited and never retested against the principle that
should gate it. Here that principle is Principle 8: boundary_revealed
needs a *new* limit. Finding 17 was a forced type at synthesis time,
caught by a structured validator. This one happens after resolution,
in free text, where no validator looks.

**The inheritance also runs through the synthesis's own continuation
links,** not only through the resolver's own continuations. The
synthesis stamps `likely_category: boundary_revealed` on each link of a
continuation chain. The resolver applies Principle 7's continuation
test ("is it unbroken?") and keeps the category. Nothing asks whether
the continuing beat itself exposes a new limit.

**Worked example: TRUDY, 19 boundary_revealed drafts, 6 distinct claimed
limits.** Grouped by the limit each entry claims (from stored
`what_changes`, or the resolver's rationale where there is no synthesis
TP). The limits are *claimed*, not verified:

| Limit claimed | First claim | Re-claims (no new limit named in their own text) |
|---|---|---|
| A. Caretaker composure breaks under grief | scene40_beat3 | none |
| B. Hidden depth of prejudice/jealousy (rests on defective trait 6, scene57_beat2) | scene143_beat7 | none |
| C. Private prayer recited in sync with Raymond's | scene193_beat1 (not drafted, outside the 19) | scene194_beat1, 195_beat1, 195_beat2, 195_beat4 (all resolver-declared, this finding) |
| D. Calm faith about infertility was a mask over a crisis of faith | scene213_beat2 | none |
| E. Capacity for premeditated control/violence (defective trait 7, scene213_beat7) | scene213_beat7 | scene214_beat1, 214_beat3, 214_beat4, 216_beat1, 216_beat2, 216_beat4, 216_beat5, 216_beat6 (synthesis continuation links); scene215_beat1 (resolver-declared) |
| F. Premeditated control breaks down into horror | scene216_beat7 | scene217_beat1 (the resolver's own rationale says "a genuine limit to the trait, not a new one") |

That gives 5 first claims inside the 19, plus C's first claim at the
undrafted scene193_beat1, and **14 re-claims**. Of the 14, 5 come
through the resolver-declared path and 9 through synthesis continuation
links.

The two defects compound. The trait 6/7 labeling problem (finding 17's
TRUDY synthesis predates the depict-don't-infer instruction; see
`FOG_TRUDY_REVIEW.md`) shapes what limits B, C and E are claimed to be.
The inheritance problem multiplies them: 6 claimed limits became 19
drafted boundary_revealed verdicts.

Most of the volume is inheritance, not labeling. The E chain would
likely draft boundary_revealed beat by beat under any trait wording,
because it is the drowning sequence itself. For the reviewer:

- Three E re-claims add content beyond "continues": scene214_beat3
  (religious grooming), and 214_beat4 and 216_beat5 (the turn to
  physical violence). Whether that exceeds 213_beat7's "control/
  violence" claim is a judgment call.
- Principle 9 is directly relevant to C. Trudy is still praying; what
  changes is the audience's information.

**Proposed fix (NOT BUILT; decide after the human review, not before):**

1. Add a structured `continuation_of` field to the resolution schema.
   It must name a synthesis turning point that is drafted *and*
   non-consistent in the same run. That rules out orphans such as
   scene193_beat1 and the resolver's own chains.
2. A rule requiring every non-consistent verdict to state its own new
   limit or change, not one inherited from the beat it continues.

**Review impact:** all 5 boundary_revealed drafts above are already in
`fog_pass2_queue.json` (`needs_correction_review`). scene193_beat1 is in
`arc_claim_check_no_draft`, with its dependent drafts listed. Quoted
lines inside model text ("all that was left was the baptism", "I -- I
don't know") have not been checked against the script.

**Follow-up (2026-09-29):** the TRUDY drowning-sequence review
(`FOG_TRUDY_REVIEW.md`, commit `5977504`) resolved 12 of the 19. It
also turned up a vocabulary gap that may sit underneath this
inheritance pattern; see finding 19.

**DECISION (2026-10-03, Pass 2 closeout, author-confirmed): build.** Both
parts of the proposed fix above are approved: (1) a structured
`continuation_of` field in the resolution schema, which must name a
drafted, non-consistent synthesis turning point from the same run, and
(2) the rule that every non-consistent verdict states its own new limit
or change instead of inheriting one from the beat it continues.
Scheduled **before the next cold run on a new script**. Not built yet.
**Evidence:** of the boundary_revealed drafts reviewed from REGGIE's queue
onward, 32 of 34 were overturned (tally at the end of
`FOG_LATINOKID_REVIEW.md`). Across the whole worklist, 47 of the 57
drafted boundary_revealed entries in `fog_pass2_queue.json` did not stay
boundary_revealed.

## 19. The "point of no return" beat: an irrevocable act inside a continuation chain has no clean slot in the vocabulary (logged 2026-09-29; ratification threshold met 2026-10-01, three characters; categorization resolved 2026-10-01, five instances, all boundary_revealed; RATIFIED as Principle 11 2026-10-02 with four instances, scene217_beat1 reassigned to 8a; fifth instance MACKIE scene140_beat6 added 2026-10-03)

**Status (2026-10-02): RATIFIED as Principle 11** in
`CAUSAL_INTEGRITY_PRINCIPLES` (`tagging_schema.py`): "An act can be a
turning point through irreversibility alone, even without violence or
escalated intensity." Four confirmed instances, three characters, all
`boundary_revealed`:
1. TRUDY scene214_beat4
2. JOHN scene172_beat6
3. REGGIE scene172_beat6
4. JOHN scene223_beat1
5. MACKIE scene140_beat6 (**added 2026-10-03**, MACKIE Pass 2,
   author-confirmed; `FOG_MACKIE_REVIEW.md`). Mackie's chokehold on his
   son ("Without warning, Mackie's big powerful hand grabs John's throat,
   squeezing.", 4484-4485), his own physical act. It is the first
   *physical* instance whose irreversibility is relational/psychological
   rather than lethal. JOHN 223_1 was already non-lethal, but it is a
   speech act. Count now: **5 instances, 4 characters**.

**Removed from the ratified list (2026-10-02, author-confirmed): JOHN
scene217_beat1.** It is correctly scored under Principle 8a
(omission-to-commission, a change in the type of act), not under
irreversibility. It joined finding 19 because it surfaced during the same
investigation, not because it independently qualifies under Principle 11.
Its `boundary_revealed` verdict (log 761) is unchanged. The count still
clears the ratification threshold: four instances across three
characters. Where earlier sections of this finding count it as an
instance, they record what stood at the time.

The same session amended Principle 8 with two clauses: 8a (ordinary trait
debut vs. singular climactic action) and 8b (check that the "established
capacity" being escalated is actually the same capacity). Principle 11
answers this finding's open question about speech acts (note 2 below): the
test is contingent vs. unconditional, not physical vs. verbal. Sections
below that call the finding "not yet a principle" are the record as it
stood then. The verification of all five instances against the final
wording is under "Principle 11 verification (2026-10-02)" at the end of
this finding.

**Found during:** TRUDY's Pass 2 review of the drowning sequence
(`FOG_TRUDY_REVIEW.md`). scene214_beat4 ("Holly struggles. Trudy forces
Holly's head overboard.") sits mid-way through an unbroken sequence
whose other beats were correctly judged "same capacity continuing." It
was confirmed as a new limit anyway. Trudy moves from arranging harm
through Raymond, which could still be reversed ("It was just for a few
days... Then we'd let Holly go."), to personally overriding Holly's
active resistance with her own hands, which can never be undone.

**The pattern:** the dramaturgical "point of no return", or irrevocable
act. It's a well-known structure in violent-crime storytelling: a
character crosses from planning or arranging harm to personally
committing an act that can't be undone. The canonical example is
Michael Corleone in the restaurant. It is distinct from both existing
notable shapes:

- **Not ordinary escalation or throughline_evolution.** That is more of
  the same, more intensely. scene216_beat5's strikes are that, an
  escalation of the scene214_beat4 limit.
- **Not ordinary boundary_revealed.** Principle 8 frames that as a
  previously hidden limit, breaking point or weakness surfacing. The
  crossing is about *irreversibility*, not intensity or discovery.

**The vocabulary gap:** the types are escalation / continuation / echo,
and the categories are consistent / throughline_evolution /
boundary_revealed / contradicted. Strictly, "continuation + likely_category
boundary_revealed" can be written, and the synthesis wrote exactly that
on every link of TRUDY's chain. What the vocabulary lacks is any way to
mark **the one link where a continuation becomes a boundary partway
through its own unbroken sequence**, or to name irreversibility as the
reason. That leaves a forced binary. Either the link is "continuation,
inheriting the chain's category", which applied indiscriminately gives
finding 18's inheritance, or it is a free-standing boundary_revealed
whose Principle 8 test (a *new, hidden* limit surfacing) doesn't
describe what happened. This may be a deeper cause of finding 18's
pattern. Even a synthesis pass that checked every beat individually
against Principle 8 would face that binary, and it doesn't fit every
real case.

**Watch for it during the rest of the 160-entry Pass 2 review**
(`fog_pass2_queue.json`). A continuation chain may hold one beat where
the character crosses from could-still-turn-back to can-never-undo-this,
while the surrounding beats are correctly "same trait continuing." The
test is irreversibility: did the character, by their own on-page action
(Hero-rule standard: action, not declared intent), do something that
closes off the way back? Likely candidates to check are JOHN's and
MACKIE's more violent sequences. Record each suspected instance in that
character's review notes, with the beat ID and the text that shows the
crossing.

**Status: named pattern, not a numbered causal-integrity principle.**
This follows the three-instances-before-ratification discipline
(`OCEANS11_OPEN_ITEMS.md`). TRUDY scene214_beat4 is instance 1. If the
same shape recurs in two more characters' reviews, propose it then as a
real principle with a concrete test. That would include how the
irrevocable-act beat should be categorized, and how the continuation
beats around it relate to it.

**Instance 2 (2026-09-30, JOHN Pass 2 batch 3, author-confirmed):** JOHN
scene172_beat6. At scene172_beat5, "Or I'll be forced to defend myself."
(`fog_full.txt` 5452-5453) is still declared intent, fully reversible.
scene172_beat6 is the act: "He pops out of the room and returns fire--"
(5494). The shot lands in scene172_beat7 ("BOOM! Another ear-splitter. A
howl from Reggie.", 5496-5498), and later text confirms it is fatal: "His
chest and shoulder perforated by John's buckshot" (5526-5527), "Lungs
collapsing from buckshot" (5550), and death at scene175_beat2 (5581-5582).
Categorization: the crossing is recorded as `throughline_evolution` at
scene172_beat6. scene172_beat7, where the same shot lands, is `consistent`
as its outcome, not a separate escalation. Full record in
`FOG_JOHN_REVIEW.md` (Pass 2, batch 3).

**How it differs from instance 1.** The moral shape is different: TRUDY's
scene214_beat4 is corrupted caregiving turned lethal, while JOHN's is
self-defense escalating into an irreversible killing during a pursuit he
chose to start. He came to the cabin looking for Reggie after O'Shea and
Cheyenne named him ("It's Reggie, John.", 5040-5051; "Reggie?", 5231).
Structurally, though, it is the same pattern: one beat inside a violent
sequence where the character's own on-page action closes off the way back.
Two unrelated characters with opposite moral framings share the shape, so
this points to a generalizable pattern, not something specific to one arc.

**Count: 2 of the 3 instances** needed before proposing a numbered
principle. Two open questions remain for that proposal. In instance 1 the
crossing sat inside a continuation chain; here it was already
escalation-shaped, so the vocabulary gap described above didn't bite. And
here the act (the trigger pull) and its irreversible consequence (the hit
landing) fall on adjacent beats.

**Instance 3 (2026-09-30, JOHN Pass 2 batch 4, author-confirmed):** JOHN
scene217_beat1, the key exchange: "Trudy realizes. She takes out her car
keys. Her and John make the exchange." (`fog_full.txt` 6582-6583). It
follows Trudy's confession ("Maybe I held her under for too long.",
6552-6555). John hands a confessed killer a vehicle and, on the author's
reading, his own identity to escape with. The page says only "Rental's due
back at the airport in the morning." (6586-6587), not whose name the rental
is in. "Nothing. It's between you and God now." (6593-6594) is declared
intent. The exchange is the act. The surrounding beats are consistent
follow-through: scene217_beat2 ("Goodbye, Tru.") and scene218_beat1 (John
drives Trudy's car away). Recorded as `throughline_evolution` at
scene217_beat1; full record in `FOG_JOHN_REVIEW.md` (Pass 2, batch 4).

**A point of no return does not require violence.** This instance is
knowing legal obstruction chosen as an act of mercy. It differs in kind
from instance 1 (TRUDY scene214_beat4, corrupted caregiving turned lethal)
and instance 2 (JOHN scene172_beat6, self-defense escalating into a chosen
killing). The author judges scene172_beat6 the bigger instance in dramatic
weight, but this is a genuine instance regardless. That makes three
structurally identical instances in three different moral registers:
corrupted devotion, violent self-defense, and merciful obstruction.

**Count against the ratification rule, as written.** There are 3
instances, but across **2 characters** (TRUDY, JOHN, JOHN). The status
paragraph above sets the condition as the shape recurring "in two more
characters' reviews". The three-instances-before-ratification discipline
(`OCEANS11_OPEN_ITEMS.md`) counts instances. The author treats the
threshold as crossed. Whether two instances in one character's arc satisfy
the rule is one of the questions for the dedicated session below.

**Instance 4 (2026-10-01, REGGIE Pass 2, author-confirmed): REGGIE
scene172_beat6, the third character.**
- **The act.** "Reggie takes aim at John's head." (`fog_full.txt` 5484);
  "Reggie pulls the trigger." (5490). Before it, "I ain't breakin' my
  promise!... you've made your choice, Detective." (5480-5482) is declared
  intent, and scene172_beat1-5 are threats he can still walk back ("I'm
  givin' you a chance here, Johnny.", 5425). Firing at a detective's head
  is the irrevocable act, and that holds even though the shot misses
  (John kicks the door closed, 5490-5491).
- **Same beat as instance 2.** It falls in the same beat as JOHN's crossing,
  from the opposite side of the same exchange: Reggie's trigger pull (5490),
  then John's return fire (5494).
- **Recorded as `boundary_revealed`,** scored against REGGIE trait 1
  (loyalty to Mackie's family), with trait 8's lethal-force escalation as
  the mechanism. Reggie turns the violence on the son of the friend he
  claims to honor by committing it. The pressure test passes, with two
  caveats (he created the standoff; the resistance is shown only in his own
  dialogue). Full record is in `FOG_REGGIE_REVIEW.md`; log 759.

**Count against the ratification rule: MET.** The shape has now recurred in
three characters' reviews: TRUDY (scene214_beat4), JOHN (scene172_beat6,
scene217_beat1) and REGGIE (scene172_beat6). That satisfies the status
paragraph's condition of "two more characters" beyond instance 1. The
character-count question raised under instance 3 is settled. Finding 19 is
ready to be proposed as a numbered causal-integrity principle in the
dedicated session below.

How the four instances are categorized now: `boundary_revealed` for
instances 1 and 4, `throughline_evolution` for instances 2 and 3. That
split is still one of the session's questions. **(SUPERSEDED 2026-10-01:
the split is resolved. All five instances are now `boundary_revealed`. See
"Resolution (2026-10-01)" at the end of this finding.)**

**OPEN ITEM (logged 2026-09-30): formalize finding 19 as a numbered
causal-integrity principle, in a dedicated session before FOG's Pass 2
review closes, separate from routine batch work.** Numbering and wording
are NOT finalized. The author's draft direction: "an act can be a turning
point through irreversibility alone, even without violence or escalated
intensity -- the test is whether the character could undo or walk back
this specific action once taken, regardless of how calm or merciful the act
appears on the page." Questions to settle there:
- the character-count question above (SETTLED 2026-10-01 by instance 4,
  REGGIE);
- how the irrevocable-act beat is categorized: the four instances are
  recorded as `boundary_revealed` (instances 1 and 4) or
  `throughline_evolution` (instances 2 and 3);
- how the continuation beats around it relate to it;
- the act/consequence split seen in instance 2.

**Session scope widened (2026-10-01): finding 19 plus the
boundary_revealed criteria.** The author has named four candidate tests
for what qualifies as a turning point or boundary: pressure, facet-reveal,
decision-trigger and downstream-connection. Only two have written
definitions in the record so far:
- **Pressure.** boundary_revealed needs external pressure, duress or force
  meeting resistance. It was applied to JOHN scene213_beat3 and TRUDY
  scene131_beat1, both -> consistent.
- **Downstream-connection.** Does any later script text or analysis record
  reference, build on or explain the beat?

Facet-reveal and decision-trigger need written definitions at the start
of the session.

**Recommended order: check the downstream-connection test FIRST, before
the pressure and facet-reveal tests.** It is a promising candidate for a
textual proxy on scripts where the author isn't available to confirm
intent. It is falsifiable from the text alone and needs no inference about
the author's state of mind. On TRUDY scene131_beat1, a full-script and
full-record search independently reproduced what the author confirmed
directly: an isolated, non-consequential beat. Full record and limits are
in `FOG_TRUDY_REVIEW.md`, "Validation note".

Two limits to carry into the session. It is one case, and it was not
blind: the search came after the author's confirmation. And it has only
been validated in the "no downstream connection -> consistent" direction.

**Other questions for that session (2026-10-01):**
- **The pressure test vs. Principle 8's wording.** Principle 8 says "a
  genuine capitulation, breaking point, or discovered weakness". As
  applied, the pressure test is stricter, and three already-confirmed
  boundary_revealed verdicts involve no external pressure:
  - JOHN scene138_beat2 (cumulative weight, "no proximate trigger");
  - JOHN scene175_beat1 (the freely offered call);
  - TRUDY scene188_beat1 (solitary devotion).

  Either the test is refined (for example, internal pressure counts), or
  those three need another look.
- **Is a point of no return inherently pressure-tested?** Or can it also
  apply to freely chosen irrevocable acts? Instance 3 (JOHN
  scene217_beat1, the key exchange) was freely chosen, so check whether it
  holds under the same test.
- **Instance 4, confirmed 2026-10-01 (see below):** REGGIE
  scene172_beat6. The three-character threshold is met.
- **Author's scope condition for the eventual principle.** It requires a
  character with enough established arc or traits for the crossing to
  carry dramaturgical weight. An anonymous or minimally established
  character firing a weapon gives the audience no baseline to register a
  change against. Record this as an explicit scope condition, not an
  afterthought.

### Resolution (2026-10-01, author-confirmed): the categorization split is resolved

The split above (instances 1 and 4 `boundary_revealed`, instances 2 and 3
`throughline_evolution`) was not a real disagreement. Two JOHN beats had
been scored on intensity when they should have been scored on the type of
act. Once they are corrected, all instances land on `boundary_revealed`,
and a fifth instance is added. The four JOHN reversals are logged as
760-763 (`FOG_JOHN_REVIEW.md`, "Finding 19 resolution"). REGGIE's record is
corrected without a value change (`FOG_REGGIE_REVIEW.md`).

**Retired as independent criteria: the pressure test and the
decision-trigger test.** Two cases show this:
- **Pressure isn't what separates the verdicts.** On scene172_beat6, JOHN
  and REGGIE are under identical external pressure in the same exchange,
  yet they correctly land on different reasoning, decided by something
  else (below).
- **Pressure isn't necessary.** JOHN scene138_beat2 is correctly
  `boundary_revealed` with no pressure and no decision point at all.

The pressure-test reasoning in earlier records (TRUDY scene131_beat1, JOHN
scene213_beat3, REGGIE scene172_beat6) stays as the cold record of what was
argued then. Those verdicts are unchanged. scene131_beat1 and scene213_beat3
each also rest on a first-showing ground, which is axis 1 below.

**The operative test (two axes):**
- **Axis 1, the trait-identity gate.** Is the beat scored against an
  already-established trait that spans several beats? Or does it actually
  introduce a standalone trait the synthesis never tracked separately,
  sharing only a root cause with something else? If it's the latter, the
  beat is `consistent` under the first-showing rule, whatever else is
  true. This gate already resolved TRUDY's trait-6 split and JOHN's split
  between baseball avoidance and reciprocal honesty.
- **Axis 2, within an established trait.** Is the change
  **quantitative**? That means the same type of act or response, now
  bigger, riskier or more intense: `throughline_evolution`. Or is it
  **qualitative**? That means a genuinely different type of act, or a
  facet never shown before, even if thematically related:
  `boundary_revealed`. Neither requires an external antagonist or a forced
  choice.

**The five instances under the two-axis test:**

| # | Beat | Type-change | Value |
|---|---|---|---|
| 1 | TRUDY scene214_beat4 | arranging harm through a proxy -> personally committing violence | `boundary_revealed` (unchanged) |
| 2 | JOHN scene172_beat6 | armed and prepared -> discharging lethal force at a person | `boundary_revealed` (was `throughline_evolution`; log 762) |
| 3 | REGGIE scene172_beat6 | scored on traits 1+5 jointly: loyalty-as-total-devotion reveals it has no limit, even against Mackie's own son. On trait 8 alone, brandishing -> firing would be `throughline_evolution` | `boundary_revealed` (unchanged; record corrected) |
| 4 | JOHN scene217_beat1 | omission -> commission | `boundary_revealed` (was `throughline_evolution`; log 761) |
| 5 | JOHN scene223_beat1 | reactive, mutual disclosure -> proactive, unilateral disclosure. **NEW instance** | `boundary_revealed` (was `consistent`; log 763) |

Instance numbering is by beat order here. In the running record above,
JOHN scene172_beat6 is "instance 2", JOHN scene217_beat1 "instance 3" and
REGGIE "instance 4".

**JOHN vs. REGGIE on the same beat.** The two verdicts differ for a
principled reason, not by inconsistency. REGGIE's lethal-force trait
(trait 8) was brandishing from its own first-shown beat (scene172_beat1),
so firing is the same type of act, more intense. JOHN had no prior beat
showing lethal force against a person: scene115_beat1 is an unarmed tackle
("he pounces hard onto Ricardo", 3559), and scene163_beat1 is arming for
readiness ("with his dad's rifle in hand", 5202). Prepare-to-fire is a jump
in type.

**Notes for the dedicated session:**

1. **Principle 8's wording vs. axis 2.** The author reads axis 2 as
   Principle 8 "read correctly". The current text in
   `tagging_schema.py` (lines 1036-1050) supports the throughline_evolution
   half: "success at an escalated version of an established capacity is
   throughline_evolution". Its boundary half is narrower than axis 2,
   though. It requires the beat to "expose something previously unknown
   that recontextualizes or limits the character -- a genuine
   capitulation, breaking point, or discovered weakness". Its closing test
   asks whether the beat taught "something new and constraining". Two
   instances fit "constraining" only loosely: instance 4 (an act of
   mercy) and instance 5 (proactive honesty). Both are new capacities, not
   limits or weaknesses. **Recommendation:** when the finding is
   formalized, amend Principle 8's text to match axis 2, so the schema
   prose and the recorded verdicts agree. Otherwise a cold model reading
   Principle 8 will keep putting type-changes like these into
   `throughline_evolution`.
2. **Instance 5 refines the "action, not declared intent" standard.** This
   finding's original test (above) required "their own on-page action
   (Hero-rule standard: action, not declared intent)". Instance 5's act is
   an utterance: "There's something I have to tell you." (6661-6662), then
   THE END. The author's ruling is that this line, spoken to the affected
   people's faces after the drive, the doorbell and the stoop, is itself
   the committed, irrevocable crossing, and that an audience will take the
   disclosure that follows THE END as given. This reverses ground 1 of log
   750 ("declared intent isn't the act") for this beat. The principle's
   wording should say when a speech act counts as the act. The
   archetype-layer removal of Hero on this beat (log 55) also cited
   declared intent, but it rests independently on the for-another test, so
   that tag is not reopened.
3. **The narrative-consequence (downstream-connection) filter, axis 3, is
   still unvalidated** beyond TRUDY scene131_beat1. It remains a candidate
   additional filter, not part of the two-axis test, unless the research
   below supports adding it.

**Status.** The three-character threshold was already met (TRUDY, JOHN,
REGGIE). The categorization is now unified, with five instances. The
finding is ready to be formally proposed as a numbered causal-integrity
principle once the axis-3 question is settled in the dedicated session.
**Not numbered or ratified yet.**

### Downstream-connection research for the dedicated session (2026-10-01, report only; no verdicts change)

**Method.** The same search scope as TRUDY scene131_beat1
(`FOG_TRUDY_REVIEW.md`, "Validation note"):
- every synthesis and resolution file in `fog_pass2_calls/`;
- `fog_pass2_queue.json`;
- the corrections log and the stored per-character fields of all 460
  beats;
- the script after each beat (fresh `pdftotext -layout -enc UTF-8` pull,
  byte-identical to `fog_full.txt`), searched with beat-specific keywords.

Every quoted line below was printed from that pull in this session. Each
hit is labeled as one of:
- **record citation**: a later beat's analysis names this beat ID;
- **concrete textual callback**: later script text refers to this beat's
  specific content;
- **thematic echo**: related content with no direct reference. Shared
  vocabulary is flagged.

| Beat | Record citations by later beats | Script after the beat | Outcome |
|---|---|---|---|
| JOHN scene138_beat2 (dock collapse, pulled ligament) | scene170_beat4's resolver (drafted `consistent`, not queued) uses it as the reference "breakdown of composure". That is a comparison citation | **Concrete textual callback:** scene141_beat1, "a cold compress over his shoulder" (4527); TRUDY "What happened to your shoulder?" / JOHN "Nothing." (4548-4551). **Thematic echo, shared vocabulary, explanatory:** the scene140 flashback two scenes later, YOUNG JOHN: "You think I'm ever gonna play baseball after this?!" (4481-4482, scene140_beat6), and MACKIE: "You'll go back to school, then spring training." (4464-4465, scene140_beat5). These explain the beat's baseball frustration, but they sit under **YOUNG JOHN**, so JOHN's synthesis can't see them (finding 21). Weaker echo: scene180_beat1, "a baseball in the other... He absently cycles through pitch grips." (5663-5664) | **Connected:** concrete callback plus an explanatory echo |
| JOHN scene175_beat1 ("Let me make a call.") | Only REGGIE's scene175_beat2 synthesis turning point and resolver. They cite it as the adjacent predecessor in Reggie's dying sequence, about Reggie's arc, not John's offer | Nothing later refers to the offer. Reggie refuses inside the same beat (5564-5567) and dies at scene175_beat2. **Candidate thematic echo, no shared vocabulary, my reading only:** mercy toward someone who has done grave wrong, at JOHN scene217_beat1 (the key exchange) | **No concrete connection;** one unconfirmed thematic echo |
| TRUDY scene188_beat1 (solitary bedside rosary) | Resolvers for scene189_beat1, scene190_beat1 and scene192_beat1 ("continuation of scene188_beat1"). TRUDY's synthesis turning point at scene193_beat1 (escalation vs. scene188_beat1, likely `boundary_revealed`; an unreviewed `arc_claim_check_no_draft` entry) | **Concrete textual callback, shared vocabulary, same intercut sequence:** Raymond begins the same prayer, "Hail Mary, full of grace, the Lord is with thee..." (5864-5869); "Trudy bedside with the rosary--" (5873); "Raymond with his eyes closed. His words matching Trudy's--" and the joint RAYMOND/TRUDY cue (5882-5892, scene193_beat1). The beat sets up that synchrony, which ties her devotion to the kidnapper | **Connected:** a set-up and payoff within the same sequence, five scenes long |
| TRUDY scene214_beat4 ("Trudy forces Holly's head overboard.") | Human-reviewed log entries on scene215_beat1, scene216_beat1 and scene216_beat5 all anchor on it, all within the same drowning sequence | **Concrete textual callback, in her own words, in a later scene:** "Maybe I held her under for too long. Maybe I hit her harder than I thought I did." (6553-6555, stored in scene217_beat1) | **Connected:** the strongest of the five |
| REGGIE scene172_beat6 (fires at John's head) | REGGIE's synthesis turning point at scene172_beat7 (continuation; an unreviewed `arc_claim_check_no_draft` entry), the adjacent beat. Other citations of this beat ID (the scene172_beat3 and scene172_beat7 resolvers, log 747) concern JOHN's act, not Reggie's | Nothing later refers to Reggie firing at John. **Thematic echoes of the scored trait complex (traits 1+5), not of the act; shared vocabulary is names only:** his dying words go back to Mackie, "Mackie looked after that little girl... like she was his own..." (5534-5535, scene175_beat1); "So Reggie got his El Vaquero." (5738, scene185_beat2); "He knows Dad and Reggie took matters into their own hands, but that they got the wrong guy." (6376-6377, scene213_beat4) | **No connection to the act;** echoes of the trait complex |

**What this suggests for the session.** This is a reading of the evidence,
not a verdict.
- Three of the five confirmed `boundary_revealed` beats have a concrete
  downstream connection (scene138_beat2, scene188_beat1, scene214_beat4).
- JOHN scene175_beat1 has none. REGGIE scene172_beat6 has none to the act
  itself.
- If the downstream filter were made **necessary**, scene175_beat1 would
  fail it. Either that verdict gets reopened, or the filter is wrong as a
  necessary condition.
- **The test has a structural blind spot near a character's exit or the
  script's end.** REGGIE dies three scenes after scene172_beat6. The new
  instance 5, JOHN scene223_beat1, is the last beat of the script, so
  nothing can follow it at all.
- So the filter is better read as evidence that **supports** a
  `boundary_revealed` verdict when present. Its absence shouldn't
  disqualify one, especially late in an arc.
- This research was done after the five verdicts were set, so, like
  scene131_beat1, it is not blind.

**Axis 3, second data point (2026-10-02, REGGIE scene132_beat1).** The
draft was throughline_evolution (escalation of trait 4, alcohol). It was
corrected to `consistent` (log 765): the author confirmed the beat is
preparatory, Reggie "getting amped and numb" before the man behind the
door, and not independently significant to his arc. Like TRUDY
scene131_beat1, it read as potentially meaningful in the draft and was
downgraded on the author's confirmation, so it is not blind either. Unlike
scene131_beat1, **no downstream-connection search was run** for this beat.
The cellar itself recurs (5193-5194, 5264-5266), but whether anything later
refers to the solitary drinking is unchecked. Run the same search scope
before counting this as a validation of the filter. Detail is in
`FOG_REGGIE_REVIEW.md`, Batch 2.

### Principle 11 verification (2026-10-02, report only; no verdicts change)

Each instance was re-checked against the final wording of Principle 11:
irreversibility; contingent vs. unconditional; the tracked character's own
act, physical or verbal; enough established arc to register the change.
Every quoted line was printed from `fog_full.txt` and from the stored beat
evidence in `fog_tagged.json` in this session.

| # | Beat | Own act | Contingent / unconditional | Result |
|---|---|---|---|---|
| 1 | TRUDY scene214_beat4 | "Trudy forces Holly's head overboard." (6468), physical | Unconditional. Her earlier proxy arrangement was framed as reversible: "just for a few days." (6419), "we'd let Holly go." (6429) | **Clean** |
| 2 | JOHN scene172_beat6 | "He pops out of the room and returns fire--" (5494), physical | beat5's "Or I'll be forced to defend myself." (5452-5453) is the principle's own contingent example; the trigger pull is not | **Clean** |
| 3 | REGGIE scene172_beat6 | "Reggie pulls the trigger." (5490), physical. The miss doesn't matter: the shot can't be unfired | beats 1-5 are contingent ("Drop the fucking gun, go on back to L.A., and let me handle this.", 5432-5433). His unconditional "you've made your choice, Detective." (5481-5482) is in the same beat, so it doesn't move the crossing | **Clean** |
| 4 | JOHN scene217_beat1 | "Her and John make the exchange." (6582-6583), physical, preceded by "Give me your keys." (6560) | Unconditional (no ultimatum), but see below | **Qualifies; second look** |
| 5 | JOHN scene223_beat1 | "There's something I have to tell you." (6661-6662), verbal | Unconditional; the principle's own worked example. Recognition ("Johnny? Johnny Kierstead? My God.", 6646) is MRS. MURPHY's line, correctly excluded | **Qualifies; one note** |

**Instance 4, second look (RESOLVED 2026-10-02):** removed from Principle
11's instance list; it stands on Principle 8a. See the status block at
the top of this finding. The original second-look note follows.
It is the only instance where irreversibility
isn't self-evident from the act on the page. Right after the key exchange,
John could still take the keys back or call it in. The way back closes
across the sequence: Trudy leaves, and John drives her car away at
scene218_beat1. The verdict's recorded basis (log 761) is the
omission-to-commission type-change, which 8a covers ("crossing into legal
obstruction"), not irreversibility alone. So `boundary_revealed` stands on
Principle 8/8a. Whether Principle 11 should claim this beat on its own
irreversibility test, or only as a crossing completed over a short
sequence, is an open wording question. That ties back to this finding's
original continuation-chain question.

**Instance 5, note.** It qualifies by construction, since it is the
principle's own example. Its irreversibility depends on the author's ruling
that the audience takes the disclosure after THE END as given (note 2
above). Principle 11 now treats this kind of unconditional declaration as
an act. At the archetype layer, the Hero rule still treats declared intent
as not yet action (log 55's removal also rests independently on the
for-another test). That difference between the two layers is deliberate,
but nothing written down states it yet. **(RESOLVED 2026-10-02:** the
deliberate split between the two layers is now documented in `CLAUDE.md`
and in Principle 11's note.**)**

**Still open from note 1 above (RESOLVED 2026-10-02:** Principle 8's
closing test was reworded to cover a newly shown strength or capacity as
well as a limit or weakness, and 8a now states that it is the exception
to the first-showing default.**)** Principle 8's closing test still asks
whether the beat taught "something new and constraining". 8a and 8b don't
change that sentence. Instances 4 and 5 (mercy, proactive honesty) are now
covered by 8a's "singular climactic action" clause, but not by that
closing test.

**Candidate worked example for Principle 11, contingent vs. unconditional
(2026-10-02, REGGIE Pass 2 Batch 4).** This is for use if the principle's
documentation is ever expanded beyond its current two speech examples
(JOHN's contingent "Or I'll be forced to defend myself", scene172_beat5,
and JOHN's unconditional scene223_beat1).

REGGIE's lines across scene172_beat2-5 are each an offer, a command or a
statement that still leaves John a way out:
- "I'm givin' you a chance here, Johnny." (5425)
- "Drop the fucking gun, go on back to L.A." (5432-5433)
- "You're forcing my hand here, John!" (5448)
- "Now stand down, soldier!" (5474)

The first line that puts John's choice in the completed past tense is
"you've made your choice, Detective." (5481-5482). It is followed by
"Reggie takes aim" (5484) at the already-confirmed scene172_beat6. That is
a single exchange where the foreclosure is visible in the grammar. Detail
is in `FOG_REGGIE_REVIEW.md`, Batch 4.

### Open items for the next principle session (as of 2026-10-02)

Not resolved here. Each item is preserved with its test case.

1. **Axis 3, the narrative-consequence (downstream-connection) filter, is
   still unvalidated.** The data points are TRUDY scene131_beat1 (searched,
   not blind) and REGGIE scene132_beat1 (author-confirmed, downstream
   search not yet run). See the research section and the axis 3 note
   above.
2. **Principle 8a's wording vs. preparatory/premeditation beats. Test case:
   REGGIE scene134_beat2** (log 766, `FOG_REGGIE_REVIEW.md` Batch 2).
   - **What 8a says:** it covers a "singular climactic action", namely
     personal violence, legal obstruction or an irreversible declaration.
   - **What the beat shows:** premeditation and preparation, mid-script.
     Reggie fills a needle and packs a hunting knife into a ritual basket
     (4291-4303). The violent act it prepares for happens off-page, and its
     purpose rests on later text (3742, 5270, 5349).
   - **The verdict's basis:** `boundary_revealed` was applied because the
     beat is the first evidence of a new, unforeseeable capacity
     (premeditated violence, antisocial behavior beneath the warm public
     persona). It was not applied because the beat depicts a climactic,
     irreversible deed.
   - **Question:** should 8a explicitly extend to preparatory or
     premeditation beats that reveal a new capacity without showing the
     deed itself? Or does that need its own, more narrowly worded clause?
     The verdict stands unless that session decides otherwise.
3. **The two-axis test reads the same transition inconsistently across
   characters. Test case: scene172_beat6, JOHN vs. REGGIE** (logged
   2026-10-02, REGGIE Pass 2 Batch 3).
   - **JOHN:** "armed and prepared -> discharging lethal force at a
     person" was scored as a **type-change** (axis 2, qualitative):
     `boundary_revealed`, log 762 (resolution table above).
   - **REGGIE:** the same beat, from the other side of the same exchange,
     says "on trait 8 alone, brandishing -> firing would be
     `throughline_evolution`", a **scale-change**. Its `boundary_revealed`
     instead rests on traits 1+5 jointly (log 759 + the 2026-10-01 record
     correction in `FOG_REGGIE_REVIEW.md`).
   - Both verdicts land on `boundary_revealed`, but through contradictory
     readings of whether going from a weapon held to a weapon fired is a
     type-change or a scale-change.
   - REGGIE Batch 3 (log 769) made scene172_beat1, gunpoint, the
     confrontational step of Reggie's premeditated-violence chain. That
     puts the REGGIE reading directly on the 172_1 -> 172_6 transition.
   - **Question:** is armed-to-firing qualitative or quantitative under
     axis 2? Should one of the two records' reasoning be rewritten, even
     though neither value changes?
4. **A grammatically unconditional declaration with no substantive
   weight. Test case: CHEYENNE scene155_beat11** (logged 2026-10-03,
   CHEYENNE Pass 2 Batch 2).
   - **The declaration:** "this'll be it for me. I'm going clean. NA, AA,
     fucking born again, whatever it takes..." (5125-5127). It has the
     flat, unconditional shape Principle 11 treats as foreclosing ("I'm
     going clean", not "if X, I'll...").
   - **The author's reading:** it carries no real weight. It is an empty
     promise, whether insincere or a sincere but unlikely-to-be-kept
     bargain made in acute crisis. Her established pattern (denial,
     manipulation under pressure, substance dependence) is the reason. It
     is recorded as a clean negative for Principle 11.
   - **Question:** can a declaration be unconditional in **grammar** but
     foreclose nothing in **substance**? Does the speaker's own
     established pattern, which makes it an empty promise either way,
     disqualify it from counting as a crossing regardless of its
     grammatical form?
   - **How this differs from "does the narrative confirm follow-through".**
     It asks whether a declaration needs real weight behind it, not just
     the right grammatical shape, to foreclose anything at all.
   - **Compare.** JOHN scene223_beat1 ("There's something I have to tell
     you.") was counted partly on the author's ruling that the disclosure
     follows after THE END. The two cases may need one consistent rule
     about what backs an unconditional declaration.

## 20. "Glued action" heuristic splits uninterrupted dialogue that starts with a character name (logged 2026-09-29, not fixed)

**Found during:** TRUDY Pass 2 review batch 2 (`FOG_TRUDY_REVIEW.md`), on
scene143_beat7. It was checked against a fresh `pdftotext -layout` pull, a
fresh `-raw` pull, and `fog_full.txt`.

**Mechanism:** `parse_script()` in `parser.py` (lines 571-581). While a
dialogue element is open, each new line is tested:

```python
looks_like_glued_action = (
    len(words) >= 2 and words[0] in prose_character_names
    and words[1][:1].islower()
)
```

If the test is true, the dialogue element is closed and the line starts a
new `action` element with `speaker: null`. `prose_character_names` is every
speaker cue in the script, title-cased, plus its last word (see
`build_prose_character_names()`). The rule is meant to catch action prose
glued straight onto a speech ("Holly runs..."). It also fires on any
dialogue line that happens to wrap so that it begins with a character's
name followed by a lowercase word.

**Distinct from findings 5, 7, 12, 15 and 16:** those need something
*interrupting* the speech (a page break, blank line, column split or
wrapped parenthetical). Here the source text is continuous: one cue, then
unbroken dialogue lines at the same indent. The split comes purely from the
NAME + lowercase-word pattern on a wrapped line.

**The 4 confirmed instances** (the source line is quoted from `fog_full.txt`;
each is stored as an unattributed `action` turn directly after the
speaker's dialogue turn):

| Beat | Speaker | Line before (dialogue) | Split-off line (stored as action) | `fog_full.txt` |
|---|---|---|---|---|
| scene123_beat13 | JOHN (CONT'D) | "So either you're too loyal to" | "Mackie and his lackies to admit..." | 4201-4202 |
| scene143_beat7 | TRUDY | "been better off in there. Maybe" | "Holly would've been better off." | 4680-4681 |
| scene155_beat9 | JOHN | "They were buying drugs? From you?" | "Mackie and Reggie?" | 5069-5070 |
| scene214_beat3 | TRUDY (V.O.) | "Communion, and then Confirmation." | "Cheyenne wasn't happy about it. But Holly was excited. She was almost there. I was her Godmother." | 6457-6458 |

**Review impact:** none on the verdicts made so far.
- scene143_beat7's Pass 2 verdict (boundary_revealed, confirmed) doesn't
  depend on the lost attribution.
- scene214_beat3's drowning-sequence verdict (consistent) was made from the
  raw text, where the line reads correctly as TRUDY V.O., not from the
  stored structured data.
- The model taggers did see these lines as speakerless action, in both
  Pass 1 and Pass 2.
- scene123_beat13 and scene155_beat9 are JOHN beats. Check them against
  the raw text if they come up in the remaining review.

**Update 2026-09-30 (JOHN Pass 2 batch 1): a fifth instance, and the JOHN
pair checked.**

| Beat | Speaker | Line before (dialogue) | Split-off line (stored as action) | `fog_full.txt` |
|---|---|---|---|---|
| scene101_beat1 | DOUG (CONT'D) | "made on that number was the morning" | "Holly went missing." | 3214-3215 |

The source is one continuous DOUG (CONT'D) speech (lines 3208-3215) on a
flush-left page. That is the layout the scan above said it would miss, and
it did: this instance turned up by eye while assembling context for JOHN's
batch 1. Stored turn 6 is DOUG's dialogue ending "...was the morning", and
turn 7 is "Holly went missing." as speakerless action. The count is now 5,
and it is still a floor.

**A new dimension of impact: this beat is a comparison anchor.**
scene101_beat1's own verdict isn't affected: JOHN is drafted `consistent`
there, and DOUG's reviews didn't depend on the line. But scene101_beat1 is
the comparison beat for the synthesis turning point on JOHN scene103_beat1
(finding 17's confirmed leak). It is also the `first_shown_beat_id` of JOHN's
trait "Willing to defy direct orders/warnings and escalate physical risk in
pursuit of a lead", and scene108_beat1, scene115_beat1, scene163_beat1,
scene172_beat6/7 and scene175_beat1 all chain back to that trait through
scene103_beat1. The defect doesn't just sit on one beat: it corrupts the
evidence other beats' reasoning is anchored to. That remains true even when
the affected beat's own verdict is sound, so a beat-local check will not
catch it. Any future assessment of this finding's impact has to follow
comparison edges, not only the beats that carry the split. (scene103_beat1
itself was corrected to `consistent` in JOHN batch 1 on continuation
grounds. This defect didn't drive that correction, but it is part of the
same unsound foundation.)

**The two JOHN beats, checked against a fresh `pdftotext -layout` pull:**
both are drafted `matched`/`consistent`. Neither is in `fog_pass2_queue.json`,
because the queue only takes non-consistent drafts and finding 17 entries.
Neither rationale depends on the split-off text, so both verdicts stand.
- scene123_beat13: the rationale cites the public outburst. The correctly
  attributed line ("...too dumb of a cop to realize it") adds a crude insult
  from JOHN, which fits the trait it was checked against.
- scene155_beat9: the rationale is "continues probing for the identity
  behind 'Army cat'", which holds either way. Its `checked_against`
  ("Investigative persistence trait") isn't one of JOHN's synthesis traits,
  another instance of finding 18's free-text problem.

**OPEN ITEM for JOHN Pass 2 batch 5: the scene123_beat13 / scene138_beat2
baseline contradiction.** scene123_beat13's resolver rationale calls JOHN's
public outburst consistent with "his already-established capacity for
volatile anger (e.g. with McAvoy, Sarge)". scene138_beat2's synthesis
turning point (a finding 17 healed boundary_revealed) says his composure
collapses there, "revealing a breaking point beneath the composure that had
never before cracked on-screen". Both can't be true. Resolve it when
scene138_beat2 is reviewed, reading scene123_beat13 (this finding) alongside
it, with finding 17 for scene138_beat2's forced type. The author reads
scene119_beat7's "Doug shifts uncomfortably" as exposure worry rather than a
reaction to John's temper. That is recorded with the scene119_beat7
correction, but the action line reads "concerned at John's temper", so it is
not treated as settling any part of this question yet. That reading also
contradicts the basis of scene119_beat7's confirmed Shadow tag
(`FOG_JOHN_REVIEW.md` chunk 2: "Doug's witnessed reaction ('concerned at
John's temper') is real textual evidence of a break from controlled
composure"), so settle it together with this item. Refinement
(2026-09-30, author-confirmed): the two readings are one causal chain
(temper -> volatility -> risk of being overheard -> Marchand, who walks in
at `fog_full.txt` lines 3750-3764), not rivals. See `FOG_JOHN_REVIEW.md`
batch 1.

**RESOLVED 2026-10-01 (JOHN Pass 2 batch 5, author-confirmed): no
contradiction.** The two claims describe two independent capacities.
- **Reactive anger at a proximate target:** scene119_beat7 (Shadow tag
  unchanged and not reopened) -> scene123_beat13, which stays consistent.
  Its citation is corrected from "McAvoy, Sarge" (scene14 trash-talk) to
  scene119_beat7.
- **Composure under cumulative weight:** scene13_beat1 -> scene138_beat2,
  boundary_revealed confirmed. It has no trigger and no target. "Never
  before cracked" is dropped as false.

Detail is in `FOG_JOHN_REVIEW.md` batch 5.

**Update 2026-09-30 (JOHN Pass 2 batch 3): a sixth instance.**

| Beat | Speaker | Line before (dialogue) | Split-off line (stored as action) | `fog_full.txt` |
|---|---|---|---|---|
| scene175_beat1 | REGGIE | "You know Cheyenne never brought" | "Holly to church? Not once. No first communion. No confession. Never even baptized. Believe that?" | 5553-5554 |

The source is one continuous REGGIE speech with no blank line (5553-5556),
on a flush-left page (104), so the scan described below would miss it.
Stored turn 9 is REGGIE dialogue, and turn 10 is an `action` turn with
`speaker: null`. The split-off line opens with a character name (HOLLY)
followed by a lowercase word, which is this finding's trigger. No verdict
depends on it: it's Reggie's line, and JOHN's scene175_beat1 verdict rests
on "Let me make a call." (5562). The count is now 6, still a floor.

**How the 4 were found, and the scan's limits:** a targeted scan of
`fog_parsed_scenes.json` for `action` elements that directly follow a
`dialogue` element, where the action's source line sits at dialogue indent
(10+ spaces) directly under a non-blank line at the same indent. That found
5 candidates. The 4 above are this rule; the fifth (scene64_beat8) is a
blank-line split, logged under finding 7. The scan **would miss** instances
on pages where dialogue is printed flush-left. Several pages in this PDF are
laid out that way (finding 7's MARCHAND lines, parts of scenes 40, 57 and
213). So 4 is a floor, not a count.

A second test with the same NAME + lowercase condition sits in the
post-cue branch (`parser.py` lines 592-607). It only fires when the cue
before it is rarely used (`cue_candidate_counts <= 3`), and it re-labels
that cue as action. No misfire of it was found, and none was specifically
searched for.

**Status:** documented only, not fixed, following the same convention as
findings 15 and 16. No re-parse, and no change to stored turns.

**For a future parser-hardening pass:** the finding 16 script-wide checks
would not have caught this. One compared parsed text against stored turns
for *missing* text, which isn't the failure here because the words are
present. The other scanned for two-column lines, which is a different
failure mode. Treat findings 5, 7, 12, 15, 16 and 20 as **one family,
"dialogue that loses its speaker"**, and search for all of them together
rather than one at a time. The direct test for the whole family is to take
every stored `action` turn and check whether its source line sits under an
open speaker cue in the raw text with nothing but that speaker's dialogue
in between.

## 21. JOHN and YOUNG JOHN are separate character entities: a character's identity fragments across the timeline, and Pass 2 synthesis can't connect the two halves of one life (logged 2026-10-01, not fixed; architectural)

**Found during:** the finding 19 resolution of JOHN scene185_beat2
(`FOG_JOHN_REVIEW.md`, "Finding 19 resolution"; log 760). The corrected
throughline is a disposition: treating justice's arrival as independent of
his own action. Its root is YOUNG JOHN's boat-accident secret and Mackie's
cover-up. On the page:
- YOUNG JOHN: "Dad, it's okay. I'll say it was me." (2349)
- MACKIE: "John! You fucked up. You can't undo this. You want to ruin two
  lives now?" (2353-2355, scene75_beat3)

Decades later the disposition surfaces in adult JOHN's behavior: in
scene185_beat2's silence, and in scene217_beat1's key exchange.

**The defect.** The tool tracks JOHN and YOUNG JOHN as separate character
entities. Each has its own synthesis and resolver files in
`fog_pass2_calls/`, and each has its own Pass 2 queue. Per-character
synthesis for JOHN therefore never sees YOUNG JOHN's beats, and the
reverse is also true. The scene185_beat2 / scene217_beat1 throughline
was invisible to any automated pass **by architectural design, not
because of a bug in how the pass ran.** It was found only because the
author holds both halves of the character's life in view at once.
Per-character synthesis structurally cannot do that.

**A second case, found the same day** in the downstream-connection research
(finding 19). JOHN scene138_beat2, the dock collapse, is explained two
scenes later by the scene140 flashback:
- YOUNG JOHN: "You think I'm ever gonna play baseball after this?!"
  (4481-4482, scene140_beat6)
- MACKIE: "You'll go back to school, then spring training." (4464-4465,
  scene140_beat5)

That explanation sits under YOUNG JOHN, out of reach of JOHN's synthesis.

**How it differs from neighboring findings:**
- Finding 18 is an inheritance/validation gap.
- Finding 19 is a vocabulary gap.
- This finding is a **character-identity resolution gap**. It's the same
  class of problem as the O'SHEA / HISPANIC / DRIVER fragmentation
  (finding 6), which was solved by a manual merge. The difference is that
  this one spans a timeline rather than a single scene, and no existing
  mechanism addresses it. Finding 13, a YOUNG JOHN relabel inside a
  flashback, was the opposite move: it correctly kept a flashback line off
  adult JOHN. The separation is right at the archetype layer. It's wrong
  only for whole-arc synthesis.

**Design direction for a future fix (author-endorsed; NOT to be built
now):**
- **Where it belongs.** The plot-facts pass already sees the whole script
  before any beat tagging. That makes it the natural place for
  canonical-identity resolution of "YOUNG X" / "X" cue pairs, the same way
  O'SHEA's variant cues were merged.
- **Don't simply merge the beats.** Folding all of YOUNG JOHN's beats into
  adult JOHN's trait-evidence pool would roughly double an already
  expensive synthesis call. It would also risk manufacturing false
  throughlines by treating every childhood scene as equally relevant
  evidence.
- **Better-scoped fix.** Flag flashback and retrospective structures as
  **biographical context** tied to the adult character's canonical ID.
  Supply them to Pass 2 synthesis as supplementary background, not as
  additional beat evidence that can claim traits. This keeps the plot-facts
  layer's existing strict boundary: context informs interpretation, and
  never asserts an archetype or trait the beat's own text doesn't show.
- **Likely necessary, not sufficient.** Even with this mechanism built,
  connecting scene185_beat2 to the Andy throughline meant recognizing an
  abstract thematic pattern across two scenes. They share no vocabulary and
  no characters on the page. All week the model has handled that kind of
  judgment unreliably, even across a few adjacent beats. The real
  connection may still need human review that holds the full shape of the
  story.

**Addendum (2026-10-03, YOUNG JOHN Pass 2 batch 1): the missing link is
withheld by design.** The moment YOUNG JOHN lets the cover-up stand is
never depicted. Scene 75 cuts from "John sits stunned." (2399) to "THE
PRESENT --". So part of the gap this finding describes is not only an
architectural limit of the tool: no connecting beat was ever meant to
exist on the page. Full reasoning is in `FOG_YOUNGJOHN_REVIEW.md`
("Structural finding: the sealed moment is withheld by design"). This
doesn't weaken the architectural defect above. Synthesis still can't see
the proposal (scene 75), the aftermath (scene 140) or the cost (adult
scene213_beat3 / scene223_beat1) together.

**Cross-character note on MACKIE (2026-10-03, author-confirmed; changes no
verdict).** Mackie has an established, repeated method of suppressing
inconvenient witness testimony to control an investigation's outcome.
`FOG_MACKIE_REVIEW.md` (archetype review only) doesn't document this, so
it is recorded here.
- **Holly Roberts case: on the page.** Beth and Krista tell John that Holly
  was texting someone "She called him El Vaquero." (2711), and that they
  told Mackie: "Why didn't you tell this to Detective Kierstead when he
  interviewed you?" / "We did tell him." (2719-2727). It is missing from
  his reports. John asks "Why would he leave something like that out?"
  (2773), Doug answers "What? Oh. El Vaquero?" (2777), and John notes the
  dates are altered too ("Says he spoke to the girls Monday, but it was
  really Sunday.", 2780-2782). John: "It's like he knew that somebody
  would be reading his notes... somebody he didn't want reading them."
  (2795-2798); "You got the father and her two best friends telling us
  things that nobody's ever heard of before. Except one man." (4181-4186).
- **The boat accident: the author's extrapolation, not on the page.** The
  author proposes that the same method was likely used 22 years earlier,
  to manage what YOUNG CHEYENNE and OTHER GIRL witnessed or reported about
  who was piloting the boat. The author also proposes that the official
  story was sealed by an off-page case-file ruling exonerating John. No
  ruling, inquest or witness statement about the accident appears
  anywhere in the script (checked 2026-10-03). Both points are offered as
  a plausible mechanism behind the withheld moment, not as depicted fact.
- **Why it matters here.** It strengthens the case that the withheld
  mechanism was a deliberate, controlled suppression inside the story,
  not a passive absence of evidence.

**Watch item (not yet a confirmed instance): CHEYENNE.** YOUNG CHEYENNE is
in the same boat flashback: "two teen girls, one of them YOUNG CHEYENNE"
(1891, scene60_beat3/scene60_beat4). She is already a separate entity,
with her own `fog_pass2_calls/resolution_YOUNG_CHEYENNE_0.json`. When
CHEYENNE's queue comes up, check whether the same fragmentation hides a
throughline on her arc.

Location correction: the instruction placed YOUNG CHEYENNE in
scene213_beat2's material. scene213_beat2 is TRUDY's confessional line
("John. Have you ever criticized God?"). It holds no YOUNG CHEYENNE and no
boat flashback. The flashback is scene60.

**Related note (2026-10-03, KRISTA Pass 2; a note, not a finding yet):
script-level motifs are invisible to per-character synthesis.** The
hobbyhorses recur from the opening (31-32) through the arena (2634-2635)
to the closing image ("holding their hobbyhorses", 6618-6620). No single
character's arc owns the motif, so Pass 2 synthesis can only see it as an
object echo on one character's beat, which is how KRISTA's scene84_beat1
claim arose (the claim does not hold; see `FOG_KRISTA_REVIEW.md`). Same
structural blind-spot family as this finding: meaning that spans entities
or arcs has nowhere to live in per-character synthesis.

**Instance (2026-10-03, PETE Pass 2): IRATE MAN / PETE.** One person
stored as two entities within two adjacent scenes. His scene 121 lines are
cued IRATE MAN ("Kierstead! Kierstead, that fuck! I wanna see him!",
3922-3923), and IRATE MAN has its own `functional_role_only` entry on
scene121_beat1. The action line names him at the end of the beat: "John
appears. He heads to the irate man, PETE (30's)." (3937). From scene 122 he
is cued PETE. Unlike JOHN/YOUNG JOHN, no timeline separates the two halves:
the split comes from the cue name alone. No verdict depended on it. See
`FOG_PETE_REVIEW.md`, which also records the script's own age
discrepancy ("40's", 3919, vs. "30's", 3937) as an author note.

## Pass 2 closeout notes (2026-10-03)

FOG Pass 2 human review is closed: all 160 `fog_pass2_queue.json` entries
are reviewed (`FOG_PASS2_CLOSEOUT.md`). These notes record the scope
decisions and the items carried forward. **None of them blocks the
closeout.** The FOG run (Pass 1 + Pass 2 + human review) was the
fully-cold pipeline test, and it is now complete. The next and only
remaining roadmap milestone is packaging: public repo, README, a demo with
pre-computed FOG examples, and sample outputs.

### Scope decision: MIN_BEATS = 3 (author, 2026-09-28)

`fog_pass2_runner.py` (`MIN_BEATS = 3`) runs Pass 2 only for characters
with 3 or more beats: "A whole-arc judgment on 1-2 beats says too little
to be worth a call." Recorded here because it was previously documented
only in the runner's docstring.

**Accepted out of scope (left at `requires_second_pass` by design):**

| Character | Beat | Fields |
|---|---|---|
| OLDER MAN | scene37_beat2 | weight_proportionality, characterization_consistency |
| DR. SHEPHARD | scene205_beat1 | weight_proportionality, characterization_consistency |
| LAWYER | scene205_beat1 | weight_proportionality, characterization_consistency |

These are the only `requires_second_pass` values left in
`fog_tagged.json` (checked 2026-10-03).

### Design note A (future work, not a blocker): "worth tracking" needs a better filter than beat count

- **MIN_BEATS = 3 is a crude proxy** for "this character is worth a
  whole-arc psychological judgment." It counts beats, not what the
  character does in them.
- **Pass 2 synthesis reliably over-claims on secondary characters.** From
  REGGIE's queue onward, 32 of 34 boundary_revealed drafts were
  overturned (`FOG_LATINOKID_REVIEW.md`, cross-queue tally). The
  overturned claims on minor characters repeatedly failed the
  "happens TO the character", universal-reaction and
  decency-vs-distinctiveness tests. The two kept (MACKIE scene140_beat6,
  RAYMOND scene205_beat1) both rest on the character's own depicted act.
- **The likely future improvement is a functional-role filter**: decide
  whether a character is functional or psychologically tracked before
  drafting arc verdicts for them. The whole-character caution was first
  recorded for RICARDO (`FOG_RICARDO_REVIEW.md`, batch 1). O'SHEA was
  explicitly ruled not functional (`FOG_OSHEA_REVIEW.md`).
- **No per-character ruling was made** for the nine small characters
  reviewed last (ALBERTO, FEDERAL AGENT, KRISTA, PETE, BLACK KID, LATINO
  KID, DET. MCAVOY, SARGE, MANAGEMENT). Their review files point here.

### Carried forward as known open items (not blockers)

1. **Principle 11 / finding 19:** the four items under "Open items for
   the next principle session" (axis 3 downstream filter; 8a vs.
   premeditation, REGGIE scene134_beat2; armed-to-firing type vs. scale,
   JOHN/REGGIE scene172_beat6; grammatically unconditional but empty
   declarations, CHEYENNE scene155_beat11).
2. **Finding 18:** build decision recorded above; scheduled before the
   next cold run on a new script.
3. **Finding 20 and the parser bug family.** Findings 5, 7, 12, 15, 16
   and 20 are one family ("dialogue that loses its speaker"), to be
   searched for together in a parser-hardening pass (see finding 20's
   closing paragraph). Documented only; no stored turns changed.
4. **Finding 21 (architectural):** one person stored as two entities
   (JOHN/YOUNG JOHN; IRATE MAN/PETE), the CHEYENNE 60_1 hidden-throughline
   note, and the related hobbyhorse-motif note. Needs a design decision on
   character identity.
5. **Candidate test, not yet a principle: reveal vs. boundary.** "A
   reveal changes what the audience knows, not what the character is"
   (`FOG_LATINOKID_REVIEW.md`, scene19_beat3). Compare Principle 9.
6. **Design note A** above.
7. **No rationale for archetype calls** (logged 2026-10-04, `FUTURE_WORK.md`
   item 2). The tagging step stores no reason for an archetype call, only
   the perception fields. Add a one-line rationale field to the tagging
   prompt before the next cold run, alongside the finding 18 build. Do not
   generate rationales after the fact for existing FOG tags.
8. **No Great Mother pole stored** (logged 2026-10-04, `FUTURE_WORK.md`
   item 3). 0 of 26 cold and 0 of 24 reviewed Great Mother calls record
   Light or Dark. Add a pole field to the schema and tagging prompt before
   the next cold run. Do not infer poles for existing FOG calls. The
   free-text evidence (MACKIE scene140_beat5; logs 97, 102, 108) is
   reference only.
9. **No prompt text in the call logs** (logged 2026-10-05, `FUTURE_WORK.md`
   item 4). Every call keeps its response and usage, but not the prompt
   it was given (at most a hash), so what the model saw can only be
   proven from git history. Log the full request with every call before
   the next cold run.

## Character review queue

Characters awaiting their own review of real-archetype tags, counted
from `fog_tagged.json` on 2026-09-27 after the chunk 3 changes. JOHN's
row was recounted on 2026-09-28 after the chunk 4 follow-up.

| character | real-archetype entries | notes |
|---|---|---|
| JOHN | 24 | archetype review complete (`FOG_JOHN_REVIEW.md` chunks 1-4); recounted 2026-09-28 after the chunk 4 follow-up |
| TRUDY | 16 | archetype review complete (`FOG_TRUDY_REVIEW.md` chunks 1-2); recounted 2026-09-28. Was 17 at the enumeration: scene30_beat2 corrected to ordinary_reaction (chunk 1); in chunk 2, scene216_beat5 Great Mother -> Shadow and scene216_beat6 Shadow -> Great Mother (count unchanged). Every one of the 16 has a row |
| MACKIE | 12 | archetype review complete (`FOG_MACKIE_REVIEW.md`); recounted 2026-09-28. scene140_beat6 and scene140_beat8 Great Mother -> Shadow (both still tagged, so the count is unchanged). Every one of the 12 has a row |
| O'SHEA | 2 (scene155_beat6 Persona, scene155_beat12 Great Mother) | review complete, all 13 beats reviewed (`FOG_OSHEA_REVIEW.md`), 2026-09-28. Both tags confirmed; scene154_beat2 confirmed ordinary_reaction; scene155_beat1 and scene155_beat11 upgraded to ordinary_reaction; the other 8 untagged confirmed as stored |
| CHEYENNE | 2 (scene64_beat6 Persona, scene64_beat7 Persona) | archetype review complete (`FOG_CHEYENNE_REVIEW.md`), recounted 2026-09-28. Both confirmed; scene64_beat7 goal corrected. scene154_beat2 was already ordinary_reaction (JOHN's review). No real tag in the scene155 car ride |
| DOUG | 2 (scene101_beat1 Chorus, scene123_beat9 Chorus) | archetype review complete (`FOG_DOUG_REVIEW.md`), recounted 2026-09-28. Was 3: both Mentor tags -> Chorus, scene123_beat15 Persona -> ordinary_reaction. Finding 8 "partner" sweep complete (5 untagged beats fixed 2026-09-28). Finding 15 (scene123_beat5 parse defect) is not fixed |
| YOUNG JOHN | 1 (scene75_beat5 Hero) | archetype review complete (`FOG_YOUNGJOHN_REVIEW.md`), recounted 2026-09-28. Hero confirmed; age wording fixed on scene140_beat2 and scene140_beat8 |
| REGGIE | 2 (scene54_beat2 Great Mother, scene94_beat3 Trickster) | archetype review complete (`FOG_REGGIE_REVIEW.md`), recounted 2026-09-28. Was 5 at the enumeration: scene54_beat1 Chorus -> ordinary_reaction; scene172_beat1 and scene172_beat2 Shadow -> ordinary_reaction (finding 14). Every one of the 5 has a row |
| ANGIE | 3 (scene80_beat1 Mentor, scene80_beat2 Mentor, scene81_beat1 Mentor) | archetype review complete (`FOG_ANGIE_REVIEW.md`), recounted 2026-09-28. scene81_beat1 Chorus -> Mentor |
| SARGE | 1 (scene14_beat6 Great Mother) | archetype review complete (`FOG_SARGE_REVIEW.md`), recounted 2026-09-28. Was 2: scene14_beat12 Mentor -> ordinary_reaction |
| PRIEST | 0 | archetype review complete (`FOG_PRIEST_REVIEW.md`), recounted 2026-09-28. Was 2: scene48_beat3 and scene48_beat4 Chorus -> functional_role_only |
| HOLLY | 1 (scene3_beat2 Trickster) | archetype review complete (`FOG_HOLLY_REVIEW.md`), recounted 2026-09-28 |
| LATINO KID | 1 (scene19_beat3 Trickster) | archetype review complete (`FOG_LATINOKID_REVIEW.md`), recounted 2026-09-28 |
| CAPTAIN MARCHAND | 1 (scene185_beat2 Chorus) | archetype review complete (`FOG_MARCHAND_REVIEW.md`), recounted 2026-09-28 |
| RAYMOND | 1 (scene205_beat1 Shadow) | archetype review complete (`FOG_RAYMOND_REVIEW.md`), recounted 2026-09-28. The tag comes from the pilot re-run; he is still missing from characters_present there (finding 2) |
| DR. SHEPHARD | 1 (scene205_beat1 Great Mother) | archetype review complete (`FOG_SHEPHARD_REVIEW.md`), recounted 2026-09-28 |

## Cold Pass 1 archetype accuracy (measured 2026-10-03)

How well the fully-cold Pass 1 archetype tags held up under human review.
This measures the archetype layer only (archetypes / non-tag category), not
causal integrity.

**Method.**
- **Cold values:** `fog_tagged.json` at commit `7a6e69e`, the finished cold
  run (460/460 beats, 0 corrections, every beat `llm_unreviewed`). The first
  human correction landed in the next commit, `1fe11c8`.
- **Final values:** `fog_tagged.json` at HEAD after the archetype review.
- **Unit:** one entry per beat x character. Its label is the set of
  archetypes, or the non-tag category (`kind`) when there are none.
- **Entity renames/merges** were matched using the 4 `character`
  corrections: DRIVER and HISPANIC -> O'SHEA (finding 6), JOHN -> YOUNG JOHN
  on scene140_beat8 (finding 13). The cold HISPANIC entry on scene154_beat2
  was merged into O'SHEA and is dropped; O'SHEA's own cold value there
  (`no_confident_archetype`, log #32) is used. One entry was added in review
  with no cold counterpart (JOHN scene172_beat3 -> Hero, log #61). That
  leaves 653 matched entries.
- **Cross-check:** the cold-vs-final diff reproduces the corrections log
  exactly. 34 `archetypes`/`kind` log entries, less TRUDY scene131_beat1's
  two-step correction (#85 Trickster -> Shadow, #752 -> ordinary_reaction)
  counted once, = 33 entries = 32 changed + 1 added.
- **Reviewed scope:** the "Character review queue" table above shows archetype
  review complete for every character with a cold real-archetype tag.
  Non-tag entries were reviewed only where touched, plus all 13 O'SHEA beats.
  The reviewed set is therefore: every cold real-archetype entry, every
  changed entry, and every O'SHEA entry (97 entries).

**Results.**

| Measure | Agreement |
|---|---|
| **Cold real-archetype tags kept exactly (headline)** | **57 / 82 = 69.5%** |
| Reviewed set | 65 / 97 = 67.0% |
| All 653 matched entries | 621 / 653 = 95.1%: **do not cite** |

The 95.1% all-entries figure is inflated: about 540 of those entries are
non-tag entries (`no_confident_archetype` / `functional_role_only`) that
were never reviewed, so they "agree" only because nobody looked. Cite 57/82
(or the reviewed-set 65/97), never 95.1%.

Of the 82 cold real-archetype tags: 57 kept, 15 demoted to
`ordinary_reaction`, 8 changed archetype, 2 demoted to
`functional_role_only`. The 69 final real-archetype entries are 57 kept + 8
retyped + 3 promoted from `no_confident_archetype` + 1 added.

**Per archetype** (entry-level membership; multi-archetype entries count
once per archetype). *Kept* = the cold tag on an entry survived review.
*Cold had it* = of the final tags, how many the cold run had on the same
entry.

| Archetype | Cold | Kept | Final | Cold had it |
|---|---|---|---|---|
| Hero | 7 | 3 (43%) | 7 | 3 |
| Mentor | 9 | 6 (67%) | 7 | 6 |
| Great Mother | 26 | 22 (85%) | 24 | 22 |
| Persona | 12 | 8 (67%) | 8 | 8 |
| Shadow | 15 | 11 (73%) | 14 | 11 |
| Trickster | 7 | 6 (86%) | 6 | 6 |
| Chorus | 7 | 3 (43%) | 5 | 3 |

**Non-tag categories.**

| Category | Cold | Kept | Final | Notes |
|---|---|---|---|---|
| `ordinary_reaction` | **0** | n/a | 19 | all 19 set by the human |
| `functional_role_only` | 30 | 30 | 32 | only 1 of the 30 reviewed; the 2 added are PRIEST's former Chorus tags (scene48_beat3, scene48_beat4) |
| `no_confident_archetype` | 541 | 534 | 534 | 14 reviewed: 7 kept, 4 -> ordinary_reaction, 3 -> Hero (JOHN scene172_beat4/6/7) |

**The cold run never used `ordinary_reaction`.** Every one of the 19 final
`ordinary_reaction` outcomes is a human correction, 15 of them demotions of
a real archetype tag. The cold tagger's only non-archetype outcomes were
`no_confident_archetype` and `functional_role_only`.

**Corrections.** 30 beats (33 entries) had their archetype outcome changed.
At beat level, across all fields including Pass 2, provenance is 125
`llm_human_corrected`, 42 `llm_human_confirmed`, 293 `llm_unreviewed`
(provenance is beat-level, so this is not a per-character review count;
see CLAUDE.md).

## Plot-facts stage: post-hoc run (2026-10-03)

**Post-hoc caveat.** The plot-facts stage was run on Full of Grace on
2026-10-03, AFTER the cold run and after Pass 1/Pass 2 human review.
`fog_tagged.json`'s `plot_facts` was empty during the cold run, so
`fog_tagging_harness.py` injected no plot facts into any tagging call. These
facts did not inform any cold-run tag, archetype review or Pass 2 value, and
nothing in this file should be read as implying they did. Every stored
fact's `notes` begins with a `[POST-HOC STAGE RUN 2026-10-03]` provenance
prefix saying so.

**Extractor.** `plot_facts_extraction.py`, recovered from Google Drive (file
last modified 2026-08-15) and committed unchanged in `e384dea`. It was missing
from the repo export. Checked before running: it reads parsed scene data
labeled by internal scene_id (never raw text), `max_tokens` 20000, and its
prompt enforces the three-category scope test (staged vs. genuine,
identity/cover, confirmed reveals about objects/events; feelings and
motives excluded). Non-behavioral mismatches: the docstring says rejected
responses are retried, but the code only raises; it returns text only (no
usage); it leaves `established_by_scene` at 0; it does not check that
`scope_scenes` IDs exist.

**Run.** `fog_plot_facts_runner.py --run`, run by the author in their own
terminal (key not exposed to the session). One call through the module's
own call path: `claude-sonnet-5`, max_tokens 20000, input
`fog_parsed_scenes.json` (223 scenes). 57,084 input / 16,641 output tokens,
`stop_reason` end_turn, **cost $0.2806** (pass2_orchestration.py Sonnet 5
constants; no cache use). The raw response and usage are in
`fog_plot_facts_call.json` (timestamp 2026-10-04T05:28 UTC, i.e. the evening
of 2026-10-03 local). **3 facts extracted and stored.** All scope_scenes
exist. Every other key of `fog_tagged.json` (beats, corrections, registry,
etc.) was verified unchanged against HEAD; the file validates (0 errors, 460
beats).

### Verification of every claim (against `fog_full.txt`)

Only 3 facts, so every claim in each fact (and its model notes) was checked
rather than a sample. Holds / doesn't hold / inference.

**Fact 0** (`staged_vs_genuine`, scenes 6-11): Holly's disappearance was a
kidnapping Trudy orchestrated via Raymond.

| Claim | Verdict | Evidence |
|---|---|---|
| Holly vanishes in the forest | holds | 114-165; "She just... disappeared." 254-255 |
| Distant, cut-off scream | holds | "A SCREAM. A girl’s scream. Holly. Distant and cut-off suddenly as if by force." 198-199 |
| Hobbyhorse found | holds | "Holly’s white Arabian hobbyhorse." 234 |
| Kidnapping orchestrated by Trudy | holds | "I hired Raymond to take her." 6418 |
| (a) Trudy "hired" Raymond | holds (her own word) | 6418. Raymond's account frames it as persuasion: "She said I would be doing the Lord’s work." 6054-6058. No payment is depicted anywhere. |
| "for a few days" | holds | "It was just for a few days." 6418-6419 |
| (b) "teach Cheyenne a lesson" verbatim | holds (across a line break) | "I wanted to teach Cheyenne a / lesson." 6425-6426 |
| Beth and Krista are Holly's friends | holds | "Holly’s two friends, Beth and Krista" 6618 |
| Family/police in scenes 6-11 are unwitting | inference | Consistent with the page (police cars 248; Beth's father questions the girls 241-272), but never stated. Model notes extend this to Cheyenne and Pete, who are not in scenes 6-11 ("Has anyone called the mother?" 282). |
| Notes: Raymond, "I gave her back... Everything was OK" (scene 201) | holds | "I gave her back. I gave Holly back to Trudy. Everything was OK." 6090-6092 |

Scope note for review: this is a genuine kidnapping, not a performed one,
so the `staged_vs_genuine` category is a questionable fit for the scope test.

**Fact 1** (`confirmed_reveal`, scenes 169-172): Alberto Gomez had no
connection to the Holly case.

| Claim | Verdict | Evidence |
|---|---|---|
| Reggie kidnapped Alberto | inference | The abduction is never shown. Alberto is found bound in the cellar (5312-5313); Reggie arrives armed and claims him (5382-5418). |
| Reggie tortured Alberto | inference (strong) | Injuries depicted 5326-5332, 5349-5354; John: "Was that before you gouged his eye out or after?" 5421-5422, not denied. The torture itself is not shown. |
| Reggie accused him of being "El Vaquero" | doesn't hold as stated | Reggie accuses him of raping Holly: "He raped Holly. He already confessed." 5417-5418. The El Vaquero framing is John's ("This is not El Vaquero." 5407; "So Reggie got his El Vaquero." 5738). |
| No actual connection to the Holly case | inference (strong) | "Just not the right vaquero." 5744, followed by "Raymond Olsen?" 5748; Trudy's confession 6418. Never stated outright. |
| Registered sex offender | holds | "Gomez was a registered sex offender." 5731-5732 |
| Wanted in Mexico City, fled north | holds in substance | "Multiple rapes of minors back in Mexico City. Escaped custody six months ago. I guess he fled as far north as he could get." 5732-5735; "extradited back to Mexico" 5715 |
| (c) A "torture-extracted confession" | inference | Alberto's only dialogue in the whole script is "... Diablo... Diablo..." 5365 (his single cue, 5364). The confession exists only as Reggie's claim, 5418. |
| Notes quote attributed to Marchand | partly misattributed | "So Reggie got his El Vaquero." is JOHN's line (5737-5738); "Just not the right vaquero." is Marchand's (5743-5744). |

**Fact 2** (`confirmed_reveal`, scenes 197, 201, 206): the official account
is incomplete.

| Claim | Verdict | Evidence |
|---|---|---|
| "The FBI's public case-closure" | doesn't hold | The broadcast reports a connection and pending trial, not a closed case. See the wording below. |
| Broadcast "naming Raymond Olsen as responsible" | doesn't hold as worded | "connecting local man, Raymond Olsen, to the kidnapping and murder of Holly" 5966-5968 |
| His subsequent interrogation | holds | Scenes 199-206, 6001-6237; Federal Agents question Raymond 6033-6147 |
| Raymond kidnapped Holly at Trudy's hiring | holds | 6418; 6090-6091 |
| He returned her to Trudy | holds | "I gave Holly back to Trudy." 6090-6091; "So I got her back from Raymond." 6448 |
| He did not kill her; Trudy drowned her in a forced baptism | holds | Baptism 6466-6538; "Holly stops struggling." 6535; "bobbing lifelessly" 6541; Trudy: "Maybe I held her under for too long." 6553-6554; Raymond: "I did not do that." 6111 |
| (d) "Never disclosed to the FBI, the police, or the public" | doesn't hold for Trudy's involvement | Raymond tells the Feds: "She said it’s OK..." 6053-6058; agent: "we know Trudy was helping you" 6060-6062; Doug: "He just started spewing all this shit about Trudy." 6007-6008; Marchand: "I’ve issued an APB." 6229, "Let us handle Trudy." 6237; John to Trudy: "Soon all of New England’s gonna be out looking for you." 6577-6578. |
| ...that Trudy (not Raymond) did the killing | holds | The agents still say Raymond "drowned her in the Bay" 6099-6101; Trudy confesses the killing only to John, who says he will tell no one: "Nothing. It’s between you and God now." 6592-6594. No public disclosure is on the page. |
| Notes: official narrative treats Raymond as "sole killer" | doesn't hold | The Feds already treat Trudy as an accomplice, 6060-6062 |

### Author correction on fact 2 (Shane, 2026-10-03): APPLIED

Shane: the news broadcast citing FBI sources CONNECTS Raymond to Holly's
kidnapping and murder; it does not charge him or close the case, and it comes
just before the interrogation scene. "The FBI's public case-closure" and
"naming Raymond Olsen as responsible" overstate it.

Broadcast wording, verified (scene 197, 5950-5972): "Breaking news out of
Dover this morning: A major break in the case of Holly Roberts, the missing
Dover girl whose body was discovered last week washed ashore along the
Piscataqua River.... ...FBI officials have now confirmed evidence from
Internet chat rooms and cell phone records, connecting local man, Raymond
Olsen, to the kidnapping and murder of Holly. Mr. Olsen is currently in
Federal custody and is awaiting trial pending a psychological evaluation. He
has pleaded not guilty."

- "Connects", not "closes": confirmed (5966-5968). Nothing in it closes the
  case.
- "Just before the interrogation": confirmed. Scene 197 (airport bar) ->
  198 (precinct, "Room Two. He’s still talking." 5998) -> 199-206
  (interrogation and observation room).
- "Does not charge him": the broadcast never uses the word "charged", but
  "awaiting trial" and "He has pleaded not guilty" (5970-5972) imply formal
  charges. Worth deciding how to word this when the correction is applied.

**Status: APPLIED 2026-10-03**, together with author corrections to facts 0
and 1 (below).

### Corrections applied (2026-10-03, author-confirmed)

All three facts were corrected through the corrections log: one entry per
fact, `beat_id` `plot_facts[N]`, `field_name` `plot_fact`, `llm_value` = the
complete original fact (text, category, scope, notes), `human_value` = the
corrected fact. Log total 844 -> 847. Each fact's `provenance` is now
`llm_human_corrected`. `PlotFact` gained an optional `provenance` field for
this (`tagging_schema.py`, defaults to `llm_unreviewed` on load), since plot
facts are not beats and `log_correction()` only accepts beat IDs. Every
quoted phrase and line range was checked against `fog_full.txt` before
applying. No beat, tag, Pass 2 value or earlier log entry changed.

- **Fact 0:** recategorized `staged_vs_genuine` -> `confirmed_reveal` (a real
  kidnapping, not a performed one). Now: "Holly's disappearance (scenes 6–11)
  was arranged by Trudy Kierstead, who hired Raymond Olsen to take Holly for a
  few days to teach Cheyenne a lesson (6418–6426)."
- **Fact 1:** now: "Alberto Gomez, held and tortured by Reggie, has no shown
  connection to Holly's case. Marchand reveals he was a registered sex
  offender, wanted for multiple rapes of minors in Mexico City, who had
  escaped custody (5731–5734). Reggie claims Alberto confessed (5417–5418),
  but Alberto's only line is "Diablo" (5365)." Two adjustments to the author's
  draft, approved before applying: the cite 5731–5733 became 5731–5734
  ("custody" is on 5734), and "escaped custody in Mexico City" was reworded
  because the page never says where he escaped from. "Wanted" rests on
  "extradited back to Mexico" (5713–5715).
- **Fact 2:** now: "Raymond took Holly but returned her to Trudy, who drowned
  her during a forced baptism (6466–6555). The FBI connects Raymond to the
  kidnapping and murder (5950–5972) and knows Trudy helped him, but no one in
  authority learns Trudy drowned Holly. The only confession shown is to John
  (6327–6555), who tells her he will tell no one (6592–6594)." One adjustment
  to the author's draft, approved before applying: "She confesses only to
  John (6592–6594)" cited John's promise of silence rather than the
  confession, and a priest exits the same confessional booth just before John
  enters (6287–6289), so the page doesn't establish that she confessed to no
  one else.

### Note: the same over-reading signature as Pass 1 and Pass 2

All 3 facts had a correct core reveal (Trudy arranged the kidnapping;
Alberto was not Holly's abductor; Trudy, not Raymond, killed Holly) but
overreached in framing: an assumed confession (fact 1), a "case closure"
(fact 2) and a "never disclosed" (fact 2). This is the same over-reading
signature seen in Pass 1, where the cold run never used `ordinary_reaction`
(all 19 final ordinary_reaction outcomes are human corrections, 15 of them
demotions of a real archetype tag), and in Pass 2, where 98 of 134 drafted
change-claims were ruled no change (see "Cold Pass 1 archetype accuracy"
above and `FOG_PASS2_CLOSEOUT.md`). The model reliably finds the real
structure, then claims more than the page shows. With only 3 plot facts this
is one more instance of the pattern, not a separate measurement.

## Development read (report section 1): two runs and the author check (2026-10-05)

**What it is.** The opening of the story report: the title (taken by code
from the title page, never generated), plus a genre and a one-paragraph
synopsis written by `claude-sonnet-5` from `fog_full.txt` page 2 on only. No
plot facts, tags or review data are sent. Generator:
`fog_dev_read_runner.py`. Every response is checked by `report_guard.py` as
report-voice summary text before it can appear on the page.

**Run 1** (prompt v1, run by the author in their own terminal; $0.2742; 66,665
and 66,761 input tokens). Both attempts were rejected: attempt 1 was 155 words
and its quote "El Vaquero," failed the verbatim match on its trailing comma;
attempt 2 broke the JSON with unescaped double quotes. The result fell back to
title + genre. Archived in `fog_dev_read_archive/`. Fixes: trailing
punctuation inside quotation marks is stripped before matching; structured
outputs; no quotations in the synopsis.

**Run 2** (prompt v3; $0.2769; 66,967 and 67,072 input tokens). Attempt 1 was
192 words and quoted "baptize", now caught by the whole-word quote match (the
script has only "baptized", lines 5556 and 5568). Attempt 2 was 161 words,
rejected only for length under the 70-140 limit. The author changed the hard
limit to 70-170 words (prompt v4 asks for at most five sentences), and attempt
2 was re-checked against the full guard with no API call
(`--accept-saved 2`): no violations. It is the stored synopsis, unchanged.

**Author check (Shane, 2026-10-05).** Checked by the author against the
script: accurate apart from two minor slips, left as written.
- "eleven-year-old" Holly: the script says "HOLLY (12)" (line 52).
- "twenty years earlier" for Andy's death: the flashbacks say "22 YEARS
  AGO..." (line 1886).

A third item Claude raised, "choosing silence over turning her in", is on the
page and is not a slip: Trudy: "What are you going to tell people?" / John:
"Nothing. It's between you and God now." (lines 6590-6594). The note is also
under the hood in section 1. The build checks that the stored genre and
synopsis match the saved API response word for word, so the text labelled
"Written by the AI" cannot be edited by hand.

**What the guard can and can't catch.** The word checks caught every wording
problem in these runs (length, quotes, malformed output). They cannot catch
factual errors: run 1's attempt 1 said Trudy "accidentally drowned" Holly,
where the page has "Holly struggles. Trudy forces Holly's head overboard."
(line 6468), and run 2's two slips passed every check. The same over-reading
signature as the plot-facts stage and Pass 1/Pass 2: the model finds the real
structure, then gets details wrong or says more than the page shows. A
synopsis needs a person to read it against the script.

## Development read, run 3 (prompt v5): length change, formatting repair, author check (2026-10-06)

**Run 3** (prompt v5: genre + logline + full synopsis in one call; $0.2913;
67,077 and 67,178 input tokens). Attempt 1 was rejected for an invented quote
('finish what they started', not in `fog_full.txt`) and length (463 words
against 250-450); it also carried a stray "```none" in the text. Attempt 2
was 462 words, rejected only for length. Its three quotations ("El Vaquero",
"the Lord's work", "gave Holly back") all match the script (lines 2711, 6055,
6091). The model runs about 10% over its word target, so the author moved the
prompt target to about 300-380 words and the hard limit to 250-500, and
attempt 2 was re-checked with no API call (`--accept-saved 2`): no
violations. Stored with its own genre and logline, which were already the
stored ones.

**Formatting repair.** Attempt 2's synopsis read "keep silent.a While
investigating further": a stray "a" and a lost paragraph break, the same kind
of output glitch as attempt 1's "```none". Neither is something the guard
checks. One repair was made: the "a" removed and the paragraph break restored
(four paragraphs). No words changed; the word count is 462 before and after.
The AI's original is stored verbatim beside the repaired text, the repair is
logged in `report_guard_log.jsonl`, and the build refuses the page unless the
text shown is the saved API response plus only that logged repair. The only
character a repair may remove is a stray glued on after a word's closing
punctuation, never a letter of a word.

**Author check (Shane, 2026-10-06).** Fact-checked against the script; the
AI's words are left unchanged and these points recorded under the hood in
section 1:
- Logline, "a case his late father secretly worked": Mackie was not working
  the case secretly; Doug gave John Mackie's case files.
- Synopsis, "Mackie had been quietly consulting on the case": the same issue.
- Synopsis, "suspended to desk duty": not in the script.
- Synopsis, "someone named Trudy": phrased as if Trudy were a stranger; the
  synopsis itself earlier identifies her as John's sister.

Otherwise confirmed accurate by the author. The build checks that each cited
phrase is in the AI's text. The previous author check (2026-10-05, on the
prompt-v3 synopsis) is archived with that synopsis in
`fog_dev_read_archive/fog_dev_read.20261006T174304Z.json`.

The pattern holds from runs 1 and 2: the guard caught every wording problem it
checks for, and none of the four factual points. Two of them (secretly,
quietly) are the model stating a hidden manner the page doesn't show, the
same over-reading signature as elsewhere in this pipeline.

**Rule changes for the next run (prompt v6).** Short quotations are allowed;
each must still match `fog_full.txt` word for word. Length is a soft target:
the prompt still asks for a 1-2 sentence logline and a synopsis of about
300-380 words, but going over logs a "length over target" note instead of
rejecting. Only a wide malfunction bound still rejects: logline under 8 or
over 120 words, synopsis under 100 or over 1,000 words.

**Quotation line, prompt v6 (approved 2026-10-06).** The line that replaces
the no-quotations rule, "You may quote the script briefly. Keep each
quotation short and copy it word for word.", was drafted by Claude Code and
approved by the author (Shane) on 2026-10-06. The same note is in the
prompt-version log at the top of `fog_dev_read_runner.py`.

**Which prompt produced the text on the page.** The genre, logline and
synopsis shown in section 1 come from run 3, which used prompt **v5** as
committed in c893b0c (2026-10-05), not the current v6. Confirmed from the
records, not assumed: the run was at 17:42Z on 2026-10-06, before the next
runner commit (7e9c994, 17:49Z); the system prompt from c893b0c hashes to the
`system_sha256` in `fog_dev_read_call.json`; and the full user message of
both attempts, rebuilt from that version's text and `fog_full.txt`
(unchanged since 2026-09-26), matches each attempt's `user_sha256`. The exact
prompt is archived verbatim (parsed from the committed source, not retyped)
in `fog_dev_read_archive/fog_dev_read_prompt.v5.93f60624.json`. The record
names it in `generated_by_prompt_version` and `generating_prompt_file`, kept
apart from the current `PROMPT_VERSION`. Under the hood, section 1 says the
text was produced by prompt v5 and that v6 is the current prompt for future
runs. The build refuses the page if the record's version, the archived prompt
file, and the call record don't all agree. From v6 on, each run saves the
exact prompt it sent to the archive folder and points the record at it.

## Emotional wave: tested on Full of Grace and left out of this release (author finding, 2026-10-06)

**What was tested.** The VADER sentiment wave (`beat_detector.py`'s turn
extraction and `signals.compound_sentiment`; deterministic, no AI calls),
variant (b): dialogue plus action, scenes with fewer than 2 such lines
skipped. It scored 161 of 223 scenes. Scratch prototype and data:
`prototype_timeline/` (kept as is, for the record).

**Author check: failed on the key moments.** Scene means from
`prototype_timeline/wave_b_dialogue_action.json`, each checked against
`fog_full.txt` and the per-scene table on 2026-10-06:
- The wave reads the inciting event as near-neutral. Holly's scream ("A
  SCREAM. A girl's scream. Holly.", line 198) is in scene 7 (page 4), which
  averaged −0.12, but the scene runs from −0.73 to +0.59: the mean averages
  away a wide swing. The search that follows (scene 8, page 4) scored 0.00.
- The wave reads the confession as near-neutral too. John letting Trudy go
  (scene 217, pages 123–124) averaged +0.02, over a range of −0.57 to
  +0.54: again a wide swing averaged away.
- The script's highest score, +0.58, falls on scene 220 (page 124): John
  watching Beth and Krista on the Santa float, "the illusion of safety and
  innocence ripped from them forever" (lines 6622–6623).

**Cause.** Ceiling category (a), content-cued emotion (`beat_detector.py`,
`signals.py`): the scores follow the vocabulary, not what happens. Scene
means also hide the swings within a scene.

**Decision (author).** The archetype timeline ships alone; the wave is out
of this release. Possible future source: the AI's stored emotion field on
tagged moments (`emotion` in each character's entry).

**Open item (closed 2026-10-06).** In the prototype's Great Mother pole
parse, MACKIE scene140_beat11 ("Great Mother + Persona (confirmed)") stayed
"not stated" pending an author ruling. Author ruling (Oct 6, 2026): Great
Mother, dark pole. It is recorded on that beat's row in
`FOG_MACKIE_REVIEW.md` (notes column; the verdict text is unchanged), and
the pole parser in `report.py` (section 4, the archetype timeline) reads
author rulings as well as verdicts: 15 dark, 9 with no pole named.
