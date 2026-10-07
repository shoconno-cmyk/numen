# Full of Grace -- HOLLY archetype review record

Per-character review record for HOLLY's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether HOLLY's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each HOLLY verdict, including confirmations that
change no data. Same convention as the other `FOG_*_REVIEW.md` files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention.

Scope: HOLLY's 1 real-archetype beat (2026-09-28 enumeration: present on 10 beats). She also has an untagged entry on scene7_beat3, one of finding 3's six unstable agency_alignment beats.

## Review (2026-09-28)

Checked against a fresh `pdftotext -layout` pull, with all stored turns
found. A reverse check (the PDF text for the scene against the stored
turns, per finding 15) found no missing text in this scene.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene3_beat2 | Trickster (confirmed) | Real unaware mark (Beth's "Hey! Not fair!"), genuine deceptive advantage-seeking: the apple for Krista, then "Last one to the river mucks all our stalls for a week!" and a sudden head start. No field changes. weight_proportionality was `matched` in the Pass 1 output, one of finding 4's premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |

HOLLY's archetype review is complete. 1 real-archetype beat, with a row (recounted 2026-09-28).

## Pass 2 review: HOLLY's queue (2026-10-03, one batch)

**Scope.** HOLLY has 7 entries in `fog_pass2_queue.json`, recounted fresh: 5
`needs_correction_review` (3 boundary_revealed, 2 throughline_evolution)
and 2 `arc_claim_check_no_draft` (scene7_beat3, scene216_beat7, both
claimed boundary_revealed). No finding 17 flags. The raw synthesis (fenced
JSON) matches the saved synthesis on every type, comparison beat and
trait. Material is printed from a fresh `pdftotext -layout -enc UTF-8`
pull, byte-identical to `fog_full.txt`.

HOLLY is on the page only at the opening (scenes 3-7, before she
disappears) and in the boat flashback ("A FEW DAYS AGO...", scenes
214-216). Her captivity is off the page apart from one image (214_2). The
kidnapping was Raymond's, hired by Trudy ("I hired Raymond to take her.",
6418; "So I got her back from Raymond.", 6448).

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Nurturing caretaker who looks out for her friends and their animals' well-being | scene3_beat1 |
| 2 | Playful, mischievous, competitive troublemaker who initiates games and dares among friends | scene3_beat2 |
| 3 | Genuine fear/vulnerability surfaces beneath her playful exterior when confronted with real danger | scene6_beat3 |

**Coverage (recorded, not chased).** Much of HOLLY's own on-page action sits
on beats where she has no entry: "She smiles mischievously." / "She lets
out a quiet laugh." (120-128, 6_1); her choice to gallop off "decidedly
somewhere in between" (163-165, 6_4); "Holly struggles." (6468, 214_4);
"Holly cries" (6478, 216_1); "Holly flails." (6485, 216_2); "Holly is
fighting back." (6512, 216_4); "Holly stops struggling." (6535, 216_6).

## The unifying finding: violence done to her, scored a second time from the victim's side (author-confirmed)

Every drafted beat in HOLLY's captivity and death sequence describes
something TRUDY (or Raymond, off the page) does TO Holly. It is narrated
from the victim's side but was scored as Holly's own capacity failing or
escalating. TRUDY's review already attributes the real character movement
in this sequence to Trudy herself:
- 214_4: boundary_revealed, Principle 11 instance 1 (her point of no
  return);
- 216_5: throughline_evolution (her escalation of the 214_4 limit);
- 216_7: boundary_revealed ("Trudy looks horrified.").

HOLLY's drafts tried to score the same events again from the victim's
side, where there is no equivalent character development. There is no
"Holly arc" during her own drowning, only what is being done to her.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene6_beat3 | boundary_revealed (trait 2 echo vs. 3_2) | **consistent** | log (822) |
| scene7_beat3 | no draft (claimed BR continuation) | **the claim does not hold** | review notes only; no field to correct |
| scene214_beat2 | boundary_revealed (continuation vs. 7_3) | **consistent** | log (823) |
| scene215_beat1 | throughline_evolution (escalation vs. 214_2) | **consistent** | log (824) |
| scene216_beat3 | throughline_evolution (continuation vs. 215_1) | **consistent** | log (825) |
| scene216_beat5 | boundary_revealed (escalation vs. 216_3) | **consistent** | log (826) |
| scene216_beat7 | no draft (claimed BR continuation) | **the claim does not hold** | review notes only; no field to correct |

weight_proportionality stays `matched` on all five drafted entries (not
contested).

**scene6_beat3, consistent (author-confirmed).** Two independent grounds.
- **(a) The echo is mis-anchored.** Its actual textual antecedent ("She
  smiles mischievously.", 120-121) is on scene6_beat1, where HOLLY has no
  entry. The cited comparison, scene3_beat2, never uses the word
  "mischief". The author cited Principle 10. Precisely: Holly's own act
  *is* on this beat ("Holly spins and looks to the source", 134; "Her
  mischief falls from her face", 137). The defect is the echo's antecedent
  sitting outside her record, not a missing own act on the echoing beat.
- **(b) Universal reaction (with 8b).** A startled reaction to an
  unexplained branch snap in an isolated cemetery ("Suddenly, a branch
  SNAPS, heavily on the other side of the cemetery.", 133) is a universal
  reaction, anyone's. It isn't evidence of a limit in trait 2: fear
  arriving was scored as mischief's limit, the same absence-as-limit shape
  as BETH's chain.

**scene7_beat3, the claim does not hold (author-confirmed).** Holly is
offscreen. Her scream being "cut-off suddenly as if by force" (198-199) is
something done TO her, not her own act. The claimed "continuation...
without a gap" ignores that she gallops away at 6_4 (163-165) and that the
next scene opens "RIVERBANK - LATER" with "It's been twenty minutes."
(168, 180). There is a real gap. ("As if" is also hedged narrative
language, the only basis for "by force".)

**scene214_beat2, consistent (author-confirmed).** "Hands bound.
Blindfolded." and the imposed white garments (6444-6445) were all done to
her by her captors, not her own acts. Her only own-act content, "She
trembles.", is an involuntary, universal response to captivity and reveals
nothing character-specific. The claimed continuation from 7_3 spans the
entire off-page captivity (about 200 scenes and days of story time), so it
can't be a continuation of anything in narrative terms.

**scene215_beat1, consistent (author-confirmed).** The claimed escalation
("active resistance never previously shown") is contradicted one beat
earlier: "Holly struggles." (6468) is on scene214_beat4 (no HOLLY entry,
but on the page before this beat). "As Holly's head is thrust down... Held
there." (6472-6473) is Trudy's act. Holly's own act, "She writhes and
struggles mightily.", is the universal physical response to drowning:
anyone held underwater fights to breathe.

**scene216_beat3, consistent (author-confirmed).** "Holly is lifted up
again." (6492) is Trudy's act. "She screams for help." is a universal
response to being repeatedly drowned, not an escalation of any
established personal trait.

**scene216_beat5, consistent (author-confirmed).** The claimed "limit of
her strength" is entirely Trudy's act: "Trudy strikes Holly across her
head. Repeatedly. She shoves her head deeper underwater." (6524-6525).
TRUDY's review already scores that as Trudy's own escalation (TRUDY
scene216_beat5, throughline_evolution vs. 214_4). Holly's own act, "Holly
begins to overpower Trudy." (6524), is the universal physical response of
someone fighting for her life, not a character-revealing escalation of a
fear/vulnerability trait.

**scene216_beat7, the claim does not hold (author-confirmed).** The beat is
narrated entirely from Trudy's side: "Trudy feels the resistance leave
Holly. She let's go of her, watches her, half overboard, bobbing
lifelessly." / "Trudy looks horrified." (6540-6543). Holly's death is the
outcome of Trudy's action. It is already scored on TRUDY's side, through
her Principle 11 crossing (214_4) and its continuation to 216_7 (TRUDY
216_7 boundary_revealed, confirmed). There is no Holly-side turning point;
death is not her own act (Principle 10's own-evidence requirement, applied
by extension).

**Trait-scope creep (author-confirmed, for the record).** Trait 3's stated
content, "fear/vulnerability surfaces beneath her **playful exterior**",
describes a specific psychological contrast. It has no referent once she
is a bound captive: there is no playful exterior left to surface beneath.
The synthesis kept applying the trait because "fear" appears in both
contexts, not because the underlying capacity is the same.

**Principle 11: no instance.** None of HOLLY's acts is a declaration or a
self-authored irreversible act ("She screams for help." is a plea).

### HOLLY Pass 2: final tally (queue closed 2026-10-03)

**Totals.**
- The 5 drafted entries go from 3 boundary_revealed and 2
  throughline_evolution to **0 boundary_revealed, 0 throughline_evolution,
  5 consistent**. Both no-draft BR claims (7_3, 216_7) do not hold.
- **5 HOLLY Pass 2 log entries** (822-826) and 2 no-draft claims recorded
  in the notes.
- Corrections log total: 826. `fog_tagged.json` validates (0 errors, 460
  beats).
- HOLLY is the first character in this review whose queue ends with no
  turning point of any kind.

**Cross-queue: BR drafts overturned since REGGIE: 26 of 27.** REGGIE 3/3,
DOUG 3/3, CHEYENNE 2/2, RICARDO 1/1, O'SHEA 2/2, YOUNG JOHN 3/3, MACKIE
5/6, BETH 4/4, HOLLY 3/3. The one kept is MACKIE scene140_beat6.

**"Something happens TO the character": the sharpest and most complete
instance yet.** This is a character whose entire post-disappearance record
was scored as her own development, when every beat is someone else's
action against her. Counting only claimed limits or turning points that
rest on another character's act (the rule used for the earlier six), HOLLY
adds four:
- 7_3: the scream cut off;
- 214_2: bound and blindfolded;
- 216_5: struck and shoved under;
- 216_7: death.

That makes **10 instances across 5 characters**:
- REGGIE 172_7, 175_2;
- RICARDO 115_1;
- O'SHEA 154_2;
- YOUNG JOHN 75_5, 140_8;
- HOLLY 7_3, 214_2, 216_5, 216_7.

215_1 and 216_3 rest on Holly's own (universal) struggle, so they aren't
counted. Neither is 6_3, where the trigger is external but the reaction
is hers.
