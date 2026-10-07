# Walkthrough map: Full of Grace, from PDF to Story Report

Groundwork for a phone-first, single-page walkthrough (not built yet).
Mapped from the code and data on 2026-10-06 (HEAD `611fae5`). Every
excerpt below was printed from the named file in the session that wrote
this map, not retyped. Paths are repo-relative.

## Stage count: the docs vs. the code

`README_NOTES.md` doesn't actually describe the pipeline's stages. The
"five-stage pipeline" wording is in the development methodology notes, not in this repo (Overview and
Architecture): parser → signals/beat_detector → integration →
tagging_schema → report. Full of Grace didn't run that way:

- **Extraction comes first and is a separate step**: `pdftotext -layout`,
  outside Python.
- **There's a hand-patch step** between parsing and beat detection
  (`fog_hand_patches.py`).
- **`integration.py` is not a stage in this run.** `build_fog_scaffold.py`
  assigns beat IDs and builds the untagged `BeatTag`s itself, using
  `tagging_schema` directly. The only thing used from `integration.py` is
  `evidence_summary()`, which `llm_orchestration.py` and
  `pass2_orchestration.py` import to format a beat's evidence for the
  prompt. (The file says it is "reconstructed".)
- **`tagging_schema.py` isn't a step either.** It's the data model and
  validator that every later step reads and writes. The tagging itself is
  done by `fog_tagging_harness.py` → `llm_orchestration.py`.
- **Several stages the five-stage diagram doesn't have:** Pass 2 (a
  separate harness), two rounds of human review, the development read,
  and a data layer (`report_data.py`) that rebuilds the AI Output view
  from git snapshots before `report.py` renders it.
- **Order of the two review rounds:** the Pass 2 run (8079f93) came
  *after* 196 Pass 1 corrections had already been applied, so it didn't
  run on purely untouched AI output. `report_data.py` records this, and
  the report's AI Output label states it.

Counted as the code actually runs them, the path from PDF to report has
10 steps (one extra side step isn't used by the report).

## a) Stages in run order

| # | Stage | Script / module | Input | Output | What it does, in one sentence |
|---|---|---|---|---|---|
| 1 | Text extraction | `pdftotext -layout` (Poppler; the command is recorded in `build_fog_scaffold.py` and in `fog_scaffold.json`'s `script_version`) | `full_of_grace.pdf` (126 PDF pages) | `fog_full.txt` (6,665 lines) | Turns the PDF into plain text that keeps each line's position on the page. |
| 2 | Parsing + hand patches | `build_fog_scaffold.py` → `parser.parse_script()`, then `fog_hand_patches.apply_hand_patches()` | `fog_full.txt` | `fog_parsed_scenes.json` (223 scenes) | Splits the script into scenes and labels every line as action, a character cue, dialogue or a parenthetical. |
| 3 | Beat detection | `build_fog_scaffold.py` → `beat_detector.package_scene_for_interpretation()` (uses `signals.py`, `suspense_signals.py`) | `fog_parsed_scenes.json` | `fog_scaffold.json` (460 beats, all untagged) | Breaks each scene into beats where the text shows a shift (pauses, cut-offs, sentiment swings) and stores the full evidence for each beat. |
| 4 | Pass 1 tagging (AI) | `fog_tagging_harness.py` → `llm_orchestration.py` (prompt built from `tagging_schema.py`; evidence formatted by `integration.evidence_summary()`; model `claude-sonnet-5`) | `fog_scaffold.json` | `fog_tagged.json` (cold snapshot at commit `7a6e69e`: 460/460 beats, 0 corrections) plus `fog_tagging_calls.jsonl` (470 logged calls, including the 12-beat pilot and re-runs) | Asks the AI, one beat at a time, which of The Big Seven (if any) each character presents as, along with how an audience and the character would see the moment, emotion, goal, and the first causal-integrity fields. Every response is validated against the schema and rejected if it doesn't fit. |
| 5 | Human archetype review | Manual, per character; corrections applied through the schema's `Correction` log | `fog_tagged.json` | `fog_tagged.json` (corrections log) + `FOG_<NAME>_REVIEW.md` (25 files) | A person checks every AI archetype call against the script and keeps, changes or removes it, writing down why. |
| 6 | Pass 2 (AI) | `fog_pass2_runner.py` → `pass2_orchestration.py` | `fog_tagged.json` | `fog_pass2_calls/` (92 call files + `progress.json`: one `synthesis_*` per character, `resolution_*` chunks); 524 drafts written into `fog_tagged.json` (commit `8079f93`, 32 characters), each logged "AWAITING HUMAN REVIEW" | For each character with 3+ beats, the AI reads the whole arc, names their traits and turning points, then judges each moment: is the reaction in proportion, and does the behavior fit who they've been? |
| 7 | Human Pass 2 review | Manual; then `build_fog_turning_points_reviewed.py` | `fog_tagged.json`, `fog_pass2_calls/`, `FOG_*_REVIEW.md` | `fog_tagged.json` (corrections log, 847 entries in total), Pass 2 tables in `FOG_*_REVIEW.md`, `FOG_PASS2_CLOSEOUT.md`, `fog_turning_points_reviewed.json` (36 turns) | A person checks every turning point and every flag the AI raised, then the reviewed turning points are collected into one file the report can read. |
| — | (Side step) Plot facts | `fog_plot_facts_runner.py` → `plot_facts_extraction.py` | `fog_parsed_scenes.json` | `fog_tagged.json` `plot_facts` (3 facts) + `fog_plot_facts_call.json` | Pulls the plot's settled facts out of the script. It ran after the cold run, informed no tag, and isn't used by the report. |
| 8 | Development read (AI) | `fog_dev_read_runner.py` (checked by `report_guard.py`) | `fog_full.txt` only (title page excluded from the prompt) | `fog_dev_read.json`, `fog_dev_read_call.json`, `fog_dev_read_archive/` | Code reads the title off the title page; the AI writes the genre, a logline and a synopsis from the script text alone, and the guard rejects any wording that grades or uses jargon. |
| 9 | Report data layer | `report_data.py` | `fog_tagged.json` now, plus git snapshots `7a6e69e` (Pass 1) and `8079f93` (Pass 2); `fog_full.txt` | `fog_line_index.json`, `fog_report_model.json` | Rebuilds the AI Output view from the snapshots, checks it against the corrections log (any unexplained difference stops the build), and maps every beat to its lines and printed pages. |
| 10 | Story Report | `report.py` (+ `report_guard.final_scan`) | `fog_report_model.json`, `fog_line_index.json`, `fog_full.txt`, `fog_tagged.json`, `fog_turning_points_reviewed.json`, `fog_dev_read.json`, `FOG_*_REVIEW.md` (Great Mother pole) | `fog_story_report.html` (public); `fog_story_report_review.html` (local, git-ignored) | Builds the four-section report page with the AI Output / Human Reviewed toggles, and refuses to write it if any reader-facing text fails the checks. |

## b) The artifact and excerpt for each stage

The excerpts follow one thread where they can: Holly's disappearance
(scenes 3 and 7), plus Mackie in scene 140 for the review stages. Short
lines are chosen for phone width.

**1. Extraction: `fog_full.txt`, lines 192-199.** The inciting moment, as
extracted:

```
Krista frowns. Beth hangs up her phone, unable to reach
Holly. She begins to tap out a text --

                                    BETH (CONT’D)
                  Where r-u you dumb... little... sh-

A SCREAM. A girl’s scream. Holly. Distant and cut-off
suddenly as if by force.
```

Phone note: the cue sits at column 37 and dialogue at column 19. To fit a
phone, either strip the common indent (as `report.py`'s `beat_text()`
does) or show this one at a reduced font size.

**2. Parsing: `fog_parsed_scenes.json`, scene 7.** The slugline fields and
the first elements:

```json
{"scene_id": 7, "slugline": "EXT. RIVERBANK - LATER",
 "int_ext": "EXT", "location_time": "RIVERBANK - LATER"}
{"type": "character_cue", "speaker": "BETH", "text": "BETH"}
{"type": "dialogue", "speaker": "BETH",
 "text": "It’s been twenty minutes. I’m calling her."}
{"type": "action", "speaker": null,
 "text": "Beth takes out her cell, begins to dial."}
```

**3. Beat detection: `fog_scaffold.json`, `scene7_beat2` → `scene7_beat3`.**
The detector closes a beat on Beth's cut-off text, just before the scream:

```json
"scene7_beat2": {"closing_signal": {"score": 4, "reasons": [
  "embedded pause (...)", "cut off (--)",
  "sentiment delta 0.54", "sentiment magnitude -0.51"]}}
"scene7_beat3" turn 9: {"kind": "action", "speaker": null,
  "text": "A SCREAM. A girl’s scream. Holly. Distant and cut-off suddenly as if by force."}
```

**4. Pass 1 tagging: `fog_tagging_calls.jsonl`, `scene3_beat2`** (the raw
AI response, logged before parsing). The HOLLY entry, cut at its
`emotion` line:

```json
{"character": "HOLLY",
 "archetypes": ["Trickster"],
 "self_perceived": ["playfully kind toward Krista, then cleverly seizing an advantage by launching the race before the others are ready"],
 "audience_perceived": ["an impish, high-spirited child who gives a sweet gift and then gleefully cheats the start of a game"],
```

Call metadata from the same line: `claude-sonnet-5`, `end_turn`, 572 input
tokens plus 10,732 read from cache, 3,277 output. On the page it could sit
as a "what the AI saw / what it said" pair, with
`demo_prototype/holly_scene3_beat2_card.html` as the finished form.

**5. Human archetype review: `FOG_HOLLY_REVIEW.md` line 23 (kept), and
`fog_tagged.json` corrections log #109 (changed).**

Kept:
```
| scene3_beat2 | Trickster (confirmed) | Real unaware mark
  (Beth's "Hey! Not fair!") ...
```
(Beth's line is at `fog_full.txt` line 87: `Hey! Not fair!`.)

Changed (#109):
```
"beat_id": "scene140_beat6", "character": "MACKIE",
"llm_value": ["Great Mother"], "human_value": ["Shadow"]
```
The before/after reads well from `fog_report_model.json`, MACKIE
`scene140_beat6`, field `audience_perceived`:
- AI Output: "A protective/older figure snapping into sudden, frightening
  violence against a child in his care"
- Human Reviewed: "a sudden, frightening break from composure -- violence
  erupting without warning"

The script line: `fog_full.txt` lines 4484-4485, "Without warning,
Mackie’s big powerful hand grabs John’s / throat, squeezing."
`demo_prototype/mackie_scene140_beat6_card.html` already presents this.

**6. Pass 2: `fog_pass2_calls/synthesis_MACKIE.json`.** The traits the AI
named for Mackie:

```json
{"trait": "Controls the narrative and shifts blame away from his son to protect him from consequences during a crisis",
 "first_shown_beat_id": "scene75_beat1"}
```
One turning point it proposed (`turning_points[0]`): `scene75_beat3`,
`"turning_point_type": "escalation"`, compared with `scene75_beat1`. Its
`what_changes` text quotes profanity ("You fucked up. ..."), so it's a poor
fit for the page. If any AI-quoted line is used, check it against
`fog_full.txt` first (CLAUDE.md quote rule).

**7. Human Pass 2 review: `FOG_MACKIE_REVIEW.md` line 86, and
`fog_turning_points_reviewed.json` (MACKIE `scene140_beat6`).**

```
| scene140_beat6 | BR / mismatch (trait 2 continuation vs. 140_5) |
  **boundary_revealed, re-anchored as its own origin / matched**;
  **Principle 11 instance** | ...
```
```json
"reviewed": {"status": "re-anchored",
  "shape": "own origin (8a)",
  "trait": "a previously untested capacity for physical violence against his own son",
  "author_checked": true}
```
For a reader: the AI read the grab as more of the same control; review
read it as something new, the first time he turns violence on his son.

**Side step, plot facts: `fog_tagged.json` `plot_facts[0]`.** This is a
spoiler (it names who arranged Holly's disappearance), so leave it out of
the walkthrough, or put it behind a spoiler gate.

**8. Development read: `fog_dev_read.json`.**
```
GENRE: Crime Drama / Thriller
LOGLINE: A burnt-out, hard-drinking LA detective returns to his New
Hampshire hometown for his father's funeral and gets pulled into
investigating the disappearance of a young girl, a case his late father
secretly worked before his death, forcing him to confront buried secrets
from his own past and his family's hidden involvement.
```
(The synopsis contains the ending.) `report_guard_log.jsonl`'s last entry
shows a check at work: a logged formatting repair, `"old": "silent.a While"`
→ a paragraph break, "no words changed".

**9. Data layer: `fog_line_index.json`, `scene7_beat3`.**
```json
{"first_line": 198, "last_line": 202, "placement": "matched",
 "pdf_pages": [5], "printed_pages": [4]}
```
This is the step where "the scream is on page 4" comes from (PDF page 5,
printed page 4).

**10. Story Report: `fog_story_report.html`.** Better as screenshots than
as code. The candidates are section 4 (the archetype timeline, desktop and
phone), the map panel for MACKIE `scene140_beat6` in Human Reviewed
(showing "What changed in review"), and the AI Output / Human Reviewed
toggle.

## c) Where human review enters, and what it produces

| Where | What it produces | Recorded in |
|---|---|---|
| After Pass 1 (stage 5): every AI archetype call, per character | Kept / changed / removed archetype calls, field rewrites, character-label fixes; a reason for each | `fog_tagged.json` corrections log; `FOG_<NAME>_REVIEW.md`; summary in `FOG_COLD_RUN_FINDINGS.md` "Cold Pass 1 archetype accuracy" |
| After Pass 2 (stage 7): every turning point and every flag the AI drafted as other than consistent/matched | Final reaction-in-proportion and in-character verdicts; re-anchored or retired turning points; new causal-integrity principles (Principles 10 and 11 came out of the Full of Grace review; 8 and 9 came earlier, from Ocean's Eleven) | Corrections log; Pass 2 tables in `FOG_*_REVIEW.md`; `FOG_PASS2_CLOSEOUT.md`; `fog_turning_points_reviewed.json` (7 entries author-checked line by line, 29 transcribed and auto-verified); `CAUSAL_INTEGRITY_PRINCIPLES` in `tagging_schema.py` |
| Author rulings | One-off decisions recorded on a review row (e.g. MACKIE `scene140_beat11`: Great Mother, dark pole) | `FOG_<NAME>_REVIEW.md`; read by `report.py`'s pole parser |
| Plot facts (side step) | One fact corrected by the author | `fog_tagged.json` corrections log (`plot_facts[0]`); `FOG_COLD_RUN_FINDINGS.md` "Plot-facts stage" |
| Development read (stage 8) | Author check of four points, shown under the hood; the AI's text is left unchanged | `fog_dev_read.json` `author_check`; `FOG_COLD_RUN_FINDINGS.md` |
| Report copy (stage 10) | Wording edits from the review build ("Copy my edits"), applied to the source by hand | `report.py` comments ("Review edit N"); the local `fog_story_report_review.html` |

A one-line result for the reader: 57 of the 82 archetype calls the AI made
were kept exactly as it made them (69.5%; `FOG_COLD_RUN_FINDINGS.md`,
which warns never to cite the inflated 95.1% all-entries figure).

## d) Problems caught and fixed (or logged) during development, by stage

The finding numbers below refer to `FOG_COLD_RUN_FINDINGS.md` unless
another file is named.

1. **Extraction**
   - Default-mode `pdftotext` silently reorders short centered cues and
     misattributes speakers; `-layout` is mandatory (`parser.py`
     docstring; found on Lake of the Brokenhearted).
   - Full of Grace: two-column `-layout` garbling of TRUDY's Creed line,
     `scene216_beat6`, repaired from a `-raw` pull (finding 12, fixed). The
     same garbling on DOUG, `scene123_beat5`, is not fixed (finding 15).
2. **Parsing**
   - Side-by-side dialogue (4 blocks) read as one merged cue, and headstone
     text read as a cue: fixed by `fog_hand_patches.py`, which raises if
     the parse drifts.
   - JOHN's continuing speech after a parenthetical parsed as action
     (finding 5); MARCHAND's line split by a blank line (finding 7).
   - A two-line parenthetical drops JOHN's line (finding 16, not fixed).
   - The "glued action" heuristic splits dialogue that starts with a name
     (finding 20, not fixed).
   - From earlier scripts: the curly-apostrophe `CONT’D` fix (`parser.py`
     comments); `PARSING_BUG_IMPACT_REPORT.md` and `OPEN_ITEMS.md` for the
     earlier silent parse bugs.
3. **Beat detection**
   - RAYMOND missing from `characters_present` on `scene205_beat1`, a
     coverage gap (finding 2).
   - The emotional wave (`beat_detector.compute_script_wave`, VADER) read
     the scream and the confession as near-neutral and was dropped from
     the release ("Emotional wave" section; `README_NOTES.md`).
4. **Pass 1 tagging**
   - An out-of-schema value the validator rejected and discarded
     (finding 1; prompt clarified).
   - `displaced` responses rejected for a missing mechanism (finding 3,
     prompt fixed, 6 beats re-run).
   - `weight_proportionality` resolved early on 21 entries, reset
     (finding 4).
   - O'Shea split across three labels (finding 6).
   - An invented relationship and occupation for Reggie (findings 8 and
     14).
   - A goal and emotions not shown on the page (finding 9).
   - Hero placed on the wrong beat twice (finding 10).
   - YOUNG JOHN labelled JOHN (finding 13).
   - JOHN and YOUNG JOHN tracked as two people (finding 21, architectural;
     the report merges them).
   - Earlier scripts: `evidence_summary()` once cut dialogue to 70
     characters before the AI saw it (`integration.py` docstring;
     CLAUDE.md).
5. **Human archetype review**
   - `BeatTag.provenance` is beat-level, so it can't show whether a
     character was reviewed (CLAUDE.md; `OCEANS11_OPEN_ITEMS.md` item 11).
6. **Pass 2**
   - The validator forced "escalation" onto 13 turning points (finding 17,
     validator fixed).
   - Free-text "continuation of X" goes unvalidated (finding 18, not
     fixed).
   - The "point of no return" gap led to Principle 11 (finding 19).
   - Chunked resolution after DANNY's call truncated on Ocean's Eleven,
     and a stale TRUDY synthesis kept for comparison only (both in the
     `fog_pass2_runner.py` docstring).
7. **Human Pass 2 review**
   - Reviewed anchors and traits were never stored as data, so
     `fog_turning_points_reviewed.json` was built from the review files,
     with cited lines checked at build time (author decision D2;
     `build_fog_turning_points_reviewed.py` docstring).
   - The external-pressure test for boundary_revealed, which may need
     re-applying to other verdicts (`FOG_TRUDY_REVIEW.md` lines 507-515).
8. **Development read**
   - Two runs plus a length rule change.
   - A logged formatting repair (a stray "a").
   - Prompt v5/v6 version tracking with the exact prompt archived ("Development
     read" sections).
9. **Data layer**
   - The replay audit's named categories (`report_data.py`):
     `entity_rename`, `finding4_wp_reset`, `human_added_entry`,
     `kind_logged_as_archetypes`, `merge_removed_entry`,
     `unlogged_kind_change`.
   - Any unexplained difference stops the build.
10. **Report**
    - Guard scoping by text type, the approved-static list, and the
      verbatim definitions class (`STORY_REPORT_SPEC.md` "Scoping the
      guard").
    - Section 3 (consistency check) dropped as implied development notes
      (`STORY_REPORT_SPEC.md`).
    - "AI" not "model", and no old product name, both enforced by the
      build (`report.py` `model_word_check`, `old_name_check`).
    - The Great Mother pole isn't stored, so it's read from the review
      records (`FUTURE_WORK.md` item 3; section 4 under the hood).
    - One approximate timeline position (TRUDY `scene216_beat6`).

## e) What will be hard to explain plainly

- **"Cold."** The AI Output view isn't one run. It's Pass 1 from
  `7a6e69e` plus Pass 2 from `8079f93`, and Pass 2 ran after 196 Pass 1
  corrections. The report's label states this. A walkthrough needs one
  honest sentence for it.
- **Two passes, and why Pass 2 waits.** Deferring proportion and
  in-character judgments until the whole arc is visible guards against
  hindsight, but it only makes sense once the reader sees why a moment
  can't be judged in isolation.
- **Causal-integrity vocabulary.** `weight_proportionality`,
  `characterization_consistency`, `boundary_revealed`,
  `throughline_evolution`, `agency_alignment`. The report already uses
  plain stand-ins ("A change that's justified", "A limit revealed",
  "Reactions that hold together"), and the walkthrough should reuse them
  rather than invent new ones.
- **The non-tags.** `no_confident_archetype`, `functional_role_only` and
  `ordinary_reaction` are results, not failures, and the cold run never
  used `ordinary_reaction` at all (every one of the 19 came from review).
- **Principles 8a and 11, and the cross-layer rule.** The same Full of
  Grace beat (`scene223_beat1`) loses Hero at the archetype layer but
  keeps boundary_revealed at the causal-integrity layer, on purpose.
- **Signals are not meaning.** The beat detector's "sentiment delta" and
  "cut off (--)" are surface patterns; the wave failure is the clearest
  proof. Show the evidence, but don't let it read as emotion detection.
- **Accuracy numbers.** 57/82 is the honest figure. 95.1% must never
  appear. The Ocean's Eleven Pass 2 pilot match rates aren't accuracy figures
  either: their ground truth lacks the cases needed to measure accuracy
  (`OCEANS11_OPEN_ITEMS.md` line 1018).
- **The plot-facts side step.** It exists in the data but informed
  nothing, and it spoils the ending.
- **Line, page and beat numbers.** PDF page vs. printed page (PDF page 2
  is printed page 1), beat IDs, and line numbers in `fog_full.txt` are
  all different coordinate systems. The walkthrough should show printed
  pages only.
- **Character identity.** John/Young John (and Cheyenne) are merged for
  display but stored as separate characters; O'Shea was once three
  labels.
- **Visible names.** The source PDF is `full_of_grace.pdf` in this repo;
  the pages call it "the script PDF".
- **Spoilers.** The synopsis, plot facts, TRUDY's drowning sequence
  (scenes 213-217) and Mackie's scene 140 all reveal the ending or late
  twists. Decide on a spoiler policy before choosing excerpts.
- **Docs that don't match the code.** CLAUDE.md says
  `llm_orchestration.py` calls the API "via `urllib.request`, no
  `anthropic` SDK dependency". The code imports `anthropic` and uses
  `client.messages.create`. (The 1-hour cache TTL claim is accurate.) A
  technical appendix should describe what the code does.
