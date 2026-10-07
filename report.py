"""
report.py -- Stage 6: the story report generator (STORY_REPORT_SPEC.md).

Build status (2026-10-05): sections 2 ("Character arcs: where characters
change, and where they don't"), 3 ("Consistency check: a second look") and
4 (the character function map), plus the static "Why should I care?" and
"What this report doesn't measure" sections. Section 1, the development
read, is not built yet; it will be the only LLM-written text, gated by
report_guard.py. "Questions for the next draft" is dropped from the first
release, and sections 2-3 keep their template wording (no LLM rewording);
see STORY_REPORT_SPEC.md. Everything here is deterministic: no API call, no
generated prose. Each section has its own AI Output / Human Reviewed switch
(default AI Output). Character names are title case in reader-facing text;
the script's cue names are shown under the hood.

Section 4, the archetype timeline (2026-10-06): one lane per Big Seven
archetype, each archetype call a mark at its moment's first line on the
script's printed pages, with the same AI Output / Human Reviewed switch. The
Great Mother pole (Human Reviewed only) is read from the review records'
verdicts and author rulings (review_row, great_mother_pole); it is not a
stored field. Template wording only (TL_HEADING, TL_INTRO, TL_TEXT).

Sections 2-3 use template wording only (TEXT, TURN_LABEL, TURN_GLOSS,
FLAG_TEXT); the build rejects pipeline terms and grading words in any
reader-facing string and in the page's static text. Reviewed turning
points are cross-checked against fog_turning_points_reviewed.json; their
comparison beats appear only under the hood (STORY_REPORT_SPEC.md).
Author decision D1: the Human Reviewed view of section 3 shows only "No
inconsistency held up on review."

Audience: non-technical readers. Plain language on top; technical detail
lives in collapsed "Under the hood" sections (same standard as the PETE
demo card). Pipeline terms (cold, provenance, beat IDs, enum names) never
appear above the fold.

Sources and checks:
- fog_report_model.json / fog_line_index.json (written by report_data.py,
  which runs the replay audit).
- Beat text is copied from fog_full.txt by line range at build time, never
  typed in. The build asserts every stored turn of a marked beat appears
  in the text shown, so the panel always holds the full beat.
- "The AI's reasoning" shows only what the model stored for that entry in
  the uncorrected run (7a6e69e). The model never wrote a rationale for an
  archetype choice; the panel says so instead of inventing one.
- "What changed in review" lines (CHANGE_LINES) are plain-language
  summaries written by Claude from the cited corrections-log entries. The
  build asserts each cited log entry exists and names that beat and
  character, and that every changed archetype call has a line. The
  verbatim log notes are shown under the hood.

Output: fog_story_report.html (one file; its fonts load from fonts/ via the
shared numen_theme.css, with system fallbacks). This is the
public build: it never contains Review mode.

Review mode (local only): python report.py --review writes
fog_story_report_review.html (git-ignored) with a "Review mode" switch for
the author's polish pass. It makes reader-facing copy editable in the
browser, keeps AI output and script text locked, and "Copy my edits" lists
every change (section, element, original, new) so it can be applied to the
source (TEXT, templates, APPROVED_STATIC, report.py). Edits in the browser
never change the source by themselves.

Run from the repo root:
    python report_data.py   # rebuild the model first if the data changed
    python report.py        # public build
    python report.py --review   # local review build
"""
import argparse
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from tagging_schema import beat_id_sort_key, BIG_SEVEN_DEFINITIONS  # noqa: E402
import report_guard  # noqa: E402
import numen_theme  # noqa: E402
import review_mode  # noqa: E402
import git_snapshots  # noqa: E402

MODEL = os.path.join(ROOT, "fog_report_model.json")
LINE_INDEX = os.path.join(ROOT, "fog_line_index.json")
FULL_TXT = os.path.join(ROOT, "fog_full.txt")
TAGGED = os.path.join(ROOT, "fog_tagged.json")
OUT = os.path.join(ROOT, "fog_story_report.html")
REVIEW_OUT = os.path.join(ROOT, "fog_story_report_review.html")  # local only, git-ignored
REVIEW_MARKER = review_mode.MARKER  # present only in the review build; the public build asserts it is absent
# Section 1, the development read, written by fog_dev_read_runner.py --run.
# Absent until that billed run; the page then shows no section 1.
DEV_READ = os.path.join(ROOT, "fog_dev_read.json")

TOP_N = 8
# BIG_SEVEN_DEFINITIONS order; each gets a fixed categorical slot.
ARCHETYPES = ["Persona", "Shadow", "Trickster", "Hero", "Mentor", "Chorus", "Great Mother"]
# One plain line per archetype: the author's wording, used verbatim
# (second version, 2026-10-04). Checked against BIG_SEVEN_DEFINITIONS.
# The Great Mother pole (Light/Dark) is NOT stored in the data (no field
# for it on any FOG call), so the map never labels a pole.
GLOSS = {
    "Hero": "acts bravely, at real risk, for someone or something beyond themselves.",
    "Mentor": "guides or teaches someone who's there to learn.",
    "Great Mother": "the nurturing force, in two poles. Light nurtures and protects; Dark smothers, controls, or devours.",
    "Persona": "the social mask a character wears over what they really feel.",
    "Shadow": "something buried breaking through, despite the character's control.",
    "Trickster": "deceives or plays games on someone who doesn't see it coming.",
    "Chorus": "steps back to comment on what's happening, like a voice from outside it.",
}

# "What are The Big Seven?" explainer: the author's wording, verbatim.
BIG_SEVEN_EXPLAINER = [
    # Review edits 11 + 12 (author, 2026-10-05; "laid out page by page" by the author's decision).
    "The psychologist Carl Jung proposed that certain character patterns (archetypes) recur across myths, "
    "stories, and dreams, spanning every culture and era, patterns audiences recognize consciously and "
    "subconsciously, such as the hero, the wise guide, or the dark double. The Big Seven were chosen as the "
    "archetypes that seem to appear most throughout screenplays and movies: six come from Jung, plus the "
    "Chorus from Greek drama. This map shows where each character presents as one of those archetypes, "
    "laid out page by page, scene by scene.",
]

# Section 1 template lines (static copy).
DEV_READ_TEXT = {
    "label": "Written by the AI",
    "title_note": "from the script’s title page",
    "fallback_title_genre": "The AI’s synopsis did not pass the report’s checks, so only the title and genre are shown.",
    "fallback_title": "The AI’s genre and synopsis did not pass the report’s checks, so only the title is shown.",
    # Prompt version 5 on: genre + logline + full synopsis.
    "synopsis_summary": "Read the full synopsis",
    "fallback": "Parts of the AI’s development read did not pass the report’s checks and are not shown: {parts}.",
}
DEV_READ_PART_NAMES = {"genre": "the genre", "logline": "the logline", "synopsis": "the full synopsis"}

# "What this report doesn't measure": the author's wording, verbatim (2026-10-05).
NOT_MEASURED_LEAD = "What this report doesn't measure:"
NOT_MEASURED = [
    # Review edit 21 (author, 2026-10-05), as written.
    "dialogue and voice; marketability, audience appeal and comparable titles; castability and budget; "
    "potential for box-office and/or critical success.",
    # Section 4 line (approved by the author 2026-10-06).
    "The archetype timeline shows where archetypes are called, not the strength of a call or how much a "
    "moment matters.",
    "And above all else: it never judges whether a story is good or bad.",
    "That call stays where it matters most: with the human audience.",
]

# "Why should I care?": the author's wording, verbatim (2026-10-05; review-mode
# edits applied the same day).
WHY_HEADING = '"Why should I care?"'
WHY_INTRO = ("When a script lands on your desk, the first questions are often about story and character. "
             "What's this story about? Who are the characters, and are they believable? Where's this story "
             "taking me, and is the journey and the twists along it solid? Traditional coverage answers this "
             "with a reader's impression. This story report answers it all with evidence, page by page, "
             "scene by scene, including:")
# (bold lead-in, rest of the bullet)
WHY_BULLETS = [
    ("Every character's role in the story", ", mapped scene by scene using The Big Seven Jungian archetypes (see Section {map})."),
    ("The moments where characters change", ", and where they don't."),
    ("Consistency checks", ": moments worth a second look, with the exact pages to check."),
]
WHY_AFTER = [
    # "{toggled}" is "Sections 2 and 3" in this release (the sections with the toggle);
    # author decision 2026-10-05, replacing "Each section below shows".
    "Mapping a script this way would take a story expert weeks by hand. The AI does it in minutes. "
    "{toggled} show what the AI produced on its own, next to a human-reviewed version, so you "
    "can see how close the AI already gets (see the \"AI Output/Human Reviewed\" toggle button).",
    # Review edit 5 (author, 2026-10-05), with the author's typo fixes ("never grades", "what it sees").
    "This report never grades a script or tells anyone what to write or how to improve the story. The "
    "report acts simply as data from an outside observer: it points only to what it sees on-the-page. "
    "The development team decides what to do next.",
]

def toggled_sections():
    """The sections that have the AI Output / Human Reviewed toggle."""
    nums = [2, 3, MAP_SECTION, TIMELINE_SECTION] if SHOW_CONSISTENCY_CHECK else [2, MAP_SECTION, TIMELINE_SECTION]
    return "Sections " + (", ".join(map(str, nums[:-1])) + " and " + str(nums[-1]))


def why_bullets():
    """The "Why should I care?" bullets for this build: the third one
    describes section 3 and is left out while that section is off."""
    return [b for b in WHY_BULLETS if SHOW_CONSISTENCY_CHECK or b[0] != "Consistency checks"]


# What changed in review, in plain words. Key: "beat_id|display character".
# Value: (line, [corrections-log numbers it summarizes]).
CHANGE_LINES = {
    "scene14_beat12|SARGE": ("Mentor removed. Sarge is enforcing a deal they had already made, not teaching anything new.", [162]),
    "scene30_beat2|TRUDY": ("Great Mother removed. Her act of care came in the moment before; here she only watches the man leave.", [84]),
    "scene48_beat3|PRIEST": ("Chorus removed. He is performing the funeral service, not commenting on the story.", [167]),
    "scene48_beat4|PRIEST": ("Chorus removed. He is performing the funeral service, not commenting on the story.", [169]),
    "scene54_beat1|REGGIE": ("Chorus removed. This is a kind remark at a funeral, not a comment on the story.", [132]),
    "scene57_beat1|JOHN": ("Persona removed. John’s anger is out in the open here, not hidden behind a front.", [3]),
    "scene77_beat1|JOHN": ("Persona removed. John is distracted and torn, not putting on a front.", [7]),
    "scene81_beat1|ANGIE": ("Chorus changed to Mentor. Angie is still giving John advice about his own situation.", [139]),
    "scene101_beat1|DOUG": ("Mentor changed to Chorus. Doug gives an outside verdict on John’s plan, not personal teaching.", [145]),
    "scene119_beat2|JOHN": ("Shadow removed. The harsh questioning is a deliberate tactic, not something breaking through John’s control.", [19]),
    "scene123_beat9|DOUG": ("Mentor changed to Chorus. Doug gives an outside read on John’s blind spot, not personal teaching.", [150]),
    "scene123_beat15|DOUG": ("Persona removed. Doug’s hurt is shown openly; holding back is self-control, not a mask.", [155]),
    "scene131_beat1|TRUDY": ("Removed. Review first changed Trickster to Shadow, then removed it: her devotion stays unbroken, so nothing breaks through her control.", [85, 752]),
    "scene140_beat6|MACKIE": ("Great Mother changed to Shadow. The grab at John’s throat is a sudden, wordless eruption, not care.", [109]),
    "scene140_beat8|MACKIE": ("Great Mother changed to Shadow. The same eruption continues as his grip hardens.", [114]),
    "scene154_beat2|CHEYENNE": ("Persona removed. What she is hiding isn’t shown until a later scene; here she is openly trying to calm things down.", [37]),
    "scene154_beat3|JOHN": ("Hero removed. Cheyenne and O’Shea were working together, so she was never in danger. John is protecting himself, not someone else.", [24]),
    "scene172_beat1|REGGIE": ("Shadow removed. Reggie stops hiding, but stays calm and in control throughout. That is a choice, not a break.", [122]),
    "scene172_beat2|JOHN": ("Hero removed. This moment is an argument. Saying you will act is not acting; John’s brave acts come next.", [60]),
    "scene172_beat2|REGGIE": ("Shadow removed. Reggie stops hiding, but stays calm and in control throughout. That is a choice, not a break.", [127]),
    "scene172_beat3|JOHN": ("Hero added. John refuses to drop his rifle and starts to raise it, protecting Alberto as well as himself. The AI made no call for John here.", [61]),
    "scene172_beat4|JOHN": ("Hero added. John levels his rifle at Reggie, protecting Alberto as well as himself.", [66]),
    "scene172_beat6|JOHN": ("Hero added. John shields himself and Alberto from gunfire and fires back.", [70]),
    "scene172_beat7|JOHN": ("Hero added. Under fire, John checks on Alberto. The reviewer called this the thinnest Hero moment in the sequence.", [74]),
    "scene172_beat8|JOHN": ("Hero removed. John is chasing Reggie to catch him, not protecting someone else.", [45]),
    "scene213_beat1|JOHN": ("Great Mother added alongside Mentor. Besides guiding Trudy, John makes a safe space for her to talk.", [51]),
    "scene216_beat5|TRUDY": ("Great Mother changed to Shadow. This is raw physical violence, with none of the ritual that marks her Great Mother moments.", [103]),
    "scene216_beat6|TRUDY": ("Shadow changed to Great Mother (its dark side). She calmly finishes the baptism vows as Holly goes still.", [97]),
    "scene223_beat1|JOHN": ("Hero removed. The only person John could be saving here is himself, and the telling never happens on the page.", [55]),
}

# Section 3, "Consistency check: a second look", is dropped from the first
# public release (author decision 2026-10-05, STORY_REPORT_SPEC.md, Future
# features): flagged "inconsistencies" are subjective judgment calls that
# read as implied development notes. Its code and data stay here, disabled;
# set this to True to bring it back (sections renumber themselves).
SHOW_CONSISTENCY_CHECK = False
MAP_SECTION = 4 if SHOW_CONSISTENCY_CHECK else 3
TIMELINE_SECTION = MAP_SECTION + 1
N_SECTIONS = TIMELINE_SECTION

# Section 4, the archetype timeline (2026-10-06): one lane per archetype,
# each archetype call a mark at its moment's first line, on the script's
# printed pages. Framing approved by the author 2026-10-06 (the first intro
# line in the author's wording): it says only what the timeline shows (no
# reading of patterns, no counts).
TL_PAGES = (1, 125)   # the script's own page numbers, first to last
TL_HEADING = "Section {n}. Archetype Timeline"
TL_INTRO = [
    # The author's wording, verbatim (2026-10-06).
    "Where each of The Big Seven is called across the script. Each lane is one archetype; each mark is a "
    "moment, placed at the page where it begins and labelled with the character.",
    "Tap or click a mark for the character, archetype and page, and a link to that character in the "
    "character map (section {map}).",
]
TL_TEXT = {
    # The map's own banner wording (section 3), reused as is.
    "tl_banner_cold": "AI Output: no human corrections.",
    "tl_banner_reviewed": "Human Reviewed: every archetype call checked by a person.",
    "tl_pole_key": "Great Mother: a filled mark is its dark pole, as named in review. "
                   "A hollow mark is one where review named no pole.",
    "tl_link": "See {name} in the character map (section {map})",
    "tl_dark": "dark pole",          # screen-reader label of a filled Great Mother mark
    "tl_nopole": "no pole named in review",
}
# The Great Mother pole is not stored on any FOG call (FUTURE_WORK.md item
# 3). The Human Reviewed view reads it from the review records: the verdict
# column of the beat's row in the character's FOG_<NAME>_REVIEW.md archetype
# table, plus any author ruling written on that row as
# "Author ruling (<date>): <ruling>." A ruling takes precedence over the
# verdict. AI Output shows no pole.
REVIEW_FILE = {"CAPTAIN MARCHAND": "MARCHAND", "DR. SHEPHARD": "SHEPHARD", "DET. MCAVOY": "MCAVOY"}
RULING_RE = re.compile(r"Author ruling \(([^)]+)\): ([^|]*?\.)(?=\s|$)")
_REVIEW_CACHE = {}


def review_row(character, beat_id):
    """The beat's row in the character's archetype review table, as
    {"file", "verdict", "rulings": [(date, text)]}, or None."""
    stem = REVIEW_FILE.get(character, re.sub(r"[^A-Z]", "", character))
    path = os.path.join(ROOT, f"FOG_{stem}_REVIEW.md")
    if path not in _REVIEW_CACHE:
        if not os.path.exists(path):
            _REVIEW_CACHE[path] = None
        else:
            with open(path, encoding="utf-8") as f:
                _REVIEW_CACHE[path] = re.split(r"\n## Pass 2", f.read())[0]
    arch = _REVIEW_CACHE[path]
    if arch is None:
        return None
    rows = [l for l in arch.split("\n") if l.startswith(f"| {beat_id} |")]
    if not rows:
        return None
    if len(rows) > 1:
        sys.exit(f"ABORT: {os.path.basename(path)} has {len(rows)} archetype rows for {beat_id}")
    cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    return {"file": os.path.basename(path), "verdict": cells[1], "rulings": RULING_RE.findall(rows[0])}


def pole_word(text):
    t = text.lower()
    dark, light = "dark pole" in t, "light pole" in t
    if dark and light:
        sys.exit(f"ABORT: both poles named in {text!r}")
    return "dark" if dark else "light" if light else None


def great_mother_pole(rec):
    """(pole, source): the latest author ruling on Great Mother that names a
    pole, else the verdict; (None, None) when neither names one."""
    for date, text in reversed(rec["rulings"]):
        if "Great Mother" in text and pole_word(text):
            return pole_word(text), f"author ruling ({date})"
    p = pole_word(rec["verdict"])
    return (p, "verdict") if p else (None, None)

# "The Big Seven: full definitions" appendix (author decisions 2026-10-05).
# It shows BIG_SEVEN_DEFINITIONS exactly as the AI was given them in the FOG
# cold run: the text is read from tagging_schema.py at the cold-run commit,
# never from the working file, and never edited here. The definitions are a
# verbatim class: exempt from the word checks only if every definition is on
# the page exactly and the label (DEFS_INTRO) is present; otherwise the
# build stops (report_guard.final_scan, verbatim=...).
SHOW_DEFINITIONS_APPENDIX = True
DEFS_HEADING = "The Big Seven: full definitions"
DEF_LINK_TEXT = "Full definition"
# The label of the verbatim class: the author's wording, verbatim.
DEFS_INTRO = [
    "These are the exact definitions given to the AI when it tagged this script, including its "
    "instructions to the AI.",
    "Where a definition says ordinary_reaction, it means the moment is ordinary behaviour, with no archetype.",
]
DEFS_COMMIT = "7a6e69e"   # the FOG cold run (report_data.COLD_PASS1_COMMIT)
_COLD_DEFS = {}


def cold_run_definitions():
    """BIG_SEVEN_DEFINITIONS as they stood at the cold-run commit, plus the
    names of any that differ from the current tagging_schema.py."""
    if not _COLD_DEFS:
        defs = git_snapshots.definitions(DEFS_COMMIT)
        if set(defs) != set(ARCHETYPES):
            sys.exit(f"ABORT: cold-run BIG_SEVEN_DEFINITIONS keys {sorted(defs)} != {ARCHETYPES}")
        _COLD_DEFS["defs"] = defs
        _COLD_DEFS["differ"] = [a for a in ARCHETYPES if defs[a] != BIG_SEVEN_DEFINITIONS.get(a)]
    return _COLD_DEFS["defs"], _COLD_DEFS["differ"]


def def_id(arch):
    return "def-" + arch.lower().replace(" ", "-")


def def_paragraph(arch, text):
    return f'<p data-verbatim="definition" data-locked="Definition, word for word">{e(text)}</p>'


def definitions_html():
    defs, differ = cold_run_definitions()
    items = "".join(f'<h3 id="{def_id(a)}">{e(a)}</h3>' + def_paragraph(a, defs[a]) for a in ARCHETYPES)
    same = ("identical to the current <code>tagging_schema.py</code>" if not differ else
            "these differ from the current <code>tagging_schema.py</code>: " + e(", ".join(differ)) +
            "; the page shows the cold-run version")
    hood = (f'<details class="more hood"><summary>Under the hood</summary>'
            f'<p>Version: <code>BIG_SEVEN_DEFINITIONS</code> in <code>tagging_schema.py</code> at commit '
            f'<code>{DEFS_COMMIT}</code>, the Full of Grace cold run (2026-09-26); {same}. The prompt sent each '
            f'one as “Name: definition” (<code>llm_orchestration._format_archetype_definitions</code>). Shown '
            f'word for word; the build checks every definition and this label are on the page exactly, which '
            f'is the only way they are exempt from the report’s word checks.</p></details>')
    intro = "".join(f'<p class="defs-intro">{e(x)}</p>' for x in DEFS_INTRO)
    return (f'<section class="panel defs" aria-labelledby="defs-h"><h2 id="defs-h">{e(DEFS_HEADING)}</h2>'
            f'{intro}{items}{hood}</section>')


def verbatim_class(page_html):
    """The verbatim class for the final scan, after checking the page holds
    every cold-run definition exactly (as escaped HTML) and the label."""
    if not SHOW_DEFINITIONS_APPENDIX:
        return None
    defs, _ = cold_run_definitions()
    for a in ARCHETYPES:
        if def_paragraph(a, defs[a]) not in page_html:
            sys.exit(f"ABORT: the {a} definition is not on the page exactly as in {DEFS_COMMIT}")
    for x in DEFS_INTRO:
        if f'<p class="defs-intro">{e(x)}</p>' not in page_html:
            sys.exit("ABORT: the definitions appendix is missing its label")
    return {"label": list(DEFS_INTRO), "texts": [defs[a] for a in ARCHETYPES]}


# --- Sections 2 and 3: template wording only --------------------------------
# Every reader-facing string for these sections is here or in TEXT, and the
# build checks them all for pipeline terms and grading words. Item text is
# filled from these templates; nothing is written per item.
TURNING_POINTS = os.path.join(ROOT, "fog_turning_points_reviewed.json")
DRAFT_FIELD = "causal_integrity (weight_proportionality + characterization_consistency)"
TURN_ORDER = ["throughline_evolution", "boundary_revealed"]
TURN_LABEL = {"throughline_evolution": "A change that’s justified", "boundary_revealed": "A limit revealed"}
# Glosses follow CAUSAL_INTEGRITY_PRINCIPLES 7 and 8 (tagging_schema.py).
TURN_GLOSS = {
    "throughline_evolution": "something already established about the character grows, deepens, or comes back in a new form.",
    "boundary_revealed": "the character shows something new about what they’re capable of: a limit, a weakness, or a strength not seen before.",
}
# A flag is any of these values; each has one sentence.
FLAG_FIELDS = {"wp": "mismatch", "cc": "contradicted", "aa": "displaced"}
FLAG_TEXT = {
    "mismatch": "{name}’s reaction may be out of proportion to what prompts it on the page.",
    "contradicted": "{name}’s behavior may not fit what earlier pages establish about them.",
    "displaced": "what happens here may be driven by someone other than {name}.",
}
# Scope: one flagged moment; two or more in one scene; flags in 3+ scenes.
SCOPE = {"moment": "A moment", "sequence": "A sequence", "throughline": "A character’s throughline"}
ROLE_MIN = 3
TEXT = {
    "banner_p2_reviewed": "Human Reviewed: a person checked every turning point and every flag the AI raised. "
                          "Moments the AI read as unremarkable were not each re-checked.",
    "turns_intro": "Moments where a character changes, or shows something new about themselves. "
                   "Tap a page number to read the corresponding scene.",
    "turns_count_cold": "The AI marked {n} turning points across {c} characters.",
    "turns_count_reviewed": "{n} turning points across {c} characters.",
    "hold_intro_cold": "For each character: how many of their moments the AI read as in character, "
                       "with a reaction in proportion to what prompts it.",
    "hold_intro_reviewed": "For each character: how many of their moments read as in character, "
                           "with a reaction in proportion to what prompts it.",
    "hold_cols": ["Character", "Moments in character and in proportion", "Pages"],
    "roles_intro": "Characters who present as the same archetype in {m} or more moments. "
                   "Tap a page number to read the scene and how the AI read it.",
    "roles_none": "No character presents as the same archetype in {m} or more moments.",
    "waver_intro": "Here’s what the AI noticed. These are observations, not verdicts: you know your story.",
    "waver_count": "The AI flagged {n} moments.",
    "waver_empty_reviewed": "No inconsistency held up on review.",
    "waver_empty_cold": "The AI flagged no moments here.",
    "flag_label": "Flagged by the AI",
    "was_turn": "In the AI Output, this moment was marked “{label}”.",
    "was_not_turn": "In the AI Output, this moment was not marked as a turning point.",
    "was_absent": "This moment is not in the AI Output; it was added in review.",
}
FORBIDDEN = [r"boundary_revealed", r"throughline_evolution", r"weight_proportionality",
             r"characterization_consistency", r"agency_alignment", r"scene\d+_beat\d+", r"\bcold\b",
             r"\bPass [12]\b", r"provenance", r"comparison beat", r"fog_", r"corrections log",
             r"requires_second_pass", r"\btrait \d"]
GRADING = [r"\bproblem", r"\bflaw", r"\bweak", r"\bstrong", r"needs work", r"\bunearned",
           r"\bfail", r"\bgood\b", r"\bbad\b", r"\berror", r"\bmistake", r"\bwrong\b"]


# Step 3 final scan (report_guard.final_scan), scoped by text type per the
# author's ruling of 2026-10-05 (STORY_REPORT_SPEC.md, "Scoping the
# guard"). Static copy and fixed templates are exempt from the banned-word
# check only when the exact string is listed here. Any other finding stops
# the build; nothing is left pending.
APPROVED_STATIC = {
    WHY_HEADING,  # '"Why should I care?"' (review edit 1; was without quotation marks)
    "It gives no grade.",
    # Review edit 5, approved by the author 2026-10-05 ("grades").
    "This report never grades a script or tells anyone what to write or how to improve the story.",
    TURN_GLOSS["boundary_revealed"],  # "...a limit, a weakness, or a strength not seen before."
    # Review edit 21, approved by the author 2026-10-05 ("good or bad"; flagged
    # by report.py's GRADING list, not by report_guard).
    "And above all else: it never judges whether a story is good or bad.",
    # Definitions appendix intro (author, 2026-10-05). Its "ordinary_reaction" is
    # a pipeline term, which this list cannot exempt; these lines are also the
    # verbatim class's label (DEFS_INTRO), checked exactly.
    *DEFS_INTRO,
}
# The AI's stored per-moment reads are exempt from banned words as a class,
# but only while they are shown verbatim AND labelled as the AI's read.
# The build checks that both labels are on the page.
AI_READ_LABELS = ("How the AI read this moment", "The AI’s read:")


def reader_strings(data):
    """Every data string the page shows a reader above the fold, as
    (where, text, text class) for the final scan. Beat text (script) and
    "Under the hood" content are excluded."""
    out = []
    # Fixed templates and author-written copy.
    for k, v in data["text"].items():
        out += [(f"TEXT[{k}]", s, "static") for s in (v if isinstance(v, list) else [v])]
    out += [("TURN_LABEL", v, "static") for v in data["turnLabel"].values()]
    out += [("TURN_GLOSS", v, "static") for v in data["turnGloss"].values()]
    out += [("GLOSS", v, "static") for v in data["gloss"].values()]
    out += [("character name", n, "static") for n in data["names"].values()]
    for v in ("cold", "reviewed"):
        if data["s3"]:
            out += [(f"section 3 item ({v})", g["text"], "static") for g in data["s3"][v]["groups"]]
        for i in data["p2info"][v].values():
            out += [(f"section 2/3 panel {f}", i[f], "static") for f in ("label", "gloss", "note") if i.get(f)]
    # Section 1: the AI's genre and synopsis are report-voice text.
    d = data.get("devread")
    if d:
        out += [(f"development read {k}", d[k], "report_voice") for k in ("genre", "logline", "synopsis") if d.get(k)]
    # Plain-language wording in the report's own voice.
    out += [(f"CHANGE_LINES {k}", c["line"], "report_voice") for k, c in data["changes"].items()]
    # The AI's stored reads, shown verbatim and labelled (AI_READ_LABELS).
    for key, x in data["ai"].items():
        for f in ("audience_perceived", "self_perceived", "emotion", "goal", "embodies"):
            vals = x["fields"].get(f) or []
            out += [(f"AI read {key} {f}", v, "ai_read") for v in (vals if isinstance(vals, list) else [vals]) if v]
    return out


def display_name(c):
    return c.title()


def check_plain(where, s):
    """Pipeline terms anywhere; grading words except inside an approved
    static string (APPROVED_STATIC, author ruling 2026-10-05)."""
    graded = html.unescape(s)
    for a in APPROVED_STATIC:
        graded = graded.replace(a, " ")
    for pat in FORBIDDEN:
        if re.search(pat, s, re.I):
            sys.exit(f"ABORT: {where}: reader-facing text {s[:80]!r} contains {pat!r}")
    for pat in GRADING:
        if re.search(pat, graded, re.I):
            sys.exit(f"ABORT: {where}: reader-facing text {s[:80]!r} contains {pat!r}")


def e(s):
    return html.escape(str(s), quote=True)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\f", " ")).strip()


PAGE_NO_RE = re.compile(r"^\f?\s*\d+\.\s*$")
CUE_RE = re.compile(r"^[A-Z0-9][A-Z0-9 .,'’()/&-]*$")
# Dual dialogue: two speaker cues side by side on one line (4 in FOG).
DUAL_CUE_RE = re.compile(r"^(\s+)([A-Z][A-Z .'’()-]+\S)(\s{4,})([A-Z][A-Z .'’()-]+?)\s*$")
SLUG_START = ("INT.", "EXT.", "INT/", "EXT/")


def dual_block(raw):
    """A dual-dialogue paragraph kept in its column layout, plus each
    column's text read top to bottom (used only to verify the full text).
    Per body line: a line indented 20+ spaces is right column only;
    otherwise it splits at the first gap of 2+ spaces that ends at column 25+."""
    m = DUAL_CUE_RE.match(raw[0])
    lines = [l.rstrip() for l in raw]
    left, right = [m.group(2)], [m.group(4)]
    for l in lines[1:]:
        if not l.strip():
            continue
        if len(l) - len(l.lstrip()) >= 20:
            right.append(l.strip())
            continue
        g = next((g for g in re.finditer(r"\S( {2,})\S", l) if g.end(1) >= 25), None)
        if g:
            left.append(l[:g.start(1)].strip())
            right.append(l[g.end(1):].strip())
        else:
            left.append(l.strip())
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    return {"pre": "\n".join(l[indent:] for l in lines),
            "cols": " ".join(left) + " " + " ".join(right), "_raw": raw}


def beat_text(lines, a, z, approx):
    """Full beat text from fog_full.txt lines a..z, as display blocks.
    Page-number header lines are dropped. Wrapped lines are joined with a
    space; nothing else is changed. Dual-dialogue paragraphs keep their
    column layout; a right-column line set off by a blank line is folded
    back into its dual block."""
    raw = [lines[i - 1].replace("\f", "") for i in range(a, z + 1)]
    raw = [l for l in raw if not PAGE_NO_RE.match(l)]
    blocks, cur = [], []
    for l in raw + [""]:
        if l.strip():
            cur.append(l)
            continue
        if not cur:
            continue
        if DUAL_CUE_RE.match(cur[0]):
            blocks.append(dual_block(cur))
            cur = []
            continue
        st = [x.strip() for x in cur]
        first = st[0]
        if blocks and "_raw" in blocks[-1] and len(cur[0]) - len(cur[0].lstrip()) >= 20 \
                and not CUE_RE.match(first):
            blocks[-1] = dual_block(blocks[-1]["_raw"] + [""] + cur)
        elif CUE_RE.match(first) and first.startswith(SLUG_START):
            blocks.append({"slug": " ".join(st)})
        elif CUE_RE.match(first) and len(first) < 45 and re.search(r"[A-Z]{2}", first):
            # A speaker cue, with its line or (when a blank line split them) alone.
            blocks.append({"cue": first, "t": " ".join(st[1:])})
        else:
            blocks.append({"t": " ".join(st)})
        cur = []
    return blocks


def page_positions(lines):
    """Fractional printed-page position of each line: printed page N spans
    [N, N+1). PDF page p is printed page p-1."""
    page_of, pg = [], 1
    for line in lines:
        pg += line.count("\f")
        page_of.append(pg)
    first_line_of = {}
    for i, p in enumerate(page_of, 1):
        first_line_of.setdefault(p, i)

    def pos(n):
        p = page_of[n - 1]
        a = first_line_of[p]
        b = first_line_of.get(p + 1, len(lines) + 1)
        return (p - 1) + (n - a) / max(1, b - a)
    return pos, page_of[-1] - 1


def build():
    with open(MODEL, encoding="utf-8") as f:
        model = json.load(f)
    with open(LINE_INDEX, encoding="utf-8") as f:
        index = json.load(f)["beats"]
    with open(FULL_TXT, encoding="utf-8") as f:
        lines = f.read().split("\n")
    with open(TAGGED, encoding="utf-8") as f:
        tagged = json.load(f)
    pos, max_page = page_positions(lines)
    alias = model["aliases"]

    # One record per (beat, display character); aliased entries merged.
    def collapse(entries):
        out = {}
        for x in entries:
            k = (x["beat_id"], x["display_character"])
            m = out.setdefault(k, {"a": [], "k": None, "fields": None, "src": []})
            m["src"].append(x["character"])
            for a in x["archetypes"]:
                if a not in m["a"]:
                    m["a"].append(a)
            if x["kind"] and not m["k"]:
                m["k"] = x["kind"]
            if x["archetypes"] or m["fields"] is None:
                m["fields"] = {f: x[f] for f in ("audience_perceived", "self_perceived",
                                                 "emotion", "goal", "embodies")}
        for m in out.values():
            if m["a"]:
                m["k"] = None
        return out

    views = {v: collapse(model["views"][v]) for v in ("cold", "reviewed")}

    # Compare the AI entry under its reviewed name (finding 6 / 13 renames).
    cold_cmp = dict(views["cold"])
    for b, old, new in model["entity_renames"]:
        ok, nk = (b, alias.get(old, old)), (b, alias.get(new, new))
        if ok == nk or ok not in cold_cmp:
            continue
        m = cold_cmp.pop(ok)
        cold_cmp.setdefault(nk, m)

    def call(m):
        return tuple(m["a"]) if m and m["a"] else ()

    # Archetype-involving changes (a non-tag to another non-tag never
    # shows as a mark, so it needs no line).
    changed = {k for k in set(cold_cmp) | set(views["reviewed"])
               if call(cold_cmp.get(k)) != call(views["reviewed"].get(k))}
    keys_needed = {f"{b}|{c}" for b, c in changed}
    missing = keys_needed - set(CHANGE_LINES)
    extra = set(CHANGE_LINES) - keys_needed
    if missing or extra:
        sys.exit(f"ABORT: change lines missing {sorted(missing)} / not a change {sorted(extra)}")
    log = tagged["corrections"]
    for key, (_, nums) in CHANGE_LINES.items():
        b, c = key.split("|")
        for n in nums:
            ent = log[n - 1]
            if ent["beat_id"] != b or alias.get(ent["character"], ent["character"]) != c \
                    or ent["field_name"] not in ("archetypes", "kind"):
                sys.exit(f"ABORT: {key} cites log {n}, which is "
                         f"{ent['beat_id']} {ent['character']} {ent['field_name']}")

    # Characters shown: anyone with an archetype call in either view.
    with_calls = Counter()
    for v in views.values():
        for (b, c), m in v.items():
            if m["a"]:
                with_calls[c] += 1
    beat_counts = Counter(c for (_, c) in views["reviewed"])
    order = sorted(with_calls, key=lambda c: (-beat_counts[c], c))
    top, rest = order[:TOP_N], order[TOP_N:]

    lanes = defaultdict(set)
    for v in views.values():
        for (_, c), m in v.items():
            lanes[c].update(m["a"])

    marked_beats = set()

    def marks_for(c):
        out = {}
        for v, vm in views.items():
            ms = []
            for (b, cc), m in vm.items():
                if cc == c and m["a"]:
                    ms.append([b, m["a"], 0])
                    marked_beats.add(b)
            if v == "reviewed":
                # AI calls that review removed: outlined, in their old lanes.
                for (b, cc), m in cold_cmp.items():
                    if cc != c or not m["a"]:
                        continue
                    now = views["reviewed"].get((b, cc))
                    gone = [a for a in m["a"] if not (now and a in now["a"])]
                    if gone:
                        ms.append([b, gone, 1])
                        marked_beats.add(b)
            ms.sort(key=lambda x: (beat_id_sort_key(x[0]), x[2]))
            out[v] = ms
        return out

    def char_payload(c):
        names = sorted({n for vm in views.values() for (b, cc), m in vm.items()
                        if cc == c for n in m["src"]})
        return {"name": c, "names": names, "beats": beat_counts[c],
                "lanes": [a for a in ARCHETYPES if a in lanes[c]], "marks": marks_for(c)}

    chars_top = [char_payload(c) for c in top]
    chars_rest = [char_payload(c) for c in rest]

    s2, s3, p2info, p2_beats, p2_stats = build_sections_2_3(model, index, tagged, views, alias)

    beats = {}
    for b in sorted(marked_beats | p2_beats, key=beat_id_sort_key):
        r = index[b]
        approx = r["placement"] == "bracketed"
        garbled = []
        if r["placement"] == "extended" and "matched_first_line" in r:
            # Lines before the matched start came out of the PDF garbled
            # (finding 12): shown exactly as extracted, columns and all.
            g = [lines[i - 1].replace("\f", "") for i in range(r["first_line"], r["matched_first_line"])]
            g = [l for l in g if not PAGE_NO_RE.match(l)]
            while g and not g[-1].strip():
                g.pop()
            ind = min(len(l) - len(l.lstrip()) for l in g if l.strip())
            garbled = [{"pre": "\n".join(l.rstrip()[ind:] for l in g), "garbled": 1}]
            blocks = garbled + beat_text(lines, r["matched_first_line"], r["last_line"], False)
        else:
            blocks = beat_text(lines, r["first_line"], r["last_line"], approx)
        shown = norm(" ".join(x.get("cols") or " ".join(v for v in x.values() if isinstance(v, str)) for x in blocks))
        # Every stored turn must appear in the text shown (the full beat).
        # Dual-dialogue columns are checked column by column.
        skip = set(r.get("unmatched_turns", [])) if r["placement"] == "extended" else set()
        if not approx:
            for ti, t in enumerate(tagged["beats"][b]["source_evidence"]["turns"]):
                if ti in skip:
                    continue
                for seg in re.split(r"\([^()]*\)", norm(t["text"])):
                    seg = seg.strip()
                    if len(seg) > 2 and seg not in shown:
                        sys.exit(f"ABORT: {b}: turn text {seg[:60]!r} missing from the text shown")
        beats[b] = {"x": round(pos(r["first_line"]), 3), "pages": r["printed_pages"],
                    "lines": [r["first_line"], r["last_line"]], "approx": approx,
                    "dual": any("pre" in x and not x.get("garbled") for x in blocks),
                    "garbled": bool(garbled),
                    "blocks": [{k: v for k, v in x.items() if k not in ("cols", "_raw", "garbled")} for x in blocks]}

    timeline, tl_stats = build_timeline(views, beats, index)

    shown_keys = {(m[0], ch["name"]) for ch in chars_top + chars_rest
                  for v in ("cold", "reviewed") for m in ch["marks"][v]}
    ai = {f"{b}|{c}": {"call": cold_cmp[(b, c)]["a"], "fields": cold_cmp[(b, c)]["fields"]}
          for (b, c) in sorted(shown_keys, key=lambda k: (beat_id_sort_key(k[0]), k[1])) if (b, c) in cold_cmp}

    changes = {}
    for key, (line, nums) in CHANGE_LINES.items():
        b, c = key.split("|")
        changes[key] = {"line": line, "logs": [{"n": n, "note": log[n - 1]["notes"]} for n in nums],
                        "was": list(call(cold_cmp.get((b, c)))),
                        "now": list(call(views["reviewed"].get((b, c))))}

    totals = {v: {"calls": sum(1 for m in vm.values() if m["a"])} for v, vm in views.items()}

    # Which marks have stored reasoning from the AI run.
    reasoning = {"ai_made_call": [], "ai_no_call_but_fields": [], "no_ai_entry": []}
    for (b, c) in sorted(shown_keys, key=lambda k: (k[1], beat_id_sort_key(k[0]))):
        m = cold_cmp.get((b, c))
        if m is None:
            reasoning["no_ai_entry"].append(f"{c} {b}")
            continue
        has = any(m["fields"][f] for f in ("audience_perceived", "self_perceived", "emotion", "goal"))
        bucket = "ai_made_call" if m["a"] else "ai_no_call_but_fields"
        reasoning[bucket].append((f"{c} {b}", has))

    # Every chip in sections 2-3 must open a beat with printed page numbers,
    # and every role chip must open an existing map panel.
    for b in p2_beats:
        if not beats[b]["pages"] or None in beats[b]["pages"]:
            sys.exit(f"ABORT: {b} has no printed page for its citation")
    for v in ("cold", "reviewed"):
        for r in s2[v]["roles"]:
            for b in r["beats"]:
                if (b, r["c"]) not in shown_keys:
                    sys.exit(f"ABORT: role chip {b} {r['c']} has no map panel")

    # Reader-facing names are title case; the script's cue names stay under the hood.
    cues = defaultdict(set)
    for v in ("cold", "reviewed"):
        for x in model["views"][v]:
            cues[x["display_character"]].add(x["character"])
    cues = {c: sorted(n) for c, n in cues.items()}
    names = {c: display_name(c) for c in cues}

    devread = load_dev_read()

    text = dict(TEXT, **TL_TEXT)
    # Review edit 13 (author, 2026-10-05): the banner drops COLD_LABEL's
    # caveat sentence; the full label stays under the hood.
    if not model["labels"]["cold"].startswith("Cold output: the AI's character-change judgments with no "
                                              "human correction."):
        sys.exit("ABORT: COLD_LABEL changed; re-check the section 2 banner wording")
    # Author wording (2026-10-06): Pass 2 ran on human-reviewed archetype calls.
    text["banner_p2_cold"] = ("AI Output: the AI's character-change judgments, unedited. "
                              "They were made after human review of its archetype calls.")
    for k, v in text.items():
        for s in (v if isinstance(v, list) else [v]):
            check_plain(f"TEXT[{k}]", s)

    data = {
        "maxPage": max_page, "archetypes": ARCHETYPES, "gloss": GLOSS,
        "beats": beats, "top": chars_top, "rest": chars_rest,
        "ai": ai, "changes": changes, "totals": totals,
        # Section 3 data stays out of the page while the section is off.
        "s2": s2, "s3": s3 if SHOW_CONSISTENCY_CHECK else None,
        "p2info": p2info if SHOW_CONSISTENCY_CHECK else
        {v: {k: x for k, x in p2info[v].items() if not k.startswith("flag|")} for v in p2info},
        "text": text, "names": names, "cues": cues,
        "turnLabel": TURN_LABEL, "turnGloss": TURN_GLOSS, "turnOrder": TURN_ORDER, "roleMin": ROLE_MIN,
        "devread": devread,
        "timeline": timeline, "tlPages": list(TL_PAGES), "mapSection": MAP_SECTION,
    }
    stats = {"changed": len(changed), "shown_keys": len(shown_keys), "beats_with_text": len(beats),
             "top": top, "rest": rest, "reasoning": reasoning, "p2": p2_stats, "timeline": tl_stats,
             "pass2_order": pass2_order(model["built_from"]["cold_pass1"], model["built_from"]["cold_pass2"])}
    return data, model, stats


def build_timeline(views, beats, index):
    """Section 4's marks: one per archetype call per (beat, character) in
    each view, the same calls as the character map. A mark's position is
    its beat's x, the printed-page position of the beat's first line. Human
    Reviewed Great Mother marks carry the pole from the review records."""
    tl, poles, approx = {}, [], []
    for v, vm in views.items():
        out = []
        for (b, c), m in vm.items():
            if not m["a"]:
                continue
            r = beats.get(b)
            if r is None:
                sys.exit(f"ABORT: timeline mark {b} {c} has no beat position")
            if not (TL_PAGES[0] <= r["x"] < TL_PAGES[1] + 1
                    and all(TL_PAGES[0] <= p <= TL_PAGES[1] for p in r["pages"])):
                sys.exit(f"ABORT: timeline mark {b} {c} at {r['x']} (pages {r['pages']}) is off pages {TL_PAGES}")
            if index[b]["placement"] != "matched" and (b, c) not in approx:
                approx.append((b, c))
            for a in m["a"]:
                x = {"b": b, "c": c, "a": a}
                if v == "reviewed" and a == "Great Mother":
                    rec = next((rr for rr in (review_row(n, b) for n in m["src"]) if rr), None)
                    if rec is None:
                        sys.exit(f"ABORT: no review row for the Great Mother call {b} {c} ({m['src']})")
                    x["pole"], src = great_mother_pole(rec)
                    poles.append({"b": b, "c": c, "pole": x["pole"], "source": src, "file": rec["file"]})
                out.append(x)
        out.sort(key=lambda x: (beats[x["b"]]["x"], ARCHETYPES.index(x["a"]), x["c"]))
        tl[v] = out
    # Every position is a matched first line except the ones described
    # under the hood; any other kind stops the build until it has a note.
    notes = []
    for b, c in sorted(approx, key=lambda k: beat_id_sort_key(k[0])):
        r = index[b]
        if r["placement"] != "extended" or "matched_first_line" not in r:
            sys.exit(f"ABORT: timeline mark {b} {c} has placement {r['placement']!r}, with no under-the-hood note")
        notes.append({"b": b, "c": c, "pages": beats[b]["pages"], "first": r["first_line"],
                      "matched": r["matched_first_line"]})
    return tl, {"poles": poles, "approx": notes}


# The commits around the Pass 2 run (checked at build time by pass2_order()).
PASS2_BEFORE = "d294e1c"     # last commit before any Pass 2 draft
PASS2_PARTIAL = "e26724d"    # first commit with Pass 2 drafts (6 of 32 characters)
PASS2_DRAFT_NOTE = "AWAITING HUMAN REVIEW"


def pass2_order(cold_pass1, cold_pass2):
    """How many human corrections were already in fog_tagged.json when the
    Pass 2 drafts were applied, verified from git: none at the cold Pass 1
    snapshot, N at PASS2_BEFORE with no drafts, and every draft logged after
    entry N in both Pass 2 commits."""
    def log_at(c):
        return git_snapshots.show_json(c, "fog_tagged.json")["corrections"]

    def drafts(cs):
        return [i for i, x in enumerate(cs, 1) if PASS2_DRAFT_NOTE in (x.get("notes") or "")]

    if log_at(cold_pass1):
        sys.exit(f"ABORT: the cold Pass 1 snapshot {cold_pass1} already has corrections")
    before = log_at(PASS2_BEFORE)
    n = len(before)
    if drafts(before):
        sys.exit(f"ABORT: {PASS2_BEFORE} already holds Pass 2 drafts")
    for c in (PASS2_PARTIAL, cold_pass2):
        cs = log_at(c)
        d = drafts(cs)
        if not d or min(d) != n + 1 or len(cs) - n != len(d) or cs[:n] != before:
            sys.exit(f"ABORT: at {c} the Pass 2 drafts are not all logged after the {n} earlier corrections")
    first = git_snapshots.first_commit_touching(cold_pass1, PASS2_BEFORE, "fog_tagged.json")
    done = log_at(cold_pass2)
    return {"n": n, "first": first, "before": PASS2_BEFORE, "partial": PASS2_PARTIAL,
            "complete": cold_pass2, "drafts": len(drafts(done)),
            "draft_chars": len({done[i - 1]["character"] for i in drafts(done)})}


def load_dev_read():
    """fog_dev_read.json, re-checked at build time: the title must still
    match the title page, and the AI's genre, logline and synopsis must pass
    the guard as report-voice summary text. None if the file doesn't exist."""
    if not os.path.exists(DEV_READ):
        return None
    with open(DEV_READ, encoding="utf-8") as f:
        d = json.load(f)
    import fog_dev_read_runner as runner
    printed, display = runner.extract_title()
    if (d["title_printed"], d["title"]) != (printed, display):
        sys.exit(f"ABORT: {os.path.basename(DEV_READ)} title {d['title']!r} != title page {display!r}")
    lines = runner.read_script().split("\n")
    # The AI's own text: what is displayed, except for a field with a logged
    # formatting repair, whose AI original is stored beside it.
    fix = d.get("formatting_repair")
    ai_text = {k: d.get(k) for k in ("genre", "logline", "synopsis")}
    if fix:
        ai_text[fix["field"]] = fix["ai_original"]
        # Displayed = the stored AI text plus only the logged repair.
        try:
            repaired = runner.check_repair(fix["ai_original"], fix["old"], fix["new"])
        except ValueError as ex:
            sys.exit(f"ABORT: development read formatting repair refused: {ex}")
        if repaired != d[fix["field"]]:
            sys.exit("ABORT: the displayed development read is not the AI text plus only the logged repair")
    attempt_no = d.get("accepted_attempt") or (d["attempts"] if fix else None)
    if attempt_no:
        # The AI text must be the saved API response, word for word.
        with open(runner.CALL_PATH, encoding="utf-8") as f:
            saved = next(a for a in json.load(f)["attempts"] if a["attempt"] == attempt_no)
        raw = json.loads(saved["raw_text"])
        if any(raw[k].strip() != ai_text.get(k) for k in raw):
            sys.exit("ABORT: the stored development read differs from the saved API response")
    if d.get("generated_by_prompt_version") is not None or d.get("generating_prompt_file"):
        try:
            runner.check_generating_prompt(d)
        except ValueError as ex:
            sys.exit(f"ABORT: development read generating prompt: {ex}")
    for x in (d.get("author_check") or {}).get("issues", []):
        if x["text"] not in (ai_text.get(x["field"]) or ""):
            sys.exit(f"ABORT: author check cites {x['text']!r}, which is not in the AI's {x['field']}")
    for k in ("genre", "logline", "synopsis"):
        if d.get(k):
            v = report_guard.check_text(d[k], "summary", full_lines=lines)
            if v:
                sys.exit(f"ABORT: development read {k} fails the guard: {[str(x) for x in v]}")
    return d


def build_sections_2_3(model, index, tagged, views, alias):
    """Sections 2 ("Character arcs: where characters change, and where they
    don't") and 3 ("Consistency check: a second look"), for both views. Returns the per-view section data, the panel
    content for each page chip, the beats the chips open, and counts."""
    log = tagged["corrections"]
    scene_of = {b: r["scene_id"] for b, r in model["beats"].items()}
    rank = {None: 0, "requires_second_pass": 1, "consistent": 2, "matched": 2, "aligned": 2}

    def collapse_p2(entries):
        """(beat, display character) -> Pass 2 values. Where two stored
        names merge (JOHN / YOUNG JOHN), the more notable value wins."""
        out = {}
        for x in entries:
            k = (x["beat_id"], x["display_character"])
            rec = {"cc": x["characterization_consistency"], "wp": x["weight_proportionality"],
                   "aa": x["agency_alignment"]}
            if k in out:
                for f in rec:
                    if rank.get(rec[f], 3) > rank.get(out[k][f], 3):
                        out[k][f] = rec[f]
            else:
                out[k] = rec
        return out

    p2 = {v: collapse_p2(model["views"][v]) for v in ("cold", "reviewed")}
    # The AI entry under its reviewed name (finding 6 / 13 renames), for comparing.
    cold_cmp = dict(p2["cold"])
    for b, old, new in model["entity_renames"]:
        ok, nk = (b, alias.get(old, old)), (b, alias.get(new, new))
        if ok != nk and ok in cold_cmp:
            cold_cmp.setdefault(nk, cold_cmp.pop(ok))

    # The AI's Pass 2 draft note for each entry, verbatim, by log number.
    renamed_from = {(b, new): old for b, old, new in model["entity_renames"]}
    drafts = defaultdict(list)
    for i, ent in enumerate(log, 1):
        if ent["field_name"] != DRAFT_FIELD:
            continue
        b, c = ent["beat_id"], ent["character"]
        for name in {c, renamed_from.get((b, c))} - {None}:
            drafts[(b, alias.get(name, name))].append(i)

    with open(TURNING_POINTS, encoding="utf-8") as f:
        tps = json.load(f)["turns"]
    tp = {(t["beat_id"], alias.get(t["character"], t["character"])): t for t in tps}

    def pages(bs):
        ps = [p for b in bs for p in index[b]["printed_pages"]]
        return [min(ps), max(ps)]

    def draft_hood(b, c):
        return [[f"The AI’s draft note before review (corrections log #{n})", log[n - 1]["notes"]]
                for n in drafts.get((b, c), [])]

    s2, s3, info, used = {}, {}, {}, set()
    for v in ("cold", "reviewed"):
        P = p2[v]
        info[v] = {}
        counts = Counter(c for (_, c) in P)
        by_count = lambda c: (-counts[c], c)  # noqa: E731

        # Turning points.
        turns = defaultdict(lambda: defaultdict(list))
        for (b, c), r in P.items():
            if r["cc"] in TURN_LABEL:
                turns[c][r["cc"]].append(b)
        turn_rows = []
        for c in sorted(turns, key=by_count):
            groups = []
            for t in TURN_ORDER:
                bs = sorted(turns[c][t], key=beat_id_sort_key)
                if bs:
                    groups.append({"type": t, "beats": bs})
                for b in bs:
                    used.add(b)
                    hood = [["Beat ID", b], ["Stored value", t]]
                    note = None
                    if v == "reviewed":
                        x = tp.get((b, c))
                        if x is None or x["verdict"] != t:
                            sys.exit(f"ABORT: reviewed turn {b} {c} is not in {os.path.basename(TURNING_POINTS)}")
                        r = x["reviewed"]
                        comp = r["comparison_beat_id"] or "none (its own origin)"
                        hood += [["Review status", r["status"]], ["Trait", r["trait"]], ["Shape", r["shape"]],
                                 ["Comparison beat", f"{comp}" + (f" ({r['comparison_source']})" if r["comparison_source"] else "")],
                                 ["Review note", r["note"]], ["Review record", ", ".join(r["sources"])],
                                 ["Checked", "author-checked line by line" if r["author_checked"] else r["verification"]]]
                        was = cold_cmp.get((b, c))
                        if was is None:
                            note = TEXT["was_absent"]
                        elif was["cc"] != t:
                            note = (TEXT["was_turn"].format(label=TURN_LABEL[was["cc"]]) if was["cc"] in TURN_LABEL
                                    else TEXT["was_not_turn"])
                            hood.append(["AI Output value", str(was["cc"])])
                    hood += draft_hood(b, c)
                    info[v][f"turn|{b}|{c}"] = {"label": TURN_LABEL[t], "gloss": TURN_GLOSS[t], "note": note,
                                                "hood": hood}
            turn_rows.append({"c": c, "name": display_name(c), "groups": groups})

        # Reactions that hold together.
        hold = []
        for c in sorted(counts, key=by_count):
            read = [b for (b, cc), r in P.items() if cc == c and r["cc"] not in (None, "requires_second_pass")]
            if not read:
                continue
            held = [b for (b, cc), r in P.items() if cc == c and r["cc"] in ("consistent", *TURN_ORDER)
                    and r["wp"] == "matched" and r["aa"] in (None, "aligned")]
            hold.append({"c": c, "name": display_name(c), "read": len(read), "held": len(held),
                         "pages": pages(read)})

        # Roles carried across the script (from the map's archetype calls).
        roles = []
        arch_beats = defaultdict(lambda: defaultdict(list))
        for (b, c), m in views[v].items():
            for a in m["a"]:
                arch_beats[c][a].append(b)
        for c in sorted(arch_beats, key=by_count):
            for a in ARCHETYPES:
                bs = sorted(arch_beats[c].get(a, []), key=beat_id_sort_key)
                if len(bs) >= ROLE_MIN:
                    roles.append({"c": c, "name": display_name(c), "arch": a, "beats": bs})
                    used.update(bs)

        s2[v] = {"turns": turn_rows, "n_turns": sum(len(g["beats"]) for r in turn_rows for g in r["groups"]),
                 "hold": hold, "roles": roles}

        # Consistency check: flags, grouped by character and scene.
        flagged = defaultdict(list)
        for (b, c), r in P.items():
            for f, val in FLAG_FIELDS.items():
                if r[f] == val:
                    flagged[(c, val)].append(b)
        groups = []
        for (c, val), bs in sorted(flagged.items(), key=lambda kv: (by_count(kv[0][0]), kv[0][1])):
            by_scene = defaultdict(list)
            for b in bs:
                by_scene[scene_of[b]].append(b)
            through = len(by_scene) >= 3
            for sc in sorted(by_scene, key=lambda s: beat_id_sort_key(by_scene[s][0])):
                g = sorted(by_scene[sc], key=beat_id_sort_key)
                scope = "throughline" if through else ("sequence" if len(g) > 1 else "moment")
                sentence = FLAG_TEXT[val].format(name=display_name(c))
                lead = "In this moment, " if len(g) == 1 else f"In these {len(g)} moments, "
                text = lead + sentence
                check_plain("waver item", text)
                groups.append({"c": c, "name": display_name(c), "scope": SCOPE[scope], "text": text,
                               "pages": pages(g), "beats": g})
                for b in g:
                    used.add(b)
                    r = P[(b, c)]
                    info[v][f"flag|{b}|{c}"] = {
                        "label": TEXT["flag_label"], "gloss": sentence, "note": None,
                        "hood": [["Beat ID", b],
                                 ["Stored values", f"weight_proportionality {r['wp']}, "
                                                   f"characterization_consistency {r['cc']}, "
                                                   f"agency_alignment {r['aa']}"]] + draft_hood(b, c)}
        s3[v] = {"groups": groups, "n": sum(len(g["beats"]) for g in groups)}

    # Checks against the recorded results.
    n_rev = s2["reviewed"]["n_turns"]
    if n_rev != len(tps):
        sys.exit(f"ABORT: {n_rev} reviewed turns shown, {len(tps)} in {os.path.basename(TURNING_POINTS)}")
    # How the AI's flags were resolved (shown under the hood, never above it).
    resolved = []
    for g in s3["cold"]["groups"]:
        for b in g["beats"]:
            ns = [i for i, ent in enumerate(log, 1) if ent["beat_id"] == b
                  and alias.get(ent.get("character"), ent.get("character")) == g["c"]
                  and ent["field_name"] == "weight_proportionality"]
            after = p2["reviewed"].get((b, g["c"]), {}).get("wp")
            resolved.append([b, g["name"], after, ns])
    excluded = sorted(f"{c} {b}" for (b, c), r in p2["reviewed"].items() if r["cc"] == "requires_second_pass")
    no_value = sum(1 for r in p2["reviewed"].values() if r["cc"] is None)
    s3["resolved"] = resolved
    stats = {v: {"turns": s2[v]["n_turns"], "turn_chars": len(s2[v]["turns"]), "hold_chars": len(s2[v]["hold"]),
                 "roles": [(r["c"], r["arch"], len(r["beats"])) for r in s2[v]["roles"]],
                 "flags": s3[v]["n"], "flag_groups": [(g["c"], g["scope"], len(g["beats"])) for g in s3[v]["groups"]]}
             for v in ("cold", "reviewed")}
    stats["excluded_rsp"] = excluded
    stats["no_value"] = no_value
    stats["resolved"] = resolved
    return s2, s3, info, used, stats


CSS = r"""
/* Fonts and color tokens: numen_theme.css (shared), inlined ahead of this. */
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.55 var(--font-body); }
main { max-width: 1240px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 28px; line-height: 1.2; font-weight: 500; margin: 0 0 4px; }
h2 { font-size: 21px; font-weight: 500; margin: 0 0 10px; }
.sub { color: var(--muted); margin: 0 0 20px; }
.status { font-size: 13px; color: var(--muted); border: 1px dashed var(--rule);
  border-radius: 6px; padding: 8px 12px; margin: 0 0 24px; }
.panel { background: var(--panel); border-radius: 8px; box-shadow: var(--shadow); padding: 20px 20px 24px; }
.toggle { display: inline-flex; border: 1px solid var(--rule); border-radius: 8px; overflow: hidden; margin: 0 0 10px; }
.toggle button { all: unset; cursor: pointer; padding: 8px 16px; font-size: 14px; font-weight: 600; color: var(--muted); }
.toggle button[aria-pressed="true"] { background: var(--ink); color: var(--panel); }
.toggle button:focus-visible { outline: 2px solid var(--muted); outline-offset: -2px; }
.banner { font-size: 14px; padding: 9px 12px; border-radius: 6px; margin: 0 0 16px;
  border-left: 4px solid var(--accent); background: var(--lane); }
.banner.reviewed { border-left-color: var(--human-rule); }
.intro p { margin: 0 0 10px; max-width: 72ch; }
.intro { margin: 0 0 16px; }
.what { margin: 0 0 18px; padding: 12px 14px; border-radius: 6px; background: var(--lane); }
.what h3 { margin: 0; font-size: 16px; font-weight: 500; }
.what p { margin: 8px 0 0; max-width: 72ch; font-size: 14px; }
.legend-h { margin: 0 0 6px; font-size: 13px; font-weight: 650; color: var(--ink); }
.legend { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 6px 18px;
  font-size: 13px; color: var(--muted); margin: 0 0 18px; }
.legend > span { display: flex; align-items: baseline; gap: 7px; }
.legend b { color: var(--ink); font-weight: 600; }
.key { flex: none; display: inline-block; width: 12px; height: 12px; border-radius: 3px; transform: translateY(1px); }
.key.out { border: 2px solid var(--muted); }
.note { font-size: 13px; color: var(--muted); margin: 0 0 14px; max-width: 72ch; }
.char { border-top: 1px solid var(--rule); padding: 14px 0 8px; }
.char-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 12px; margin: 0 0 6px; }
.char-head h3 { font-size: 17px; margin: 0; font-weight: 500; }
.char-head .sum { font-size: 13px; color: var(--muted); }
.row { display: grid; grid-template-columns: 110px minmax(0, 1fr); align-items: center; gap: 10px; min-height: 26px; }
.row .lab { font-size: 12.5px; color: var(--ink); font-weight: 600; text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.track { position: relative; height: 22px; background: var(--lane); border-radius: 4px; }
.mk { all: unset; box-sizing: border-box; position: absolute; top: 2px; width: 10px; height: 18px; margin-left: -5px;
  border-radius: 3px; box-shadow: 0 0 0 1.5px var(--lane); cursor: pointer; }
.mk.out { background: var(--lane); border: 2px solid; box-shadow: none; }
.mk:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
.mk::after { content: ""; position: absolute; inset: -6px -5px; }
.axis { position: relative; height: 22px; font-size: 11px; color: var(--faint); }
.axis > span { position: absolute; top: 4px; transform: translateX(-50%); white-space: nowrap; }
.axis-row { display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 10px; }
details.more { margin-top: 18px; border-top: 1px solid var(--rule); padding-top: 12px; }
details > summary { cursor: pointer; font-weight: 600; font-size: 14px; color: var(--muted); }
summary:focus-visible { outline: 2px solid var(--muted); outline-offset: 3px; }
.hood { font-size: 13px; color: var(--muted); }
.hood p { max-width: 80ch; }
.hood code, .sheet code { font-size: 12px; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; font-size: 13px; margin-top: 12px; width: 100%; }
th, td { text-align: left; padding: 5px 8px; border-bottom: 1px solid var(--rule); vertical-align: top; }
th { color: var(--muted); font-weight: 600; }
td.n { font-variant-numeric: tabular-nums; }
.tip { position: fixed; z-index: 10; pointer-events: none; max-width: 300px; background: var(--panel);
  color: var(--ink); border: 1px solid var(--rule); border-radius: 6px; box-shadow: var(--shadow);
  padding: 8px 10px; font-size: 12.5px; line-height: 1.45; display: none; }
.tip .t1 { font-weight: 650; }
.tip .t2 { color: var(--muted); }
.scrim { position: fixed; inset: 0; background: var(--scrim); z-index: 20; display: none; }
.sheet { position: fixed; z-index: 21; display: none; background: var(--panel); color: var(--ink);
  box-shadow: var(--shadow); overflow-y: auto; overscroll-behavior: contain;
  top: 16px; right: 16px; bottom: 16px; width: min(480px, calc(100vw - 32px)); border-radius: 10px;
  padding: 18px 20px 24px; }
.sheet.open, .scrim.open { display: block; }
.sheet h3 { font-size: 18px; margin: 0 40px 2px 0; line-height: 1.3; }
.sheet .gl { color: var(--muted); font-size: 13.5px; margin: 0 0 4px; }
.sheet .where { color: var(--muted); font-size: 13px; margin: 0 0 4px; }
.script pre + p, .script p + pre { margin-top: 9px; }
.sheet h4 { font-size: 13px; color: var(--muted); font-weight: 500; margin: 18px 0 6px; }
.close { all: unset; position: absolute; top: 12px; right: 12px; width: 36px; height: 36px; border-radius: 6px;
  display: grid; place-items: center; cursor: pointer; font-size: 24px; line-height: 1; color: var(--muted); }
.close:hover { background: var(--lane); }
.close:focus-visible { outline: 2px solid var(--ink); }
.script { background: var(--lane); border-radius: 6px; padding: 12px 14px; font: 14px/1.5 var(--font-script); }
.script p { margin: 0 0 9px; }
.script p:last-child { margin: 0; }
.script .cue { display: block; font-size: 14px; }
.script .slug { font-size: 14px; }
.script pre { margin: 0; font: 12.5px/1.45 var(--font-script); white-space: pre; overflow-x: auto; }
.reason dl { margin: 0; display: grid; gap: 8px; }
.reason dt { font-size: 12.5px; color: var(--muted); font-weight: 600; }
.reason dd { margin: 0; }
.reason .lead { margin: 0 0 10px; font-size: 13.5px; color: var(--muted); }
.changed { margin: 0; border-left: 4px solid var(--human-rule); background: var(--lane); border-radius: 6px; padding: 9px 12px; }
.sheet details { margin-top: 18px; border-top: 1px solid var(--rule); padding-top: 10px; }
.sheet details p { font-size: 12.5px; color: var(--muted); margin: 6px 0; overflow-wrap: anywhere; }
.panel + .panel { margin-top: 24px; }
.why { margin: 0 0 24px; }
.why h2 { margin-bottom: 8px; }
.why p, .why li { max-width: 72ch; }
.why p { margin: 0 0 10px; }
.why ul { margin: 0 0 12px; padding-left: 22px; }
.why li { margin: 0 0 6px; }
.why p:last-child { margin-bottom: 0; }
.not-measured p { margin: 0; max-width: 72ch; }
.dr { margin: 0 0 12px; display: grid; gap: 4px 0; max-width: 72ch; }
.dr dt { font-size: 13px; color: var(--muted); font-weight: 650; margin-top: 8px; }
.dr dd { margin: 0; }
.dr .dr-title { font-size: 17px; font-weight: 650; }
.muted { font-weight: 400; }
.deflink { font-size: 12px; color: var(--muted); white-space: nowrap; }
.defs .defs-intro { margin: 0 0 8px; max-width: 72ch; color: var(--muted); font-size: 14px; }
.defs h3 { font-size: 15px; margin: 18px 0 4px; scroll-margin-top: 16px; }
.defs h3:target { color: var(--accent); }
.defs p { margin: 0; max-width: 80ch; font-size: 14px; }
.dr-syn { margin: 4px 0 12px; max-width: 72ch; }
.dr-syn > summary { cursor: pointer; font-weight: 600; font-size: 14px; color: var(--muted); }
.dr-syn > div { margin-top: 8px; }
.dr-syn p { margin: 0 0 10px; }
.ai-label { margin: 10px 0 0; }
.sec h3 { font-size: 17px; font-weight: 500; margin: 22px 0 6px; }
.sec h3:first-of-type { margin-top: 4px; }
.sec .lead { margin: 0 0 10px; max-width: 72ch; }
.sec .count { margin: 0 0 12px; font-size: 14px; color: var(--muted); }
.types { display: grid; gap: 4px; margin: 0 0 12px; font-size: 13.5px; max-width: 80ch; }
.types b { font-weight: 650; }
.tp-row { display: grid; grid-template-columns: 140px minmax(0, 1fr); gap: 4px 12px; padding: 8px 0;
  border-top: 1px solid var(--rule); align-items: baseline; }
.tp-row .who { font-weight: 650; font-size: 14px; }
.tp-row .grp { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px; margin: 0 0 4px; }
.tp-row .grp:last-child { margin: 0; }
.tp-row .gl2 { font-size: 13px; color: var(--muted); margin-right: 2px; }
.chip { all: unset; box-sizing: border-box; cursor: pointer; font-size: 12.5px; font-variant-numeric: tabular-nums;
  padding: 2px 8px; border-radius: 999px; border: 1px solid var(--rule); background: var(--lane); color: var(--ink);
  white-space: nowrap; min-height: 24px; display: inline-flex; align-items: center; }
.chip:hover { border-color: var(--muted); }
.chip:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
/* Turning-point chips (.ev, .br): neutral ink, told apart by their label text. */
.roles { display: grid; gap: 6px; }
.roles > div { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px; }
.roles .what2 { font-size: 14px; margin-right: 4px; }
.flag { border-top: 1px solid var(--rule); padding: 12px 0 10px; }
.flag .scope { display: inline-block; font-size: 12px; font-weight: 650; color: var(--muted);
  border: 1px solid var(--rule); border-radius: 4px; padding: 1px 6px; margin-right: 8px; }
.flag .head { font-weight: 650; }
.flag p { margin: 6px 0 8px; max-width: 72ch; }
.flag .chips { display: flex; flex-wrap: wrap; gap: 6px; }
.empty { font-size: 15px; margin: 4px 0 8px; padding: 12px 14px; border-radius: 6px; background: var(--lane); }
.hold td.n { white-space: nowrap; }
footer { margin-top: 28px; font-size: 12px; color: var(--muted); }
/* Section 4, archetype timeline. Wide: pages left to right, one row per lane.
   Narrow (max-width 640px, set in JS): pages top to bottom, lanes side by side. */
.tl-chart { position: relative; margin: 4px 0 0; }
.tl-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; transform: translateY(1px); }
.tl-dot.hollow { background: transparent; border: 2px solid; margin-right: 8px; }
.tl-row { display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 10px; align-items: start; }
.tl-row + .tl-row { margin-top: 4px; }
.tl-row .lab { display: flex; justify-content: flex-end; align-items: center; gap: 6px; padding-top: 3px;
  font-size: 12.5px; font-weight: 600; white-space: nowrap; }
.tl-track { position: relative; background: var(--lane); border-radius: 4px; }
.tl-grid { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--rule); }
.tl-axis { position: relative; height: 20px; font-size: 11px; color: var(--faint); }
.tl-axis > span { position: absolute; top: 3px; transform: translateX(-50%); white-space: nowrap; }
.tlm { all: unset; box-sizing: border-box; position: absolute; width: 10px; height: 10px; margin: -5px 0 0 -5px;
  border-radius: 50%; background: var(--c); box-shadow: 0 0 0 1.5px var(--lane); cursor: pointer; }
.tlm.hollow { background: var(--lane); border: 2px solid var(--c); }
.tlm::after { content: ""; position: absolute; inset: -4px; border-radius: 50%; }
.tlm:focus-visible, .tlm[aria-expanded="true"] { outline: 2px solid var(--ink); outline-offset: 2px; }
.tl-lab, .tl-vlab { position: absolute; color: var(--ink); font-weight: 600; pointer-events: none; }
.tl-lab { font-size: 11.5px; line-height: 14px; white-space: nowrap; }
.tl-vlab { font-size: 10.5px; line-height: 12px; text-align: center; overflow-wrap: normal; }
.tl-vhead { position: sticky; top: 0; z-index: 2; display: grid; background: var(--panel);
  padding: 6px 0 6px; border-bottom: 1px solid var(--rule); }
.tl-vh { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 5px; }
.tl-vh span { writing-mode: vertical-rl; transform: rotate(180deg); font-size: 11.5px; font-weight: 600; white-space: nowrap; }
.tl-vh .key { width: 10px; height: 10px; }
.tl-vh.ax span { font-weight: 400; color: var(--faint); font-size: 11px; }
.tl-vbody { position: relative; margin-top: 6px; }
.tl-vcol { position: absolute; top: 0; bottom: 0; background: var(--lane); border-radius: 4px; }
.tl-vgrid { position: absolute; right: 0; height: 1px; background: var(--rule); }
.tl-vtick { position: absolute; left: 0; text-align: right; font-size: 10.5px; line-height: 12px; color: var(--faint);
  transform: translateY(-50%); }
.tl-pop { position: fixed; z-index: 12; display: none; max-width: 280px; background: var(--panel); color: var(--ink);
  border: 1px solid var(--rule); border-radius: 6px; box-shadow: var(--shadow); padding: 8px 12px 10px;
  font-size: 13px; line-height: 1.45; }
.tl-pop.open { display: block; }
.tl-pop .t1 { font-weight: 650; }
.tl-pop .t2 { color: var(--muted); }
.tl-pop a { display: inline-block; margin-top: 4px; padding: 2px 0; color: var(--ink); text-underline-offset: 2px; }
.tl-pop a:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
@media (max-width: 640px) {
  .axis .pw { display: none; }
  .row, .axis-row { grid-template-columns: 78px minmax(0, 1fr); gap: 6px; }
  .row .lab { font-size: 11px; }
  .tp-row { grid-template-columns: 1fr; }
  .sheet { top: auto; left: 0; right: 0; bottom: 0; width: 100%; max-height: 86vh;
    border-radius: 14px 14px 0 0; padding: 18px 16px 28px; }
}
"""

JS = r"""
const D = JSON.parse(document.getElementById('data').textContent);
const SLOT = Object.fromEntries(D.archetypes.map((a, i) => [a, `var(--s${i + 1})`]));
const ALL = D.top.concat(D.rest);
const HASH = new URLSearchParams(location.hash.slice(1));
// Each section has its own view; all default to AI Output. "#reviewed" (older
// shareable links) still opens the map in Human Reviewed.
const V = {s2: 'cold', s3: 'cold', map: HASH.has('reviewed') ? 'reviewed' : 'cold', tl: 'cold'};
const nm = c => D.names[c] || c;
const pct = x => (100 * x / D.maxPage).toFixed(3) + '%';
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
const pageText = b => b.pages[0] === b.pages[b.pages.length - 1] ? `Page ${b.pages[0]}` : `Pages ${b.pages[0]}–${b.pages[b.pages.length - 1]}`;

function summary(ch) {
  const view = V.map;
  const ms = ch.marks[view].filter(m => !m[2]);
  const c = {};
  ms.forEach(m => m[1].forEach(a => c[a] = (c[a] || 0) + 1));
  const parts = D.archetypes.filter(a => c[a]).map(a => `${a} ${c[a]}`);
  const removed = view === 'reviewed' ? ch.marks.reviewed.filter(m => m[2]).length : 0;
  let s = `In ${ch.beats} beats. ` + (ms.length ? `Archetype calls: ${ms.length} (${parts.join(', ')}).` : 'No archetype calls.');
  if (removed) s += ` ${removed} removed in review.`;
  return s;
}

function charBlock(ch) {
  const ms = ch.marks[V.map];
  let h = `<div class="char"><div class="char-head"><h3>${esc(nm(ch.name))}</h3><span class="sum">${esc(summary(ch))}</span></div>`;
  for (const a of ch.lanes) {
    h += `<div class="row"><div class="lab" title="${esc(a)}: ${esc(D.gloss[a])}">${esc(a)}</div><div class="track">`;
    for (const m of ms) if (m[1].includes(a)) {
      const b = D.beats[m[0]];
      const lab = `${nm(ch.name)}, ${a}${m[2] ? ', removed in review' : ''}, ${pageText(b)}`;
      h += `<button type="button" class="mk${m[2] ? ' out' : ''}" style="left:${pct(b.x)};${m[2] ? 'border-color' : 'background'}:${SLOT[a]}" ` +
        `data-b="${m[0]}" data-c="${esc(ch.name)}" data-a="${esc(a)}" data-o="${m[2]}" data-v="${V.map}" aria-label="${esc(lab)}" aria-haspopup="dialog"></button>`;
    }
    h += `</div></div>`;
  }
  return h + `</div>`;
}

function axis() {
  let h = '<div class="axis-row"><div></div><div class="axis" aria-hidden="true">';
  for (const p of [1].concat([...Array(Math.floor(D.maxPage / 10)).keys()].map(i => (i + 1) * 10)))
    h += `<span style="left:${pct(p)}">${p === 1 ? '<span class="pw">Page </span>1' : p}</span>`;
  return h + '</div></div>';
}

function table() {
  let h = '<table><thead><tr><th>Character</th>' + D.archetypes.map(a => `<th>${esc(a)}</th>`).join('') +
    '<th>Total</th></tr></thead><tbody>';
  for (const ch of ALL) {
    const ms = ch.marks[V.map].filter(m => !m[2]), c = {};
    ms.forEach(m => m[1].forEach(a => c[a] = (c[a] || 0) + 1));
    h += `<tr><td>${esc(nm(ch.name))}</td>` + D.archetypes.map(a => `<td class="n">${c[a] || ''}</td>`).join('') +
      `<td class="n">${ms.length}</td></tr>`;
  }
  return h + '</tbody></table>';
}

// --- sections 2 and 3 ---------------------------------------------------------
const T = D.text;
const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k]);
const pagesShort = p => p[0] === p[p.length - 1] ? `p. ${p[0]}` : `pp. ${p[0]}–${p[p.length - 1]}`;
const pagesLong = p => p[0] === p[1] ? `page ${p[0]}` : `pages ${p[0]}–${p[1]}`;
function chip(view, kind, bid, c, name, extra) {
  const b = D.beats[bid];
  return `<button type="button" class="chip${extra || ''}" data-k="${kind}" data-v="${view}" data-b="${bid}" data-c="${esc(c)}" data-n="${esc(name)}" ` +
    `aria-haspopup="dialog" aria-label="${esc(name)}, ${pagesShort(b.pages)}">${pagesShort(b.pages)}</button>`;
}
// Role chips open the map's archetype panel, so they carry the map's data attributes.
function roleChip(view, r, bid) {
  const b = D.beats[bid];
  return `<button type="button" class="chip mk-like" data-v="${view}" data-b="${bid}" data-c="${esc(r.c)}" data-a="${esc(r.arch)}" data-o="0" ` +
    `aria-haspopup="dialog" aria-label="${esc(r.name)}, ${esc(r.arch)}, ${pagesShort(b.pages)}">${pagesShort(b.pages)}</button>`;
}
function holdTable(rows) {
  return `<table class="hold"><thead><tr>${T.hold_cols.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>` +
    rows.map(r => `<tr><td>${esc(r.name)}</td><td class="n">${r.held} of ${r.read}</td>` +
      `<td class="n">${pagesShort(r.pages)}</td></tr>`).join('') + '</tbody></table>';
}
function renderLanding() {
  const view = V.s2, s = D.s2[view];
  let h = `<h3>Turning points</h3><p class="lead">${esc(T.turns_intro)}</p>` +
    `<div class="types">` + D.turnOrder.map(t => `<span><b>${esc(D.turnLabel[t])}</b>: ${esc(D.turnGloss[t])}</span>`).join('') + `</div>` +
    `<p class="count">${esc(fill(T['turns_count_' + view], {n: s.n_turns, c: s.turns.length}))}</p>`;
  for (const r of s.turns) {
    h += `<div class="tp-row"><div class="who">${esc(r.name)}</div><div>`;
    for (const g of r.groups)
      h += `<div class="grp"><span class="gl2">${esc(D.turnLabel[g.type])}:</span>` +
        g.beats.map(b => chip(view, 'turn', b, r.c, r.name, g.type === 'boundary_revealed' ? ' br' : ' ev')).join('') + `</div>`;
    h += `</div></div>`;
  }
  const top = s.hold.slice(0, 8), more = s.hold.slice(8);
  h += `<h3>Reactions that hold together</h3><p class="lead">${esc(T['hold_intro_' + view])}</p>` +
    `<div class="scroll">${holdTable(top)}</div>` +
    (more.length ? `<details class="more"><summary>More characters (${more.length})</summary><div class="scroll">${holdTable(more)}</div></details>` : '');
  h += `<h3>Roles carried across the script</h3>`;
  if (!s.roles.length) h += `<p class="lead">${esc(fill(T.roles_none, {m: D.roleMin}))}</p>`;
  else h += `<p class="lead">${esc(fill(T.roles_intro, {m: D.roleMin}))}</p><div class="roles">` +
    s.roles.map(r => `<div><span class="what2"><b>${esc(r.name)}</b> presents as <b>${esc(r.arch)}</b> in ${r.beats.length} moments:</span>` +
      r.beats.map(b => roleChip(view, r, b)).join('') + `</div>`).join('') + `</div>`;
  document.getElementById('landing').innerHTML = h;
}
function renderWaver() {
  const view = V.s3, s = D.s3[view];
  let h = '';
  if (!s.groups.length) {
    h += `<p class="empty">${esc(T['waver_empty_' + view])}</p>`;
  } else {
    h += `<p class="lead">${esc(T.waver_intro)}</p><p class="count">${esc(fill(T.waver_count, {n: s.n}))}</p>`;
    for (const g of s.groups)
      h += `<div class="flag"><span class="scope">${esc(g.scope)}</span><span class="head">${esc(g.name)}, ${pagesLong(g.pages)}</span>` +
        `<p>${esc(g.text)}</p><div class="chips">${g.beats.map(b => chip(view, 'flag', b, g.c, g.name)).join('')}</div></div>`;
  }
  document.getElementById('waver').innerHTML = h;
}

function setBanner(id, view, text) {
  const ban = document.getElementById(id);
  ban.textContent = text;
  ban.className = 'banner' + (view === 'reviewed' ? ' reviewed' : '');
}
function renderMap() {
  const view = V.map;
  setBanner('banner', view, view === 'cold' ? 'AI Output: no human corrections.' : 'Human Reviewed: every archetype call checked by a person.');
  document.getElementById('outkey').style.display = view === 'reviewed' ? '' : 'none';
  document.getElementById('top').innerHTML = axis() + D.top.map(charBlock).join('');
  document.getElementById('rest').innerHTML = axis() + D.rest.map(charBlock).join('');
  document.getElementById('table').innerHTML = table();
}
// --- section 4: archetype timeline -------------------------------------------
// Wide screens: pages run left to right, one row per lane. Narrow screens
// (the CSS phone breakpoint): pages run top to bottom, lanes side by side.
const TLEL = document.getElementById('tl');
const TL_NARROW = matchMedia('(max-width: 640px)');
const TL_PAGE_PX = 18;            // narrow layout: pixels per page
const TL_GAP = 11;                // marks closer than this (px) are set side by side
const TL_RUN_PAGES = 4;           // same-character marks this close in a lane share a label
const [TL_P0, TL_P1] = D.tlPages;
const TL_SPAN = TL_P1 + 1 - TL_P0;  // page N runs from N to N+1
const TL_TICKS = [TL_P0].concat([...Array(Math.floor(TL_P1 / 10)).keys()].map(i => (i + 1) * 10), TL_P1 % 10 ? [TL_P1] : []);
const tlCtx = document.createElement('canvas').getContext('2d');
function textW(s, font) { tlCtx.font = font; return tlCtx.measureText(s).width; }
// Greedy slots: each position takes the first slot whose last position is far enough back.
function slots(ps, gap) {
  const last = [];
  return ps.map(p => { let k = last.findIndex(l => p - l >= gap); if (k < 0) { k = last.length; last.push(p); } else last[k] = p; return k; });
}
function tlRuns(ms) {
  const runs = [];
  for (const m of ms) {
    const r = runs[runs.length - 1];
    if (r && r.c === m.c && m.x - r.ms[r.ms.length - 1].x <= TL_RUN_PAGES) r.ms.push(m);
    else runs.push({c: m.c, ms: [m]});
  }
  return runs;
}
function tlMarks(view) {
  return D.timeline[view].map(m => Object.assign({x: D.beats[m.b].x}, m)).sort((a, b) => a.x - b.x);
}
function tlMark(m, view, style) {
  const b = D.beats[m.b], gm = view === 'reviewed' && m.a === 'Great Mother', hollow = gm && m.pole !== 'dark';
  const lab = `${nm(m.c)}, ${m.a}${gm ? ', ' + (hollow ? T.tl_nopole : T.tl_dark) : ''}, ${pageText(b)}`;
  return `<button type="button" class="tlm${hollow ? ' hollow' : ''}" style="${style};--c:${SLOT[m.a]}" data-b="${m.b}" ` +
    `data-c="${esc(m.c)}" data-a="${esc(m.a)}" data-v="${view}" aria-label="${esc(lab)}" aria-haspopup="dialog" aria-expanded="false"></button>`;
}
function tlWide(view, ms) {
  const labW = 110, gap = 10, tw = Math.max(240, TLEL.clientWidth - labW - gap);
  const px = x => (x - TL_P0) / TL_SPAN * tw;
  const font = `600 11.5px ${getComputedStyle(TLEL).fontFamily}`;
  const grid = TL_TICKS.map(t => `<i class="tl-grid" style="left:${px(t).toFixed(1)}px"></i>`).join('');
  const axis = '<div class="tl-row" aria-hidden="true"><div></div><div class="tl-axis">' +
    TL_TICKS.map(t => `<span style="left:${px(t).toFixed(1)}px">${t === TL_P0 ? 'Page ' : ''}${t}</span>`).join('') + '</div></div>';
  let h = axis;
  for (const a of D.archetypes) {
    const lm = ms.filter(m => m.a === a), sl = slots(lm.map(m => px(m.x)), TL_GAP);
    const markH = 8 + Math.max(1, ...sl.map(k => k + 1)) * TL_GAP;
    let marks = lm.map((m, i) => tlMark(m, view, `left:${px(m.x).toFixed(1)}px;top:${9 + sl[i] * TL_GAP}px`)).join('');
    const rowEnd = [];
    let labs = '';
    for (const r of tlRuns(lm)) {
      const t = nm(r.c), w = textW(t, font);
      const left = Math.max(0, Math.min(px(r.ms[0].x) - 5, tw - w));
      let k = rowEnd.findIndex(e => left >= e + 8);
      if (k < 0) { k = rowEnd.length; rowEnd.push(0); }
      rowEnd[k] = left + w;
      labs += `<span class="tl-lab" aria-hidden="true" style="left:${left.toFixed(1)}px;top:${markH - 2 + k * 15}px">${esc(t)}</span>`;
    }
    const H = markH + rowEnd.length * 15 + 2;
    h += `<div class="tl-row"><div class="lab"><i class="key" style="background:${SLOT[a]}"></i>${esc(a)}</div>` +
      `<div class="tl-track" role="group" aria-label="${esc(a)}" style="height:${H}px">${grid}${marks}${labs}</div></div>`;
  }
  return h + axis;
}
function tlNarrow(view, ms) {
  const axW = 28, n = D.archetypes.length, cw = (TLEL.clientWidth - axW) / n;
  const py = x => (x - TL_P0) * TL_PAGE_PX, H = TL_SPAN * TL_PAGE_PX;
  const font = `600 10.5px ${getComputedStyle(TLEL).fontFamily}`;
  const cols = `${axW}px repeat(${n}, minmax(0, 1fr))`;
  let h = `<div class="tl-vhead" aria-hidden="true" style="grid-template-columns:${cols}"><div class="tl-vh ax"><span>Page</span></div>` +
    D.archetypes.map(a => `<div class="tl-vh"><span>${esc(a)}</span><i class="key" style="background:${SLOT[a]}"></i></div>`).join('') + '</div>';
  h += `<div class="tl-vbody" style="height:${H + 30}px">`;
  D.archetypes.forEach((a, i) => { h += `<div class="tl-vcol" style="left:${(axW + i * cw + 1).toFixed(1)}px;width:${(cw - 2).toFixed(1)}px"></div>`; });
  for (const t of TL_TICKS)
    h += `<i class="tl-vgrid" style="left:${axW}px;top:${py(t)}px"></i><span class="tl-vtick" aria-hidden="true" style="top:${py(t)}px;width:${axW - 5}px">${t}</span>`;
  D.archetypes.forEach((a, i) => {
    const lm = ms.filter(m => m.a === a), ps = lm.map(m => py(m.x)), sl = slots(ps, TL_GAP);
    const mid = axW + i * cw + cw / 2;
    // Side-by-side marks are centred on the lane, per group of overlapping marks.
    let g0 = 0;
    const width = lm.map(() => 1);
    for (let j = 1; j <= lm.length; j++) {
      if (j === lm.length || sl[j] === 0) {
        const w = Math.max(...sl.slice(g0, j)) + 1;
        for (let k = g0; k < j; k++) width[k] = w;
        g0 = j;
      }
    }
    h += `<div role="group" aria-label="${esc(a)}">` + lm.map((m, j) =>
      tlMark(m, view, `left:${(mid + (sl[j] - (width[j] - 1) / 2) * TL_GAP).toFixed(1)}px;top:${ps[j].toFixed(1)}px`)).join('') + '</div>';
    // Labels go below a run, else above it, else further down: never over a mark or another label.
    const busy = ps.map(p => [p - 7, p + 7]);
    const free = (t, b) => !busy.some(([u, v]) => t < v && b > u);
    for (const r of tlRuns(lm)) {
      const words = nm(r.c).split(' '), lines = [];
      for (const wd of words) {
        const cur = lines[lines.length - 1];
        if (cur !== undefined && textW(cur + ' ' + wd, font) <= cw - 4) lines[lines.length - 1] = cur + ' ' + wd;
        else lines.push(wd);
      }
      const lh = lines.length * 12, p0 = py(r.ms[0].x), p1 = py(r.ms[r.ms.length - 1].x);
      let top = p1 + 7;
      if (!free(top, top + lh)) {
        if (p0 - 7 - lh >= 0 && free(p0 - 7 - lh, p0 - 7)) top = p0 - 7 - lh;
        else while (!free(top, top + lh)) top = Math.max(...busy.filter(([u, v]) => top < v && top + lh > u).map(x => x[1])) + 1;
      }
      busy.push([top, top + lh]);
      h += `<span class="tl-vlab" aria-hidden="true" style="left:${(axW + i * cw + 1).toFixed(1)}px;width:${(cw - 2).toFixed(1)}px;top:${top.toFixed(1)}px">${lines.map(esc).join('<br>')}</span>`;
    }
  });
  return h + '</div>';
}
let tlWidth = 0;
function renderTimeline() {
  const view = V.tl;
  setBanner('banner-tl', view, view === 'cold' ? T.tl_banner_cold : T.tl_banner_reviewed);
  document.getElementById('tl-key').style.display = view === 'reviewed' ? '' : 'none';
  closePop();
  tlWidth = TLEL.clientWidth;
  TLEL.dataset.layout = TL_NARROW.matches ? 'narrow' : 'wide';
  TLEL.innerHTML = (TL_NARROW.matches ? tlNarrow : tlWide)(view, tlMarks(view));
}
let tlFrame = 0;
addEventListener('resize', () => {
  cancelAnimationFrame(tlFrame);
  tlFrame = requestAnimationFrame(() => {
    if (TLEL.clientWidth !== tlWidth || TLEL.dataset.layout !== (TL_NARROW.matches ? 'narrow' : 'wide')) renderTimeline();
  });
});

// Tap a mark: character, archetype, page, and a link to that moment in the map.
const pop = document.createElement('div');
pop.className = 'tl-pop'; pop.id = 'tl-pop'; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-labelledby', 'tl-pop-h');
document.body.appendChild(pop);
let popFrom = null;
function openPop(el) {
  closePop();
  const b = D.beats[el.dataset.b], name = nm(el.dataset.c);
  pop.innerHTML = `<div class="t1" id="tl-pop-h">${esc(name)} · ${esc(el.dataset.a)}</div><div class="t2">${pageText(b)}</div>` +
    `<a href="#map-h" class="tl-go">${esc(fill(T.tl_link, {name: name, map: D.mapSection}))}</a>`;
  pop.classList.add('open');
  const r = el.getBoundingClientRect(), w = pop.offsetWidth, hh = pop.offsetHeight;
  const x = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), innerWidth - w - 8);
  let y = r.bottom + 8; if (y + hh > innerHeight - 8) y = r.top - hh - 8;
  pop.style.left = x + 'px'; pop.style.top = Math.max(8, y) + 'px';
  popFrom = el; el.setAttribute('aria-expanded', 'true');
  pop.querySelector('a').focus({preventScroll: true});
}
function closePop(refocus) {
  if (!popFrom) return;
  pop.classList.remove('open');
  popFrom.setAttribute('aria-expanded', 'false');
  if (refocus && document.body.contains(popFrom)) popFrom.focus({preventScroll: true});
  popFrom = null;
}
pop.addEventListener('click', ev => {
  if (!ev.target.closest('a.tl-go') || !popFrom) return;
  ev.preventDefault();
  const {b, c, a, v} = popFrom.dataset;
  closePop();
  if (V.map !== v) { V.map = v; render('map'); }
  const el = [...document.querySelectorAll('.mk')].find(m => m.dataset.b === b && m.dataset.c === c && m.dataset.a === a && m.dataset.o === '0');
  if (!el) return;
  const d = el.closest('details'); if (d) d.open = true;
  el.scrollIntoView({block: 'center'});
  openSheet(el);
});
document.addEventListener('click', ev => {
  const t = ev.target.closest('.tlm');
  if (t) { t === popFrom ? closePop(true) : openPop(t); return; }
  if (popFrom && !ev.target.closest('#tl-pop')) closePop();
});
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && popFrom) closePop(true); });
document.addEventListener('scroll', () => { if (popFrom && !pop.contains(document.activeElement)) closePop(); }, true);

const RENDER = {
  s2: () => { setBanner('banner-s2', V.s2, T['banner_p2_' + V.s2]); renderLanding(); },
  s3: () => { setBanner('banner-s3', V.s3, T['banner_p2_' + V.s3]); renderWaver(); },
  map: renderMap,
  tl: renderTimeline,
};
function render(sec) {
  document.querySelectorAll(`.toggle[data-sec="${sec}"] button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === V[sec]));
  RENDER[sec]();
}

// --- hover: brief -----------------------------------------------------------
const tip = document.getElementById('tip');
// The AI's own read of the moment, labelled as such (as in the panel).
function oneLine(key, removed) {
  if (removed) return 'Removed in review. Click to see why.';
  const f = (D.ai[key] || {}).fields || {};
  const line = (f.audience_perceived && f.audience_perceived[0]) || f.embodies || '';
  return line ? 'The AI’s read: ' + line : '';
}
function showTip(el) {
  const b = D.beats[el.dataset.b], key = `${el.dataset.b}|${el.dataset.c}`;
  const line = oneLine(key, el.dataset.o === '1');
  tip.innerHTML = `<div class="t1">${esc(nm(el.dataset.c))} · ${esc(el.dataset.a)}</div><div class="t2">${pageText(b)}</div>` +
    (line ? `<div>${esc(line)}</div>` : '');
  tip.style.display = 'block';
  const r = el.getBoundingClientRect(), w = tip.offsetWidth, hh = tip.offsetHeight;
  const x = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), innerWidth - w - 8);
  let y = r.top - hh - 10; if (y < 8) y = r.bottom + 10;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
}
const hideTip = () => { tip.style.display = 'none'; };

// --- click: detail panel ----------------------------------------------------
const sheet = document.getElementById('sheet'), scrim = document.getElementById('scrim');
let opener = null;
const isOpen = () => sheet.classList.contains('open');
function list(v) { return Array.isArray(v) ? v.map(cap).join('; ') : cap(v || ''); }

function scriptHtml(b) {
  return b.blocks.map(x => x.pre !== undefined ? `<pre>${esc(x.pre)}</pre>` :
    x.cue ? `<p><span class="cue">${esc(x.cue)}</span>${esc(x.t)}</p>` :
    x.slug ? `<p class="slug">${esc(x.slug)}</p>` : `<p>${esc(x.t)}</p>`).join('');
}

function reasoningHtml(key, ch, arch) {
  const ai = D.ai[key];
  if (!ai) return `<p class="lead">The AI made no call for ${esc(ch)} in this beat, so there is no AI reasoning. This mark was added in review.</p>`;
  const made = ai.call.includes(arch);
  const f = ai.fields;
  const rows = [['How an audience would see it', f.audience_perceived], [`How ${ch} sees it`, f.self_perceived],
    ['What they feel', f.emotion], ['What they want', f.goal], ['The role they fill', f.embodies]];
  let dl = '';
  for (const [k, v] of rows) if (v && (!Array.isArray(v) || v.length)) dl += `<dt>${esc(k)}</dt><dd>${esc(list(v))}</dd>`;
  if (!dl) return `<p class="lead">The AI stored no reasoning for this call.</p>`;
  const lead = made ? 'The AI didn’t write out why it chose this archetype. This is what it recorded about the moment:'
    : ai.call.length ? `The AI marked this beat as ${ai.call.join(' and ')}, not ${arch}. This is what it recorded about the moment:`
    : 'The AI did not mark an archetype here. This is what it recorded about the moment:';
  return `<p class="lead">${esc(lead)}</p><dl data-ai="1">${dl}</dl>`;
}

function whereHtml(b) {
  return `<p class="where">${pageText(b)} · lines ${b.lines[0]}–${b.lines[1]} of the script text${b.approx ? ' (approximate)' : ''}</p>` +
    (b.dual ? `<p class="where">Part of this scene is written as two columns of dialogue, side by side. It is shown as printed.</p>` : '') +
    (b.garbled ? `<p class="where">The first lines of this scene came out of the PDF jumbled, with two columns run together. They are shown exactly as extracted.</p>` : '');
}
function showSheet(h, el) {
  sheet.innerHTML = h;
  opener = el;
  sheet.classList.add('open'); scrim.classList.add('open');
  sheet.scrollTop = 0;
  sheet.querySelector('.close').addEventListener('click', closeSheet);
  sheet.querySelector('.close').focus({preventScroll: true});
}
// Panel for a turning-point or flag chip (sections 2 and 3).
function openChip(el) {
  hideTip();
  const bid = el.dataset.b, c = el.dataset.c, kind = el.dataset.k;
  const b = D.beats[bid], info = D.p2info[el.dataset.v][`${kind}|${bid}|${c}`];
  let h = `<button type="button" class="close" aria-label="Close">×</button>` +
    `<h3 id="sheet-h">${esc(el.dataset.n)} · ${esc(info.label)}</h3>` +
    `<p class="gl">${esc(kind === 'turn' ? info.label + ': ' + info.gloss : info.gloss)}</p>` + whereHtml(b);
  if (info.note) h += `<h4><span class="chip-human">What changed in review</span></h4><p class="changed">${esc(info.note)}</p>`;
  h += `<h4>The scene</h4><div class="script" data-locked="Script text">${scriptHtml(b)}</div>`;
  h += `<details><summary>Under the hood</summary>` +
    `<p><b>Character cue in the script:</b> ${esc((D.cues[c] || [c]).join(', '))}</p>` +
    info.hood.map(([k, v]) => `<p><b>${esc(k)}:</b> ${esc(v)}</p>`).join('') +
    `<p>Lines ${b.lines[0]}–${b.lines[1]} of <code>fog_full.txt</code> (pdftotext -layout of the script PDF), copied by line range.</p></details>`;
  showSheet(h, el);
}

function openSheet(el) {
  hideTip();
  const bid = el.dataset.b, ch = el.dataset.c, arch = el.dataset.a, key = `${bid}|${ch}`;
  const view = el.dataset.v, name = nm(ch);
  const b = D.beats[bid], chg = D.changes[key];
  const removed = el.dataset.o === '1';
  let h = `<button type="button" class="close" aria-label="Close">×</button>` +
    `<h3 id="sheet-h">${esc(name)} · ${esc(arch)}${removed ? ' (removed in review)' : ''}</h3>` +
    `<p class="gl">${esc(arch)}: <span class="gtxt">${esc(D.gloss[arch])}</span>` +
    (D.defLinks ? ` <a class="deflink" href="#def-${arch.toLowerCase().replace(/ /g, '-')}">${esc(D.defLinkText)}</a>` : '') +
    `</p>` + whereHtml(b);
  if (view === 'reviewed' && chg) h += `<h4><span class="chip-human">What changed in review</span></h4><p class="changed">${esc(chg.line)}</p>`;
  h += `<h4>The scene</h4><div class="script" data-locked="Script text">${scriptHtml(b)}</div>`;
  h += `<h4><span class="chip-ai">How the AI read this moment</span></h4><div class="reason">${reasoningHtml(key, name, arch)}</div>`;
  h += `<details><summary>Under the hood</summary>` +
    `<p>Character cue in the script: ${esc((D.cues[ch] || [ch]).join(', '))}.</p>` +
    `<p>Beat ID <code>${esc(bid)}</code>. Lines ${b.lines[0]}–${b.lines[1]} of <code>fog_full.txt</code> (pdftotext -layout of the script PDF), copied by line range. Page-number header lines are left out; wrapped lines are joined.</p>` +
    `<p>The AI’s fields come from the uncorrected run (commit 7a6e69e): <code>audience_perceived</code>, <code>self_perceived</code>, <code>emotion</code>, <code>goal</code>, <code>embodies</code>. The tagging output has no field for a written rationale.</p>` +
    (chg ? `<p>AI call: ${esc(chg.was.join(' + ') || 'none')}. Reviewed call: ${esc(chg.now.join(' + ') || 'none')}. The plain line under “What changed in review” is Claude’s summary of the review notes below.</p>` +
      chg.logs.map(l => `<p>Corrections log #${l.n}: ${esc(l.note)}</p>`).join('') : '') +
    `</details>`;
  showSheet(h, el);
}
function closeSheet() {
  if (!isOpen()) return;
  sheet.classList.remove('open'); scrim.classList.remove('open');
  if (opener && document.body.contains(opener)) opener.focus({preventScroll: true});
  opener = null;
  hideTip();
}

document.addEventListener('pointerover', ev => {
  if (ev.pointerType !== 'mouse' || isOpen()) return;
  const t = ev.target.closest('.mk'); t ? showTip(t) : hideTip();
});
document.addEventListener('focusin', ev => {
  const t = ev.target.closest('.mk'); t && !isOpen() ? showTip(t) : hideTip();
});
document.addEventListener('scroll', hideTip, true);
document.addEventListener('click', ev => {
  if (ev.target.closest('#sheet a.deflink')) { closeSheet(); return; }
  const t = ev.target.closest('.mk, .mk-like, .chip');
  if (!t) return;
  t.dataset.k ? openChip(t) : openSheet(t);
});
scrim.addEventListener('click', closeSheet);
document.addEventListener('keydown', ev => {
  if (ev.key === 'Escape') { closeSheet(); hideTip(); }
  if (ev.key === 'Tab' && isOpen()) {
    const f = [...sheet.querySelectorAll('button, summary, [href]')];
    const first = f[0], last = f[f.length - 1];
    if (!sheet.contains(document.activeElement)) { ev.preventDefault(); first.focus(); }
    else if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
    else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
  }
});

document.querySelectorAll('.toggle button').forEach(b => b.addEventListener('click', () => {
  const sec = b.closest('.toggle').dataset.sec;
  V[sec] = b.dataset.v; closeSheet(); render(sec); }));
// Only the sections on this page (section 3 is off in the first public release).
['s2', 's3', 'map', 'tl'].filter(k => document.querySelector(`.toggle[data-sec="${k}"]`)).forEach(render);
// "#open=<beat>|<character>|<archetype>" opens that mark's panel (shareable link).
if (HASH.get('open')) {
  const [ob, oc, oa] = HASH.get('open').split('|');
  const el = [...document.querySelectorAll('.mk')].find(m => m.dataset.b === ob && m.dataset.c === oc && (!oa || m.dataset.a === oa));
  if (el) { const d = el.closest('details'); if (d) d.open = true; openSheet(el); }
}
"""


def hood_2_3(data, model, stats):
    bf = model["built_from"]
    s2c, s2r = stats["p2"]["cold"], stats["p2"]["reviewed"]
    res = "; ".join(f"{name} <code>{e(b)}</code>: {e(after)} (log {', '.join(f'#{n}' for n in ns) or 'none'})"
                    for b, name, after, ns in stats["p2"]["resolved"])
    po = stats["pass2_order"]
    landing = f"""<details class="more hood"><summary>Under the hood</summary>
<p><b>When the AI made these judgments.</b> {po["n"]} human corrections (corrections-log entries 1–{po["n"]}, commits <code>{e(po["first"])}</code> to <code>{e(po["before"])}</code>) were already in <code>fog_tagged.json</code> when the {po["drafts"]} Pass 2 drafts were applied (commits <code>{e(po["partial"])}</code>, partial, and <code>{e(po["complete"])}</code>, complete), so the AI Output view of this section rests on human-reviewed archetype calls.</p>
<p><b>Turning points.</b> “A change that’s justified” is <code>characterization_consistency = throughline_evolution</code>; “A limit revealed” is <code>boundary_revealed</code>. AI Output: {s2c["turns"]} from the Pass 2 drafts (<code>{e(bf["cold_pass2"])}</code>). Human Reviewed: {s2r["turns"]} from the current <code>fog_tagged.json</code>; each one is cross-checked against <code>fog_turning_points_reviewed.json</code> at build time. Of those, 7 were checked line by line by the author; the other 29 are marked “transcribed from author-confirmed review records” after an automated consistency check. Each panel’s own “Under the hood” shows the reviewed trait, shape, comparison beat and review record; comparison beats appear only there.</p>
<p><b>Reactions that hold together.</b> The total in “N of M” counts a character’s entries that carry a character-change judgment (<code>characterization_consistency</code> set, and not <code>requires_second_pass</code>). N counts those that are not <code>contradicted</code>, have <code>weight_proportionality = matched</code>, and are not <code>agency_alignment = displaced</code> (every FOG entry is <code>aligned</code> in both views). {stats["p2"]["no_value"]} reviewed entries carry no character-change judgment at all and are not counted. Still unresolved and not counted: {", ".join(e(x) for x in stats["p2"]["excluded_rsp"])}. The human review checked every entry the AI drafted as something other than <code>consistent</code> (138 drafts, plus 22 arc claims with no draft); entries drafted <code>consistent</code> and <code>matched</code> were not each re-read, so most of the “Human Reviewed” counts are the AI’s reads that review had no reason to revisit. <code>chain_soundness</code> is not stored on any FOG entry, so it is not used.</p>
<p><b>Roles carried across the script.</b> A character’s archetype appears here when it is called in {ROLE_MIN} or more beats in that view: the same calls as the character map (section {MAP_SECTION}). Tapping a page opens that map panel.</p>
<p>{e(model["labels"]["aliases"])}</p>
<p>All wording above the fold is fixed template text in <code>report.py</code> (<code>TEXT</code>, <code>TURN_LABEL</code>, <code>TURN_GLOSS</code>, <code>FLAG_TEXT</code>); the build rejects pipeline terms and grading words in it. No API call, no generated prose.</p>
</details>"""
    waver = f"""<details class="more hood"><summary>Under the hood</summary>
<p><b>What counts as a flag.</b> Any entry with <code>weight_proportionality = mismatch</code>, <code>characterization_consistency = contradicted</code>, or <code>agency_alignment = displaced</code>. AI Output: {stats["p2"]["cold"]["flags"]} flags, all <code>weight_proportionality = mismatch</code>. Human Reviewed: {stats["p2"]["reviewed"]["flags"]}.</p>
<p><b>Scope.</b> One flagged moment is “a moment”; two or more for the same character in one scene are “a sequence”; flags for one character in three or more scenes are “a character’s throughline”.</p>
<p><b>How review resolved the AI’s flags</b> (reviewed <code>weight_proportionality</code> and its corrections-log entries): {res}.</p>
<p><b>Author decision D1</b> (2026-10-04): the Human Reviewed view shows the empty result plainly, and no observations from review are added to this section. The AI Output label is <code>report_data.COLD_LABEL</code> with “Cold output” shown as “AI Output”.</p>
</details>"""
    return landing, waver


# Review mode (local only): the shared implementation in review_mode.py.
# This page keeps its original storage key, so edits already saved in the
# browser survive the move.
REVIEW_CSS = review_mode.CSS
REVIEW_STORE = "a-score-review-edits"
# One-line archetype summaries are edited through .gtxt, so the archetype
# name and the "Full definition" link around them stay out of the edit.
REVIEW_CAND = "h1, h2, h3, h4, p, li, th, dt, .sum, .gl2, .what2, .scope, .gtxt"
REVIEW_SKIP = ("details.hood, .script, button, #review-bar, .tip, summary, footer, .defs h3, a, #tl, .tl-pop, "
               ".lab, .char-head h3, .who, td, .head, #sheet h3")


def review_sources(data):
    """The source map for the review page's edit list: every framing string
    the page shows, named by its constant and report.py line."""
    entries = [(where, text, None) for where, text, cls in reader_strings(data) if cls != "ai_read"]
    entries += [("WHY_HEADING", WHY_HEADING, None), ("WHY_INTRO", WHY_INTRO, None)]
    entries += [(f"WHY_BULLETS[{i}]", a + b.format(map=MAP_SECTION), a) for i, (a, b) in enumerate(WHY_BULLETS)]
    entries += [(f"WHY_AFTER[{i}]", x.format(toggled=toggled_sections()), x) for i, x in enumerate(WHY_AFTER)]
    entries += [("NOT_MEASURED_LEAD", NOT_MEASURED_LEAD, None)] + [(f"NOT_MEASURED[{i}]", x, None) for i, x in enumerate(NOT_MEASURED)]
    entries += [(f"BIG_SEVEN_EXPLAINER[{i}]", x, None) for i, x in enumerate(BIG_SEVEN_EXPLAINER)]
    entries += [("DEFS_HEADING", DEFS_HEADING, None)] + [(f"DEFS_INTRO[{i}]", x, None) for i, x in enumerate(DEFS_INTRO)]
    entries += [("TL_HEADING", TL_HEADING.format(n=TIMELINE_SECTION), TL_HEADING)]
    entries += [(f"TL_INTRO[{i}]", x.format(map=MAP_SECTION), x) for i, x in enumerate(TL_INTRO)]
    entries += [(f"DEV_READ_TEXT[{k}]", v, v) for k, v in DEV_READ_TEXT.items()]
    return review_mode.source_map(entries, os.path.abspath(__file__))


def prompt_version_html(d):
    """Which prompt produced the text shown, kept apart from the current one."""
    import fog_dev_read_runner as runner
    v, now = d["generated_by_prompt_version"], runner.PROMPT_VERSION
    tail = (f"v{now} is the current prompt, for future runs." if now != v else "It is the current prompt.")
    return (f'<p><b>Prompt version.</b> The text shown was produced by prompt v{v} (archived verbatim: '
            f'<code>{e(d["generating_prompt_file"])}</code>). {tail}</p>')


def author_check_html(c):
    """The author's fact check, under the hood: a note, then each point,
    quoting the AI's words (which stay unchanged on the page)."""
    h = f'<p><b>Author check ({e(c["date"])}).</b> {e(c["note"])}</p>'
    if c.get("issues"):
        h += "<ul>" + "".join(f'<li>{e(x["field"].capitalize())}: “{e(x["text"])}”. {e(x["issue"])}</li>'
                              for x in c["issues"]) + "</ul>"
    if c.get("closing"):
        h += f'<p>{e(c["closing"])}</p>'
    return h


def dev_read_html(d):
    """Section 1, or "" before the billed run. No toggle: one AI version."""
    if not d:
        return ""
    t = DEV_READ_TEXT
    body = (f'<dl class="dr"><dt>Title <span class="muted">({e(t["title_note"])})</span></dt>'
            f'<dd class="dr-title" data-locked="Title from the title page">{e(d["title"])}</dd>')
    ai = ""
    if d.get("genre"):
        ai += f'<dt>Genre</dt><dd data-ai="1">{e(d["genre"])}</dd>'
    layered = d.get("prompt_version", 0) >= 5   # logline + collapsed full synopsis
    if layered and d.get("logline"):
        ai += f'<dt>Logline</dt><dd data-ai="1">{e(d["logline"])}</dd>'
    if d.get("synopsis") and not layered:
        ai += f'<dt>Synopsis</dt><dd data-ai="1">{e(d["synopsis"])}</dd>'
    if ai:
        body += f'</dl><p class="ai-label chip-ai">{e(t["label"])}</p><dl class="dr">{ai}'
    body += "</dl>"
    if d.get("synopsis") and layered:
        paras = "".join(f"<p>{e(p)}</p>" for p in d["synopsis"].split("\n\n") if p.strip())
        body += (f'<details class="dr-syn"><summary>{e(t["synopsis_summary"])}</summary>'
                 f'<div data-ai="1">{paras}</div></details>')
    if d["source"] == "fallback":
        parts = [DEV_READ_PART_NAMES[k] for k in d.get("missing", [])]
        body += f'<p class="note">{e(t["fallback"].format(parts=", ".join(parts)))}</p>'
    elif d["source"].startswith("fallback"):
        body += f'<p class="note">{e(t[d["source"]])}</p>'  # earlier versions: fallback_title_genre | fallback_title
    hood = (f'<details class="more hood"><summary>Under the hood</summary>'
            f'<p>Title: taken by code from the title page of <code>fog_full.txt</code> '
            f'(printed “{e(d["title_printed"])}”), not generated.</p>'
            f'<p>{"Genre, logline and synopsis" if layered else "Genre and synopsis"}: model <code>{e(d["model"])}</code>, '
            f'written in one call (prompt version {d.get("prompt_version", "1-3")}) from the script text only '
            f'({e(d["inputs"])}). Result: <code>{e(d["source"])}</code> after {d["attempts"]} call(s), '
            f'${d["total_cost_usd"]:.4f}. Raw responses and usage: <code>{e(d["call_file"])}</code>. '
            f'Checked by <code>report_guard.py</code> as report-voice summary text when written and again '
            f'when this page was built.</p>'
            + (prompt_version_html(d) if d.get("generated_by_prompt_version") is not None else "")
            + (f'<p>Accepted after a rule change, with no new API call: saved attempt {d["accepted_attempt"]}. '
               f'{e(d["accepted_note"])}</p>' if d.get("accepted_note") else "")
            + (f'<p><b>Formatting repair ({e(d["formatting_repair"]["date"])}).</b> '
               f'{e(d["formatting_repair"]["note"])} The AI’s original {e(d["formatting_repair"]["field"])} is '
               f'stored verbatim beside the repaired text in <code>fog_dev_read.json</code>, and the build checks '
               f'that the text shown is that original plus only this repair.</p>'
               if d.get("formatting_repair") else "")
            + (author_check_html(d["author_check"]) if d.get("author_check") else "")
            + '</details>')
    return (f'<section class="panel" aria-labelledby="read-h"><h2 id="read-h">Section 1. Development Read</h2>'
            f'{body}{hood}</section>')


def timeline_html(data, model, stats):
    """Section 4, the archetype timeline. The chart itself is drawn by JS
    (renderTimeline) from data["timeline"]; framing is TL_HEADING/TL_INTRO
    here and TL_TEXT in the page data."""
    ts = stats["timeline"]
    tl = data["timeline"]
    gm = ts["poles"]
    gm_slot = f"var(--s{ARCHETYPES.index('Great Mother') + 1})"
    dark = [p for p in gm if p["pole"] == "dark"]
    light = [p for p in gm if p["pole"] == "light"]
    ruled = [p for p in gm if p["source"] and p["source"].startswith("author ruling")]
    if light:
        sys.exit("ABORT: a light-pole Great Mother mark; section 4 has no key for it yet")
    ruled_txt = "; ".join(f'{e(display_name(p["c"]))} <code>{e(p["b"])}</code>, {e(p["source"])} in '
                          f'<code>{e(p["file"])}</code>' for p in ruled) or "none"
    pos = []
    for x in ts["approx"]:
        pg = x["pages"][0]
        pos.append(f'{e(display_name(x["c"]))}, <code>{e(x["b"])}</code> (page {pg}): the first lines of that '
                   f'moment came out of the PDF garbled (finding 12), so its first line is the first line of '
                   f'the garbled block (line {x["first"]}), {x["matched"] - x["first"]} lines before the first '
                   f'line that matches the stored text (line {x["matched"]}), on the same page')
    approx_p = (f'<p><b>{"One approximate position" if len(pos) == 1 else f"{len(pos)} approximate positions"}.'
                f'</b> {"; ".join(pos)}. Every other mark sits on a first line that matches the stored text.</p>'
                if pos else "<p>Every mark sits on a first line that matches the stored text.</p>")
    intro = "".join(f"<p>{e(x.format(map=MAP_SECTION))}</p>" for x in TL_INTRO)
    return f"""<section class="panel sec" aria-labelledby="tl-h">
<h2 id="tl-h">{e(TL_HEADING.format(n=TIMELINE_SECTION))}</h2>
<div class="intro">{intro}</div>
<div class="toggle" data-sec="tl" role="group" aria-label="Which version to show in this section">
<button type="button" data-v="cold" aria-pressed="true">AI Output</button>
<button type="button" data-v="reviewed" aria-pressed="false">Human Reviewed</button>
</div>
<p id="banner-tl" class="banner"></p>
<p id="tl-key" class="note"><i class="tl-dot" style="background:{gm_slot}"></i><i class="tl-dot hollow" style="border-color:{gm_slot}"></i>{e(TL_TEXT["tl_pole_key"])}</p>
<div id="tl" class="tl-chart"></div>
<details class="more hood"><summary>Under the hood</summary>
<p><b>Placement.</b> Each mark sits at its moment’s first line in <code>fog_full.txt</code> (the first line of the beat’s range in <code>fog_line_index.json</code>), on the script’s own printed page numbers, pages {TL_PAGES[0]}–{TL_PAGES[1]}. Printed page N runs from its first line to the first line of page N+1, so a mark’s place within a page follows that line. One mark is one archetype call for one character in one beat: the same calls as the character map (section {MAP_SECTION}), {len(tl["cold"])} in AI Output and {len(tl["reviewed"])} in Human Reviewed. A beat with two archetypes for one character has a mark in each lane. AI calls that review removed are not shown here. Marks closer together than their own size are set side by side, and nearby marks for the same character in one lane share one label. Wide screens run the pages left to right; narrow screens run them top to bottom, with the lanes side by side.</p>
<p><b>John and Young John.</b> {e(model["labels"]["aliases"])} Their marks carry one label, as everywhere else in the report.</p>
<p><b>Great Mother pole.</b> The tagging data has no field for the pole (<code>FUTURE_WORK.md</code> item 3), so it is not a stored value. The Human Reviewed view reads it from the review records: the verdict column of the beat’s row in that character’s archetype review table (<code>FOG_&lt;NAME&gt;_REVIEW.md</code>), plus any author ruling written on that row (“Author ruling (date): …”), which takes precedence over the verdict. A mark is filled when the dark pole is named: {len(dark)} of {len(gm)} Great Mother marks. The other {len(gm) - len(dark)} name no pole and are hollow; none names the light pole. From an author ruling rather than a verdict: {ruled_txt}. AI Output shows no pole: the AI’s output has no field for one.</p>
{approx_p}
<p>All wording above the fold is fixed template text in <code>report.py</code> (<code>TL_HEADING</code>, <code>TL_INTRO</code>, <code>TL_TEXT</code>); the build checks it like the rest of the page. No API call, no generated prose.</p>
</details>
</section>"""


def page(data, model, stats, review=False):
    hood_landing, hood_waver = hood_2_3(data, model, stats)
    # Section 3 (off in the first public release; see SHOW_CONSISTENCY_CHECK).
    section3 = f"""<section class="panel sec" aria-labelledby="waver-h">
<h2 id="waver-h">3. Consistency check: a second look</h2>
<div class="toggle" data-sec="s3" role="group" aria-label="Which version to show in this section">
<button type="button" data-v="cold" aria-pressed="true">AI Output</button>
<button type="button" data-v="reviewed" aria-pressed="false">Human Reviewed</button>
</div>
<p id="banner-s3" class="banner"></p>
<div id="waver"></div>
{hood_waver}
</section>
"""
    defs_on = review or SHOW_DEFINITIONS_APPENDIX
    legend = "".join(
        f'<span><i class="key" style="background:var(--s{i + 1})"></i><span><b>{e(a)}</b>: <span class="gtxt">{e(GLOSS[a])}</span>'
        + (f' <a class="deflink" href="#{def_id(a)}">{e(DEF_LINK_TEXT)}</a>' if defs_on else "")
        + '</span></span>'
        for i, a in enumerate(ARCHETYPES))
    legend += ('<span id="outkey"><i class="key out"></i><span><b>Outlined</b>: an AI call that '
               'review removed</span></span>')
    bf = model["built_from"]
    t = data["totals"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(model["script"])} Story Report</title>
<style>{numen_theme.css(ROOT)}{CSS}{REVIEW_CSS if review else ""}</style></head>
<body><main>
<h1>{e(model["script"])}: The Story Report</h1>
<p class="sub">How the story and characters hold together. It gives no grade.</p>

<section class="panel why" aria-labelledby="why-h">
<h2 id="why-h">{e(WHY_HEADING)}</h2>
<p>{e(WHY_INTRO)}</p>
<ul>{"".join(f"<li><b>{e(a)}</b>{e(b.format(map=MAP_SECTION))}</li>" for a, b in why_bullets())}</ul>
{"".join(f"<p>{e(x.format(toggled=toggled_sections()))}</p>" for x in WHY_AFTER)}
</section>
<p class="status">{f"Work in progress: all {['zero', 'one', 'two', 'three', 'four', 'five'][N_SECTIONS]} sections are built." if data["devread"] else f"Work in progress: sections 2 to {N_SECTIONS} are built. Section 1 is not built yet."}</p>

{dev_read_html(data["devread"])}

<section class="panel sec" aria-labelledby="landing-h">
<h2 id="landing-h">Section 2. Character Arcs: Where They Change, And Where They Don’t</h2>
<div class="toggle" data-sec="s2" role="group" aria-label="Which version to show in this section">
<button type="button" data-v="cold" aria-pressed="true">AI Output</button>
<button type="button" data-v="reviewed" aria-pressed="false">Human Reviewed</button>
</div>
<p id="banner-s2" class="banner"></p>
<div id="landing"></div>
{hood_landing}
</section>

{section3 if SHOW_CONSISTENCY_CHECK else ""}

<section class="panel" aria-labelledby="map-h">
<h2 id="map-h">{MAP_SECTION}. Character map: The Big Seven (Jungian Archetypes)</h2>
<div class="what">
<h3>What are The Big Seven?</h3>
{"".join(f"<p>{e(x)}</p>" for x in BIG_SEVEN_EXPLAINER)}
</div>
<div class="intro">
<p>Each row defines a character. Each colored mark along that row is a beat where the AI saw one of The Big Seven in that character. Marks run left to right through the script’s pages.</p>
<p>Only beats with a clear archetype are marked. Many moments in a script are ordinary behavior, and the AI leaves those unmarked.</p>
<p>Hover over a mark for quick summary info. Click or tap it to read the full scene and how the AI read it.</p>
</div>
<p class="legend-h">The Big Seven</p>
<div class="legend">{legend}</div>
<div class="toggle" data-sec="map" role="group" aria-label="Which version to show in this section">
<button type="button" data-v="cold" aria-pressed="true">AI Output</button>
<button type="button" data-v="reviewed" aria-pressed="false">Human Reviewed</button>
</div>
<p id="banner" class="banner"></p>
<p class="note">John and Young John are shown as one person, as are Cheyenne and Young Cheyenne.</p>
<div id="top"></div>
<details class="more"><summary>More characters ({len(data["rest"])})</summary><div id="rest"></div></details>
<details class="more"><summary>Table view</summary><div id="table" class="scroll"></div></details>
<details class="more hood"><summary>Under the hood</summary>
<p><b>AI Output</b> is the pipeline’s cold run on this script with no human correction. Every archetype call on this map comes from snapshot <code>{e(bf["cold_pass1"])}</code> (460/460 beats tagged, 0 corrections), so on this map the AI Output view is fully uncorrected. The report-wide label for this view also covers the later character-change judgments (Pass 2, <code>{e(bf["cold_pass2"])}</code>): {e(model["labels"]["cold"])}</p>
<p><b>Human Reviewed</b> is the current <code>fog_tagged.json</code> ({bf["corrections_log_entries"]} corrections-log entries). Every confident archetype call was reviewed; <code>no_confident_archetype</code> entries were reviewed only where a correction touched them.</p>
<p>Counts: {t["cold"]["calls"]} character entries carry an archetype call in AI Output and {t["reviewed"]["calls"]} in Human Reviewed (one entry can carry two archetypes). Between the two views 33 entries changed (32 changed, 1 added), matching the audit in <code>FOG_COLD_RUN_FINDINGS.md</code>; the 29 that involve an archetype appear on this map. The other 4 changed one non-tag to another.</p>
<p>Unmarked beats hold the honest non-tags <code>no_confident_archetype</code>, <code>ordinary_reaction</code> and <code>functional_role_only</code>. Only characters with at least one archetype call in either view are listed.</p>
<p>{e(model["labels"]["aliases"])} The pipeline also first named O’Shea “Driver” and “Hispanic” in three beats (finding 6); none of those carries an archetype.</p>
<p>“How the AI read this moment” in each panel shows the fields the AI stored for that character in that beat. The tagging output has no field for a written rationale, so none is shown and none is generated (logged in <code>FUTURE_WORK.md</code> item 2: add one before the next cold run). “What changed in review” lines are Claude’s plain summaries of the cited corrections-log entries; the full notes are in each panel’s own “Under the hood”.</p>
<p>Page numbers are printed page numbers. Line numbers refer to <code>fog_full.txt</code>; each beat’s range comes from <code>fog_line_index.json</code>.</p>
</details>
</section>

{timeline_html(data, model, stats)}

<section class="panel not-measured" aria-label="What this report doesn't measure">
<p><b>{e(NOT_MEASURED_LEAD)}</b> {e(" ".join(NOT_MEASURED))}</p>
</section>

{definitions_html() if defs_on else ""}

<footer>Built by report.py. No API call was made to build this page.</footer>
</main>
{"" if review else numen_theme.home_button(ROOT)}
<div id="tip" class="tip" role="tooltip"></div>
<div id="scrim" class="scrim"></div>
<div id="sheet" class="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-h"></div>
<script type="application/json" id="data">{json.dumps({**data, "defLinks": defs_on, "defLinkText": DEF_LINK_TEXT}, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{JS}</script>
{review_mode.bar("story report", REVIEW_STORE, REVIEW_CAND, REVIEW_SKIP, review_sources(data),
                  "not in the source map: search report.py for the original text") if review else ""}
</body></html>
"""


def model_word_check(label, html_out, strings):
    """Framing says "AI", never "model" (author, 2026-10-06): the page's
    visible text, Under the hood included, and every framing string in the
    page data (static templates, and Claude's plain change lines). Not
    checked: the AI's own text (its stored reads and the development read)
    and the author's verbatim review notes, which aren't framing. The one
    exception is the line naming the model ID ("model claude-sonnet-5")."""
    locked = [s for where, s, cls in strings if cls == "ai_read" or where.startswith("development read")]
    hits = report_guard.model_word_hits(report_guard.all_visible_text(html_out), locked)
    hits += [f"{where}: {s[:80]}" for where, s, cls in strings
             if (cls == "static" or where.startswith("CHANGE_LINES")) and report_guard.model_word_hits(s)]
    if hits:
        for h in hits:
            print("  MODEL", h)
        sys.exit(f"ABORT: \"model\" appears {len(hits)} time(s) in framing on the {label}; say \"AI\"")
    print(f"model check ({label}): framing says AI (model ID line excepted)")


def old_name_check(label, html_out):
    """The product is Numen: the old name must not appear in visible text."""
    hits = report_guard.old_name_hits(html_out)
    if hits:
        for h in hits:
            print("  OLD NAME", h)
        sys.exit(f"ABORT: the old name a-score appears {len(hits)} time(s) in the visible text of the {label}")
    print(f"name check ({label}): no a-score in visible text")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", action="store_true",
                    help="local build with Review mode, written to fog_story_report_review.html (git-ignored)")
    args = ap.parse_args()
    data, model, stats = build()
    html_out = page(data, model, stats)
    review_mode.assert_public(html_out, "Story Report")
    # Above the fold = the page minus scripts, data and "Under the hood" blocks.
    verbatim = verbatim_class(html_out)
    legacy_text = report_guard.visible_text(html_out)
    for t in (verbatim["label"] + verbatim["texts"]) if verbatim else []:
        legacy_text = legacy_text.replace(re.sub(r"\s+", " ", t).strip(), "\n")
    check_plain("static page text", legacy_text)
    for label in AI_READ_LABELS:
        if label not in html_out:
            sys.exit(f"ABORT: the AI's reads are exempt only while labelled; {label!r} is missing")
    strings = reader_strings(data)
    findings = report_guard.final_scan(html_out, strings, APPROVED_STATIC, verbatim=verbatim)
    if findings:
        for x in findings:
            print("  GUARD", x)
        sys.exit(f"ABORT: final scan found {len(findings)} findings (report_guard.py)")
    print(f"final scan: 0 findings ({len(strings)} data strings by class "
          f"{dict(Counter(c for _, _, c in strings))}, plus the static page text; "
          f"{len(APPROVED_STATIC)} approved static strings)")
    old_name_check("public page", html_out)
    model_word_check("public page", html_out, strings)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_out)
    if args.review:
        review_out = page(data, model, stats, review=True)
        review_mode.assert_review(review_out, "Story Report")
        old_name_check("review page", review_out)
        model_word_check("review page", review_out, strings)
        with open(REVIEW_OUT, "w", encoding="utf-8") as f:
            f.write(review_out)
        print(f"review build (local only, git-ignored): {os.path.basename(REVIEW_OUT)}")
    p = stats["p2"]
    for v in ("cold", "reviewed"):
        print(f"sections 2-3, {v}: {p[v]['turns']} turning points ({p[v]['turn_chars']} characters), "
              f"hold table {p[v]['hold_chars']} characters, roles {p[v]['roles']}, "
              f"flags {p[v]['flags']} in groups {p[v]['flag_groups']}")
    print(f"flags resolved in review: {p['resolved']}")
    print(f"not counted: {p['no_value']} without a judgment; unresolved {p['excluded_rsp']}")
    r = stats["reasoning"]
    print(f"calls: AI Output {data['totals']['cold']['calls']}, Human Reviewed {data['totals']['reviewed']['calls']}")
    print(f"archetype-involving changes: {stats['changed']} (each has a plain line and verified log citations)")
    print(f"marks (character x beat): {stats['shown_keys']}; beats with full text: {stats['beats_with_text']} "
          f"(every stored turn verified present)")
    print(f"reasoning: AI made the call {len(r['ai_made_call'])} "
          f"(with stored fields: {sum(h for _, h in r['ai_made_call'])}); "
          f"AI made no call but stored fields {len(r['ai_no_call_but_fields'])} {[k for k, _ in r['ai_no_call_but_fields']]}; "
          f"no AI entry {r['no_ai_entry']}")
    print("top:", stats["top"])
    print("more:", stats["rest"])
    print(f"wrote {os.path.basename(OUT)} ({os.path.getsize(OUT) // 1024} KB)")


if __name__ == "__main__":
    main()
