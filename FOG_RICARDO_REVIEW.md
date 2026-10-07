# Full of Grace -- RICARDO review record

Per-character review record for RICARDO in the fully-cold run
(`fog_tagged.json`). Beat-level `provenance` can't show whether RICARDO's
own entry was reviewed (CLAUDE.md), so this file is the authoritative
record of each RICARDO verdict, including confirmations that change no
data. Same convention as the JOHN, TRUDY, REGGIE, DOUG and CHEYENNE review
files.

RICARDO has no real-archetype tags in the cold output (every entry is
`no_confident_archetype`), so there is no archetype review section.

## Pass 2 review: RICARDO's queue (started 2026-10-03)

**Scope.** RICARDO has 9 entries in `fog_pass2_queue.json`, recounted
fresh: 7 `needs_correction_review` (6 throughline_evolution, 1
boundary_revealed) and 2 `arc_claim_check_no_draft` (scene119_beat4,
scene119_beat7). None has a finding 17 flag, and every raw synthesis type
and comparison beat matches the saved synthesis. Material is printed from
a fresh `pdftotext -layout -enc UTF-8` pull, byte-identical to
`fog_full.txt`.

Before this review, the only corrections naming RICARDO were 185 (the
finding 4 WP reset on scene115_beat1) and the Pass 2 drafts 617-628.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Freezes and reacts with visible fear when summoned by an authority figure | scene106_beat1 |
| 2 | Stalls/delays complying, quietly evading rather than confronting directly | scene106_beat2 |
| 3 | Flees physically to avoid capture when directly confronted | scene111_beat1 |
| 4 | Cooperates with basic, low-risk factual answers once caught and questioned | scene119_beat1 |
| 5 | Denies knowledge or wrongdoing to protect himself under threat | scene119_beat5 |

Batches, in story order:
1. The flight: scene111_beat1, scene114_beat1, scene115_beat1 (context,
   drafted consistent and not queued: scene106_beat1/2). **Done.**
2. The interrogation, up to the crack: scene119_beat4, scene119_beat7
   (both no-draft; 119_7 anchors the 9-11 continuation chain). **Done.**
3. The disclosure: scene119_beat9, scene119_beat10, scene119_beat11,
   scene119_beat12 (context: scene147_beat1, the recorded replay). Note
   for this batch: Doug relays the motive to John before 119_12 ("Except
   he thought you were ICE.", 3610, scene 118), which bears on Principle
   10 and on whether 119_12 is new. **Done. Queue closed.**

Batches 2 and 3 were assembled and reviewed together.

### Coverage gaps (factual, recorded at batch 1)

- **No RICARDO entry while he is still unnamed.** He is on the page as
  "the young Hispanic" before he is named: "We focus on one young Hispanic
  man, 20's, operating a lathe machine." (3335, scene104_beat1); "The
  young Hispanic takes notice of the two men, showing particular concern
  towards John." (3348-3349) and "He and John trade a look." (3357-3358,
  scene104_beat2); "the young Latino at his lathe machine" (3385,
  scene105_beat1). Same class as finding 6 (a descriptor-introduced
  character named later), but here no entry exists at all.
- **No RICARDO entry on the beats where the flight happens:**
  scene107_beat1 (the flight starts: "Suddenly, he takes an abrupt turn
  and heads briskly down a hallway.", 3446-3447), scene110_beat1 (the
  fence vault, 3481-3492), scene113_beat1 ("Ricardo leaps off and onto
  another trailer roof. The race is on.", 3532-3540).
- **Not in `characters_present`** on any of 106-115 (he has no dialogue
  there); same gap shape as finding 2.

Per the whole-character finding below, these are recorded, not chased.

### Batch 1: the flight (2026-10-03)

Every stored turn was found word for word.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene111_beat1 | throughline_evolution (trait 2 escalation vs. scene106_beat2) | **consistent** | log (789) |
| scene114_beat1 | throughline_evolution (trait 3 continuation vs. 111_1) | **consistent** | log (790) |
| scene115_beat1 | boundary_revealed (trait 3 continuation vs. 114_1) | **consistent** | log (791) |

weight_proportionality stays `matched` on all three (not contested).

**scene111_beat1, consistent (author-confirmed).** Two grounds.
- **(a) Mechanical.** The flight begins at scene107_beat1 ("Suddenly, he
  takes an abrupt turn and heads briskly down a hallway.", 3446-3447), and
  the fence vault that both the synthesis and the resolver cite ("running
  and vaulting a fence") is in scene110_beat1 (3490-3492). Neither beat has
  a RICARDO entry. 111_1's whole text is "Ricardo cuts between trailers and
  disappears from sight." (3497): a snapshot from the middle of a flight
  already in progress. It is not a genuine first showing of trait 3, and
  it can't be judged as an escalation of trait 2 (stalling, 106_2). No
  legitimate comparison beat for this capacity exists on Ricardo's own
  tagged record.
- **(b) Ricardo is a functional plot device** (whole-character finding,
  below). The honest answer to "does this reveal something new" is "no,
  and that's expected."

**scene114_beat1, consistent (author-confirmed).** A clean, explicit
continuation: "John appears at the edge and catches Ricardo making another
leap over onto one more trailer up ahead." (3546-3547). The resolver's own
language ("the same unbroken chase sequence... extending") describes no
new content; it just wasn't translated into the right verdict. With 111_1
now consistent, there is no escalation for it to continue.

**scene115_beat1, consistent (author-confirmed).** The claimed limit
(failing to evade, being physically overtaken) is not Ricardo's own act.
His acts in the beat are watching and leaping: "Ricardo watches from the
other end. They exchange a look, then Ricardo turns and leaps off onto the
ground." (3554-3555). The tackle is John's ("he pounces hard onto
Ricardo", 3559), and "Wind knocked out of him. He groans." (3562-3563) is
what happens to him.
- **Precedent:** REGGIE scene172_beat7 (`FOG_REGGIE_REVIEW.md`): being
  shot is something that happens *to* Reggie, not evidence of his own
  capacity failing.
- **Cross-character:** JOHN's side of this beat is already consistent
  ("success at an already-established risk-taking capacity",
  `FOG_JOHN_REVIEW.md`).
- Nothing about Ricardo's evasion capacity is tested or revealed; he is
  caught by someone else's successful pursuit.

**Principle 11: clean negative for the tagged beats (author-confirmed).**
No candidate within RICARDO's tagged batch 1 beats. The genuine crossing,
choosing to keep running from someone who has identified himself as
police ("Ricardo! Police! Stop right now!", 3530), starts at
scene107_beat1, which has no RICARDO entry. The real crossing likely sits
off his tagged record, consistent with other characters' untagged moments
found this week. (Principle 11's established-arc scope condition would
also have to be met: before he runs, Ricardo's arc is 104_2-106_2.)

### Whole-character finding: RICARDO is a functional plot device (author-confirmed, 2026-10-03)

**Finding.** Ricardo's chase does not carry real character weight,
whichever beats are tagged. He is written as a functional plot device: his
narrative job is to be caught, questioned, and hand over a short list of
plot-critical names. He is not written with the kind of psychological
interiority this project's trait-tracking framework is designed to
capture. The missing beats (107_1, 110_1, 113_1) are not a data gap worth
chasing: for this character, "nothing new is revealed" is very often the
expected answer, not evidence of incomplete analysis.

**Textual confirmation (checked against raw, 2026-10-03):**
- The names: "Two other men. Alberto Gomez and Raymond Olsen." (3694-3695);
  "Silver Dollar Saloon." (3718).
- The exit: once the names are out, Marchand orders, re: Ricardo, "Take
  his statement and cut him loose." (3759-3761). Ricardo never appears live
  again.
- The consequence for John: in the next scene Marchand tells him "Your job
  is done here. Understood?" (scene 120), citing among other things the
  Maine complaint about "a cop impersonating a salesman" and John's "I
  detained him. And he's an illegal." / "He ran from me."
- **Record correction to the author's statement:** the instruction said
  there is "no later scene, callback, or reference to Ricardo after this
  point." There is one: scene147_beat1 ("From his recorded interview with
  Ricardo...", 4715), which replays his recorded answers in his own voice
  (cued RICARDO, 4717-4734: the two names, Raymond's firing, the Silver
  Dollar Saloon) as John drives, and cuts straight to "EXT. SILVER DOLLAR
  SALOON" (4736). It is on his tagged record, drafted consistent and not
  queued. It *supports* the finding rather than weakening it: his only
  later presence is a recording of the name transfer, used to carry John
  to the next location.
- **Record correction 2:** the instruction described his job as to
  "implicate Mackie's father". Mackie is John's father (MACKENZIE "MACKIE"
  KIERSTEAD, 1339), and nothing Ricardo says names or implicates Mackie.
  What he implicates is Alberto Gomez and Raymond Olsen. His episode does
  feed John's removal (scene 120).

**Standing caution for the rest of RICARDO's queue.** Apply a
correspondingly lower bar for claimed escalations and boundary reveals
throughout his remaining beats, especially the scene119 interrogation,
where he is reacting under pressure rather than driving anything.

**Relation to the existing test family.** This extends, at whole-character
level, the same caution as:
- the **decency-vs-distinctiveness test** (DOUG, `FOG_DOUG_REVIEW.md`
  batch 3): baseline appropriate conduct is not a personal trait;
- the **universal-reaction test** (CHEYENNE, `FOG_CHEYENNE_REVIEW.md`
  batch 3): a reaction anyone would have tells us nothing
  character-specific.

Those two tests ask whether a single beat's behavior is distinctive. This
one asks it of the character: some characters are functional rather than
psychological, and forcing their beats into a meaningful trait arc risks
manufacturing depth the writing never intended. Product implication: a
pipeline that confidently drafts escalation and boundary verdicts on a
plot-device character is reporting structure the script doesn't have.
All three of Ricardo's batch 1 drafts claimed movement; none held.

### Batches 2 and 3: the interrogation (2026-10-03)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene118_beat1,
scene119_beat1-14 and scene147_beat1 was found word for word (cosmetic
only: 119_1 stores the subtitle note ending `subtitles**` for the raw's
`subtitles***`). The interrogation is noted as spoken in Spanish with
English subtitles (3636-3637); "Silver Dollar Saloon." is marked "(in
English)" (3717). The standing whole-character caution from Batch 1 was
applied throughout.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene119_beat4 | no draft (`arc_claim_check_no_draft`; claimed trait 1 escalation vs. 106_1, likely TE) | **the claim does not hold as scored**; distinct concrete-threat fear recorded | review notes only; no field to correct |
| scene119_beat7 | no draft (claimed trait 5 escalation vs. 119_5, likely boundary_revealed) | **the claimed boundary does not hold** | review notes only; no field to correct |
| scene119_beat9 | throughline_evolution (trait 5 continuation vs. 119_7) | **throughline_evolution, confirmed; re-anchored to trait 4** (escalation vs. 119_1) | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |
| scene119_beat10 | throughline_evolution (continuation vs. 119_9) | **consistent** | log (792) |
| scene119_beat11 | throughline_evolution (continuation vs. 119_10) | **consistent** | log (793) |
| scene119_beat12 | throughline_evolution (echo vs. 111_1) | **consistent** (reasoning corrected) | log (794) |

weight_proportionality stays `matched` on all four drafted entries (not
contested).

**scene119_beat4: the escalation claim does not hold as scored; the
nuance is recorded (author-confirmed).** The beat's whole text is
"Ricardo, confused, scared--" (3664). The synthesis claimed an escalation
of trait 1 ("visible terror", "a categorically higher personal stake").
The claim doesn't fail entirely, but its framing is wrong.
- **Two different fears.** At the factory (104_2, 106_1) his fear is
  ambient, uncertain dread: "showing particular concern towards John"
  (3348-3349), "nervous, sweating" before the summons (3429). He doesn't
  know why he's being summoned or who John is, and as an undocumented
  man his baseline fear is always "this could be ICE". Here he is
  reacting to a concrete, named threat: "That card is fraudulent. That
  makes you a fraud. Now, I'm calling ICE unless you tell me what you
  know." (3660-3662).
- **Why it isn't scoreable on his record.** That threat is spoken in
  scene119_beat3, which is JOHN's beat; Ricardo has no entry there. The
  escalating trigger sits outside Ricardo's own tagged record, so 119_4
  can't be scored as an escalation of trait 1 ("summoned by an authority
  figure") on his page.
- **What it is instead.** The honest first showing of a distinct, more
  concrete fear-response (reaction to a specific, spoken threat), not a
  continuation of trait 1. The ambient-dread vs. threat-specific
  distinction is real and worth preserving, even though it produces no
  scoreable turning point. Note also that "visible terror" is stronger
  than the text's "scared".

**scene119_beat7: the claimed boundary does not hold (author-confirmed,
8b).** "Yes." (3675) answers "Bullshit. You make hobbyhorses?" (3671). It
confirms a job fact John already knew independently: "Matter of fact, we
got one of our makers on the floor right now." (3421-3423, scene105).
Confirming an innocuous, already-known fact is not a crack in trait 5
("denies knowledge or wrongdoing to protect himself"); it is categorically
different from admitting criminal involvement. John's intensified demand
("Who makes the fucking hobbyhorses, Ricardo?! Who else?!", 3685-3686)
comes after the "Yes", Ricardo's only other line is "My team?" (3682),
and no names are given in this beat.

**scene119_beat9: throughline_evolution confirmed, re-anchored from trait
5 to trait 4 (author-confirmed, 8b).** "Two other men. Alberto Gomez and
Raymond Olsen." (3694-3695) is cooperation, trait 4's content, not trait
5's (denial).
- **The escalation.** It is the first point in the scene where Ricardo
  gives John anything John didn't already have. That runs from trait 4's
  basic, low-risk factual answers ("Six months.", 3643, trait 4's origin
  at 119_1) to substantive, consequential disclosure. The names are of
  people later shown to be dangerous: Gomez "a registered sex offender.
  Multiple rapes of minors back in Mexico City." (5730-5732); Olsen
  connected "to the kidnapping and murder of Holly" (5966-5967). The
  disclosure is made under an active ICE threat (3661-3662).
- **Record correction 1: trait 4's origin.** The instruction said trait 4
  was established at "scene119_beat1/beat5". Its origin is 119_1 only;
  119_5 ("I know nothing. I swear.", 3667) is trait 5's origin, denial.
- **Record correction 2: "volunteers".** The names were demanded, not
  volunteered unasked. They come after "Who else?!" (3686) and the
  stare-down ("John stares down Ricardo, waiting. Finally...", 3691).
  This doesn't affect the verdict: the escalation is in what he gives,
  not in whether he offered it.
- **Effect.** The verdict stands on firmer ground than its original
  basis, which anchored it as a continuation of the 119_7 "crack" that
  doesn't hold. No log entry is made, because the value is unchanged.

**scene119_beat10 and scene119_beat11: consistent (author-confirmed).**
Clean continuations of 119_9's trait-4 escalation: more detail on the
same subject, nothing new in kind. 119_10: "Raymond no longer works with
us. They fired him a month ago." (3702-3703), answering "More. Tell me
more." (3699). 119_11: "I still see him at the bar." (3711), "Silver
Dollar Saloon." (3718), "Alberto lives in Dover. ... He's a very good
friend of mine." (3733-3736). The resolvers' own language ("directly
continues", "same unbroken interrogation continues") already described
this. (119_11 also opens with a non-answer, "Why'd they fire him?" /
"Ricardo shrugs.", 3706-3708; that doesn't change the verdict.)

**scene119_beat12: consistent, reasoning corrected (author-confirmed).**
"I think ICE get him. That's why I run from you." (3744-3745).
- **What the original claim got right.** "In his own words" is accurate
  and matters under Principle 10. Doug's account in scene118_beat1 was
  secondhand ("Except he thought you were ICE.", 3610); this is Ricardo's
  own first-person admission.
- **What it got wrong.** The motive was already fully known to John and
  the audience before this beat ("Immigration. That's why he ran.",
  3617). The flight was unexplained at 111_1, but by 119_12 it had already
  been explained, so the synthesis's "the motive the story had withheld
  until now" is false. Nothing new is learned about why he ran; only the
  source and form change (secondhand report to first-person
  confirmation). This is not a genuine echo of 111_1.
- **Reading.** A continuation of the trait-4 cooperation thread (119_9-11):
  Ricardo voluntarily owning something already on record. It is
  consistent not because nothing of note happens, but because the content
  isn't new, even though the voice delivering it is.

**Principle 11: no instance (author-confirmed).** The one candidate,
naming Alberto Gomez and Raymond Olsen at 119_9 (his own speech act, and
one that can't be unsaid), is excluded by the principle's own scope
condition: "an anonymous or minimally-established character's
irreversible act does not qualify". That is what the Batch 1
functional-device finding established about RICARDO. This is not a
borderline case; it is the scenario the exclusion exists for. With Batch
1's negative, RICARDO has no Principle 11 instance on his tagged record.

### RICARDO Pass 2: final tally (queue closed 2026-10-03)

| Beat | Draft | Final | Log |
|---|---|---|---|
| scene111_beat1 | throughline_evolution | consistent | 789 |
| scene114_beat1 | throughline_evolution | consistent | 790 |
| scene115_beat1 | boundary_revealed | consistent | 791 |
| scene119_beat4 | no draft (claimed TE) | claim does not hold as scored (distinct concrete-threat fear noted) | review notes |
| scene119_beat7 | no draft (claimed BR) | claim does not hold | review notes |
| scene119_beat9 | throughline_evolution | **throughline_evolution** (re-anchored trait 5 -> trait 4) | no-op confirmation |
| scene119_beat10 | throughline_evolution | consistent | 792 |
| scene119_beat11 | throughline_evolution | consistent | 793 |
| scene119_beat12 | throughline_evolution | consistent | 794 |

**Totals.**
- The 7 drafted entries go from 6 throughline_evolution and 1
  boundary_revealed to **1 throughline_evolution, 6 consistent and 0
  boundary_revealed**. The boundary_revealed draft was overturned.
- Both no-draft arc claims (119_4 TE, 119_7 BR) do not hold.
- **6 RICARDO Pass 2 log entries** (789-794), 1 no-op confirmation, and 2
  no-draft claims recorded in the notes.
- Corrections log total: 794. `fog_tagged.json` validates (0 errors, 460
  beats).

**Did the functional-device finding hold?** Yes, with one exception that
fits it rather than contradicting it. 8 of the 9 claimed turning points
fail. scene119_beat9 survives as a genuine escalation, but only after
re-anchoring, and its content is exactly the device's job: handing over
the names. The one real movement on Ricardo's record is the plot transfer
itself.

**Cross-queue comparison (record correction).** The instruction framed
this as "every claimed turning point fails, matching REGGIE/DOUG/
CHEYENNE's pattern". That isn't the prior pattern:
- DOUG kept 5 throughline_evolution drafts (`FOG_DOUG_REVIEW.md` totals).
- CHEYENNE kept 2, and gained a boundary_revealed.
- REGGIE overturned all 11 TE drafts but ended with 3 boundary_revealed
  re-scored from them.

What does hold across all four queues is narrower: **every
boundary_revealed draft has been overturned**. REGGIE 3/3, DOUG 3/3,
CHEYENNE 2/2, RICARDO 1/1, plus RICARDO's no-draft boundary claim at
119_7. Every final boundary_revealed verdict across those queues came
from a throughline_evolution draft.
