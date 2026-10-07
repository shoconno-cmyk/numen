# Full of Grace -- Pass 2 closeout (2026-10-03)

FOG Pass 2 (whole-arc `weight_proportionality` / `characterization_consistency`
judgment, per character) is closed. This file summarizes what the human
review did and found. The per-character `FOG_*_REVIEW.md` files are the
authoritative record of every verdict; `FOG_COLD_RUN_FINDINGS.md` holds the
findings. Line numbers are `fog_full.txt` (byte-identical to a fresh
`pdftotext -layout -enc UTF-8` pull of the script).

**Roadmap.** The FOG run (Pass 1 + Pass 2 + human review) was the
fully-cold pipeline test, and it is now complete. The next and only
remaining roadmap milestone is **packaging**: public repo, README, a demo
with pre-computed FOG examples, and sample outputs.

## What was reviewed

- **Worklist:** `fog_pass2_queue.json` (77b15c4), built from the completed
  LLM Pass 2 run (8079f93): **160 entries**, 138 `needs_correction_review`
  (drafted values to accept or correct) and 22
  `arc_claim_check_no_draft` (synthesis turning points on entries with no
  causal_integrity block, checked as arc-level claims only).
- **All 160 reviewed**, across 24 character entities. Audited 2026-10-03:
  every queue entry has a Pass 2 table row in its character's review
  record. Reviewed entries are annotated in the queue file, never removed.
- **The 138 drafted entries, before and after:**

  | characterization_consistency | LLM draft | After review |
  |---|---|---|
  | throughline_evolution | 77 | 18 |
  | boundary_revealed | 57 | 18 |
  | consistent | 4 | 102 |

## Corrections log

- **Total: 844 entries** in `fog_tagged.json`. `fog_tagged.json` validates
  (0 errors, 460 beats).
- **197-720 (524):** the LLM Pass 2 drafts, one entry per drafted beat,
  marked "AWAITING HUMAN REVIEW".
- **721-844 (124):** human corrections made during the review: 111
  characterization_consistency, 7 weight_proportionality, and 6 Pass 1
  fields found along the way (goal 2, archetypes 1, self_perceived 1,
  audience_perceived 1, emotion 1).
- Confirmations that change no value get no log entry (the no-op
  convention); they are recorded in the review files.

## Overturn tally

- **From REGGIE's queue onward: 32 of 34 boundary_revealed drafts were
  overturned.** REGGIE 3/3, DOUG 3/3, CHEYENNE 2/2, RICARDO 1/1, O'SHEA
  2/2, YOUNG JOHN 3/3, MACKIE 5/6, BETH 4/4, HOLLY 3/3, MARCHAND 1/1,
  RAYMOND 1/2, PETE 2/2, BLACK KID 1/1, LATINO KID 1/1
  (`FOG_LATINOKID_REVIEW.md`, cross-queue tally).
- **The two kept share one shape:** MACKIE scene140_beat6 and RAYMOND
  scene205_beat1 are real boundaries that the drafts had placed as
  continuations of an earlier beat. Both were kept only after being
  re-anchored as their own origin under 8a, and both rest on the
  character's own depicted act (RAYMOND: "Raymond starts to thrash his
  head against the metal tabletop. Over and over.", 6216-6217).
- **Whole worklist:** 47 of the 57 drafted boundary_revealed entries did
  not stay boundary_revealed. The 10 kept are TRUDY 6, JOHN 2, MACKIE 1,
  RAYMOND 1. JOHN and TRUDY, reviewed first, kept more of their drafts.

## Principles ratified or formalized during the pass

(`CAUSAL_INTEGRITY_PRINCIPLES` in `tagging_schema.py`; summaries in `CLAUDE.md`.)

- **Principle 10** (e26724d, 2026-09-29): an echo needs the tracked
  character's own action or line as primary evidence. Caught on TRUDY
  scene217_beat1, an "echo" resting on JOHN's line alone.
- **Principle 8, clauses 8a and 8b** (dae87f7, 2026-10-02).
  - **8a:** a singular climactic action is judged on whether the
    character's prior pattern made it foreseeable, not on whether it is
    the first showing.
  - **8b:** check that the escalated capacity is the same capacity, not
    a different one sharing a surface theme. The worked example is
    JOHN's risk to himself vs. lethal force against another person at
    scene172_beat6 ("He pops out of the room and returns fire--", 5494).
- **Principle 11** (finding 19 ratified, dae87f7, 2026-10-02; refined in
  05e0308): an act can be a turning point through irreversibility alone.
  For speech, the test is contingent (ultimatum) vs. unconditional (a
  flat declaration of a fixed future). It must be the tracked character's
  own act, by a character with enough established arc.
  - **5 instances / 4 characters:** TRUDY scene214_beat4, JOHN
    scene172_beat6, REGGIE scene172_beat6, JOHN scene223_beat1, MACKIE
    scene140_beat6 (0bd217e).
- **Principle 8 closing test and the cross-layer note** (05e0308): a
  never-shown strength counts as well as a limit, and 8a is declared the
  exception to the first-showing default. The archetype layer's Hero
  declared-intent rule stays strict on purpose (`CLAUDE.md`).

## Named tests developed in review

These are review tests recorded in the per-character files. They are not
numbered principles.

- **Trait conflation / shared subject (formalized as 8b).** Two capacities
  that share a surface theme are not one trait. Cases: TRUDY concealment
  vs. resentment; JOHN baseball avoidance vs. reciprocal honesty; JOHN
  risk to self vs. willingness to kill (`CLAUDE.md` cross-layer note).
- **"Something happens TO the character."** Cost imposed by others is not
  a change in the character.
  - First recorded on REGGIE scene172_beat7: being shot, "A howl from
    Reggie." (5498).
  - Named at O'SHEA (`FOG_OSHEA_REVIEW.md`).
  - 11 instances across 6 characters as of RAYMOND, and applied again in
    the ALBERTO, FEDERAL AGENT, DET. MCAVOY and MANAGEMENT records.
- **Universal reaction.** A reaction anyone would have tells us nothing
  character-specific. It was first applied at CHEYENNE
  (`FOG_CHEYENNE_REVIEW.md` batch 3). Example: "Hear the sobs of Beth and
  Krista." (251), BETH and KRISTA scene11_beat1.
- **Decency vs. distinctiveness.** Basic decency suited to the situation
  is not a personal trait. From DOUG scene175_beat2 (log 777): "I'm sorry,
  John. We really tried." (5612). Its whole-character extension, the
  functional-device caution, starts at RICARDO (`FOG_RICARDO_REVIEW.md`).
- **Reveal vs. boundary (candidate test, not yet a principle).** "A
  reveal changes what the audience knows, not what the character is."
  From LATINO KID scene19_beat3: "John got played by a 12-year old.
  Damn." (801-802). Compare Principle 9.

## Findings 17-21: status at close

| Finding | Subject | Status |
|---|---|---|
| 17 | Synthesis validator forced "escalation" onto 13 turning points | Validator fixed (`validate_turning_points()`). All 5 mandatory review items reviewed; item 5 (MANAGEMENT scene107_beat2 orphan) closed with no causal_integrity block needed. All 4 listed model quotes verified verbatim (3292/3361/3366, 5032, 5562, 6148). Cold drafts deliberately not rewritten. |
| 18 | Free-text "continuation of X" lets boundary_revealed be inherited without a Principle 8 retest | **Decision: build** a structured `continuation_of` field plus the "every non-consistent verdict states its own limit" rule, scheduled before the next cold run on a new script. Evidence: the 32-of-34 overturn rate. Not built yet. |
| 19 | Point-of-no-return beat | **Ratified as Principle 11.** Four open items carried forward (below). |
| 20 | "Glued action" parser heuristic splits dialogue | Documented, not fixed. Grouped with findings 5, 7, 12, 15 and 16 as one parser bug family ("dialogue that loses its speaker"). |
| 21 | One person stored as two character entities | Architectural, not fixed. Instances: JOHN/YOUNG JOHN; IRATE MAN/PETE. Related notes: CHEYENNE 60_1 hidden throughline; the hobbyhorse motif (31-32, 2634-2635, 6618-6620). |

## Scope decisions accepted at close

- **MIN_BEATS = 3** (author, 2026-09-28; `fog_pass2_runner.py`): Pass 2
  runs only for characters with 3+ beats.
- **Left at `requires_second_pass` by design:** OLDER MAN scene37_beat2,
  DR. SHEPHARD scene205_beat1 and LAWYER scene205_beat1. These are the
  only such values left in `fog_tagged.json`.

## Carried forward (known open items, not blockers)

1. **Principle 11 open items:**
   - (a) the axis 3 downstream-connection filter is still unvalidated;
   - (b) 8a vs. premeditation/preparation beats (REGGIE scene134_beat2);
   - (c) whether going from a held weapon to a fired one is a change of
     type or of scale (JOHN vs. REGGIE scene172_beat6);
   - (d) a declaration that is unconditional in grammar but empty in
     substance (CHEYENNE scene155_beat11, cf. JOHN scene223_beat1).
2. **Finding 18 build**, before the next cold run on a new script.
3. **Parser bug family** (findings 5, 7, 12, 15, 16, 20), to be searched
   for together in a parser-hardening pass.
4. **Finding 21**, character identity across entities (needs a design
   decision).
5. **Reveal vs. boundary**, a candidate test.
6. **Design note A (future work).**
   - MIN_BEATS = 3 is a crude proxy for "worth tracking", and Pass 2
     synthesis reliably over-claims on secondary characters (32 of 34
     boundary_revealed drafts overturned).
   - A functional-role filter is the likely improvement.
   - No per-character functional ruling was made for the nine small
     characters reviewed last.
   - Detail is in `FOG_COLD_RUN_FINDINGS.md`, "Pass 2 closeout notes".
