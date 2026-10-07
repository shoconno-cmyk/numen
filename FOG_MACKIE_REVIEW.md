# Full of Grace -- MACKIE archetype review record

Per-character review record for MACKIE's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether MACKIE's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each MACKIE verdict, including confirmations that
change no data. Same convention as `FOG_JOHN_REVIEW.md` and
`FOG_TRUDY_REVIEW.md`.

**Status column:** `pending apply` means the verdict is decided here but
the tagged data file has not been changed yet. `applied` means the change
has landed (`git log` on this file gives the commit). Confirmations that
change no data are also marked `applied`. They get no corrections-log
entry, per the no-op convention, and the beat's provenance is set to
`llm_human_confirmed`.

Scope: MACKIE's 12 real-archetype beats in the cold output (2026-09-28
enumeration: MACKIE present on 16 beats, 12 with a non-empty archetypes
list). Every tag was model output that nobody had reviewed, and no
corrections-log entry named MACKIE before this review. All 12 are in two
continuous flashbacks, scene 75 (the marina, after Andy's death) and
scene 140 (John's bedroom before the funeral).

## Review (2026-09-28)

Each beat was checked against a fresh `pdftotext -layout` pull, with all
stored turns found except for one character difference: scene75_beat5
turn 34 stores "You tell ‘em" with a curly quote, where the PDF has a
backtick ("You tell \`em"). The words are otherwise identical.
Hand-patched dual dialogue (`fog_hand_patches.py`): scene 75's patched
pair is turns 10-11 of scene75_beat1. Scene 140's patched pair is split
across scene140_beat2 and scene140_beat3, neither of which is
MACKIE-tagged.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene75_beat1 | Great Mother (confirmed, dark pole) | Author-confirmed: a sustained cover-up arc where the parental relationship itself becomes the instrument of control -- cutting off John's honesty, forcing acceptance of a hard truth to secure compliance, coaching him on what to tell police, going cold and transactional. | applied |
| scene75_beat3 | Great Mother (confirmed, dark pole) | Same basis (scene 75 cover-up arc). | applied |
| scene75_beat4 | Great Mother (confirmed, dark pole), goal pronoun fixed | Same basis. goal: "so he'll listen to her next instructions" -> "his next instructions" (pronoun error; Mackie is male). | applied |
| scene75_beat5 | Great Mother (confirmed, dark pole) | Same basis. weight_proportionality was `matched` in the Pass 1 output, one of finding 4's 21 premature-resolution entries; reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |
| scene140_beat1 | Great Mother (confirmed, dark pole) | Author-confirmed: instrumental caregiving (arranging support: "I spoke to Cheyenne's mom. Cheyenne said she'll go.") continuing into smothering reassurance pushed past an explicit rejection. weight_proportionality was `matched` in the Pass 1 output (finding 4); reset to `requires_second_pass` 2026-09-28 (finding 4 reset). | applied |
| scene140_beat4 | Great Mother (confirmed, dark pole) | Same basis: physically steadying John ("Mackie goes over and helps John up. He sits him onto the bed."). | applied |
| scene140_beat5 | Great Mother (confirmed, dark pole) | Same basis: reassurance pushed past an explicit rejection ("John pushes Mackie away." ... "Young John recoils."). | applied |
| scene140_beat6 | Shadow, Great Mother removed; fields rewritten | Author-confirmed: "Without warning, Mackie's big powerful hand grabs John's throat, squeezing." carries no relational or instrumental content of its own -- a sudden, wordless rupture, distinct from beat 9's coherent guilt-script. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays achieved. | applied |
| scene140_beat7 | Shadow (confirmed) | Already correctly tagged: "You fucking ungrateful shit!" is raw insult, not yet the structured relational appeal that distinguishes beat 9. No field changes. | applied |
| scene140_beat8 | Shadow, Great Mother removed; fields rewritten; co-present label fixed | Author-confirmed: "John struggles, but can't break free. Mackie's grip hardens." is wordless continuation of the same eruption as beat 6, with no relational content. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays achieved. The second character's label changed from JOHN to YOUNG JOHN (finding 13, data consistency). | applied |
| scene140_beat9 | Great Mother (confirmed, dark pole) | Author-confirmed, reversing an earlier draft proposal to change it to Shadow: "This family has done nothing but sacrifice for you! Your poor dead mother. You wanna disappoint her?!" is a coherent, purposeful invocation of the family bond as leverage -- the same mechanism as a corrupted caregiving ritual actively performed, not a rupture in one. No field changes. | applied |
| scene140_beat11 | Great Mother + Persona (confirmed) | Composure snapping back on ("Trudy. Get in the car, honey."), cold transactional handling of John (the money, "you can take a cab to the church"), while Trudy's lingering stare marks the real gap underneath. No field changes. Author ruling (Oct 6, 2026): Great Mother, dark pole. | applied |

**scene140 shape:** Great Mother on beats 1, 4, 5 (caregiving turning
smothering), Shadow on beats 6, 7, 8 (the wordless eruption and the raw
insult), Great Mother again on beat 9 (the guilt-script), then Great
Mother + Persona on beat 11 (composure back on).

MACKIE's archetype review is complete. Every MACKIE beat with a real
archetype has a row (12, recounted 2026-09-28).

## Pass 2 review: MACKIE's queue (2026-10-03, one batch)

**Scope.** MACKIE has 6 entries in `fog_pass2_queue.json`, recounted
fresh: all `needs_correction_review`, all drafted **boundary_revealed /
mismatch**, no finding 17 flags. All six sit on scene 140 (the funeral
morning, "22 YEARS AGO...", 4399) and form one continuation chain from
140_5. It is the first queue in this review where weight_proportionality
was contested. Every raw synthesis type, comparison beat and trait matches
the saved synthesis. Material is printed from a fresh `pdftotext -layout
-enc UTF-8` pull, byte-identical to `fog_full.txt`. MACKIE's scene 75
turning points (75_3, 75_4, 75_5) were drafted consistent by the resolver
and never queued.

MACKIE's own on-page record is three flashback scenes (68_1, scene 75,
scene 140); in the present timeline he is already dead. His adult conduct
(the shakedown of O'Shea, the doctored Holly reports) is reported by
others only.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Controls the narrative and shifts blame away from his son to protect him from consequences during a crisis | scene75_beat1 |
| 2 | Maintains composed, authoritative control to push his son toward normalcy, minimizing or denying the emotional and moral weight of the crisis | scene75_beat5 |

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene140_beat5 | BR / mismatch (trait 2 escalation vs. 75_5) | **consistent / matched** | logs (807, 808) |
| scene140_beat6 | BR / mismatch (trait 2 continuation vs. 140_5) | **boundary_revealed, re-anchored as its own origin / matched**; **Principle 11 instance** | WP log (809); CC unchanged, re-anchor recorded here (no log) |
| scene140_beat7 | BR / mismatch | **consistent / matched** | logs (810, 811) |
| scene140_beat8 | BR / mismatch | **consistent / matched** | logs (812, 813) |
| scene140_beat9 | BR / mismatch (trait 1) | **consistent / matched** | logs (814, 815) |
| scene140_beat11 | BR / mismatch | **consistent / matched** | logs (816, 817) |

**scene140_beat5, consistent / matched (author-confirmed).**
- **The premise is already disproven.** The draft said the normalization
  tactic "previously secured compliance (John left 'stunned' but
  obedient)" and "now visibly fails". YOUNG JOHN's review established that
  scene75_beat5 shows no compliance or obedience: "John sits stunned."
  (2399), Mackie leaves the choice open ("You tell 'em whatever the hell
  you want", 2389-2390), and trait 5 ("submits") was retired for zero
  textual instances (`FOG_YOUNGJOHN_REVIEW.md`). A tactic can't be shown
  "failing for the first time" when it never succeeded in the cited
  comparison beat. The draft fails on its own stated terms.
- **Whose act.** The claimed limit is John's refusal ("John pushes Mackie
  away." / "Get out." / "Fuck you!", 4458-4471). YOUNG JOHN's review
  recorded that refusal as his own act, the origin of his
  refusal-of-normalization trait. It is the inverse shape of the
  "something happens TO the character" pattern: a limit claimed for one
  character from another character's act.
- **What Mackie does.** His own acts ("It's over. Okay? It's all over.",
  4453-4454; "Now trust me.", 4466; "Mackie moves in for a hug.", 4468)
  are trait 2 continuing, meeting resistance that was always latent, not
  newly exposed.
- **WP matched.** Reassurance before a funeral is proportionate to the
  situation, however it lands.

**scene140_beat6, boundary_revealed confirmed and re-anchored as its own
origin; WP matched; Principle 11 instance (author-confirmed).**
- **Re-anchored (8b, 8a).** Composure breaking into violence ("Without
  warning, Mackie's big powerful hand grabs John's throat, squeezing.",
  4484-4485) is not an escalation of trait 2 ("composed, authoritative
  control"). It is that trait's opposite emerging, the same conflation
  the archetype layer already flagged (Shadow, "a sudden, wordless
  rupture", log 109). It is not trait 1 either. It is a genuine,
  previously untested capacity for physical violence against his own son,
  shown nowhere else on his page; no prior Mackie violence appears in the
  script (checked). It is scored as its own new boundary: 8a's
  singular-climactic-action exception, not foreseeable from his
  established pattern. Record correction: synthesis comparison
  "continuation vs. scene140_beat5, trait 2" becomes **its own origin, no
  comparison**. The value is unchanged, so there is no CC log.
- **WP mismatch -> matched (log 809).**
  - The resolver mis-cited the trigger as "a verbal 'Fuck you'". The line
    immediately before the grab is "You think I'm ever gonna play
    baseball after this?!" (4481-4482), after "Mackie, stunned--" /
    "What?".
  - Per YOUNG JOHN's review (scene140_beat6, accusation of causation),
    that line is not a flat remark about sports. John turns the thing
    Mackie has pushed throughout ("Besides, you got baseball coming up.",
    2396-2397; "You'll go back to school, then spring training.",
    4464-4465) into a direct accusation that Mackie's cover-up ruined it.
  - Measured against the real weight of that provocation, the explosive
    physical reaction is an extreme response to an extreme accusation,
    not a disproportionate one. Newness and proportionality are separate
    questions; this is still unambiguously a crossing into new territory.
  - Record precision: "the thing Mackie values most" and "retaliation for
    everything Mackie has orchestrated" are the author's reading. The page
    supports Mackie's repeated baseball push (2396-2397, 4464-4465; adult
    John: "Dad was supposed to take me to a pitching clinic down in
    Boston.", scene213_beat3) and the line's place directly after
    Mackie's normalizing speech.
- **Principle 11: confirmed instance (author-confirmed).**
  - It is Mackie's irrevocable crossing into physical violence against
    his own son, his own physical act. It cannot be undone once done,
    whatever its non-lethality.
  - It shadows the relationship for the rest of Mackie's life. He dies
    before any reconciliation or reckoning is shown; the next time we see
    him in story order, he is already dead ("MACKENZIE 'MACKIE' KIERSTEAD
    - 1953-2023", 1339).
  - **What it adds to the principle.** It is the first *physical*
    instance whose irreversibility is relational/psychological rather
    than lethal. The other physical instances are lethal or potentially
    lethal force (TRUDY 214_4, JOHN 172_6, REGGIE 172_6). The instruction
    called it "the first instance where the irreversibility is
    relational/psychological rather than physically fatal or legally
    final", but JOHN 223_1 is already non-lethal. It is a speech act
    whose finality is relational. So this broadens the "cannot be undone"
    test for physical acts specifically: a non-lethal physical act can
    cross a point of no return through what it does to a relationship.
  - **Scope condition.** MACKIE's own record is three flashback scenes,
    but he is central to the story's backstory, and the scene 75 / 140
    material gives a clear baseline (control, coaching, smothering
    reassurance) to register the change against.
  - Instance list updated in finding 19 and in Principle 11's note
    (`tagging_schema.py`): now 5 instances across 4 characters.

**scene140_beat7 and scene140_beat8, consistent / matched
(author-confirmed).** Genuine continuations of 140_6's violent crossing,
the same unbroken chokehold: verbal degradation added ("You fucking
ungrateful shit!", 4488), grip hardening ("Mackie's grip hardens.",
4490). Nothing new beyond 140_6. WP matched on both, continuing 140_6's
proportionate response to its real trigger.

**scene140_beat9, consistent / matched (author-confirmed).**
- **Fails 8b decisively.** Trait 1 is specifically "shifts blame AWAY
  FROM his son"; this beat does the opposite, placing guilt ONTO him:
  "This family has done nothing but sacrifice for you! Your poor dead
  mother. You wanna disappoint her?!" (4493-4495). Not trait 1 at all.
  The synthesis's "manipulative-control trait" was a widened reading of
  trait 1 (trait-scope creep).
- **What it is.** A continuation of 140_6's crossing: the archetype
  layer's "family bond as leverage" layered onto ongoing violence. The
  same event continuing, not a second boundary.
- **WP matched**, continuing 140_6's proportionate response.

**scene140_beat11, consistent / matched (author-confirmed).** Trait 2's
stated content resuming after Young Trudy's arrival ends the violence:
"Trudy. Get in the car, honey." (4504); "Mackie composes himself."
(4506); "When you're ready..." / "... you can take a cab to the church."
(4509-4516) with the tossed money (4511); "Mackie walks out." (4518). The
draft's "unprecedented capacity to compartmentalize" framing invents drama
where the beat shows the established pattern resuming. WP matched:
composure resuming is proportionate to the trait as originally
established. (Record precision: the instruction said trait 2 returns
"word for word". It is the trait's content that returns; its wording
isn't in the script.)

### Cross-reference against `FOG_YOUNGJOHN_REVIEW.md` (scene 140)

| Beat | What YOUNG JOHN's review established | MACKIE's draft | Outcome |
|---|---|---|---|
| 140_5 | 75_5 shows no submission (trait 5 retired); John's refusal is his own act | rested on "previously secured compliance" and on John's refusal | **Contradicted**; draft overturned |
| 140_6 | the grab is Mackie's act; John's line is an accusation of causation | Mackie's own act | **Consistent**; BR kept, re-anchored; YJ's reading of John's line grounds the WP correction |
| 140_7 | no YOUNG JOHN entry | Mackie's own act | no conflict |
| 140_8 | the grip is Mackie's act (the happens-TO instance for John); the release follows Trudy's arrival | Mackie's own act | **Consistent**; continuation |
| 140_9 | no YOUNG JOHN entry | Mackie's own act | no conflict |
| 140_11 | the release follows Young Trudy's arrival | composure, money, exit are Mackie's own | **Consistent**; the release was Trudy-prompted, the resumed composure is trait 2 |

The "something happens TO the character" pattern stays at six instances
across four characters. MACKIE is the actor in 140_6-140_9 and 140_11.
140_5 is the inverse shape (a limit drawn from another character's act),
which is recorded here but not counted in the six.

### MACKIE Pass 2: final tally (queue closed 2026-10-03)

**Trait set after review (override; synthesis JSON untouched):**

| # | Trait | Origin | Turning points |
|---|---|---|---|
| 1 | Controls the narrative and shifts blame away from his son | scene75_beat1 | none (75_3, 75_4 drafted consistent, not queued; 140_9 rejected, 8b) |
| 2 | Composed, authoritative control pushing toward normalcy | scene75_beat5 | none; 140_5 and 140_11 consistent |
| new | Physical violence against his son (singular crossing) | scene140_beat6 | 140_6 is the origin itself (boundary_revealed, 8a; Principle 11); 140_7-9 consistent continuations |

**Totals.**
- The 6 drafted entries go from 6 boundary_revealed / 6 mismatch to **1
  boundary_revealed, 5 consistent; 6 matched**.
- **11 MACKIE Pass 2 log entries** (807-817): 5 characterization_consistency
  and 6 weight_proportionality. The 140_6 re-anchor and its Principle 11
  confirmation are record-only.
- Corrections log total: 817. `fog_tagged.json` validates (0 errors, 460
  beats).

**Cross-queue: the BR-draft streak breaks.** MACKIE overturns 5 of 6
boundary_revealed drafts and keeps one (140_6). The count since REGGIE is
now **19 of 20**:
- REGGIE 3/3, DOUG 3/3, CHEYENNE 2/2, RICARDO 1/1, O'SHEA 2/2, YOUNG JOHN
  3/3, MACKIE 5/6.

This is the first BR draft kept since REGGIE. Like JOHN 175_1 earlier, it
is kept on a corrected basis (here re-anchored as its own origin under
8a), not on the draft's own reasoning, which called it a continuation of
trait 2.

**Principle 11 count: 5 instances across 4 characters**, all
boundary_revealed: TRUDY scene214_beat4, JOHN scene172_beat6, REGGIE
scene172_beat6, JOHN scene223_beat1, MACKIE scene140_beat6.
