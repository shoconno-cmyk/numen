# Full of Grace -- TRUDY archetype review record

Per-character review record for TRUDY's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether TRUDY's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each TRUDY verdict, including confirmations that
change no data. Same convention as `FOG_JOHN_REVIEW.md`.

**Status column:** `pending apply` means the verdict is decided here but
the tagged data file has not been changed yet. `applied` means the change
has landed (`git log` on this file gives the commit). Confirmations that
change no data are also marked `applied`. They get no corrections-log
entry, per the no-op convention, and the beat's provenance is set to
`llm_human_confirmed`.

Scope: TRUDY's 17 real-archetype beats in the cold output (2026-09-28
enumeration: TRUDY present on 68 beats, 17 with a non-empty archetypes
list). Every tag was model output that nobody had reviewed, and no
corrections-log entry named TRUDY before this review. scene154_beat2 and
the scene155 car scene, both touched during JOHN's review, are CHEYENNE
beats; TRUDY is not present on either.

## Chunk 1: scene30_beat1 - scene213_beat7 (2026-09-28)

Each beat was checked against a fresh `pdftotext -layout` pull of
`full_of_grace.pdf`, with all stored turns found
verbatim. On scene143_beat7, turns 22 and 23 are side-by-side dual
dialogue in the PDF; they were checked by eye against the two columns and
match word for word, speakers included.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene30_beat1 | Great Mother (confirmed) | Real depicted charity and unconditional comfort. Author-confirmed: "A look of recognition on her face" is Trudy recognizing Raymond -- deliberate setup, not an unexplained beat. Payoff check: no later scene returns to the soup kitchen or explains the recognition; logged as `FOG_COLD_RUN_FINDINGS.md` finding 11 (continuity note, not an archetype question). | applied |
| scene30_beat2 | ordinary_reaction, Great Mother removed | Author-confirmed: the caregiving act already happened in beat 1; this beat only shows her watching the man leave ("Trudy watches after the man for a beat."), nothing newly offered or enacted. | applied |
| scene34_beat2 | Persona (confirmed) | Clean fit, no changes. | applied |
| scene82_beat1 | Great Mother (confirmed) | Clean fit, no changes. | applied |
| scene131_beat1 | Shadow, Trickster removed; fields rewritten | Trickster fails outright: no unaware mark; nothing is done to the priest, and no social order is destabilized. Author-confirmed intent: repressed desire surfacing despite her outward piety ("an odd touch of seduction in her eyes"), in a context (communion) that makes the repression visible -- genuine Shadow. self_perceived, audience_perceived, goal, goal_status (achieved -> none) and emotion rewritten to Shadow's mechanism (something surfacing against her control), replacing the Trickster framing (a deliberate provocation aimed at destabilizing the ritual). | applied |
| scene141_beat2 | Chorus (confirmed) | Author-confirmed: she steps back from her own immediate stake to name a pattern in how John treats people ("Everyone here is just trying their best."), not just defending Doug in the moment. No field changes. | applied |
| scene143_beat7 | Shadow (confirmed), reasoning corrected | Author-confirmed: "She reloads--" describes the speed of an old wound surfacing, not a calculated tactical choice -- she's barely given it thought, which is evidence of something breaking through despite her control, not a deliberate weapon being deployed. This is the basis for Shadow here, replacing any tactical-delivery reading. No field changes; the existing fields (resentment, bitterness breaking through) already fit. | applied |
| scene213_beat7 | Shadow (confirmed) | No changes. weight_proportionality was `matched` in the Pass 1 output, one of finding 4's 21 premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |

**Chunk 1 follow-up field fixes (2026-09-28):** scene30_beat2's fields
still described active caregiving after the Great Mother ->
ordinary_reaction correction. They now match the verdict:
self_perceived "watching him walk away after giving him the soup",
audience_perceived "a quiet, lingering moment after the exchange", goal
goalless, goal_status achieved -> none, emotion "quiet attentiveness",
agency_role active -> passive. Each change is logged as a follow-up to the
beat's archetype correction.

## Chunk 2: scene214_beat3 - scene216_beat7 (2026-09-28)

Scenes 214-216 are one continuous flashback (the baptism on the boat),
between scene213_beat7's "A FEW DAYS AGO..." and "THE PRESENT:". Each
beat was checked against a fresh `pdftotext -layout` pull, with all
stored turns found. scene216_beat6's first turn was garbled in both the
layout pull and the stored text. It was repaired from a `pdftotext -raw`
pull of p. 123 (`FOG_COLD_RUN_FINDINGS.md` finding 12). That repair is a
text-completeness fix with no corrections-log entry.

**Isolation test:** each beat is judged on its own text. Great Mother
(dark pole) applies where the beat's own text lays ritual performance
(quoted baptismal liturgy, the Creed, "I taught her the Bible") over the
violence. Shadow applies where the beat's own text has no ritual language
and shows the violence bare, or where something surfaces despite her
control.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene214_beat3 | Great Mother (confirmed, dark pole) | Author-confirmed: a real caregiving/spiritual bond (Godmother, catechist -- "I taught her the Bible") sustained and weaponized through unbroken ritual performance laid directly over escalating violence. | applied |
| scene214_beat4 | Great Mother (confirmed, dark pole) | Same basis: "All that was left was the baptism." | applied |
| scene215_beat1 | Shadow (confirmed; isolation test) | Author-confirmed: judged on this beat's own text alone, which has no ritual language, no liturgy and no dialogue, just "Held there. She writhes and struggles mightily.". The ritual veneer that grounds the Great Mother beats in this sequence is absent, leaving the raw violence exposed on its own. No field changes. | applied |
| scene216_beat1 | Great Mother (confirmed, dark pole) | Same basis as scene214_beat3: quoted baptismal liturgy over the dunking. | applied |
| scene216_beat2 | Great Mother (confirmed, dark pole), emotion corrected | Same basis. emotion: "obliviousness to Holly's panic" replaced with "dissociation" -- the text shows persistence, not lack of perception; matches the term on scene216_beat4 and scene216_beat6. audience_perceived ("ritual fervor overriding the child's visible distress") already covers this and is unchanged. | applied |
| scene216_beat4 | Great Mother (confirmed, dark pole) | Same basis: the liturgy and her own baptismal vows ("I do") recited over Holly being forced back under. weight_proportionality was `mismatch` in the Pass 1 output, one of finding 4's 21 premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |
| scene216_beat5 | Shadow, Great Mother removed; fields rewritten | Author-confirmed, isolation test: no ritual language in this beat's own text ("Holly begins to overpower Trudy. Trudy strikes Holly across her head. Repeatedly. She shoves her head deeper underwater.") -- raw physical escalation, not the weaponized-ritual mechanism. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays deferred. | applied |
| scene216_beat6 | Great Mother (dark pole), Shadow removed; fields rewritten; text repaired | Correction, not a confirmation: the cold output stored Shadow. Author-confirmed: unbroken ritual composure -- she calmly finishes her own baptismal vows ("... I do.") straight through Holly going still ("Holly stops struggling."), the same mechanism as the other Great Mother beats in this sequence. self_perceived, audience_perceived, goal and emotion rewritten from the removed Shadow reading (violence/rage breaking through) to devotion carried through to a lethal end; goal_status stays achieved. Turn 11 repaired (finding 12). | applied |
| scene216_beat7 | Shadow (confirmed) | "Trudy looks horrified." is a real, textually anchored break in her ritual composure -- the one moment in the sequence where something surfaces despite her control rather than being performed. No field changes. | applied |

TRUDY's archetype review is complete. Every TRUDY beat with a real
archetype has a row (16, recounted 2026-09-28). scene30_beat2 also has a
row for its correction to ordinary_reaction.

## Pass 2 synthesis: known defects to correct during TRUDY's Pass 2 review (logged 2026-09-29)

The synthesis used for TRUDY's Pass 2 run is `fog_pass2_calls/synthesis_TRUDY.json`
(identical copy kept as `synthesis_TRUDY_v2.json`). It was generated after
Principle 10 and the first trait-statement instruction ("reflect only what's shown
at first_shown_beat_id"), but BEFORE the sharpened follow-up ("describe only what
the beat depicts, not an inference, motive, or interior state"). By author decision
there was no third re-run. `synthesis_TRUDY_v1.json` predates both fixes and is
comparison-only.

Two trait labels in it compress later material into the label, and need correcting
when TRUDY's Pass 2 drafts are reviewed:

- **"Hidden resentment/jealousy toward Cheyenne and Holly, masked behind piety,
  surfaces first as silent evasion"** (first_shown `scene57_beat2`). That beat's own
  text shows only evasion: asked "When were you gonna tell me about Cheyenne's
  girl?", she "has no answer." Resentment, jealousy and masking are not depicted
  there. This is the defect the sharpened instruction targets. It is still present
  in the synthesis being used.
- **"Capacity for premeditated, controlling, extreme action carried out under
  religious justification"** (first_shown `scene213_beat7`). That beat shows the
  premeditation ("I hired Raymond to take her. It was just for a few days.") and her
  stated motive ("I wanted to teach Cheyenne a lesson... Show her what it means not
  to have children."). It has no religious content. "Under religious justification"
  appears only at the later scene216 drowning/baptism sequence. The same
  hindsight-compression problem as the original trait 3; not caught by the
  instruction fix.

**Open question, check once during this review (not blocking the full run):** does
`integration.evidence_summary()`, which `pass2_orchestration._format_beat_for_pass2()`
uses to build the synthesis input, include Pass 1's interpretive fields
(`self_perceived` / `audience_perceived`), or only raw beat text? If it includes
them, that's a path for hindsight language to leak into Pass 2 synthesis
independently of any prompt instruction. For example, scene213_beat7's stored
audience_perceived reads "a woman's repressed envy and grief over childlessness
curdling into a cruel scheme against another mother".

## Pass 2 review: drowning sequence, scene213_beat7 - scene217_beat1 (2026-09-29)

Reviewed as one continuous read, against the 6 claimed limits (A-F) in
`FOG_COLD_RUN_FINDINGS.md` finding 18. Source: a fresh `pdftotext -layout` pull
of pp. 121-124. Every stored turn matches it except scene216_beat6's Creed line;
the `-layout` pull garbles that line into two columns (finding 12), and the
stored repair matches a fresh `-raw` pull exactly. scene214_beat2, scene216_beat3
and scene216_beat8 have no TRUDY entry. All values below are
characterization_consistency; weight_proportionality stays `matched` throughout.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene213_beat7 | boundary_revealed | **boundary_revealed, confirmed** | no log entry (no-op convention); provenance stays `llm_human_corrected` from the earlier finding 4 weight_proportionality reset |
| scene214_beat1 | boundary_revealed | consistent | log: "I panicked" elaborates why the confessed act happened, not a new capacity (Principle 9) |
| scene214_beat3 | boundary_revealed | consistent | log: the grooming backstory is mechanism for the already-confessed capacity |
| scene214_beat4 | boundary_revealed | **boundary_revealed, confirmed as a NEW limit** | no log entry (no-op convention); provenance stays `llm_human_confirmed`. See below |
| scene215_beat1 | boundary_revealed | consistent | log: same continuous physical act as scene214_beat4, seen from under the water |
| scene216_beat1 | boundary_revealed | consistent | log: the liturgy is the baptism plan stated at scene214_beat4 being carried out |
| scene216_beat2 | boundary_revealed | consistent | log: continuing liturgy-as-method |
| scene216_beat4 | boundary_revealed | consistent | log: same basis as scene216_beat2 |
| scene216_beat5 | boundary_revealed | **throughline_evolution** | log: escalation of the scene214_beat4 limit, vs. scene214_beat4 |
| scene216_beat6 | boundary_revealed | consistent | log: same basis as scene216_beat2/216_beat4 |
| scene216_beat7 | boundary_revealed | **boundary_revealed, confirmed** | no log entry (no-op convention); provenance stays `llm_human_confirmed` |
| scene217_beat1 | boundary_revealed | consistent | log: the draft's own rationale already said "a genuine limit to the trait, not a new one" |

**Result:** of the 12 drafted TRUDY entries in this sequence, **3 are
boundary_revealed** (scene213_beat7, scene214_beat4, scene216_beat7), **1 is
throughline_evolution** (scene216_beat5), and **8 are consistent**. That took 9
new corrections-log entries. This covers 12 of TRUDY's 19 boundary_revealed
drafts. The other 7 are outside the sequence and still unreviewed: scene40_beat3
(limit A), scene143_beat7 (B), scene194_beat1, scene195_beat1, scene195_beat2 and
scene195_beat4 (C), and scene213_beat2 (D).

**Confirmation of finding 18's diagnosis.** In the sequence, 10 of the 12 drafts
were re-claims of an earlier beat's limit, stamped with the same category down a
continuation chain. 8 of those 10 turned out to be consistent. Inheritance, not the
trait 6/7 labeling defect alone, drove the volume.

**A synthesis limit was split, not only collapsed.** The synthesis treated
scene214_beat4 as a continuation of limit E, the hiring/arranging capacity
confessed at scene213_beat7. Review found a distinct capacity here: **personal
physical violence overriding a victim's visible resistance**, first shown at
scene214_beat4 ("Holly struggles. Trudy forces Holly's head overboard."). Trudy
moves from arranging harm through Raymond to personally overriding Holly's active
resistance and continuing anyway. A baptism's meaning (welcome, joy) is already
being violated in real time, before the drowning itself begins. The comparison
beat is scene213_beat7, still the prior reference point, but this is its own
limit, not a continuation of the arranging capacity. scene216_beat5's strikes are
then an escalation of *this* limit ("different form of violence [strikes vs.
forced submersion] but the same pathway toward a goal -- getting Holly baptized by
any means necessary"). So review can separate one synthesis-claimed limit into two
genuine ones where the text supports it, as well as collapsing re-claims downward.

**scene216_beat7** is a genuine break anchored in the text ("Trudy looks
horrified."): composure cracking into real horror, distinct from both
premeditated-violence limits (scene213_beat7, scene214_beat4).

**Recording decisions (author, 2026-09-29):**
- **Confirmations follow the project's no-op convention.** They get no
  `log_correction()` entry; this section is TRUDY's per-character record for
  scene213_beat7, scene214_beat4 and scene216_beat7. scene216_beat7 is shared
  with HOLLY, whose entry there has no causal_integrity block.
- **scene216_beat5's "escalation" is recorded as `throughline_evolution`.**
  "Escalation" isn't a characterization_consistency value, and Principle 8 maps
  an escalated established capacity to throughline_evolution.
- **scene216_beat1's basis is anchored at scene214_beat4.** The review's first
  wording tied the liturgy to scene213_beat7's confession ("then we'd let Holly
  go"). That beat never mentions a baptism; the plan is first stated at
  scene214_beat4: "All that was left was the baptism."
- **The comparison-beat and limit-description changes live only here and in the
  log notes.** They cover scene214_beat4 (vs. scene213_beat7, new limit) and
  scene216_beat5 (vs. scene214_beat4). `fog_pass2_calls/synthesis_TRUDY.json`
  stays unedited as the cold record (finding 17).

## Pass 2 review, batch 2: the rest of TRUDY's boundary_revealed claims (2026-09-29)

Source: a fresh `pdftotext -layout` pull, with speaker attribution checked
against raw cues. These items cover the 7 boundary_revealed drafts outside the
drowning sequence, plus scene143_beat6 and scene57_beat3, and the no-draft
turning point scene193_beat1. All values are characterization_consistency;
weight_proportionality stays `matched` throughout.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene40_beat3 | boundary_revealed | **boundary_revealed, confirmed** | no log entry (no-op); provenance stays `llm_human_confirmed`. A genuine structural reversal of who cares for whom. At scene32_beat2 she starts the embrace, joyful, holding John; here John crosses to her and she is the one breaking down while he holds her. A real, previously untested limit on her steady-caretaker role |
| scene143_beat6 | throughline_evolution | **throughline_evolution, confirmed** | no log entry (no-op); provenance `llm_unreviewed` -> `llm_human_confirmed`. A clean escalation: silence (scene57_beat2's "She has no answer.") becomes actual speech, the same trait more overt |
| scene143_beat7 | boundary_revealed | **boundary_revealed, confirmed** | no log entry (no-op); provenance stays `llm_human_confirmed`. John names it outright ("You were always jealous of Cheyenne"), and Trudy's retort ("Cheyenne never had to grow up, John... And neither did you.") tacitly accepts the framing rather than denying it. A genuine depth reveal beyond scene143_beat6's partial admission. Source flag below |
| scene213_beat2 | boundary_revealed | **boundary_revealed, confirmed** | no log entry (no-op); provenance `llm_unreviewed` -> `llm_human_confirmed`. A reveal distinct from scene213_beat7: her faith cracking specifically ("I did. Twice. When mom died I had my first doubts... And when I found out I couldn't have children--"), directly reversing scene34_beat2's composed "Maybe it's just not in God's plan, right?" Different trait, different limit, both genuinely exposed in the same confession |
| scene57_beat3 | consistent | **consistent, confirmed against text** | no log entry (no-op); provenance `llm_unreviewed` -> `llm_human_confirmed`. The finding 17 downgraded entry; the draft was already right |
| scene194_beat1 | boundary_revealed | consistent | log: the same unbroken prayer continues word for word through the raid; no character-level change |
| scene195_beat1 | boundary_revealed | consistent | log: same basis |
| scene195_beat2 | boundary_revealed | consistent | log: same basis |
| scene195_beat4 | boundary_revealed | consistent | log: same basis |
| scene193_beat1 | no draft | **arc claim likely does not hold** | no causal_integrity block, so nothing to correct; marked in `fog_pass2_queue.json` (`arc_claim_check_no_draft`) |

**The prayer-sync chain (scene193_beat1 - scene195_beat4), author-confirmed
reasoning:** Trudy never appears on screen in this sequence. It is Raymond
alone, praying, intercut with an off-screen shared "RAYMOND/TRUDY" cue showing
the words match ("His words matching Trudy's--"). Trudy is never shown
learning anything, reacting to anything, or doing anything beyond her
established rosary habit. What changes is the audience's understanding
(dramatic irony, foreshadowing the Raymond connection), not Trudy's own
behavior or awareness. That is the "audience learns something, character
doesn't" pattern Principle 9 excludes. The same reasoning applies to the
orphaned synthesis turning point at **scene193_beat1**. Its claim, "exposing a
previously unknown, literal connection between her private devotion and the
kidnapper, recontextualizing her piety as entangled with the crime", is a claim
about what the audience learns, not about Trudy's own character, so it likely
doesn't hold. It is the anchor the four drafts above chained from (finding 18).

**Source flag, scene143_beat7:** stored turn 27 (TRUDY) ends "...Maybe she
would've been better off in there. Maybe", and turn 28 stores "Holly would've
been better off." as unattributed action. `fog_full.txt` and both fresh pulls
show one continuous TRUDY speech with no interruption. This is **not already
covered by findings 5, 7, 12, 15 or 16**. Those are interrupted-dialogue
failures (page break, blank line, two-column split, wrapped parenthetical).
This one is the parser's "glued action" heuristic (`parser.py`, dialogue branch
of `parse_script()`): a dialogue line that begins with a known character name
followed by a lowercase word ("Holly would've") is split off as action. A
script-wide check found 4 such false positives:

- scene123_beat13, JOHN: "Mackie and his lackies..."
- scene143_beat7, TRUDY: "Holly would've been better off."
- scene155_beat9, JOHN: "Mackie and Reggie?"
- scene214_beat3, TRUDY (V.O.): "Cheyenne wasn't happy about it. But Holly was
  excited. She was almost there. I was her Godmother."

It also turned up one new blank-line split of finding 7's kind: scene64_beat8,
CHEYENNE's "help." None of these is repaired. They don't change any verdict
here. scene214_beat3's drowning-sequence verdict was made from the raw text,
where the line reads correctly as TRUDY V.O.

**Final tally, TRUDY's 19 claimed boundary reveals (full arc):**

- **6 boundary_revealed:** scene213_beat7, scene214_beat4, scene216_beat7,
  scene40_beat3, scene143_beat7, scene213_beat2.
- **1 throughline_evolution:** scene216_beat5, the escalation of the
  scene214_beat4 limit.
- **12 consistent:** the 8 drowning-sequence re-claims and the 4 prayer-sync
  beats.

That totals 19. scene143_beat6 (throughline_evolution, confirmed) was never
one of the 19; its draft was throughline_evolution from the start. Against
finding 18's grouping:

- **All 5 first claims inside the 19 held:** A scene40_beat3, B scene143_beat7,
  D scene213_beat2, E scene213_beat7, F scene216_beat7.
- **Of the 14 re-claims,** 12 are consistent, 1 split out as a genuine new limit
  (scene214_beat4), and 1 is throughline_evolution (scene216_beat5).
- **C's anchor, scene193_beat1** (outside the 19, no draft), likely doesn't hold.

**TRUDY's queue status:** 21 of her
24 `needs_correction_review` entries reviewed. Still pending are the 3
throughline_evolution drafts: scene57_beat1, scene131_beat1, scene188_beat1.

## Pass 2 review, final batch: scene57, scene131, scene188, and the trait 6 split (2026-09-29)

Source: fresh `pdftotext -layout` pulls. Speaker attribution was checked
against raw cues, and every quote below was confirmed in the pull in the
same session. All values are characterization_consistency;
weight_proportionality stays `matched` throughout.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene57_beat1 | throughline_evolution | consistent | log. First-claim beat for a **new trait** (see below), not an escalation of "deflects/avoids hard conversations". There is no deflection; she raises the hard topic directly: "I noticed you skipped out on your own father's funeral." |
| scene57_beat2, flare ("Don't fucking start, man.", the dishwasher slam, "Hey!") | consistent | **consistent, confirmed** | no log entry (no-op); provenance `llm_unreviewed` -> `llm_human_confirmed`. The same resentment as scene57_beat1, continuing and visibly erupting; a direct continuation, not an escalation or a new limit |
| scene57_beat2, ending silence ("Her anger dampens. She has no answer.") | consistent | **consistent, confirmed; ANCHOR of a new trait** | same entry as the row above. First-claim beat for "conceals the truth about Holly's disappearance, caught when confronted" |
| scene131_beat1 | throughline_evolution | **boundary_revealed** | log. "A sick sort of devotion." See the **OPEN ITEM** below |
| scene188_beat1 | throughline_evolution | **boundary_revealed** | log. The first private, solitary devotional act in her arc |

### The chronology behind scene57: Doug's porch scene (scene56)

scene56 ("EXT. KIERSTEAD HOME - FRONT PORCH - DUSK") comes directly before
scene57 ("INT. KIERSTEAD HOME - KITCHEN - CONTINUOUS"). In scene56_beat5 and
scene56_beat6, Doug tells John that Mackie was "Consulting on the Holly
Roberts case? ... Cheyenne's girl?". John is stunned ("Cheyenne? Cheyenne's
daughter is missing?"), and Doug realizes: "I thought you knew. I'm sorry. I
thought Trudy -- she was gonna--". Then "John goes into the house."

So John walks into the kitchen already knowing about Holly, and knowing Trudy
was supposed to tell him. His question at scene57_beat2 ("When were you
gonna tell me about Cheyenne's girl?") uses Doug's exact phrase. Trudy's
silence ("Trudy looks to Doug, then back to John. Her anger dampens. She has
no answer.") comes with Doug in the room. It is not resentment, and not a
spontaneous slip. She is being confronted about a specific, pre-existing lie
of omission about Holly's disappearance, and recognizes she has been caught.

### Synthesis-record note: trait 6 is split into two traits (no field to change)

Synthesis trait 6, "Hidden resentment/jealousy toward Cheyenne and Holly,
masked behind piety, surfaces first as silent evasion" (anchored at
scene57_beat2), merged two different kinds of psychological material because
both involve Holly and Cheyenne:

- **Concealment:** "conceals the truth about Holly's disappearance, caught
  when confronted." New trait, anchored at **scene57_beat2's ending silence**.
  This is what the silence actually shows, given the scene56 chronology.
- **Resentment:** trait 6 is re-anchored to **scene143_beat6** and reworded
  as **"resentment/jealousy over the family's favoritism toward Cheyenne and
  Holly."** The "masked behind piety" and "surfaces first as silent evasion"
  framing is dropped; it belonged to the concealment moment, not to this
  trait. The resentment is first voiced at scene143_beat6 ("I never liked the
  way dad treated her.").

A second new trait also comes from this batch:

- **Resentment at John's rejection of his hometown/family role,** anchored at
  **scene57_beat1**. She wants him to take up the family/sibling role in a
  crisis; his answer (back to the motel, "flying to L.A. in the morning") is a
  rejection she answers with the funeral-skipping jab. The flare at
  scene57_beat2 is this trait continuing.

Like scene193_beat1's "claim likely doesn't hold", this is recorded here only.
`fog_pass2_calls/synthesis_TRUDY.json` stays unedited as the cold record
(finding 17), and `fog_tagged.json` has no trait field.

**Flag, not resolved: scene143_beat6's stored verdict now rests on a moved
anchor.** The author asked that scene143_beat6 and scene143_beat7 keep their
verdicts, and both are unchanged in the data. They are **throughline_evolution**
and **boundary_revealed** respectively; the instruction for this batch called
them "first-claim and escalation", which doesn't match what is stored.
scene143_beat6's throughline_evolution was confirmed in batch 2 as an
escalation *from* scene57_beat2's silence ("silence becomes actual speech").
With that silence reassigned to the concealment trait and trait 6
re-anchored *at* scene143_beat6, scene143_beat6 becomes the resentment
trait's first showing. By the rule applied to scene57_beat1 and scene57_beat2
in this same batch, a first showing would be consistent. **Revisit
scene143_beat6** with the re-anchored trait in mind.

**Resolved (2026-09-29, author-confirmed):** scene143_beat6 is now
throughline_evolution -> **consistent**, logged via `log_correction()`. It
is trait 6's first-claim beat ("That is so not true! I never liked the way
dad treated her."), so it can't also be an escalation of itself. The same
first-showing rule was applied to scene57_beat1 and scene57_beat2.

**Comparison chain after the split, confirmed:** scene143_beat7
(boundary_revealed, unchanged) is compared against **scene143_beat6** in
both the synthesis turning point ("escalation vs. scene143_beat6") and the
resolver's checked_against ("escalation vs. scene143_beat6 (Hidden
resentment)"). The batch 2 row above also measures it against
"scene143_beat6's partial admission". Nothing in scene143_beat7's record
points to scene57_beat2. The resentment chain is internally consistent:

- scene143_beat6: first claim (consistent)
- scene143_beat7: depth reveal beyond it (boundary_revealed)

The concealment trait (scene57_beat2) stands apart. The trait label in the
unedited synthesis file still reads "Hidden resentment/jealousy toward
Cheyenne and Holly". The reworded label lives only in this record.

### scene131_beat1: "sick devotion" (boundary_revealed)

Author-confirmed: not repressed desire breaking through despite her piety,
but devotion itself curdled. Sensuality and faith are fused, not one
interrupting the other ("presents her tongue to him, sensually"; "an odd
touch of seduction in her eyes"). A previously hidden, corrupted capacity of
her faith trait, exposed here for the first time. It is not an intensified
version of scene30_beat1 or scene128_beat1, both of which stay consistent.

> **OPEN ITEM, not decided here.** "scene131_beat1 Shadow archetype tag vs.
> Pass 2 'sick devotion' boundary_revealed classification -- needs
> reconciliation in a future session, not decided here." The archetype review
> (chunk 1, above) tagged this beat **Shadow**: repressed desire surfacing
> *despite* her control, an involuntary crack. Its fields say so:
> `emotion: ["repressed desire", "unease", "involuntary"]`, `goal: "none -- this
> happens despite her, not because of a goal"`. The Pass 2 reading is
> devotion operating *as she intends*, just corrupted. These are two different
> accounts of the same beat's psychology. By author decision the Shadow tag
> and its fields are left **exactly as committed** (asserted unchanged when
> this batch was applied); only characterization_consistency changed.
>
> **CLOSED 2026-10-01:** Shadow -> ordinary_reaction, and
> characterization_consistency -> consistent. See "scene131_beat1
> resolution" at the end of this file.

### scene188_beat1: boundary_revealed

The first private, solitary devotional act in her arc. Every earlier TRUDY
faith beat is public or social: the soup kitchen (scene30), the airport
"Praise God" (scene32), the funeral, the choir (scene128), communion
(scene131), the meal blessing with Doug (scene139). It comes after Holly's
death is public knowledge (scene181_beat1, "Holly's wake"). It also runs
alongside Raymond's call to the Dover Police Department in the same sequence
(scene186-187: "Good morning, Dover Police Department, how may we help
you?"). Private prayer as personal reckoning: a previously untested register
of her faith trait, not an intensification of her public devotion.

Two items in the instruction for this beat were **not verified and are not
used as evidence here**:

- The quoted phrase "Trudy knows her time is up" does not appear anywhere in
  the script (fresh `-layout` pull).
- Raymond's call is to the Dover Police dispatch line, not 911. The only "911"
  in the script is John dialing it in the furnace room.

The instruction also described this verdict as "already settled in this
session". No earlier decision on scene188_beat1 was recorded in this Claude
Code session; its stored value was throughline_evolution until this batch.

### TRUDY Pass 2: final tally

All 24 of TRUDY's `needs_correction_review` entries are reviewed:

| Outcome | Count | Beats |
|---|---|---|
| boundary_revealed | 7 | scene40_beat3, scene143_beat7, scene188_beat1, scene213_beat2, scene213_beat7, scene214_beat4, scene216_beat7 |
| throughline_evolution | 1 | scene216_beat5 |
| consistent | 16 | scene57_beat1, scene57_beat3, scene131_beat1 (closed 2026-10-01, line 453), scene143_beat6, scene194_beat1, scene195_beat1, scene195_beat2, scene195_beat4, scene214_beat1, scene214_beat3, scene215_beat1, scene216_beat1, scene216_beat2, scene216_beat4, scene216_beat6, scene217_beat1 |

(The tally was updated 2026-09-29 after scene143_beat6 was resolved. It
was 8 / 2 / 14. Updated again 2026-10-05: scene131_beat1 moved to consistent per the 2026-10-01 closure, line 453.)

- **Corrections logged across TRUDY's Pass 2:** 17 (9 drowning sequence + 4
  prayer-sync + 3 final batch + 1 scene143_beat6 follow-up). Every other
  reviewed entry is a no-op confirmation recorded in this document.
- **No-draft item:** scene193_beat1, whose claim likely doesn't hold.
- **Synthesis-level changes:**
  - trait 6 split into concealment (anchor scene57_beat2) and resentment over
    favoritism (re-anchored to scene143_beat6);
  - new trait "resentment at John's rejection of his family role" (anchor
    scene57_beat1);
  - scene214_beat4 split out as its own limit (drowning-sequence section).
- **Named pattern observed:** the finding 19 point of no return
  (scene214_beat4), instance 1 of 3.
- **Open item carried forward (the only one):** **scene131_beat1**, Shadow
  archetype vs. "sick devotion" boundary_revealed. It needs reconciliation
  in a future session. The scene143_beat6 flag is resolved (see above).
  **RESOLVED 2026-10-01** (see the next section). The tally above was
  written before that and still counts scene131_beat1 as boundary_revealed.
  The current tally is **7 boundary_revealed / 1 throughline_evolution /
  16 consistent**.

## scene131_beat1 resolution: the open item is closed (2026-10-01)

Checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). The beat's full text: "Communion.
Trudy in line to receive the Eucharist. She approaches the priest and
presents her tongue to him, sensually. The priest lays the wafer on her
tongue." / "Trudy accepts the body of Christ, looking up at the priest, an
odd touch of seduction in her eyes." (4262-4268). Both layers were
corrected, each author-confirmed and logged. There were 6 entries (the
archetype, the 4 fields and the CC change), taking the log to 757, and the REGGIE scene167_beat1 entry logged in the same
session makes it 758.

**Archetype: Shadow -> ordinary_reaction.** Applying this file's own
dark-pole/Shadow distinction (the drowning-sequence isolation test above):
- **The ritual stays intact.** She is mid-communion and the ritual is
  unbroken. The unsettling quality is fused *into* the devotional act
  rather than breaking it open. That points away from Shadow.
- **No other archetype fits.** It is not Great Mother's dark pole (no one
  is being cared for; the act is solitary), not Persona (no audience is
  being managed), and Trickster was already ruled out in chunk 1.
- **Honest non-tag over a forced fit.** The value is `ordinary_reaction`,
  not `no_confident_archetype`. The material is clear and legible, so a
  confident exclusion resolves to ordinary_reaction under
  `ArchetypeTagKind`'s definition.

The Shadow-era fields were rewritten to the author's wording:

| Field | New value |
|---|---|
| self_perceived | "fully present in the ritual, nothing about this feels wrong to her" |
| audience_perceived | "devotion and sensuality fused into one unsettling act, performed in full awareness" |
| emotion | devotion, intensity, absorption |
| goal | "none stated -- this is her faith as she lives it, not a choice being made" |

goal_status stays `none`.

**characterization_consistency: boundary_revealed -> consistent.** This
corrects the final-batch verdict above.
- **The pressure test fails.** boundary_revealed needs pressure, duress or
  force meeting resistance. The schema's canonical example is "Brianna's
  capitulation to Cortes", and the `HeldValue` docstring frames it as a
  value "forced into direct conflict". This beat has no antagonist, no
  pressure and nothing being resisted. Trudy freely performs a sacrament
  she has chosen, and the sensuality is hers, uncoerced.
- **Same reasoning as JOHN scene213_beat3.** There, voluntary disclosure
  under no external conflict was resolved consistent. This is arguably the
  purer case, since there isn't even reciprocal vulnerability creating
  social pull.
- **It is a first showing.** This is the first full on-page showing of a
  facet of her faith trait that the synthesis never tracked separately:
  devotion fused with sensuality, freely given. A first showing is
  consistent.
- **The gap in the earlier review.** It correctly diagnosed the trait
  conflation (devotion vs. escalation). It did not apply the
  external-pressure test that boundary_revealed requires.

**"Sick devotion" in the record.** The reading survives, now as an
uncoerced facet of the faith trait rather than a revealed limit. It lives
in the rewritten fields and the corrections-log note.

**Consistency check: carried forward, not resolved here.** Several
boundary_revealed verdicts already confirmed in this project may not
involve external pressure, so the same test would need to be re-applied to
them. They are TRUDY scene188_beat1 ("the first private, solitary
devotional act"), JOHN scene138_beat2 (confirmed 2026-10-01 on "no
proximate trigger... no target") and JOHN scene175_beat1 (the
life-preserving offer). See `FOG_COLD_RUN_FINDINGS.md` finding 19's
session notes.

### Validation note: the downstream-reference search (2026-10-01)

**Question:** does anything later in the script, or in any analysis record,
reference, build on or explain scene131_beat1?

**Search scope:**
- every synthesis and resolution file in `fog_pass2_calls/`, for all
  characters;
- `fog_pass2_queue.json`;
- the full corrections log;
- the stored per-character fields and source text of all 460 beats in
  `fog_tagged.json`;
- every `.md` review file;
- `fog_full.txt`, for communion / eucharist / wafer / tongue / sensual /
  seduct / "body of Christ" / priest.

**Result: nothing downstream references scene131_beat1's content.**
- **The only forward link is a comparison citation.** scene188_beat1's own
  synthesis turning point and resolver cite scene131_beat1 as their
  comparison beat. The human-reviewed scene188_beat1 verdict (2026-09-29,
  above) had already set that comparison aside on independent grounds: it
  lists communion as one of six earlier *public or social* faith beats
  ("not an intensification of her public devotion"). So in the final record
  the link carries no weight.
- **The only forward-pointing claim is the model's own.** In the whole
  corpus it is scene131_beat1's own resolver rationale, which says the
  register "persists and deepens through scene188 toward the eventual
  reveal". Nothing downstream ever confirms it. It is the model asserting
  its own future relevance, unverified.
- **The later script hits are not callbacks.** They are Holly's sacraments
  (Reggie at 5553-5556; Trudy at 6453-6460), the Creed's "communion of
  saints" (6530), and Cheyenne's tongue-and-pill image in scene133_beat1
  (4281-4282). That last one is an intercut juxtaposition two scenes later.
  No record links it to scene131.

**Agreement with the author.** The author's stated intent, given in the
2026-10-01 instruction, is that this is a deliberately isolated,
non-consequential beat. The full-script and full-record search
independently agree with it.

This is the first of the author's four candidate tests to be checked
against real evidence rather than argued for in the moment. The four, as
named by the author on 2026-10-01, are pressure, facet-reveal,
decision-trigger and downstream-connection.

**Limits of this validation, recorded so it isn't over-read:**
- **One case.** It is a single beat.
- **Not blind.** The search ran after the author had already confirmed the
  verdict. It is a consistency check, not a prediction.
- **Mostly lexical.** The script search was by keyword. A purely thematic
  or visual callback with no shared vocabulary could be missed by it,
  though the record search covers the analysis side.
- **One direction only.** It validates the test's "no downstream
  connection" result, which here corresponds to consistent. It says
  nothing yet about what a positive downstream connection implies for the
  verdict.

Carried to the finding 19 / boundary_revealed-criteria session
(`FOG_COLD_RUN_FINDINGS.md` finding 19).

## Turning-points check (2026-10-05, author-checked)

Author check of `fog_turning_points_reviewed.json`, for TRUDY's flagged entries:
- **scene213_beat7: re-anchored as its own origin, no comparison
  (author-confirmed).** Limit E, the hiring/arranging capacity, is first
  shown here (line 160). The turning point is her act of confessing, not
  only the past hiring. The cold comparison scene30_beat1 (the soup
  kitchen) is dropped. Value unchanged (boundary_revealed), so no log
  entry; the re-anchor is recorded here.
- **scene216_beat7: comparison scene216_beat6 confirmed (author-confirmed).**
  It was carried from the AI draft, since review never restated one.
- **scene188_beat1: confirmed, no comparison** (a new register of her faith
  trait).
