# Full of Grace -- BETH review record

Per-character review record for BETH in the fully-cold run
(`fog_tagged.json`). Beat-level `provenance` can't show whether BETH's own
entry was reviewed (CLAUDE.md), so this file is the authoritative record of
each BETH verdict, including confirmations that change no data. Same
convention as the other `FOG_*_REVIEW.md` files.

BETH has no real-archetype tags in the cold output (every entry is
`no_confident_archetype`), so there is no archetype review section.

## Pass 2 review: BETH's queue (started 2026-10-03)

**Scope.** BETH has 7 entries in `fog_pass2_queue.json`, recounted fresh: 5
`needs_correction_review` (4 boundary_revealed, 1 throughline_evolution)
and 2 `arc_claim_check_no_draft` (scene8_beat1, scene11_beat1, both claimed
boundary_revealed). None has a finding 17 flag. Every entry is scored under
trait 1. The raw synthesis (wrapped in a ```` ```json ```` fence) matches the saved
synthesis on every type, comparison beat and trait. Her synthesis
turning point at scene4_beat1 ("Holly, you bitch!", trait 2) was drafted
consistent by the resolver and not queued. Material is printed from a fresh
`pdftotext -layout -enc UTF-8` pull, byte-identical to `fog_full.txt`.

Before this review, the only correction naming BETH was 177 (the finding 4
WP reset on scene3_beat2).

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Bossy, impatient, and dismissive toward friends' fears, hesitations, or objections | scene3_beat1 |
| 2 | Competitive; reacts to being outmaneuvered or losing with anger or insults | scene3_beat2 |

**Functional or psychological: indicators (no ruling).** BETH is 12. Her
record is the opening (scenes 3-11), the arena interview (scenes 84-85),
and one later sighting ("Holly's two friends, Beth and Krista, are aboard",
6618). Her plot-critical contribution is at the arena: "We did tell him."
(2727), the Mackie-suppression evidence recorded in finding 21.

Batches, in story order:
1. The woods, the scream and the search (scenes 7-9): scene7_beat2,
   scene8_beat1 (no draft), scene9_beat1, scene9_beat2. Context: 3_1, 3_2,
   4_1, 6_4, 7_1, and 7_3 (HOLLY only). **Done.**
2. Home that night (scene 11, EXT. RESIDENTIAL HOME, not a police station):
   scene11_beat1 (no draft), scene11_beat2. **Done.**
3. The arena interview (scene 85): scene85_beat2. **Done. Queue closed.**
   (Batches 2 and 3 were assembled and reviewed together.)

### Batch 1: the woods (2026-10-03)

Every stored turn was found word for word.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene7_beat2 | boundary_revealed (trait 1 escalation vs. 6_4) | **consistent** | log (818) |
| scene8_beat1 | no draft (`arc_claim_check_no_draft`; claimed BR continuation) | **the claim does not hold** | review notes only; no field to correct |
| scene9_beat1 | boundary_revealed (continuation vs. 8_1) | **consistent** | log (819) |
| scene9_beat2 | boundary_revealed (continuation vs. 9_1) | **consistent** | log (820) |

weight_proportionality stays `matched` on all three drafted entries (not
contested).

**scene7_beat2, consistent (author-confirmed).** Fails on independent
grounds.
- **(a) 8b.** Nothing in trait 1 (dismissing *others'* fears and
  hesitations) is tested by her own cut-off insult. Her actual content here
  is trait 2's competitive insult: "No. It means I win, moron. I got here
  first." (189-190). It isn't trait 1 at all.
- **(b) The claimed crack isn't on the page.** The synthesis's "cracks
  mid-sentence into a cut-off curse and visible worry" has no basis. Her
  text stops mid-insult ("Where r-u you dumb... little... sh-", 196). The
  scream that would explain any worry ("A SCREAM. A girl's scream.
  Holly.", 198) and the girls' reaction ("The girls spin and look into the
  woods, chilled by the terror of the sound.", 201-202) are in the NEXT
  beat, scene7_beat3, where BETH has no entry. The resolver's rationale
  admits reaching "per surrounding context" into a beat outside her own
  record. Claimed evidence must be the tracked character's own, on her own
  beat. The author cited Principle 10; its text states this requirement
  for echoes, so here it applies by extension. Nothing in this beat shows a
  crack in anything.

**scene8_beat1, the claim does not hold (author-confirmed).** "Beth running
through the woods." / "Holly?!" (206-210). The claimed continuation of a
crack can't hold once its origin (7_2) fails. Running through the woods
shouting a missing friend's name after hearing her scream is the
universal-reaction test in its cleanest form: any child would do it, and
it reveals nothing distinctive about Beth.

**scene9_beat1, consistent (author-confirmed).** "Beth runs up to her, out
of breath." (223) is her only act in the beat: arriving breathless at a
search point, the same search anyone would conduct (universal-reaction
test). The stored BR was inherited down the continuation chain from 7_2
(finding 18 shape).

**scene9_beat2, consistent (author-confirmed).** The claimed "fear
intensifies" isn't on the page at all. The text cuts away as the
hobbyhorse appears ("Holly's white Arabian hobbyhorse.", 234), with no
description of her reaction. Her only acts are "What is it?" (226) and
"Beth looks down at..." (228). There is nothing to evaluate as a turning
point.

**Principle 11: no candidate in this batch.** "Holly?!" and "What is it?"
are not declarations, and she takes no irreversible act.

**Disqualifiers across the batch (author framing, with per-beat
precision).** The author names the universal-reaction test as the dominant
disqualifier: a scream, a search, and discovering an abandoned object are
reactions anyone would have, not evidence of Beth's character. That test
decides 8_1 and 9_1 directly. 7_2 fails first on 8b and on the crack not
being on its own beat (the scream is outside her record). 9_2 fails
because no reaction is on the page to test. All four claims share one
shape: the sequence's turn is an external event (Holly's scream, 7_3) that
happens around BETH, scored as a limit of her own trait.

### Batches 2 and 3: home that night, and the arena (2026-10-03)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scenes 10-11 and
84-86 was found.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene11_beat1 | no draft (`arc_claim_check_no_draft`; claimed BR continuation) | **the claim does not hold** | review notes only; no field to correct |
| scene11_beat2 | boundary_revealed (continuation vs. 11_1) | **consistent** | log (821) |
| scene85_beat2 | throughline_evolution (trait 1 escalation vs. 3_1) | **throughline_evolution, confirmed**; factual correction | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |

weight_proportionality stays `matched` on both drafted entries (not
contested).

**scene11_beat1, the claim does not hold (author-confirmed).** "Hear the
sobs of Beth and Krista." (251). Sobbing the night a friend disappears is
a universal reaction; the deciding question is whether any two
12-year-olds would react differently. The beat also inherits the
already-disproven "crack" from the scene7_beat2 chain (finding 18
inheritance), which Batch 1 established never happened on BETH's page.
- **Setting corrected:** EXT. RESIDENTIAL HOME - NIGHT ("Bungalow. Quiet
  sub-division. Two POLICE CARS parked out front.", 246-249), not "the
  police station" as the synthesis states.
- Also recorded: the sobbing is heard, not seen, and comes after a cut to
  night (236), not "without narrative gap".

**scene11_beat2, consistent (author-confirmed).** Same basis as 11_1.
Answering a parent's questions while crying ("Dad! That's all we know!
She just... disappeared.", 254-255; "No! We were just -- (sobs) I don't
know where she is!", 266-269, voice-over) is universal distress (the
universal-reaction test decides it). It isn't a crack in a dismissiveness
trait that was never present in this sequence. The chain inherits from
7_2, already ruled consistent in Batch 1.

**scene85_beat2, throughline_evolution confirmed, with a factual
correction (author-confirmed).**
- **The escalation.** Trait 1's capacity (impatience and dismissiveness
  when pressed) genuinely generalizes here from peers to an adult
  authority figure, under the real stress of an ongoing missing-persons
  investigation: "I don't get why we gotta talk about this stuff over and
  over. Don't you cops share notes?" (2650-2652); "We said no. What else
  are we supposed to say?..." (2670-2678); "Duh! She never said who."
  (2693); "No. Body. Knows." (2708); the snarky look and "We did tell
  him." (2724-2727). The author rules this a legitimate escalation of the
  same underlying trait, not a different thing sharing adjectives.
- **Record note on scope.** This reads trait 1's object more broadly than
  its synthesis wording ("toward friends' fears, hesitations, or
  objections"). Unlike YOUNG JOHN 140_5's quietly widened trait 4
  (`FOG_YOUNGJOHN_REVIEW.md`), the widening here was raised explicitly at
  assembly and ruled on: same capacity, wider target.
- **Factual correction.** John IS a police detective ("DETECTIVE JOHN
  KIERSTEAD, 41", 305; "showing a badge and gun", 584). The assembly
  material for this batch said he wasn't one. That was wrong: the
  synthesis's "adult police detective" was literally accurate. The precise
  point is narrower: he has no jurisdiction or official standing in
  *this* investigation. Marchand: "You are not a member of this police
  force." (3773-3775); "You are an outside agent acting in a consultancy
  role" (3789-3791). Beth's "cops" is accurate, not loose. Record
  correction: the synthesis's "targets an adult police detective" becomes
  "targets an adult detective with no official standing in this
  investigation". The escalation's validity is unaffected either way.

**Principle 11: no candidate in either batch (author-confirmed).** "I
don't know where she is!" and "We did tell him." both report the past;
neither declares a fixed future.

### Trait-identity ruling for the whole queue (author-confirmed)

The scene7_beat2 -> scene11_beat2 chain was **misattributed from the
start**. Fear and searching content was scored as trait 1's "limit" or
"crack", when it was never trait 1's content: trait 1 is dismissiveness
and impatience, not their absence under fear.
- Trait 1's genuine instances are 3_1 (origin) and 6_4, both before the
  scream.
- 85_2 is the only queued beat that is trait 1, correctly scoped as a
  legitimate escalation once the detective/jurisdiction correction is
  applied.
- No separate fear/grief trait is needed: per the universal-reaction test,
  that response is not character-specific.

### BETH Pass 2: final tally (queue closed 2026-10-03)

| Beat | Draft | Final | Log |
|---|---|---|---|
| scene7_beat2 | boundary_revealed | consistent | 818 |
| scene8_beat1 | no draft (claimed BR) | claim does not hold | review notes |
| scene9_beat1 | boundary_revealed | consistent | 819 |
| scene9_beat2 | boundary_revealed | consistent | 820 |
| scene11_beat1 | no draft (claimed BR) | claim does not hold | review notes |
| scene11_beat2 | boundary_revealed | consistent | 821 |
| scene85_beat2 | throughline_evolution | throughline_evolution (confirmed, factual correction) | no-op |

**Totals.**
- The 5 drafted entries go from 4 boundary_revealed and 1
  throughline_evolution to **1 throughline_evolution, 4 consistent and 0
  boundary_revealed**.
- Both no-draft BR claims (8_1, 11_1) do not hold.
- **4 BETH Pass 2 log entries** (818-821), 1 no-op confirmation, and 2
  no-draft claims recorded in the notes.
- Corrections log total: 821. `fog_tagged.json` validates (0 errors, 460
  beats).

**Cross-queue: BR drafts overturned since REGGIE: 23 of 24.** REGGIE 3/3,
DOUG 3/3, CHEYENNE 2/2, RICARDO 1/1, O'SHEA 2/2, YOUNG JOHN 3/3, MACKIE
5/6, BETH 4/4. The one kept is MACKIE scene140_beat6, on a corrected
basis.

**Functional-plot-transfer indicator (recorded, no ruling).** BETH's most
consequential line, "We did tell him." (2727), is information that drives
John's suspicion of Mackie: "Why would he leave something like that out?"
(2773), "It's like he knew that somebody would be reading his notes..."
(2795-2796). That parallels RICARDO's pattern (`FOG_RICARDO_REVIEW.md`:
a character whose main job is handing over plot-critical information).
No ruling on whether BETH herself is functional: unlike RICARDO, she keeps
a genuine throughline_evolution (85_2), and her trait 1 has a literal
origin and instances (3_1, 6_4).
