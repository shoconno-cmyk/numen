"""
suspense_signals.py -- textually-grounded suspense signals, distinct
from the emotion-driven beat signals in signals.py.

Discovered empirically against three real suspense scenes from two
different films (No Country for Old Men's coin-flip and hotel/chase
scenes, Training Day's poker/bathroom scene), specifically because the
existing sentiment-based signals were shown to be largely BLIND to two
of these scenes' suspense (both No Country scenes scored near-neutral
on valence despite being famously tense) -- suspense here isn't an
emotion-intensity phenomenon, it's built from conversational CONTROL,
narrated STILLNESS, and explicit VULNERABILITY -- three mechanisms
sentiment analysis has no way to see.

KNOWN CEILING (same posture as signals.py): the single largest driver
of suspense in all three scenes -- the AUDIENCE's prior knowledge of
just how dangerous the antagonist is -- is established in earlier
scenes and is NOT reachable by anything here. These signals catch the
textual techniques a scene uses to build suspense; they cannot supply
the audience-knowledge context those techniques are leaning on.
"""

import re

# --- Signal S1: cross-turn echo (weaponized repetition) ---
# A character repeating another character's own words/phrase back at
# them -- distinct from signals.py's repetition signal, which only
# looks for a word repeated WITHIN one line ("no, no, no"). This is
# about one speaker's words being echoed by a DIFFERENT speaker,
# often mockingly or controllingly.

_STOPWORDS = {
    'the', 'a', 'an', 'to', 'of', 'in', 'on', 'at', 'is', 'it', 'and',
    'or', 'but', 'you', 'i', 'me', 'my', 'your', 'we', 'he', 'she',
    'that', 'this', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'did', 'does', 'for', 'with', 'as', 'not', 'no', 'so', 'if',
    'what', 'who', 'how', 'well', 'just', 'know', 'don\'t', 'didn\'t',
}


def _content_bigrams(text):
    words = re.findall(r"[a-z']+", text.lower())
    bigrams = set()
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if w1 in _STOPWORDS and w2 in _STOPWORDS:
            continue
        bigrams.add((w1, w2))
    return bigrams


def signal_cross_turn_echo(current_kind, current_text, prev_kind, prev_text, current_speaker, prev_speaker):
    """S1: does the current turn echo a distinctive 2-word phrase from
    the immediately preceding DIFFERENT speaker's turn? Requires a
    multi-word match (not just one shared word) to avoid flagging
    ordinary topical continuity between adjacent lines.

    RESTRICTED TO DIALOGUE-TO-DIALOGUE comparisons only. Action turns
    always have speaker=None, so comparing an action turn against a
    dialogue turn would trivially satisfy "different speaker" without
    either one being an actual character talking -- echo-as-control is
    a conversational phenomenon between two people, not a coincidence
    of narration mentioning the same prop twice in adjacent sentences."""
    if current_kind != 'dialogue' or prev_kind != 'dialogue':
        return 0, []
    if not prev_text or current_speaker == prev_speaker:
        return 0, []
    prev_bigrams = _content_bigrams(prev_text)
    curr_bigrams = _content_bigrams(current_text)
    shared = prev_bigrams & curr_bigrams
    if shared:
        example = next(iter(shared))
        return 1, [f'echoes prior turn ("{example[0]} {example[1]}")']
    return 0, []


# --- Signal S2: refused closure ---
# A character explicitly tries to end an exchange/leave, and the
# scene keeps going without granting it. Detected as a bounded phrase
# list -- each occurrence is itself notable, since a closure attempt
# that doesn't succeed is a structural tell that someone is being
# held in the exchange against their will.

CLOSURE_ATTEMPT_PHRASES = (
    "need to go", "gotta go", "got to go", "have to go", "we're done",
    "we are done", "will there be anything else", "will there be something else",
    "need to close", "need to see about clos", "i should get going",
    "let's go", "lemme go", "let me go", "we're leaving", "i'm leaving",
    "gonna get going", "time to go",
)


def signal_refused_closure(text):
    """S2: a bounded phrase list for explicit attempts to end an
    exchange or leave. Flagged per-occurrence -- repeated attempts
    within one scene are themselves the suspense signature (someone
    trying and failing to disengage), which a beat-level count can
    surface without needing complex cross-turn state tracking."""
    lowered = text.lower()
    for phrase in CLOSURE_ATTEMPT_PHRASES:
        if phrase in lowered:
            return 1, [f'closure attempt ("{phrase}")']
    return 0, []


# --- Signal S3: standalone stillness markers ---
# "A beat." / "A long beat." / "Long beat. Stillness." appearing as
# their OWN freestanding action line -- not a parenthetical attached
# to dialogue (which signals.py already partially covers via
# EMPHASIS_PARENS), but a whole action sentence whose entire content
# IS the passage of tense, uncertain time. Functions like a held shot.

STILLNESS_MARKER_RE = re.compile(
    r'^(a\s+)?(long\s+)?(beat|pause|wait|stillness|silence|quiet)s?\.?\s*'
    r'(beat|pause|wait|stillness|silence|quiet)?\.?\s*$',
    re.IGNORECASE
)


def signal_stillness_marker(kind, text):
    """S3: an action-type turn whose entire text is a stillness marker,
    not embedded in a longer descriptive paragraph."""
    if kind != 'action':
        return 0, []
    stripped = text.strip()
    if len(stripped.split()) > 4:
        return 0, []
    if STILLNESS_MARKER_RE.match(stripped):
        return 1, ['standalone stillness marker']
    return 0, []


# --- Signal S4: vulnerability/isolation declarations ---
# Explicit statements that a character is outmatched, alone, or out
# of options -- distinct from restraint-cued or content-cued emotion,
# because the text is NOT withholding anything here; it states the
# vulnerability outright. The gap is that nothing in signals.py's
# vocabulary was built to recognize this specific category.

VULNERABILITY_PHRASES = (
    'outnumbered', 'outgunned', 'outsized', 'outmatched', 'outweighed',
    'defenseless', 'helpless', 'no way out', 'trapped', 'cornered',
    'abandoned', 'no choice', 'nothing he could do', 'nothing she could do',
    'all he could do', 'all she could do', 'left for dead', 'no one to help',
    'is gone', 'was gone', 'were gone',
)


def signal_vulnerability_declaration(text):
    """S4: bounded phrase list for explicit powerlessness/isolation
    statements. These are declarative, not subtle -- the writer is
    telling you directly that a character has no good options -- but
    nothing in the emotion-driven signal set looks for this category
    at all."""
    lowered = text.lower()
    for phrase in VULNERABILITY_PHRASES:
        if phrase in lowered:
            return 1, [f'vulnerability declaration ("{phrase}")']
    return 0, []
