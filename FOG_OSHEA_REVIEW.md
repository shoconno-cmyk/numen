# Full of Grace -- O'SHEA archetype review record

Per-character review record for O'SHEA's tags in the fully-cold run
(`fog_tagged.json`). Beat-level `provenance` can't show whether O'SHEA's
own entry was reviewed (CLAUDE.md), so this file is the authoritative
record of each O'SHEA verdict, including confirmations that change no
data. Same convention as `FOG_JOHN_REVIEW.md`, `FOG_TRUDY_REVIEW.md` and
`FOG_MACKIE_REVIEW.md`.

**Status column:** `applied` means the verdict has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention. The beat's provenance is
set to `llm_human_confirmed` unless it is already `llm_human_corrected`
(scene154_beat2, from the finding 6 merge).

Scope: O'SHEA has 13 beats under his merged identity (`FOG_COLD_RUN_FINDINGS.md`
finding 6, HISPANIC/DRIVER/O'SHEA). Enumerated fresh on 2026-09-28: 2
carry a real archetype (scene155_beat6, scene155_beat12), and scene154_beat2
is the provisional merged entry from finding 6. The other 10 carry no
real archetype tag.

## Review (2026-09-28)

Each beat was checked against a fresh `pdftotext -layout` pull, with all
stored turns found.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene154_beat2 | ordinary_reaction (confirmed, no change) | Author-confirmed: O'Shea's confrontation is genuine protectiveness toward Cheyenne against a perceived outsider threat (a cop "snooping"), not a concealed jealous motive -- rules out Persona (no gap between shown and felt). The protection is delivered through aggression/dominance, not a caregiving act (contrast scene155_beat12's genuine enacted care) -- rules out Great Mother. He holds the gun and the advantage until John disarms him, so there's no real personal risk being faced -- rules out Hero. Legible, proportionate behavior without a deeper archetypal layer. The provisional merged entry from finding 6 is confirmed as correctly non-archetypal. | applied |
| scene155_beat6 | Persona (confirmed) | "Compassionate favor" framing ("All I'm tryin' to do is help her forget for a moment about this hell she's in.") collapses into an explicit threat ("Look, I know a lot of fucked up dudes who know a lotta fucked up dudes. If you know what I'm sayin'?") -- real depicted gap between stated motive and actual leverage. | applied |
| scene155_beat12 | Great Mother (confirmed) | Author-confirmed: going around to the front and physically helping Cheyenne out of the car ("He gets out and goes around to the front and helps Cheyenne out of the car.") is a caregiving act that exceeds what John's blunt "Take her home." required -- genuine enacted care toward someone visibly distressed ("pleading, desperate"), not just tone or framing. | applied |

## Untagged beats (2026-09-28)

The other 10 beats under O'SHEA's merged identity, each checked against a
fresh `pdftotext -layout` pull. All stored turns were found. The only
difference is in scene155_beat10: the stored text has "told ‘em" with a
curly quote, where the PDF has a backtick ("told \`em"). The author
confirmed all 10 as non-archetypal. Two changed kind (scene155_beat1 and
scene155_beat11, logged). The rest are confirmed as stored. Reasons are
brief and describe what the beat's own text shows.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene151_beat1 | no_confident_archetype (confirmed) | Correctly thin setup: one line of action, "POV: unseen driver, watching things escalate in the alley." He isn't identified, and he does nothing beyond watching. Provenance was already `llm_human_corrected` from the finding 6 relabel. | applied |
| scene153_beat1 | functional_role_only (confirmed) | Correctly functional setup: he takes out his gun and gets out of the car, which starts the scene154 confrontation. Provenance was already `llm_human_corrected` from the finding 6 relabel. | applied |
| scene155_beat1 | ordinary_reaction (was no_confident_archetype) | Author-confirmed: legible, proportionate humiliation/defiance after being disarmed and locked in the car ("a bit emasculated", "John auto-locks all the doors.") -- no concealment, unaware mark or caregiving act present. Logged. | applied |
| scene155_beat3 | no_confident_archetype (confirmed) | Self-serving deflection: one cynical line ("Cuz cops don't give a fuck, that's why."), with no concealment, trickery or care depicted. | applied |
| scene155_beat7 | no_confident_archetype (confirmed) | Information delivery only ("Crickets. ... I would've heard about it by now."). | applied |
| scene155_beat8 | no_confident_archetype (confirmed; held as correctly minor) | Reviewed and held as correctly minor: a single reaction beat ("Cheyenne gives O'Shea a pleading look. O'Shea softens, sighs--"), not a sustained caregiving act like scene155_beat12's. | applied |
| scene155_beat9 | no_confident_archetype (confirmed) | Information delivery: the Mackie/Reggie shakedown account ("It was a mutha-fuckin' salt and pepper shakedown."). | applied |
| scene155_beat10 | no_confident_archetype (confirmed) | Information delivery: what was taken and the threat to "pin Holly all on me". | applied |
| scene155_beat11 | ordinary_reaction (was no_confident_archetype) | Author-confirmed: the "Serpico"/"Switzerland" line answers John's question to Cheyenne ("Why didn't you tell anyone?") on her behalf -- a retroactive justification for both of them staying quiet about Mackie and Reggie (cops don't fare well snitching on cops), not a sacrifice he's already made for her sake. Self-serving dark humor covering ordinary caution, not a depicted caregiving act -- no Great Mother. Same non-archetypal shape as scene155_beat1. Logged. | applied |
| scene181_beat1 | no_confident_archetype (confirmed; held as correctly minor) | Reviewed and held as correctly minor: one line of action at the wake ("next to a glum O'Shea in a dark suit"), a presence with no action of his own. | applied |

O'SHEA's review is complete: all 13 beats under his merged identity have a
row. 2 carry a real archetype (both confirmed), and 11 are non-archetypal.

## Pass 2 review: O'SHEA's queue (started 2026-10-03)

**Scope.** O'SHEA has 8 entries in `fog_pass2_queue.json` (stored under
the curly-apostrophe name `O’SHEA`), recounted fresh: 7
`needs_correction_review` (2 boundary_revealed, 4 throughline_evolution,
1 consistent) and 1 `arc_claim_check_no_draft` (scene155_beat8).
scene155_beat7 carries a finding 17 flag: the raw synthesis says
"continuation" vs. the adjacent 155_6, the validator forced
"escalation", and the resolver drafted consistent (finding 17's
mandatory-review list). Every other type, comparison beat and trait
matches the raw synthesis. Material is printed from a fresh `pdftotext
-layout -enc UTF-8` pull, byte-identical to `fog_full.txt`.

**YOUNG CHEYENNE** (scene60_beat4, closed the same day, log 795) is
recorded in `FOG_CHEYENNE_REVIEW.md`, alongside the CHEYENNE queue.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Uses a firearm and aggressive physical posture to confront a perceived threat to Cheyenne | scene153_beat1 |
| 2 | Displays swaggering, foul-mouthed cynicism about cops/authority | scene155_beat3 |
| 3 | Shows genuine tenderness and concern for Cheyenne beneath his tough exterior | scene155_beat6 |

Batches, in story order:
1. The alley and the disarming: scene154_beat2, scene155_beat1 (context:
   scene151_beat1, scene153_beat1, scene155_beat2/3). **Done.**
2. The car ride, the turn: scene155_beat7 (f17), scene155_beat8 (no
   draft); context scene155_beat6 (trait 3 origin, Persona). **Done.**
3. The disclosure and the gun returned: scene155_beat9, scene155_beat10,
   scene155_beat11, scene155_beat12; context scene165_beat1 (O'Shea's
   texts to John, "From O'Shea: Army cat just took more gear.", 5235, no
   O'SHEA entry) and scene185_beat2. CHEYENNE's scene155_beat11 is
   boundary_revealed (log 785), for cross-reference. **Done. Queue
   closed.** (Batches 2 and 3 were assembled and reviewed together.)

**Functional or psychological (indicators recorded at batch 1, no ruling
yet).** Toward functional: his live presence is essentially one night
(scenes 151-155); elsewhere he is silent or offscreen (an unnamed glimpse
at 3172-3174, the wake at 5670 and 5741, two texts at 5235-5239); his big
dramatic job is information delivery (the shakedown, 155_9-11). Toward
psychological: two confirmed real archetypes (Persona 155_6, Great
Mother 155_12; RICARDO had none), three distinct traits, and a later
self-initiated act as John's informant (scene165_beat1).

### Batch 1: the alley and the disarming (2026-10-03)

Every stored turn was found word for word. The stored evidence keeps the
`HISPANIC` speaker label on "Let her go, holmes." (4918-4919); finding 6
merged the entries, not the turns.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene154_beat2 | boundary_revealed (trait 1 escalation vs. scene153_beat1) | **throughline_evolution** | log (796) |
| scene155_beat1 | boundary_revealed (trait 1 continuation vs. 154_2) | **consistent** | log (797) |

weight_proportionality stays `matched` on both (not contested).

**scene154_beat2, throughline_evolution (author-confirmed).**
- **Why the boundary fails.** The claimed limit ("bravado without real
  capability against a trained opponent") rests entirely on JOHN's act:
  "In a flash, John disarms O'Shea of his weapon and has him on his knees
  about to snap his arm in half." (4943-4944). Something happening TO a
  character is not evidence of his own capacity failing.
- **What is his own, and escalates.** His own acts are a genuine
  escalation of trait 1, from 153_1's readiness ("He pops open his
  console and takes out his gun. He gets out of the car.", 4877-4879) to
  active armed aggression: "Barrel of a gun touches John's head." (4916),
  "Let her go, holmes." (4919), "O'SHEA roughs up John, shoves him up
  against the wall." (4926). Same capacity, more intense, his own doing.
  This is throughline_evolution, not a revealed limit.
- **Cross-character.** CHEYENNE and JOHN are both consistent on this beat.
  The archetype review (ordinary_reaction) already noted "he holds the gun
  and the advantage until John disarms him".

**scene155_beat1, consistent (author-confirmed).** A continuation of the
same aggressive posture, now verbal because he has been disarmed: "What
the fuck?!" (4960), "(to Cheyenne) You best tell your friend he better
watch his step." (4969-4971). It is the same capacity continuing through
whatever means remain, not a new facet. "a bit emasculated" (4953) is the
narrator's description of his state, not his action; emptying and
tossing the gun (4955-4957) is John's act. The stored boundary_revealed
was inheriting 154_2's now-corrected verdict down a continuation chain
without a retest: the finding 18 shape.

**Principle 11: no instance in this batch (author-confirmed).** "Let her
go, holmes." is a contingent demand John satisfies ("John releases
Cheyenne.", 4921), not an unconditional crossing.

**The "something happens TO the character" error: fourth instance.** The
instruction called this the third instance. Counting from the review
records, it is the fourth:
1. REGGIE scene172_beat7: being shot "is something that happens *to*
   him" (`FOG_REGGIE_REVIEW.md`; no-draft claim, does not hold).
2. REGGIE scene175_beat2: "His death happens to him" (log 775).
3. RICARDO scene115_beat1: the tackle is John's act (log 791).
4. O'SHEA scene154_beat2: the disarming is John's act (log 796).

All four are claimed boundary_revealed or claimed limits, and in every
case the drafted limit was an outcome another character imposed. The
pattern: the synthesis/resolver reads a character *losing* to someone
else as that character's capacity reaching its limit. Principle 8's test
asks what the beat teaches about what *the character* is capable of; an
outcome produced by another character's act answers a different
question.

**Carried to Batches 2 and 3 (not resolved).** Trait 1's definition
("firearm and aggressive physical posture") doesn't fit 5 of O'Shea's 8
queued beats. The confession (155_9-11) and the gun return (155_12) are
all scored under trait 1 but involve no firearm aggression, except that
155_12 involves the gun itself. These need trait re-identification
before they can be judged. Setup to keep in view for 155_12: "You can
have it back when we're finished." (4965-4966); the gun is retrieved
from the snow and handed back at 5133.

### Batches 2 and 3: the car ride, the disclosure, the gun returned (2026-10-03)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene155_beat4-12
was found. Known defect: scene155_beat9 stores JOHN's "Mackie and
Reggie?" (5070) as an unattributed action turn, an instance already
logged under finding 20.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene155_beat7 | consistent (f17: raw continuation, forced escalation, resolver rejected) | **consistent, confirmed**; reasoning tightened | no log entry (no-op convention). Provenance already `llm_human_confirmed` (archetype review) |
| scene155_beat8 | no draft (`arc_claim_check_no_draft`; claimed trait 3 continuation, likely TE) | **consistent reading; claimed turning point does not hold** | review notes only; no field to correct |
| scene155_beat9 | throughline_evolution (trait 1 escalation vs. 154_2) | **consistent; re-identified as the origin of new trait 4** | log (798) |
| scene155_beat10 | throughline_evolution (continuation vs. 155_9) | **consistent** | log (799) |
| scene155_beat11 | throughline_evolution (continuation vs. 155_10) | **consistent** | log (800) |
| scene155_beat12 | throughline_evolution (trait 1 echo vs. 155_1) | **throughline_evolution, confirmed; re-anchored to trait 3 escalation vs. 155_8** | no log entry (no-op convention). Provenance already `llm_human_confirmed` |

weight_proportionality stays `matched` throughout (not contested).

**scene155_beat7, consistent, reasoning tightened (author-confirmed).**
"Crickets. I ain't proud to say it, but if this was some kinda heinous
pedo underground shit, I would've heard about it by now." (5032-5035).
"I ain't proud to say it" grammatically attaches to what follows. What
he's ashamed of is his own proximity to that criminal world, not a
continuation of 155_6's "help her forget" tenderness. The synthesis
skipped the actual intervening content (155_6's threat-adjacent "I know a
lot of fucked up dudes who know a lotta fucked up dudes.", 5024-5026) to
manufacture a continuity that isn't there. The resolver's rejection
already reached the right verdict; this corrects only what the line
attaches to. This closes finding 17's mandatory-review item for this
beat: the outcome is confirmed.

**scene155_beat8, the claim does not hold; consistent reading
(author-confirmed).** "Cheyenne gives O'Shea a pleading look. O'Shea
softens, sighs--" (5037). The trigger is Cheyenne's act, but "softens,
sighs" is genuinely his own. It continues trait 3's established
vulnerability, and nothing new is revealed.

**scene155_beat9, consistent: origin of a new trait (author-confirmed,
8b).**
- **Not trait 1 or 3.** There is no firearm or aggression content, and it
  isn't tenderness.
- **Not trait 2.** Trait 2 is cynicism about cops, an attitude ("Cuz cops
  don't give a fuck, that's why.", 4988-4989). This is an actual account
  of having been victimized: "They came to me. Yo, I had to give it up.
  Only way I was able to stay out of the equation." (5064-5066); "Wasn't
  no transaction. It was a mutha-fuckin' salt and pepper shakedown. Every
  time. Pullin' me over. Gangbustin' my home and shit." (5073-5076).
- **New trait 4 (author-identified):** self-protective disclosure under
  vulnerability. That is, willingness to expose his own past
  victimization when sufficiently moved (the trigger is Cheyenne's look
  at 155_8), despite real danger to himself. Origin scene155_beat9. A
  first showing, so consistent.
- **Record precision on "self-protective".** The author described his
  stated motive "throughout" as self-protective ("stay out of the
  equation"). On the page, that line explains why he gave the men what
  they demanded, not why he is telling John now. No line states his
  motive for disclosing. The trait's "self-protective" element rests on
  the account's content: he presents himself as coerced, not as a
  willing dealer.
- **Names.** O'Shea never names the men: "that old Army cat" (5040), "Him
  and his cop buddy." (5054). Cheyenne does (5051, 5060).
- **Override record.** Like REGGIE's trait 8, the new trait lives in this
  file; `synthesis_O_SHEA.json` is untouched (it stays the cold record).

**scene155_beat10 and scene155_beat11, consistent (author-confirmed).**
Continuations of 155_9's disclosure. Each adds detail without new
character-revealing content:
- 155_10: what was taken ("More like what'd they rob... High-grade.
  Pharmaceutical. Government. Military.", 5082-5085) and the threat
  against him ("Said they're gonna pin Holly all on me.", 5089-5090).
- 155_11: his fear-driven silence, answered on Cheyenne's behalf ("(to
  Cheyenne) Why didn't you tell anyone?" / "I thought you were a cop.
  Didn't you see Serpico? Sucka got shot in the face, yo! And I don't
  wanna have to move to no Switzerland.", 5101-5108).

Ruling these consistent breaks the finding 18 inheritance chain that
carried trait 1's firearm-aggression label down through three beats it
never belonged to.

**scene155_beat12, throughline_evolution confirmed, re-anchored
(author-confirmed, Principle 10).**
- **The echo fails.** The prop transfer ("He opens the door, reaches into
  the snow and picks up the gun and hands it to O'Shea.", 5132-5133) is
  John's act, not O'Shea's, and the gun comes back empty (the bullets
  were pocketed, 4955-4956). The synthesis's "pockets it" and "gently
  walks Cheyenne home" are not in the text.
- **What is his own.** Sustained physical tenderness toward Cheyenne, in
  front of a witness, after a humiliating night: "O'Shea takes the gun."
  (5138) without complaint; "He gets out and goes around to the front and
  helps Cheyenne out of the car." (5138-5139); "C'mon, babe. Let's go."
  (5142). This is already confirmed Great Mother at the archetype layer
  as exceeding what "Take her home." required.
- **The escalation.** Trait 3, established as verbal gentleness and
  private vulnerability (155_6, 155_8), escalates into demonstrated
  physical care, under circumstances that could easily have produced
  resentment instead.
- **Record correction.** Comparison 155_1 -> **155_8**; trait 1 -> **trait
  3**; shape echo -> **escalation**. The value is unchanged, so there is
  no log entry.

**Principle 11: no instance across Batches 2-3 (author-confirmed).**
- Correction to the earlier framing: O'Shea never names Reggie or Mackie.
  Cheyenne does, and her naming was already ruled a disclosure, not a
  declaration (log 786, `FOG_CHEYENNE_REVIEW.md`).
- O'Shea's own disclosure (155_9-11) is an account of past events, the
  same non-declarative form.
- The self-initiated informant texts at scene165_beat1 ("From O'Shea:
  Army cat just took more gear.", 5235) are his own act, but there is no
  O'SHEA entry to score.
- With Batch 1's negative, O'SHEA has no Principle 11 instance.

**"Something happens TO the character": a case where the synthesis
avoided the error.** 155_10's "Said they're gonna pin Holly all on me."
is a threat made *to* O'Shea, which he reports. The synthesis framed it as
"deepening the same risky confession" and did not score it as his own
capacity failing. That's worth tracking: the four instances so far
(REGGIE 172_7 and 175_2, RICARDO 115_1, O'SHEA 154_2) all involved a
*physical* outcome imposed by another character. Here the imposed
outcome is a *reported verbal threat*, and the error didn't occur. One
case is not a pattern, but it's a data point on where the error does and
doesn't appear. (There is no separate pattern file; the pattern is
recorded here, under Batch 1.)

### Functional-device question: RESOLVED, NOT functional (author-confirmed, 2026-10-03)

O'SHEA is psychologically tracked, the opposite of RICARDO's finding
(`FOG_RICARDO_REVIEW.md`). The grounds:
- **Two confirmed real archetypes:** Persona at 155_6, and Great Mother at
  155_12, which exceeds its own narrative instruction ("Take her home.").
  RICARDO had none.
- **A new trait identified in this batch:** self-protective disclosure
  under vulnerability (origin 155_9).
- **He keeps acting on his own initiative after his main scene ends:**
  the informant texts at scene165_beat1 (5235-5239).

That is real interiority across several distinct facets, not a single
plot-delivery function. His information delivery (the shakedown account)
is real, but it isn't all he is on the page.

### O'SHEA Pass 2: final tally (queue closed 2026-10-03)

**Trait set after review (override; synthesis JSON untouched):**

| # | Trait | Origin | Turning points |
|---|---|---|---|
| 1 | Uses a firearm and aggressive physical posture to confront a perceived threat to Cheyenne | scene153_beat1 | scene154_beat2 (escalation, TE); 155_1 continuation, consistent |
| 2 | Swaggering, foul-mouthed cynicism about cops/authority | scene155_beat3 | none queued |
| 3 | Genuine tenderness and concern for Cheyenne beneath his tough exterior | scene155_beat6 | scene155_beat12 (escalation vs. 155_8, TE); 155_7 and 155_8 consistent |
| 4 (new) | Self-protective disclosure under vulnerability | scene155_beat9 | none; 155_10 and 155_11 consistent continuations |

| Beat | Draft | Final | Log |
|---|---|---|---|
| scene154_beat2 | boundary_revealed | throughline_evolution | 796 |
| scene155_beat1 | boundary_revealed | consistent | 797 |
| scene155_beat7 | consistent (f17) | consistent | no-op |
| scene155_beat8 | no draft (claimed TE) | claim does not hold | review notes |
| scene155_beat9 | throughline_evolution | consistent (trait 4 origin) | 798 |
| scene155_beat10 | throughline_evolution | consistent | 799 |
| scene155_beat11 | throughline_evolution | consistent | 800 |
| scene155_beat12 | throughline_evolution | throughline_evolution (re-anchored) | no-op |

**Totals.**
- The 7 drafted entries go from 2 boundary_revealed, 4
  throughline_evolution and 1 consistent to **2 throughline_evolution, 5
  consistent and 0 boundary_revealed**.
- Both boundary_revealed drafts were overturned.
- **5 O'SHEA Pass 2 log entries** (796-800), 2 no-op confirmations, and 1
  no-draft claim recorded in the notes.
- Corrections log total: 800. `fog_tagged.json` validates (0 errors, 460
  beats).

**Cross-queue: "every boundary_revealed draft overturned" (scoped).** The
count is now REGGIE 3/3, DOUG 3/3, CHEYENNE 2/2, RICARDO 1/1, O'SHEA
2/2: **11/11 across the five queues reviewed since Principle 11 was
ratified** (YOUNG CHEYENNE had no BR draft). It does **not** hold for the
earlier two queues: JOHN kept scene175_beat1's BR draft and TRUDY kept
scene214_beat4's (both confirmed with no log entry), among others. So the
pattern runs from REGGIE onward, reviewed under the full P8/8a/8b/P11
standard. Whether that reflects the drafts or the sharpened standard is
an open question.
