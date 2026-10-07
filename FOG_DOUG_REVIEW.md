# Full of Grace -- DOUG archetype review record

Per-character review record for DOUG's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether DOUG's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each DOUG verdict, including confirmations that
change no data. Same convention as the JOHN, TRUDY, MACKIE, O'SHEA and
REGGIE review files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit).

Scope: DOUG's 3 real-archetype beats in the cold output (2026-09-28
enumeration: DOUG present on 38 beats, 3 with a non-empty archetypes
list). Author-confirmed context: Doug is a Dover PD officer in a
relationship with Trudy, not John's official partner (finding 8).

## Review (2026-09-28)

All three beats were checked against a fresh `pdftotext -layout` pull,
with all stored turns found. Scene 123 is one continuous parking-lot
argument (pp. 77-78). Its beat 5 has a parse defect in DOUG's own lines
(finding 15).

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene101_beat1 | Chorus, Mentor removed; fields rewritten | Author-confirmed: a stepped-back verdict on John's whole plan ("You're already way out of your jurisdiction. So promise me that you won't go--"), not a targeted personal insight -- the classic "friend/bartender leaning in" Chorus shape. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays violated. The rewrite also removes the invented "partner" wording from DOUG's self_perceived on this beat (finding 8). The earlier `llm_human_corrected` on this beat came from JOHN's wording fix. | applied |
| scene123_beat9 | Chorus, Mentor removed; fields rewritten | Same mechanism as scene101_beat1: an outside observer's diagnosis of John's blind spot regarding Holly ("So... in another life Holly could've been your daughter. And I think that's making you not see things so clearly."), delivered as a read on the situation, not a transmitted skill. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays deferred. | applied |
| scene123_beat15 | ordinary_reaction, Persona removed; fields rewritten | Author-confirmed: his hurt is explicitly narrated ("Doug is stung."), not hidden. Only his restraint ("he takes the high road", "Doug wants to say one more thing... but wisely doesn't") is depicted, and that is shown self-control, not a mask. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays achieved. | applied |

**Recount (2026-09-28):** DOUG went from 3 tagged beats to 2, both
Chorus (scene101_beat1, scene123_beat9). scene123_beat15 no longer
carries an archetype. All 3 beats from the enumeration have a row.

**Finding 8 sweep (complete 2026-09-28):** the "partner" wording on
DOUG's 5 untagged beats (scene83_beat1, scene86_beat2, scene86_beat3,
scene123_beat3, scene175_beat2) is now "colleague", logged as
wording-only fixes. The scene101_beat1 instance was removed in this
review. No DOUG field contains "partner" any more.

DOUG's archetype review is complete.

## Pass 2 review: DOUG's queue (started 2026-10-02)

**Scope.** DOUG has 12 entries in `fog_pass2_queue.json`, recounted fresh
from the file after TRUDY, JOHN and REGGIE closed. They are 11
`needs_correction_review` (8 throughline_evolution, 3 boundary_revealed)
and 1 `arc_claim_check_no_draft` (scene175_beat3). scene101_beat1 and
scene197_beat2 are finding 17 auto-heal entries. Material is printed from
a fresh `pdftotext -layout -enc UTF-8` pull, byte-identical to
`fog_full.txt`.

Batches, in story order:
1. Precinct help: scene101_beat1, scene118_beat1. **Done.**
2. scene123, outside the precinct: scene123_beat7, beat9, beat14, beat15. **Done.**
3. The call about Holly's body and its aftermath: scene175_beat2,
   scene175_beat3 (no draft), scene177_beat1. **Done.**
4. Composure-break chain: scene197_beat2 (finding 17), scene199_beat1,
   scene207_beat1. **Done. Queue closed.**

### Batch 1: precinct help (2026-10-02)

Every stored turn was found word for word, and raw lines 3189-3277 and
3588-3628 are covered by the stored turns. The one known defect is
scene101_beat1 turn 7, "Holly went missing." (3215), stored as
unattributed action. That is finding 20's glued-action split, already
logged. The words are intact and no verdict depends on it.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene101_beat1 | throughline_evolution (claim a, trait 5); claim b (trait 4, auto-healed boundary_revealed) carried as a secondary note | **throughline_evolution, confirmed, with corrected reasoning.** Claim b **does not hold** | no log entry: the confirmation follows the no-op convention, and claim b has no field of its own (see below). Provenance already `llm_human_corrected` |
| scene118_beat1 | throughline_evolution (trait 5) | **throughline_evolution, confirmed** | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |

**scene101_beat1, claim (a): throughline_evolution, confirmed with
corrected reasoning (author-confirmed).**
- **The "unasked" framing is wrong.** The synthesis and resolver both say
  Doug traced the tower pings "unasked". John explicitly asked for this
  kind of digging at scene86_beat4: "Do it again. Call her provider, bring
  up her records, see who she was texting." / "How far back?" / "As far as
  you can get." (2825-2835).
- **Corrected framing:** a meaningful escalation within a broader request
  John did make, not an entirely self-initiated one. "So I tracked the
  tower pings, and the last call made on that number was the morning Holly
  went missing." (3212-3215). Tracing a specific burner number's tower
  pings to pinpoint a physical location still goes beyond the general
  records request. It is real investigative initiative within trait 5's
  established capacity, measured against the anchor at scene71_beat1
  ("Mackie's work." / "Just let us know if you need anything else.",
  2216-2227).
- **Record correction (resolver metadata, no field, no log entry):** the
  rationale's "unasked" is replaced by the framing above.

**scene101_beat1, claim (b), trait 4 vs. scene57_beat3: does not hold
(author-confirmed, Principle 8b).**
- **Three real differences from the anchor.** The anchor is "Trudy goes
  after John. Doug stops her." (1867), "Nope." (1871).
  - **Target:** Trudy there, John here.
  - **Means:** physical restraint there, verbal pleading over a phone call
    here: "I'll call Maine staties." (3235); "Listen to me, John -- don't
    go to Biddeford." (3256-3257); "You're already way out of your
    jurisdiction. So promise me that you won't go--" (3270-3272).
  - **Whose act the failure is:** the failure belongs to John's own
    choice, "CLICK. John's hangs up." (3274). It is not a crack in Doug's
    protective capacity.
- **The capacity works as established.** Doug tries everything available
  to him: calling the staties, warning, pleading, invoking jurisdiction.
  That is the protective instinct operating exactly as established, in a
  situation where its only effective method, physical intervention, was
  never available.
- **The author's reading:** "Doug did everything he could, and he knows
  at the end of it all it's John's decision, and John's consequences." The
  capacity is working as designed and accepting its own limits
  consciously. No boundary is revealed against Doug's will. His "Shit.
  Shit-fuck-shit." (3277) is frustration at the outcome, not a limit
  exposed.
- **This resolves finding 17's mandatory-review item 4.** The item asked
  whether the draft addresses the boundary claim. It does, and the claim
  does not hold.
- **Why there's no log entry.** DOUG has a single characterization_consistency
  field on this beat, and claim (a) governs it, now confirmed as
  `throughline_evolution`. Recording claim (b) as "-> consistent" would
  overwrite the confirmed claim-(a) value. Claim (b)'s rejection is
  therefore recorded here only, the same way a no-draft arc claim is
  handled.

**scene118_beat1, throughline_evolution, confirmed (author-confirmed).** This
is a clean escalation within trait 5. Legitimate channel work (phone
records) becomes actively facilitating an off-book interrogation: "Doug
comes out of a room that certainly isn't any official interrogation room.
He looks around, worried." (3593-3595). That is genuinely riskier and more
procedurally compromising, the same capacity intensifying.
- **Context that doesn't change the verdict.** John brought the suspect in
  (Doug: "Why did you have to bring him here?", 3601). Doug's own part is
  questioning him off the books ("I didn't get much out of him.", 3609).
- **Provenance caveat.** Provenance is beat-level. JOHN's entry on this
  beat (drafted `consistent`, not in JOHN's queue) is covered by the same
  flag, but it was not reviewed here.

**Principle 11: no candidates in this batch (a clean negative result, not
an open question).** Each of Doug's own acts and statements falls into one
of two groups:
- **Already completed, with no real stakes.** He traces the pings
  (3212-3213). "Yes. I got it." (3265) agrees to run the plate, which he
  later does: "Came back clean. Guy's a drywall contractor down in
  Quincy." (4120-4121). In scene118, he questions Ricardo off the books.
- **Explicitly left unresolved.** "I'll call Maine staties." (3235) is a
  declared intent John refuses ("No. Don't.", 3238). Nothing on the page
  shows Doug made the call. "promise me that you won't go--" (3271-3272)
  is cut off when John hangs up, before Doug can finish the request, let
  alone get a commitment.

### Batch 2: scene123, outside the precinct (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn in scene123 was found
word for word, except scene123_beat5's DOUG line. The `-layout` pull
garbles that line across two columns. It was repaired under finding 15
and re-checked against a fresh `-raw` pull (2953-2957), where it matches.
scene123_beat13 turn 31 is JOHN's line split off as action (finding 20,
already logged).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene123_beat7 | throughline_evolution (trait 2 vs. scene56_beat1) | **throughline_evolution, confirmed, with corrected reasoning** | no log entry (no-op convention). Provenance -> `llm_human_confirmed` (12e1b6b) |
| scene123_beat9 | throughline_evolution (continuation of 123_7) | **consistent** | log (776) |
| scene123_beat14 | throughline_evolution (trait 7 vs. scene86_beat3) | **throughline_evolution, confirmed, with corrected reasoning** | no log entry (no-op convention). Provenance `llm_unreviewed` -> `llm_human_confirmed` |
| scene123_beat15 | throughline_evolution (trait 3 echo vs. scene56_beat2) | **throughline_evolution, confirmed, re-anchored**: echo of scene123_beat9 | no log entry (value unchanged). Record correction below. Provenance already `llm_human_corrected` (archetype row) |

**scene123_beat7, throughline_evolution, confirmed (author-confirmed). Two
factual corrections to the record (resolver metadata, no field, no log
entry):**
- **The cigarette is John's, not Doug's.** The synthesis's "offering a
  cigarette" has it backwards. JOHN asks "Wanna smoke?" (1682), and then
  "John hands him a cigarette, lights it for him." (1687), at
  scene56_beat1-2.
- **The truth is never finished in this beat.** The "painful personal
  truth" is cut off: "It's just... man, it's like... You're dad passing
  away, and like... whatever you and Cheyenne had at one time, it's--"
  (4155-4158), interrupted by JOHN's "So what?" (4161).
- **Why the verdict stands anyway.** Attempting a hard, personal truth
  Doug has never raised before is a real escalation past the established
  quiet-companionship baseline of trait 2 ("You, uh, want to be left alone
  or--", 1679), even though John interrupts it. The attempt is what's new,
  not its completion.

**scene123_beat9, consistent (author-confirmed).** This is not a separate
escalation. It is scene123_beat7's escalation completing its interrupted
sentence: "So... in another life Holly could've been your daughter. And I
think that's making you not see things so clearly." (4164-4167). It is one
continuous act split by John's "So what?" (4161), and Doug's "So..." picks
up John's words. There is no new content beyond finishing what 123_7
began.

**scene123_beat14, throughline_evolution, confirmed with corrected reasoning
(author-confirmed).**
- **What the distinction is not.** It is not public vs. private
  witnessing. Both insults share Doug-and-Mackie competence content, but
  the scene86_beat3 anchor is **private**: "EXT. FOOD TRUCK - DAY", Doug
  and John alone at Doug's cruiser (2739-2770). Only the scene123 outburst
  has witnesses ("Some passing officers stop. They watch John's
  outburst.", 4198). An earlier instruction in this review said both were
  witnessed; that is corrected here.
- **What the distinction is: severity and personal cost.**
  - The anchor is impersonal, professional criticism of work product:
    "It's a bullshit report, man. And you know it." (2805-2806). Doug's
    reaction is "Doug takes the insult on behalf of himself and Mackie. He
    checks his watch." (2808-2809).
  - scene123's insults are personal and cutting, from someone Doug is
    actively trying to help: "Fuck you." (4172), and "So either you're too
    loyal to Mackie and his lackies to admit that this case stinks, or
    maybe your just too dumb of a cop to realize it." (4201-4205).
  - The text explicitly marks the cost here: "Doug is stung. But he takes
    the high road--" (4207).
- **The verdict.** Composure holding under a genuinely harder emotional
  test than before is a clean escalation of trait 7.
- **A note for the record.** Doug's direct reply to "Fuck you" is
  "John, c'mon--" (4175, scene123_beat11). scene123_beat14 follows both
  insults cumulatively.
- **Record correction (resolver metadata, no log entry).** The resolver
  framed this as "direct personal hostility... over the earlier
  professional-criticism instance". The reading above replaces that
  rationale's framing, on the same comparison and with the same value.

**scene123_beat15, throughline_evolution, confirmed and re-anchored
(author-confirmed).**
- **Record correction (resolver metadata, no field, no log entry).** The
  comparison moves from scene56_beat2 (trait 3) to **scene123_beat9, as an
  echo**.
- **Trait 3 doesn't hold (8b).** scene56_beat2 is professional-status envy
  toward LA policing ("a cop like me, could get onto the force out
  there?", 1720-1723). scene123_beat15's "I feel sorry for you, John. You
  know? I really do." (4210-4211) has no professional-standing content.
  The only professional term nearby is John's own "too dumb of a cop"
  (4204).
- **The echo.** scene123_beat9's tentative diagnosis ("I think that's
  making you not see things so clearly.", 4166-4167) and scene123_beat15's
  flat statement are the same observation. It escalates in directness and
  emotional weight now that John's outburst has proven the diagnosis
  correct.
  - This is a **two-beat echo relationship (123_9 -> 123_15) inside the
    trait-2 thread that 123_7 escalated**. It is not a new permanent trait
    slot.
  - Doug's own line is the primary evidence (Principle 10).
- **"Doug wants to say one more thing... but wisely doesn't." (4213),
  recorded narrowly.** It is a further thought he chooses not to voice. It
  is **not** evidence of an "even more stinging truth" being deliberately
  withheld; that oversteps what the line supports. This matches DOUG's
  archetype-layer review of the same beat, which read it as shown
  self-control, not suppressed escalation.

**Principle 11: no candidates in this batch (a clean negative result,
consistent with Batch 1).** Each of Doug's statements is one of:
- explicitly unfinished: cut off by John at scene123_beat7 (4158), or a
  further thought left unspoken at scene123_beat15 (4213);
- a judgment or feeling rather than an act with stakes (4166-4167,
  4210-4211);
- undercut by the relationship visibly continuing afterward. "Doug begins
  to eat, avoiding John's eyes." (4390). TRUDY: "Doug is trying his
  best... you really didn't need to go and shit on him like that."
  (4564-4567). JOHN: "Sorry, Doug!" / "You're a very good police
  officer!" (4572-4579), and "Doug pauses mid-bite, looks up from his
  food." (4581).

"I'm sorry, John. We really tried." (5612) is **not** evidence for that
last point: it refers to the search for Holly, not to Doug and John's
relationship.

### Batch 3: the call about Holly's body and its aftermath (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn was found word for
word, and raw lines 5587-5646 are fully covered by the stored turns. The
only defect in range is REGGIE's split line at scene175_beat2 turn 17
(finding 7, already logged), which is not DOUG's.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene175_beat2 | throughline_evolution (trait 2, escalation vs. scene56_beat1) | **consistent** | log (777) |
| scene175_beat3 | no draft (claimed trait 2 continuation vs. 175_2) | **claim partly holds**: the offer is real and consistent with trait 2; "yielding" is unsupported | review notes only; no field to correct |
| scene177_beat1 | throughline_evolution (trait 4, continuation vs. 175_3) | **consistent** | log (778) |

**scene175_beat2, consistent (author-confirmed).**
- **What the beat is.** Doug relays devastating news: "John. They they
  found Holly's body." (5598); "Washed up on the bay this morning."
  (5606); "I'm sorry, John. We really tried." (5612). Any competent,
  decent officer would do the same. It is ordinary decency suited to the
  situation, not trait 2's personal gentleness reaching a new,
  higher-stakes expression.
- **On "official channels".** The author called this relaying the news
  through official channels. The page shows a call to John's cell and the
  plural "We". It does not say whether the call is official or personal.
- **8b support.**
  - "We really tried" is about the search effort (settled in Batch 2), not
    a reading of John's emotional state.
  - Doug shows no awareness of John's situation. The call rings in a dead
    man's pocket: "A phone rings... In Reggie's pocket. John's ringtone."
    (5587). That is not attentiveness calibrated to John.

**Distinction to carry forward (author-confirmed): decency vs.
distinctiveness.** Behaving with basic human decency appropriate to a
situation is not the same as showing a personally distinctive trait.
Scoring ordinary, appropriate conduct as a character escalation inflates
basic decency into something exceptional, and undersells what genuine
distinctiveness looks like. Apply this test to later beats where a
character does the obviously decent thing under hard circumstances.

**scene175_beat3, no draft: the claimed turning point partly holds
(author-confirmed). Corrected, not fully rejected.**
- **The offer: supported as a high-confidence inference from the
  dialogue.** "Offers to take on the burden of telling Cheyenne himself."
  Doug's "No. I was gonna--" (5618) directly answers John's "Does
  Cheyenne--" (5615). It is consistent with trait 2: the same established
  protective gentleness, extended to this particular burden, not a new
  escalation.
- **"Before yielding to John's insistence": not supported.** It asserts a
  specific event, Doug accepting being overruled, that the page never
  shows. Doug is cut off mid-sentence by "Don't... Let me do it." (5621),
  with no narrated reaction. It is an invented emotional beat and should
  not be cited as evidence of anything.
- **Two record notes on the instruction.**
  - It cited "this project's standing rule that inference may complete
    what's clearly implied by the text". No such rule exists in the repo.
    The nearest rule points the other way: Pass 2's "depict, don't infer"
    instruction for trait labels (`pass2_orchestration.py`). The only
    formal home for inference is the `high_confidence_inferred` flag on
    linkages. The offer is recorded here as a high-confidence inference on
    its own merits.
  - It said Doug shoulders this "on top of everything else Doug's been
    through that day". That isn't on the page. Between "The alarm clock
    goes off. Doug stirs." (5188) and the call (5591), Doug does not
    appear.

**scene177_beat1, consistent (author-confirmed, 8b).**
- **Trait 4 doesn't apply.** Its content at scene57_beat3 is physical
  restraint of another person: "Trudy goes after John. Doug stops her."
  (1867). This beat shows the literal opposite: "Doug gets out of his
  cruiser but stays behind, watching." (5646).
- **The resolver's wording isn't trait 4 either.** Its "deference to
  John's wishes" isn't trait 4's content. Its comparison beat,
  scene175_beat3, carries a trait-2 claim and has no draft.
- **What the beat is.** Ordinary professional conduct: an officer staying
  back to give space during a personal notification. Nothing in Doug's
  established pattern makes it a dramatically significant crossing, so it
  is not a fresh boundary either.

**Principle 11: no candidates in this batch.** Doug's acts are the call
and the news (5598, 5606), a statement of regret (5612), an unfinished
offer cut off by John (5618), and following John in the cruiser, then
staying back (5642-5646).

This is the **third clean negative result in a row** for DOUG (Batches
1-3). **Pattern, provisional (CONFIRMED after Batch 4; see below):** DOUG may simply have no point-of-no-return
moment anywhere in his arc. That would be an honest finding about the
character, not an open question to keep searching for. It covers 3 of 4
batches. Batch 4 (scene197_beat2, scene199_beat1, scene207_beat1) carries
the queue's three boundary_revealed drafts and is still unreviewed.
Confirm or revise this pattern after Batch 4.

### Batch 4: the composure-break chain (2026-10-02)

Material comes from a fresh `pdftotext -layout -enc UTF-8` pull,
byte-identical to `fog_full.txt`. Every stored turn was found word for
word, and raw spans 5974-5987, 6003-6029 and 6247-6256 are fully covered
by the stored turns. No defects. Doug is not on the page in scenes
200-206, the Raymond interrogation.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene197_beat2 | boundary_revealed (trait 7 vs. scene123_beat14; finding 17 auto-heal) | **consistent**: first showing of a new trait | log (779) |
| scene199_beat1 | boundary_revealed (continuation of 197_2) | **consistent** | log (780) |
| scene207_beat1 | boundary_revealed (continuation of 199_1) | **consistent** | log (781) |

**scene197_beat2, consistent (author-confirmed, Principle 8b +
trait-identity gate).**
- **Trait 7's established content.** Composure under *personal insult*
  aimed at Doug, or at Doug and Mackie together:
  - "It's a bullshit report, man. And you know it." (2805-2806,
    scene86_beat3, private)
  - "too dumb of a cop" / "Doug is stung. But he takes the high road--"
    (4204-4207, scene123_beat14, public)
- **This beat has no insult to Doug.** He places the call himself: "Doug's
  voice is shaky, nervous--" (5980); "Yeah... Um, look, John... (clears
  throat) Uh... Do you, uh... Have you seen Trudy?" (5983-5987). The cause
  is accusations against Trudy: "He just started spewing all this shit
  about Trudy." (6007-6008, scene199_beat1).
- **Two different capacities.** "Composure under attack on myself" and
  "anxiety when someone I love is implicated" are categorically
  different. They are not the same capacity at different intensities;
  they only share Doug's emotional state.
- **The verdict.** This is the first showing of a trait the synthesis
  never tracked: **protective anxiety for Trudy**, set off by a threat to
  her, not to himself. Under the trait-identity gate a first showing is
  `consistent`. It is neither a boundary of trait 7 nor an escalation of
  it.
- **Scope note on the instruction.** It described an interrogation
  "Doug isn't even present for". The interrogation scenes shown (201-206)
  don't include him. But his own line, "He just started spewing all this
  shit about Trudy." (6007-6008), implies he heard Raymond, or was told,
  off-screen.
- **"For the first time Doug's composure visibly cracks" is literally
  false, even apart from trait identity.** Doug shows visible agitation
  earlier:
  - "Shit. Shit-fuck-shit." (3277, scene101_beat1)
  - "He looks around, worried." (3594-3595, scene118_beat1)
  - "Doug, frustrated--" (4137, scene123_beat4)

  None of these responds to a personal insult. The claim conflated
  "first crack under insult", which would be real if this beat involved
  an insult, with "first crack at all", which is false.

**scene199_beat1 and scene207_beat1, consistent (author-confirmed).** With
scene197_beat2 reclassified as the origin of protective anxiety for Trudy,
both beats are simple continuations of that trait, not of trait 7. Neither
adds a new facet:
- **scene199_beat1: the same state, intensifying in outward form.** "An
  upset Doug paces outside Interview Room Two." (6003); "Why would he say
  that, John?" (6008-6009); "Why would he say those things?" (6015); "But,
  John--" (6023).
- **scene207_beat1: the same state, unresolved.** Doug is still trying to
  connect while brushed off: "A rattled Doug approaches with coffee."
  (6247-6248), after "Get a coffee, Doug. Go." (6026); "... John?"
  (6251); John: "Relax, Doug. Everything's fine." (6256).
- **Finding 18.** This is finding 18's inheritance pattern:
  boundary_revealed passed down a continuation chain without being
  retested against its origin. It is corrected here by tracing the chain
  back to its properly identified root.

**Principle 11: CONFIRMED, no point-of-no-return instance for DOUG.**
- **Why this batch was the test.** It was the strongest candidate, holding
  all three of DOUG's boundary_revealed drafts, and it still gives a clean
  negative.
- **Every Doug statement in the batch** is a question, an interrupted
  protest or passive compliance: "Have you seen Trudy?" (5986-5987); "Why
  would he say that, John?" (6008-6009); "But, John--" (6023), cut off;
  "... John?" (6251). He leaves when told to (6028-6029) and comes back
  with the coffee (6248).
- **Across all four batches,** he makes no declaration and takes no
  unconditional action. This is recorded as a genuine finding about the
  character: Doug is a consistently supportive, reactive presence, never
  an agent of irreversible change himself. That is an honest fact about
  him, not a gap in the review.
- **Scope.** This covers the 12 queued entries, which run to scene207_beat1,
  Doug's last appearance on the page. After that he is only referred to
  (TRUDY: "How much does Doug know?", 6373).

### DOUG's Pass 2 queue is closed (2026-10-02)

All 12 entries have been reviewed: 11 `needs_correction_review` and 1
`arc_claim_check_no_draft`.

| Beat | Draft | Final | Record |
|---|---|---|---|
| scene101_beat1 | throughline_evolution (f17) | throughline_evolution | no-op. "Unasked" corrected; claim (b) trait 4 does not hold (notes) |
| scene118_beat1 | throughline_evolution | throughline_evolution | no-op |
| scene123_beat7 | throughline_evolution | throughline_evolution | no-op. Cigarette and cut-off line corrected |
| scene123_beat9 | throughline_evolution | consistent | 776 |
| scene123_beat14 | throughline_evolution | throughline_evolution | no-op. Severity, not witnessing |
| scene123_beat15 | throughline_evolution | throughline_evolution | no-op. Re-anchored as an echo of scene123_beat9 |
| scene175_beat2 | throughline_evolution | consistent | 777 |
| scene175_beat3 | no draft | claim partly holds (offer inferred; "yielding" unsupported) | notes |
| scene177_beat1 | throughline_evolution | consistent | 778 |
| scene197_beat2 | boundary_revealed (f17) | consistent | 779 |
| scene199_beat1 | boundary_revealed | consistent | 780 |
| scene207_beat1 | boundary_revealed | consistent | 781 |

**Totals.**
- The 11 drafted entries go from 8 throughline_evolution and 3
  boundary_revealed to **5 throughline_evolution, 6 consistent and 0
  boundary_revealed**. All three boundary_revealed drafts were
  overturned.
- **6 DOUG Pass 2 log entries** (776-781), 5 no-op confirmations, and 1
  no-draft claim recorded in the notes.
- Corrections log total: 781.

**Trait threads corrected or identified during this review (synthesis
file untouched; this file overrides it for DOUG):**
- **The diagnosis-into-pity echo (scene123_beat9 -> scene123_beat15).**
  Doug's tentative diagnosis ("that's making you not see things so
  clearly", 4166-4167) is restated as flat pity ("I feel sorry for you,
  John.", 4210-4211). As decided in Batch 2, this is a two-beat **echo
  inside the trait-2 thread** that scene123_beat7 escalated, not a new
  standalone trait. It replaces scene123_beat15's trait-3 anchor.
- **Protective anxiety for Trudy (new trait, origin scene197_beat2).** It
  is set off by a threat to her, not to himself, and is categorically
  distinct from trait 7. Its continuations are scene199_beat1 and
  scene207_beat1.
- **Traits 3 and 4 hold no queued turning point any more.** Trait 3's only
  claim (123_15) moved to the echo above. Trait 4's two claims (101_1(b),
  177_1) fail under 8b.

**Carried forward:** the decency-vs-distinctiveness test (Batch 3).

