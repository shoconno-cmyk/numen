# Full of Grace -- CHEYENNE archetype review record

Per-character review record for CHEYENNE's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether CHEYENNE's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each CHEYENNE verdict, including confirmations
that change no data. Same convention as the JOHN, TRUDY, MACKIE, O'SHEA
and REGGIE review files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention, and the beat's
provenance is set to `llm_human_confirmed`.

Scope: CHEYENNE's 2 real-archetype beats in the cold output (2026-09-28
enumeration: CHEYENNE present on 24 beats, 2 with a non-empty archetypes
list). scene154_beat2 (Persona -> ordinary_reaction) was already
corrected during JOHN's review and is not in the enumeration. She has no
real archetype tag in the scene155 car ride (beats 3, 5, 8, 9 and 11 are
all no_confident_archetype).

## Review (2026-09-28)

Both beats were checked against a fresh `pdftotext -layout` pull, with all
stored turns found. Scene 64 is one continuous scene at her townhouse
(pp. 39-40).

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene64_beat6 | Persona (confirmed) | Real depicted gap: "She turns on a hopeful expression." is textually marked as a deliberate performance, not spontaneous feeling. No field changes. | applied |
| scene64_beat7 | Persona (confirmed), goal corrected | Same basis: the hopeful expression she has just turned on carries into her ask ("Trudy... she, um, she said you might be able to help? Mackie, he was--"). goal: "Get Trudy's contact to help Mackie" -> "ask John to help investigate something involving Mackie". The stored goal inverted her line: she is asking John for help regarding Mackie, not asking for a contact from Trudy. goal_status stays deferred. weight_proportionality was `matched` in the Pass 1 output, one of finding 4's 21 premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |

CHEYENNE's archetype review is complete. Both of her real-archetype
beats have a row, and both still carry Persona (recounted 2026-09-28).

## Pass 2 review: CHEYENNE's queue (started 2026-10-03)

**Scope.** CHEYENNE has 9 entries in `fog_pass2_queue.json`, recounted
fresh: all `needs_correction_review`, 7 throughline_evolution and 2
boundary_revealed. None has a finding 17 flag, and every raw synthesis
type matches its stored type. Material is printed from a fresh
`pdftotext -layout -enc UTF-8` pull, byte-identical to `fog_full.txt`.

**YOUNG CHEYENNE is a separate entity with 1 entry** (scene60_beat4,
throughline_evolution), not counted here. This is the CHEYENNE/YOUNG
CHEYENNE split watched under finding 21. It still needs its own review.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Greets John with warmth and a forgiving smile, reflecting an easy familiarity/history between them | scene63_beat1 |
| 2 | Presents as an apologetic, hospitable host trying to maintain normal domestic routine (coffee, a decorated home, a birthday cake) despite being a struggling single mother | scene64_beat1 |
| 3 | Shows visible signs of strain and substance use beneath a functioning exterior (strung out, smoking, working a service job) | scene98_beat1 |
| 4 | When cornered or physically restrained, resorts to manipulation, false threats, or denial to escape confrontation | scene152_beat1 |

Batches, in story order:
1. The molly night: scene133_beat1, scene135_beat1, scene149_beat2,
   scene150_beat1. **Done.**
2. John's car, late night: scene155_beat5, scene155_beat9, scene155_beat11
   (context, drafted consistent and not queued: scene152_beat1/2,
   scene154_beat2, scene155_beat3). **Done.**
3. The news, and Holly's wake: scene179_beat1, scene181_beat1 (both
   boundary_revealed drafts; 179_1 echoes scene155_beat11). **Done. Queue closed.**

### Batch 1: the molly night (2026-10-03)

Every stored turn was found word for word, and raw lines 3130-3132,
4278-4282, 4307-4311 and 4782-4833 are fully covered by the stored turns.
No defects. scene133_beat1 and scene135_beat1 are the cutaways intercut
with REGGIE's cellar ritual (`FOG_REGGIE_REVIEW.md` Batch 2).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene133_beat1 | throughline_evolution (trait 3, escalation vs. scene98_beat1) | **throughline_evolution, confirmed** | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |
| scene135_beat1 | throughline_evolution (continuation vs. 133_1) | **consistent** | log (782) |
| scene149_beat2 | throughline_evolution (continuation vs. 135_1) | **consistent** | log (783) |
| scene150_beat1 | throughline_evolution (continuation vs. 149_2) | **consistent** | log (784) |

**scene133_beat1, throughline_evolution, confirmed (author-confirmed).** A
clean escalation within trait 3's strain/substance-use half. The anchor's
implied condition, "She looks a bit strung out." (3131, scene98_beat1),
becomes an overt, deliberate act: "She opens her mouth, sticks out her
tongue, and places a pill onto it. Ecstacy. She closes her mouth and
swallows." (4281-4282). It is the first drug use shown on the page.

**scene135_beat1, consistent (author-confirmed).** A pure continuation:
same pill, same effect. "Except Cheyenne. She's rolling like hell on
molly, dancing to a beat heard only in her head." (4310-4311). The
resolver's own wording ("unbroken continuation", "same event, same
escalated state") already says so. Nothing new beyond scene133_beat1.

**scene149_beat2, consistent (author-confirmed).**
- **The synthesis's claim isn't on the page.** It said "mocking his
  concern about her missing daughter's case". John never mentions Holly
  or the case. He asks "Shouldn't you be at work?" (4808), and she
  answers "What are you? A cop?" (4813), "Pause. She realizes, laughs
  hysterically." (4815), "Oh! I am so sorry, officer." (4818), after
  hugging him from behind (4795-4796).
- **The author's reading:** deflection by flirtation and laughter.
  "Flirtation" is an interpretation; the page shows the hug, the joke and
  the laugh.
- **Not a new facet.** The beat shows trait 3's "functioning exterior"
  half failing in real time. That confirms the gap already established at
  scene98_beat1, where she is "a bit strung out" while in uniform
  (3130-3131). It is the same pattern caught from a different angle, not
  new information about her ("She's still rolling on molly.", 4800).
- **The resolver already pointed this way.** Its own "proportionate
  banter under intoxication, continuing the same drug-fueled state"
  supports `consistent`. It simply wasn't turned into the matching
  verdict.

**scene150_beat1, consistent (author-confirmed).** The beat has no
substance-use or strain content: "Cheyenne spills out, followed by John."
(4829-4830); "The fuck is your problem, man?" (4833). It is a pure
reaction to being dragged out of the bar. The synthesis's own framing,
"the same confrontation continuing without a break", describes a
continuation, not new content.

**Principle 11: no candidates in this batch (a clean negative result).**
Each of Cheyenne's acts is one of:
- private, with no declared consequence: swallowing the pill (4281-4282),
  dancing (4310-4311);
- a reaction to something done to her: "Hey!" (4825) as she is dragged
  out, "The fuck is your problem, man?" (4833).

None is her own unconditional declaration.

### Methodological caution for CHEYENNE (author-confirmed, 2026-10-03)

Cheyenne's characterization is deliberately unstable and sometimes
contradictory: an addict with a chaotic personality, whose reactions don't
follow the clean, linear logic of DOUG's or JOHN's. Don't over-fit her
beats into tidy escalating trait ladders. Her inconsistency may itself be
the honest characterization, not evidence of a missed thread to untangle.
Apply this to Batch 3 and to YOUNG CHEYENNE.

### Batch 2: John's car, late night (2026-10-03)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene152_beat1 to
scene155_beat12 was found word for word, and raw lines 4840-5146 are fully
covered by the stored turns. The one known defect is scene155_beat9 turn
28, JOHN's "Mackie and Reggie?" (5070), stored as action. That is finding
20, already logged, and no CHEYENNE verdict depends on it.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene155_beat5 | throughline_evolution (trait 2, escalation vs. scene64_beat7/155_3) | **throughline_evolution, confirmed, re-anchored**: escalation within the advocacy-for-Holly thread (origin scene155_beat3) | no log entry (value unchanged, no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed`. Record correction below |
| scene155_beat9 | throughline_evolution (continuation vs. 155_5) | **consistent** | log (786) |
| scene155_beat11 | throughline_evolution (trait 4, echo vs. 152_2) | **boundary_revealed**, re-anchored as the first failure of trait 4's avoidance function | log (785) |

**A new thread: advocacy for Holly's case. Its origin is scene155_beat3
(author-confirmed).**
- **The origin.** "Why are you not working Holly's case anymore?"
  (4984-4985). It is addressed to John: O'SHEA answers "Cuz cops don't
  give a fuck, that's why." (4988-4989), then JOHN answers "I didn't
  quit." (4992). The author reads it as sincere, undefended worry that if
  John can't help, all hope of finding Holly is lost.
  - scene155_beat3 stays `consistent`, as drafted: this is its first
    showing.
  - Its synthesis entry and CHEYENNE's stored fields wrongly direct the
    question at O'Shea. That error is in the record only; there is no
    field change.
- **Not part of this thread: scene154_beat2.** "Mackie was doing a
  helluva lot more than you are." (4904-4905) and "(with venom) What'd
  you do? Quit?" (4913-4914) are adversarial deflection, venom at John for
  abandoning the case. That is trait 4's territory (avoidance and denial
  when cornered, drafted `consistent` vs. scene152_beat2), not advocacy.
  Keep the two threads distinct.
- **Not trait 2.** scene64_beat7's help request ("Mackie, he was--",
  2124-2126) is about Mackie, in a domestic visit. Trait 2 is
  hospitality and domestic routine. Neither is this thread.

**scene155_beat5, throughline_evolution, confirmed and re-anchored
(author-confirmed). This corrects the earlier proposal of `consistent`.**
- **The escalation.** From scene155_beat3's question to material
  commitment: "You gotta stay on the case, John." (4995); "(she thinks)
  I'll hire you." (4997-4998); "(turns to O'Shea) Baby, give him some
  money." (5000-5001).
- **Why it counts.** It is a real jump from expressing worry to acting on
  it materially: the same underlying drive, now backed by concrete stakes.
- **Record correction (resolver metadata, no field, no log entry).**
  checked_against "Escalation vs scene64_beat7/scene155_beat3 (seeking
  help for Holly's case)", under trait 2 -> "escalation within the
  advocacy-for-Holly thread vs. its origin scene155_beat3".

**scene155_beat9, consistent (author-confirmed).**
- **What the beat is.** A continuation of the advocacy thread (origin 155_3,
  escalated at 155_5). After her pleading look at O'Shea ("Cheyenne gives
  O'Shea a pleading look. O'Shea softens, sighs--", 5037, scene155_beat8),
  she confirms the names his account points to: "It's Reggie, John."
  (5051); "John to Cheyenne. She nods." (5056); "Mackie." (5060).
- **Why it isn't an escalation.** She does it at real personal and
  relational risk, to keep John on the case. That is the same capacity
  continuing, with no further escalation beyond 155_5's material
  commitment.
- **What O'Shea's account shows.** Mackie and Reggie shook O'Shea down for
  drugs and threatened to pin Holly on him: "Wasn't no transaction. It was
  a mutha-fuckin' salt and pepper shakedown." (5073-5075); "crazy cocktail
  shit. High-grade. Pharmaceutical. Government. Military." (5083-5085);
  "Said they're gonna pin Holly all on me." (5089-5090).
- **Correction (a), author-confirmed.** These drugs are **never stated on
  the page** to be the ones used on Alberto. The cellar's needle and vials
  are shown (4295-4300; "used needles and a few empty vials", 5193), but
  the link to Alberto's captivity is inference, not stated fact.

**scene155_beat11, boundary_revealed (author-confirmed). Re-anchored.**
- **Not a content-echo.** The synthesis's echo of scene152_beat2's denial
  fails 8b on content. The denial ("She's not gone. She's coming back, and
  then everything will be fine.", 4869-4870) is about Holly being gone;
  this beat is about her mothering.
- **Trait 4 is defined by its function.** When cornered, she resorts to
  manipulation, false threats or denial to escape: "I swear I'll scream
  'rape'." (4851, scene152_beat1); the denial, then "She breaks free, goes
  to flee." (4873, scene152_beat2).
- **What happens here.** Under the weight of O'Shea's account (5064-5090)
  plus John's "Why didn't you tell anyone?" (5102), the avoidance
  mechanism doesn't activate at all: "Crying wins out." (5111); "I know I
  could've been a better mom. God, I know. (crying intensifies) I'm so
  sorry." (5114-5118).
- **The verdict.** This is the first failure of the trait-4 avoidance
  function, which is what `boundary_revealed` captures.
- **Correction (c), author-confirmed: restraint.** The pressure is not
  bodily restraint, but it is not free of restraint either. "John
  auto-locks all the doors." (4962) is a real, if non-physical, form of
  restraint still in force in this scene.
- **Record correction (resolver metadata).** checked_against "Echo vs
  scene152_beat2 (direct reversal of earlier denial)" -> "first failure of
  the trait-4 avoidance mechanism (function, not content), vs.
  scene152_beat1/2".
- **The value did change.** The stored draft was `throughline_evolution`,
  not `boundary_revealed`, so the change is logged (785).

**Principle 11: the scene155_beat11 vow is a clean negative
(author-confirmed).**
- **The vow:** "You gotta find her, John. I mean, this'll be it for me.
  I'm going clean. NA, AA, fucking born again, whatever it takes... You
  gotta find her... please." (5124-5130).
- **It carries no foreclosing weight.** It is an empty promise, whether
  deceptive or a sincere but unlikely-to-be-kept bargain under acute
  crisis.
- **Correction (b), author-confirmed.** The negative rests on **no
  confirmation either way** on the page, not on any inferred worsening.
  "Deepens her addiction" is not shown. Her later appearances show only
  grief: "Cheyenne collapses." (5657); "Cheyenne is lost, part of her has
  died" (5670-5671).
- **The general question** (grammatically unconditional, substantively
  empty) is finding 19's principle-session backlog item 4.

**Principle 11 for the rest of the batch: no candidates.**
- "I'll hire you." (4998) is an offer, contingent on John accepting.
- "Baby, give him some money." (5001) is a directive.
- The confirmations at scene155_beat9 are disclosures, not declarations
  about what will happen.

### Batch 3: the news, and Holly's wake (2026-10-03)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Both beats' stored turns were found word
for word, and raw lines 5652-5672 are fully covered by the stored turns.
No defects. Both beats are action-only, with empty `characters_present`.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene179_beat1 | boundary_revealed (trait 2, echo vs. scene155_beat11) | **consistent** | log (787) |
| scene181_beat1 | boundary_revealed (trait 2, continuation vs. 179_1) | **consistent** | log (788) |

**scene179_beat1, consistent (author-confirmed).**
- **The citation is incoherent on several axes**, apart from the
  substantive question:
  - The beat is scored under **trait 2**, hospitality and domestic
    routine, which it has no content for.
  - It is anchored on scene155_beat11's **advocacy plea** ("You gotta find
    her, John." / "You gotta find her... please.", 5124/5130). That plea
    belongs to the advocacy-for-Holly thread. It is not the **confession**
    (5114-5118) that Batch 2 scored as trait 4's break.
  - The resolver's rationale ("a previously untested breaking point of her
    hope/denial coping mechanism") uses **trait 4**'s language.
- **Substantively, it isn't a test of Cheyenne's defenses.** "Cheyenne
  opens her door. She sees John. She instantly knows." (5653); "John
  struggles, then breaks the news." (5655); "Cheyenne collapses. John
  catches her before the fall, into his arms. He remains stoic. She is in
  hysterics." (5657-5658).
  - A trusted figure at the door confirming her child's death would
    overwhelm anyone's capacity for denial, however avoidant or resilient.
    This is universal grief at devastating, unequivocal news. It reveals
    nothing distinctive about Cheyenne's own pattern.
- **Principle 9, in a sharper form.** The beat isn't only a plot event that
  changes what the audience knows (Holly found dead; "John. They they found
  Holly's body.", 5598). Its devastating weight is **external to her
  entirely** and would break anyone's composure, so it tells us nothing
  character-specific.
- **A distinction for future reviews.** When a beat's force comes from an
  event that would overwhelm anyone, the reaction is not evidence about the
  character. This sits alongside Batch 3 of DOUG's review
  (decency vs. distinctiveness).

**scene181_beat1, consistent (author-confirmed).**
- **What the beat is.** An explicit, stated continuation of the grief into
  its aftermath: "Cheyenne is up front in a black dress next to a glum
  O'Shea in a dark suit. Cheyenne is lost, part of her has died, and without
  anymore tears to shed for it." (5670-5672). Nothing new is revealed. The
  resolver's own "the same exposed limit persisting" describes a
  continuation, and with scene179_beat1 now `consistent` there is no limit
  to persist.
- **Record note: the value did change.** The instruction treated this beat
  as already `consistent`, but the stored draft was `boundary_revealed`.
  The change is logged (788).

**Nuance added to scene155_beat11's record (author-confirmed; verdict
unchanged, still `boundary_revealed`, log 785).**
- **The nuance.** Cheyenne's outward denial at scene152_beat1/2 ("She's not
  gone. She's coming back, and then everything will be fine.", 4869-4870)
  was probably never fully sincere. Underneath, she likely already
  suspected the worst.
- **What it changes.** scene155_beat11's confession may be less "an
  avoidance mechanism failing" and more "a truth she already knew beneath
  a performance of denial, finally surfacing".
  - The confession is still a genuine, previously unshown moment of
    honesty, which is what the verdict rests on.
  - It is not necessarily evidence that her denial was ever a reliable
    defense.
- **Basis.** This is the author's reading. The page offers support but no
  statement: at scene179_beat1, "She instantly knows." (5653), before John
  says anything.

**Principle 11: CONFIRMED, no instance anywhere in CHEYENNE's queue.**
- **Every batch is a clean negative:**
  - Batch 1: the pill, the dancing, her protests.
  - Batch 2: the offer, the directive, the disclosures, and the "going
    clean" vow, an empty promise.
  - Batch 3: the collapse, and her presence at the wake.
- **What the finding is.** Cheyenne makes no foreclosing declaration and
  takes no foreclosing act anywhere in her reviewed arc. That is an honest
  finding about the character, consistent with the methodological caution
  above.
- **Record note on wording.** The instruction called her "a reactive, not
  a choosing, presence". That overstates the record. Batch 2 confirmed
  scene155_beat5 as an active, material choice ("I'll hire you." / "Baby,
  give him some money.", 4998-5001), and she prompts O'Shea's disclosure
  at scene155_beat8 (5037). The finding is narrower: she makes choices,
  but none of them forecloses anything.
- **Scope.** Her last tagged beat is scene181_beat1. At scene185 she
  appears only in action lines ("Cheyenne is led to the Chrysler 300 by
  O'Shea.", 5741; "She looks out the window at John.", 5754-5755), with no
  per_character entry. That is the presence-detection gap (FUTURE_WORK
  item 1).

### CHEYENNE's Pass 2 queue is closed (2026-10-03)

All 9 entries are reviewed, all `needs_correction_review`.

| Beat | Draft | Final | Record |
|---|---|---|---|
| scene133_beat1 | throughline_evolution | throughline_evolution | no-op |
| scene135_beat1 | throughline_evolution | consistent | 782 |
| scene149_beat2 | throughline_evolution | consistent | 783 |
| scene150_beat1 | throughline_evolution | consistent | 784 |
| scene155_beat5 | throughline_evolution | throughline_evolution (re-anchored to the advocacy thread, origin 155_3) | no-op |
| scene155_beat9 | throughline_evolution | consistent | 786 |
| scene155_beat11 | throughline_evolution | **boundary_revealed** (first failure of trait 4's avoidance function; sincerity nuance) | 785 |
| scene179_beat1 | boundary_revealed | consistent | 787 |
| scene181_beat1 | boundary_revealed | consistent | 788 |

**Totals.**
- The 9 drafts go from 7 throughline_evolution and 2 boundary_revealed to
  **2 throughline_evolution, 6 consistent and 1 boundary_revealed**. Both
  boundary_revealed drafts were overturned. The one final
  boundary_revealed (155_11) came from a throughline_evolution draft.
- **7 CHEYENNE Pass 2 log entries** (782-788) and 2 no-op confirmations.
- Corrections log total: 788.

**Trait threads identified or corrected (synthesis file untouched; this
file overrides it for CHEYENNE):**
- **Advocacy for Holly's case**, a thread the synthesis never tracked.
  Origin **scene155_beat3** ("Why are you not working Holly's case
  anymore?"), escalated at scene155_beat5 (money), continued at
  scene155_beat9 (naming Reggie and Mackie). scene154_beat2's "What'd you
  do? Quit?" is trait-4 venom, not advocacy. This thread is not trait 2.
- **Trait 4 reframed by function.** Avoidance or denial when cornered is
  defined by what it does, not by what is denied. scene155_beat11 is its
  first failure. It carries the sincerity nuance: the denial may have been
  a performance over a truth she already suspected.
- **Trait 2 (hospitality/domestic routine)** holds no queued turning point
  any more. Its three claims (155_5, 155_9, 179_1/181_1) were each re-anchored
  or rejected.
- **Trait 3 (strain/substance use):** one confirmed escalation
  (scene133_beat1). Its continuations are `consistent`.

## YOUNG CHEYENNE Pass 2: scene60_beat4 (closed 2026-10-03)

A separate entity (finding 21's CHEYENNE/YOUNG CHEYENNE watch item) with
1 queue entry: `needs_correction_review`, drafted throughline_evolution /
matched, no finding 17 flag. Her whole tagged record is the boat
flashback, scene60_beat3 (trait origin, consistent), scene60_beat4, and
the aftermath scene67_beat1 (consistent). Single synthesis trait:
"Notices approaching danger and vocalizes it to the group" (60_3).
Checked against a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`; every stored turn found.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene60_beat4 | throughline_evolution (escalation vs. 60_3) | **consistent** | log (795) |

**scene60_beat4, consistent (author-confirmed).** Three grounds.
- **(a) 8b.** Reporting a hazard to the group ("They're coming back.",
  1970, 60_3) and making a direct personal request to the driver ("John? I
  think you should slow down.", 1984) are different capacities, not the
  same vigilance escalating.
- **(b) Hindsight.** The resolver's "moments before an actual collision"
  imports plot information the beat doesn't support. The collision comes
  from the second jet-skier while John watches the first ("John watches
  the injured jet-skier, unaware of the 2nd skier banking in quick toward
  the boat.", 1995-1996), with no textual link to the speed she asked
  about.
- **(c) Universal-reaction test.** Anyone in that position ("Young
  Cheyenne holds on tight", 1980) would ask a speeding driver to slow
  down; it reveals nothing distinctive about her.
- **Whole-character bar.** Her entire tagged presence is 3 beats in one
  flashback, so RICARDO's lowered whole-character bar applies
  (`FOG_RICARDO_REVIEW.md`).
- **Principle 11:** no candidate. Her line is a request, not a
  declaration.

**Finding 21 note (record only).** 60_1 has her "sits close to a
shirtless Young John" (1898) and "Cheyenne looks to John and smiles at
him proudly." (1912-1913), with no YOUNG CHEYENNE entry. Adult CHEYENNE's
trait 1 (warmth/"easy familiarity/history" with John, origin 63_1) can't
see this, which is the hidden-throughline shape finding 21 watches for.
It doesn't bear on 60_4's verdict.

YOUNG CHEYENNE's queue is closed (1/1).

