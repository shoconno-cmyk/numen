"""
fog_tagging_harness.py -- the tagging driver for Full of Grace, the
project's fully-cold pipeline test. Adapted from lms_tagging_harness.py;
the batching, checkpoint/resume and call structure are unchanged. Only
CANONICAL_NAMES, NAME_ALIASES, the file paths and the per-call log differ.

Every live call appends one JSON line to CALL_LOG_PATH (usage: input,
cache write/read, output; request id; stop_reason; full raw response)
BEFORE the response is parsed or applied, so every billed response is
kept on disk even if applying it fails.

DOES NOT RUN ON IMPORT. Execution is gated behind __main__ and requires
an explicit run to start. Built and verified, held for greenlight.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tagging_schema import ScriptAnalysis, beat_id_sort_key
from llm_orchestration import call_claude_for_tagging, apply_llm_tagging

# Named characters, spelled exactly as their cues parse (post
# fog_hand_patches.py). Role-only speakers (FEDERAL AGENT, MANAGEMENT,
# PRIEST, OFFICER, ...) are deliberately left off; the prompt's standing
# rule tags them by their functional descriptor. The childhood versions
# are separate entries from their adult counterparts by author decision,
# not aliases.
CANONICAL_NAMES = [
    'JOHN', 'TRUDY', 'DOUG', 'REGGIE', 'CAPTAIN MARCHAND', 'CHEYENNE',
    'MACKIE', 'O’SHEA', 'PETE', 'BETH', 'RICARDO', 'ANGIE', 'SARGE',
    'RAYMOND', 'ANDY', 'KRISTA', 'FRANK', 'HOLLY', 'DET. MCAVOY',
    'ALBERTO', 'DR. SHEPHARD', 'MR. MURPHY', 'MRS. MURPHY',
    'YOUNG JOHN', 'YOUNG TRUDY', 'YOUNG CHEYENNE',
]

# Full names the script uses in action lines (character introductions,
# the headstone) for characters whose cues use the short form.
NAME_ALIASES = {
    'DETECTIVE JOHN KIERSTEAD': 'JOHN',
    'MACKENZIE “MACKIE” KIERSTEAD': 'MACKIE',
}

SCAFFOLD_PATH = 'fog_scaffold.json'
OUTPUT_PATH = 'fog_tagged.json'
PROGRESS_PATH = 'fog_tagged.json.progress.json'
CALL_LOG_PATH = 'fog_tagging_calls.jsonl'

# Pilot target set: the highest-risk material first, then a spread of
# ordinary dialogue beats. Run with: python fog_tagging_harness.py --pilot
PILOT_BEAT_IDS = [
    'scene0_beat1',     # OVER BLACK cold open (recovered by 6b03ed8; no speakers)
    'scene75_beat1',    # hand-patched dual dialogue: YOUNG JOHN / MACKIE
    'scene120_beat7',   # hand-patched dual dialogue: JOHN / CAPTAIN MARCHAND
    'scene140_beat2',   # hand-patched dual dialogue: YOUNG JOHN's half ...
    'scene140_beat3',   # ... MACKIE's half (the detector split the pair across beats)
    'scene143_beat7',   # hand-patched dual dialogue: JOHN / TRUDY
    'scene14_beat12',   # ordinary dialogue, early   (JOHN, SARGE, DET. MCAVOY)
    'scene53_beat2',    # ordinary dialogue, early   (JOHN, REGGIE)
    'scene86_beat4',    # ordinary dialogue, middle  (JOHN, DOUG)
    'scene122_beat5',   # ordinary dialogue, middle  (JOHN, PETE)
    'scene172_beat1',   # ordinary dialogue, late    (JOHN, REGGIE)
    'scene205_beat1',   # ordinary dialogue, late    (LAWYER, FEDERAL AGENT, DR. SHEPHARD)
]


def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()


def save_progress(done_ids):
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(sorted(done_ids), f)


def run_batch(max_beats=None, model="claude-sonnet-5", max_tokens=8000, beat_ids=None, dry_run=False):
    """Tag every untagged beat in the scaffold (or resume from wherever
    the sidecar progress file left off). Checkpoints every 10 beats.

    beat_ids: tag only these beats, in the order given. Every id must
    exist in the scaffold (raises otherwise, before any call). Beats
    already in the progress file are skipped, never re-billed. Tagged
    beats are recorded in the same progress file, so a later full run
    skips them.
    max_beats: cap on how many beats this call tags (applies after
    beat_ids filtering).
    dry_run: print the target list and stop, making no API calls."""
    src_path = OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else SCAFFOLD_PATH
    analysis = ScriptAnalysis.load(src_path)

    done = load_progress()
    if beat_ids is not None:
        unknown = [bid for bid in beat_ids if bid not in analysis.beats]
        if unknown:
            raise KeyError(f"beat_ids not in {src_path}: {unknown}")
        skipped = [bid for bid in beat_ids if bid in done]
        if skipped:
            print(f"Skipping {len(skipped)} already-tagged beat(s): {skipped}")
        target_ids = [bid for bid in beat_ids if bid not in done]
    else:
        target_ids = [bid for bid in sorted(analysis.beats.keys(), key=beat_id_sort_key) if bid not in done]
    if max_beats:
        target_ids = target_ids[:max_beats]

    if dry_run:
        print(f"DRY RUN (no API calls): would tag {len(target_ids)} beat(s), "
              f"model={model}, max_tokens={max_tokens}:")
        for bid in target_ids:
            print(f"  {bid}  present={analysis.beats[bid].source_evidence.get('characters_present')}")
        return analysis

    print(f"Full of Grace tagging run: {len(target_ids)} beats remaining "
          f"({len(done)} already done, {len(analysis.beats)} total).")
    print(f"Per-call log: {CALL_LOG_PATH}")

    succeeded, failed = 0, 0
    for i, beat_id in enumerate(target_ids, 1):
        bt = analysis.beats[beat_id]
        print(f"[{i}/{len(target_ids)}] Tagging {beat_id}...")
        try:
            raw = call_claude_for_tagging(
                bt, registry_context=None,
                canonical_names=CANONICAL_NAMES,
                name_aliases=NAME_ALIASES,
                plot_facts=analysis.plot_facts_for_scene(bt.scene_id),
                model=model,
                max_tokens=max_tokens,
                call_log_path=CALL_LOG_PATH,
            )
            apply_llm_tagging(bt, raw)
            done.add(beat_id)
            succeeded += 1
        except Exception as e:
            print(f"    FAILED: {e}")
            failed += 1

        if i % 10 == 0:
            analysis.save(OUTPUT_PATH)
            save_progress(done)
            print(f"    [checkpoint saved at beat {i}/{len(target_ids)}]")

    analysis.save(OUTPUT_PATH)
    save_progress(done)
    print(f"\nDone. {succeeded} succeeded, {failed} failed.")
    return analysis


if __name__ == '__main__':
    # python fog_tagging_harness.py                     -> full run (resumes)
    # python fog_tagging_harness.py --pilot             -> PILOT_BEAT_IDS only
    # python fog_tagging_harness.py --pilot --dry-run   -> show targets, no calls
    args = sys.argv[1:]
    run_batch(beat_ids=PILOT_BEAT_IDS if '--pilot' in args else None,
              dry_run='--dry-run' in args)
