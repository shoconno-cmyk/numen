# Full of Grace -- SARGE archetype review record

Per-character review record for SARGE's real-archetype tags in the
fully-cold run (`fog_tagged.json`). Beat-level `provenance` can't show
whether SARGE's own entry was reviewed (CLAUDE.md), so this file is the
authoritative record of each SARGE verdict, including confirmations that
change no data. Same convention as the other `FOG_*_REVIEW.md` files.

**Status column:** `applied` means the change has landed (`git log` on
this file gives the commit). Confirmations that change no data get no
corrections-log entry, per the no-op convention.

Scope: SARGE's 2 real-archetype beats (2026-09-28 enumeration: present on 5 beats, all in scene 14, EXT. EAST LOS ANGELES). scene14_beat12 is a pilot beat. Its first response was rejected whole (finding 1), and the stored tag comes from the re-run, which gave Mentor both times.

## Review (2026-09-28)

Checked against a fresh `pdftotext -layout` pull, with all stored turns
found. A reverse check (the PDF text for the scene against the stored
turns, per finding 15) found no missing text in this scene.

| beat_id | verdict | reason | status |
|---|---|---|---|
| scene14_beat6 | Great Mother (confirmed) | Protective action (he "keeps his hand on John's shoulder as he leads him away from the crime scene", as the kid-sized bodybag comes out) plus genuine supportive words ("everybody here is super proud of your decision"). No field changes. | applied |
| scene14_beat12 | ordinary_reaction, Mentor removed; fields rewritten | Author-confirmed: Sarge is enforcing an already-agreed boundary ("That was the deal -- prove to us you deserve to be back in there. Until then, you're door-to-door.") after John's own outburst proved the point ("This is what I'm talking about."), not transmitting anything new. Direct personal stake as John's supervisor rules out Chorus; no new insight or skill rules out Mentor. self_perceived, audience_perceived, goal and emotion rewritten; goal_status stays achieved. The goal uses the script's "door-to-door", not "desk duty" (the text never says desk duty). | applied |

SARGE's archetype review is complete. 1 real-archetype beat remains (scene14_beat6 Great Mother). Both beats from the enumeration have a row (recounted 2026-09-28).

## Pass 2 review: SARGE's queue (2026-10-03, one batch)

**Scope.** SARGE has 1 entry in `fog_pass2_queue.json`, recounted fresh:
scene14_beat13, `arc_claim_check_no_draft` (claimed throughline_evolution,
continuation vs. scene14_beat12). No finding 17 flag. His drafted entries
(scene14_beat6, 14_7, 14_12, 14_14) were all drafted consistent and not
queued. Material is printed from a fresh `pdftotext -layout -enc UTF-8`
pull, byte-identical to `fog_full.txt`. A reverse check (finding 15) found
no missing text on the queued or comparison beats. Every quoted line
below was re-checked against `fog_full.txt` in the logging turn.

Before this review, the corrections naming SARGE were 162-166 (the
scene14_beat12 archetype correction above) and the Pass 2 drafts 698-701.

**Synthesis traits (reference):**

| # | Trait | First shown |
|---|---|---|
| 1 | Directs John with firm, calm command authority -- assigning tasks, denying him entry to the crime scene despite pushback, and enforcing departmental protocol -- while briefly acknowledging John's personal circumstances with some warmth | scene14_beat6 |

**Functional or psychological:** no per-character ruling; see `FOG_COLD_RUN_FINDINGS.md`, "Pass 2 closeout notes", design note A (future work, not a blocker).

| Beat | Draft | Reviewed | Record |
|---|---|---|---|
| scene14_beat13 | no draft (`arc_claim_check_no_draft`; claimed TE continuation vs. 14_12) | **the claim does not hold** | review notes only; no CI field to correct. Pass 1 goal corrected: log (844) |

**scene14_beat13, the claim does not hold (author-confirmed).** The
synthesis's own `what_changes` ("the unbroken continuation of the
ultimatum just delivered in beat12 -- he is pressing for confirmation of
the same demand, not introducing a new development") contradicts its
throughline_evolution label. "Got that?" (516) is the same command
authority holding.

**Pass 1 correction: goal (log 844).** The stored goal "confirm
compliance/understanding from someone off-page" is wrong. "Got that?"
(516) is addressed to John: it follows Sarge's lines to him ("Not
happening! You gotta work your way back up to that. That was the deal --
prove to us you deserve to be back in there. Until then, you're
door-to-door.", 506-511) and "John's pissed. A moment passes." (513).
Corrected to "get John to acknowledge he's door-to-door until he earns
his way back". `characters_present` is speaker-only (`['SARGE']`), which
is likely how the model lost John (FUTURE_WORK item 1).

**Trait-wording note (record only; synthesis JSON untouched).** The
trait's "calm" is unsupported. The text gives "Sarge stops the dispute
quickly and with AUTHORITY." (481-482) and "Not happening!" (507).
"Firm" is supported; "calm" is not.

SARGE's Pass 2 queue is closed: 1/1 reviewed, the no-draft claim does not
hold, 1 Pass 1 log entry (844).
