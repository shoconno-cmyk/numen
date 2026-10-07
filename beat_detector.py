"""
beat_detector.py -- reusable beat-boundary candidate detection.

Consumes the parser's scene['elements'] output and produces a scored
list of "turns" (character_cue+dialogue pairs, or standalone action
blocks) flagged with candidate beat-boundary signals.

IMPORTANT SCOPE NOTE (see design note): this module does NOT claim to
detect emotion, archetypes, or beat boundaries with certainty. It
surfaces textually-grounded EVIDENCE of likely emotional shifts --
structural (signals 1-4) and lightweight sentiment (signals 5-6) --
so a human or LLM-assisted interpretive layer has well-organized
scaffolding instead of a flat wall of turns. Goal/Plan inference,
archetype classification, and causal-integrity judgment are explicitly
NOT attempted here.

Known ceiling (do not try to "fix" these here -- they are structural
limits of what this layer can see, not bugs):
 - content-cued emotion with no formatting tell: partially covered by
   sentiment magnitude, not fully solved
 - restraint-cued emotion (flat text made devastating by context):
   NOT reachable by any signal here, by design
 - cross-scene dramatic irony / narrative rhyme: requires whole-script
   context this module never has access to
"""

from signals import (
    signal_formatting_emphasis, signal_interrupting_action,
    signal_pacing_contraction, signal_repetition, word_count,
    compound_sentiment, signal_sentiment_delta, signal_sentiment_magnitude,
)
from suspense_signals import (
    signal_cross_turn_echo, signal_refused_closure,
    signal_stillness_marker, signal_vulnerability_declaration,
)


def extract_turns(scene_elements):
    """Flatten a scene's elements into a turn list: each character_cue
    is paired with its immediately-following parenthetical (if any) and
    ALL consecutive parenthetical+dialogue chunks that follow for that
    same speaker, up to the next character_cue or action element;
    standalone action blocks are their own turn.

    FIX (parenthetical-drop bugs -- found and repaired via the Little
    Miss Sunshine cold run, see that project's PARSING_BUG_IMPACT_REPORT.md):
    the previous version only ever consumed the FIRST parenthetical+
    dialogue pair after a cue. Real screenplay formatting regularly
    splits one speaker's line across multiple parenthetical-separated
    chunks ("CHARACTER (beat) Line one. (to someone) Line two."), and
    the old code silently dropped every chunk after the first with no
    trace -- confirmed 36 real instances script-wide on LMS, including
    the beat's defining Shadow-archetype evidence in one case. Since
    this file is the shared source for every script except LMS (which
    now has its own patched copy for unrelated reasons), any script
    tagged before this fix may have the same silent evidence gaps.
    Every parenthetical after the first is now inlined directly into
    'text' so no content is lost even for a consumer that only reads
    'text'; the FIRST parenthetical stays in the separate 'paren'
    field, unchanged, since that's what the emphasis-scoring signal
    reads."""
    turns = []
    i = 0
    els = scene_elements
    while i < len(els):
        el = els[i]
        if el['type'] == 'character_cue':
            j = i + 1
            first_paren = None
            if j < len(els) and els[j]['type'] == 'parenthetical':
                first_paren = els[j]['text']
                j += 1
            text_parts = []
            if j < len(els) and els[j]['type'] == 'dialogue':
                text_parts.append(els[j]['text'])
                j += 1
                while (j + 1 < len(els) and els[j]['type'] == 'parenthetical'
                       and els[j + 1]['type'] == 'dialogue'):
                    text_parts.append(els[j]['text'])       # subsequent parenthetical, inlined
                    text_parts.append(els[j + 1]['text'])   # the dialogue chunk it precedes
                    j += 2
            turns.append({
                'kind': 'dialogue',
                'speaker': el['speaker'],
                'text': ' '.join(text_parts),
                'paren': first_paren,
            })
            i = j
        elif el['type'] == 'action':
            turns.append({'kind': 'action', 'speaker': None, 'text': el['text'], 'paren': None})
            i += 1
        else:
            i += 1
    return turns


def score_turns(turns, mag_threshold=0.5, delta_threshold=0.5):
    """Score every turn against all six validated EMOTION signals, plus
    the four SUSPENSE signals (a distinct mechanism -- see design note:
    suspense is frequently invisible to sentiment, built instead from
    conversational control and narrated stillness). Both are attached
    to the same turn dict so a human or LLM sees all available
    textual evidence for a turn together, not split across two
    disconnected data structures."""
    prev_word_count = None
    prev_compound = None
    prev_text, prev_speaker, prev_kind = None, None, None
    scored = []

    for n, t in enumerate(turns):
        score = 0
        reasons = []

        is_mid = t['kind'] == 'action' and 0 < n < len(turns) - 1
        s, r = signal_interrupting_action(t['kind'] == 'action', is_mid, t['text'])
        score += s
        reasons += r

        s, r = signal_formatting_emphasis(t['text'], t.get('paren'))
        score += s
        reasons += r

        s, r = signal_repetition(t['text'])
        score += s
        reasons += r

        if t['kind'] == 'dialogue':
            wc = word_count(t['text'])
            s, r = signal_pacing_contraction(prev_word_count, wc)
            score += s
            reasons += r
            prev_word_count = wc
        else:
            prev_word_count = None

        compound = compound_sentiment(t['text'])
        s, r = signal_sentiment_delta(prev_compound, compound, delta_threshold)
        score += s
        reasons += r
        s, r = signal_sentiment_magnitude(compound, mag_threshold)
        score += s
        reasons += r
        prev_compound = compound

        # Suspense signals (weak/corroborating cross-turn echo included;
        # see design note on why echo alone can't disambiguate function)
        suspense_score = 0
        suspense_reasons = []
        s, r = signal_cross_turn_echo(t['kind'], t['text'], prev_kind, prev_text, t['speaker'], prev_speaker)
        suspense_score += s
        suspense_reasons += r
        s, r = signal_refused_closure(t['text'])
        suspense_score += s
        suspense_reasons += r
        s, r = signal_stillness_marker(t['kind'], t['text'])
        suspense_score += s
        suspense_reasons += r
        s, r = signal_vulnerability_declaration(t['text'])
        suspense_score += s
        suspense_reasons += r
        prev_text, prev_speaker, prev_kind = t['text'], t['speaker'], t['kind']

        scored.append({
            **t,
            'index': n,
            'compound': compound,
            'score': score,
            'reasons': reasons,
            'suspense_score': suspense_score,
            'suspense_reasons': suspense_reasons,
        })

    return scored


def detect_beat_boundaries(scene_elements, boundary_threshold=2, mag_threshold=0.5, delta_threshold=0.5):
    """End-to-end: scene elements in, scored turns out, with a boolean
    'is_boundary_candidate' flag for turns crossing the threshold.
    Threshold of 2 (multiple independent signals agreeing) was the
    level that produced real convergent hits in validation; a lone
    signal firing is kept visible but not flagged as a strong candidate."""
    turns = extract_turns(scene_elements)
    scored = score_turns(turns, mag_threshold, delta_threshold)
    for t in scored:
        t['is_boundary_candidate'] = t['score'] >= boundary_threshold
    return scored


def group_into_beats(scored_turns, break_threshold=2):
    """Group scored turns into discrete beat segments.

    DESIGN CHOICE: only STRONG turns (multiple independent signals
    converging, score >= break_threshold) become hard segment breaks.
    Weak (score==1) turns stay embedded INSIDE a segment as annotated
    evidence, not treated as a confident new-beat declaration.

    Why: forcing every flagged turn into a hard boundary would
    over-fragment a scene into dozens of micro-beats -- the opposite
    of the goal (hand the interpretive layer fewer, better-organized
    units). It also matches what testing showed: a lone signal is
    sometimes a real beat (sustained-intensity content) and sometimes
    pure noise (a kid yelling "Save!") -- multiple signals agreeing is
    the level that repeatedly held up across three different scenes.
    A strong turn CLOSES the segment it appears in (it's the
    culminating reaction); the next turn opens a new segment. Two
    strong turns back-to-back correctly produce a one-turn segment --
    validated case: the riverside confession (turn 12) and the
    knife-lowering action (turn 13) are adjacent, independently
    significant beats, not one beat.

    Returns a list of segments, each: {'turns': [...], 'closing_turn':
    the strong turn that ended it (or None if the scene ended without
    one), 'notable_turns': weak turns embedded inside}."""
    segments = []
    current = {'turns': [], 'closing_turn': None, 'notable_turns': []}

    for t in scored_turns:
        current['turns'].append(t)
        if t['score'] >= break_threshold:
            current['closing_turn'] = t
            segments.append(current)
            current = {'turns': [], 'closing_turn': None, 'notable_turns': []}
        elif t['score'] == 1:
            current['notable_turns'].append(t)

    if current['turns']:
        segments.append(current)

    return segments


def print_beat_segments(segments):
    for i, seg in enumerate(segments, 1):
        start = seg['turns'][0]['index']
        end = seg['turns'][-1]['index']
        print(f"--- BEAT {i} (turns {start}-{end}) ---")
        for t in seg['turns']:
            tag = ''
            if seg['closing_turn'] and t['index'] == seg['closing_turn']['index']:
                tag = ' [CLOSES BEAT]'
            elif t in seg['notable_turns']:
                tag = ' [notable]'
            print(f"  #{t['index']:2d} [{t['kind']:8}] {(t['speaker'] or ''):10} {t['text'][:65]}{tag}")
        print()


def package_scene_for_interpretation(scene, break_threshold=2, low_signal_scene_ratio=0.10):
    """The actual handoff contract to the interpretive layer (human or
    LLM-assisted archetype/causal-integrity pass).

    DESIGN PRINCIPLE: the algorithm reports EVIDENCE, never conclusions.
    Every beat carries its full turn text (structured, not flattened --
    speaker/kind/text preserved as in the original script), plus the
    exact signal evidence that justified where it was cut, so a human
    can see the reasoning and override it -- the same "flag, don't
    guess" posture that made the parser trustworthy.

    THE MOST IMPORTANT FIELD IS confidence_flag. A beat with zero
    signal evidence does NOT mean nothing emotionally significant
    happened -- it means the algorithm has no textual evidence either
    way. Four documented ceiling categories (content-cued, restraint-
    cued, character-state-dependent sincerity, cross-scene dramatic
    irony/trait-establishment) all produce exactly this signature: a
    real, important beat that scores flat. Silently treating a flat
    score as "nothing happened" would make this tool actively
    misleading rather than merely incomplete. So a signal-less beat is
    explicitly flagged for human/LLM review, not dropped or minimized.

    SCENE-LEVEL ROLLUP: some scenes are low-signal throughout -- not
    because nothing happens, but because a character's whole trait is
    affective flatness (e.g. Lou's negotiation scene, Nightcrawler:
    every turn scored zero, yet the scene is doing real characterization
    work). This is different from one quiet beat inside an otherwise
    eventful scene, and needs its own flag so the interpretive layer
    knows to read the WHOLE scene closely rather than trusting the
    absence of beat-level flags."""
    scored = detect_beat_boundaries(scene['elements'], boundary_threshold=1)
    segments = group_into_beats(scored, break_threshold=break_threshold)

    beats = []
    for i, seg in enumerate(segments, 1):
        turns_out = [
            {
                'index': t['index'], 'kind': t['kind'], 'speaker': t['speaker'], 'text': t['text'],
                'paren': t.get('paren'),
                'suspense_signals': t['suspense_reasons'] if t['suspense_score'] >= 1 else [],
            }
            for t in seg['turns']
        ]
        closing = seg['closing_turn']
        closing_evidence = None
        if closing:
            closing_evidence = {
                'turn_index': closing['index'], 'score': closing['score'], 'reasons': closing['reasons']
            }
        notable_evidence = [
            {'turn_index': t['index'], 'score': t['score'], 'reasons': t['reasons']}
            for t in seg['notable_turns']
        ]
        suspense_evidence = [
            {'turn_index': t['index'], 'suspense_score': t['suspense_score'], 'reasons': t['suspense_reasons']}
            for t in seg['turns'] if t['suspense_score'] >= 1
        ]
        has_any_evidence = bool(closing_evidence or notable_evidence or suspense_evidence)
        # Speaker-only by construction: non-speaking characters named in action lines are
        # never listed. A tagged beat's per_character is the authoritative cast list, not this.
        characters_present = sorted({t['speaker'] for t in seg['turns'] if t['speaker']})

        beats.append({
            'scene_id': scene.get('scene_id'),
            'slugline': scene.get('slugline'),
            'beat_number': i,
            'turns': turns_out,
            'evidence': {'closing_signal': closing_evidence, 'notable_signals': notable_evidence},
            'suspense_evidence': suspense_evidence,
            'characters_present': characters_present,
            'confidence_flag': 'algorithmic' if has_any_evidence else 'low_signal — needs human/LLM review',
        })

    # Scene-level rollup: what fraction of turns had ANY signal at all?
    total_turns = len(scored)
    signaled_turns = sum(1 for t in scored if t['score'] >= 1)
    signal_ratio = (signaled_turns / total_turns) if total_turns else 0
    scene_flag = None
    if total_turns > 0 and signal_ratio <= low_signal_scene_ratio:
        scene_flag = (
            f'LOW_SIGNAL_SCENE ({signaled_turns}/{total_turns} turns show any signal) — '
            'likely a restrained/affectively flat character or a deliberately '
            'underplayed scene; needs a full human/LLM read rather than relying '
            'on beat-level flags, which will under-detect here by design.'
        )

    # Suspense rollup: distinct from emotion signal_ratio, since a scene
    # can score low on emotion (restrained/flat) while still showing
    # real suspense-specific evidence (control, stillness, vulnerability),
    # or vice versa -- the two mechanisms are independent, not redundant.
    suspense_signaled = sum(1 for t in scored if t['suspense_score'] >= 1)
    suspense_ratio = (suspense_signaled / total_turns) if total_turns else 0

    return {
        'scene_id': scene.get('scene_id'),
        'slugline': scene.get('slugline'),
        'beats': beats,
        'scene_level_flag': scene_flag,
        'signal_ratio': round(signal_ratio, 3),
        'suspense_ratio': round(suspense_ratio, 3),
    }


def compute_scene_valence(scene_elements):
    """Emotional arc ("the wave") metric #1: aggregate emotional valence
    for one scene. Reuses the same per-turn VADER compound sentiment
    already validated for beat-boundary detection (signals 5-6) -- here
    aggregated across the whole scene instead of used for change-
    detection. This is the mechanism the original Scope decision called
    "the wave": a sentiment/valence-per-scene sequence meant to catch
    pacing problems ("this drags") rather than per-line nuance.

    Returns mean compound sentiment across all turns, plus min/max to
    preserve some sense of the scene's emotional RANGE, not just its
    average -- a scene that swings from very positive to very negative
    and nets out near zero is a different scene than one that's flat
    and neutral throughout, even though both might average to ~0."""
    turns = extract_turns(scene_elements)
    if not turns:
        return {'mean': 0.0, 'min': 0.0, 'max': 0.0, 'n_turns': 0}
    compounds = [compound_sentiment(t['text']) for t in turns if t['text'].strip()]
    if not compounds:
        return {'mean': 0.0, 'min': 0.0, 'max': 0.0, 'n_turns': 0}
    return {
        'mean': sum(compounds) / len(compounds),
        'min': min(compounds),
        'max': max(compounds),
        'n_turns': len(compounds),
    }


def compute_script_wave(scenes):
    """The wave across a whole script: ordered sequence of per-scene
    valence. Scenes with too little dialogue to be meaningful (title
    pages, single-line fragments) are skipped rather than diluting the
    wave with near-zero noise."""
    wave = []
    for scene in scenes:
        n_dialogue = sum(1 for el in scene['elements'] if el['type'] == 'dialogue')
        if n_dialogue < 2:
            continue
        valence = compute_scene_valence(scene['elements'])
        wave.append({
            'scene_id': scene.get('scene_id'),
            'slugline': scene.get('slugline'),
            **valence,
        })
    return wave


def print_wave(wave):
    """Simple ASCII sparkline of the emotional arc, for quick visual
    inspection -- not a substitute for real charting, just a fast way
    to eyeball the trajectory."""
    print(f"{'SCENE':6} {'MEAN':7} {'MIN':7} {'MAX':7} {'RANGE':7} SLUGLINE")
    print('-' * 90)
    for w in wave:
        rng = w['max'] - w['min']
        bar_pos = int((w['mean'] + 1) / 2 * 20)  # map [-1,1] to [0,20]
        bar = ' ' * bar_pos + '#'
        print(f"{w['scene_id']:<6} {w['mean']:7.3f} {w['min']:7.3f} {w['max']:7.3f} {rng:7.3f} "
              f"{str(w['slugline'])[:35]:35} |{bar}")


def print_report(scored_turns):
    """Diagnostic print, matching the format used during manual testing."""
    print(f"{'#':>2} {'KIND':8} {'SPEAKER':10} SCORE SIGNALS")
    print('-' * 100)
    for t in scored_turns:
        marker = '<<<' if t['is_boundary_candidate'] else ('<' if t['score'] == 1 else '')
        print(f"{t['index']:2d} {t['kind']:8} {(t['speaker'] or ''):10} {t['score']:5d} "
              f"{'; '.join(t['reasons']):45s}{marker}")
        print(f"     {t['text'][:90]}")
