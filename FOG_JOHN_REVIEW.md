# Full of Grace -- JOHN archetype review record

Per-character review record for JOHN's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether JOHN's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each JOHN verdict, including confirmations that
change no data. Same convention as `OCEANS11_DANNY_REVIEW.md`.

**Status column:** `pending apply` means the verdict is decided here but
the tagged data file has not been changed yet. `applied` means the change
has landed (`git log` on this file gives the commit). Confirmations that
change no data are also marked `applied`. They get no corrections-log
entry, per the no-op convention, and the beat's provenance is set to
`llm_human_confirmed`.

Scope: JOHN's 27 real-archetype beats in the cold output (2026-09-26
enumeration). Every tag was model output that nobody had reviewed.
`scene77_beat1` and `scene206_beat1` came from the post-fix re-run
(`FOG_COLD_RUN_FINDINGS.md` finding 3), not the pure cold pass.

## Chunk 1: scene14_beat4 - scene77_beat1 (2026-09-26)

Each beat was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
which is byte-identical to `fog_full.txt`, with all stored turns found
verbatim. scene40 and scene76-78 were also printed in full for context.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene14_beat4 | Chorus (confirmed) | A generalized verdict on the neighborhood's culture of silence, not a reaction to personal stake in this specific case. | applied |
| scene19_beat1 | Mentor (confirmed) | Real transmitted skill to a present mentee; the wager is open and consented to (NEGOTIATION/PRESSURE, not Trickster). | applied |
| scene19_beat2 | Mentor (confirmed) | Same basis, continued. | applied |
| scene40_beat3 | Great Mother (confirmed) | Unhedged depicted comfort, a real pivot from his prior prickliness right at the moment Trudy breaks -- author-confirmed as clean fit. | applied |
| scene55_beat1 | Mentor (confirmed archetype), fields corrected | self_perceived/audience_perceived rewritten to drop the invented alienation/seeking-connection framing -- nothing in the text draws that causal line. Grounded in only what's shown: teaching a curveball to two present people. | applied |
| scene57_beat1 | ordinary_reaction, Persona removed | Author-confirmed: John is genuinely simmering (not concealed), Trudy is genuinely trying to stay calm (not fooled) -- no gap between felt and shown. self_perceived, audience_perceived and goal rewritten; goal_status already deferred. | applied |
| scene77_beat1 | ordinary_reaction, Persona removed | Author-confirmed: top of one continuous phone call spanning scenes 76-78, where the visuals aren't synchronized with the dialogue -- John is genuinely torn and calling Angie for advice, working up to the real question in the next beat. "I'm not home right now" is distracted preoccupation, not concealment; no unaware mark for Trickster either. self_perceived, audience_perceived and goal rewritten; goal_status achieved -> deferred. Post-fix re-run beat. | applied |

**Chunk 1 follow-up field fixes (2026-09-26):** emotion fields that still
carried the removed framing were corrected, each logged as a follow-up to
its beat's verdict. scene55_beat1: emotion -> warm, focused, connecting;
goal now names both people present (elderly man and little boy).
scene57_beat1: "suppressed anger" -> irritated, tense (open, not
concealed). scene77_beat1: guarded, evasive -> distracted, unsettled,
preoccupied ("hurried" kept). scene77_beat1's weight_proportionality
(`matched`) is left as stored and handled under finding 4 in
`FOG_COLD_RUN_FINDINGS.md`.

**Context note, scenes 76-78:** these form one continuous phone call
between John and Angie that is not synchronized with the visuals: Angie
on her balcony (76), John packing in the motel (77), John driving past
the airport exit (78). That matters for reading scene78_beat1/2 too
("Ang... how does a person know if they're doing the right thing?" / "I
gotta know, Ang."), though neither carries a real archetype tag at
present. The author acknowledges that the staggered visuals-vs-dialogue
structure across scenes 76-78 is somewhat unclear on the page, which
likely contributed to the model's misreading here: Trickster in the cold
response, Persona in the post-fix re-run (both in `fog_tagging_calls.jsonl`).

## Chunk 2: scene95_beat1 - scene119_beat7 (2026-09-27)

Each beat was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
again byte-identical to `fog_full.txt`, with all stored turns found
verbatim. Plot facts used in the reasoning were checked in the same
pull: Dover is the town, and Doug says Mackie was "Consulting on the
Holly Roberts case" ("your dad's progress"), fog_full.txt lines 1745-1764.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene95_beat1 | Persona (confirmed), reasoning corrected and fields rewritten | Reggie frames Dover and Mackie's legacy as still John's; John flatly denies any personal stake. Asking about his father's involvement is ordinary procedure (Mackie was investigating the case), not itself evidence -- the tell is the quiet, weighted way John receives Reggie's answer, which reads as more than the indifference he's claiming. self_perceived, audience_perceived and goal rewritten; goal_status stays achieved. | applied |
| scene103_beat1 | Trickster (confirmed) | One continuous undercover operation ("Mr. Matthews") actively maintained across scene103_beat1, scene104_beat2 and scene105_beat1 -- Sheldon Wills-shape re-tagging, not repetition of a settled act. | applied |
| scene104_beat2 | Trickster (confirmed) | Same basis, continued. | applied |
| scene105_beat1 | Trickster (confirmed) | Same basis, continued. | applied |
| scene119_beat2 | ordinary_reaction, Shadow removed | Author-confirmed: a deliberate interrogation tactic, not something surfacing despite John's control -- fails Shadow's despite-control test. Also fails Trickster's unaware-mark test (NEGOTIATION/PRESSURE clause): Ricardo is fully aware he's being pressured. self_perceived, audience_perceived and emotion rewritten; goal and goal_status unchanged. Beat's `characters_present` is empty because of a parsing speaker-loss (`FOG_COLD_RUN_FINDINGS.md` finding 5). | applied |
| scene119_beat7 | Shadow (confirmed) | Doug's witnessed reaction ("concerned at John's temper") is real textual evidence of a break from controlled composure, not just an inferred one. | applied |

`scene206_beat1`, the other post-fix re-run beat, is not in this chunk.
Next JOHN beat is scene123_beat13.

## Chunk 3: scene123_beat13 - scene170_beat1 (2026-09-27)

Each beat was checked against a fresh `pdftotext -layout -enc UTF-8` pull,
again byte-identical to `fog_full.txt`, with all stored turns found
verbatim. scene154_beat2 carries no real archetype tag (JOHN was
`no_confident_archetype`) but is reviewed here with scene154_beat3 because
the same plot fact decides both.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene123_beat13 | Shadow (confirmed) | Witnessed public loss of composure (passing officers watch); incoherent, undirected rant; goal violated, not a tactic. | applied |
| scene138_beat2 | Shadow (confirmed) | Text names the displacement directly ("in frustration. At so many things"); genuine escalation past proportionate reaction to the stated task. | applied |
| scene152_beat1 | Shadow (confirmed) | Author-confirmed, one continuous encounter with scene154_beat1: John crosses from investigative pressure into physical restraint and coercion against Cheyenne's explicit resistance ("I swear I'll scream 'rape'"), pressing forward rather than backing off -- a genuine crossing of a line, not a deliberate interrogation tactic (distinct from scene119_beat2's correction). No field changes. | applied |
| scene154_beat1 | Shadow (confirmed) | Same basis, continued. No field changes. | applied |
| scene154_beat2 | ordinary_reaction (was no_confident_archetype) | Author-confirmed plot fact: Cheyenne and O'Shea are in collusion, so disarming O'Shea is self-preservation, not protection of another -- fails the for-another test regardless of how decisive the act is. No deception, so not Trickster. Kind changed only; stored fields already describe self-defense. | applied |
| scene154_beat3 | ordinary_reaction, Hero removed | Same plot fact and basis. self_perceived, audience_perceived, goal and emotion rewritten to decisive self-preservation under a threat that was real to him, not protection of the group ("protective resolve" dropped). goal_status stays deferred. | applied |
| scene166_beat2 | Hero (confirmed) | Real physical risk-taking, genuinely for another person, action actually taken. | applied |
| scene170_beat1 | Hero (confirmed) | Same basis -- real unknown danger entered alone, genuine for-another orientation. | applied |

**Observed, not acted on:** in scene154_beat2 the gun line is cued
`HISPANIC (O.S.)`, and the very next line is Cheyenne's "O'Shea. Baby.
Don't." John then "disarms O'Shea of his weapon". `per_character` stores
HISPANIC (functional_role_only) and O'SHEA as separate characters.
CHEYENNE's own tag on the beat (Persona, "protecting John from the
violence around her") was not reviewed against the collusion fact.

Next JOHN beat is scene172_beat2.

**O'SHEA identity merge (2026-09-27, `FOG_COLD_RUN_FINDINGS.md` finding
6):** HISPANIC and DRIVER relabelled to O'SHEA, author-confirmed.
Evidence differs by beat. scene153_beat1's own text names him ("The
driver is the Hispanic"), while scene151_beat1 rests on scene continuity
only (same unbroken car scene running into scene153; its text says
"unseen driver"). On scene154_beat2 the former HISPANIC and O'SHEA
entries are merged into one O'SHEA entry, synthesized across the beat's
arc: the armed threat succeeds (John releases Cheyenne), then the
dominance display fails once John disarms him. kind ordinary_reaction
(legible jealousy, aggression, humiliation rule out
no_confident_archetype and functional_role_only; no concealment, unaware
mark or composure break for a real archetype), goal_status violated.
**Provisional, pending O'SHEA's own character review.** The merge doesn't
change the scene154 reasoning above: the only armed man is Cheyenne's
partner, and the gun is on John.

**CHEYENNE note, scene154_beat2 (2026-09-27):** Persona ->
ordinary_reaction, author-confirmed. Her concealment of Mackie's
business is real, but it isn't depicted until a later beat in John's car
(scene155), so this beat doesn't carry it: per the plot-facts principle,
a later-confirmed fact can only correct an earlier beat's tag when that
earlier beat's own text already depicts the content. This beat shows
only her trying to calm her partner down mid-confrontation ("O'Shea.
Baby. Don't. He's a friend.", "O'Shea, stop.") -- an open, visible
de-escalation attempt, not a concealed one. self_perceived,
audience_perceived, goal and emotion rewritten ("guilt" and
"defensiveness" dropped). goal_status stays violated: O'Shea roughs John
up after her first plea, and the confrontation stops only because John
disarms him. Status: applied. CHEYENNE and O'SHEA are both now in the
review queue (`FOG_COLD_RUN_FINDINGS.md`). The scene155 car scene is a
strong candidate for a real Persona/Trickster tag for CHEYENNE.

## Chunk 4: scene172_beat2 - scene223_beat1 (2026-09-28)

These are the last 7 JOHN beats with a real archetype. The list was
rebuilt from `fog_tagged.json` (JOHN's non-empty archetypes, minus beats
that already have a row here). Only scene172_beat2 and beat8 of scene172
carry a JOHN tag. On beats 1 and 4-7 JOHN is no_confident_archetype, and
he has no entry on beat 3. Each beat was checked against a fresh
`pdftotext -layout -enc UTF-8` pull (byte-identical to `fog_full.txt`),
and every stored turn was found verbatim. All of scene172 (beats 1-8)
and scene204_beat1-scene205_beat1 were also printed for context. Every
quote below was checked against the same pull.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene172_beat2 | ordinary_reaction, Hero removed (revised in the chunk 4 follow-up); fields corrected | Author-confirmed: beat 2 is the argument ("El Vaquero is a man named Raymond Olsen. You got the wrong guy." / "Was that before you gouged his eye out or after?"), and declared intent is not the act. The Hero acts are in beats 3, 4, 6 and 7 (rows below; finding 10). The first chunk 4 verdict was Hero, on the basis "drawn gun on Reggie, standing between him and a tortured man". The text doesn't support that: John's rifle isn't raised until beat 3, and no line places him between Reggie and Alberto. That wording is also corrected in this beat's earlier corrections-log notes. The field fixes below are kept. The goal named Raymond Olsen as the harmed man, but John's own line says Olsen *is* El Vaquero and Reggie has "the wrong guy"; goal now names Alberto (deferred). "partner" removed from self_perceived and audience_perceived (finding 8). | applied |
| scene172_beat3 | Hero (new JOHN entry) | Author-confirmed: "John doesn't comply. He begins to slowly raise his rifle." He is protecting both himself and Alberto, so the for-another test passes (contrast scene154, where the only person protected was himself). The cold output had no JOHN entry, because characters_present is speaker-only (`['REGGIE']`, FUTURE_WORK item 1; no change). New fields: self_perceived "refusing to drop his rifle with a shotgun on him"; audience_perceived "a man holding his ground under threat, slowly raising his own weapon"; goal "keep Reggie from killing him or harming Alberto" (deferred); emotion tension, resolve; agency active; causal_integrity at the script's Pass 1 defaults. | applied |
| scene172_beat4 | Hero (was no_confident_archetype) | Author-confirmed: "John, rifle fully levelled at Reggie." Same arc and basis as beat 3. self_perceived, audience_perceived and goal rewritten; goal_status stays deferred; emotion left as stored (tense, urgent, defensive). | applied |
| scene172_beat6 | Hero (was no_confident_archetype) | Author-confirmed: John is again protecting himself and Alberto from Reggie. "John kicks the heavy furnace room door closed, shielding the Remington's spray of buckshot... Alberto screams. John stays composed. He pops out of the room and returns fire--". Real risk, action depicted, Alberto present. The schema's continuous-arc language ("subdue a threat, then approach to help ... even when an early step is also immediately self-defensive") covers an early step that is also self-defensive. self_perceived, audience_perceived and goal rewritten; goal_status (deferred) and emotion (adrenaline, alarm, grim determination) left as stored. | applied |
| scene172_beat7 | Hero (was no_confident_archetype) | Author-confirmed: John is showing care and concern for Alberto, as part of protecting him at great risk to himself. "A howl from Reggie. John ducks back into the room, glances to Alberto -- in his tortured state it's tough to tell if he's been hit." This is the "then approach to help" half of the continuous-arc clause. **It is the thinnest Hero beat in the arc and rests on that clause.** The author's account of care and concern gives meaning to an action already shown; it adds no new act. The archetype was changed first with the stored fields kept. Three fields were then corrected in a follow-up, because they asserted things beat 7 doesn't show. audience_perceived: "a controlled operator managing chaos" -> "a man checking on the tortured captive in the middle of a gunfight", and "quick protective concern for a bystander" -> "quick protective concern for Alberto". emotion: "controlled alertness" -> "alertness" (composure is narrated in beat 6, not beat 7). goal: "assess Alberto's condition and the immediate threat" -> "check whether Alberto has been hit" (deferred). self_perceived kept. | applied |
| scene172_beat8 | ordinary_reaction, Hero removed | Author-confirmed: John is chasing Reggie to apprehend him, which is pursuit of a suspect, not protection of another (fails the for-another test). No deception, so not Trickster. The stored fields rested on the invented "partner" relationship (finding 8). self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays deferred. Checked first: nothing in beats 3-7 contradicts pursuit. Reggie aims at John's head and fires, John returns fire, "A howl from Reggie", then a commotion upstairs and "A door being thrown open." characters_present is empty (FUTURE_WORK item 1); no change. | applied |
| scene185_beat2 | Persona (confirmed), one field corrected | Real on-page gap between what John knows and what he shows ("Knowing he'll keep the truth of his father's involvement forever a secret" against nodding at the Captain's praise). The motive is protective, so Persona and not Trickster. audience_perceived: "quiet grief masked as stoic acceptance" -> "outwardly accepting the praise while keeping his father's secret". This beat also carries finding 7 (MARCHAND's split line) and mentions Cheyenne and O'Shea in the action text, but neither is tagged here. | applied |
| scene206_beat1 | Persona (confirmed, author's call), fields corrected | Author-confirmed: "John's had enough" covers the whole situation, mainly Raymond's account of Trudy and the mishandled interrogation, and John wants to get to the bottom of Trudy's involvement. The Captain's "Let us handle Trudy" answers exactly that, so the earlier hold condition no longer applies. The tag rests on the unhedged narration "John's had enough", his attempt to leave, and his "I understand" against the Captain's order. It does NOT rest on the later beats where he searches for Trudy. The motive is personal and protective, so Persona and not Trickster. self_perceived, audience_perceived, goal ("get to the bottom of Trudy's involvement") and emotion (frustration, determination) replaced; goal_status stays violated because the Captain blocks him. Finding 9. Post-fix re-run beat. First held (see note below), then applied in the follow-up. | applied |
| scene213_beat1 | Mentor + Great Mother (author-confirmed, both tags) | Mentor rests on the closing guidance ("But the biggest sins were always the ones we were too afraid to admit"), aimed at a present, addressed mentee (Trudy, behind the confessional screen). Great Mother rests on the holding-space setup: he sits in the priest's chair and uses gentle humor and shared memory with a woman who is "all bottled up". No field changes: the stored fields already describe both functions. characters_present is only JOHN, although Trudy appears in the action text (FUTURE_WORK item 1); no change. | applied |
| scene217_beat1 | Great Mother (confirmed), not Hero; fields corrected | Author-confirmed: John gives his sister Trudy, who killed Holly (her confession is in the beat: "Maybe I held her under for too long"), a head start on the police, knowing she won't get far ("Soon all of New England's gonna be out looking for you. At least this way you get a chance to think."). The time is given as comfort, not as an escape plan, and he faces no danger on the page, so not Hero. self_perceived, audience_perceived and goal rewritten; goal_status stays achieved. | applied |
| scene223_beat1 | ordinary_reaction, Hero removed | Author-confirmed: John is about to tell Andy's parents that he is responsible for their son's death. The only thing he could be saving is himself (his own soul and spirit), which fails the for-another test even though it costs him. That confession comes from the author; the beat doesn't state it. Independently, the telling never happens on the page. The beat ends on "There's something I have to tell you," then THE END, and declared intent isn't the act. self_perceived, audience_perceived, goal and emotion rewritten; "young" dropped because his introduction gives his age as 41 (`fog_full.txt` line 305). goal_status stays deferred. | applied |

**scene213_beat1 co-tag note:** this is the first Mentor + Great Mother
co-tag in Full of Grace. The schema has no explicit ruling on this
pairing. Its co-tag language covers Mentor with Trickster/Shadow ("tag
both when both are earned") and Mentor with Chorus. **Watch item:** Great
Mother is already the most-tagged archetype in the script, with 27
entries after this change (Shadow 14 is next).

**scene206_beat1 hold (step-2 check):** the planned change was Persona,
confirmed narrowly on the gap between the unhedged narration "John's had
enough" and his compliant "I understand". The condition for applying it
was that "had enough" not clearly refer to something unrelated to
John's stance toward the Captain's order. The context pull found:

- **"him" / "had enough":** scene205_beat1 (INT. INTERROGATION ROOM)
  ends "Raymond starts to thrash his head against the metal tabletop.
  Over and over. Blood comes out." / DR. SHEPHARD: "Raymond!" / "Officers
  subdue him. It's chaos." So "him" is Raymond. scene206 (INT.
  OBSERVATION ROOM, where John and the Captain have been watching the
  interrogation since scene200) opens "John's had enough. He goes to
  leave. Captain stops him." The narration comes right after the
  interrogation chaos and *before* the Captain gives any order. What
  John has had enough of is the interrogation he has been watching, not
  the order, which doesn't yet exist when the line lands. He does try to
  leave, and that is what prompts the order.
- **Suspicion of Trudy before this beat:** no line states or narrates it.
  The closest lines are: Doug on the phone, "Have you seen Trudy?"
  (scene197). Doug again: "He just started spewing all this shit about
  Trudy. Why would he say that, John?", to which John answers "I don't
  know. But just -- we'll figure it out." (scene199_beat1). The
  interrogator: "Yeah, we know Trudy was helping you, Raymond." Raymond:
  "I gave Holly back to Trudy." Then "WITH JOHN / Stunned." Asked "Do you
  believe that what he claims holds any validity?", "John is quiet,
  struggles genuinely for an answer." (scene202).

The narration refers to the interrogation, not the order, so I held the
change rather than apply it and reported back for an author decision.

**Update (chunk 4 follow-up, 2026-09-28): hold lifted, applied.** The
author confirmed that "had enough" covers the whole situation and that
John wants to get to the bottom of Trudy's involvement (row above).
Pre-beat context, recorded here but not used to gate the change: in
scene202_beat1 (INT. OBSERVATION ROOM), John answers the Captain's "I'm
gonna assume you know nothing about any of this." with "Of course." To
"Do you believe that what he claims holds any validity?" he says
nothing: "John is quiet, struggles genuinely for an answer." The exchange
is then cut off by the lawyer's entrance ("Suddenly, a man in a suit
enters the Interrogation Room, followed by a woman."). Earlier, in
scene201_beat2, Raymond's "No. What? No... I gave her back. I gave Holly
back to Trudy. Everything was OK." is followed by the direction "WITH
JOHN / Stunned." (both stored as action turns).

**Supporting pre-beat context, not the basis of the tag:** scene201_beat2
(Raymond: "I gave Holly back to Trudy" / "WITH JOHN" / "Stunned.") and
scene202_beat1 (Captain: "I'm gonna assume you know nothing about any of
this." John: "Of course.") show what John has just heard and been asked
before scene206_beat1. The Persona tag rests only on scene206_beat1's own
text: "John's had enough", his attempt to leave, and "I understand"
against the Captain's order. John's "Of course" can be read as honest, and
it isn't treated as concealment.

**scene172 beats 1 and 5:** left as stored (no_confident_archetype).
Beat 1 (the 911 attempt, then hands raised) and beat 5 (talk) are
untagged, and the author hasn't ruled otherwise.

**Doug wording (scene101_beat1, scene199_beat1):** JOHN's
audience_perceived said "partner" for Doug. It now names him ("dismissing
Doug's legitimate warnings", "managing Doug's emotional outburst"). This
is a wording change only; both stay no_confident_archetype, and neither
is a real-archetype beat. `fog_full.txt` never uses "partner". Author-confirmed
context: Doug is a Dover PD officer in a relationship with Trudy. He and
John are both working the Holly Roberts case, but they are not official
partners. **For TRUDY's review:** Doug is her partner in the romantic sense.

JOHN's archetype review is complete. Every JOHN beat with a real
archetype has a row.

## Pass 2 review: JOHN's queue (2026-09-30)

**Scope.** JOHN has 22 entries in `fog_pass2_queue.json`, recounted from the
file. All 22 are `needs_correction_review`, with none in
`arc_claim_check_no_draft`: 4 boundary_revealed and 18 throughline_evolution.
Five are finding 17 entries: scene103_beat1 (the confirmed leak), plus
scene108_beat1, scene138_beat2, scene175_beat1 and scene213_beat3 (healed).
Six have no synthesis turning point at all (119_6/7/8, 154_1, 164_1, 165_1);
they exist only because the resolver declared them "continuation of X" in
free text (finding 18). The confirmation convention matches TRUDY's: a
confirmation gets no corrections-log entry (no-op convention), and this file
is the per-character record.

**Batches**, grouped by narrative sequence:

| Batch | Sequence | Entries |
|---|---|---|
| 1 | Woodworks infiltration, shop-floor chase, Ricardo interrogation | scene103_beat1, scene108_beat1, scene119_beat3, scene119_beat6, scene119_beat7, scene119_beat8 |
| 2 | Cheyenne/O'Shea coercion | scene152_beat1, scene154_beat1, scene155_beat1 |
| 3 | Armed cabin break-in, Reggie gunfight, "Let me make a call" | scene163_beat1, scene164_beat1, scene165_beat1, scene172_beat6, scene172_beat7, scene175_beat1 |
| 4 | Willful-blindness chain | scene185_beat2, scene217_beat1, scene217_beat2, scene218_beat1, scene223_beat1 |
| 5 | Individual first-crack boundary claims | scene138_beat2, scene213_beat3 |

**Outside the queue, checked for finding 20:** scene123_beat13 and
scene155_beat9 each carry a finding 20 split, and both were drafted
`matched`/`consistent`. Neither rationale depends on the split-off line, so
both stand (details in `FOG_COLD_RUN_FINDINGS.md` finding 20, 2026-09-30
update). scene115_beat1 is a synthesis turning point (continuation of
scene108_beat1) that was drafted `consistent` and so isn't queued. It is
scene163_beat1's comparison beat.

### Batch 1: scene103_beat1 - scene119_beat8

Every beat was checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). Every stored turn was found verbatim,
and a reverse check (PDF to stored) found no missing lines. Scenes 101, 107
and 118-119 were printed for context. All values are
characterization_consistency. weight_proportionality is unchanged
throughout: `matched`, except scene108_beat1, which stays `mismatch` (see
below).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene103_beat1 | throughline_evolution | consistent | log: continuation, not escalation. Going undercover as "Mr. Matthews" executes the decision John already made in scene101_beat1 (hanging up on "don't go to Biddeford"). The resolver's own rationale says "direct, unbroken execution... extending the trait via continuation". Finding 17's confirmed leak: scene101_beat1 is the trait's first-shown beat, not a turning point, so the chain had no sound foundation anyway |
| scene108_beat1 | boundary_revealed | consistent | log: John never registers the woman or her disability ("doesn't stop, bumps her hard but keeps running"). The Down's Syndrome detail is narrated after the collision ("We see..."), for the reader and the co-workers. This is a physical consequence of momentum inside the established pursuit; with no awareness on his part, nothing about his values or limits is exposed |
| scene119_beat3 | throughline_evolution | **throughline_evolution, confirmed** | no log entry (no-op convention); provenance `llm_unreviewed` -> `llm_human_confirmed`. A clean escalation: the consent-based wager with the Latino Kid (scene19_beat1: "if he can't hit it, you tell me everything you know") becomes institutional coercion against a frightened adult ("Now, I'm calling ICE unless you tell me what you know."). The same persuasion-through-leverage capacity, genuinely more severe |
| scene119_beat6 | throughline_evolution | consistent | log: the same unbroken interrogation as beat3; the resolver's own "unbroken continuation... without a new independent jump" |
| scene119_beat7 | throughline_evolution | consistent | log: the same unbroken interrogation; John crosses no new threshold. See the open item below on Doug's reaction |
| scene119_beat8 | throughline_evolution | consistent | log: same basis as beat6/7 ("still unbroken"); the silent stare-down adds no new content |

**Result:** of 6 entries, **1 throughline_evolution** (scene119_beat3) and
**5 consistent**, with 5 new corrections-log entries (742 total). The
escalation in this sequence is recorded once, at its source beat. Inherited
continuations are not re-stamped (finding 18's pattern again: 4 of the 6
drafts were continuation re-claims).

**Left as drafted, not addressed:** scene108_beat1's weight_proportionality
is still `mismatch`. The resolver's basis was "the disregard for the injured
woman is disproportionate". The consistent verdict rests on John having no
awareness of her, which undercuts that basis. That needs its own decision.

**OPEN ITEM: scene119_beat7, Doug's reaction.** The author's reading is that
Doug's discomfort is about exposure risk, because the interrogation is
unsanctioned: scene118 says "a room that certainly isn't any official
interrogation room. He looks around, worried."; here "He takes a quick peek
out the door window". On that reading, Doug's discomfort is not evidence of
John's temper cracking. The verdict above doesn't depend on this, since it
rests on continuation. But the action line itself reads "Doug shifts
uncomfortably, concerned at John's temper." (`fog_full.txt` line 3688), and
two things rest on the opposite reading:
- the chunk 2 archetype row for this beat, **Shadow (confirmed)**, whose
  stated basis is "Doug's witnessed reaction ('concerned at John's temper')
  is real textual evidence of a break from controlled composure". The tag is
  left untouched.
- the scene123_beat13 / scene138_beat2 baseline contradiction
  (`FOG_COLD_RUN_FINDINGS.md` finding 20, 2026-09-30 update). Does John's
  composure crack before scene138? This reading is not treated as settling
  any part of it.

Settle both together in batch 5.

**Refinement (2026-09-30, author-confirmed, note only, no data change):**
Doug's exposure worry and his concern at John's temper are not competing
explanations. They form one causal chain: John's temper flares, which makes
the interrogation louder and more volatile. That raises the risk of being
overheard, and the risk is specifically Captain Marchand finding out. The
script bears this out in the same scene, checked against a fresh
`pdftotext -layout` pull:
- DOUG (O.S.): "Oh, shit." / "John turns, sees Doug backing away from the
  door as it swings open and CAPTAIN MARCHAND enters." / "(to John, stern)
  You. Come with me." (`fog_full.txt` lines 3750-3764)
- in his office: "Arresting innocent individuals, dragging them across
  state lines, and accusing them of--" (lines 3814-3817)

So the beat's evidence supports both readings at once, and neither has to
be chosen over the other. If anything, this strengthens the case that
John's temper is genuinely visible and consequential here. That bears on
batch 5: the scene119_beat7 Shadow tag, whose basis this supports rather
than undercuts, and the scene123_beat13 / scene138_beat2 baseline
contradiction.

**Follow-up, scene108_beat1 weight_proportionality (2026-09-30):**
mismatch -> **matched**, author-confirmed and logged (743 entries). The
resolver's "disproportionate" call rested on "the disregard for the injured
woman", but John never perceives her, so there is no choice to weigh for
proportionality. The reaction being measured, an all-out sprint after a
fleeing suspect, is proportionate. The collision is incidental momentum.

**Knock-on for scene115_beat1 (not queued, drafted `matched`/`consistent`,
no change):** the synthesis turning point (continuation of scene108_beat1)
calls the tackle "the physical payoff of the collateral-harm-risking pursuit
begun in the prior beat". The resolver rejected it: "not a continuation of
the collateral-harm boundary revealed at scene108 -- no bystander is harmed
here, so it doesn't extend that specific revelation; it's simply success at
an already-established risk-taking capacity." Now that scene108_beat1 is
`consistent`, the scene108 boundary that rationale argues against no longer
exists. The rationale's other ground (an established capacity succeeding) is
the one that carries the verdict. scene115_beat1 is scene163_beat1's
comparison beat (batch 3).

### Batch 2: scene152_beat1 - scene155_beat1 (2026-09-30)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull.
All stored turns were found verbatim, and a reverse check (PDF to stored)
found no missing lines. The sequence runs continuously from scene149
(`fog_full.txt` lines 4790-4971).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene108_beat1 (WP, carried from batch 1) | mismatch | **matched** | log (743). John never perceives the bystander, so there is no choice to weigh; the sprint itself is proportionate. Dependency at scene115_beat1 resolved: that verdict (`consistent`) is unaffected. One of its two supporting reasons (arguing against the scene108 boundary) no longer applies, and the other ("success at an already-established risk-taking capacity") stands on its own. Detail in the batch 1 follow-up above |
| scene152_beat1 | throughline_evolution | **throughline_evolution, confirmed** | no log entry (no-op convention); provenance already `llm_human_confirmed`. The basis is the corrected comparison, escalation vs. **scene119_beat3** (not scene19_beat1): verbal/institutional coercion (the ICE threat) becomes physical coercion (pinning Cheyenne), the same interrogation capacity re-tested on a different person in a separate encounter. See the record corrections below |
| scene154_beat1 | throughline_evolution | **throughline_evolution, confirmed, with corrected reasoning** | no log entry (no-op convention); provenance already `llm_human_confirmed`. The value stands, but the resolver's justification ("a direct, unbroken continuation of the scene152_beat1 turning point", checked against "scene152_beat1 ... continuation") is replaced. See below |
| scene155_beat1 | throughline_evolution | **pending** | factual description corrected (below); verdict not yet decided, value unchanged |

**scene154_beat1, corrected reasoning (author-confirmed):** a continued
escalation of the same event vs. scene152_beat1, not a repetition and not a
flat continuation. John's line isn't de-escalating or pleading: "Know how
many of these cases I've worked? The chances of Holly just walking through
your front door... Jesus, Chey, go play the Powerball if you want better
odds." (`fog_full.txt` lines 4885-4890, checked this session). He is
weaponizing grim missing-child statistics to shock Cheyenne into grasping
the urgency, since the clock is running on Holly's survival. The method is
not new: "Cheyenne is practically pinned to the wall by John." (4883), the
same physical pin as scene152_beat1. What this beat adds is calculated
psychological pressure layered onto the physical coercion already in play.
The same interrogation-capacity throughline develops one notch further.
Comparison: **escalation vs. scene152_beat1**, replacing the resolver's
"continuation".

**Record corrections (resolver/synthesis metadata; no `fog_tagged.json`
field holds these, so there is no log entry. The saved `fog_pass2_calls/`
files stay as the cold record, per finding 17's convention):**

- **scene152_beat1, resolver checked_against: scene19_beat1 -> scene119_beat3.**
  The synthesis turning point already names scene119_beat3. Author-confirmed,
  this is a one-step escalation, not a two-step jump. Verbal/institutional
  coercion (the ICE threat against Ricardo, scene119_beat3) escalates into
  physical coercion (pinning Cheyenne). It is the same psychological thread,
  interrogating someone for vital case information, tested again on a
  different person. The scene gap doesn't break the throughline, because the
  capacity is re-tested in a separate encounter rather than continued in one
  unbroken act (contrast TRUDY scene214/216, one continuous physical act).
  The drafted type and verdict (throughline_evolution) are left as drafted,
  pending batch 2 review; only the comparison citation is corrected.
  - **Note:** John has no equivalent stake with Ricardo, whom he never
    touches (scene119 is all verbal: "John slaps the fake Social Security
    card onto the table"). That is part of why the same capacity shows up
    differently here: personal history intersecting with professional
    method, not escalation of method alone.
  - **What the script actually establishes about the history** (search
    2026-09-30, fresh pull; see below): a significant shared past is on the
    page. A *romantic* relationship is not. The synthesis/resolver wording
    "someone with intimate personal history" is supported in the sense of
    "close shared past", and the word "intimate" goes beyond the text if read
    as romantic. The resolver's instinct may be right about the romance
    without textual support. That is a smaller, separate problem from
    inventing a false detail, and romance is not cited as textual evidence
    here.
- **scene155_beat1, synthesis turning point `what_changes`: factual error.**
  It says "he disarms O'Shea and locks everyone in the car". The resolver
  repeats "disarming O'Shea's weapon and locking everyone in the car". The
  disarming happens in **scene154_beat2** ("In a flash, John disarms O'Shea
  of his weapon and has him on his knees about to snap his arm in half.",
  `fog_full.txt` lines 4943-4944). scene155_beat1 shows only the aftermath:
  "John ejects the clip from O'Shea's gun, empties the bullets into his
  hand, pockets them. He tosses the gun out the window into the snow." and
  "John auto-locks all the doors." (lines 4955-4962). This is corrected here
  whatever the beat's verdict turns out to be.

**John/Cheyenne history: what is on the page.** A search of the fresh pull
for YOUNG CHEYENNE and for past-relationship language (girlfriend,
boyfriend, sweetheart, dated, ex, "used to", "remember", "years ago",
"storied", and similar) found:
- **The only YOUNG JOHN + YOUNG CHEYENNE scene** is the boat flashback
  (EXT. GREAT BAY - MOTORBOAT, "22 YEARS AGO...", lines 1886-2001):
  - "YOUNG JOHN (19), ANDY (19), and two teen girls, one of them YOUNG
    CHEYENNE (African-American, pretty)" (1890-1892)
  - "Young Cheyenne sits close to a shirtless Young John." (1898)
  - "Cheyenne looks to John and smiles at him proudly." (1912-1913)
  - "John? I think you should slow down." (1984)
- **Adult reunion** (EXT. UNIT 305, lines 2021-2035): "She gives John a
  small, forgiving smile." / "They linger a moment in the doorway, holding
  each other's gaze. Studying one another. Revisiting a storied history as
  their expressions do the remembering for them." This is unhedged narration.
- **Other lines:** "This is John. The guy I told you about." (to O'Shea,
  4929-4930). "Cheyenne? Cheyenne's daughter is missing?" (stunned, when
  Doug tells him, 1771). "Jesus, Chey" (4889).
- **Not on the page:** no word for the nature of the relationship
  (girlfriend, ex, dated, sweethearts, together). Holly's father is PETE
  ("I'm her father!", 3990), not John.

**scene155_beat1, resolved (2026-09-30):** throughline_evolution ->
**consistent**, author-confirmed and logged (744). Tossing the
already-confiscated gun into the snow and "You can have it back when we're
finished." are one continuous act, not two. O'Shea's "What the fuck?!"
reacts to the toss, and John's line answers that reaction (after "John
auto-locks all the doors."), so "it" is the gun (`fog_full.txt` lines
4955-4966). This is withholding-as-leverage control, already established at
scene154_beat2: the disarming (4943-4944) and "Everyone get the fuck in my
car." (4947). Discarding the weapon into the snow rather than pocketing it
is a vivid execution of that established control pattern, not a new
capacity revealed. It is functionally the same move as scene154_beat2's
disarming and control assertion.

Location check: the author's instruction noted that the "have it back"
phrase might already appear at scene154_beat2. It doesn't. It appears only
in scene155_beat1 (stored turn 4), and the script reads "finished", not
"done".

**Batch 2 result (complete):**
- **2 throughline_evolution confirmed:** scene152_beat1 and scene154_beat1,
  both with corrected comparison records.
- **1 consistent:** scene155_beat1.
- **Plus the scene108_beat1 weight_proportionality fix** carried from
  batch 1, whose scene115_beat1 dependency is resolved.

This batch took 2 corrections-log entries (scene108_beat1 WP and
scene155_beat1), for 744 in total. The persuasion/extraction chain now reads:
scene19_beat1 (first shown) -> scene119_beat3 (escalation: institutional
coercion) -> scene152_beat1 (escalation: physical coercion) ->
scene154_beat1 (escalation: psychological pressure added to the pin).
scene155_beat1 is the consistent aftermath.

### Batch 3: scene163_beat1 - scene175_beat1 (2026-09-30)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). The sequence was printed continuously
from scene160 to scene176 (lines 5190-5638), with the comparison beat
scene115_beat1 (3554-3563). Every stored turn was found verbatim. The
reverse check (PDF to stored) found three split lines and one dropped
parenthetical, all in Reggie's speech in scene175. They are logged under
findings 7 and 20 in `FOG_COLD_RUN_FINDINGS.md`, and no verdict below
depends on them. weight_proportionality stays `matched` on all six.

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene163_beat1 | throughline_evolution | **throughline_evolution, confirmed, with corrected reasoning** | no log entry (no-op convention); provenance `llm_unreviewed` -> `llm_human_confirmed`. The basis is replaced; see below |
| scene164_beat1 | throughline_evolution | consistent | log: the same unbroken armed search. The resolver's own "Directly continues the break-in with no gap" describes no new content |
| scene165_beat1 | throughline_evolution | consistent | log: same basis. Archetype-layer note below |
| scene172_beat6 | throughline_evolution | **throughline_evolution, confirmed** | no log entry (no-op convention); provenance already `llm_human_corrected` (Hero tag). **Finding 19 instance 2**; see below |
| scene172_beat7 | throughline_evolution | consistent | log: the outcome of scene172_beat6's single shot, not a second act. The synthesis's "second exchange of shots" is corrected |
| scene175_beat1 | boundary_revealed | **boundary_revealed, confirmed, with corrected reasoning** | no log entry (no-op convention); provenance `llm_unreviewed` -> `llm_human_confirmed`. See below |

**scene163_beat1, corrected reasoning (author-confirmed).** This is not
breaking-and-entering, and not entry "on private property". The synthesis
and resolver both said it was. What the page shows:
- The cabin is John's. Their father's estate lawyer puts "the keys and deed
  to the cabin into a large envelope labelled 'John'" (2240-2241), and John
  later has "the cabin keys" (2484). Mackie is the father whose estate this
  is: Mackie's den has the gun cabinet with "A hunting rifle is missing"
  (5179-5182). John also says "This is my property." (5451).
- At the door, John tries his own key first: "He fishes the keys out of his
  pocket, sticks the key in the lock. Key won't turn... Brand new. Locks have
  been changed." (5206-5209). Only then does he boot the door in (5210).
- Reggie wanted the cabin: "Reggie's been trying to get dad to sell him the
  cabin." (2547-2548), plus Reggie's own pitch at 1554-1584, and "Reggie's
  newly-completed patio" (4255).

The author's reading is that Reggie changed the locks to keep John out,
effectively controlling access to John's own property, so forcing the door
means entering his own home after being locked out of it. Note: the page
says only "Locks have been changed". Who changed them, and why, is
inference from the above, strongly supported but not stated.

The genuine escalation: this is the first beat where John arms himself in
anticipation of a confrontation. He carries his dad's rifle (5202), and the
open box of ammunition with "Some shells missing" sits in his car
(scene161_beat1, 5197-5198). That is a real step beyond the unarmed
physical risk-taking of the rooftop chase and tackle (scene115_beat1). The
comparison (escalation vs. scene115_beat1) and the verdict stand. The
resolver's stated basis ("forcing open a locked door on private property...
premeditation") is replaced by this one. "Loading" the rifle is inferred
from the missing shells; loading isn't shown on the page.

**scene165_beat1, note for the archetype layer (not Pass 2, no change
here):** "He sees the bloody clothes, yet he remains cop-calm. But behind
the calm he's amped." (5224-5225) is a real gap between what is shown and
what is felt. Flag it for a possible Persona read if JOHN's beats are
reconsidered at that layer.

**scene172_beat6, confirmed, and finding 19 instance 2 (author-confirmed).**
Carrying a weapon for readiness becomes an actual lethal exchange of
gunfire. This is the first time the trait crosses into taking a life, a
genuine escalation-shaped turning point. It is also not an ambush John
merely reacted to. He came to the cabin looking for Reggie, already
suspecting him from what O'Shea and Cheyenne told him. O'Shea: "Except for
that old Army cat... Been hittin me up every couple days. And for serious
gear." Cheyenne: "It's Reggie, John." (5040-5051). Then O'Shea's text, "Army
cat just took more gear." (5235), and John calling "Reggie?" into the cabin
(5231). So the gunfight is the culmination of a pursuit John deliberately
started, which sharpens the escalation.

Point of no return: scene172_beat5's "Or I'll be forced to defend myself."
(5452-5453) is declared intent, fully reversible. scene172_beat6's "He pops
out of the room and returns fire--" (5494) is the irrevocable act. Later
text confirms the shot is fatal: "perforated by John's buckshot" (5527),
"Lungs collapsing from buckshot" (5550), and death at scene175_beat2
(5581-5582). The moral shape differs from TRUDY's instance 1
(scene214_beat4, corrupted caregiving turned lethal). Here, self-defense
escalates into an irreversible killing during a pursuit he chose to start.
Structurally it is the same pattern. Two unrelated characters with opposite
moral framings share it, which is stronger evidence that finding 19 is a
generalizable pattern than a quirk of one arc. **2 of the 3 instances**
needed before promotion to a numbered principle (recorded in
`FOG_COLD_RUN_FINDINGS.md` finding 19).

**scene172_beat7, corrected reasoning (author-confirmed).** The sequence
has two shots in total: Reggie's blast ("Reggie pulls the trigger", 5490)
and John's single return shot. John fires once. "He pops out of the room
and returns fire--" (end of beat 6) starts it. "BOOM! Another ear-splitter.
A howl from Reggie." (5496-5498, this beat) is that same shot landing and
taking effect, not a second, separate act. The synthesis's "a second
exchange of shots wounds Reggie" is corrected. This beat is the outcome of
the lethal shot already recorded as the turning point at scene172_beat6,
not a further escalation.

**scene175_beat1, confirmed, with corrected reasoning (author-confirmed).**
"Let me make a call." (5562) is not a vague offer. The author's reading:
John is asking Reggie to hand back his phone so he can call EMS for him.
Reggie took the phone at scene172_beat1 ("Reggie picks it up and pockets
it.", 5392), and it is still "In Reggie's pocket" at 5587. Reggie refuses:
"Reggie smiles, shakes his head 'no'." / "Nah..." (5564-5567). Note: the
page gives only the line and the phone's location. "Hand back the phone"
and "EMS" are the author's reading of it, not stated text.

This is not the scene172_beat1 instinct (John "goes to dial 911" for
Alberto, 5376-5377) simply recurring. It is a harder version of that
instinct, extended to the man who tried to kill him moments earlier rather
than to an innocent victim. The offer reveals the limit whether or not
Reggie accepts it: John's capacity for lethal force in self-defense
coexists with an intact instinct to preserve life, even his attacker's,
once the threat is down. The comparison (vs. scene172_beat7) and the value
stand.

**Record corrections (resolver/synthesis metadata; no `fog_tagged.json`
field holds these, so there is no log entry; the saved `fog_pass2_calls/`
files stay as the cold record):**
- scene163_beat1: "premeditated armed breaking-and-entering... forcing open
  a locked door on private property" -> entry into John's own cabin after
  the locks were changed on him. The escalation is arming for an expected
  confrontation.
- scene172_beat7: "a second exchange of shots wounds Reggie" -> John's single
  shot from beat 6 landing.
- scene175_beat1: the resolver's "exposing a previously unknown limit" is
  kept. The basis is sharpened to the instinct from scene172_beat1 now
  extended to his attacker, per the author's reading above.
- scene165_beat1: the resolver's checked_against mixes in a second trait
  ("maintains calm composure under pressure"). This is moot now that the
  beat is `consistent`.

**Batch 3 result:** 3 confirmed (scene163_beat1 throughline_evolution,
scene172_beat6 throughline_evolution, scene175_beat1 boundary_revealed) and
3 -> consistent (scene164_beat1, scene165_beat1, scene172_beat7), with 3 new
corrections-log entries (747 total). The armed-pursuit chain now reads:
scene115_beat1 (unarmed risk-taking, consistent) -> scene163_beat1
(escalation: arming for confrontation) -> scene172_beat6 (escalation:
lethal exchange, point of no return) -> scene175_beat1 (boundary: the
life-preserving limit). scene164_beat1, scene165_beat1 and scene172_beat7
are consistent continuations and outcome.

### Batch 4: scene185_beat2 - scene223_beat1, the willful-blindness chain (2026-09-30)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). Printed for context: scene14_beat4
(342-395), scenes 183-185 (5661-5790), scenes 216-223 (6535-6664), the Andy
boat flashback and cover-up (1976-1999, 2280-2364), and the scene213
confessional lines (6337-6360). Every stored turn was found verbatim. The
reverse check found one new blank-line split, on the comparison anchor
scene14_beat4 (finding 7, sixth occurrence), and no verdict depends on it.
weight_proportionality stays `matched` on all five. All five relate to the
trait "Holds to a personal philosophy that willful blindness ('see no evil,
hear no evil') is how people survive", first shown at scene14_beat4 ("See
no evil, hear no evil, and you will survive.", 392-393).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene185_beat2 | throughline_evolution | **throughline_evolution, confirmed, reasoning replaced** | no log entry (no-op convention); provenance already `llm_human_corrected` (Persona row). See below |
| scene217_beat1 | throughline_evolution | **throughline_evolution, confirmed** | no log entry (no-op convention); provenance already `llm_human_corrected` (Great Mother row). **Finding 19 instance 3**; see below |
| scene217_beat2 | throughline_evolution | consistent | log: "Goodbye, Tru." continues the choice already made in scene217_beat1 and adds nothing new |
| scene218_beat1 | throughline_evolution | consistent | log: mechanical follow-through; the key exchange at scene217_beat1 is the point of no return. See the note below on why this is logged |
| scene223_beat1 | throughline_evolution | consistent | log: the echo claim rests on two false premises. See below |

**scene185_beat2, reasoning replaced (author-confirmed).** Principle 2
analysis: this is John's first personal practice of the philosophy he
stated as an observation at scene14_beat4. It's the trait's genuine first
enactment, not the continuation of an earlier pattern. **scene95_beat1** was
considered and ruled out as an earlier instance. On the author's reading,
John's "John thinks for a moment. Nods. He turns and leaves. That's it. No
further questions." after "Matter of fact he did." is investigative
strategy: he deliberately doesn't press Reggie further, to keep him as a
source and warn him off. It is not avoidance of an uncomfortable truth.
(Its chunk 2 archetype row, Persona, rests on the weighted way John
receives the answer. That row is untouched.)

The synthesis/resolver basis ("at the cost of his integrity as a
detective", "secret from the Captain") is invented and is replaced
entirely. The author's basis: John's silence ("Knowing he'll keep the truth
of his father's involvement forever a secret.", 5785-5786) is a pragmatic
judgment that the truth no longer serves any purpose. Holly, Mackie and
Reggie are all dead: Holly's wake (5667), Reggie's urn (5682), and "Three
funerals in two weeks." (5698). The only suspect still being sought is
Raymond Olsen ("It's still an open case... But we'll find him.",
5751-5762). Disclosing Mackie's misconduct would tarnish a dead man's memory
and accomplish nothing for the investigation. This is willful blindness
practiced as reasoned pragmatism, not cowardice or careerism.

**scene217_beat1, confirmed (author-confirmed).** Two framings of this beat
are on record. The synthesis/resolver's legal framing is "obstruction". The
archetype layer's framing (chunk 4, Great Mother) is "time given as
comfort, not as an escape plan". These are not in tension: they are the
same act read from two honest vantage points. Legally it is obstruction,
and John knows it. Emotionally it is mercy, temporary and futile, since he
already knows she won't get far ("Soon all of New England's gonna be out
looking for you. At least this way you get a chance to think.",
6577-6579). The Great Mother motive is what makes John willing to cross
into knowing obstruction. That crossing is the actual escalation, from
scene185_beat2's passive omission to active, illegal complicity.
Comparison: escalation vs. scene185_beat2, as drafted.

**Finding 19, instance 3 (author-confirmed).** The key exchange is the act:
"Trudy realizes. She takes out her car keys. Her and John make the
exchange." (6582-6583). It is John's own irrevocable physical act, handing
a confessed killer ("Maybe I held her under for too long.", 6552-6555) a
vehicle and his own identity to escape with. Note: "his own identity" is
the author's reading. The page gives "Rental's due back at the airport in
the morning." (6586-6587), not whose name the rental is in. "Nothing. It's
between you and God now." (6593-6594) is declared intent; the exchange is
the act.

A point of no return does not require violence. This is knowing legal
obstruction chosen as an act of mercy. It differs in kind from TRUDY's
scene214_beat4 (corrupted caregiving turned lethal) and JOHN's own
scene172_beat6 (self-defense escalating into a chosen killing). The author
judges scene172_beat6 likely the bigger instance in dramatic weight, but
this is a genuine instance regardless. Three structurally identical
instances in three moral registers (corrupted devotion, violent
self-defense, merciful obstruction) strongly confirm finding 19 as a real,
generalizable pattern.

**OPEN ITEM: finding 19 -> numbered principle, in a dedicated session**
(logged in `FOG_COLD_RUN_FINDINGS.md` finding 19). It is to be proposed as a
numbered causal-integrity principle before FOG's Pass 2 review closes,
separately from routine batch work. Numbering and wording are not
finalized. Draft direction from the author: "an act can be a turning point
through irreversibility alone, even without violence or escalated
intensity -- the test is whether the character could undo or walk back
this specific action once taken, regardless of how calm or merciful the act
appears on the page." For that session: the three instances span two
characters (TRUDY, JOHN, JOHN), while finding 19's own status paragraph
asks for recurrence "in two more characters' reviews". Settle whether that
condition is met, or is superseded by the instance-count discipline.

**scene218_beat1, consistent (author-confirmed).** The drive-off is
meaningless in itself. John simply drives Trudy's car away while she has
the rental ("He unlocks it and climbs in. He starts it up and drives
away.", 6604-6605). It is mechanical follow-through of the decision made at
scene217_beat1 and adds nothing new. The author's instruction described
this as confirming an existing `consistent`, but the stored draft was
`throughline_evolution`. So this is a real value change, logged, not a
no-op. The synthesis's "to cover her escape" states a purpose the page
doesn't give.

**scene223_beat1, consistent (author-confirmed).** There are two
independent grounds, and either alone defeats the echo claim vs.
scene14_beat4:
1. **The confession never happens on the page.** The beat ends on declared
   intent: "Mr. Murphy, Mrs. Murphy... um... (pause, deep breath) There's
   something I have to tell you." (6658-6662), then THE END. Declared intent
   isn't the act. This matches the archetype-layer finding recorded when
   Hero was removed from this beat (chunk 4). The resolver's "John's own
   action -- voluntarily confessing the truth" describes something that
   isn't shown.
2. **"For the first time" is factually false.** John already told Trudy the
   full truth in the confessional, scene213_beat3: "I was piloting Andy's
   boat." (6346) and "I killed my best friend, Tru. And I never had to
   answer for it." (6359-6360). He also tried to confess as a boy: "Dad,
   it's okay. I'll say it was me." (2349).
   **Cross-reference corrected in batch 5:** this ground still holds, since
   John plainly disclosed the truth before scene223_beat1. But scene213_beat3
   is now recorded as `consistent`, the first showing of a separate
   reciprocal-honesty trait, not as a prior boundary_revealed instance. The
   batch 4 corrections-log note cites it only as the earlier disclosure, so
   it needs no change.

**Record corrections (resolver/synthesis metadata; no `fog_tagged.json`
field holds these, so there is no log entry; the saved `fog_pass2_calls/`
files stay as the cold record):**
- scene185_beat2: "at the cost of his integrity as a detective" / "secret
  from the Captain" -> pragmatic judgment that the truth serves no purpose,
  with every other party dead and Raymond Olsen the only open suspect.
- scene217_beat1: "actively enabling his living sister's escape... act of
  obstruction" is kept, with the mercy framing added as the motive for the
  obstruction. The two are the same act.
- scene218_beat1: "to cover her escape" is not on the page.
- scene223_beat1: "voluntarily confessing the truth about killing Andy to
  Andy's parents... for the first time" is wrong on both counts.

**Batch 4 result:** 2 confirmed throughline_evolution (scene185_beat2,
scene217_beat1) and 3 -> consistent (scene217_beat2, scene218_beat1,
scene223_beat1), with 3 new corrections-log entries (750 total). The
willful-blindness chain now reads: scene14_beat4 (first shown, as an
observation) -> scene185_beat2 (escalation: first personal practice, as
pragmatism) -> scene217_beat1 (escalation: knowing obstruction as mercy;
finding 19 instance 3). The other three beats are consistent.

Next: batch 5 (scene138_beat2, scene213_beat3), plus the open items carried
from batch 1: the scene123_beat13 / scene138_beat2 composure baseline and
the scene119_beat7 Shadow tag.

### Batch 5: scene138_beat2, scene213_beat3, and the composure baseline (2026-10-01)

Material was checked against a fresh `pdftotext -layout -enc UTF-8` pull
(byte-identical to `fog_full.txt`). Printed: scene119 (3657-3699),
scene123 (4150-4214), scene138 (4330-4391), scene213 (6309-6370), the
scene14 McAvoy/Sarge exchange (395-525) and both comparison beats,
scene13_beat1 and scene37_beat5. Every stored turn was found verbatim.
weight_proportionality stays `matched` on all three beats.

| Beat | Stored | Reviewed | Record |
|---|---|---|---|
| scene123_beat13 (outside the queue) | consistent | **consistent, confirmed, citation corrected** | no log entry (no-op convention); provenance already `llm_human_confirmed`. See below |
| scene138_beat2 | boundary_revealed | **boundary_revealed, confirmed, reasoning substantially corrected** | no log entry (no-op convention); provenance already `llm_human_confirmed`. See below |
| scene213_beat3 | boundary_revealed | **consistent** | log (751). See below |

**scene119_beat7's Shadow archetype tag is NOT changed or reopened.** It
stands as confirmed in chunk 2 and is now also used as supporting evidence
for scene123_beat13 below.

**scene123_beat13, citation corrected (author-confirmed).** The verdict
stands. The resolver's cited evidence, "already-established capacity for
volatile anger (e.g. with McAvoy, Sarge)", points at scene14 and is
imprecise. Those beats are crude interpersonal trash-talk ("Way ahead of
ya, ya fat fuck!", 479) and defiance over a demotion ("John's pissed. A
moment passes.", 513). That is not the same thing as professional
composure cracking under case pressure. The correct, closer antecedent is
**scene119_beat7**, one scene earlier: during the Ricardo interrogation,
"Doug shifts uncomfortably, concerned at John's temper." (3688). That beat
already establishes the capacity, so the public outburst at
scene123_beat13 ("Some passing officers stop. They watch John's
outburst.", 4198) is consistent with it.

**scene138_beat2, reasoning corrected (author-confirmed).** Two phrases are
dropped as factually false: the synthesis's "had never before cracked
on-screen" and the resolver's "a breaking point never before shown". By
scene138, John's composure has already cracked twice (scene119_beat7,
scene123_beat13). Both of those are reactive flares at specific people or
targets under immediate provocation.

The corrected basis: scene138_beat2 is not an escalation or continuation of
that reactive-anger pattern at all. It is a structurally independent event.
It has no proximate trigger and no target. He is alone on the dock, there
are no character cues, and `characters_present` is empty. "He screams out
in frustration. At so many things." (4378-4379). It is the cumulative
weight of everything finally exceeding what his composure can hold: the
case, Mackie's death, his own guilt, and his physical decline from the
athlete he was ("He howls. Grabs for his shoulder. The ball soars but falls
up short again. He's pulled a ligament.", 4375-4378). John would have
reached this collapse whether or not scene119_beat7 or scene123_beat13 had
happened. It doesn't depend on or escalate from that chain. What it
reveals is a genuinely different, previously untested limit: total
physical/emotional collapse under cumulative, unprocessed weight, with no
target and no proximate cause. The comparison against scene13_beat1 ("seems
calm, but with eyes always tense, anticipating"; "He barely reacts.") stays
correct. This beat was never measured against the interpersonal-anger
beats. weight_proportionality stays `matched`.

**scene213_beat3, boundary_revealed -> consistent (author-confirmed,
logged).** This is a correction, not a confirmation, on two independent
grounds.

1. **This is a different trait.** The synthesis checked the beat against
   "Reacts with clipped avoidance/denial when confronted about his
   baseball-playing past" (scene37_beat5: "Say, didja ever get back into
   playin' ball at all?" / "No."). This beat is not that trait reaching a
   breaking point. It is a separate psychological thread that shares the
   same root traumatic event.
   - The baseball-avoidance pattern is grief and resentment toward the
     sport itself. John quit under his father's over-investment and
     pressure to go pro, and he doesn't want to revisit a career soured by
     a loss whose real context most people don't know. This is the
     author's reading of the backstory.
   - The confession is guilt over causing Andy's death specifically: "I
     was piloting Andy's boat." (6346) and "I killed my best friend, Tru.
     And I never had to answer for it." (6359-6360). A different mechanism
     triggers it: Trudy's reciprocal confession ("John. Have you ever
     criticized God?... I did. Twice.", 6325-6335), plus the literal
     confessional booth priming disclosure.

   These are not the same capacity at different intensities. They are two
   distinct threads with a common traumatic root, the same kind of
   conflation as TRUDY's trait 6 split (concealment vs. resentment,
   `FOG_TRUDY_REVIEW.md`). The beat is the first-claim beat of an
   untracked trait, roughly "capable of reciprocal honesty under the right
   conditions". A first showing is consistent, not a turning point.
2. **Independently, the shape doesn't fit.** boundary_revealed typically
   describes a limit exposed under external pressure or force, something
   the character didn't choose to reveal. Here John faces no external
   conflict or confrontation. He volunteers the confession freely,
   overpowering whatever internal battle existed rather than having it
   forced out. That is agency and self-overcoming, not a boundary forced
   into view. Even taken as a candidate turning point on its own terms,
   voluntary disclosure doesn't fit the external-pressure shape
   boundary_revealed needs.

The batch 4 scene223_beat1 cross-reference is annotated accordingly
(above).

**Record corrections (resolver/synthesis metadata; no `fog_tagged.json`
field holds these, so there is no log entry; the saved `fog_pass2_calls/`
files stay as the cold record):**
- scene123_beat13: the resolver's "(e.g. with McAvoy, Sarge)" -> scene119_beat7.
- scene138_beat2: "had never before cracked on-screen" (synthesis) and "a
  breaking point never before shown" (resolver) are false. The basis is
  replaced by the cumulative-weight, no-proximate-trigger reading above.
- scene170_beat4 (drafted consistent, not queued, no change): its resolver
  uses scene138_beat2 as the reference "breakdown of composure". That still
  holds under the corrected reading.
- scene213_beat3: the trait checked against is the wrong trait. The beat is
  the first showing of an untracked reciprocal-honesty trait.

**Batch 5 result:** scene138_beat2 boundary_revealed confirmed, and
scene213_beat3 -> consistent, with 1 new corrections-log entry (751 total).
scene123_beat13, outside the queue, is confirmed with its citation
corrected.

## JOHN Pass 2: closing summary (2026-10-01)

> **Partly superseded later on 2026-10-01** by "Finding 19 resolution" (the
> next section). Four verdicts were reversed: scene185_beat2,
> scene172_beat6, scene217_beat1 and scene223_beat1. The tally is now **4
> throughline_evolution, 5 boundary_revealed and 13 consistent**, with 763
> log entries. The chain table below is restated there. This summary stays
> as the record of the queue's first close.

**JOHN's Pass 2 queue is closed.** All 5 batches and all 22 entries are
reviewed. The final values, recounted from `fog_tagged.json`, are **7
throughline_evolution, 2 boundary_revealed and 13 consistent**.
weight_proportionality is `matched` on all 22. The one mismatch,
scene108_beat1, was corrected to matched.

**Corrections logged during JOHN's review: 14.** The log went from 737
entries (end of TRUDY) to 751. By batch: batch 1 = 5, plus the
scene108_beat1 weight_proportionality follow-up = 1; batch 2 = 1; batch 3
= 3; batch 4 = 3; batch 5 = 1. Every other verdict was a confirmation
under the no-op convention. `fog_tagged.json` validates: 460 beats, 0
errors.

**The final shape of each chain:**

| Chain | Shape |
|---|---|
| Persuasion/extraction | scene19_beat1 (first shown: the consent-based wager) -> scene119_beat3 (escalation: institutional coercion, the ICE threat) -> scene152_beat1 (escalation: physical coercion, pinning Cheyenne) -> scene154_beat1 (escalation: psychological pressure layered onto the pin). Consistent: scene119_beat6/7/8 and scene155_beat1 |
| Armed pursuit | scene101_beat1 (first shown: defying "don't go to Biddeford") -> scene115_beat1 (unarmed risk-taking, consistent) -> scene163_beat1 (escalation: arming for an expected confrontation, entering his own cabin) -> scene172_beat6 (escalation: lethal exchange, finding 19 instance 2) -> scene175_beat1 (boundary: the life-preserving instinct extended to his attacker). Consistent: scene103_beat1, scene108_beat1, scene164_beat1, scene165_beat1 and scene172_beat7 |
| Willful blindness | scene14_beat4 (first shown, as an observation) -> scene185_beat2 (escalation: first personal practice, as pragmatism) -> scene217_beat1 (escalation: knowing obstruction as mercy, finding 19 instance 3). Consistent: scene217_beat2, scene218_beat1 and scene223_beat1 |

**Composure baseline: resolved, no contradiction.** The two drafts seemed
to contradict each other because two independent capacities had been
filed under one trait.
1. **Reactive anger at a proximate provocation, aimed at a specific
   target.** It is shown at scene119_beat7 (Shadow; Doug "concerned at
   John's temper") and is consistent at scene123_beat13. The scene14
   McAvoy/Sarge trash-talk is a different thing: crude deflection, closer
   to the synthesis trait "Deflects confrontation and emotional pain with
   crude jokes and insults" (first shown scene14_beat8). Reactive anger is
   not one of the synthesis's eight traits.
2. **Composure under cumulative, unprocessed weight.** It is first shown
   at scene13_beat1 and gives way at scene138_beat2 (boundary_revealed),
   with no trigger and no target.

So "already-established" and "never before cracked" each described a
different capacity. Once the citation and reasoning are corrected, both
records are accurate.

**A newly identified trait: reciprocal honesty under the right
conditions.** Its first showing is scene213_beat3 (consistent), in the
confessional, triggered by Trudy's own confession. It is untracked by the
synthesis. It is distinct from the baseball-avoidance trait (scene37_beat5)
even though both share the Andy trauma. scene223_beat1 ("There's something
I have to tell you.") is declared intent toward the same disclosure and
was resolved consistent in batch 4.

**Still open, carried beyond JOHN's queue:**
- Finding 19 -> a numbered principle, in a dedicated session (batch 4).
- scene165_beat1: a possible Persona read at the archetype layer (batch 3).
- The JOHN arc as a whole now contains two traits the synthesis didn't
  track (reactive anger, reciprocal honesty). This is a synthesis-coverage
  observation, with no field to change.

## Finding 19 resolution: four JOHN verdicts reversed (2026-10-01, author-confirmed)

Each reversal supersedes an earlier verdict and is logged as its own entry
naming what it replaces, following TRUDY scene131_beat1's convention. The
operative test is finding 19's two-axis test (`FOG_COLD_RUN_FINDINGS.md`
finding 19, "Resolution"):
- **Axis 1:** is the beat scored against an established trait, or is it
  the first showing of an untracked one?
- **Axis 2:** within an established trait, is the change quantitative
  (`throughline_evolution`) or a change in the type of act
  (`boundary_revealed`)?

weight_proportionality stays `matched` on all four. Nothing here concerns
the proportionality of the reaction, only its type.

**Quote check.** Every line below was printed in this session from a fresh
`pdftotext -layout -enc UTF-8` pull, byte-identical to `fog_full.txt`. One
quote in the instruction did not verify and is **not used**: "where it
matters most, not with the Law, but with the Lord" (scene217_beat1) appears
nowhere in the script. The on-page line is "Nothing. It's between you and
God now." (6593-6594).

| Beat | Was | Now | Supersedes | Log |
|---|---|---|---|---|
| scene185_beat2 | throughline_evolution | **consistent** | batch 4 confirmation (no-op, no log entry); synthesis escalation vs. scene14_beat4 | 760 |
| scene217_beat1 | throughline_evolution | **boundary_revealed** | batch 4 confirmation (no-op, no log entry) | 761 |
| scene172_beat6 | throughline_evolution | **boundary_revealed** | batch 3 confirmation (no-op, no log entry) | 762 |
| scene223_beat1 | consistent | **boundary_revealed** | batch 4 correction (log 750) | 763 |

**scene185_beat2 -> consistent.**
- **scene14_beat4 is not John's creed.** "See no evil, hear no evil, and
  you will survive." (392-393) is Chorus-register commentary. It riffs on
  the officer's "Streets are blind as usual. Buncha amnesiacs." (385-387)
  and is already Chorus at the archetype layer. It establishes nothing
  John personally lives by, so this beat can't be "stated philosophy
  becoming personal practice".
- **Trait replaced:** "Treats the arrival of justice as independent of his
  own personal action, whether permanently foreclosed (no one left to hold
  accountable) or already guaranteed (the outcome is coming regardless),
  which frees him to act in favor of those he loves without believing he's
  actually obstructing anything."
- **Its root is his own buried guilt over Andy's death,** not a philosophy
  picked up from watching others:
  - YOUNG JOHN: "Dad, it's okay. I'll say it was me." (2349)
  - MACKIE: "John! You fucked up. You can't undo this. You want to ruin
    two lives now?" (2353-2355, scene75_beat3)
  - JOHN, decades later: "I killed my best friend, Tru. And I never had to
    answer for it." (6358-6360, scene213_beat3)
- **The author's reading of the calculation.** John stayed silent because
  the damage was already done: Andy dead, his relationship with his father
  fractured, his baseball career over. Speaking would undo none of it. He
  makes the same calculation here, with Mackie, Holly and Reggie all dead:
  "Knowing he'll keep the truth of his father's involvement forever a
  secret." (5785-5786).
- **Verdict.** This is the first on-page showing of a lifelong disposition
  (Principle 2), not an escalation of anything: `consistent`.
- **Architectural note.** This throughline was visible only because the
  author holds JOHN and YOUNG JOHN as one continuous person. The tool
  tracks them as separate entities, so no per-character synthesis could
  have connected this beat to the boat-accident flashback. That is the
  basis of **finding 21** (`FOG_COLD_RUN_FINDINGS.md`).

**scene217_beat1 -> boundary_revealed.**
- **Same disposition as scene185_beat2.** Here it takes the "already
  guaranteed" form: "Soon all of New England's gonna be out looking for
  you. At least this way you get a chance to think." (6577-6579). He is not
  obstructing justice's eventual arrival. He is buying Trudy time to settle
  things with God ("Nothing. It's between you and God now.", 6593-6594).
- **A type-change within that disposition.** Every earlier instance, the
  decades of silence about Andy and scene185_beat2, is **omission**. This
  is its first **commission**: actively handing over the means to escape.
  "Trudy realizes. She takes out her car keys. Her and John make the
  exchange." (6582-6583). Omission and commission are different kinds of
  act, not one act at different intensities, the same distinction as
  scene172_beat6 below.
- **What it tests for the first time:** can this disposition only ever
  withhold, or can it actively intervene?
- **Finding 19 instance 3, recategorized.**

**scene172_beat6 -> boundary_revealed.**
- **No prior JOHN beat shows a capacity for discharging lethal force at a
  person.**
  - scene115_beat1 is an unarmed tackle ("he pounces hard onto Ricardo",
    3559).
  - scene163_beat1 is carrying a weapon for readiness while entering his
    own cabin ("with his dad's rifle in hand", 5202; "boots the door in",
    5210). Author-confirmed: he doesn't know what he'll find and is
    preparing for the worst, not seeking to shoot anyone.
- **Different types of act.** "Armed and prepared" and "has used lethal
  force against a person" differ in type, not intensity. TRUDY's arc was
  split the same way: arranging Holly's kidnapping through Raymond
  (scene213_beat7) and personally forcing her under (scene214_beat4) are
  two separate limits.
- **The act:** "He pops out of the room and returns fire--" (5494).
- **Contrast with REGGIE on the same beat.** REGGIE's lethal-force trait
  was already brandishing from its own first-shown beat (scene172_beat1),
  so brandish-to-fire is the same type of act, more intense. John's
  prepare-to-fire is a jump in type. The two characters get different
  verdicts on the same beat for a principled reason, not by inconsistency.
- **Finding 19 instance 2, recategorized.**

**scene223_beat1 -> boundary_revealed. Finding 19 instance 5 (NEW).**
- **What still stands from batch 4 (log 750):** the rejection of the false
  echo claim vs. scene14_beat4.
- **What changes:** the beat shouldn't default to `consistent`. It is
  scored against the trait first shown at scene213_beat3: reciprocal
  honesty under the right conditions ("I killed my best friend, Tru. And I
  never had to answer for it.", 6358-6360), which is `consistent` there as
  a first showing.
- **The type-change.** This beat is the first proactive, unilateral
  expression of that capacity. There is no reciprocal confession, no
  confessional booth, and nothing external prompting him except his own
  resolve:
  - "John, car idling, stares out at the home. He shuts off the car and
    climbs out." (6632-6633)
  - "A doorbell chimes." (6637)
  - "John standing here on the stoop." (6638)
  - "There's something I have to tell you." (6661-6662)

  Reactive disclosure under mutual exposure becoming proactive disclosure
  chosen entirely alone is a change in type, not a repetition.
- **Author-confirmed: the line itself is the crossing.** "There's something
  I have to tell you", spoken to the Murphys' faces after the doorbell and
  the stoop, is the committed, irrevocable act. It plays the role the key
  exchange (not the drive-off) played at scene217_beat1. Based on its
  relationship to drama and conflict, an audience will fully accept that
  John tells them the truth after THE END. What follows off the page is
  not in question.
- **This reverses batch 4's ground 1** for this beat ("declared intent
  isn't the act"). The archetype-layer removal of Hero (log 55) also cited
  declared intent, but it rests independently on the for-another test, so
  the tag is **not reopened**. How a speech act can count as the act is
  recorded as a question for the finding 19 session.

**Chains, restated.** The willful-blindness chain no longer exists as
batch 4 drew it, because scene14_beat4 is not its origin.

| Chain | Shape |
|---|---|
| Justice-independent-of-my-action | Root: YOUNG JOHN's Andy secret (scene75_beat3; separate character entity, finding 21) -> scene185_beat2 (first on-page showing, as omission: consistent) -> scene217_beat1 (first commission: boundary_revealed, finding 19). Consistent: scene217_beat2, scene218_beat1 |
| Reciprocal honesty | scene213_beat3 (first showing, reactive and mutual: consistent) -> scene223_beat1 (proactive, unilateral: boundary_revealed, finding 19 instance 5) |
| Armed pursuit | scene101_beat1 (first shown) -> scene115_beat1 (unarmed risk-taking, consistent) -> scene163_beat1 (escalation: arming for an expected confrontation) -> scene172_beat6 (lethal force at a person, a type-change: boundary_revealed, finding 19) -> scene175_beat1 (boundary: the life-preserving instinct extended to his attacker). Consistent: scene103_beat1, scene108_beat1, scene164_beat1, scene165_beat1, scene172_beat7 |
| Persuasion/extraction | unchanged (see the closing summary) |

**Tally, recounted from `fog_tagged.json`:** JOHN's 22 queue entries are now
**4 throughline_evolution** (scene119_beat3, scene152_beat1,
scene154_beat1, scene163_beat1), **5 boundary_revealed** (scene138_beat2,
scene172_beat6, scene175_beat1, scene217_beat1, scene223_beat1) and **13
consistent**. weight_proportionality is `matched` on all 22. This adds 4
log entries, for 763 in total. `fog_tagged.json` validates: 460 beats, 0
errors.
