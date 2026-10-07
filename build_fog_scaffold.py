"""
build_fog_scaffold.py -- cold-run scaffold for Full of Grace, adapted from
build_oceans11_scaffold.py.

Pipeline, all structural (no archetype judgment, no LLM call):
  1. pdftotext -layout "full_of_grace.pdf" fog_full.txt
     (-layout is mandatory; see parser.py's module docstring)
  2. parser.parse_script(fog_full.txt) + fog_hand_patches.py
                                              -> fog_parsed_scenes.json
  3. beat_detector.package_scene_for_interpretation() per scene
                                              -> fog_scaffold.json

Every beat stores full source_evidence (turns, evidence, preceding
context), so later audits can check exactly what the tagger saw. LOTB and
WHTBD never stored this (LOTB_WHTBD_OPEN_ITEMS.md item 3).

Differences from the Ocean's Eleven builder:
- reads/writes UTF-8 explicitly;
- runs the parser itself from fog_full.txt, then applies
  fog_hand_patches.py (dual-dialogue blocks, headstone text);
- records the source PDF and extraction command in ScriptVersion.

Every beat starts untagged (per_character=[]). Nothing here makes any
archetype judgment; it only organizes evidence.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tagging_schema import ScriptAnalysis, ScriptVersion, BeatTag
from beat_detector import package_scene_for_interpretation
import parser as script_parser
from fog_hand_patches import apply_hand_patches

SOURCE_PDF = 'full_of_grace.pdf'
RAW_PATH = 'fog_full.txt'
PARSED_PATH = 'fog_parsed_scenes.json'
SCAFFOLD_PATH = 'fog_scaffold.json'


def build_beat_id(scene_id, beat_number):
    return f"scene{scene_id}_beat{beat_number}"


def build_scaffold(raw_path=RAW_PATH, parsed_path=PARSED_PATH, output_path=SCAFFOLD_PATH):
    with open(raw_path, 'r', encoding='utf-8') as f:
        scenes = script_parser.parse_script(f.read())
    patched = apply_hand_patches(scenes)
    print(f"Hand patches applied to scenes: {patched}")
    with open(parsed_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)

    version = ScriptVersion(
        title="Full of Grace",
        stage="mid-development draft",
        identifying_features=[
            "written by Shane O'Connor",
            f"source: {SOURCE_PDF} (126 pages)",
            f'extracted with: pdftotext -layout "{SOURCE_PDF}" {raw_path}',
        ],
    )
    analysis = ScriptAnalysis(version)

    total_beats = 0
    low_signal_scenes = 0
    prev_beat_last_turn_text = None  # for preceding_context across beat/scene boundaries

    for scene in scenes:
        scene_id = scene.get('scene_id')
        if not scene.get('elements'):
            continue

        packaged = package_scene_for_interpretation(scene)
        if packaged.get('scene_level_flag'):
            low_signal_scenes += 1

        for beat in packaged['beats']:
            beat_id = build_beat_id(scene_id, beat['beat_number'])
            preceding = [prev_beat_last_turn_text] if prev_beat_last_turn_text else None

            source_evidence = {
                'characters_present': beat['characters_present'],
                'turns': beat['turns'],
                'evidence': beat['evidence'],
                'suspense_evidence': beat['suspense_evidence'],
                'preceding_context': preceding,
                # carried through for audit/triage, not read by evidence_summary()
                'confidence_flag_from_detector': beat['confidence_flag'],
                'scene_level_flag': packaged.get('scene_level_flag'),
            }

            analysis.beats[beat_id] = BeatTag(
                beat_id=beat_id,
                scene_id=scene_id,
                per_character=[],
                source_evidence=source_evidence,
            )
            total_beats += 1

            if beat['turns']:
                last_turn = beat['turns'][-1]
                prev_beat_last_turn_text = {
                    'kind': last_turn['kind'],
                    'speaker': last_turn['speaker'],
                    'text': last_turn['text'],
                }

    analysis.save(output_path)

    print(f"Scaffold built: {total_beats} beats across {len(scenes)} scenes.")
    print(f"Scenes flagged LOW_SIGNAL (needs full human/LLM read, not just beat flags): {low_signal_scenes}")
    print(f"Saved to {output_path}")
    return analysis


if __name__ == '__main__':
    build_scaffold()
