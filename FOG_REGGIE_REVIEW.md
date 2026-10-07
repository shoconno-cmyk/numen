# Full of Grace -- REGGIE archetype review record

Per-character review record for REGGIE's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether REGGIE's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each REGGIE verdict, including confirmations that
change no data. Same convention as the JOHN, TRUDY, MACKIE and O'SHEA
review files.

**Status column:** `pending apply` means the verdict is decided here but
the tagged data file has not been changed yet. `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention, and the beat's
provenance is set to `llm_human_confirmed`.

Scope: REGGIE's 5 real-archetype beats in the cold output (2026-09-28
enumeration: REGGIE present on 29 beats, 5 with a non-empty archetypes
list). Every tag was model output that nobody had reviewed. No
corrections-log entry named REGGIE before this review. scene172_beat2's
earlier `llm_human_corrected` came from JOHN's corrections.

## Review (2026-09-28)

Each beat was checked against a fresh `pdftotext -layout` pull, with all
stored turns found.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene54_beat1 | ordinary_reaction, Chorus removed; fields rewritten | Author-confirmed: a polite, warm remark at a funeral reception ("A fine thing you've done. Coming back." / "Let me be the one to say that your father would've appreciated this. I know Trudy does."), not informing John of anything new and not generalizing beyond this one moment -- no Chorus lift. self_perceived, audience_perceived, goal (-> goalless), goal_status (deferred -> none) and emotion rewritten. | applied |
| scene54_beat2 | Great Mother (confirmed) | Author-confirmed, no changes. | applied |
| scene94_beat3 | Trickster (confirmed) | Author-confirmed, no changes. | applied |
| scene172_beat1 | ordinary_reaction, Shadow removed; fields rewritten | Author-confirmed: Reggie has always been a controlled, deranged person who intelligently contained it -- here he stops hiding it, but he remains fully composed and deliberate throughout (negotiating, offering John a genuine out), never losing control. A willful unmasking, not a break -- the same shape as JOHN's scene119_beat2 correction (fails Shadow's despite-control test). self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays achieved. The removed audience_perceived carried the invented "professional ... facade" framing (finding 14). | applied |
| scene172_beat2 | ordinary_reaction, Shadow removed; fields rewritten | Same basis: "I'm givin' you a chance here, Johnny. ... Drop the fucking gun, go on back to L.A., and let me handle this." self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays deferred. The removed audience_perceived called him "a cop" with a "professional front" (finding 14). | applied |

REGGIE's archetype review is complete. Every REGGIE beat that had a real
archetype at the enumeration has a row (5). After the review, 2 still
carry one (scene54_beat2 Great Mother, scene94_beat3 Trickster), recounted
2026-09-28.

## Pass 2 review: REGGIE's queue (started 2026-10-01)

**Scope.** REGGIE has 16 entries in `fog_pass2_queue.json`, recounted from
the file: 15 `needs_correction_review` and 1 `arc_claim_check_no_draft`
(scene172_beat7, which has no causal_integrity block). scene94_beat3 is a
finding 17 entry. All of the material was printed against a fresh
`pdftotext -layout -enc UTF-8` pull (byte-identical to `fog_full.txt`), and
every stored turn was found verbatim. The two entries below were resolved
ahead of the batches. The remaining 14 are in five batches, in story order (2026-10-02):

1. Holly Roberts questioning: scene94_beat3, scene95_beat1. **Done.**
2. Hidden cellar ritual: scene132_beat1, scene134_beat2, scene136_beat1. **Done.**
3. Approach and arming: scene168_beat1, scene172_beat1. **Done.**
4. Standoff: scene172_beat2, beat3, beat4, beat5. **Done.**
5. Shot and dying confession: scene172_beat7 (no draft), scene175_beat1, scene175_beat2. **Done. Queue closed.**

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene167_beat1 | throughline_evolution | **consistent** | log (758). See below |
| scene172_beat6 | throughline_evolution | **boundary_revealed** (vs. traits 1+5 jointly; record corrected 2026-10-01, value unchanged) | log (759). **Finding 19 instance 4**; see below and "Record correction" at the end |

**scene167_beat1, consistent (author-confirmed).** The comparison beat is
corrected, and the verdict changes with it. The synthesis compared this
beat with scene54_beat5, but that beat's own resolver checked it against a
different trait: trait 2, "Tightly wound/guarded beneath a composed
exterior". Reggie's line there is said to Trudy about the idling Honda John
was watching: "Hundred bucks says she never gets out of her car." (1624).
Trait 5's actual origin is scene95_beat1: "Oh, but it does. This is my
town." (3074).

Against that origin, scene167_beat1 shows no trait-5 behavior: "Reggie
drives down the private cabin road... snorts it. He comes around a bend,
sees John's car parked just up ahead. He pulls in behind and idles. He
eyes John's car. He shuts his truck off." (5282-5289). He asserts no
authority, enforces nothing and confronts no one.
- The resolver's "actively track down John's car" is not on the page: he
  comes upon it.
- The drug use is not new: the needle and pills were already shown at
  scene134_beat2.
- The first escalation of trait 5 beyond scene95_beat1 is scene172_beat1
  (gunpoint), which the synthesis itself already compares with
  scene95_beat1.

**Knock-on, for the batch review:** scene168_beat1 is drafted as a
"continuation of scene167_beat1", so it now has no anchor. Its arming
("grabs his hunting rifle off the rack", 5296-5297) may be the real first
step, comparable to JOHN scene163_beat1.

**scene172_beat6, boundary_revealed vs. trait 1 (author-confirmed,
2026-10-01).** Material is from a fresh `pdftotext -layout` pull, and every
quote below was rechecked against `fog_full.txt` on 2026-10-01.

- **Trait scored.** The beat is scored against trait 1, "Performs warm,
  seemingly genuine camaraderie and loyalty toward Mackie's family", first
  shown at scene53_beat1: "Mackie's favorite. Your's too, from what I
  remember?" (1478-1480). Trait 8 ("willing to use lethal force") alone
  would be `throughline_evolution`: the threat escalating into the act, as
  with JOHN's own scene172_beat6. That escalation is the **mechanism**, not
  the verdict.
- **The limit exposed.** The loyalty collides with Reggie's promise to
  Mackie and loses, against Mackie's own son:
  - "I made him a promise: that I'd finish what we started." (5462-5463)
  - "I ain't breakin' my promise!... you've made your choice, Detective."
    (5480-5482)
  - "Reggie takes aim at John's head." (5484)
  - "Reggie pulls the trigger." (5490)

  scene172_beat1-5 hold the conflict open: "I'm givin' you a chance here,
  Johnny." (5425). Beat 6 shows where the limit is. Mackie and Reggie were
  best friends ("hunting photos and wartime photos. Best buds, smiling.",
  4289; "Your father was my buddy. My man!", 5456).
- **Pressure test passes.** External pressure from John meets resistance
  in Reggie's own lines:
  - Pressure: "He begins to slowly raise his rifle." (5435); "rifle fully
    levelled at Reggie" (5441); "Or I'll be forced to defend myself."
    (5452-5453).
  - Resistance: 5425, 5432-5433; "You're forcing my hand here, John!"
    (5448).

  This is the distinction from TRUDY scene131_beat1 and JOHN
  scene213_beat3, neither of which has an opposing party.
- **Caveat 1: Reggie created the standoff he is under.** He armed himself
  at scene168_beat1 and put John at gunpoint first at scene172_beat1 ("You're
  way outta your jurisdiction, John.", 5383). The test asks whether pressure
  meets resistance, not who started it. JOHN's scene172_beat6 likewise sat
  inside a pursuit he chose.
- **Caveat 2: the resistance is shown only in Reggie's own dialogue.** The
  evidence is his repeated offers of a way out. No narration shows
  hesitation, and "forcing my hand" is also self-justification. The
  author's "resisting his own hesitation" is an inference from those
  offers, not narrated text.
- **Record correction (resolver metadata, no field, no log entry; the cold
  record is kept):** checked_against "Willing to use lethal force...
  (continuation vs scene172_beat1/5)" -> trait 1, vs. scene53_beat1, with
  trait 8's escalation as the mechanism. weight_proportionality stays
  `matched`.

**Finding 19, instance 4 (confirmed).** This is REGGIE's point of no
return: attempted murder of a detective, by actually firing rather than
threatening. It falls in the same beat as JOHN's instance 2, from the
opposite side of the same exchange. JOHN's crossing is his return shot
(5494); REGGIE's is pulling the trigger (5490). With TRUDY (scene214_beat4),
this is the third character, so finding 19's own "two more characters"
threshold is met. See `FOG_COLD_RUN_FINDINGS.md` finding 19.

### Record correction: scene172_beat6 is scored against traits 1 and 5 jointly (2026-10-01, author-confirmed)

**Value unchanged: `boundary_revealed`.** There is no new corrections-log
entry, because the value doesn't change. Log 759's note ("Scored against
trait 1... not trait 8") stays as the cold record of the earlier reasoning,
and this section supersedes its trait basis. weight_proportionality stays
`matched`.

**What changes.** The record scored this beat against trait 1 alone, as
loyalty *failing*: colliding with the promise and losing. The author's
reading is that Reggie isn't experiencing loyalty failing here. He is
enacting loyalty in its most extreme, violent form. He cites two
justifications in one speech, and the author calls them "both loyalty
threads belong to the same sweater", one combined complex rather than two
competing claims:
- **Trait 1, loyalty to Mackie and finishing what they started:** "I made
  him a promise: that I'd finish what we started." (5462-5463)
- **Trait 5, self-appointed protector of "his town":** "This is our town."
  (5463-5464)

**The combined reveal.** Loyalty and town-protection show they have no
limit, not even for Mackie's own son, the one person they should most
protect: "I ain't breakin' my promise!... you've made your choice,
Detective." (5480-5482); "Reggie takes aim at John's head." (5484);
"Reggie pulls the trigger." (5490). On trait 8 alone (lethal force),
brandishing to firing would still be `throughline_evolution`. The verdict
rests on the relational complex, where the change is in type (finding 19,
"Resolution", axis 2).

**Quote check (fresh `pdftotext -layout -enc UTF-8` pull).** The
instruction quoted "This is my town. This was Mackie's town... This is our
town." as said "in the same breath before firing". That is a splice of two
scenes:
- "Oh, but it does. This is my town. This was Mackie's town. It's still
  your town, too, John." is from **scene95_beat1** (3074-3076). That is
  trait 5's own first-shown beat, in the kitchen, long before scene172.
- Only "This is our town." (5463-5464) is in the scene172 speech, and it is
  stored in **scene172_beat5**, together with "I made him a promise..."
  (5462-5463).

Both justifications therefore come in the speech immediately before the
beat 6 trigger pull, not inside beat 6 itself. This doesn't change the
reading. The beat 5 speech is the stated motive, and beat 6 is the act.

**Record correction (resolver metadata, no field, no log entry):** the
checked_against for this beat, set 2026-10-01 as "trait 1, vs.
scene53_beat1", becomes **traits 1+5 jointly**. The anchors are
scene53_beat1 (trait 1) and scene95_beat1 (trait 5), with trait 8's
escalation as the mechanism.

### Batch 1: Holly Roberts questioning (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene94-95 was
found word for word, and every raw line from 2955 to 3113 is covered by the
stored turns. The one defect is the speaker attribution at 3003; see the
end of this section.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene94_beat3 | consistent (finding 17 entry) | **consistent, confirmed** | no log entry (no-op convention). Provenance was already `llm_human_confirmed` from the Trickster confirmation |
| scene95_beat1 | boundary_revealed | **consistent** | log (764) |

**scene94_beat3, consistent (author-confirmed).** This is one of finding 17's
mandatory-review entries. The raw synthesis said `continuation`
(`synthesis_raw_REGGIE.json`), and the validator relabeled it `escalation`.
The resolver rejected the escalation independently: "the trait's first full
verbal expression, not evolution." The comparison beat is the one right
before it in the same scene (scene94_beat2), so the finding 17 fix would
have dropped the entry. Confirmed as stored.

**scene95_beat1, boundary_revealed -> consistent (author-confirmed, Principle
8b + axis 1).**
- **Not the same capacity as trait 6.** Trait 6 is evasion when Reggie is
  questioned about his *own* involvement: "Reggie? Where were you the day
  Holly Roberts disappeared?" (3008-3009), "Pardon?" (3015), then
  deflection onto Cheyenne's associate (3043-3053). John's question here
  is about a third party's confidence: "My father ever speak privately to
  you about the Holly Roberts case?" (3097-3098). "Matter of fact he did."
  (3103) is a direct admission that costs Reggie nothing. It is not his
  evasion cracking.
- **A first showing.** The beat is the low-stakes first showing of a trait
  the synthesis never tracked: the private Mackie/Reggie connection on the
  Holly case. A standalone trait's ordinary first showing is `consistent`
  (axis 1). The beat has no stakes, no witnesses and nothing climactic, so
  8a's exception does not apply.
- **Planted origin (author-confirmed connection).** This beat is the origin
  of the promise Reggie invokes at scene172_beat5: "Your father was my
  buddy. My man! In his last moments, we were together... me and him... in
  the goddamn fucking ambulance!" (5456-5459), then "I made him a promise:
  that I'd finish what we started." (5462-5463). That loyalty-to-Mackie
  thread is what scene172_beat6 scores jointly with trait 5 (see the
  scene172_beat6 record correction above). That record's trait-1 anchor
  is still scene53_beat1, and its value is unchanged. The page never says
  what "what we started" was. Linking it to the Holly case is the
  author's reading of 3097-3103 together with 5462-5463.
- **Quote and fact checks on the instruction.**
  - "Whaddya gonna do about it?" was given as Reggie's tone. It is not in
    the script. The page has only "Reggie gives pause, visibly annoyed."
    (3100). The challenging delivery is recorded as the author's reading.
  - The instruction called the deflection target a "fabricated suspect".
    He is a real person: the Chrysler 300 driver is O'SHEA (3160, 4045,
    4877, 5741). The deflection is real; the person is not invented.

  Neither point changes the verdict.

**Secondary note for later batches (does not change the verdict).** The
author reads Reggie's blunt, challenging delivery as a sign that his
defensiveness toward John is *hardening* at this point in the story, not
weakening. Keep that in view for the consistency checks on his later beats
(Batches 3-5). The textual basis is 3100 and 3103 alone.

**Text-integrity defect (logged as finding 7, seventh occurrence).**
"You had tremendous talent." (3003) is the second paragraph of REGGIE's
`(O.S.) (CONT'D)` speech that begins at 3000-3001. It is stored as
scene94_beat2 turn 12, an `action` turn with `speaker: null`, and the beat
boundary between scene94_beat1 and scene94_beat2 falls mid-speech. The
wording is intact, and no verdict depends on it.

### Batch 2: hidden cellar ritual (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene132-136 was
found word for word, and every raw line from 4270 to 4328 is covered by the
stored turns. Reggie has no dialogue in the sequence, which is intercut
with two CHEYENNE cutaways (scene133, scene135). No text-integrity defects.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene132_beat1 | throughline_evolution (escalation of trait 4 vs. scene54_beat1) | **consistent** | log (765) |
| scene134_beat2 | throughline_evolution (escalation of trait 7 vs. scene132_beat1) | **boundary_revealed**, re-anchored as trait 8's origin (trait 7 was later retired into trait 8, line 585) | log (766) |
| scene136_beat1 | throughline_evolution (continuation vs. scene134_beat2) | **consistent** | log (767) |

**scene132_beat1, consistent (author-confirmed).**
- **Not trait 4.** The anchor is drinking with John, socially: "Both men
  are drinking the Tullamore and smoking cigarettes." (1498-1500,
  scene54_beat1). This beat is "Reggie descends the stairs, shirtless,
  clutching a bottle of scotch. He takes a swig. Not his first of the
  night." (4273-4274). The "socialize" half of trait 4 is absent.
- **The author's reading.** Reggie is getting amped and numb before going
  back to the man behind the door. The beat is preparatory, not
  independently significant to his arc, and it is neither an escalation
  nor a first showing.
- **That purpose is inferred, not shown.** Scenes 132-136 never show who is
  behind the door. The support comes from elsewhere: Ricardo on Alberto,
  "He hasn't been to work in a week." (3742, before this sequence); John
  finds the furnace room off this cellar "Padlocked." (5270); and "John
  pulls the bag off, revealing ALBERTO GOMEZ, blood-soaked" (5349).
- **Axis 3 data point.** This is the second data point, after TRUDY
  scene131_beat1, for the narrative-consequence (axis 3) question still
  open from the principle session. It is a beat that read as potentially
  meaningful in the draft and was downgraded once the author confirmed it
  carries no real weight in the arc. Like scene131_beat1, this was not
  blind: the author's confirmation came first.

**scene134_beat2, boundary_revealed, re-anchored as trait 7's origin
(author-confirmed, Principle 8b + 8a).**
- **8b, not the same content as the anchor.** The synthesis scored the
  beat as an escalation of trait 7 vs. scene132_beat1. That beat shows only
  "A handyman's man-cave." (4272) and drinking, with no ritual, drug or
  weapon content.
- **First appearance of everything here.**
  - "On the cushion sits the bottle of scotch and a large hunting knife."
    (4292-4293)
  - "a disposable needle and a vial of clear liquid" (4295-4296)
  - "He unwraps the needle, sticks its tip into the vial and fills the
    chamber" (4299-4300)
  - "He carefully sets the needle and pill bottle onto the cushion of the
    basket alongside the knife and the scotch." (4302-4303)

  A search for snort, cocaine, coke, pill, vial, knife, needle and
  syringe found no earlier Reggie drug or knife reference. His cocaine
  next appears at 5283-5284 (scene167). This is trait 7's birth, not an
  escalation of it.
- **8a.** This is the first evidence of premeditated violence and antisocial
  behavior beneath Reggie's warm public persona. Nothing in his pattern
  up to this point (loyal friend, protective camaraderie toward Mackie's
  family) makes it foreseeable. So the first showing is
  `boundary_revealed`, not the axis-1 default of `consistent`.
- **Caveat on the 8a fit (for the record, not a reversal).**
  - 8a names a *singular climactic action*: personal violence, legal
    obstruction or an irreversible declaration. The on-page act here is
    *preparation*. The violent purpose rests on later text (3742, 5270,
    5349), which Pass 2's whole-arc view allows.
  - The beat is mid-script, not climactic by position.
  - The author's reading extends 8a to premeditation. If 8a's wording is
    revisited, this is the test case. It is preserved as open item 2 at the
    end of finding 19 in `FOG_COLD_RUN_FINDINGS.md` (2026-10-02).
- **Quote check on the instruction.** It described Reggie's established
  pattern as "local cop". He is not a cop (finding 14): he is introduced
  "in a U.S. Marines uniform" (1409). This doesn't affect the verdict.

**scene136_beat1, consistent (author-confirmed).**
- **No new capacity.** The beat is the immediate continuation of the
  ritual begun at the re-anchored scene134_beat2: "He climbs into the suit.
  Slips the hideous headpiece on." (4320); "He steps into the darkness,
  shuts the door behind him" (4325).
- **The plaque is a note only.** "This Is Our Town" (4328) is a thematic
  echo, a mantra or mission statement, of the town-loyalty language: "This
  is my town. This was Mackie's town." (3074-3075, scene95_beat1) and "This
  is our town." (5463-5464, scene172_beat5). But it is ambient set
  dressing, not Reggie's own shown justification in this beat, so the beat
  is **not** scored against trait 5 as well as trait 7.

**Record correction: trait 7's first-shown beat (synthesis metadata, no
field, no log entry).** `fog_pass2_calls/synthesis_REGGIE.json` gives
trait 7 ("Maintains a hidden, secretive private space/behavior apart from
his sociable public persona") `first_shown_beat_id: scene132_beat1`. The
correct origin is **scene134_beat2**. The synthesis file is not edited:
the saved synthesis files stay the cold record (finding 17 convention), and
this section supersedes that field. Two downstream effects:
- scene136_beat1's continuation anchor (scene134_beat2) is unchanged.
- scene132_beat1 now carries no trait-7 role.

### Batch 3: approach, arming, first gunpoint (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene167-172_1 was
found word for word, every speaker matches its raw cue, and a reverse
check of raw lines 5280-5410 against the stored turns found nothing
missing. No text-integrity defects.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene168_beat1 | throughline_evolution (continuation vs. scene167_beat1, stale) | **consistent**, re-anchored to scene134_beat2 | log (768) |
| scene172_beat1 | throughline_evolution (trait 5, escalation vs. scene95_beat1) | **boundary_revealed**, re-scored to the premeditated-violence capacity (trait 8) | log (769) |

**scene168_beat1, consistent (author-confirmed).**
- **The anchor.** scene167_beat1 is `consistent` (log 758), so the drafted
  continuation had nothing to continue. The beat is re-anchored to
  scene134_beat2.
- **What the page shows.** "Reggie approaches, peeks in John's front seat.
  Sees the box of ammunition. He glances down the road to the cabin."
  (5293-5294); "He walks back to his truck, opens his door, and grabs his
  hunting rifle off the rack." (5296-5297).
- **The author's reading: targeted preparation against a recognized
  threat, not generic caution.**
  - He recognizes John's car: "sees John's car parked just up ahead"
    (5286).
  - He infers from the ammunition that John is armed.
  - He almost certainly connects this to John closing in on Holly and
    Alberto.

  The last two are inferences; the beat has no dialogue.
- **No new capacity.** This is the premeditated-violence disposition
  established at scene134_beat2, redirected from the captive to John.
  Preparatory arming in service of an established capacity is not a fresh
  crossing. It plays the same role as TRUDY scene214_beat1, which is
  `consistent` (log: "'I panicked' elaborates why the confessed act
  happened, not a new capacity").

**scene172_beat1, boundary_revealed (author-confirmed, Principle 8b +
axis 2).**
- **8b, a different capacity from the anchor.** scene95_beat1's "Oh, but it
  does. This is my town. This was Mackie's town." (3074-3075) is a mild
  verbal claim of standing, said to John's "Doesn't really concern you,
  Reggie." (3071). It comes with no enforcement and doesn't anticipate
  armed obstruction of a detective.
- **What this beat shows.**
  - John "quickly digs out his cell phone, goes to dial 911." (5376-5377)
  - "From behind comes the sound of a Remington pump-action rifle."
    (5379)
  - "Your phone." (5390); "Reggie picks it up and pockets it." (5392)
  - Three commands to drop the gun (5398, 5404, 5410).
- **The type-change.** This is the premeditated-violence capacity's first
  direct, confrontational use against a person: physically stopping a
  detective from summoning help for the captive whose torture he is
  investigating. Preparing to harm a helpless captive becomes violently
  obstructing an investigator. That is a change in type (axis 2), not
  scale.
- **Trait 5 is rhetorical cover, not the engine.** The trait-5 escalation
  framing is replaced entirely.
  - "You're way outta your jurisdiction, John." (5383-5384) invokes an
    office Reggie doesn't hold (finding 14, "in a U.S. Marines uniform",
    1409). It is said on John's own property ("This is my property.",
    5451).
- **Fact checks on the instruction.**
  - It said "jurisdiction" was Reggie *borrowing* Doug's line from
    "scene123". The line is "You're already way out of your
    jurisdiction." (3270-3271), and it is in **scene101_beat1**, a phone
    call between Doug and John. Reggie isn't present, so this is recorded
    as a verbal echo, not a borrowing.
  - The underlying point stands: the word claims a legitimacy he doesn't
    have.

**The corrected chain (premeditated-violence capacity):**

| Beat | Role | Value |
|---|---|---|
| scene134_beat2 | origin: needle, knife, ritual basket | boundary_revealed (log 766, 8a) |
| scene168_beat1 | same capacity, redirected at a recognized threat | consistent (log 768) |
| scene172_beat1 | first direct confrontational use, obstructing the 911 call | boundary_revealed (log 769) |
| scene172_beat6 | lethal culmination, the **mechanism**; the verdict is scored on traits 1+5 jointly | boundary_revealed (log 759 + record correction) |

**Record correction: trait 8's label and origin (synthesis metadata, no
field, no log entry).** The synthesis's trait 8 is "Willing to use lethal
force to enforce his own sense of justice", with `first_shown_beat_id:
scene172_beat1`. Per the author, the capacity the chain tracks is
premeditated violence, labeled trait 8, and its origin is
**scene134_beat2**. Two things to keep straight:
- Batch 2 recorded scene134_beat2 as trait **7**'s origin (log 766, hidden
  private behavior). That beat is therefore now the origin of both traits
  7 and 8. Log 766's own 8a reasoning was already about the violence
  capacity ("first evidence of premeditated violence").
- **Open:** are traits 7 and 8 one capacity or two? Not resolved here.

The synthesis file is not edited (it is the cold record).

**scene172_beat6's citation: it holds, no change.** Its verdict rests on
traits 1+5 jointly, anchored at scene53_beat1 and scene95_beat1, with
trait 8's escalation as the **mechanism** (record correction, 2026-10-01).
It never cited trait 8's first-shown beat, so moving that origin to
scene134_beat2 doesn't touch it. One wording point, flagged and not
changed:
- **The record's trait-8 statement.** The record says that "on trait 8
  alone, brandishing -> firing would be `throughline_evolution`". With
  scene172_beat1 now the confrontational step, that statement still holds
  for the chain: 172_1 -> 172_6 is gunpoint -> firing. So scene172_beat6
  is **not** "trait 8, boundary_revealed" in its own right. The chain row
  above is worded accordingly.
- **A tension with JOHN.** JOHN's scene172_beat6, "armed and prepared ->
  discharging lethal force at a person", was scored `boundary_revealed`
  as a type-change (finding 19 resolution table, log 762). REGGIE's record
  calls the same transition quantitative on trait 8. Both verdicts are
  `boundary_revealed` on their stated bases, so nothing changes. If the
  two-axis test is revisited, though, the same act reads as a type-change
  for one character and a scale change for the other.

### Record correction: scene134_beat2 is trait 8's origin, not trait 7's (2026-10-02, author-confirmed)

**Value unchanged: `boundary_revealed`.** There is no new log entry,
because the value doesn't change.

- **What this supersedes.** It replaces Batch 2's record correction ("the
  correct origin is scene134_beat2" for trait 7) and Batch 3's "now the
  origin of both traits 7 and 8". Log 766's note, which says "Re-anchored
  as trait 7's origin", stays as the cold record. This section supersedes
  its trait label.
- **Why.** Batch 2's verdict reasoning for scene134_beat2 ("the first
  evidence of premeditated violence and antisocial behavior") always
  described trait 8's content (as the author relabeled it in Batch 3:
  premeditated violence). It never described trait 7's. Trait 7 ("Maintains
  a hidden, secretive private space/behavior apart from his sociable public
  persona") is a much milder claim that doesn't require violence; a hobby
  or a private vice would satisfy it.
- **Current state.** Trait 8's origin is scene134_beat2. Trait 7's origin
  is **undetermined**; see the open item below.

### Does trait 7 stand on its own? (RESOLVED 2026-10-02: no; see "Trait 7 retired" below)

**What the record shows.** The synthesis cites trait 7 on exactly three
beats, and the resolver checked exactly the same three against it:

| Beat | Synthesis role for trait 7 | Current state |
|---|---|---|
| scene132_beat1 | first_shown_beat_id | `consistent` (log 765). Batch 2 removed its trait-7 role when it moved the origin to scene134_beat2. That move is now itself withdrawn |
| scene134_beat2 | escalation vs. scene132_beat1 | now trait 8's origin (above) |
| scene136_beat1 | continuation vs. scene134_beat2 | `consistent` (log 767). Its anchor is now a trait-8 beat |

No other synthesis turning point, resolver entry or REGGIE field mentions
hidden, secret or private behavior. The only stored fields that come close
are:
- scene132_beat1: "unwinding alone", "isolating himself";
- scene92_beat1: "possibly masking alertness", an audience reading with no
  hidden-space content.

**Non-violent candidate text for a standalone trait 7, by script order.**
Every line below was printed from `fog_full.txt` this session.

1. **His occupation of the cabin, which is not his property.**
   - TRUDY: "You know Reggie's been trying to get dad to sell him the
     cabin." (2547-2548)
   - "A half-built patio sits over an old root cellar." (2893, scene92,
     Reggie building it)
   - "Lived in. Cluttered with take-out containers and empty beer cans...
     Clearly Reggie's been sleeping here." (2957-2959, scene94_beat1)
   - "Reggie's newly-completed patio... we catch glimpses of the bulkhead
     cellar door." (4255-4259, scene130)
   - "Locks have been changed." (5209, scene163). The page doesn't say
     who changed them.

   These are concealment by occupation: a private space carved out of
   someone else's property. But apart from the patio over the cellar,
   none of it is hidden from anyone. Reggie says it openly ("The patio was
   one of our projects. I thought it'd be fitting to see it through.",
   2942-2944).
2. **The cellar as a private space, before anything violent is shown.**
   - "The light snaps on showing the cellar. A handyman's man-cave.
     Reggie descends the stairs, shirtless, clutching a bottle of scotch."
     (4272-4274, scene132_beat1)
   - "On a shelf are displayed a few photos of Mackie and Reggie --
     hunting photos and wartime photos. Best buds, smiling." (4288-4289,
     scene134_beat1, not queued, no CI block)

   This is the closest thing to a non-violent private space on the page.
   But log 765 already ruled scene132_beat1 preparatory: "amped and numb"
   before the man behind the door.
3. **The costume and the door.** "a furry grey costume -- a bunny suit"
   (4317); "a heavy steel door... Only darkness inside" (4322-4323);
   "This Is Our Town" (4328), all scene136_beat1. Nothing violent is shown
   on the page here. But the door leads to the room where Alberto is later
   found ("door to the old furnace room. Padlocked.", 5270; 5349), so its
   secrecy serves trait 8's content.

**The question to decide.** Is there a trait 7 independent of trait 8?
- **If yes,** its origin would be scene132_beat1 (the man-cave, as the
  synthesis had it) or the earlier cabin-occupation lines. Neither of
  those is queued with a trait-7 claim.
- **If no,** trait 7 is the concealment *aspect* of trait 8, the secrecy
  that keeps the violence apart from the sociable persona. It would not
  be a separately tracked trait.

Batch 4 (scene172_beat2-5) cites only traits 5 and 8, and 172_5 cites
trait 5 alone. None of them depends on trait 7.

### Synthesis-record override: trait 7 retired, folded into trait 8 (2026-10-02, author-confirmed)

**No values change.** No field or log entry is touched. The synthesis
file `fog_pass2_calls/synthesis_REGGIE.json` is not edited, because it
is the cold record. This section overrides its trait list for REGGIE.

**The decision.** Trait 7, "Maintains a hidden, secretive private
space/behavior apart from his sociable public persona", is **not a
standalone trait**. It is the concealment mechanism of trait 8, not an
independently meaningful capacity. Every candidate for non-violent trait-7
content fails on inspection:
- **The cabin occupation isn't concealed.** Reggie talks about the patio
  openly: "The patio was one of our projects." (2942). Trudy knows about
  his pursuit of the cabin: "You know Reggie's been trying to get dad to
  sell him the cabin." (2547-2548).
- **The man-cave was already ruled preparatory** (scene132_beat1, log
  765).
- **The bunny suit and the steel door exist to conceal the violence**
  (4317-4328). The door leads to the room where Alberto is found (5270,
  5349).

A hidden space carries dramatic weight only because of what is hidden in
it. A private hobby room with nothing sinister in it would never have
registered as a trait worth tracking.

**REGGIE's trait, as now recorded.** Trait 8 is premeditated violence,
with concealment an inherent feature of how it's carried out. It
originates at **scene134_beat2**. The single thread:

| Beat | Synthesis citation (cold) | Now | Value |
|---|---|---|---|
| scene132_beat1 | trait 7 first_shown (also trait 4, escalation) | trait 8: ruled-preparatory context before the origin | consistent (log 765), unchanged |
| scene134_beat2 | trait 7, escalation vs. scene132_beat1 | **trait 8 origin** | boundary_revealed (log 766), unchanged |
| scene136_beat1 | trait 7, continuation vs. scene134_beat2 | trait 8 continuation | consistent (log 767), unchanged |
| scene168_beat1 | trait 5, continuation vs. scene167_beat1 | trait 8, redirected at John | consistent (log 768) |
| scene172_beat1 | trait 5, escalation vs. scene95_beat1 | trait 8, first confrontational use | boundary_revealed (log 769) |
| scene172_beat6 | trait 8, continuation | traits 1+5 jointly, trait 8 as mechanism | boundary_revealed (log 759 + record correction) |

**What this supersedes.** The trait labels in logs 765-767's notes and in
Batch 2's record correction stay as the cold record. This section
supersedes them. scene136_beat1's note that the plaque "This Is Our Town"
is a thematic echo only is unaffected.

**Precedent and its direction.** The author files this in the same family
as TRUDY's trait 6 and JOHN's baseball avoidance vs. reciprocal honesty: a
descriptive wrapper mistaken for an independent trait (axis 1, the
trait-identity gate). One difference, for the record. TRUDY's trait 6 was
*one* synthesis trait that had to be **split** into two (concealment and
resentment; `FOG_TRUDY_REVIEW.md`, "trait 6 is split into two traits").
JOHN's case surfaced a *new*, untracked trait. REGGIE's trait 7 is the
inverse: *two* synthesis traits that are **merged** into one. The gate
works in both directions. It asks whether a trait's identity holds, not
only whether a trait is too broad.

### Batch 4: the standoff, scene172_beat2-5 (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene172_beat2-6 was
found word for word, every speaker matches its raw cue, and raw lines
5412-5491 are fully covered by the stored turns. The mid-speech "(pause)"
(5461) is stored inline, which is how the beat detector is designed to
work. No defects.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene172_beat2 | throughline_evolution (trait 5, continuation vs. 172_1) | **consistent** | log (770) |
| scene172_beat3 | throughline_evolution (trait 5, continuation vs. 172_2) | **consistent** | log (771) |
| scene172_beat4 | throughline_evolution (trait 5, continuation vs. 172_3) | **consistent** | log (772) |
| scene172_beat5 | throughline_evolution (trait 5, echo vs. scene95_beat1) | **consistent** | log (773) |

**scene172_beat2-4, consistent (author-confirmed).**
- **Re-anchored.** These beats are no longer scored on trait 5. They
  continue scene172_beat1, which is now trait 8's gunpoint confrontation
  (log 769). They belong to the trait 8 chain that starts at
  scene134_beat2.
- **Nothing new happens.** The synthesis and resolver already describe
  pure continuation: "same unbroken standoff", "direct continuation", "no
  gap or new context".
- **Every Reggie command still presupposes John has a choice left:**
  - "I'm givin' you a chance here, Johnny." (5425-5426)
  - "Drop the fucking gun, go on back to L.A., and let me handle this."
    (5432-5433)
  - "You dumb motherfucker. Drop that fucking gun!" (5438-5439)
  - "You're forcing my hand here, John!" (5448)
- **Provenance note.** scene172_beat3 and beat4 show provenance
  `llm_human_corrected` only because of JOHN's corrections. Before logs
  771-772, no log entry touched REGGIE's entries on those beats except
  his Pass 2 drafts. His stored fields on them (beat3: emotion "fear,
  anger, urgency"; beat4: "being pushed into a violent decision he doesn't
  want to make") have still never been reviewed.

**scene172_beat5, consistent (author-confirmed).**
- **What the beat is.** It is the Mackie-loyalty thread planted at
  scene95_beat1 ("Matter of fact he did.", 3103; log 764), speaking its
  full content for the first time, under pressure:
  - "Your father was my buddy. My man! In his last moments, we were
    together... me and him... in the goddamn fucking ambulance!"
    (5456-5459)
  - "I made him a promise: that I'd finish what we started." (5462-5463)
- **Elaboration, not a new crossing.** It is new in detail, not in kind.
  scene95_beat1 already showed that Mackie spoke to him privately about
  the case, and this beat fills in what that was.
- **The author's reading of scene95_beat1** as "some private
  understanding" is an inference; the page has only the admission.

**The corrected chain (trait 8; supersedes the Batch 3 and trait 7
tables):**

| Beat | Role | Value |
|---|---|---|
| scene132_beat1 | preparatory context | consistent (765) |
| scene134_beat2 | origin | boundary_revealed (766) |
| scene136_beat1 | continuation | consistent (767) |
| scene168_beat1 | redirected at John | consistent (768) |
| scene172_beat1 | first confrontational use | boundary_revealed (769) |
| scene172_beat2-4 | continuation of the standoff | consistent (770-772) |
| scene172_beat6 | lethal culmination; trait 8 is the **mechanism** | boundary_revealed (759); basis below |

scene172_beat5 sits inside the standoff but is scored on the
Mackie-loyalty thread, not trait 8 (log 773).

### Record correction 2: scene172_beat6's basis is the Mackie-loyalty motive alone; trait 5 is cover (2026-10-02, author-confirmed)

**Value unchanged: `boundary_revealed`.** No log entry. Only the stated
basis changes, and it supersedes the 2026-10-01 "traits 1 and 5 jointly"
record correction above.

**The resolution of the trait-5 tension.** scene172_beat1's framing (log
769, "rhetorical cover, not the engine") was the more accurate one.
Within scene172_beat5's speech, the substantive and specific motive is
loyalty to Mackie personally, through the ambulance promise (5456-5463).
"This is our town." (5463-5464) is four words of borrowed public-facing
rhetoric on a much longer, much more personal speech about a dying
friend's wish. That makes it **one real motive wearing trait 5's language
as cover**, not two equal engines. scene172_beat6's verdict therefore
rests on that loyalty alone:
- "I ain't breakin' my promise! May the Lord be my witness, you've made
  your choice, Detective." (5480-5482)
- "Reggie takes aim at John's head." (5484)
- "Reggie pulls the trigger." (5490)

The loyalty is revealed to have no limit, not even for Mackie's own son.
Trait 8 stays the mechanism.

**Flag: which trait is "trait 1"? (RESOLVED 2026-10-02: the Mackie-personally thread, scene95_beat1; see "Record correction 3" below).** The instruction names
this motive "trait 1, loyalty to Mackie". The record holds two different
things under that idea:
- **Synthesis trait 1**, "Performs warm, seemingly genuine camaraderie and
  loyalty toward Mackie's **family** (John/Trudy), offering gifts,
  reminiscence, and unconditional help". It is first shown at
  scene53_beat1 ("Mackie's favorite. Your's too, from what I remember?",
  1478-1480).
- **The Mackie-promise thread** that Batch 1 recorded as a separate,
  untracked trait (log 764). Its planted origin is scene95_beat1, and it
  is spoken at scene172_beat5.

The 2026-10-01 record correction already filed the promise under "trait
1". The choice matters for what the verdict says, though not for its
value:
- **If trait 1 means loyalty to Mackie's family**, scene172_beat6 shows
  that loyalty's *limit*: it loses to the promise, against Mackie's son.
  That was log 759's original reading.
- **If the motive is loyalty to Mackie personally**, scene172_beat6 shows
  that loyalty has *no* limit, which is this correction's reading. Its
  anchor is then scene95_beat1, not scene53_beat1.

Either way the value is `boundary_revealed`. The anchor to record is for
the author to decide. Until then, both anchors are listed.

### Principle 11 check, scene172_beat2-5 (report only; no new instance)

Each Reggie statement in this stretch is an offer, a command, or a
statement that still leaves John an action to take:
- "I'm givin' you a chance here, Johnny." (5425)
- "Drop the fucking gun, go on back to L.A." (5432-5433)
- "Drop that fucking gun!" (5439)
- "You're forcing my hand here, John!" (5448)
- "I made him a promise: that I'd finish what we started." (5462-5463), a
  past commitment, not a declaration of what will now happen
- "Now stand down, soldier!" (5474)

The only line that puts John's own choice in the completed past tense is
"you've made your choice" (5481-5482), at the already-confirmed
scene172_beat6 endpoint. Every statement before 172_6 leaves a way out,
and only 172_6 forecloses it. That is clean textual support for Principle
11's contingent/unconditional test. It is recorded as a candidate worked
example (see `FOG_COLD_RUN_FINDINGS.md`, finding 19, "Principle 11
verification").

**One correction to the instruction.** It listed "turn around and leave"
among Reggie's imperatives. That line is JOHN's ("This is my property. I
want you to turn around and leave. Or I'll be forced to defend myself.",
5451-5453), and it is Principle 11's own contingent example. Reggie's
imperatives are the ones listed above. The pattern holds without it.

### Record correction 3: scene172_beat6 anchors on the Mackie-personally thread, scene95_beat1 (2026-10-02, author-confirmed)

**Values unchanged: `boundary_revealed`, weight_proportionality
`matched`.** No log entry. Only the anchor and the reasoning change. This
supersedes the trait-1 anchor (scene53_beat1) in record corrections 1 and
2 above.

**The anchor.** The loyalty thread behind the verdict is the private,
specific bond with Mackie personally, planted at **scene95_beat1** ("My
father ever speak privately to you about the Holly Roberts case?" /
"Matter of fact he did.", 3097-3103; log 764). It is **not** synthesis
trait 1, camaraderie toward Mackie's family (scene53_beat1). The thread
runs:
- scene95_beat1 plants a private, specific bond with Mackie.
- scene172_beat5 reveals what that bond demanded: "I made him a promise:
  that I'd finish what we started." (5462-5463)
- scene172_beat6 shows that narrow devotion to one dead friend has no
  limit: "I ain't breakin' my promise! May the Lord be my witness, you've
  made your choice, Detective." (5480-5482); "Reggie takes aim at John's
  head." (5484); "Reggie pulls the trigger." (5490).

It is not a broader family loyalty collapsing. Loyalty to Mackie
specifically was always able to override the life of Mackie's own son.
Trait 8 stays the mechanism, and trait 5's "This is our town." stays
cover.

**The author's reasoning, checked against the standoff text
(5380-5484).**
- **No family appeal.** Reggie never invokes Trudy, Cheyenne or Mackie's
  family as such; neither name appears in his lines in this range. Every
  justification is about Mackie personally:
  - "Your father was my buddy. My man!" (5456)
  - "I made him a promise" (5462)
  - "I ain't breakin' my promise!" (5480)
- **One qualification.** "Your father not turning you in 20 years ago?
  Was that right? You're goddamn right it was!" (5471-5474) does refer to
  John's place as Mackie's son: Mackie protected *him*. Reggie uses it as
  a rebuttal to "It's not right." (5467), endorsing Mackie's own
  rule-breaking. It is not an appeal to family feeling, and it softens
  nothing.
- **How Reggie addresses John, across the whole standoff:** "John"
  (5383-5384, 5404), then "Johnny" (5426, in the offer "I'm givin' you a
  chance here"), then "John" (5448), "soldier" (5474) and "Detective"
  (5482).
  - The author's "Johnny -> John -> soldier -> Detective" is accurate from
    scene172_beat2 on. Over the full standoff, though, the sequence opens
    on "John", warms once to "Johnny" with the offer, and only then grows
    more distant and formal.
  - That reading holds from the offer onward. It is not a monotonic
    progression from the first line.

### Note on John's exit offer (2026-10-02, author-confirmed; no change)

Batch 4's flag stands: "turn around and leave" is JOHN's line. The
grammar pattern (every pre-172_6 Reggie statement leaves a way out) holds
on Reggie's own lines alone: "go on back to L.A." (5432-5433), "Drop that
fucking gun!" (5438-5439), "Now stand down, soldier!" (5474).

John's line separately gives Reggie an explicit exit: "This is my
property. I want you to turn around and leave. Or I'll be forced to
defend myself." (5451-5453). Reggie doesn't take it. He answers with the
promise speech (5456-5464) and, two exchanges later, fires (5490). If
anything, this strengthens the case that scene172_beat6 is a genuine
crossing (Principle 11): Reggie had a stated way out and fired anyway.

### Batch 5: shot and dying confession (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene172_beat7 to
scene175_beat2 was found word for word. Every text defect in the stretch
was already logged:
- finding 7, 4th and 5th occurrences: scene175_beat1 turn 6 and
  scene175_beat2 turn 17;
- finding 20: scene175_beat1 turn 10;
- finding 7's minor gap: the dropped "(smiles)" at 5537.

No verdict depends on any of them.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene172_beat7 | no draft (`arc_claim_check_no_draft`; claimed boundary_revealed, trait 8 continuation) | **the claimed turning point does not hold** | review notes only; no field to correct |
| scene175_beat1 | boundary_revealed (two claims: trait 6 echo vs. scene94_beat2; trait 8 continuation vs. scene172_beat7) | **consistent** | log (774) |
| scene175_beat2 | boundary_revealed (trait 8 continuation vs. scene175_beat1) | **consistent** | log (775) |

**Provenance note.** REGGIE's fields on all three beats have never been
reviewed. The beat-level provenance reflects JOHN's and DOUG's
corrections.

**scene172_beat7: the claimed turning point does not hold (author-confirmed,
8b).**
- **The claim.** The synthesis said "Reggie is hit and howls in pain... now
  exposing his own physical vulnerability and the failure of his violent
  campaign."
- **Why it fails.** Trait 8 tracks Reggie's *willingness* to use
  violence. Being shot is something that happens *to* him: "returns
  fire--" (5494, John), "BOOM! Another ear-splitter." (5496), "A howl from
  Reggie." (5498). Vulnerability under attack was never part of what
  trait 8 tracks.
- **Precedent.** This is the same disposition as TRUDY's scene193_beat1,
  a no-draft arc claim recorded as not holding. TRUDY's scene131_beat1
  reached the same outcome, but as a drafted entry corrected through the
  log.

**scene175_beat1, consistent (author-confirmed). Both cited grounds
fail.**
- **(a) The echo vs. scene94_beat2 (trait 6) is a misread (8b).**
  - Trait 6's anchor is evasion about Reggie's *own* involvement: "Reggie?
    Where were you the day Holly Roberts disappeared?" (3008-3009),
    "Pardon?" (3015).
  - No one asks him anything about the case here. John says only "Toss the
    gun." (5547) and "Let me make a call." (5562).
  - What he volunteers is entirely about other people, and none of it
    concerns his whereabouts or guilt:
    - "Mackie looked after that little girl... like she was his own..."
      (5534-5535)
    - "You know Cheyenne never brought Holly to church?" (5553-5554)
    - "Mackie wanted to change that. Started takin' Holly to Sunday
      service. Him and Trudy..." (5570-5572)
  - It is the Mackie-personally thread (origin scene95_beat1, log 764)
    speaking its full content now that death removes any reason to protect
    it.
- **(b) The trait-8 continuation vs. scene172_beat7 fails (8b).**
  - He performs no act of force. "Reggie tosses the rifle off to his
    side." (5549) complies with John's "Toss the gun." (5547). "Reggie
    smiles, shakes his head 'no'." (5564) declines help.
  - Trait 8 was already spent at scene172_beat6. A trait can't reveal a
    "final limit" in beats where it doesn't act.
  - The synthesis's own continuation anchor, scene172_beat7, does not hold
    either (above).
- **What the beat is.** The Mackie-devotion thread, turning from action to
  explanation and meaning-making as Reggie dies. It elaborates that
  thread's established content; it doesn't cross anything new.

**scene175_beat2, consistent (author-confirmed).**
- **Why the claim fails.** It fails on the same ground as 175_1(b): trait 8
  performs no act. His death happens to him: "He opens his eyes, looks up
  at John standing over him. He takes one last breath, and then he's
  gone." (5581-5582). It is not his own action or statement, so it can't
  be scored as his turning point.
- **Which principle.** The author cited Principle 10. Its text states the
  own-evidence requirement for *echoes*, and Principle 11 carries the same
  requirement for crossings ("every point-of-no-return instance confirmed
  so far rests on the tracked character's OWN action or declaration... see
  Principle 10"). This beat's claim was a continuation, so the citation
  is to P10 as extended by P11. Principle 9 (a plot event is not a
  character turning point) also applies.
- **His own acts.** "He shuts his eyes." (5574), and his last words: "In
  this topsy-turvy world... you gotta have God on your team..."
  (5577-5579). Those are the Mackie-devotion thread's closing expression,
  theological comfort-seeking, not a violence capacity reaching a limit.

**The corrected understanding.** scene175_beat1 and scene175_beat2 belong
entirely to the Mackie-devotion thread (origin scene95_beat1), in its
dying, reflective final form. They do not belong to trait 8. Trait 8's
arc ends at scene172_beat6, the lethal shot. Everything after is
consequence and closure, not further revelation.

**Later lines that bear on earlier records (context, no change).**
- "He knows Dad and Reggie took matters into their own hands, but that
  they got the wrong guy." (6376-6378, scene213_beat4). This is the only
  later line that says what Mackie and Reggie did together. It bears on
  Batch 1's note that the page never says what "what we started" was
  (5462-5463).
- The captain on Alberto: "Gomez was a registered sex offender. Multiple
  rapes of minors back in Mexico City." (5731-5733). JOHN: "So Reggie got
  his El Vaquero." (5738).

### REGGIE's Pass 2 queue is closed (2026-10-02)

All 16 entries from `fog_pass2_queue.json` have been reviewed, recounted
from the file: 15 `needs_correction_review` and 1
`arc_claim_check_no_draft` (scene172_beat7). scene172_beat7 is REGGIE's
only no-draft entry. scene193_beat1 is TRUDY's.

| Beat | Draft | Final | Record |
|---|---|---|---|
| scene94_beat3 | consistent (finding 17) | consistent | no-op confirmation |
| scene95_beat1 | boundary_revealed | consistent | 764 |
| scene132_beat1 | throughline_evolution | consistent | 765 |
| scene134_beat2 | throughline_evolution | **boundary_revealed** (trait 8 origin) | 766 |
| scene136_beat1 | throughline_evolution | consistent | 767 |
| scene167_beat1 | throughline_evolution | consistent | 758 |
| scene168_beat1 | throughline_evolution | consistent | 768 |
| scene172_beat1 | throughline_evolution | **boundary_revealed** (trait 8, first confrontational use) | 769 |
| scene172_beat2 | throughline_evolution | consistent | 770 |
| scene172_beat3 | throughline_evolution | consistent | 771 |
| scene172_beat4 | throughline_evolution | consistent | 772 |
| scene172_beat5 | throughline_evolution | consistent | 773 |
| scene172_beat6 | throughline_evolution | **boundary_revealed** (Mackie-personally thread; P11 instance) | 759 + record corrections 1-3 |
| scene172_beat7 | no draft (claimed boundary_revealed) | claim does not hold | review notes |
| scene175_beat1 | boundary_revealed | consistent | 774 |
| scene175_beat2 | boundary_revealed | consistent | 775 |

**Totals.**
- The 15 drafted entries end at **3 boundary_revealed, 0
  throughline_evolution, 12 consistent**. The drafts were 3
  boundary_revealed, 11 throughline_evolution and 1 consistent.
- All 11 throughline_evolution drafts were overturned.
- Of the three boundary_revealed drafts, none survived. The three final
  boundary_revealed verdicts all come from throughline_evolution drafts.
- **14 REGGIE Pass 2 log entries** (758, 759, 764-775) and 1 no-op
  confirmation.
- Corrections log total: 775.

**Synthesis-record overrides for REGGIE (synthesis file untouched).**
- Trait 7 is retired into trait 8.
- Trait 8 is premeditated violence, with its origin at scene134_beat2
  (not scene172_beat1) and its arc ending at scene172_beat6.
- The Mackie-personally thread is an untracked trait in the synthesis. It
  originates at scene95_beat1 and anchors scene172_beat5, scene172_beat6
  and scene175_beat1-2.
- Trait 5 is rhetorical cover, not an engine, from scene172_beat1 on.

**Still open, carried to finding 19's principle-session backlog:**
- the axis-3 data point (scene132_beat1; downstream search not run);
- 8a vs. premeditation (scene134_beat2);
- JOHN vs. REGGIE scene172_beat6, type-change vs. scale-change.

## Turning-points check (2026-10-05, author-checked)

Author check of `fog_turning_points_reviewed.json`, for REGGIE's flagged entries:
- **scene172_beat1: comparison scene134_beat2 confirmed (author-confirmed).**
  It is derived from the review's reasoning at lines 396-414 ("Preparing to
  harm a helpless captive becomes violently obstructing an investigator"),
  not stated there as a comparison beat. scene95_beat1 stays the anchor
  that 8b rules a different capacity.
- **scene134_beat2: confirmed as trait 8's origin, no comparison.**
