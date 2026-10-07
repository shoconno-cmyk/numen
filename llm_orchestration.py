"""
llm_orchestration.py -- the layer that actually calls an LLM to
perform the judgment step, strictly bound to the tagging_schema.py
vocabulary. The LLM acts as an INTERPRETER, not a free-form component:
its output must validate against the fixed enums exactly as a human's
would, via the same from_dict() constructors used everywhere else in
this project. A response that doesn't match the vocabulary isn't a
disagreement to weigh -- it's a malformed response to reject and retry,
the same way Linkage.validate() already rejects an unratified
analytically_discovered entry regardless of who produced it.

NOTE: this module builds and validates around LLM responses but does
NOT make a live API call itself -- no API credentials are available in
this environment. The prompt-construction and response-parsing/
validation logic is real and tested (with a simulated response,
exactly the way save/load was tested before a second live session
existed to prove it against). Wiring in a live call is a small, later
step once credentials are available -- swap the simulated response for
a real API call; nothing else in this module needs to change.
"""

import sys
import os
import json
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from tagging_schema import (
    ArchetypeTag, Provenance,
    ArchetypeTagKind, ChainSoundness, WeightProportionality,
    AgencyAlignment, CharacterizationConsistency, ConfidenceFlag,
    BIG_SEVEN_DEFINITIONS, GENERAL_TAGGING_PRINCIPLES,
)
from integration import evidence_summary


def _format_archetype_definitions():
    """Render BIG_SEVEN_DEFINITIONS as prompt text. Fix for a real gap:
    VOCABULARY_INSTRUCTIONS below only lists the seven enum NAMES the
    JSON response must use -- it never told the model what any of them
    actually MEAN. Every hard-won refinement to these definitions (the
    domain test, the for-another test, the child-development principles,
    the caregiving-under-strain distinction, and everything else worked
    out across LOTB/WHTBD/GWH/Babadook) lives in tagging_schema.py's
    BIG_SEVEN_DEFINITIONS and was going completely unseen by the model.
    Pulling it in here means any script using this module gets the full,
    current calibration automatically -- nothing script-specific."""
    lines = [GENERAL_TAGGING_PRINCIPLES, "",
              "=== THE BIG SEVEN -- READ CAREFULLY BEFORE TAGGING ==="]
    for name, definition in BIG_SEVEN_DEFINITIONS.items():
        lines.append(f"\n{name}: {definition}")
    return "\n".join(lines)


VOCABULARY_INSTRUCTIONS = """
You must respond with valid JSON matching this exact schema. Every
enum field below MUST use one of the listed values EXACTLY as written
(case-sensitive) -- any other value will be rejected, not interpreted.

{
  "per_character": [
    {
      "character": "<name, must match a name present in the evidence>",
      "archetypes": ["Hero"|"Shadow"|"Trickster"|"Mentor"|"Great Mother"|"Chorus"|"Persona", ...]
        -- OR, if there is genuinely insufficient evidence for ANY archetype:
      "kind": "no_confident_archetype",
        -- OR, if the character is causally significant but has no personal/
           psychological grounding (a faceless institutional function):
      "kind": "functional_role_only", "embodies": "<what it embodies, e.g. institutional Shadow>",
      "self_perceived": ["<how the character understands their own action>"],
      "audience_perceived": ["<how the audience is likely to read it>"],
      "emotion": ["<layered/compound, e.g. multiple co-occurring emotions>"],
      "goal": "<free text, or 'goalless' if genuinely none>",
      "goal_status": "achieved"|"violated"|"deferred"|"none",
      "agency_role": "active"|"passive",
      "causal_integrity": {
        "weight_proportionality": "matched"|"mismatch"|"requires_second_pass",
        "agency_alignment": "aligned"|"displaced",
          -- MUST be resolved to "aligned" or "displaced" in THIS pass. No other values exist;
             there is NO "requires_second_pass" option for agency_alignment.
        "displacement_mechanism": {"enabling_character": "<who actually makes the outcome happen>",
                                   "convenient_capability": "<the capability that lets them do it>"},
          -- REQUIRED whenever agency_alignment is "displaced" (a response with "displaced" and no
             displacement_mechanism is rejected). OMIT it when agency_alignment is "aligned".
        "characterization_consistency": one of the following, chosen carefully --
          "consistent" -- this beat matches THIS CHARACTER's established pattern directly, nothing notable
          "contradicted" -- this beat requires a trait/state INCOMPATIBLE with what's established for THIS
                            CHARACTER, appearing suddenly with no gradual buildup, often only explicable by
                            something OUTSIDE the story's own logic (e.g. a production note)
          "throughline_evolution" -- THIS CHARACTER's underlying trait itself has genuinely CHANGED,
                            gradually, with a clear in-story trigger, explicable entirely within the story,
                            and persists afterward
          "boundary_revealed" -- THIS CHARACTER has NOT changed at all; a previously-untested LIMIT of an
                            already-consistent, long-established trait is being exposed for the first time,
                            specifically because the story has generated pressure severe enough to locate it
          "requires_second_pass" -- you don't have enough of THIS CHARACTER's full arc to judge this yet
        "contradiction_trace": {"suspected_external_note": "<free text>", "craft_evidence": ["<free text>", ...]},
          -- REQUIRED whenever characterization_consistency is "contradicted" (a response with
             "contradicted" and no contradiction_trace is rejected). OMIT it otherwise.
      }
        -- OMIT causal_integrity entirely for a character whose presence in this beat is
           too thin/minor to warrant causal-integrity scrutiny at all (matches "kind":
           "no_confident_archetype" for most such characters, but the two are independent --
           an archetype-tagged character can still validly omit causal_integrity, and vice versa)
    }
  ],
  "chain_soundness": "intact"|"broken"|"undetermined"
    -- BEAT-LEVEL, not per-character: is the plot's own causal mechanics sound in this
       beat, independent of any single character's psychology. Omit if not assessable
       from this beat alone.
}

CRITICAL, LEARNED FROM REAL DATA LOSS: weight_proportionality and
characterization_consistency are PER CHARACTER, never shared across
everyone present in a beat. Two characters in the identical beat can
legitimately receive DIFFERENT values -- e.g. one character's reaction
is proportionate to the stakes (matched) while another's, in that same
moment, is not (mismatch). Do not default to one shared read for the
whole beat.

IMPORTANT: weight_proportionality and characterization_consistency can
ONLY be resolved (not left as requires_second_pass) if you have been
given the FULL script's later beats for THAT CHARACTER specifically.
If you are only seeing this beat in isolation during a first pass,
default both to "requires_second_pass" for every character -- do not
guess.
"""


def _format_canonical_names_instructions(canonical_names, name_aliases=None):
    """Character-name discipline, carried forward from every prior
    harness (LOTB/WHTBD/GWH/Babadook) into this reusable module. Without
    this, the model has no way to know the fixed cast list and will
    happily invent inconsistent name variants across beats -- breaking
    continuity/registry tracking downstream, which depends on exact
    string matches.

    name_aliases (optional): a dict mapping an alternate name/spelling
    the SOURCE TEXT actually uses to the one canonical name it should
    always be tagged as -- e.g. a script that alternates between a
    character's first and last name across different scenes. This is a
    recurring, not one-off, screenplay phenomenon (confirmed across
    multiple scripts in this project), so it belongs here as a proper
    parameter rather than being worked around per-script."""
    names_list = ", ".join(canonical_names)
    parts = [
        "=== CHARACTER NAMES ===\n"
        f"For a character on this list, use EXACTLY this string, verbatim, "
        f"matching case and punctuation. Never invent a fuller name, never "
        f"re-case an existing one, even if the beat's own text uses a "
        f"nickname or partial name: {names_list}\n\n"
        "If a character present in the beat is NOT on this list (a minor "
        "or unnamed character -- a guard, a dealer, a stranger identified "
        "only by role), do NOT force them onto a name from the list above "
        "just because it's the closest match. Instead use their exact "
        "functional descriptor in ALL CAPS as it would appear as a script "
        "character cue (e.g. GUARD, DEALER, PIT BOSS). A name from the "
        "list appearing in a line of DIALOGUE (someone saying \"Danny's "
        "plan\") does not mean that entity is the character speaking or "
        "acting in this beat -- only tag a canonical name when that "
        "character is physically present and doing something in the "
        "beat's own turns, never merely because their name was spoken."
    ]
    if name_aliases:
        alias_lines = "\n".join(
            f'  - "{alt}" is the SAME character as "{canon}" -- the script '
            f'itself uses both across different scenes. Always tag as '
            f'"{canon}" regardless of which name the evidence shows.'
            for alt, canon in name_aliases.items()
        )
        parts.append(f"\n\nKNOWN NAME ALIASES (same character, inconsistent naming "
                      f"in the source text itself):\n{alias_lines}")
    return "".join(parts)


def _format_plot_facts(plot_facts):
    """Render the scoped PlotFact list for one beat. Explicitly labeled
    as OMNISCIENT/SETTLED to distinguish it from REGISTRY CONTEXT below,
    which is deliberately 'as of this beat' -- the model needs to
    understand these are two different kinds of context with different
    rules: plot facts are always true within their scope regardless of
    story position, registry context evolves and must not be read
    backward into earlier beats."""
    lines = [
        "=== ESTABLISHED PLOT FACTS (omniscient -- true throughout this "
        "beat's scope regardless of story position; these are NOT "
        "something to discover, they are settled) ===",
        "These describe what KIND of event is objectively occurring -- "
        "staged vs. genuine, a cover identity, a confirmed mechanical "
        "reveal. They do NOT tell you how any character genuinely FEELS "
        "in this beat -- a plot fact that an event is staged does not "
        "mean every character present is complicit or insincere (see "
        "notes on individual facts below for exactly who is and isn't "
        "in on it, when specified).",
        "KNOWING vs. TAGGING -- a critical distinction: these facts let "
        "you correctly INTERPRET action that is actually depicted in "
        "this beat's own evidence (e.g. recognizing that a shouted "
        "warning IS a performance, because the warning itself is right "
        "there in the text). They must NEVER be used to assert an "
        "archetype for an action the beat's own evidence does not "
        "depict at all. If a plot fact establishes that a character "
        "later does something covert (plants an object, activates a "
        "device) but THIS beat's own turns show no sign of it -- no "
        "gesture, no aside, nothing a reader of just this beat could "
        "point to -- do not tag that character for it here. You may "
        "know it happened; you may not tag a beat for evidence that "
        "beat doesn't contain. Tag the beat where the action is "
        "actually shown, not every beat the omniscient fact happens to "
        "cover.",
    ]
    for pf in plot_facts:
        lines.append(f"- [{pf.category}] {pf.fact}" + (f" ({pf.notes})" if pf.notes else ""))
    return "\n".join(lines)


def build_system_blocks(canonical_names=None, name_aliases=None):
    """Assemble the STATIC portion of the prompt as a list of content
    blocks for the API's `system` parameter, with an ephemeral cache
    breakpoint on the final block -- character-name discipline, the
    full archetype definitions, and the fixed output vocabulary. This
    is IDENTICAL on every single beat-tagging call within one script
    (canonical_names and name_aliases don't change beat to beat), which
    is exactly what prompt caching needs: a large, byte-identical
    prefix that gets fully reused instead of reprocessed at full price
    on every call.

    Uses the 1-HOUR cache TTL ("ttl": "1h"), not the 5-minute default.
    Confirmed via a real usage-pattern finding, not a guess: this
    project's actual workflow runs batches interrupted by conversation,
    review, fund top-ups, and session breaks, and gaps between batches
    regularly exceed 5 minutes -- an org-level cache-hit-rate alert
    from Anthropic surfaced this directly. The 5-minute default would
    force a fresh (more expensive) cache WRITE at the start of most
    batches instead of a cheap cache READ, even though the underlying
    mechanism is otherwise working correctly (verified live: within a
    tight batch loop, calls do hit the cache). The 1-hour write costs
    2x base input rate instead of 1.25x, but reads stay equally cheap
    either way -- worth it specifically because THIS workflow's gaps
    are usually well under an hour, even when they exceed 5 minutes.

    Deliberately excludes plot_facts, evidence, and registry_context --
    those vary per beat (different beats see different scoped subsets
    of plot facts), so folding them in here would fragment the cache
    into many small, rarely-reused entries instead of one large,
    consistently-reused one. Per Anthropic's own documented guidance,
    genuinely static instructions belong in `system`, not embedded in
    the user message -- this isn't just a caching optimization, it's
    the structurally correct place for this content regardless."""
    parts = [
        "You are tagging ONE beat of a screenplay for archetype and "
        "causal-integrity analysis. You never compute a judgment "
        "mechanically -- you read the beat's actual text and reason "
        "about motive, consequence, and psychology, the same way a "
        "human story analyst would. Read the character-name rules and "
        "archetype definitions below; the specific beat you're tagging, "
        "any established plot facts, and registry context will follow "
        "in the next message. Produce your judgment strictly in the "
        "required JSON format described below.",
        "",
    ]
    if canonical_names:
        parts.append(_format_canonical_names_instructions(canonical_names, name_aliases))
        parts.append("")
    parts += [
        _format_archetype_definitions(),
        "",
        "=== REQUIRED OUTPUT FORMAT ===",
        VOCABULARY_INSTRUCTIONS,
    ]
    system_text = "\n".join(parts)
    return [
        {"type": "text", "text": system_text, "cache_control": {"type": "ephemeral", "ttl": "1h"}},
    ]


def build_user_message(beat_tag, registry_context=None, plot_facts=None):
    """Assemble the DYNAMIC, per-beat portion: established plot facts
    scoped to this beat, algorithmic evidence, and registry context
    (throughline as-of this beat, not final state). Never cached --
    this changes on every single call by design."""
    parts = []
    if plot_facts:
        parts.append(_format_plot_facts(plot_facts))
        parts.append("")
    parts += [
        "=== ALGORITHMIC EVIDENCE (textual patterns only -- not meaning) ===",
        evidence_summary(beat_tag),
        "",
    ]
    if registry_context:
        parts.append("=== REGISTRY CONTEXT (established BEFORE this beat) ===")
        for character, info in registry_context.items():
            parts.append(f"{character}: {info}")
        parts.append("")
    parts.append("Tag this beat now, in the required JSON format.")
    return "\n".join(parts)


def build_tagging_prompt(beat_tag, registry_context=None, canonical_names=None,
                          name_aliases=None, plot_facts=None):
    """DEBUG/PREVIEW ONLY -- returns the full prompt as one flat string
    by concatenating the system and user portions, for manual
    inspection. The live API call path (call_claude_for_tagging) does
    NOT use this function -- it calls build_system_blocks() and
    build_user_message() separately and sends them as distinct
    system/messages parameters, which is what actually enables caching.
    Kept for anyone who wants to see/log the complete prompt as text."""
    system_blocks = build_system_blocks(canonical_names, name_aliases)
    user_message = build_user_message(beat_tag, registry_context, plot_facts)
    return system_blocks[0]["text"] + "\n\n" + user_message


def _self_correct_misplaced_non_tag_values(per_character_data):
    """Known, recurring model failure (confirmed across GWH, WHTBD, and
    now Ocean's 11): a non-tag verdict -- 'ordinary_reaction',
    'no_confident_archetype', 'functional_role_only' -- shows up as a
    string INSIDE the 'archetypes' list instead of in the separate
    'kind' field the schema actually requires. The older per-script
    harnesses in this project self-corrected this rather than treating
    it as a rejection worth burning a retry on; porting that same fix
    here so the shared module doesn't regress on an already-solved
    problem."""
    NON_TAG_VALUES = {"no_confident_archetype", "functional_role_only", "ordinary_reaction"}
    for t in per_character_data:
        archetypes = t.get("archetypes") or []
        if not t.get("kind") and len(archetypes) == 1 and archetypes[0] in NON_TAG_VALUES:
            t["kind"] = archetypes[0]
            t["archetypes"] = []
    return per_character_data


def parse_llm_response(raw_json_text, beat_id):
    """Strictly parse and validate an LLM's response against the fixed
    schema. Returns (success: bool, result_or_error).

    On success: result is (per_character: list[ArchetypeTag] -- each
    carrying its OWN causal_integrity now, not shared across the beat
    -- chain_soundness: Optional[ChainSoundness], the one genuinely
    beat-level axis).
    On failure: result is a string describing exactly what was
    invalid -- itself useful telemetry, distinct from a substantive
    correction (this is 'the LLM violated the schema', not 'the LLM's
    judgment was wrong but validly formatted')."""
    try:
        cleaned = raw_json_text.strip()
        if cleaned.startswith('```'):
            # strip a leading ```json / ``` fence and trailing ``` -- a
            # common real-world quirk even when explicitly told not to
            cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned
            if cleaned.rstrip().endswith('```'):
                cleaned = cleaned.rstrip()[:-3]
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    try:
        raw_per_character = _self_correct_misplaced_non_tag_values(data.get("per_character", []))
        per_character = [ArchetypeTag.from_dict(t) for t in raw_per_character]
        for tag in per_character:
            tag.validate()
    except (ValueError, KeyError) as e:
        return False, f"Invalid per_character data: {e}"

    chain_soundness = None
    if data.get("chain_soundness"):
        try:
            chain_soundness = ChainSoundness(data["chain_soundness"])
        except ValueError as e:
            return False, f"Invalid chain_soundness value: {e}"

    return True, (per_character, chain_soundness)


def _append_call_log(call_log_path, record):
    """One JSON object per line, appended and flushed immediately, so a
    crash or interruption mid-run never loses a billed response."""
    import json
    with open(call_log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()


def call_claude_for_tagging(beat_tag, registry_context=None, canonical_names=None, name_aliases=None,
                             plot_facts=None, model="claude-sonnet-5", max_tokens=3000,
                             call_log_path=None):
    """The actual live API call. Reads the key ONLY from the
    ANTHROPIC_API_KEY environment variable -- never accepted as a
    function argument or hardcoded, so a key is never something that
    could end up captured in a script, a saved file, or a conversation
    transcript. Set it in your own shell/environment before running:
        export ANTHROPIC_API_KEY=sk-ant-...

    Returns the raw response text, UNPARSED -- pass it to
    parse_llm_response() or apply_llm_tagging() exactly as the
    simulated response was during testing. Nothing downstream of the
    API call changes; this function only replaces where the JSON text
    comes from.

    call_log_path (optional): when given, every call appends one JSON line
    to that file BEFORE this function returns: beat_id, UTC timestamp,
    model, request id, stop_reason, token usage (input, cache write,
    cache read, output) and the full raw response text. Every billed
    response is kept on disk even if parsing or applying it fails later
    (per the capture-costly-output rule). Leaving it unset keeps the old
    behaviour exactly."""
    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set in the environment. This function "
            "deliberately does not accept a key as an argument -- set it via "
            "an environment variable in your own shell before calling this, "
            "never paste a key into a script or a chat transcript."
        )

    try:
        import anthropic
    except ImportError:
        raise RuntimeError("The 'anthropic' package is not installed. Run: "
                            "pip install anthropic --break-system-packages")

    client = anthropic.Anthropic(api_key=api_key)
    system_blocks = build_system_blocks(canonical_names, name_aliases)
    user_message = build_user_message(beat_tag, registry_context, plot_facts)
    user_message += "\n\nRespond with ONLY the JSON object. No markdown code fences, no preamble, no explanation."

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": user_message}],
    )

    # Response content is a list of blocks; find the text block(s).
    text_parts = [block.text for block in response.content if block.type == "text"]
    raw_text = "".join(text_parts)

    if call_log_path:
        import datetime
        usage = response.usage
        _append_call_log(call_log_path, {
            "beat_id": beat_tag.beat_id,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "model": response.model,
            "request_id": getattr(response, "_request_id", None),
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": usage.input_tokens,
                "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", None),
                "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", None),
                "output_tokens": usage.output_tokens,
            },
            "max_tokens": max_tokens,
            "raw_text": raw_text,
        })

    return raw_text


def call_and_apply(beat_tag, registry_context=None, canonical_names=None, name_aliases=None,
                    plot_facts=None, model="claude-sonnet-5", call_log_path=None):
    """Convenience wrapper: real API call -> strict parse/validate ->
    apply to the beat, provenance marked llm_unreviewed. Raises if the
    response doesn't validate against the schema -- a malformed
    response is rejected, never silently accepted."""
    raw_response = call_claude_for_tagging(beat_tag, registry_context, canonical_names, name_aliases,
                                            plot_facts, model=model, call_log_path=call_log_path)
    return apply_llm_tagging(beat_tag, raw_response)


def apply_llm_tagging(beat_tag, raw_json_text):
    """Parse a validated LLM response directly onto a BeatTag, marking
    provenance as llm_unreviewed -- awaiting human confirmation or
    correction, never treated as final on its own. Each per_character
    entry carries its own causal_integrity already (set during
    ArchetypeTag.from_dict() inside parse_llm_response) -- nothing
    further to do for that part here."""
    success, result = parse_llm_response(raw_json_text, beat_tag.beat_id)
    if not success:
        raise ValueError(f"LLM response for {beat_tag.beat_id} rejected: {result}")
    per_character, chain_soundness = result
    beat_tag.per_character = per_character
    if chain_soundness:
        beat_tag.chain_soundness = chain_soundness
    beat_tag.provenance = Provenance.LLM_UNREVIEWED
    return beat_tag
