# Full of Grace -- YOUNG JOHN archetype review record

Per-character review record for YOUNG JOHN's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether YOUNG JOHN's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each YOUNG JOHN verdict, including confirmations that
change no data. Same convention as the other `FOG_*_REVIEW.md` files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention.

Scope: YOUNG JOHN's 1 real-archetype beat (2026-09-28 enumeration: present on 12 beats, all labeled `YOUNG JOHN` after finding 13, in scenes 60, 67, 75 and 140).

## Review (2026-09-28)

Checked against a fresh `pdftotext -layout` pull, with all stored turns
found. A reverse check (the PDF text for the scene against the stored
turns, per finding 15) found no missing text in this scene.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene75_beat5 | Hero (confirmed) | First review of his own tag, not just as MACKIE's context. A real act for someone else (shielding Andy from posthumous blame: "But I was the one. Don't put it on him.") at genuine personal cost, overpowered rather than succeeding. No field changes. Provenance was already `llm_human_confirmed` from MACKIE's review (beat-level). weight_proportionality was `matched` in the Pass 1 output, one of finding 4's premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |

YOUNG JOHN's archetype review is complete. 1 real-archetype beat, with a row (recounted 2026-09-28).

**Age-consistency wording (non-archetype beats, flagged during MACKIE's review):** audience_perceived on scene140_beat8 ("a man overpowered and trapped" -> "a teenager overpowered and trapped") and scene140_beat2 ("a young man in the grip of..." -> "a teenager in the grip of...") now match how he is described elsewhere in the flashback (kid, teenager, child). Both logged; kinds unchanged.

## Pass 2 review: YOUNG JOHN's queue (started 2026-10-03)

**Scope.** YOUNG JOHN has 8 entries in `fog_pass2_queue.json`, recounted
fresh: all `needs_correction_review`, drafted 3 boundary_revealed, 4
throughline_evolution and 1 consistent. scene75_beat2 carries a finding 17
flag: the raw synthesis says "continuation" vs. the adjacent 75_1, the
validator forced "escalation", and the resolver drafted consistent. Every
other type, comparison beat and trait matches the raw synthesis. Material
is printed from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Per the author's direction, this queue
gets full depth: YOUNG JOHN's beats are half of the John/Andy throughline
(finding 21) that no automated pass could see.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Easygoing, sociable teen who enjoys camaraderie and praise from friends | scene60_beat1 |
| 2 | Calm and capable under sudden practical pressure (takes the helm, steadies the boat when threatened) | scene60_beat2 |
| 3 | Falls into shock/psychological distress when a situation exceeds his coping capacity | scene67_beat1 |
| 4 | Insists on taking personal blame/responsibility to protect Andy from consequences | scene75_beat1 |
| 5 | Suppresses his own moral stance and submits to his father's dominant control despite objecting | scene75_beat5 |

Batches, in story order:
1. In Mackie's car at the marina (scene 75): scene75_beat2 (f17),
   scene75_beat3, scene75_beat4, scene75_beat5 (context: 60_2, 60_4, 67_1,
   75_1). **Done.**
2. The funeral morning (scene 140, also "22 YEARS AGO", 4399):
   scene140_beat2, scene140_beat5, scene140_beat6, scene140_beat8.
   **Done. Queue closed.**

**Two synthesis errors found at assembly.**
- **"False confession."** The synthesis and resolver call 75_3's "I'll say
  it was me" a "false confession" / "proposing to lie to police". But
  YOUNG JOHN was at the helm: "John chugs his beer, gets up and goes and
  takes the helm." (1943); "John watches the injured jet-skier, unaware of
  the 2nd skier banking in quick toward the boat." (1995-1996); "I ran out
  of room." (2282). Mackie: "John! You fucked up. You can't undo this."
  (2353-2354). Adult JOHN later confirms it: "I was piloting Andy's boat."
  (6346). His confession is the true account. The deception is Mackie's
  cover-up, which blames the dead Andy.
- **"22 years later."** The synthesis and resolver place 140_2's panic
  attack "22 years later". Scene 140 is introduced "22 YEARS AGO..." (4399):
  it's the funeral morning, days after the accident.

**Stored-turn defect (context beat, not queued; no log).** scene75_beat1
stores MACKIE's "Those jet-skiers say it was" as dialogue and "provoked."
as a separate unattributed action turn. The raw has a blank line at 2277:
the blank-line split class in finding 20 (cf. 64_b8). The 2302-2305 dual
dialogue is hand-patched and stored correctly.

### Batch 1: in Mackie's car at the marina (2026-10-03)

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene75_beat2 | consistent (f17) | **consistent, confirmed** | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |
| scene75_beat3 | throughline_evolution (escalation vs. 75_2) | **throughline_evolution, confirmed; reasoning corrected** | no log entry (no-op convention). Provenance already `llm_human_confirmed` |
| scene75_beat4 | throughline_evolution (continuation vs. 75_3) | **consistent** | log (801) |
| scene75_beat5 | boundary_revealed (continuation vs. 75_4) | **consistent** | log (802) |

weight_proportionality stays `matched` on all four (not contested).

**scene75_beat2, consistent, confirmed (author-confirmed).** The resolver's
rejection of the forced escalation already resolved it: "Dad, I told you I
was the one--" (2314), "Andy didn't do anything, Dad." (2320), "He didn't
do anything." (2325) repeat 75_1's claims inside the same exchange. This
closes finding 17's mandatory-review item for this beat. Record note: "I
told you I was the one" refers back to a line that was cut off in 75_1
("And, Dad, I was the one who was--", 2294-2295).

**scene75_beat3, throughline_evolution, confirmed; reasoning corrected
(author-confirmed).**
- **Not a false confession.** The confession is the true account (see
  above), so the synthesis's "false confession" and the resolver's "lie to
  police" are struck.
- **The escalation.** It runs from privately arguing with his father (75_1,
  75_2) to actively offering to tell the authorities the truth himself:
  "Dad, it's okay. I'll say it was me. The jet skiers. I panicked--"
  (2349-2350), after "We don't have to do this." (2343). That's a real jump
  in commitment and stakes, even though the content is accurate rather
  than false.
- **Principle 11: no instance.** "I'll say it was me" is an offer made to
  his father, conditional on what follows, and never carried out on the
  page.

**scene75_beat4, consistent (author-confirmed).** Its own synthesis type is
continuation, not escalation. "You're not putting this on Andy." (2358)
repeats an already-made plea: the shape collapsed to consistent throughout
this project. **Sequence corrected:** the line comes *before* Mackie's
"Andy's dead." (2361), so the synthesis's "Immediately after learning Andy
is dead" and the resolver's "now under the even higher stakes of Andy's
confirmed death" reverse the order. The claimed death-triggered causation
doesn't exist.

**scene75_beat5, consistent (author-confirmed).**
- **Fifth instance of the "something happens TO the character" error.**
  The others are REGGIE scene172_beat7 and scene175_beat2, RICARDO
  scene115_beat1, and O'SHEA scene154_beat2 (`FOG_OSHEA_REVIEW.md`, Batch
  1).
- **Whose acts.** The claimed capitulation rests entirely on MACKIE's acts
  and speech: his dominance; the state-line threat ("You guys crossed state
  lines. Did you know that?", 2372-2374); the loss-of-protection ultimatum
  ("as soon as you talk, I can't protect you.", 2390-2391); "Besides, you
  got baseball coming up." (2396-2397); and "Mackie, all business, drives
  on." (2399). Young John's own acts are a repeated plea ("But I was the
  one. Don't put it on him.", 2367-2368), a look of surprise ("John's look:
  clearly he was not aware.", 2376) and "John sits stunned." (2399). None
  of these is his own capitulation.
- **Factual correction.** Mackie does not drive off "mid-plea". He speaks
  four more times after John's last line, and explicitly leaves the choice
  open: "You tell 'em whatever the hell you want." (2389-2390).
- **Trait 5's origin.** The synthesis makes this beat trait 5's first
  showing ("submits to his father's dominant control"). With the
  capitulation not depicted here, trait 5's origin claim has no own-act
  basis in this beat; the question carries to Batch 2.
- **Cross-layer note (archetype layer, not Pass 2 scope).** 75_5 carries
  Hero, confirmed 2026-09-28 on "But I was the one. Don't put it on him."
  That predates the 2026-10-02 CLAUDE.md note keeping the Hero
  declared-intent rule strict. Whether the line is an act or a
  declaration is an open archetype-layer question; not reopened here.

**Principle 11, batch-wide (author-confirmed).** No instance can be scored
within YOUNG JOHN's tagged beats. The real crossing exists structurally
but is permanently off-page by design (below). This is a different
category from RICARDO's and CHEYENNE's off-page gaps:
- **Off-page but findable** (RICARDO: the flight starts at scene107_beat1,
  which has no RICARDO entry). The crossing is on the page, and a beat
  could in principle be tagged for it.
- **Off-page by design** (YOUNG JOHN). The script itself never depicts the
  crossing, and no tagging change can recover it.

## Structural finding: the sealed moment is withheld by design (author-confirmed, 2026-10-03)

**The finding.** YOUNG JOHN's actual capitulation is never depicted on the
page: his choice to let the cover-up stand and stay silent for 22 years.
This is a deliberate authorial choice, not a gap to fill. Scene 75 cuts
directly from "Mackie, all business, drives on. John sits stunned." (2399)
to "THE PRESENT --".

**The shape: proposal, confirmation, cost, with the choice elided.**
1. **The proposal (scene 75, the car).** Mackie lays out the cover-up and
   hands John the choice: "You tell 'em whatever the hell you want. But
   remember, as soon as you talk, I can't protect you." (2389-2391).
2. **Confirmation it has already worked (scene 140, the funeral
   morning).** Mackie: "John, hey. It's over. Okay? It's all over. Look,
   all we gotta do is go to this funeral, and then everything is behind
   us. Alright?" (4453-4456). John still resists, and actively: "John
   pushes Mackie away." / "Get out." (4458-4461). Mackie: "You'll go back
   to school, then spring training. You'll feel back to normal in no time.
   Now trust me." (4464-4466). Then "Mackie moves in for a hug. Young John
   recoils." / "Fuck you!" (4468-4471).
3. **The decades-later cost (adult JOHN).** scene213_beat3, to Trudy: "I
   was piloting Andy's boat." (6346); "I killed my best friend, Tru. And I
   never had to answer for it." (6359-6360). Then scene223_beat1, to
   Andy's parents ("These are Andy's parents.", 6648): "There's something I
   have to tell you." (6661-6662).

The moment the secret was sealed, and the mechanism that sealed it, are
both permanently elided. Neither the audience nor John ever accesses
them; we see only the proposal and the cost. That mirrors how repression
works, and the author reads it as deliberate.

**Active refusal makes the unseen crossing harder-won.** At the funeral
morning, John's response is active refusal ("Get out", pushing Mackie
away, "Fuck you!"), not passive acceptance. So the eventual, unseen
capitulation is a harder-won and more significant crossing than stunned
silence alone would suggest. That strengthens the case that it is the
story's real, deliberately withheld turning point.

**Record corrections to the instruction.**
- **The funeral-morning beat is scene140_beat5, and it is in the queue.**
  The instruction described it as a scene "pre-dating scene140, not
  currently in the queue". Every quoted line is in scene140_beat5 (stored
  turns match 4453-4471), which is Batch 2 entry 140_5 (drafted
  throughline_evolution, echo vs. 75_5). Its use here as structural
  evidence doesn't resolve its Batch 2 verdict.
- **The quote is two Mackie speeches.** "it's over... you'll feel back to
  normal... trust me" joins two speeches (4453-4456 and 4464-4466), with
  John's push and "Get out." between them. Recorded in full above.
- **The sealing mechanism is the author's inference.** The author
  proposes the official story was sealed by an off-page case-file ruling
  exonerating John. No ruling, inquest or witness statement about the
  accident appears in the script (checked 2026-10-03). Recorded as a
  plausible mechanism, not depicted fact. See the MACKIE cross-character
  note in `FOG_COLD_RUN_FINDINGS.md` finding 21, which pairs it with
  Mackie's on-page suppression of Beth and Krista's El Vaquero account.
- **Finding 21's wording.** Finding 21 frames the gap as architectural:
  per-character synthesis can't see across JOHN / YOUNG JOHN. It doesn't
  literally say "no connecting beat exists". This finding adds that part of
  the connection was never on the page at all. Both hold. An addendum
  pointing here is now in finding 21.

**Connection to the adult arcs (from the JOHN review's restated
chains).**
- **Justice-independent-of-my-action:** root 75_3 (finding 21) ->
  scene185_beat2 (first on-page showing, as omission) -> scene217_beat1
  (first commission, boundary_revealed). The elided capitulation is where
  that disposition would have been formed. Its absence from the page is
  why the root can be identified only by its proposal (75_3, 75_5) and its
  later effects.
- **Reciprocal honesty:** scene213_beat3 (first showing) -> scene223_beat1
  (proactive, unilateral; Principle 11 instance). "I'll say it was me."
  (2349) and "But I was the one." (2367) at 19 are the offered confession
  that the elided moment cancelled. scene223_beat1 is the same confession,
  made at last to Andy's parents.

**Product implication.** A tool that only scores what is on the page will
always miss a turning point the author withheld on purpose. The honest
output is not a manufactured turning point on the nearest tagged beat
(which is what 75_5's boundary_revealed draft did). It is a recorded
structural gap: the proposal, the cost, and an explicit note that the
crossing between them is elided by design.

**Further confirmation (Batch 2): trait 5 has zero textual instances and
is retired.** The synthesis's trait 5 ("Suppresses his own moral stance
and submits to his father's dominant control despite objecting", origin
75_5) *is* this withheld content. Across every own-act beat from 75_1
through 140_8, YOUNG JOHN never once submits. Every instance shows
objection, refusal or involuntary breakdown:
- the 75 pleas ("Dad, it's okay. I'll say it was me.", 2349; "But I was
  the one. Don't put it on him.", 2367-2368);
- the funeral-morning refusal ("John pushes Mackie away." / "Get out." /
  "Fuck you!", 4458-4471);
- the struggle ("John struggles, but can't break free.", 4490).

The scene's last image of him, "sitting on the bed, rubbing his throat"
(4519, scene140_beat11, no YOUNG JOHN entry), doesn't show him yielding
either. The submission exists in the story only through its cost (adult
"I never had to answer for it.", 6359-6360). So trait 5 has no tagged
origin because the script never depicts it, by design. See the Batch 2
record below.

### Batch 2: the funeral morning (2026-10-03)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene140_beat1-11
was found. 140_5's text matches what the structural finding quoted. The
4436-4439 dual dialogue is hand-patched across 140_2/140_3 and stored
correctly.
- **Stored-turn defect (context, no log).** 140_11 splits "... you can take
  a cab to the" / "church." (blank line at 4515), the same blank-line
  class as 75_1.
- **Coverage.** YOUNG JOHN has no entry on 140_1, 140_3, 140_4, 140_7,
  140_9 or 140_11, though he is present in all of them. That includes the
  panic's onset ("His hands begin to tremble. His breathing goes hard.
  Panic sets in.", 4427-4428, 140_1).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene140_beat2 | boundary_revealed (trait 3 escalation vs. 67_1) | **throughline_evolution** (reasoning corrected) | log (803) |
| scene140_beat5 | throughline_evolution (trait 5 echo vs. 75_5) | **consistent** (origin of a new refusal-of-normalization capacity; attribution corrected, see below) | log (804) |
| scene140_beat6 | throughline_evolution (trait 5 echo vs. 75_5) | **consistent** (first showing of a new facet) | log (805) |
| scene140_beat8 | boundary_revealed (trait 5 continuation vs. 140_6) | **consistent** | log (806) |

weight_proportionality stays `matched` on all four (not contested).

**Trait 5 retired (record-only, author-confirmed; option (a)).** It is
different from REGGIE's trait 7 and O'SHEA's trait 1. Those had real
content, conflated with something else, so they could be folded in or
re-identified. Trait 5 has **no textual instance at all**, so there is
nothing to re-anchor. It is folded into the structural finding above as
further confirmation, not treated as a separate trait-identity
correction. `synthesis_YOUNG_JOHN.json` is untouched (it stays the cold
record); the retirement lives here.

**scene140_beat2, throughline_evolution (author-confirmed).**
- **Struck:** "22 years later" and "never resolved and has only
  intensified with time". Scene 140 is "22 YEARS AGO..." (4399), the
  funeral morning, days after the accident.
- **The escalation.** Comparing 67_1's quiet shock ("pale and in shock",
  2173) with this beat's full physical panic attack ("John claws at his
  tie, gasping for air.", 4434; "No! Oh fuck! No! No, no, no!", 4437) is a
  real intensification of trait 3, the coping-capacity limit. It is driven
  by the specific new trigger of the funeral ("all we gotta do is go to
  this funeral", 4455), not by elapsed time.
- **Stored-value correction.** The instruction treated this as a
  value-unchanged confirmation. The stored draft was `boundary_revealed`,
  so the change is logged (803). This is the third time this week an
  instruction assumed a stored value that wasn't there (CHEYENNE 155_11,
  CHEYENNE 181_1, now this).

**scene140_beat5, consistent: origin of a new, untracked capacity
(author-confirmed; trait attribution corrected 2026-10-03, after the
queue closed).** Not an echo of trait 5 (retired). It is the first showing
of a broader capacity the synthesis never tracked: **refusal to let Mackie
normalize or cover up the situation, independent of Andy specifically.**
On the page, that is physical refusal of Mackie's normalization: "It's
over. Okay? It's all over." (4453-4454) / "John pushes Mackie away." /
"Get out." (4458-4461); "Now trust me." (4466) / "Young John recoils." /
"Fuck you!" (4468-4471). A first showing, so consistent; the verdict is
unchanged.
- **Correction (trait-scope creep, 8b).** The first version of this record
  called 140_5 "a continuation of trait 4" and quietly widened trait 4
  from the synthesis's "Insists on taking personal blame/responsibility to
  protect Andy from consequences" to "refusal of the cover-up", so that
  140_5 would fit. That widening was never tested against trait 4's
  stated content, and 140_5 has no Andy content at all. This is the same
  pattern as earlier trait corrections, a definition drifting to absorb a
  beat instead of the beat being tested against the trait:
  - TRUDY trait 6, split into concealment and resentment
    (`FOG_TRUDY_REVIEW.md`);
  - REGGIE trait 7, folded into trait 8 (`FOG_REGGIE_REVIEW.md`);
  - O'SHEA trait 1's misfit, resolved by new trait 4
    (`FOG_OSHEA_REVIEW.md`).
- **Corrected record.** Trait 4 keeps its original Andy-specific content.
  Its instances are 75_1 (origin), 75_2, 75_3 (escalation, TE) and 75_4,
  each Andy-directed on the page: "His dad let him use the boat." (2303);
  "Andy didn't do anything, Dad." (2320); "I'll say it was me." (2349),
  against Mackie putting it on Andy; "You're not putting this on Andy."
  (2358). The new refusal capacity is its own trait, with origin
  scene140_beat5.
- **Corrections-log note superseded (no new entry).** Log 804's notes say
  "A continuation of trait 4's refusal of the cover-up (established
  scene75_beat1)". The value (consistent) is unchanged, so no new entry is
  made; this file is the authoritative trait record and supersedes that
  wording. The precedent is REGGIE scene134_beat2's trait re-anchor
  (record correction, no log). The log entry itself is left as written.

**scene140_beat6, consistent: first showing of a new facet
(author-confirmed).** Not trait 4 (it has nothing to do with Andy) and not
trait 5 (retired).
- **What it is.** An accusation of causation aimed at Mackie, directly
  after "You'll go back to school, then spring training." (4464-4465):
  "You think I'm ever gonna play baseball after this?!" (4481-4482).
  Something has been broken in him, and he asserts he had no choice in
  losing it. As a first showing it is consistent under the trait-identity
  gate.
- **Record precision.** "after this" is the line's own referent, and the
  page doesn't specify it further: the accident, Andy's death, the
  cover-up, or all three. Aiming it at Mackie's cover-up is the author's
  reading, supported by the line being addressed to Mackie in reply to
  his normalizing speech.
- **Principle 11: not an instance (author-confirmed).** It asserts damage
  already done *to* him by someone else, not his own unconditional
  declaration of future action. He is asserting he never had agency in
  this outcome at all, which is structurally incompatible with a
  self-authored crossing.
- **Later context on the page.** Frank Cisco, a fishing friend of
  Mackie's ("I used to fish with your dad.", 1164; "I'm Frank. Frank
  Cisco.", 1173), asks "Say, didja ever get back into playin' ball at
  all?" and John answers "No." (1187-1191). Then Frank: "Well, that's a
  damn shame, ain't it? You had some arm! Padres were scouting you heavy,
  weren't they?" (1201-1204). An earlier conversation message called the
  speaker a "coach"; that attribution was never written to any file
  (finding 21 included), so there was nothing to correct on disk.

**scene140_beat8, consistent (author-confirmed).** The claimed limit rests
entirely on Mackie's grip ("John struggles, but can't break free.
Mackie's grip hardens.", 4490). The release comes from Young Trudy's
arrival ("Mackie lets go of Young John.", 4500-4501, scene140_beat11), not
anything John does. His own act, "struggles", is resistance, not
capitulation. The stored boundary_revealed was also inherited down a
continuation chain (finding 18 shape).

### "Something happens TO the character": running count

Six instances across **four** characters. The instruction said five
characters; recounted:
1. REGGIE scene172_beat7 (being shot)
2. REGGIE scene175_beat2 ("His death happens to him")
3. RICARDO scene115_beat1 (the tackle)
4. O'SHEA scene154_beat2 (the disarming)
5. YOUNG JOHN scene75_beat5 (Mackie's override and departure)
6. YOUNG JOHN scene140_beat8 (Mackie's grip)

A seventh possible case was considered and not counted. 140_2's panic
attack is John's own body, but involuntary. It was resolved as trait 3
intensifying, not as a limit imposed by another character.

### YOUNG JOHN Pass 2: final tally (queue closed 2026-10-03)

**Trait set after review (override; synthesis JSON untouched):**

| # | Trait | Origin | Turning points |
|---|---|---|---|
| 1 | Easygoing, sociable teen | scene60_beat1 | none queued |
| 2 | Calm and capable under sudden practical pressure | scene60_beat2 | none queued |
| 3 | Shock/psychological distress past his coping capacity | scene67_beat1 | scene140_beat2 (escalation, TE) |
| 4 | Insists on taking personal blame/responsibility to protect Andy from consequences (synthesis wording, kept; Andy-specific) | scene75_beat1 | scene75_beat3 (escalation, TE); 75_2, 75_4 consistent |
| new | Refusal to let Mackie normalize/cover up the situation, independent of Andy | scene140_beat5 | none (first showing) |
| 5 | ~~Submits to his father's dominant control~~ **RETIRED**: no textual instance; withheld by design (structural finding) | -- | -- |
| new | Accusation of causation: blames Mackie for a loss he had no choice in | scene140_beat6 | none (first showing) |

| Beat | Draft | Final | Log |
|---|---|---|---|
| scene75_beat2 | consistent (f17) | consistent | no-op |
| scene75_beat3 | throughline_evolution | throughline_evolution (reasoning corrected: a true confession) | no-op |
| scene75_beat4 | throughline_evolution | consistent | 801 |
| scene75_beat5 | boundary_revealed | consistent | 802 |
| scene140_beat2 | boundary_revealed | throughline_evolution | 803 |
| scene140_beat5 | throughline_evolution | consistent | 804 |
| scene140_beat6 | throughline_evolution | consistent | 805 |
| scene140_beat8 | boundary_revealed | consistent | 806 |

**Totals.**
- The 8 drafted entries go from 3 boundary_revealed, 4
  throughline_evolution and 1 consistent to **2 throughline_evolution, 6
  consistent and 0 boundary_revealed**.
- All three boundary_revealed drafts were overturned.
- **6 YOUNG JOHN Pass 2 log entries** (801-806) and 2 no-op
  confirmations.
- Corrections log total: 806. `fog_tagged.json` validates (0 errors, 460
  beats).

**Cross-queue: "every boundary_revealed draft overturned" (scoped).**
YOUNG JOHN extends the streak: REGGIE 3/3, DOUG 3/3, CHEYENNE 2/2, RICARDO
1/1, O'SHEA 2/2, YOUNG JOHN 3/3, so **14/14 since REGGIE** (YOUNG
CHEYENNE had none). It still does not hold for JOHN (175_1) or TRUDY
(214_4), which kept BR drafts.

**Not the last queue (record correction).** The instruction called this
the last named character queue. Recounted from `fog_pass2_queue.json`
against the corrections log, 15 characters with **50 queue entries** have
no Pass 2 human review yet:
- BETH 7, HOLLY 7, MACKIE 6, ANGIE 5, CAPTAIN MARCHAND 5, RAYMOND 4,
  ALBERTO 3, FEDERAL AGENT 3, KRISTA 3, PETE 2;
- 1 each: BLACK KID, LATINO KID, DET. MCAVOY, MANAGEMENT, SARGE.

YOUNG JOHN closes the sequence the review has been following (TRUDY,
JOHN, REGGIE, DOUG, CHEYENNE, YOUNG CHEYENNE, RICARDO, O'SHEA, YOUNG
JOHN): 110 of 160 queue entries.
