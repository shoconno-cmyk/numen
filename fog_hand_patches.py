"""
fog_hand_patches.py -- targeted, documented fixes for Full of Grace
parse errors that parser.py cannot resolve on its own. Per-script, not a
parser.py change -- same approach as oceans11_hand_patches.py.

Apply AFTER parse_script(), before beat detection (build_fog_scaffold.py
does this).

1. Side-by-side simultaneous dialogue (4 blocks). pdftotext -layout keeps
   both columns but interleaves them on each text line, so the parser
   reads one merged two-name cue with the two speakers' words mixed
   together. The split below was taken from fog_full.txt by column
   position, and no word straddles the column boundary. The left column
   comes first, matching oceans11_hand_patches.py. Scene 75's block is
   not recognized as a cue at all; the parser folded it into action, so
   neither line was attributed to anyone.

2. Headstone text (scene 46). The inscription's last line, "PARENTS OF
   JOHN & TRUDY", passes as a character cue, so the next action line
   became its "dialogue". Both are restored to action.

Each patch checks the exact parsed elements it expects before changing
anything, and raises if the parse has drifted. A silent no-op would leave
the misattribution in place with nothing to show for it.
"""

APOS = '’'


def _cue(name, text=None):
    return {'type': 'character_cue', 'speaker': name, 'text': text or name}


def _dlg(name, text):
    return {'type': 'dialogue', 'speaker': name, 'text': text}


def _act(text):
    return {'type': 'action', 'speaker': None, 'text': text}


# (scene_id, [expected (type, text) of the elements being replaced], replacement elements)
PATCHES = [
    (46,
     [('character_cue', 'PARENTS OF JOHN & TRUDY'),
      ('dialogue', 'Pull back to a freshly-dug grave, and John, alone, in suit and tie, '
                   'sitting in the grass next to his parents headstone.')],
     [_act('PARENTS OF JOHN & TRUDY'),
      _act('Pull back to a freshly-dug grave, and John, alone, in suit and tie, '
           'sitting in the grass next to his parents headstone.')]),

    (75,
     [('action', f'YOUNG JOHN                        MACKIE (CONT{APOS}D) His dad let him use the boat.  '
                 'Operating a watercraft while'),
      ('action', 'under the influence.')],
     [_cue('YOUNG JOHN'), _dlg('YOUNG JOHN', 'His dad let him use the boat.'),
      _cue('MACKIE', f'MACKIE (CONT{APOS}D)'),
      _dlg('MACKIE', 'Operating a watercraft while under the influence.')]),

    (120,
     [('character_cue', f'JOHN                CAPTAIN MARCHAND (CONT{APOS}D)'),
      ('dialogue', f'You can{APOS}t -- Why would you?    She is a girl of tender There{APOS}s no known '
                   'interstate    years, 12 and under -- they transportation -- if you just  can monitor '
                   f'interstate travel let me, sir, give me some      -- they{APOS}ll share with us more '
                   'time--                    intel on other kidnapping situations --')],
     [_cue('JOHN'),
      _dlg('JOHN', f'You can{APOS}t -- Why would you? There{APOS}s no known interstate transportation -- '
                   'if you just let me, sir, give me some more time--'),
      _cue('CAPTAIN MARCHAND', f'CAPTAIN MARCHAND (CONT{APOS}D)'),
      _dlg('CAPTAIN MARCHAND', 'She is a girl of tender years, 12 and under -- they can monitor '
                               f'interstate travel -- they{APOS}ll share with us intel on other '
                               'kidnapping situations --')]),

    (140,
     [('character_cue', f'YOUNG JOHN                       MACKIE (CONT{APOS}D)'),
      ('dialogue', f'No! Oh fuck! No! No, no, no!  Jesus, John, it{APOS}s okay. Hey,'),
      ('action', 'calm down.')],
     [_cue('YOUNG JOHN'), _dlg('YOUNG JOHN', 'No! Oh fuck! No! No, no, no!'),
      _cue('MACKIE', f'MACKIE (CONT{APOS}D)'),
      _dlg('MACKIE', f'Jesus, John, it{APOS}s okay. Hey, calm down.')]),

    (143,
     [('character_cue', f'JOHN (CONT{APOS}D)                       TRUDY'),
      ('dialogue', 'You better watch what you            With a drug problem that dad always '
                   'looked the other way say!                                 on!')],
     [_cue('JOHN', f'JOHN (CONT{APOS}D)'), _dlg('JOHN', 'You better watch what you say!'),
      _cue('TRUDY'), _dlg('TRUDY', 'With a drug problem that dad always looked the other way on!')]),
]


def apply_hand_patches(scenes):
    by_id = {s['scene_id']: s for s in scenes}
    applied = []
    for scene_id, expected, replacement in PATCHES:
        els = by_id[scene_id]['elements']
        starts = [i for i in range(len(els) - len(expected) + 1)
                  if all(els[i + k]['type'] == t and els[i + k]['text'] == txt
                         for k, (t, txt) in enumerate(expected))]
        if len(starts) != 1:
            raise RuntimeError(f"fog hand patch for scene {scene_id}: expected elements found "
                               f"{len(starts)} times (need exactly 1); the parse has changed")
        i = starts[0]
        els[i:i + len(expected)] = [dict(e) for e in replacement]
        by_id[scene_id].setdefault('hand_patched', []).append('fog_hand_patches.py')
        applied.append(scene_id)
    return applied
