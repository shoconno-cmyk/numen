# Full of Grace -- ANGIE archetype review record

Per-character review record for ANGIE's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether ANGIE's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each ANGIE verdict, including confirmations that
change no data. Same convention as the JOHN, TRUDY, MACKIE, O'SHEA and
REGGIE review files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention, and the beat's
provenance is set to `llm_human_confirmed`.

Scope: ANGIE's 3 real-archetype beats in the cold output (2026-09-28
enumeration: ANGIE present on 14 beats, 3 with a non-empty archetypes
list). All three are in one continuous phone call. It opens in scene 76
(`EXT. APARTMENT BALCONY - RESEDA`: "Where you at, baby John?"; John:
"Ang... how does a person know if they're doing the right thing?") and
runs in voice-over through scenes 79-81, over John arriving home and
opening the estate lawyer's envelope.

## Review (2026-09-28)

All three beats were checked against a fresh `pdftotext -layout` pull,
with all stored turns found.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene80_beat1 | Mentor (confirmed) | Genuine transmitted wisdom to a present, addressed John ("But, ya know, whether right or wrong, John, we all got a voice in our head..."). No field changes. | applied |
| scene80_beat2 | Mentor (confirmed) | Same basis: "It'll never tell ya what to do. But it'll always tell ya what NOT to do." No field changes. | applied |
| scene81_beat1 | Mentor, Chorus removed; fields rewritten | Direct continuation of the same guidance arc as the two beats before it ("I guess ya gotta listen for that, ya know?"), still aimed at John's specific situation -- no Chorus lift. self_perceived, audience_perceived, goal, goal_status (none -> deferred) and emotion rewritten. | applied |

ANGIE's archetype review is complete. All 3 beats have a row, and all 3
now carry Mentor (recounted 2026-09-28).

## Pass 2 review: ANGIE's queue (2026-10-03, one batch)

**Scope.** ANGIE has 5 entries in `fog_pass2_queue.json`, recounted fresh:
all `needs_correction_review`, all drafted **throughline_evolution /
matched**, no finding 17 flags, no BR drafts. The raw synthesis matches the
saved synthesis on every type, comparison beat and trait. Material is
printed from a fresh `pdftotext -layout -enc UTF-8` pull, byte-identical
to `fog_full.txt`; the parser drops the "(O.S.)"/"(ON PHONE)" cue
extensions from stored speaker names, with no word changes. ANGIE's own
record is the L.A. motel night (scenes 23-26) and one phone call (scenes
76-81).

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Transactional, affectionate-on-the-surface relationship with John -- sex exchanged for cash, framed with casual endearments like 'baby John' | scene23_beat1 |
| 2 | Self-contained, practical bluntness -- declines to stay unless paid, teases John, entertains herself without needing emotional reciprocity | scene24_beat2 |
| 3 | Discomfort with compassion/emotional depth -- reacts to serious news with surface-level, awkward sympathy; narration states outright that compassion isn't her strong suit | scene26_beat6 |

**Record correction: it is one phone call throughout.** The resolver's
scene79_beat1 rationale said the exchange is "now face-to-face rather than
a phone call". That is false: every ANGIE line from 78 to 81 is cued
"ANGIE (O.S.)", the same call that opens at 76 ("Her phone rings.", 2407),
as the archetype review above already recorded. (The error is in the
resolver's rationale, not the synthesis's turning-point text.)

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene78_beat1 | throughline_evolution (trait 1 echo vs. 23_1) | **consistent** | log (827) |
| scene79_beat1 | throughline_evolution (trait 3 escalation vs. 26_6) | **consistent; origin of a new trait** | log (828) |
| scene80_beat1 | throughline_evolution (continuation vs. 79_1) | **consistent** | log (829) |
| scene80_beat2 | throughline_evolution (continuation vs. 80_1) | **consistent** | log (830) |
| scene81_beat1 | throughline_evolution (continuation vs. 80_2) | **consistent** | log (831) |

weight_proportionality stays `matched` on all five (not contested).

**scene78_beat1, consistent (author-confirmed).** The concrete textual
reversal is real: cash changes hands at their first meeting ("digs out
some cash, peels off a few bills. She takes it", 827-828), and here it is
"On the house." (2436). But it is the same transactional pitch, repriced
to zero under pressure, not a qualitative shift to "genuine felt
investment": "Just come back home where you belong, baby. A'ight? I'll
fuck your brains out. On the house." (2434-2436). It comes in the same
register as every prior line ("baby"), still as a come-back-to-me pitch,
with the price adjusted because the stakes of losing him have risen. It is
also her answer to John's serious question ("how does a person know if
they're doing the right thing?", 2430-2431). This is trait 1 adapting its
terms, not escalating into something new.

**scene79_beat1, scene80_beat1, scene80_beat2, scene81_beat1, consistent
(author-confirmed).**
- **Trait 3 doesn't apply.** Trait 3 is discomfort with compassion,
  reacting to grief with awkward surface sympathy ("Oh... bummer. Well, I
  mean... that sucks." / "She grows uncomfortable. Compassion isn't her
  strong suit.", 942-945, at news of John's father's death). These beats
  show Angie engaging with a philosophical question about conscience and
  offering considered personal moral guidance. That has nothing to do with
  grief or compassion-discomfort.
- **New trait (author-identified): capable of real, considered moral
  guidance when someone she cares about is in genuine need.** It is
  supported by the archetype layer's confirmed Mentor tag on 80_1, 80_2
  and 81_1.
  - **79_1 is its origin** (first showing, consistent): "Man, I don't know.
    Ya just... I guess ya just feel something?" (2449-2450), after John
    presses: "I gotta know, Ang." (2442).
  - **80_1, 80_2, 81_1 are continuations** of that one origin, not
    separate escalations: "I haven't always done the right thing. Duh.
    But, ya know, whether right or wrong, John, we all got a voice in our
    head..." (2461-2464); "It'll never tell ya what to do. But it'll always
    tell ya what NOT to do." (2469-2471); "I guess ya gotta listen for
    that, ya know?" (2480-2481).
- **Record precision.**
  - The origin's line opens "Man, I don't know." The Mentor tags begin at
    80_1, not 79_1. The author places the origin at 79_1 as the first point
    where she engages the question instead of deflecting it.
  - The instruction described 80_1-81_1 as "the same cued 'ANGIE (O.S.)
    (CONT'D)' line... no scene breaks". Precisely: only 80_2 carries
    "(CONT'D)" (2468). 80_1 and 81_1 each open on a new slugline ("INT.
    KIERSTEAD HOME - KITCHEN - CONTINUOUS", 2455; "EXT. KIERSTEAD HOME -
    BACKYARD - DAY", 2473). It is one continuous phone speech carried in
    voice-over across those cuts, with 80_1's trailing "..." completed in
    80_2. The continuation verdict is unaffected.
  - 80_1's synthesis "volunteering unprompted vulnerability" is inaccurate:
    the line answers John's "What do you feel?" (2453).

**Principle 11: clean negative for ANGIE (author-confirmed).** No candidate
from her. The crossing in this sequence is John's: "Road sign: Airport
exit. John drives past it." (2438, 78_2); he opens the estate envelope
(2466) and appears "twirling the cabin keys on his finger" (2484). Angie's
counsel is the catalyst playing in voice-over, not her own irreversible
act.

### New failure-mode variant: opposite behavior mistaken for escalation (author-confirmed, for the methodology writeup)

This is related to, but distinct from, the absence-as-limit pattern in
BETH's and HOLLY's queues:
- **Absence mistaken for a limit (BETH, HOLLY):** a trait's *absence* under
  pressure (fear replacing dismissiveness or mischief) was scored as that
  trait's crack or boundary.
- **Opposite mistaken for escalation (ANGIE):** a trait's *opposite*
  (genuine engagement replacing compassion-discomfort) was scored as that
  trait's intensification.

In both, the synthesis kept a beat attached to a trait because the trait's
subject matter (emotion, fear, compassion) appears in both places, instead
of testing whether the beat shows the trait's stated content. The right
move in both is to test the beat against the trait's own wording, and,
where the beat shows something real but different, to identify a new
trait rather than stretch the old one.

### ANGIE Pass 2: final tally (queue closed 2026-10-03)

**Trait set after review (override; synthesis JSON untouched):**

| # | Trait | Origin | Turning points |
|---|---|---|---|
| 1 | Transactional, affectionate-on-the-surface relationship with John | scene23_beat1 | none; 78_1 consistent (terms adapted) |
| 2 | Self-contained, practical bluntness | scene24_beat2 | none queued |
| 3 | Discomfort with compassion/emotional depth | scene26_beat6 | none (79-81 rejected) |
| new | Real, considered moral guidance for someone she cares about in genuine need | scene79_beat1 | none; 80_1, 80_2, 81_1 continuations (Mentor at the archetype layer) |

**Totals.**
- The 5 drafted entries go from 5 throughline_evolution to **0
  boundary_revealed, 0 throughline_evolution, 5 consistent**.
- **5 ANGIE Pass 2 log entries** (827-831).
- Corrections log total: 831. `fog_tagged.json` validates (0 errors, 460
  beats).

**Cross-queue.** ANGIE had no boundary_revealed drafts, so the BR-draft
count since REGGIE is unchanged at **26 of 27 overturned** (the one kept
is MACKIE scene140_beat6). ANGIE adds no "something happens TO the
character" instance (she speaks and acts in every beat), so that count
stays at 10 across 5 characters.
