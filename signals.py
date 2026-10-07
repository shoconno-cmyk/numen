"""
Beat-boundary signal prototype: signals 1-4 (structural/formatting,
action-interrupting-dialogue, pacing/length, repetition/hesitation).

These are all textually-grounded, non-semantic signals -- deliberately
NOT a sentiment model or LLM read. Goal is to see how much of a real
beat structure emerges just from formatting/pacing the writer already
put on the page.
"""

import re

EMPHASIS_PARENS = (
    'beat', 'pause', 'quietly', 'quiet', 'softly', 'silence', 'urgent',
    'urgently', 'explodes', 'shouting', 'shouts', 'screaming', 'whispers',
    'whisper', 'suddenly', 'gently', 'sharply', 'coldly', 'breaking',
    'choked', 'tears'
)

REPEATED_WORD_RE = re.compile(r'\b(\w+)\b[,]?\s+\1\b', re.IGNORECASE)


def signal_formatting_emphasis(text, nearby_parenthetical=None):
    """Signal 1: ellipses, trailing dashes, and emphasis-flavored
    parentheticals the writer used to cue delivery.

    Ellipsis check covers BOTH a trailing "..." (a line that trails off)
    AND an embedded mid-sentence "..." (a meaningful pause before the
    real blow -- e.g. "If you ever disrespect my wife again...I will
    end you"). The trailing-only version missed this shape entirely;
    a threat delivered after a pause is exactly the kind of formatting
    emphasis this signal exists to catch."""
    score = 0
    reasons = []
    stripped = text.strip()
    if '...' in stripped:
        score += 1
        if stripped.endswith('...'):
            reasons.append('trails off (...)')
        else:
            reasons.append('embedded pause (...)')
    if stripped.endswith('--') or stripped.endswith('-'):
        score += 1
        reasons.append('cut off (--)')
    if nearby_parenthetical:
        p = nearby_parenthetical.lower()
        for kw in EMPHASIS_PARENS:
            if kw in p:
                score += 1
                reasons.append(f'parenthetical cues "{kw}"')
                break
    return score, reasons


# Bounded, narrow vocabulary of body-language/emotional-tell language --
# physical action that reveals an INTERNAL state, as opposed to routine
# physical/game mechanics (chasing a ball, opening a door). Same spirit
# as EMPHASIS_PARENS: a specific list, not a broad heuristic, chosen to
# avoid the overcorrection trap hit repeatedly in the parser work.
PHYSICAL_EMOTION_TELLS = (
    'closes his eyes', 'closes her eyes', 'closes their eyes',
    'trembles', 'trembling', 'flinches', 'flinch', 'freezes', 'freeze',
    'recoils', 'recoil', 'collapses', 'collapse', 'clenches', 'clench',
    'jerks away', 'jerks back', 'shakes his head', 'shakes her head',
    'stares', 'stare', 'dark smile', 'smiles a dark',
    'horrified', 'terrified', 'furious', 'devastated', 'sobbing',
    'sobs', 'weeps', 'weeping', 'gasps', 'gasp', 'shaking',
    'tears well', 'breaks down', 'lowers the', 'goes pale', 'grips',
    'afraid', 'scared', 'petrified', 'panicked', 'screaming', 'screams',
    'by the throat', 'grabs', 'grabbed', 'helpless', 'strangles',
    'slams', 'shoves', 'shoved', 'pins', 'pinned', 'lunges'
)


def signal_interrupting_action(is_action, is_mid_dialogue, text=''):
    """Signal 2 (revised): an action interrupting dialogue is only
    meaningful if it ALSO describes an emotional tell, not just any
    physical business. Structural position alone fires constantly in a
    naturally physical scene (kids playing street hockey generate
    action-interrupts-dialogue as a byproduct of the content itself,
    not because anything emotionally significant is happening) --
    confirmed as a real false-positive source in testing. Requiring
    both position AND emotionally-expressive content fixes this
    without abandoning the underlying insight (a director/writer
    choosing to interrupt dialogue to SHOW something is deliberate)."""
    if not (is_action and is_mid_dialogue):
        return 0, []
    lowered = text.lower()
    for tell in PHYSICAL_EMOTION_TELLS:
        if tell in lowered:
            return 1, [f'action interrupts dialogue w/ emotional tell ("{tell}")']
    return 0, []


def signal_pacing_contraction(prev_word_count, curr_word_count):
    """Signal 3: utterances getting shorter/terser than what preceded
    them often tracks rising emotional pressure (long speech -> clipped
    exchange)."""
    if prev_word_count is None:
        return 0, []
    if prev_word_count >= 6 and curr_word_count <= 3:
        return 1, ['sharp contraction in utterance length']
    return 0, []


def signal_repetition(text):
    """Signal 4: repeated words/stammering ("Yeah, yeah"), or trailing
    fragment ("I remember, man. I --") as textual tells of emotional
    strain."""
    score = 0
    reasons = []
    if REPEATED_WORD_RE.search(text):
        score += 1
        reasons.append('word repetition (stammer/emphasis)')
    return score, reasons


def word_count(text):
    return len(text.split())


# --- Signals 5-6: lightweight sentiment (VADER), not an LLM read ---
# Validated against two real scenes of different emotional shape
# (confrontation-under-pressure, Shadow-emergence): strong convergent
# hits with the structural signals above, plus real independent catches
# structural signals alone missed entirely (sustained-intensity beats
# with no formatting tell). Known ceiling: content-cued emotion is
# mostly covered by magnitude; restraint-cued emotion and cross-scene
# narrative significance are NOT reachable by any of signals 1-6 --
# see design note for why that's a deliberate, not accidental, limit.

_analyzer = None


def _get_analyzer():
    global _analyzer
    if _analyzer is None:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def compound_sentiment(text):
    return _get_analyzer().polarity_scores(text)['compound']


def signal_sentiment_delta(prev_compound, curr_compound, threshold=0.5):
    """Signal 5: a large swing in valence between consecutive turns --
    catches SUDDEN shifts. Blind to sustained intensity (two consecutive
    dark turns show a small delta even if both carry real weight) --
    that gap is what signal 6 is for."""
    if prev_compound is None:
        return 0, []
    delta = abs(curr_compound - prev_compound)
    if delta >= threshold:
        return 1, [f'sentiment delta {delta:.2f}']
    return 0, []


def signal_sentiment_magnitude(curr_compound, threshold=0.5):
    """Signal 6: raw sentiment intensity of a turn on its own, regardless
    of its neighbors -- catches sustained-intensity beats that delta
    alone misses (e.g. a turn embedded in an already-dark stretch)."""
    if abs(curr_compound) >= threshold:
        return 1, [f'sentiment magnitude {curr_compound:.2f}']
    return 0, []
