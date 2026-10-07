"""
lms_pass2_orchestration.py -- Stage 1+2 of the "make Pass 2 independent"
project: a real harness for LLM-assisted causal-integrity resolution
(weight_proportionality, characterization_consistency), following the
exact same discipline as llm_orchestration.py -- the LLM acts as an
INTERPRETER strictly bound to tagging_schema.py's fixed vocabulary, a
malformed response is rejected and retried rather than silently
accepted, and the API key is read ONLY from the environment.

WHY THIS IS SEPARATE FROM llm_orchestration.py: that module resolves
ONE beat at a time, in isolation -- correct for archetype tagging,
but causal-integrity Pass 2 is explicitly, by the schema's own design,
a whole-ARC judgment. weight_proportionality and characterization_
consistency cannot be honestly assessed from a single beat; they
require every beat a character appears in, in story order, considered
together. So this module's unit of work is a CHARACTER's full presence
across the script, not a beat.

SCOPE: chain_soundness and agency_alignment are NOT part of this
module -- both were already resolved during the original tagging pass
(confirmed via real LMS data: 100% resolved, 0% left at their
placeholder defaults) and don't require whole-arc context the way the
other two fields do. This module only ever writes weight_proportionality
and characterization_consistency.

PILOT MODE FIRST: run_pass2_pilot() is the entry point to actually use
right now. It is NON-DESTRUCTIVE -- it never writes to the analysis --
and exists specifically to test this harness against a character whose
Pass 2 has already been human-resolved (Richard, this session), to get
a real hit-rate number before trusting this on new material. Only after
a pilot run's numbers are reviewed does apply_pass2_results() become
the right tool, for characters with no ground truth to check against yet.

NOTE: like llm_orchestration.py, this module builds and validates
around LLM responses but does not have a live API call available in
THIS environment -- credentials must be supplied via ANTHROPIC_API_KEY
in the calling shell. The prompt-construction and response-parsing/
validation logic is real and independently testable without a live call.
"""

import sys
import os
import json
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from tagging_schema import (
    WeightProportionality, CharacterizationConsistency, CausalIntegrityTag,
    CAUSAL_INTEGRITY_PRINCIPLES, beat_id_sort_key,
)


# Claude Sonnet 5 pricing, confirmed current (standing, not introductory) rate as of
# August 2026: $2.00 / MTok input, $10.00 / MTok output. Verified against Anthropic's
# own pricing docs before this constant was written -- re-check before trusting this
# in a much later session, since rates can change.
_SONNET_5_INPUT_PER_MTOK = 2.00
_SONNET_5_OUTPUT_PER_MTOK = 10.00


def _print_usage_and_cost(label, usage):
    """Print ACTUAL token usage and cost for one API call, from the
    real response object -- not an estimate. Called right after every
    live call in this module so cost is always reported from ground
    truth, never guessed."""
    input_cost = (usage.input_tokens / 1_000_000) * _SONNET_5_INPUT_PER_MTOK
    output_cost = (usage.output_tokens / 1_000_000) * _SONNET_5_OUTPUT_PER_MTOK
    total_cost = input_cost + output_cost
    print(
        f"[USAGE] {label}: input={usage.input_tokens} output={usage.output_tokens} "
        f"(thinking={usage.output_tokens_details.thinking_tokens if usage.output_tokens_details else 'n/a'}) "
        f"cache_write={usage.cache_creation_input_tokens} (not in cost below) "
        f"cache_read={usage.cache_read_input_tokens} -- cost=${total_cost:.4f} "
        f"(${input_cost:.4f} in + ${output_cost:.4f} out)"
    )
    return total_cost


def _find_character_tag(beat_tag, character):
    """Find `character`'s ArchetypeTag within one beat's per_character
    list -- this is where causal_integrity actually lives now (see
    tagging_schema.py's ArchetypeTag docstring for why it moved off
    BeatTag). Returns None if the character has no entry at all,
    which shouldn't happen for any beat where they're listed as
    present (confirmed: every present character gets a per_character
    entry, even a bare no_confident_archetype one) -- but checked
    defensively rather than assumed."""
    for tag in beat_tag.per_character:
        if tag.character == character:
            return tag
    return None


def gather_character_beats(analysis, character):
    """Every beat where `character` is PRESENT, in story order --
    NOT filtered to archetype-tagged beats only.

    THIS FILTER CHOICE IS LOAD-BEARING, not incidental. Real errors
    from this session's manual Pass 2, caught only because the author
    happened to look further: Dwayne's actual resolution beat
    (scene113_beat5, breaking his vow of silence for real) carried no
    archetype tag at all -- an archetype-tagged-only pass would have
    concluded his arc simply never resolved. Separately, Olive's
    single most load-bearing causal action in the entire script (the
    eye-chart game that triggers Dwayne's colorblindness discovery,
    scene87) also carries no archetype tag. A harness that only
    gathers archetype-tagged beats will silently reproduce both
    mistakes on every future character.

    Filters on `per_character` membership, NOT `characters_present` --
    the latter is computed upstream in beat_detector.py from turn
    SPEAKERS only, so it silently misses any character who acts in a
    beat without a dialogue turn attributed to them (a pickpocket lift,
    a silent tail, gassing a guard from behind). Confirmed via real
    Ocean's Eleven data: for LINUS specifically, filtering on
    characters_present returned 44 beats against per_character's
    correct 85 -- a 41-beat undercount, not a handful of edge cases.
    See OCEANS11_OPEN_ITEMS.md item 6 for the full coverage-gap
    writeup. `characters_present` remains fine for per-beat display
    purposes; it is not safe as a filter for enumerating a character's
    beats."""
    beats = []
    for beat_id, bt in analysis.beats.items():
        if any(t.character == character for t in bt.per_character):
            beats.append((beat_id, bt))
    beats.sort(key=lambda pair: beat_id_sort_key(pair[0]))
    return beats


PASS2_VOCABULARY_INSTRUCTIONS = """
You must respond with valid JSON matching this exact schema. Every
enum field below MUST use one of the listed values EXACTLY as written
(case-sensitive) -- any other value will be rejected, not interpreted.

You have been given, as FIXED CONTEXT below, an already-completed
synthesis of this character's established pattern AND a list of
CANDIDATE turning-point beats a separate, dedicated pass identified as
possibly escalating, continuing, or echoing that pattern. Unlike plot
facts, these candidates are NOT verified conclusions -- the synthesis
pass was deliberately instructed to search exhaustively and cast a
wide net, which means some candidates on this list will not hold up
to closer inspection. Your job includes being the check on that list,
not deferring to it.

For EVERY beat, you MUST name which established trait (or which
turning point) you checked it against. A beat that just seems locally
plausible or unremarkable in isolation is NOT enough to call it
"consistent" -- you must have actually checked it against the given
synthesis.

IF A BEAT_ID APPEARS IN THE GIVEN turning_points LIST, INDEPENDENTLY
RE-VERIFY IT -- do not simply adopt its likely_category. You have the
full evidence for both beat_id and its comparison_beat_id available in
the evidence below (they're beats from the same character's full
presence). Actually re-check both:

- If turning_point_type is "escalation": does beat_id's scale/cost/risk
  CONCRETELY and DEMONSTRABLY exceed comparison_beat_id's, on inspecting
  both directly -- or does it just plausibly sound like more?
- If "continuation": is beat_id genuinely the SAME unbroken event/
  sequence as comparison_beat_id, with no real gap -- or is it simply a
  later beat that happens to involve the same character trait?
- If "echo": is there an actual, specific, textually concrete callback
  to comparison_beat_id (the same prop, the same phrase, direct
  reversal of a stated rule) -- or is the connection thematic/vibes-
  based rather than a real, nameable textual echo?
- If marked UNVERIFIED: the synthesis pass's claim failed structural
  validation (a continuation whose comparison beat is not itself a
  turning point, or no turning-point type claimed at all). Do NOT
  treat it as any of the three types above. Keep a notable
  classification only if your own direct comparison of both beats
  shows a concrete change, name that change, and say in your rationale
  that the candidate was unverified.

A candidate that sounds reasonable in the synthesis pass's own
description is NOT sufficient justification on its own -- you must be
able to independently confirm the SAME comparison holds up when you
look at the actual evidence yourself. If it does not concretely hold
up under this direct re-check, DOWNGRADE to "consistent" and say so
explicitly in your rationale (e.g. "candidate turning point rejected on
independent review -- the comparison doesn't hold up because..."). Only
keep a candidate's notable classification when your own direct
inspection of both beats confirms it, not because a separate pass
already proposed it.

{
  "beat_resolutions": [
    {
      "beat_id": "<must match a beat_id from the evidence exactly>",
      "checked_against": "<which established trait or turning point you compared this beat to>",
      "weight_proportionality": "matched"|"mismatch",
      "characterization_consistency": "consistent"|"contradicted"|"throughline_evolution"|"boundary_revealed",
      "contradiction_trace": {"suspected_external_note": "<free text>", "craft_evidence": ["<free text>", ...]},
        -- REQUIRED if and only if characterization_consistency is "contradicted", omit otherwise
      "rationale": "<1-3 sentences: what established pattern, trigger, or prior beat justifies this specific call>"
    },
    ...
  ]
}

CRITICAL: you have been given this character's COMPLETE presence
across the script, in story order -- you have exactly what "requires
the whole work first" requires. Do NOT respond with "requires_second_pass"
for any beat; that value does not exist in this task's output vocabulary
and will be rejected. Every beat must resolve to a real value.

Produce EXACTLY one entry per beat_id listed in the evidence, in the
same order. Do not skip beats, do not add beats not listed.
"""


SYNTHESIS_ONLY_INSTRUCTIONS = """
You are reading ONE character's COMPLETE presence across a screenplay,
in story order. Your ONLY job is synthesis -- you are NOT resolving
any individual beat's causal integrity here. A separate pass will use
your output to do that; your job is to produce the structured
reference material that pass will check every beat against.

Respond with ONLY this JSON structure, no markdown fences, no preamble:

{
  "established_pattern_synthesis": [
    {"trait": "<short statement of an established trait/value>", "first_shown_beat_id": "<beat_id>"},
    ...
  ],
  "turning_points": [
    {
      "beat_id": "<beat_id>",
      "trait_it_relates_to": "<which trait from established_pattern_synthesis above>",
      "turning_point_type": "escalation"|"continuation"|"echo",
      "comparison_beat_id": "<meaning depends on turning_point_type -- see the three definitions below, required for all three>",
      "what_changes": "<1-2 sentences: concrete justification matching the type -- see below>",
      "likely_category": "throughline_evolution"|"boundary_revealed"|"contradicted"
    },
    ...
  ]
}

THERE ARE THREE DISTINCT SHAPES A REAL TURNING POINT CAN TAKE. Do not
force every genuine finding through only one of these -- each has its
own justification test:

ESCALATION -- comparison_beat_id is a specific earlier beat where this
SAME trait appeared at CLEARLY LESSER scale, cost, or risk. what_changes
must state concretely how this beat exceeds that one, not just that
the trait is present in both.

CONTINUATION -- comparison_beat_id is a DIFFERENT beat ALREADY IN THIS
turning_points LIST (not an arbitrary earlier beat) that this beat
directly extends -- the same event or sequence continuing with no
gap, immediately after or very close to it. A single dramatic action
often has its consequence or continuation land in the very next beat,
which is its own equally or more significant turning point, not a
mere aftermath of the one before it. Use this type specifically for
beats that follow an already-identified turning point in the same
unbroken sequence.

ECHO -- comparison_beat_id is a specific earlier beat (from this
character's OWN established pattern -- an earlier statement, rule, or
behavior of theirs) that THIS beat concretely reverses, answers, or
completes. Unlike escalation, an echo does NOT need to be BIGGER or
more costly than what it's answering -- it can be quieter, smaller, a
single line. Its significance comes from being a direct, textually
concrete callback (the same prop, the same phrase, the character
doing the opposite of a rule they themselves stated), not from its own
scale. Do not require magnitude for this type -- require concreteness
of the echo instead. A vague thematic vibe ("this feels like growth")
is NOT enough; you must be able to point to what specific earlier
moment this one is answering and how. Per Principle 10, THIS
character's own action or line in the echo beat must be the primary
evidence. Another character's line can support the reading, but a
beat where only someone else acts or speaks is NOT an echo for this
character, however directly it answers their earlier beat.

TRAIT STATEMENTS MUST REFLECT ONLY WHAT'S SHOWN AT first_shown_beat_id.
Do not write the character's later, more developed, or ending
expression of a trait into its label -- describe only what that first
beat's own text actually shows. Later intensification, change, or
reversal belongs in turning_points, not in the trait definition itself.
A trait label must describe only what its first_shown_beat_id's own
text actually depicts -- not an inference, motive, or interior state
you're reading into silence, evasion, or an unrelated action. If the
beat shows behavior X, the trait is X, not what you believe X reveals
or conceals. (Real error caught: TRUDY's trait "resentment/jealousy
... masked behind piety" was anchored to a beat that only shows her
having no answer to a question -- evasion is depicted there;
resentment and masking are not.)

BEFORE ADDING ANY ENTRY TO turning_points, YOU MUST BE ABLE TO NAME A
VALID comparison_beat_id matching the type you chose. If you cannot,
this is NOT a turning point, no matter how emotionally resonant the
moment feels in isolation -- it is simply the established trait
operating normally, which happens repeatedly through a story without
every instance being remarkable. A short, or even EMPTY, turning_points
list is a correct and honest result for a character whose narrative
role is to remain a stable presence others are tested against -- it is
not evidence you didn't look hard enough.

turning_points is the critical output. Do not just note that a
character's pattern is broadly consistent -- actively hunt for beats
where the established trait is pushed to a SCALE, COST, or RISK it
has never been tested at before (escalation), directly continues an
already-found turning point without a gap (continuation), or answers/
reverses something the character themselves established earlier, even
quietly (echo).

If a trait is tested but the character does NOT change (a
previously-untested limit gets exposed instead, or the story reveals
something without the trait itself moving), that's boundary_revealed,
not throughline_evolution -- still name the specific beat_id and type.

BE EXHAUSTIVE, NOT ILLUSTRATIVE. Finding one or two clean examples per
trait and stopping there is NOT enough.

STORIES DON'T END A THREAD EARLY -- NEITHER SHOULD YOU. Every trait
you name in established_pattern_synthesis is a THREAD that runs from
its first_shown_beat_id all the way to THIS CHARACTER'S VERY LAST
BEAT in the script -- it does not stop mattering just because you
found one clear turning point partway through. For EACH trait,
explicitly trace it beat-by-beat, in order, from where it starts to
the character's final beat -- THE END -- not just the handful of
beats near your first finding. A single thread can cross several
escalating thresholds on its way there, and the LAST beats of a
thread (often at or near the story's climax/ending) are exactly where
a fully-resolved evolution is MOST likely to show, not least likely.
If you notice yourself stopping a trait's check partway through this
character's beats, go back and continue tracing it all the way to
their actual last appearance before finalizing your list.

IN PARTICULAR: always check the beat(s) immediately following any
turning point you identify, specifically for the CONTINUATION type
above. Does the same event or sequence continue there with even
greater stakes? Do not treat your first finding in a sequence as
closing the sequence.

THREADS ARE NOT LINEAR -- A DIP OR PAUSE IS NOT AN ENDING. A
character's journey along one trait rarely rises in a straight line;
it can ebb, sit still, or even seem to reverse before continuing.
Do NOT stop tracing a thread just because a beat's intensity doesn't
exceed the highest point you've already found for it -- a quieter or
lower-stakes beat can still belong to the same live thread, and a
later beat can pick the escalation back up after an apparent lull.
Do NOT require every beat in a sequence to be MORE extreme than the
last on the exact same axis, either -- a character can express the
same underlying stake through a genuinely different KIND of action
(a moment of physical risk, then later a moment of purely emotional
exposure) and both can belong to the same thread even though they
aren't directly comparable in scale. A beat that sits BEFORE your
strongest finding, building toward it, is as much a candidate as one
that comes after. Keep tracing every thread all the way to THE END
regardless of apparent pauses in between -- a real arc's shape is
rarely a clean staircase. This is exactly what the ECHO type exists
for -- a quiet, small, low-magnitude beat can still be the thread's
most important moment if it's a concrete answer to something earlier.

An empty turning_points list is a legitimate answer if this
character's presence, on genuine inspection, really doesn't contain
one -- but check hard before concluding that, especially across a
character's climax/ending beats.
"""


UNVERIFIED_DANGLING_CONTINUATION = "unverified -- comparison beat not independently flagged"
UNVERIFIED_NO_TYPE_CLAIMED = ("unverified -- model put a likely_category value in "
                              "turning_point_type; no turning-point type was claimed")


def _is_immediately_preceding_beat(analysis, comparison_beat_id, beat_id):
    """True when comparison_beat_id is the beat directly before beat_id
    in the same scene (by beat_id_sort_key over every beat in that scene)."""
    bt = analysis.beats.get(beat_id)
    cmp_bt = analysis.beats.get(comparison_beat_id)
    if bt is None or cmp_bt is None or bt.scene_id != cmp_bt.scene_id:
        return False
    scene_ids = sorted((bid for bid, b in analysis.beats.items() if b.scene_id == bt.scene_id),
                       key=beat_id_sort_key)
    i = scene_ids.index(beat_id)
    return i > 0 and scene_ids[i - 1] == comparison_beat_id


def validate_turning_points(analysis, turning_points):
    """Validate the three-type structure of a synthesis call's
    turning_points. Returns (kept, dropped). Never makes an API call.

    Catches a malformed/missing comparison_beat_id before it silently
    becomes an unjustified turning point downstream, and repairs two
    known model slips WITHOUT inventing a type the model never chose
    (FOG_COLD_RUN_FINDINGS.md finding 17):

    - "continuation" whose comparison_beat_id isn't another entry in
      this list (dangling -- continuation requires the referenced beat
      to ALSO be flagged).
    - turning_point_type holding a likely_category value
      (throughline_evolution/boundary_revealed/contradicted). The value
      moves into likely_category if that field is empty; no type was
      claimed, so turning_point_type becomes None.

    Both slips were previously relabeled "escalation" in place. That
    asserted a magnitude claim the model never made (all 5 dangling
    continuations described an unbroken sequence; all 8 healed entries
    described a limit exposed), and the relabel left no trace on the
    entry. Both used to be hard rejections, which discarded whole paid
    synthesis calls ($0.29) for one entry -- so these still repair
    rather than raise. The fallback is now:

    - comparison beat is the immediately preceding beat in the same
      scene -> drop the entry (it is the trait continuing to operate,
      which the synthesis prompt already says is NOT a turning point);
      it's kept in `dropped` with the reason, not discarded.
    - otherwise -> keep it with its original claim, set "validation"
      and requires_human_review=True. The resolution prompt shows the
      flag, and the human Pass 2 review must check it.

    Every entry records model_turning_point_type (the value the model
    actually wrote), so the model's claim is never overwritten silently."""
    valid_types = {"escalation", "continuation", "echo"}
    category_values = {"throughline_evolution", "boundary_revealed", "contradicted"}
    tp_beat_ids = {tp.get("beat_id") for tp in turning_points if isinstance(tp, dict)}
    kept, dropped, flagged = [], [], []
    for i, tp in enumerate(turning_points):
        tp_type = tp.get("turning_point_type")
        comparison = tp.get("comparison_beat_id")
        tp.setdefault("model_turning_point_type", tp_type)
        validation = None

        if tp_type in category_values:
            if not tp.get("likely_category"):
                tp["likely_category"] = tp_type
            tp["turning_point_type"] = None
            validation = UNVERIFIED_NO_TYPE_CLAIMED
        elif tp_type not in valid_types:
            raise ValueError(
                f"turning_points[{i}] ({tp.get('beat_id')}): turning_point_type must be one "
                f"of {valid_types}, got {tp_type!r}. Full entry: {tp!r}"
            )
        if not comparison:
            raise ValueError(
                f"turning_points[{i}] ({tp.get('beat_id')}): missing comparison_beat_id -- "
                f"required for all three types. Full entry: {tp!r}"
            )
        if tp_type == "continuation" and comparison not in tp_beat_ids:
            validation = UNVERIFIED_DANGLING_CONTINUATION

        if validation is None:
            kept.append(tp)
        elif _is_immediately_preceding_beat(analysis, comparison, tp.get("beat_id")):
            tp["dropped_reason"] = (f"{validation}; comparison beat is the immediately "
                                    f"preceding beat in the same scene")
            dropped.append(tp)
        else:
            tp["validation"] = validation
            tp["requires_human_review"] = True
            kept.append(tp)
            flagged.append((tp.get("beat_id"), tp_type, comparison))

    if dropped:
        print(f"[TP-DROPPED] {len(dropped)} entr{'y' if len(dropped) == 1 else 'ies'} "
              f"(invalid claim vs. the immediately preceding beat): "
              f"{[(tp.get('beat_id'), tp['model_turning_point_type'], tp.get('comparison_beat_id')) for tp in dropped]}")
    if flagged:
        print(f"[TP-FLAGGED] {len(flagged)} entr{'y' if len(flagged) == 1 else 'ies'} kept as "
              f"unverified, MANDATORY human review: {flagged}")
    return kept, dropped


def synthesize_character_arc(analysis, character, model="claude-sonnet-5", max_tokens=40000,
                             raw_save_path=None):
    """Dedicated, SEPARATE call whose only output is the structured
    arc synthesis (established traits + explicitly-named turning-point
    beats) -- mirrors plot_facts_extraction.py's design: a focused
    whole-script/whole-arc read producing a fixed artifact, injected
    as given context into every subsequent beat-level call, rather
    than asking one call to both discover cross-references AND act on
    130 individual beat judgments in the same generation.

    Built after two live pilot runs on RICHARD where a single-call,
    two-step-in-one-generation version of this task caught real
    transition beats inconsistently (3/11, then regressed to 1/11 on
    a revised prompt) -- the model's own language showed it recognizing
    a before/after split internally but not translating that into an
    explicit, checkable list of WHICH beats are the transition itself.
    Splitting synthesis into its own call, with an explicit
    turning_points requirement, is the direct structural fix, not
    another wording change to the same single-call design.

    max_tokens raised 20000 -> 40000 after a real failure on SHERYL:
    output hit exactly 20000 (18027 of it thinking), truncating the
    JSON response mid-string with too little room left to finish.
    Same failure shape documented in plot_facts_extraction.py and
    already fixed once before on the resolution call (8000 -> 40000)
    -- the growing instruction set (now three types, self-heal notes,
    exhaustiveness/thread-to-the-end framing) has made 20000 no longer
    reliably sufficient, even for a smaller-presence character than
    the one this budget was originally sized for."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set in the environment. Set it via an "
            "environment variable in your own shell before calling this, "
            "never paste a key into a script or a chat transcript."
        )
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("The 'anthropic' package is not installed. Run: "
                            "pip install anthropic --break-system-packages")

    character_beats = gather_character_beats(analysis, character)
    if not character_beats:
        raise ValueError(f"No beats found where {character} is present.")

    client = anthropic.Anthropic(api_key=api_key)
    system_text = CAUSAL_INTEGRITY_PRINCIPLES + "\n\n" + SYNTHESIS_ONLY_INSTRUCTIONS
    system_blocks = [
        {"type": "text", "text": system_text, "cache_control": {"type": "ephemeral", "ttl": "1h"}},
    ]
    user_message = build_pass2_user_message(character, character_beats)
    user_message += "\n\nRespond with ONLY the JSON object described in your instructions."

    with client.messages.stream(
        model=model, max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        response = stream.get_final_message()
    _print_usage_and_cost(f"{character} synthesis call", response.usage)
    text_parts = [block.text for block in response.content if block.type == "text"]
    raw = "".join(text_parts)
    if raw_save_path:
        # Saved BEFORE parsing so a parse failure never loses a paid call.
        with open(raw_save_path, 'w', encoding='utf-8') as f:
            json.dump({'character': character, 'raw_text': raw}, f, indent=2, ensure_ascii=False)

    try:
        cleaned = raw.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned
            if cleaned.rstrip().endswith('```'):
                cleaned = cleaned.rstrip()[:-3]
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Arc synthesis response was not valid JSON: {e}\nRaw: {raw[:1000]}")

    synthesis = data.get("established_pattern_synthesis")
    turning_points = data.get("turning_points")
    if not isinstance(synthesis, list) or not synthesis:
        raise ValueError("Arc synthesis response missing established_pattern_synthesis")
    if not isinstance(turning_points, list):
        raise ValueError("Arc synthesis response missing turning_points (empty list is fine, missing key is not)")

    turning_points, dropped = validate_turning_points(analysis, turning_points)
    return {"synthesis": synthesis, "turning_points": turning_points,
            "dropped_turning_points": dropped}


def _turning_point_type_label(tp):
    """Type label for the resolution prompt. An entry flagged by
    validate_turning_points() says so, instead of showing a type the
    model never validly claimed."""
    if not tp.get("validation"):
        return tp["turning_point_type"]
    claimed = tp.get("turning_point_type") or "NO TYPE CLAIMED"
    return f"{claimed} -- " + tp["validation"].replace("unverified -- ", "UNVERIFIED: ", 1)


def build_pass2_system_blocks(arc_synthesis):
    """Static-per-call portion: the causal-integrity principles, field
    definitions, output vocabulary, AND the pre-computed arc synthesis
    (established traits + turning points) from synthesize_character_arc(),
    injected here as FIXED, given context -- mirrors exactly how
    plot_facts get injected into every beat-tagging call in Pass 1,
    rather than asking this call to re-derive the synthesis itself."""
    synthesis_text = "\n".join(
        f"  - {s['trait']} (first shown: {s['first_shown_beat_id']})"
        for s in arc_synthesis["synthesis"]
    )
    if arc_synthesis["turning_points"]:
        turning_points_text = "\n".join(
            f"  - {tp['beat_id']} [{_turning_point_type_label(tp)} vs. {tp['comparison_beat_id']}]: "
            f"{tp['what_changes']} "
            f"(relates to: {tp['trait_it_relates_to']}, likely: {tp['likely_category']})"
            for tp in arc_synthesis["turning_points"]
        )
    else:
        turning_points_text = "  (none identified -- this character's presence, on synthesis-pass inspection, showed no turning point)"

    parts = [
        "You are resolving causal-integrity judgments (weight_proportionality "
        "and characterization_consistency ONLY) for ONE character's complete "
        "presence across a screenplay, given in story order. This requires "
        "genuine reasoning about the character's established pattern and "
        "whether each beat matches it, tests it, or reveals something new -- "
        "not a mechanical per-beat check. Read the principles below carefully; "
        "they were earned by correcting real errors on this exact task.",
        "",
        CAUSAL_INTEGRITY_PRINCIPLES,
        "",
        "=== ESTABLISHED PATTERN SYNTHESIS (already completed, given as fact) ===",
        synthesis_text,
        "",
        "=== CANDIDATE TURNING POINTS (proposed, NOT verified -- independently ===",
        "=== re-check each against its comparison_beat_id's actual evidence) ===",
        turning_points_text,
        "",
        "=== FIELD DEFINITIONS ===",
        "weight_proportionality: does the INTENSITY of the character's reaction "
        "in this beat match what's actually at stake in it? 'mismatch' means "
        "the reaction is disproportionate to the real stakes (e.g. rigid, "
        "escalated control over a genuinely low-stakes choice).",
        "",
        "characterization_consistency:",
        "  consistent -- matches the character's established pattern directly, nothing notable",
        "  contradicted -- requires a trait/state INCOMPATIBLE with what's established, "
        "appearing suddenly with no gradual buildup, often only explicable by something "
        "OUTSIDE the story's own logic (e.g. a production note)",
        "  throughline_evolution -- the character's underlying trait itself has genuinely "
        "CHANGED, gradually, with a clear in-story trigger, explicable entirely within the "
        "story, and persists afterward",
        "  boundary_revealed -- the character has NOT changed; a previously-untested LIMIT "
        "of an already-consistent trait is exposed for the first time because the story "
        "generated pressure severe enough to locate it",
        "",
        "=== REQUIRED OUTPUT FORMAT ===",
        PASS2_VOCABULARY_INSTRUCTIONS,
    ]
    system_text = "\n".join(parts)
    return [
        {"type": "text", "text": system_text, "cache_control": {"type": "ephemeral", "ttl": "1h"}},
    ]


def _format_beat_for_pass2(beat_id, beat_tag):
    """One beat's evidence, in the same untruncated turn format
    integration.py uses -- reused rather than reinvented, since it's
    already been validated as the correct level of detail for an LLM
    making an interpretive judgment on this project."""
    from integration import evidence_summary
    return evidence_summary(beat_tag)


def build_pass2_user_message(character, character_beats, target_beat_ids=None):
    """The dynamic portion: this character's full ordered evidence.
    Never cached -- different per character by design.

    target_beat_ids, when given, restricts only the CLOSING instruction
    to a subset -- the evidence section above it still lists this
    character's full arc unchanged. That's required, not just simpler:
    PASS2_VOCABULARY_INSTRUCTIONS requires independently re-verifying
    each turning-point candidate against its comparison_beat_id's own
    evidence, and that comparison beat can be any beat in the character's
    presence, not necessarily one of the current targets. Only the
    resolution call (call_claude_for_pass2) passes this; the synthesis
    call (synthesize_character_arc) always leaves it None -- whole arc,
    by design, since it's the call that produces the trajectory itself."""
    parts = [
        f"=== CHARACTER: {character} ===",
        f"Total beats where {character} is present, in story order: {len(character_beats)}",
        "",
    ]
    for beat_id, beat_tag in character_beats:
        parts.append(f"--- {beat_id} ---")
        parts.append(_format_beat_for_pass2(beat_id, beat_tag))
        parts.append("")
    if target_beat_ids is not None:
        target_ids_text = "\n".join(f"  - {bid}" for bid in target_beat_ids)
        parts.append(
            f"Resolve weight_proportionality and characterization_consistency ONLY for the "
            f"following {len(target_beat_ids)} target beat_id(s), each explicitly checked "
            f"against the established pattern synthesis and turning points already given in "
            f"your instructions, in the required JSON format:\n{target_ids_text}\n\n"
            f"Beats appearing above but not in this list are context only -- do not emit "
            f"entries for them, even if you reference their evidence while resolving a "
            f"target beat."
        )
    else:
        parts.append(
            f"First synthesize {character}'s established pattern(s) (Step 1), then resolve "
            f"weight_proportionality and characterization_consistency for every one of the "
            f"{len(character_beats)} beats listed above, explicitly checked against that "
            f"synthesis (Step 2), in the required JSON format."
        )
    return "\n".join(parts)


def parse_pass2_response(raw_json_text, expected_beat_ids):
    """Strictly parse and validate. Returns (success: bool, result_or_error).

    On success: result is dict[beat_id -> {"weight_proportionality":
    WeightProportionality, "characterization_consistency":
    CharacterizationConsistency, "contradiction_trace": dict|None,
    "checked_against": str, "rationale": str}]. No top-level synthesis
    here anymore -- that's produced separately by
    synthesize_character_arc() and injected as given context, not
    re-requested from this call.

    Validates: valid JSON, exact enum values, contradiction_trace
    present iff characterization_consistency == CONTRADICTED (same
    rule CausalIntegrityTag.validate() enforces elsewhere), response
    covers EXACTLY the expected beat_id set with no extras/omissions,
    and rejects "requires_second_pass" explicitly -- a model
    attempting to punt on a whole-arc task it was given full context
    for is a malformed response for THIS task, not a valid answer."""
    try:
        cleaned = raw_json_text.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned
            if cleaned.rstrip().endswith('```'):
                cleaned = cleaned.rstrip()[:-3]
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    resolutions = data.get("beat_resolutions")
    if not isinstance(resolutions, list):
        return False, "Missing or malformed 'beat_resolutions' array"

    beats_result = {}
    seen_ids = set()
    for i, entry in enumerate(resolutions):
        beat_id = entry.get("beat_id")
        if not beat_id:
            return False, f"Entry {i}: missing beat_id"
        if beat_id in seen_ids:
            return False, f"Entry {i}: duplicate beat_id {beat_id!r}"
        seen_ids.add(beat_id)

        wp_raw = entry.get("weight_proportionality")
        cc_raw = entry.get("characterization_consistency")
        if wp_raw == "requires_second_pass" or cc_raw == "requires_second_pass":
            return False, (
                f"{beat_id}: 'requires_second_pass' is not a valid response for this "
                f"task -- full character context was provided specifically to resolve this."
            )
        try:
            wp = WeightProportionality(wp_raw)
            cc = CharacterizationConsistency(cc_raw)
        except ValueError as e:
            return False, f"{beat_id}: invalid enum value -- {e}"

        contradiction_trace = entry.get("contradiction_trace")
        if cc == CharacterizationConsistency.CONTRADICTED and not contradiction_trace:
            return False, f"{beat_id}: characterization_consistency=contradicted requires contradiction_trace"

        beats_result[beat_id] = {
            "weight_proportionality": wp,
            "characterization_consistency": cc,
            "contradiction_trace": contradiction_trace,
            "checked_against": entry.get("checked_against", ""),
            "rationale": entry.get("rationale", ""),
        }

    expected_set = set(expected_beat_ids)
    if seen_ids != expected_set:
        missing = expected_set - seen_ids
        extra = seen_ids - expected_set
        return False, (
            f"beat_id set mismatch -- missing: {sorted(missing) or 'none'}, "
            f"unexpected: {sorted(extra) or 'none'}"
        )

    return True, beats_result


def call_claude_for_pass2(analysis, character, model="claude-sonnet-5", max_tokens=40000, target_beat_ids=None,
                          arc_synthesis=None, synthesis_max_tokens=40000):
    """The live API call sequence for one character's full Pass 2
    resolution -- TWO calls now, not one: synthesize_character_arc()
    first, then this call's own per-beat resolution, with the first
    call's output injected as fixed context via build_pass2_system_
    blocks(). Same API-key-from-environment-only discipline as every
    other live call in this project -- never accepted as an argument,
    never written to a file or transcript.

    target_beat_ids, when given, restricts the RESOLUTION call (call 2)
    to producing beat_resolutions entries for only this beat_id subset
    -- e.g. re-resolving a handful of previously-flagged beats without
    regenerating (and needing an exact match against) a whole
    character's worth of entries. synthesize_character_arc (call 1) is
    NEVER restricted -- the arc synthesis is always whole-character, it
    IS the trajectory. The resolution call's evidence section is also
    left untouched (still the full arc) even when targeting a subset:
    only the closing instruction in the UNCACHED user message is
    restricted (see build_pass2_user_message), never the cached system
    block, so resolving different subsets across calls doesn't bust the
    system-prompt cache. Every id in target_beat_ids must actually be
    one of this character's beats -- checked before spending anything
    on a live call.

    Returns (raw_response_text, expected_beat_ids, arc_synthesis) --
    the synthesis is returned too so callers can report/inspect it
    without a third call. expected_beat_ids is target_beat_ids (sorted
    via beat_id_sort_key) when given, else every beat for this character.

    max_tokens=40000, revised UP from an initial 8000 after a real
    diagnostic failure on Richard (this project's largest character by
    presence -- 130 beats, ~35K input tokens): the model used extended
    thinking without being asked to, consumed the entire 8000-token
    budget on thinking alone, and returned zero output tokens --
    stop_reason=max_tokens with no text block at all. Same failure
    shape plot_facts_extraction.py already documented for whole-script
    reads ('an insufficient budget truncates the actual JSON output
    mid-array rather than failing cleanly') -- here more extreme,
    truncating BEFORE any output began. Revisit this number if a
    smaller-presence character still hits the cap, or lower it once a
    character's real needed budget is known instead of guessed.

    arc_synthesis, when given, skips call 1 and injects that synthesis
    instead -- it must be the dict this function (or
    synthesize_character_arc) returned for the SAME character on the
    SAME data. Added for chunked characters: the resolution call can't
    fit a very large arc in one response (DANNY, 169 beats, truncated at
    40000), so the arc is resolved in target_beat_ids chunks, and without
    this every chunk re-paid the whole-arc synthesis (cache_read=0 on
    both calls in practice). Save the synthesis from the first chunk and
    pass it to the rest, so all chunks are checked against one trajectory.
    synthesis_max_tokens is passed through to synthesize_character_arc;
    raise it for arcs large enough to strain its 40000 default."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set in the environment. Set it via an "
            "environment variable in your own shell before calling this, "
            "never paste a key into a script or a chat transcript."
        )
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("The 'anthropic' package is not installed. Run: "
                            "pip install anthropic --break-system-packages")

    character_beats = gather_character_beats(analysis, character)
    if not character_beats:
        raise ValueError(f"No beats found where {character} is present.")

    target_beat_ids_sorted = None
    if target_beat_ids is not None:
        full_ids = {bid for bid, _ in character_beats}
        missing = [bid for bid in target_beat_ids if bid not in full_ids]
        if missing:
            raise ValueError(
                f"target_beat_ids contains beat_id(s) not present for {character}: {missing}"
            )
        target_beat_ids_sorted = sorted(target_beat_ids, key=beat_id_sort_key)

    # Call 1: dedicated arc synthesis, mirroring plot_facts_extraction.py -- always whole-arc.
    # Skipped when a saved synthesis for this character is injected (chunked runs).
    if arc_synthesis is None:
        arc_synthesis = synthesize_character_arc(analysis, character, model=model,
                                                 max_tokens=synthesis_max_tokens)
    elif not isinstance(arc_synthesis.get("synthesis"), list) or not isinstance(arc_synthesis.get("turning_points"), list):
        raise ValueError("arc_synthesis must be a dict with 'synthesis' and 'turning_points' lists "
                         "(the shape synthesize_character_arc returns)")

    # Call 2: per-beat resolution, with Call 1's output injected as given context
    client = anthropic.Anthropic(api_key=api_key)
    system_blocks = build_pass2_system_blocks(arc_synthesis)
    user_message = build_pass2_user_message(character, character_beats, target_beat_ids=target_beat_ids_sorted)
    user_message += "\n\nRespond with ONLY the JSON object. No markdown code fences, no preamble, no explanation."

    # Streaming required by the SDK at this max_tokens -- a non-streaming
    # call risks exceeding the client's 10-minute timeout ceiling and is
    # refused outright before ever making the request. Discovered via a
    # real ValueError on the first live pilot attempt, not anticipated
    # in advance.
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        response = stream.get_final_message()
    _print_usage_and_cost(f"{character} resolution call", response.usage)
    text_parts = [block.text for block in response.content if block.type == "text"]
    raw = "".join(text_parts)
    expected_ids = target_beat_ids_sorted if target_beat_ids_sorted is not None else [bid for bid, _ in character_beats]
    return raw, expected_ids, arc_synthesis


def run_pass2_pilot(analysis, character, model="claude-sonnet-5"):
    """NON-DESTRUCTIVE. Snapshots this character's CURRENT (human-
    verified) weight_proportionality/characterization_consistency as
    ground truth, makes a fresh live call as if Pass 2 had never been
    done, and reports a hit-rate comparison. Never writes to `analysis`.

    Reads ground truth from THIS character's own ArchetypeTag.causal_
    integrity, not from any shared beat-level field -- required after
    the per-character migration; reading a beat-level field here would
    silently compare the model's Richard-specific prediction against
    whichever character's data happened to be stored there, which is
    exactly the bug this migration fixed.

    This is the tool for the actual pilot test: run this on RICHARD
    first, since his Pass 2 was fully human-verified this session --
    a real, checkable ground truth, not a guess at what a model 'should'
    produce. Only after reviewing this report does using
    apply_pass2_results() on an unverified character make sense."""
    character_beats = gather_character_beats(analysis, character)
    ground_truth = {}
    for beat_id, bt in character_beats:
        tag = _find_character_tag(bt, character)
        ci = tag.causal_integrity if tag else None
        ground_truth[beat_id] = {
            "weight_proportionality": ci.weight_proportionality if ci else None,
            "characterization_consistency": ci.characterization_consistency if ci else None,
        }

    raw, expected_ids, arc_synthesis = call_claude_for_pass2(analysis, character, model=model)
    success, beats_result = parse_pass2_response(raw, expected_ids)
    if not success:
        return {"error": beats_result, "raw_response": raw, "synthesis": arc_synthesis}

    matches, mismatches = [], []
    for beat_id in expected_ids:
        gt = ground_truth[beat_id]
        pred = beats_result[beat_id]
        wp_match = gt["weight_proportionality"] == pred["weight_proportionality"]
        cc_match = gt["characterization_consistency"] == pred["characterization_consistency"]
        row = {
            "beat_id": beat_id,
            "ground_truth": {
                "weight_proportionality": gt["weight_proportionality"].value if gt["weight_proportionality"] else None,
                "characterization_consistency": gt["characterization_consistency"].value if gt["characterization_consistency"] else None,
            },
            "predicted": {
                "weight_proportionality": pred["weight_proportionality"].value,
                "characterization_consistency": pred["characterization_consistency"].value,
            },
            "checked_against": pred["checked_against"],
            "rationale": pred["rationale"],
            "wp_match": wp_match, "cc_match": cc_match,
        }
        (matches if (wp_match and cc_match) else mismatches).append(row)

    total = len(expected_ids)
    full_match = len(matches)
    return {
        "character": character,
        "synthesis": arc_synthesis["synthesis"],
        "turning_points": arc_synthesis["turning_points"],
        "total_beats": total,
        "full_match_count": full_match,
        "full_match_rate": round(full_match / total, 3) if total else None,
        "matches": matches,
        "mismatches": mismatches,
    }


def apply_pass2_results(analysis, character, raw_json_text, corrections_list=None, target_beat_ids=None):
    """Writes model output onto THIS character's own ArchetypeTag.
    causal_integrity within each beat -- NOT a shared beat-level
    field. This is the actual fix for the overwrite bug this whole
    migration exists to prevent: writing here can never clobber a
    different character's causal_integrity in a shared beat, because
    each character now has their own slot. Creates a bare
    CausalIntegrityTag on the character's tag if one didn't already
    exist (e.g. a beat where this character was present but never
    previously assessed).

    target_beat_ids, when given, must be the SAME subset (or a subset
    of it) passed to the call_claude_for_pass2() call that produced
    raw_json_text -- restricts expected_ids/validation to just this
    beat set instead of the character's full arc, so only these beats
    get written. beats_by_id is still built from the full
    gather_character_beats() regardless, since it's just a lookup table
    and every target beat is necessarily in it.

    Logs each as a Correction with human_value=None (explicitly NOT
    auto-confirmed) -- awaiting actual human review, same discipline
    as every other correction in this project.

    Use this only for characters with no ground truth to pilot-test
    against -- for anything where a human-verified answer already
    exists, use run_pass2_pilot() instead and don't overwrite it."""
    character_beats = gather_character_beats(analysis, character)
    if target_beat_ids is not None:
        full_ids = {bid for bid, _ in character_beats}
        missing = [bid for bid in target_beat_ids if bid not in full_ids]
        if missing:
            raise ValueError(
                f"target_beat_ids contains beat_id(s) not present for {character}: {missing}"
            )
        expected_ids = sorted(target_beat_ids, key=beat_id_sort_key)
    else:
        expected_ids = [bid for bid, _ in character_beats]
    success, beats_result = parse_pass2_response(raw_json_text, expected_ids)
    if not success:
        raise ValueError(f"Pass 2 response rejected: {beats_result}")

    beats_by_id = dict(character_beats)
    for beat_id, resolution in beats_result.items():
        bt = beats_by_id[beat_id]
        tag = _find_character_tag(bt, character)
        if tag is None:
            continue  # character has no per_character entry at all in this beat -- shouldn't happen, skip defensively
        if tag.causal_integrity is None:
            tag.causal_integrity = CausalIntegrityTag()
        old_wp = tag.causal_integrity.weight_proportionality
        old_cc = tag.causal_integrity.characterization_consistency
        tag.causal_integrity.weight_proportionality = resolution["weight_proportionality"]
        tag.causal_integrity.characterization_consistency = resolution["characterization_consistency"]
        if resolution["contradiction_trace"]:
            tag.causal_integrity.contradiction_trace = resolution["contradiction_trace"]
        if corrections_list is not None:
            corrections_list.append({
                "beat_id": beat_id,
                "field_name": "causal_integrity (weight_proportionality + characterization_consistency)",
                "llm_value": [old_wp.value if old_wp else None, old_cc.value if old_cc else None],
                "human_value": None,  # explicitly not human-confirmed yet
                "character": character,
                "notes": f"Pass 2 LLM draft, AWAITING HUMAN REVIEW (checked_against: {resolution['checked_against']}): {resolution['rationale']}",
            })
    return beats_result
