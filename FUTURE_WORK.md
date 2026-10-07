# Future work (cross-script)

Improvements that would affect more than one script's pipeline or data,
logged so they aren't lost. None is urgent or blocking unless marked.

## 1. Presence detection for non-speaking characters in characters_present (logged 2026-09-26)

**Not urgent, not blocking. Not being built now.**

`characters_present` is built from speakers only (`characters_present` in `beat_detector.py`),
so a canonical character who acts in a beat's action lines without
speaking is never listed. See `FOG_COLD_RUN_FINDINGS.md` finding 2
(RAYMOND on `scene205_beat1`). A tagged beat's `per_character` is the
authoritative cast list. `characters_present` is not.

A presence-detection pass would fix this: find canonical characters and
aliases named in a beat's action turns and add them to
`characters_present`. It would change every script's scaffold, so it
needs its own decision and a re-scaffold/diff plan. It would also make a
names-must-be-present validator check possible. A strict check against
today's speaker-only field would reject hundreds of existing tags
(Ocean's Eleven 220/881, Babadook 127/470, LMS 105/624, GWH 58/626).
Open design point: a text match can't tell a character who is present
from one who is only mentioned. The prompt already draws that line
("Danny's plan").

**Instance recorded (2026-10-03, FOG PETE Pass 2):** `scene121_beat3`.
"Pete gets one solid punch into John's face before the dog pile begins."
(`fog_full.txt` 3946-3947) is action only, so PETE is not in
`characters_present` and has no entry on the beat (only JOHN does). In
review this surfaced as a claimed turning point pinned to the wrong beat
(scene122_beat1), not as a lost turning point: see `FOG_PETE_REVIEW.md`.

## 2. A one-line rationale for each archetype call (logged 2026-10-04)

**Build before the next cold run, alongside the finding 18 build.**

The tagging step stores no reason for an archetype call. All 470 FOG
tagging responses (`fog_tagging_calls.jsonl`) contain only the
perception fields (`self_perceived`, `audience_perceived`, `emotion`,
`goal`, `goal_status`, `agency_role`, plus `embodies` for
`functional_role_only`). Nothing says *why* a beat is Hero rather than
ordinary_reaction. The story report's click panel ("How the AI read this
moment") can therefore only show those fields, and says plainly that the
AI didn't write out why it chose the archetype.

Fix: add a one-line rationale field to the tagging prompt and schema
(validated like the other fields), so each call carries the model's own
stated reason, citing the beat's text.

**Do NOT generate rationales after the fact for existing FOG tags.** A
rationale written now would be a new model output dressed up as the
original call's reasoning. The FOG cold run stays as it was recorded.

## 3. Great Mother pole (Light/Dark) is not stored (logged 2026-10-04)

**Build before the next cold run, alongside item 2 and the finding 18 build.**

Great Mother is a dual-pole archetype in `BIG_SEVEN_DEFINITIONS` (Light:
nurtures and protects; Dark: smothers, controls, or devours), but the
data stores only the string "Great Mother". No FOG call records its
pole: 0 of 26 in the cold run (7a6e69e), 0 of 24 after review. There is
no field for it, and `moral_coloring` is empty on all of them. So the
story report's map can't show a pole.

Fix: add a Light/Dark pole field to the schema and tagging prompt,
required whenever "Great Mother" is tagged and validated like the other
enums.

**Do NOT infer poles for existing FOG calls.** The free-text pole
evidence that exists is reference only, not data: MACKIE
`scene140_beat5` (audience_perceived: "a parent smothering grief with
forced reassurance"), and review notes in corrections-log entries 97,
102 and 108.

## 4. Log the full prompt sent with every API call (logged 2026-10-05)

**Build before the next cold run, alongside items 2 and 3 and the finding 18 build.**

Every live call keeps its response and usage, but none keeps the prompt
it was given:
- tagging (`fog_tagging_calls.jsonl`): beat, model, request id, stop
  reason, usage, raw response; no prompt;
- Pass 2 (`fog_pass2_calls/*.json`): the raw response only;
- plot facts (`fog_plot_facts_call.json`): a SHA-256 of the prompt, not
  its text;
- development read (`fog_dev_read_call.json`): SHA-256s of the system
  prompt and user message, not their text.

So proving exactly what the model was given rests on git history. On
2026-10-05 the Big Seven definitions in the story report's appendix were
verified that way: `tagging_schema.py` was unchanged from c89b6da through
the cold run to 7a6e69e, and the prompt-rendering function was identical
in all four versions used during the run. But uncommitted edits made
during a run can't be ruled out from git alone.

Fix: write the full request (system blocks, messages, model, max_tokens,
output format) to the call log BEFORE each call, next to the response
that comes back. The script text sent many times over can be stored once
and referenced by hash, so the log doesn't repeat it for every beat.
