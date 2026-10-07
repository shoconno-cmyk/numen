"""
fog_pass2_runner.py -- Pass 2 (weight_proportionality,
characterization_consistency) on Full of Grace, using
pass2_orchestration.py. DOES NOT RUN ON IMPORT; every live mode spends
real money and needs ANTHROPIC_API_KEY in the environment.

Modes:
  python fog_pass2_runner.py --plan              # no API calls: targets, chunks, sizes
  python fog_pass2_runner.py --synthesis TRUDY   # ONE synthesis call only (cheap token check)
  python fog_pass2_runner.py --run               # full run, resumable

Scope decisions (2026-09-28, author):
- Characters with 3+ beats only (MIN_BEATS). A whole-arc judgment on 1-2
  beats says too little to be worth a call.
- The synthesis call always sees the character's FULL arc (every beat
  with a per_character entry). Resolution targets only beats where the
  character's entry ALREADY has a causal_integrity block, so Pass 2 never
  creates a block on an entry that had none.
- Resolution is chunked (CHUNK_SIZE targets per call) so no response
  hits max_tokens (DANNY's 169-beat call truncated at 40000). The
  synthesis is computed once per character, saved, and injected into
  every chunk via call_claude_for_pass2(arc_synthesis=...).

Capture discipline: every synthesis and every raw resolution response is
written to OUT_DIR BEFORE parsing, so a parse failure never loses a paid
call. Results are applied with apply_pass2_results(); each written value
is also recorded in the corrections log with human_value=None and notes
"AWAITING HUMAN REVIEW" (same shape as Ocean's Eleven's pending
causal_integrity entries). Beat provenance is NOT touched --
log_correction() would mark beats llm_human_corrected, which a model
draft isn't. Everything written here is a draft for the human Pass 2
review phase.

Stale artifact: fog_pass2_calls/synthesis_TRUDY_v1.json predates
Principle 10 (echo needs the character's own evidence) and the
trait-statements-reflect-only-first_shown_beat_id instruction
(2026-09-29). Kept for comparison only -- never use it for resolution.
"""
import sys
import os
import json
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from tagging_schema import ScriptAnalysis, Correction, beat_id_sort_key
import pass2_orchestration as p2

DATA_PATH = os.path.join(_THIS_DIR, 'fog_tagged.json')
OUT_DIR = os.path.join(_THIS_DIR, 'fog_pass2_calls')
PROGRESS_PATH = os.path.join(OUT_DIR, 'progress.json')
MIN_BEATS = 3
CHUNK_SIZE = 60
SYNTHESIS_MAX_TOKENS = 64000


def _safe(name):
    return ''.join(c if c.isalnum() else '_' for c in name)


def plan(analysis):
    chars = sorted({t.character for bt in analysis.beats.values() for t in bt.per_character})
    rows = []
    for ch in chars:
        beats = p2.gather_character_beats(analysis, ch)
        if len(beats) < MIN_BEATS:
            continue
        targets = [bid for bid, bt in beats if p2._find_character_tag(bt, ch).causal_integrity is not None]
        chunks = [targets[i:i + CHUNK_SIZE] for i in range(0, len(targets), CHUNK_SIZE)]
        rows.append((ch, len(beats), targets, chunks))
    rows.sort(key=lambda r: -r[1])
    return rows


def synthesis_path(ch):
    return os.path.join(OUT_DIR, f'synthesis_{_safe(ch)}.json')


def get_synthesis(analysis, ch):
    """Load the saved synthesis for ch, or make ONE synthesis call and save it."""
    path = synthesis_path(ch)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    syn = p2.synthesize_character_arc(analysis, ch, max_tokens=SYNTHESIS_MAX_TOKENS,
                                      raw_save_path=os.path.join(OUT_DIR, f'synthesis_raw_{_safe(ch)}.json'))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(syn, f, indent=2, ensure_ascii=False)
    print(f'  saved {path}: {len(syn["synthesis"])} traits, {len(syn["turning_points"])} turning points')
    return syn


def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, encoding='utf-8') as f:
            return set(json.load(f))
    return set()


def save_progress(done):
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(sorted(done), f, indent=2)


def run():
    analysis = ScriptAnalysis.load(DATA_PATH)
    done = load_progress()
    for ch, n, targets, chunks in plan(analysis):
        if not targets:
            print(f'{ch}: no entries with a causal_integrity block, skipped')
            continue
        syn = get_synthesis(analysis, ch)
        for i, chunk in enumerate(chunks):
            key = f'{ch}|{i}'
            if key in done:
                continue
            print(f'{ch}: chunk {i + 1}/{len(chunks)} ({len(chunk)} beats)')
            raw, expected, _ = p2.call_claude_for_pass2(analysis, ch, target_beat_ids=chunk, arc_synthesis=syn)
            raw_path = os.path.join(OUT_DIR, f'resolution_{_safe(ch)}_{i}.json')
            with open(raw_path, 'w', encoding='utf-8') as f:
                json.dump({'character': ch, 'chunk': i, 'expected_ids': expected, 'raw_text': raw},
                          f, indent=2, ensure_ascii=False)
            pending = []
            p2.apply_pass2_results(analysis, ch, raw, corrections_list=pending, target_beat_ids=chunk)
            # Turning points validate_turning_points() kept as unverified
            # (finding 17) need a human check, whatever the draft says.
            unverified = {tp['beat_id']: tp['validation']
                          for tp in syn['turning_points'] if tp.get('validation')}
            for c in pending:
                if c['beat_id'] in unverified:
                    c['notes'] = (f"MANDATORY HUMAN REVIEW -- unverified turning point "
                                  f"({unverified[c['beat_id']]}). " + c['notes'])
                analysis.corrections.append(Correction(
                    beat_id=c['beat_id'], field_name=c['field_name'], llm_value=c['llm_value'],
                    human_value=None, character=c['character'], notes=c['notes']))
            for bt in analysis.beats.values():
                bt.validate()
            analysis.save(DATA_PATH)
            done.add(key)
            save_progress(done)
            print(f'  applied {len(pending)} drafts; saved')
    print('run complete')


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    args = sys.argv[1:]
    if args[:1] == ['--plan']:
        a = ScriptAnalysis.load(DATA_PATH)
        rows = plan(a)
        tot_t = sum(len(r[2]) for r in rows)
        print(f'{len(rows)} characters with {MIN_BEATS}+ beats; {tot_t} target entries; '
              f'{sum(len(r[3]) for r in rows)} resolution calls + {len(rows)} synthesis calls')
        for ch, n, targets, chunks in rows:
            print(f'  {ch:18s} beats={n:3d} targets={len(targets):3d} chunks={len(chunks)}')
    elif args[:1] == ['--synthesis'] and len(args) == 2:
        get_synthesis(ScriptAnalysis.load(DATA_PATH), args[1])
    elif args[:1] == ['--run']:
        run()
    else:
        print(__doc__)
