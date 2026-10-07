# Full of Grace -- CAPTAIN MARCHAND archetype review record

Per-character review record for CAPTAIN MARCHAND's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether CAPTAIN MARCHAND's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each CAPTAIN MARCHAND verdict, including confirmations that
change no data. Same convention as the other `FOG_*_REVIEW.md` files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention.

Scope: CAPTAIN MARCHAND's 1 real-archetype beat (2026-09-28 enumeration: present on 18 beats). He also has an untagged entry on scene206_beat1, one of finding 3's six unstable agency_alignment beats.

## Review (2026-09-28)

Checked against a fresh `pdftotext -layout` pull, with all stored turns
found. A reverse check (the PDF text for the scene against the stored
turns, per finding 15) found no missing text in this scene. The beat carries finding 7's split line ("Your father would be very proud of / you, John.").

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene185_beat2 | Chorus (confirmed) | A closing verdict on John's career and lineage ("despite our obvious differences in methodology, I want to thank you...", "Your father would be very proud of you, John."), not a reaction to an immediate event. No field changes. Provenance was already `llm_human_corrected` from JOHN's review. | applied |

CAPTAIN MARCHAND's archetype review is complete. 1 real-archetype beat, with a row (recounted 2026-09-28).

## Pass 2 review: CAPTAIN MARCHAND's queue (2026-10-03, one batch)

**Scope.** CAPTAIN MARCHAND has 5 entries in `fog_pass2_queue.json`,
recounted fresh: all `needs_correction_review`, drafted 4
throughline_evolution and 1 boundary_revealed, no finding 17 flags. The raw
synthesis matches the saved synthesis on every type, comparison beat and
trait. The synthesis also claimed scene206_beat1 as a continuation of
204_1; the resolver rejected it (drafted consistent, not queued). Material
is printed from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Enforces institutional authority and procedural boundaries over John's outside-consultant role, issuing direct orders and reprimands when John oversteps | scene119_beat13 |
| 2 | Shows personal warmth and respect for John beneath the professional friction between them | scene184_beat1 |

**Stored-turn defects (finding 20 blank-line split class; no log).**
- 120_8: "Your job is done here. Understood?" (3911) is stored as an
  unattributed action turn, split from "You had your time, John. No way."
  (3909) by a blank line under one CAPTAIN MARCHAND cue.
- 185_2: "Your father would be very proud of" / "you, John. Understand me?"
  (5781-5783) is split the same way.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene120_beat6 | throughline_evolution (trait 1 escalation vs. 120_1) | **consistent** | log (832) |
| scene120_beat7 | throughline_evolution (continuation vs. 120_6) | **consistent** | log (833) |
| scene120_beat8 | throughline_evolution (continuation vs. 120_7) | **consistent** | log (834) |
| scene185_beat2 | throughline_evolution (trait 2 echo vs. 120_6) | **consistent** | log (835) |
| scene204_beat1 | boundary_revealed (trait 1 escalation vs. 202_1) | **consistent** | log (836) |

weight_proportionality stays `matched` on all five (not contested).

**scene120_beat6, 120_beat7, 120_beat8, consistent (author-confirmed).
Dominant mechanism: decency vs. distinctiveness.**
- **What 120_6 is.** Calling in the Bureau on a week-old child abduction
  is justified entirely by case facts: "I'm calling in the Bureau." / "It's
  been a week. We both know the grim stats on kids missing beyond a week."
  (3888-3897). Nothing in it is specific to John. It is standard,
  procedurally correct escalation any competent captain would make, not a
  personally distinctive act of authority.
- **8b / trait scope.** Trait 1's stated object is "boundaries over John's
  outside-consultant role". This is case management that sidelines John as
  a side effect, not an escalation of that capacity. Trait 1's genuine
  content is already at its origin, scene119_beat13, a direct John-specific
  order: "Take his statement and cut him loose. ... You. Come with me."
  (3760-3764).
- **120_7 and 120_8** are the same decision continuing to its natural
  conclusion, not separate escalations. First the procedural justification
  ("She is a girl of tender years, 12 and under -- they can monitor
  interstate travel -- they'll share with us intel on other kidnapping
  situations --", 3901-3906), then the dismissal ("You had your time,
  John. No way." / "Your job is done here. Understood?", 3909-3911).
- **Principle 11: no instance.** "I'm calling in the Bureau" and "Your job
  is done here" are reversible institutional decisions. Nothing is
  foreclosed irrevocably: investigations can run in parallel, and
  decisions can be revisited.

**scene185_beat2, consistent (author-confirmed).**
- **Weak echo.** "Look, despite our obvious differences in methodology"
  (5773-5774) is vague and non-specific. It doesn't concretely name the
  Bureau call, so it is weak under Principle 7's concrete-callback test.
- **Whose beat it is.** The more fundamental problem is that the beat's
  dramatic weight belongs entirely to JOHN. "Your father would be very
  proud of you, John." (5781-5783) carries irony only because of what the
  audience and John know: "John nods. Looks away. Knowing he'll keep the
  truth of his father's involvement forever a secret." (5785-5786). That is
  the Andy/cover-up secret: JOHN scene185_beat2, the first on-page showing
  of the justice-independent-of-my-action chain
  (`FOG_JOHN_REVIEW.md`; structural finding in
  `FOG_YOUNGJOHN_REVIEW.md`).
- **What Marchand does.** His own behavior (warmth, gratitude, offering
  closure, "Captain places his hand onto John's shoulder, reassuringly.",
  5778) is trait 2 continuing from its origin one beat earlier at 184_1
  ("Three funerals in two weeks. How are you holding up?"). Nothing in
  Marchand's own arc shifts; the poignancy is situational irony riding on
  John's side (Principle 9 shape).

**scene204_beat1, consistent (author-confirmed).** Fails on two grounds.
- **(a) Factual error.** The synthesis contrasts this with "his confident,
  controlled questioning of Raymond in scene202_beat1", but in that beat
  Marchand questions JOHN: "I'm gonna assume you know nothing about any of
  this." / "Do you believe that what he claims holds any validity?"
  (6155-6164). The Raymond interrogation is run by Federal Agents, with
  Marchand watching through the mirror ("Captain Marchand watches through
  a two-way mirror. On the other side, Federal Agents grill a frightened
  Raymond.", 6033-6034).
- **(b) Something happens TO the character.** The lawyer's intervention
  that halts the interrogation ("This stops now. Now!", 6172; "I'm Raymond
  Olsen's lawyer.", 6182) is not Marchand's action; it interrupts him.
  Trait 1's stated object (boundaries over John's role) has nothing to do
  with an outside lawyer halting an interrogation of Raymond. Marchand's
  own content ("Captain, a sinking feeling..." / "Shit.", 6190-6194) is a
  universal reaction to watching a case collapse and reveals nothing
  distinctive about his capacities.

### CAPTAIN MARCHAND Pass 2: final tally (queue closed 2026-10-03)

**Totals.**
- The 5 drafted entries go from 4 throughline_evolution and 1
  boundary_revealed to **0 boundary_revealed, 0 throughline_evolution, 5
  consistent**.
- **5 MARCHAND Pass 2 log entries** (832-836).
- Corrections log total: 836. `fog_tagged.json` validates (0 errors, 460
  beats).

**No surviving turning point.** MARCHAND joins the characters whose whole
queue resolves to consistent: YOUNG CHEYENNE (1/1), HOLLY (5/5 drafted,
2 no-draft claims failed), ANGIE (5/5), and now MARCHAND (5/5).

**Cross-queue.**
- **BR drafts overturned since REGGIE: 27 of 28.** REGGIE 3/3, DOUG 3/3,
  CHEYENNE 2/2, RICARDO 1/1, O'SHEA 2/2, YOUNG JOHN 3/3, MACKIE 5/6, BETH
  4/4, HOLLY 3/3, MARCHAND 1/1. The one kept is MACKIE scene140_beat6.
- **"Something happens TO the character": 11 instances across 6
  characters.** MARCHAND 204_1 is added to REGGIE 172_7 and 175_2, RICARDO
  115_1, O'SHEA 154_2, YOUNG JOHN 75_5 and 140_8, and HOLLY 7_3, 214_2,
  216_5 and 216_7.
