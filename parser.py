"""
Numen: first-pass screenplay parser (prototype)

Goal: turn raw extracted script text into the slugline scaffold —
a list of scenes, each containing a sequence of classified elements
(action, character_cue, dialogue, parenthetical).

This is a PROTOTYPE. It's built against Mystic River specifically
and will need testing/tuning against the other 16 scripts before
we trust it as a general-purpose parser.

REQUIRED PDF EXTRACTION MODE: when the source script is a PDF, it
MUST be converted with `pdftotext -layout input.pdf output.txt`,
never the default (no-flag) mode. Confirmed on Lake of the
Brokenhearted: default-mode pdftotext silently reordered text for
short centered character cues sandwiched between dialogue blocks --
on the page a cue, a one-word line, a second cue and that second
speaker's line read correctly, but default extraction emitted the
first line ahead of its cue and the two cues back to back, which
corrupted speaker attribution
(dialogue lines got glued onto the wrong character's turn). This
produces no error and no obviously-malformed text -- it reads as
plausible dialogue, just attributed to the wrong speaker -- so it
is a silent correctness failure, not something the noise-stripping
or ambiguous-candidate logic in this file can detect or repair.
`-layout` preserves the PDF's visual column position, which fixes
this at the source. Always extract with `-layout` before handing
text to parse_script().
"""

import re

# Professionally-typeset PDFs (Final Draft, Word exports) commonly use a
# curly apostrophe (U+2019) instead of a straight one — "CONT'D" vs
# "CONT'D". A pattern hardcoded to the straight quote silently fails to
# strip the suffix, leaving speaker identity fragmented (same failure
# class as the earlier OCR V.O.-garbling bug, but triggered by clean,
# well-formatted text instead of scan noise). Match both.
APOSTROPHE_CHARS = "'’"
SUFFIX_STRIP_RE = re.compile(
    r'\([^)]*?(V\.O\.|O\.S.|CONT[' + APOSTROPHE_CHARS + r']?D)[^)]*\)',
    re.IGNORECASE
)

# Any other trailing parenthetical on a cue is a delivery or disguise note,
# not part of the name: "TRUDY (ON PHONE)", "TOM (INTO RADIO)",
# "TURK (TOURIST)". Left in, each one became a separate speaker (see
# LOTB_WHTBD_OPEN_ITEMS.md item 5, OCEANS11_OPEN_ITEMS.md items 18-19).
# Only used to derive the speaker name; is_character_cue() is unchanged.
TRAILING_PAREN_RE = re.compile(r'\s*\([^()]*\)\s*$')


def cue_speaker(cue_text):
    speaker = SUFFIX_STRIP_RE.sub('', cue_text).strip()
    while True:
        trimmed = TRAILING_PAREN_RE.sub('', speaker).strip()
        if trimmed == speaker or not trimmed:
            return speaker
        speaker = trimmed
import json

SLUGLINE_RE = re.compile(
    r'^\s*(?:[A-Z]{0,3}\d+[A-Z]{0,3}\s+)?(INT\.?|EXT\.?|INT\.?/EXT\.?|I/E\.?)[\s./-]+(.+)$',
    re.IGNORECASE
)

# A bare slugline (Nightcrawler-style: no INT./EXT. prefix at all) is
# nearly unambiguous when it ends in a time-of-day / continuity marker —
# no character is ever named "SOMETHING - NIGHT".
BARE_SLUGLINE_TIME_RE = re.compile(
    r'^([A-Z0-9 \'\-\.]{3,50})\s+-\s+'
    r'(DAY|NIGHT|MORNING|EVENING|DAWN|DUSK|LATER|CONTINUOUS|SAME TIME|MOMENTS LATER)$',
    re.IGNORECASE
)

# Bug V (The Babadook): the reverse of Bug U's slugline-wrap pattern -- the
# dash lands at the START of the continuation line ("- DAY") rather than
# the END of the original slugline line ("...OFFICE -"). Only ever applied
# when the current scene has zero elements yet (see usage below), since a
# bare "- DAY" deep into a scene's content would be a different situation.
LEADING_DASH_CONTINUATION_RE = re.compile(
    r'^-\s*(DAY|NIGHT|MORNING|EVENING|DAWN|DUSK|LATER|CONTINUOUS|SAME TIME|MOMENTS LATER)\.?\s*$',
    re.IGNORECASE
)

# Fallback signal: a short ALL-CAPS line containing a common location noun
# and NOT immediately followed by dialogue-shaped text. This is a weaker,
# lower-confidence heuristic than the time-suffix check above — it's a
# known limitation, not a guarantee, and should be reviewed by a human
# during the tagging pass rather than trusted blindly.
LOCATION_KEYWORDS = (
    'ROOM', 'HOUSE', 'STREET', 'APARTMENT', 'OFFICE', 'BAY', 'DESK',
    'GARAGE', 'SKYLINE', 'KITCHEN', 'CAR', 'BAR', 'PARK', 'BRIDGE',
    'HALL', 'STATION', 'LOT', 'BUILDING', 'WAREHOUSE', 'HOSPITAL',
    'SCHOOL', 'STORE', 'MARKET', 'YARD', 'DRIVEWAY', 'PORCH', 'RIVER',
    'DOCK', 'PIER', 'ALLEY', 'ROOFTOP', 'ELEVATOR', 'LOBBY', 'CHURCH',
    'DINER', 'MOTEL', 'HOTEL', 'JAIL', 'PRISON', 'COURT', 'STUDIO',
    'SET', 'NEWSROOM', 'DESK', 'EDITING', 'DOWNTOWN', 'CITY'
)

# Revision-page headers appear in the wild with wildly different exact
# wording ("TITLE - Rev. DATE PAGENUM.", "PAGENUM. Rev.-Color DATE",
# "Shooting Draft Color DATE PAGENUM.", "Revision Color DATE PAGENUM.")
# — same industry convention (WGA-standard revision colors), different
# phrasing every time. Rather than memorize each exact phrase, detect
# the underlying STRUCTURE: a revision/draft marker, a standard color
# name, and a date, appearing together regardless of order.
REVISION_COLOR_NAMES = (
    'WHITE', 'BLUE', 'PINK', 'YELLOW', 'GREEN', 'GOLDENROD', 'GOLD',
    'BUFF', 'SALMON', 'CHERRY', 'TAN'
)
REVISION_DATE_RE = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4}')
REVISION_MARKER_RE = re.compile(r'\bREV(?:ISION)?\.?\b|\bSHOOTING\s+DRAFT\b', re.IGNORECASE)
REVISION_COLOR_RE = re.compile(
    r'\b(?:' + '|'.join(REVISION_COLOR_NAMES) + r')\b', re.IGNORECASE
)


def is_revision_header(stripped):
    """Structural check, not phrase-matching: a short line containing a
    date plus either a revision/draft marker or a standard WGA revision
    color name is almost certainly page-layout noise, not story content —
    no real dialogue or action line is built this way."""
    if len(stripped) > 80:
        return False
    if not REVISION_DATE_RE.search(stripped):
        return False
    return bool(REVISION_MARKER_RE.search(stripped) or REVISION_COLOR_RE.search(stripped))


NOISE_RE = re.compile(
    r'^\s*(\d+\s+)?CONTINUED\s*:?\s*\(?\d*\)?\s*$'
    r'|^\s*\(CONTINUED\)\s*$',
    re.IGNORECASE
)

BARE_PAGE_NUMBER_RE = re.compile(r'^\s*\d+\.?\s*$')

TRANSITION_RE = re.compile(
    r'^\s*((CUT|MATCH CUT|JUMP CUT|TIME CUT|SMASH CUT|INTERCUT) TO:?'
    r'|CUT TO BLACK:?'
    r'|FADE (IN|OUT|TO)\.?:?'
    r'|DISSOLVE TO:?'
    r'|BLACKOUT:?'
    r'|TIME DISSOLVE TO:?'
    r'|RESUME\s*-*:?)\s*$',
    re.IGNORECASE
)

NON_CHARACTER_MARKERS = (
    'SUPERIMPOSE', 'CONTINUED', 'INSERT', 'TITLE', 'FLASHBACK',
    'BACK TO SCENE', 'ANGLE', 'CLOSE ON', 'POV', 'MONTAGE',
    'INTERCUT', 'SERIES OF SHOTS', 'END OF FLASHBACK', 'CHAPTER',
    'LEGEND', 'BLACK SCREEN', 'FROM OUTSIDE', 'FROM INSIDE',
    'FROM ABOVE', 'FROM BELOW'
)

ABBREV_NAME_RE = re.compile(r'^[A-Z]{1,2}(\.[A-Z]{1,2})+\.?$')

NUMBERED_HANDLE_RE = re.compile(r"^[A-Z][A-Z'.\- ]{0,30}#\d+$")


def looks_like_ocr_garbled_abbrev_name(check):
    normalized = check.replace('0', 'O').replace('8', 'B')
    return bool(ABBREV_NAME_RE.match(normalized))

def is_character_cue(line):
    stripped = line.strip()
    if not stripped:
        return False
    if SLUGLINE_RE.match(stripped) or TRANSITION_RE.match(stripped):
        return False
    if ':' in stripped:
        return False
    if any(c.isdigit() for c in stripped):
        check_prelim = SUFFIX_STRIP_RE.sub('', stripped).strip()
        if looks_like_ocr_garbled_abbrev_name(check_prelim):
            return True
        if NUMBERED_HANDLE_RE.match(check_prelim):
            return True
        return False
    check = SUFFIX_STRIP_RE.sub('', stripped).strip()
    if not check:
        return False
    if any(marker in check.upper() for marker in NON_CHARACTER_MARKERS):
        return False
    if re.match(r'^(ON|WITH)\s+\S', check.upper()) or SCENE_DIRECTION_RE.match(check.upper()):
        return False
    letters = [c for c in check if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    word_count = len(check.split())
    is_abbrev_name = bool(ABBREV_NAME_RE.match(check)) or looks_like_ocr_garbled_abbrev_name(check)
    QUOTE_PAIRS = (('"', '"'), ("'", "'"), ('‘', '’'), ('“', '”'))
    is_fully_quoted = any(
        check.startswith(open_q) and check.endswith(close_q) and len(check) > 1
        for open_q, close_q in QUOTE_PAIRS
    )
    if is_fully_quoted:
        return False
    if check.startswith('(') and check.endswith(')') and len(check) > 1:
        return False
    ends_ok = is_abbrev_name or (not check.endswith('.') and not check.endswith('!') and not check.endswith('?'))
    return upper_ratio > 0.9 and len(check) < 40 and word_count <= 6 and ends_ok

MIXED_CASE_NAME_TOKEN_RE = re.compile(r"\b[A-Z][A-Z']{1,}\b")

CAPS_FALSE_FRIENDS = {
    'POV', 'CLOSE', 'ANGLE', 'INSERT', 'BEAT', 'CONTINUOUS', 'LATER',
    'CONTINUED', 'SUPER', 'TITLE', 'MOS', 'VO', 'OS', 'OK', 'NO',
    'STOP', 'FREEZE', 'THE', 'AND', 'FADE', 'CUT'
}

SENTENCE_BOUNDARY_RE = re.compile(r'(?:^|[.!?]\s+|--\s*)')

WATERMARK_FRAGMENT_MAX_LEN = 6


def build_cue_candidate_counts(lines):
    from collections import Counter
    counts = Counter()
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped and is_character_cue(stripped):
            speaker = cue_speaker(stripped)
            counts[speaker] += 1
    return counts


def build_watermark_fragment_set(lines, min_occurrences=None):
    from collections import Counter
    counts = Counter()
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or len(stripped) > WATERMARK_FRAGMENT_MAX_LEN:
            continue
        if any(c.isdigit() for c in stripped):
            continue
        letters = [c for c in stripped if c.isalpha()]
        if letters and all(c.isupper() for c in letters):
            continue
        counts[stripped] += 1

    if min_occurrences is None:
        min_occurrences = max(15, len(lines) // 120)

    return {frag for frag, n in counts.items() if n >= min_occurrences}


def build_confirmed_names(lines):
    confirmed = set()
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue
        letters = [c for c in stripped if c.isalpha()]
        if not letters:
            continue
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        if upper_ratio >= 0.9:
            continue
        for boundary in SENTENCE_BOUNDARY_RE.finditer(stripped):
            clause_start = stripped[boundary.end():]
            match = MIXED_CASE_NAME_TOKEN_RE.match(clause_start)
            if not match:
                continue
            token = match.group(0)
            if token in CAPS_FALSE_FRIENDS or len(token) < 2:
                continue
            confirmed.add(token)
    return confirmed


BARE_NUMBERED_SLUGLINE_RE = re.compile(
    r'^(\d+)\s+([A-Z][A-Z0-9\'\.\- ]{2,50}?)\s+\1\s*$'
)

def build_prose_character_names(lines):
    names = set()
    for line in lines:
        stripped = line.strip()
        if is_character_cue(stripped):
            check = SUFFIX_STRIP_RE.sub('', stripped).strip()
            words = check.split()
            if words:
                names.add(' '.join(w.capitalize() for w in words))
                names.add(words[-1].capitalize())
    return names

def is_bare_slugline(stripped):
    if TRANSITION_RE.match(stripped) or is_parenthetical(stripped):
        return False
    if BARE_SLUGLINE_TIME_RE.match(stripped):
        return True
    if BARE_NUMBERED_SLUGLINE_RE.match(stripped):
        return True
    if ':' in stripped or any(c.isdigit() for c in stripped):
        return False
    letters = [c for c in stripped if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    if upper_ratio <= 0.9 or len(stripped) >= 45:
        return False
    words = stripped.upper().split()
    return any(w.strip('.,-') in LOCATION_KEYWORDS for w in words)


def is_short_caps_candidate(stripped):
    if ':' in stripped or any(c.isdigit() for c in stripped):
        return False
    if TRANSITION_RE.match(stripped) or is_parenthetical(stripped):
        return False
    letters = [c for c in stripped if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return upper_ratio > 0.9 and len(stripped) < 45


def looks_like_location_phrase(stripped):
    if ',' in stripped:
        return True
    first_word = stripped.split()[0].upper().rstrip('.,') if stripped.split() else ''
    return first_word in ('A', 'AN', 'THE')


def resolve_ambiguous_candidate(stripped, confirmed_names):
    tokens = MIXED_CASE_NAME_TOKEN_RE.findall(stripped)
    if any(t in confirmed_names for t in tokens):
        return 'character'
    return 'ambiguous'


def looks_like_broken_continuation(stripped):
    if not stripped.endswith('-'):
        return False
    letters = [c for c in stripped if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return upper_ratio > 0.9


def is_parenthetical(line):
    stripped = line.strip()
    return stripped.startswith('(') and stripped.endswith(')')


# "OVER BLACK:" opens real script content (sound or action heard before
# the first image), not title-page material. Confirmed on Full of Grace
# and LOTB, where the lines under it sit above FADE IN: and were being
# cut away with the title page. Line-anchored so prose mentioning black
# never matches; accepts "OVER BLACK", "OVER BLACK:", "OVER BLACK." and
# text continuing on the same line. The leading class includes \f and \v:
# pdftotext puts a form feed at the start of each new page's first line,
# and "OVER BLACK:" is typically the first line after the title page.
OVER_BLACK_RE = re.compile(r'^[ \t\f\v]*OVER[ \t]+BLACK\b[ \t]*[:.\-]*', re.IGNORECASE | re.MULTILINE)


# A whole line that is only a time jump -- "LATER", "MOMENTS LATER",
# "TWO WEEKS LATER", "CONTINUOUS", "MEANWHILE", "SAME TIME" -- with an
# optional trailing ":", "." or "--". Found on Full of Grace ("LATER"
# parsed as a speaker x4), LOTB and WHTBD. Only all-caps lines count, so
# ordinary dialogue or action containing "later" is never affected.
TIME_CUT_RE = re.compile(
    r"^(?:(?:[A-Z0-9'’]+ ){0,3}LATER|CONTINUOUS|MEANWHILE|SAME TIME|SIMULTANEOUSLY"
    r"|(?:THE )?PRESENT)"
    r"\s*(?:[:.]|--)?$"
)


def is_time_cut_line(stripped):
    return stripped == stripped.upper() and bool(TIME_CUT_RE.match(stripped))


# A short all-caps line that opens with a preposition or "BACK TO/WITH" is
# a shot or sub-location direction ("AT POKER MACHINE", "BACK TO JOHN",
# "OVER SWAT LEADER'S SHOULDER"), never a speaker. Found as phantom
# speakers in Full of Grace (6), WHTBD (3), LOTB, LMS and Ocean's Eleven
# (1 each). Extends is_character_cue()'s existing ON/WITH rejection.
SCENE_DIRECTION_RE = re.compile(
    r"^(?:AT|IN|INSIDE|OUTSIDE|NEAR|BEHIND|OVER|UNDER|BACK\s+(?:TO|WITH|ON|AT|IN))\s+\S"
)


def is_scene_direction_line(stripped):
    return (stripped == stripped.upper() and len(stripped) < 45
            and bool(SCENE_DIRECTION_RE.match(stripped)))


def strip_title_page(raw_text):
    fade_in_match = re.search(r'FADE IN:', raw_text, re.IGNORECASE)
    over_black_match = OVER_BLACK_RE.search(raw_text)
    if not fade_in_match and not over_black_match:
        return raw_text

    earliest_slugline_pos = None
    for m in re.finditer(r'^.*$', raw_text, re.MULTILINE):
        if SLUGLINE_RE.match(m.group(0).strip()):
            earliest_slugline_pos = m.start()
            break

    candidates = [pos for pos in (
        fade_in_match.start() if fade_in_match else None,
        over_black_match.start() if over_black_match else None,
        earliest_slugline_pos,
    ) if pos is not None]
    return raw_text[min(candidates):]


FLASHBACK_HEADING_RE = re.compile(r'^\s*FLASHBACK\b', re.IGNORECASE)
BACK_TO_SCENE_RE = re.compile(r'^\s*BACK TO (SCENE|PRESENT)\.?\s*$', re.IGNORECASE)


def parse_script(raw_text):
    raw_text = strip_title_page(raw_text)
    raw_text = re.sub(
        r"\b([A-Z][A-Z'.]*(?: [A-Z][A-Z'.]*){0,4})-\1\b",
        r'\1\n\1',
        raw_text,
    )
    raw_text = re.sub(r'([a-z])-([A-Z]{2,})', r'\1-\n\2', raw_text)
    lines = raw_text.split('\n')
    confirmed_names = build_confirmed_names(lines)
    prose_character_names = build_prose_character_names(lines)
    watermark_fragments = build_watermark_fragment_set(lines)
    cue_candidate_counts = build_cue_candidate_counts(lines)
    scenes = []
    current_scene = None
    current_element = None
    last_speaker = None
    bare_slugline_count = 0
    flashback_stack = []

    def flush_element():
        nonlocal current_element
        if current_element and current_element['text'].strip():
            current_scene['elements'].append(current_element)
        current_element = None

    for raw_line in lines:
        line = raw_line.rstrip()
        line = re.sub(r'\s*\*\s*$', '', line)
        stripped = line.strip()

        if not stripped:
            flush_element()
            continue

        if NOISE_RE.match(stripped) or is_revision_header(stripped) or stripped in watermark_fragments:
            continue

        if BARE_PAGE_NUMBER_RE.match(stripped):
            awaiting_dialogue = (
                current_element is None and current_scene and current_scene['elements']
                and current_scene['elements'][-1]['type'] == 'character_cue'
            )
            if not awaiting_dialogue:
                continue

        if current_scene and current_scene.get('awaiting_continuation'):
            current_scene['awaiting_continuation'] = False
            current_scene['slugline'] = current_scene['slugline'] + ' ' + stripped
            current_scene['location_time'] = (current_scene['location_time'] + ' ' + stripped).strip()
            continue

        if (current_scene and not current_scene['elements']
                and LEADING_DASH_CONTINUATION_RE.match(stripped)):
            current_scene['slugline'] = current_scene['slugline'] + ' ' + stripped
            current_scene['location_time'] = (current_scene['location_time'] + ' ' + stripped).strip()
            continue

        if BACK_TO_SCENE_RE.match(stripped) and flashback_stack:
            flush_element()
            if current_scene:
                scenes.append(current_scene)
            current_scene = flashback_stack.pop()
            last_speaker = None
            continue

        slug_match = SLUGLINE_RE.match(stripped)
        if slug_match:
            flush_element()
            if current_scene:
                scenes.append(current_scene)
            loc_time = slug_match.group(2).strip()
            current_scene = {
                'scene_id': len(scenes) + len(flashback_stack) + 1,
                'slugline': stripped,
                'int_ext': slug_match.group(1).upper().replace('.', ''),
                'location_time': loc_time,
                'elements': [],
                'slugline_type': 'standard',
                'awaiting_continuation': loc_time.rstrip().endswith('-')
            }
            last_speaker = None
            continue

        if is_bare_slugline(stripped):
            flush_element()
            bare_slugline_count += 1
            if FLASHBACK_HEADING_RE.match(stripped) and not flashback_stack and current_scene:
                flashback_stack.append(current_scene)
            elif current_scene:
                scenes.append(current_scene)
            current_scene = {
                'scene_id': len(scenes) + len(flashback_stack) + 1,
                'slugline': stripped,
                'int_ext': 'UNSPECIFIED',
                'location_time': stripped,
                'elements': [],
                'slugline_type': 'bare (no INT/EXT — flag for review)'
            }
            last_speaker = None
            continue

        if current_scene is None:
            current_scene = {
                'scene_id': 0,
                'slugline': None,
                'int_ext': None,
                'location_time': 'PRE-SLUGLINE / COLD OPEN',
                'elements': [],
                'slugline_type': 'none'
            }

        if TRANSITION_RE.match(stripped):
            flush_element()
            continue

        # Kept as its own action element (never a cue: bare "OVER BLACK"
        # otherwise passes is_character_cue), so the lines under it start
        # a fresh action element instead of merging into this one. Same for
        # a flush-left time-jump line ("LATER", "MOMENTS LATER"), which
        # otherwise parses as a phantom speaker named LATER, and a shot or
        # sub-location direction ("AT POKER MACHINE", "BACK TO JOHN"). Inside
        # an open dialogue block a direction needs 3+ words to break out, so
        # a shouted two-word fragment ("IN HERE") stays dialogue.
        in_open_dialogue = current_element is not None and current_element['type'] == 'dialogue'
        if (OVER_BLACK_RE.match(stripped) or is_time_cut_line(stripped)
                or (is_scene_direction_line(stripped)
                    and (not in_open_dialogue or len(stripped.split()) >= 3))):
            flush_element()
            current_element = {'type': 'action', 'speaker': None, 'text': stripped}
            flush_element()
            continue

        if is_character_cue(stripped) and not follows_unresolved_cue(current_scene, current_element):
            if looks_like_location_phrase(stripped):
                resolution = resolve_ambiguous_candidate(stripped, confirmed_names)
                if resolution == 'ambiguous':
                    flush_element()
                    current_scene.setdefault('ambiguous_bare_headings', []).append(stripped)
                    current_element = {'type': 'action', 'speaker': None, 'text': stripped}
                    flush_element()
                    continue
            flush_element()
            speaker = cue_speaker(stripped)
            last_speaker = speaker
            current_element = {'type': 'character_cue', 'speaker': speaker, 'text': stripped}
            flush_element()
            continue

        if is_parenthetical(stripped):
            flush_element()
            current_element = {'type': 'parenthetical', 'speaker': last_speaker, 'text': stripped}
            flush_element()
            continue

        if current_element and current_element['type'] == 'dialogue':
            words = stripped.split()
            looks_like_glued_action = (
                len(words) >= 2 and words[0] in prose_character_names
                and words[1][:1].islower()
            )
            if not looks_like_glued_action:
                current_element['text'] += ' ' + stripped
                continue
            flush_element()
            current_element = {'type': 'action', 'speaker': None, 'text': stripped}
            continue

        if current_scene and (looks_like_broken_continuation(stripped) or current_scene.get('continuation_pending')) \
                and current_scene['elements'] and current_element is None:
            reopened = current_scene['elements'].pop()
            reopened['text'] += ' ' + stripped
            current_element = reopened
            current_scene['continuation_pending'] = looks_like_broken_continuation(stripped)
            continue

        if scenes_last_was_dialogue_trigger(current_scene, last_speaker):
            words = stripped.split()
            looks_like_glued_action = (
                len(words) >= 2 and words[0] in prose_character_names
                and words[1][:1].islower()
            )
            fake_cue_candidate = (
                current_scene['elements'][-1]['type'] == 'character_cue'
                and cue_candidate_counts.get(last_speaker, 0) <= 3
            ) if current_scene['elements'] else False
            if looks_like_glued_action and fake_cue_candidate:
                fake_cue = current_scene['elements'].pop()
                current_scene.setdefault('reclassified_fake_cues', []).append(fake_cue['text'])
                current_element = {'type': 'action', 'speaker': None, 'text': fake_cue['text'] + ' ' + stripped}
                last_speaker = None
                continue
            current_element = {'type': 'dialogue', 'speaker': last_speaker, 'text': stripped}
            continue

        if current_element and current_element['type'] == 'action':
            current_element['text'] += ' ' + stripped
        else:
            flush_element()
            current_element = {'type': 'action', 'speaker': None, 'text': stripped}

    flush_element()
    if current_scene:
        scenes.append(current_scene)

    scenes.sort(key=lambda s: s['scene_id'])

    return scenes


def uses_bare_sluglines(parsed_scenes, threshold=2):
    bare_count = sum(
        1 for s in parsed_scenes
        if s.get('slugline_type', '').startswith('bare')
    )
    return bare_count >= threshold


def follows_unresolved_cue(current_scene, current_element):
    if current_element is not None:
        return False
    if not current_scene or not current_scene['elements']:
        return False
    return current_scene['elements'][-1]['type'] == 'character_cue'


def scenes_last_was_dialogue_trigger(current_scene, last_speaker):
    if not current_scene or not current_scene['elements']:
        return False
    last = current_scene['elements'][-1]
    return last['type'] in ('character_cue', 'parenthetical') and last_speaker is not None


if __name__ == '__main__':
    with open('mystic_river_raw.txt', 'r') as f:
        raw = f.read()

    parsed = parse_script(raw)

    with open('mystic_river_parsed.json', 'w') as f:
        json.dump(parsed, f, indent=2)

    print(f"Parsed {len(parsed)} scenes.\n")
    for scene in parsed[:5]:
        print(f"Scene {scene['scene_id']}: {scene['slugline']}")
        print(f"  int_ext={scene['int_ext']} location_time={scene['location_time']}")
        for el in scene['elements'][:6]:
            preview = el['text'][:60].replace('\n', ' ')
            print(f"    [{el['type']:14s}] {el.get('speaker','') or '':16s} {preview}")
        print()
