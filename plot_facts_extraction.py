"""
plot_facts_extraction.py -- the dedicated whole-script read pass that
populates PlotFact objects BEFORE any beat-level archetype tagging
begins. This is the formalized version of what was done by hand for
Ocean's Eleven: reading the entire script once, extracting objective
structural facts (staged vs. genuine, cover identities, confirmed
mechanical reveals), so beat-level tagging never has to guess at
information that's only knowable from the whole story.

Reusable across any script, not tied to this one -- follows the same
discipline as llm_orchestration.py: strict schema validation, a
malformed response is rejected and retried rather than silently
accepted, and the API key is read ONLY from the environment.

CRITICAL DESIGN CHOICE: the extraction prompt is built from the
ALREADY-PARSED scene data, labeled with the PARSER's own internal
scene_id -- never from the raw script text, which only contains the
screenplay's own printed scene numbers. Those two numbering schemes
reliably diverge (confirmed repeatedly against Ocean's Eleven), and if
the model were shown raw text it would naturally reference the
script's own numbers, producing PlotFact.scope_scenes values that
silently don't match any real beat_id. Labeling with the internal
scene_id from the start means the model can only ever reference the
authoritative numbering -- no translation step, no room for mismatch.
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tagging_schema import PlotFact


SCOPE_TEST_INSTRUCTIONS = """
You are reading this ENTIRE screenplay, start to finish, before any
beat-by-beat analysis begins -- the way a careful human reader forms a
complete mental model of a story before judging any single moment in
it. Your ONLY job is to extract a narrow category of OBJECTIVE,
STRUCTURAL facts about the story's own construction.

=== THE SCOPE TEST (read carefully -- this is deliberately narrow) ===

A fact belongs in your output ONLY if it changes what CATEGORY an
observable action belongs to -- genuine vs. staged/performed -- not if
it merely describes an underlying feeling or motive. Three categories,
and nothing outside them:

1. STAGED VS. GENUINE ACTION -- any sequence where what's observably
   happening is deliberately different from what it's designed to look
   like WITHIN THE STORY (a con, a staged fight, a fake crisis, a
   fabricated emergency). Include this ONLY if the script itself
   eventually confirms it was performed -- never speculate.

2. IDENTITY/COVER CONTINUITY -- a character operating under a false
   name, disguise, or fabricated role that might recur in a LATER scene
   without being locally re-flagged as fake in that later scene's own
   text.

3. CONFIRMED FACTUAL REVEALS ABOUT OBJECTS OR EVENTS (not people) --
   something being swapped, planted, replicated, or already resolved
   before a later scene plays out, where a reader encountering only that
   later scene would have no way to know.

=== EXPLICITLY EXCLUDED -- DO NOT extract these ===

- A character's true feelings or private motive, even once eventually
  revealed. This is exactly the kind of fact that must stay scoped to
  where it's genuinely, textually shown in each individual scene --
  extracting it here would let hindsight retroactively recolor a
  character's earlier, authentic reactions, which is a real analytical
  error this scope test exists specifically to prevent.
- How a relationship emotionally resolves, or where a character's arc
  ends up.
- Anything not explicitly, textually confirmed by the script itself. A
  plausible guess or inference is NOT a fact. When in doubt, leave it
  out -- an incomplete list is far better than a speculative one.

=== A REAL WORKED EXAMPLE, showing why nuance matters ===

Two characters can be present in the same staged scene while only ONE
of them is complicit. If a scene shows a deliberately engineered
confrontation, but only ONE character is knowingly staging it and the
OTHER is a genuine, unwitting participant, your fact's "notes" field
MUST say so explicitly and name which character is and isn't complicit
-- do not let a scope note default to implying everyone present is in
on it. Flattening a genuine reaction into "staged" because it happens
inside a staged scene is exactly the error this distinction guards
against.

=== OUTPUT FORMAT ===

Respond with ONLY a JSON array, no markdown fences, no preamble:

[
  {
    "fact": "<the fact itself, written precisely, including who is and isn't complicit if relevant>",
    "category": "staged_vs_genuine" | "identity_cover" | "confirmed_reveal",
    "scope_scenes": [<list of integer scene_id values -- ONLY the internal SCENE N labels shown below, never any other numbering>],
    "confidence": "high" | "moderate" | "low",
    "notes": "<any nuance, especially who is/isn't complicit, or supporting textual evidence>"
  }
]

If you find no facts meeting this narrow scope, return an empty array
[]. An empty or short list is a correct, honest result if the story
genuinely doesn't contain this kind of content -- do not stretch to
find something.
"""


def build_script_content_for_extraction(parsed_scenes):
    """Assemble the full parsed script into one text block, each scene
    labeled ONLY with the parser's internal scene_id. Character cues are
    dropped (redundant with the speaker label already on each dialogue
    element) to keep the block as compact as possible without losing any
    actual content."""
    lines = []
    for scene in parsed_scenes:
        if not scene.get('elements'):
            continue
        lines.append(f"--- SCENE {scene['scene_id']} ---")
        for el in scene['elements']:
            if el['type'] == 'character_cue':
                continue
            speaker = f"{el.get('speaker')}: " if el.get('speaker') and el['type'] == 'dialogue' else ''
            lines.append(f"{speaker}{el['text']}")
    return "\n".join(lines)


def build_plot_facts_extraction_prompt(parsed_scenes):
    script_content = build_script_content_for_extraction(parsed_scenes)
    return (
        SCOPE_TEST_INSTRUCTIONS
        + "\n\n=== FULL SCRIPT (scenes labeled with their SCENE N id -- "
          "use ONLY these numbers in scope_scenes) ===\n\n"
        + script_content
    )


def parse_plot_facts_response(raw_json_text):
    """Strictly parse and validate an extraction response. Returns
    (success: bool, result_or_error) -- result is list[PlotFact] on
    success, an error string on failure. A malformed response is
    rejected, never silently accepted, same discipline as
    llm_orchestration.parse_llm_response."""
    try:
        cleaned = raw_json_text.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned
            if cleaned.rstrip().endswith('```'):
                cleaned = cleaned.rstrip()[:-3]
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    if not isinstance(data, list):
        return False, f"Expected a JSON array, got {type(data).__name__}"

    valid_categories = {"staged_vs_genuine", "identity_cover", "confirmed_reveal"}
    valid_confidence = {"high", "moderate", "low"}

    try:
        facts = []
        for i, item in enumerate(data):
            if item.get("category") not in valid_categories:
                return False, f"Item {i}: invalid category {item.get('category')!r}"
            if item.get("confidence", "high") not in valid_confidence:
                return False, f"Item {i}: invalid confidence {item.get('confidence')!r}"
            scope = item.get("scope_scenes", [])
            if not isinstance(scope, list) or not all(isinstance(s, int) for s in scope):
                return False, f"Item {i}: scope_scenes must be a list of integers, got {scope!r}"
            facts.append(PlotFact(
                fact=item["fact"], category=item["category"],
                scope_scenes=scope,
                confidence=item.get("confidence", "high"),
                notes=item.get("notes", ""),
            ))
    except (KeyError, TypeError) as e:
        return False, f"Malformed item: {e}"

    return True, facts


def call_claude_for_plot_facts_extraction(parsed_scenes, model="claude-sonnet-5", max_tokens=20000):
    """The live extraction call. Same API-key discipline as
    llm_orchestration.py: read ONLY from ANTHROPIC_API_KEY, never
    accepted as an argument.

    max_tokens defaults much higher than a single beat-tagging call
    (3000) -- confirmed via real testing that a whole-script read
    invites substantial extended-thinking token usage (over 7000 tokens
    of thinking alone on the first real Ocean's Eleven run), and an
    insufficient budget truncates the actual JSON output mid-array
    rather than failing cleanly. Do not lower this without re-testing."""
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

    client = anthropic.Anthropic(api_key=api_key)
    prompt = build_plot_facts_extraction_prompt(parsed_scenes)

    response = client.messages.create(
        model=model, max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text_parts = [block.text for block in response.content if block.type == "text"]
    return "".join(text_parts)


def extract_plot_facts(parsed_scenes, model="claude-sonnet-5"):
    """Convenience wrapper: real API call -> strict parse/validate ->
    return the resulting list[PlotFact]. Raises if the response doesn't
    validate -- malformed extraction output is rejected, never silently
    accepted as a partial or best-effort result. Caller is responsible
    for reviewing the result (this is a DRAFT, same as any LLM-produced
    beat tag -- confidence is marked per-fact, but nothing here should
    be treated as final without a human pass)."""
    raw = call_claude_for_plot_facts_extraction(parsed_scenes, model=model)
    success, result = parse_plot_facts_response(raw)
    if not success:
        raise ValueError(f"Plot-facts extraction response rejected: {result}")
    return result
