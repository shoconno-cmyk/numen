"""
fog_plot_facts_runner.py -- run the recovered plot_facts_extraction.py
on Full of Grace, POST-HOC (2026-10-03, after the cold run).

These facts did NOT exist when the cold run tagged FOG (fog_tagged.json's
plot_facts was empty then, so fog_tagging_harness.py injected nothing).
They must never be read as having informed the cold-run tags. Every
stored fact's notes carries that provenance.

Modes (run from the repo root):
  python fog_plot_facts_runner.py --dry-run   # free: prompt size + exact input
                                              # token count (count_tokens) + cost cap check
  python fog_plot_facts_runner.py --run       # ONE billed call, then store

--run goes through the module's own call path
(plot_facts_extraction.call_claude_for_plot_facts_extraction: same
prompt, model, max_tokens). The only addition is a thin wrapper that
records the API response so usage/cost can be reported -- the module
itself returns text only. The raw response and usage are written to
fog_plot_facts_call.json BEFORE parsing, so a rejected or truncated
response is never lost (see feedback: capture costly API output).

Changes ONLY fog_tagged.json's plot_facts. Refuses to run if plot_facts
is already populated, and verifies after saving that every other part of
the file is byte-identical to before.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plot_facts_extraction as pfe
from pass2_orchestration import _SONNET_5_INPUT_PER_MTOK, _SONNET_5_OUTPUT_PER_MTOK
from tagging_schema import ScriptAnalysis

ROOT = os.path.dirname(os.path.abspath(__file__))
SCENES_PATH = os.path.join(ROOT, "fog_parsed_scenes.json")
DATA_PATH = os.path.join(ROOT, "fog_tagged.json")
CALL_PATH = os.path.join(ROOT, "fog_plot_facts_call.json")
COST_CAP = 2.00
MODEL = "claude-sonnet-5"      # the module's default
MAX_TOKENS = 20000             # the module's default
RUN_DATE = "2026-10-03"

PROVENANCE = (f"[POST-HOC STAGE RUN {RUN_DATE}] Extracted by plot_facts_extraction.py "
              f"(recovered from Google Drive) on {RUN_DATE}, AFTER the FOG cold run. "
              "Not available to, and did not inform, any cold-run tag. LLM draft, not "
              "human-reviewed.")


def load_scenes():
    with open(SCENES_PATH, encoding="utf-8") as f:
        return json.load(f)


def cost_of(input_tokens, output_tokens):
    return (input_tokens / 1e6) * _SONNET_5_INPUT_PER_MTOK + (output_tokens / 1e6) * _SONNET_5_OUTPUT_PER_MTOK


def count_input_tokens(prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    r = client.messages.count_tokens(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return r.input_tokens


def preflight():
    scenes = load_scenes()
    prompt = pfe.build_plot_facts_extraction_prompt(scenes)
    print(f"scenes: {len(scenes)}  prompt chars: {len(prompt)}  "
          f"sha256: {hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]}")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        est_in = len(prompt) // 3.5
        print(f"ANTHROPIC_API_KEY not set: rough input estimate ~{int(est_in)} tokens "
              f"(chars/3.5), worst case ~${cost_of(est_in, MAX_TOKENS):.2f}")
        return scenes, prompt, None
    n_in = count_input_tokens(prompt)
    worst = cost_of(n_in, MAX_TOKENS)
    print(f"exact input tokens: {n_in}  worst-case cost (full {MAX_TOKENS} output): ${worst:.4f}  "
          f"cap ${COST_CAP:.2f}")
    return scenes, prompt, worst


def run():
    with open(DATA_PATH, encoding="utf-8") as f:
        before_raw = f.read()
    before = json.loads(before_raw)
    if before.get("plot_facts"):
        sys.exit(f"ABORT: fog_tagged.json already has {len(before['plot_facts'])} plot_facts; not overwriting")
    if os.path.exists(CALL_PATH):
        sys.exit(f"ABORT: {CALL_PATH} exists; a call was already made. Inspect it before re-running.")

    scenes, prompt, worst = preflight()
    if worst is None:
        sys.exit("ABORT: ANTHROPIC_API_KEY not set")
    if worst > COST_CAP:
        sys.exit(f"ABORT: worst-case ${worst:.4f} exceeds the ${COST_CAP:.2f} cap")

    # Record the response from the module's own call path.
    import anthropic
    captured = {}
    _Real = anthropic.Anthropic

    class _Recording(_Real):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            create = self.messages.create

            def recording_create(**kwargs):
                captured["request"] = {k: v for k, v in kwargs.items() if k != "messages"}
                resp = create(**kwargs)
                captured["response"] = resp
                return resp
            self.messages.create = recording_create

    anthropic.Anthropic = _Recording
    try:
        raw_text = pfe.call_claude_for_plot_facts_extraction(scenes)
    finally:
        anthropic.Anthropic = _Real

    resp = captured["response"]
    u = resp.usage
    cost = cost_of(u.input_tokens, u.output_tokens)
    record = {
        "run_date": RUN_DATE,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "module": "plot_facts_extraction.py (recovered from Google Drive, file dated 2026-08-15)",
        "input": "fog_parsed_scenes.json",
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "request": captured["request"],
        "model_returned": resp.model,
        "stop_reason": resp.stop_reason,
        "usage": {
            "input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
            "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", None),
            "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", None),
        },
        "cost_usd": round(cost, 4),
        "pricing": f"${_SONNET_5_INPUT_PER_MTOK}/M in, ${_SONNET_5_OUTPUT_PER_MTOK}/M out (pass2_orchestration.py constants)",
        "raw_text": raw_text,
    }
    with open(CALL_PATH, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"[USAGE] in={u.input_tokens} out={u.output_tokens} stop={resp.stop_reason} "
          f"cost=${cost:.4f} -- saved {CALL_PATH}")

    if resp.stop_reason != "end_turn":
        sys.exit(f"ABORT: stop_reason={resp.stop_reason}; nothing stored")
    ok, result = pfe.parse_plot_facts_response(raw_text)
    if not ok:
        sys.exit(f"ABORT: response rejected by parse_plot_facts_response: {result}; nothing stored")

    valid_ids = {s["scene_id"] for s in scenes}
    bad = [(i, sorted(set(pf.scope_scenes) - valid_ids)) for i, pf in enumerate(result)
           if set(pf.scope_scenes) - valid_ids]
    if bad:
        sys.exit(f"ABORT: facts reference scene_ids not in fog_parsed_scenes.json: {bad}; nothing stored")

    analysis = ScriptAnalysis.load(DATA_PATH)
    for pf in result:
        pf.notes = PROVENANCE + (" Model notes: " + pf.notes if pf.notes else "")
        analysis.add_plot_fact(pf)
    for bt in analysis.beats.values():
        bt.validate()
    analysis.save(DATA_PATH)

    with open(DATA_PATH, encoding="utf-8") as f:
        after = json.load(f)
    for k in before:
        if k != "plot_facts" and before[k] != after[k]:
            sys.exit(f"INTEGRITY FAILURE: {k} changed; restore with git checkout fog_tagged.json")
    print(f"stored {len(result)} plot facts; every other key unchanged")
    for i, pf in enumerate(result):
        print(f"{i:2} [{pf.category} / {pf.confidence}] scenes {pf.scope_scenes}: {pf.fact}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if args.dry_run:
        preflight()
    else:
        run()
