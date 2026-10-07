"""
walkthrough.py -- builds numen_walkthrough.html: one script, Full of Grace,
followed from the script PDF to its Story Report, stage by stage
(WALKTHROUGH_MAP.md). Phone-first, single scrolling page, in the Story
Report's design (report.CSS: same tokens, fonts, light and dark themes).

Deterministic: no API call, no generated prose.
- Every number on the page is computed from the data at build time
  (numbers()); the framing templates hold no digits, and the build stops if
  one does.
- Every excerpt is read from its file by code and checked word for word
  against that file again before the page is written (verify_excerpts()).
  Excerpts are a verbatim class for report_guard's final scan.
- Framing passes report.check_plain, report_guard (banned, praise and
  critique words, pipeline terms), the "model" check and the old-name
  check. The source PDF is "the script PDF", never its filename.

Run from the repo root:  python walkthrough.py
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report  # noqa: E402
import report_guard  # noqa: E402
import numen_theme  # noqa: E402
import review_mode  # noqa: E402

OUT = os.path.join(ROOT, "numen_walkthrough.html")
REVIEW_OUT = review_mode.review_path(OUT)   # local only, git-ignored
# Why each excerpt is locked in review mode (data-locked on its container).
LOCK = {"script": "Script text, printed from fog_full.txt",
        "parsed": "Pipeline output, from fog_parsed_scenes.json",
        "scaffold": "Pipeline output, from fog_scaffold.json",
        "ai": "The AI's text, from its saved response",
        "devread": "The AI's text, from the development read",
        "review": "Review record",
        "report": "Story Report text: edit it on the report's review page",
        "card": "Card title, from the card's own page"}
P = {k: os.path.join(ROOT, v) for k, v in {
    "full": "fog_full.txt", "parsed": "fog_parsed_scenes.json", "scaffold": "fog_scaffold.json",
    "calls": "fog_tagging_calls.jsonl", "syn_mackie": "fog_pass2_calls/synthesis_MACKIE.json",
    "devread": "fog_dev_read.json", "model": "fog_report_model.json", "index": "fog_line_index.json",
    "tpr": "fog_turning_points_reviewed.json", "tagged": "fog_tagged.json", "report_py": "report.py",
}.items()}
REPORT_HTML = "fog_story_report.html"
CARDS = ["holly_scene3_beat2_card.html", "mackie_scene140_beat6_card.html",
         "pete_scene122_beat1_card.html", "protected_protector_card.html"]

# The threads the excerpts follow (WALKTHROUGH_MAP.md b).
SCREAM_LINES = (192, 199)          # fog_full.txt: Beth's cut-off text, then the scream
SCREAM_SCENE = 7
PARSED_ELEMENTS = (3, 6)           # scene 7: Beth's cue, her line, her phone
HOLLY_LINES = (70, 87)             # scene 3: the apple, the head start, "Hey! Not fair!"
HOLLY_BEAT = "scene3_beat2"
MACKIE_LINES = (4484, 4485)        # scene 140: the grab
MACKIE_BEAT = "scene140_beat6"
MACKIE_TRAIT = 1                   # synthesis_MACKIE.json synthesis[1]
GARBLED_BEAT = "scene216_beat6"    # finding 12

# --- framing: every reader-facing line (approved by the author 2026-10-06; the author's
# review edits applied 2026-10-07) -----------------------------------------------------
# Templates only: {name} fields are filled from numbers(); no digit may be typed.
TAGLINE = "Numen: Archetype and Character-Arc Analysis for Screenplays"
OPENING = ("This walkthrough follows one feature-length script, Full of Grace, from the script’s PDF to its "
           "final Story Report.")
# No separate excerpt label line (author edit 2026-10-07): each excerpt's own caption
# is its label. The final scan exempts excerpts from the word checks only while
# every caption is on the page word for word (excerpt_labels()).
LBL = {"in": "WHAT GOES IN:", "out": "WHAT COMES OUT:", "does": "WHAT IT DOES:", "note": "WORTH KNOWING:"}
STAGES = [
    {"title": "The Script Read", "steps": [1, 2],
     "in": "The script PDF.",
     "out": "{scenes} scenes, with every line labelled as a scene heading, action, character name, "
            "dialogue or a direction.",
     "does": "The text is pulled out of the script PDF with its layout kept, split into scenes, and every "
             "line is labelled by what it is.",
     "note": "When two characters’ lines are printed side by side (dual dialogue), pulling the text from "
             "the PDF can scramble them. One of Trudy’s lines on page {garbled_page} lost her name and had "
             "words out of order; it was repaired by hand, checked against a second extraction."},
    {"title": "Finding the Moments", "steps": [3],
     "in": "The {scenes} labelled scenes.",
     "out": "{beats} moments, each holding its full text and the signals that marked where it begins and "
            "ends.",
     "does": "Each scene is split into moments wherever the text shifts — a pause, a line that stops short, "
             "a sharp swing in tone.",
     "note": "These signals read the words one at a time, not what they amount to. A tone measure built on "
             "them was tested as an emotional wave across the script and eventually left out: it read "
             "Holly’s scream as close to neutral."},
    {"title": "The AI Labels the Archetypes", "steps": [4],
     "in": "Each of the {beats} moments, one at a time, with its full text.",
     "out": "Each character in each moment gets one of The Big Seven, or no archetype. The AI also records "
            "how the audience sees the moment, how the character sees it, and what the character feels and "
            "wants. The run made {calls} AI calls.",
     "does": "The AI reads one moment at a time and says which of The Big Seven, if any, each character "
             "presents as; an answer outside the allowed terms is rejected and asked for again.",
     "note": "In one confrontation, the AI put John’s Hero call on the argument, not on the acts that "
             "follow. A Hero call needs the act itself, and review moved it."},
    {"title": "The AI Tracks Character Changes", "steps": [6],
     "in": "Every moment for each character with {min_beats} or more moments.",
     "out": "{drafts} judgments across {pass2_chars} characters: whether each reaction fits the moment and "
            "fits the character, and where a character changes or shows a limit we haven’t seen before.",
     "does": "The AI reads each character’s full arc first, names the traits that define them, then "
             "measures every moment against those traits.",
     "plain": "It never checks a moment on its own; it waits until the character’s whole arc is in view. "
              "Note that it worked from human-reviewed archetype calls: {pass2_before} corrections had "
              "already been made to the previous stage.",
     "note": "The AI tracks John and Young John as two people, so it can’t connect the two halves of one "
             "life. The report shows them as one person, but these judgments were made separately."},
    {"title": "The Story Report", "steps": [8, 9, 10],
     "in": "The script text, and everything the AI produced in the stages above.",
     "out": "The Story Report: {sections} sections, each tied to pages of the script.",
     "does": "The AI writes a genre, logline and synopsis from the script alone, code assembles the rest "
             "from the earlier stages, and a check rejects wording that passes judgment on the script.",
     "note": "One stray letter in the AI’s synopsis was removed and a lost paragraph break restored. The "
             "repair is logged, and no words were changed."},
]
CAP = {
    "scream": "Holly goes missing, as pulled from the script PDF (page {scream_page}).",
    "parsed": "Part of the same scene after labelling:",
    "beat_end": "The end of one moment, and the signals that closed it:",
    "beat_next": "The next moment opens:",
    "holly_script": "The script, page {holly_page}.",
    "holly_ai": "The AI’s call for Holly, from its saved response:",
    "mackie_script": "The script, page {mackie_page}.",
    "mackie_ai": "The AI on Mackie, from its saved response:",
    "devread": "The AI’s genre and logline, as the report shows them:",
}
ROW = {"action": "Action", "character_cue": "Character", "dialogue": "Dialogue", "parenthetical": "Direction",
       "slugline": "Scene heading", "character": "Character", "archetype": "Archetype",
       "audience": "How an audience would see it", "self": "How {name} sees it",
       "trait": "A trait the AI named", "turn": "Its label for this moment", "changes": "What it says changes",
       "genre": "Genre", "logline": "Logline"}
TRACK = {
    "chip": "Human review track",
    "title": "How the AI Is Measured",
    "lead": "The aim of the finished product is to be AI-only, with no human review. This track shows how "
            "close the AI currently gets: a person checked the AI’s work on the Full of Grace script, call "
            "by call.",
    "kept": "{kept} of the AI’s {ai_calls} archetype calls were kept as made.",
    "ordinary": "The AI never called a moment ordinary behavior; review did, {ordinary_reviewed} times.",
    "example": "One call review changed: Mackie, page {mackie_page}.",
    "ai_call": "The AI’s call", "review_call": "After review", "change": "What changed, in plain words",
    "turn": "Review’s reading of the turn",
    "cards": "{cards} moments, each shown the way review checks it:",
}
CLOSE = "Read the Story Report for Full of Grace"
HOOD = "Under the hood"


def framing_templates():
    out = [TAGLINE, OPENING, CLOSE, HOOD, *LBL.values(), *CAP.values(), *ROW.values(),
           *TRACK.values()]
    for s in STAGES:
        out += [s["title"]] + [s[k] for k in ("in", "out", "does", "plain", "note") if k in s]
    return out


# --- numbers --------------------------------------------------------------------

def load(k):
    with open(P[k], encoding="utf-8") as f:
        return json.load(f)


def kept_as_made(model):
    """The AI's archetype calls kept exactly in review: one entry per beat x
    character, entity renames matched (FOG_COLD_RUN_FINDINGS.md, "Cold Pass 1
    archetype accuracy"). Returns (kept, calls)."""
    rev = {(x["beat_id"], x["character"]): x for x in model["views"]["reviewed"]}
    ren = {(b, old): new for b, old, new in model["entity_renames"]}
    calls = [x for x in model["views"]["cold"] if x["archetypes"]]
    kept = 0
    for x in calls:
        r = rev.get((x["beat_id"], ren.get((x["beat_id"], x["character"]), x["character"])))
        kept += bool(r and set(r["archetypes"]) == set(x["archetypes"]))
    return kept, len(calls)


def numbers():
    """Every number the page shows, computed from the data."""
    with open(P["full"], encoding="utf-8") as f:
        lines = f.read().split("\n")
    pos, _ = report.page_positions(lines)
    index = load("index")["beats"]
    model = load("model")
    scaffold = load("scaffold")
    with open(P["calls"], encoding="utf-8") as f:
        calls = sum(1 for l in f if l.strip())
    kept, ai_calls = kept_as_made(model)
    po = report.pass2_order(model["built_from"]["cold_pass1"], model["built_from"]["cold_pass2"])
    import fog_pass2_runner
    scream = index[f"scene{SCREAM_SCENE}_beat3"]
    if scream["first_line"] != SCREAM_LINES[1] - 1:
        sys.exit("ABORT: the scream moment no longer starts where the excerpt does")
    n = {
        "printed_first": min(p for r in index.values() for p in r["printed_pages"]),
        "printed_last": max(p for r in index.values() for p in r["printed_pages"]),
        "lines": len(lines),
        "scenes": len(load("parsed")),
        "beats": len(scaffold["beats"]),
        "calls": calls,
        "kept": kept, "ai_calls": ai_calls,
        "ordinary_cold": sum(x["kind"] == "ordinary_reaction" for x in model["views"]["cold"]),
        "ordinary_reviewed": sum(x["kind"] == "ordinary_reaction" for x in model["views"]["reviewed"]),
        "pass2_before": po["n"], "drafts": po["drafts"],
        "pass2_chars": po["draft_chars"],
        "min_beats": fog_pass2_runner.MIN_BEATS,
        "sections": report.N_SECTIONS,
        "cards": len(CARDS),
        "scream_page": int(pos(SCREAM_LINES[0])), "scream_line": scream["first_line"],
        "scream_pdf": scream["pdf_pages"][0], "scream_printed": scream["printed_pages"][0],
        "holly_page": int(pos(HOLLY_LINES[0])), "mackie_page": int(pos(MACKIE_LINES[0])),
        "garbled_page": index[GARBLED_BEAT]["printed_pages"][0],
        "plot_facts": len(load("tagged")["plot_facts"]),
        "corrections": len(load("tagged")["corrections"]),
    }
    if n["ordinary_cold"]:
        sys.exit("ABORT: the AI's output now has ordinary_reaction calls; reword TRACK['ordinary']")
    if n["scream_page"] != n["scream_printed"]:
        sys.exit("ABORT: the scream excerpt and the scream moment are on different pages")
    return n, po, lines


# --- excerpts -----------------------------------------------------------------------
EXCERPTS = []   # (source key, text): every excerpt string the page shows


def ex(src, text):
    """Register an excerpt string and return it escaped."""
    if not isinstance(text, str) or not text.strip():
        sys.exit(f"ABORT: empty excerpt from {src}")
    EXCERPTS.append((src, text))
    return report.e(text)


def json_leaves(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from json_leaves(v)
    elif isinstance(x, list):
        for v in x:
            yield from json_leaves(v)
    elif isinstance(x, str):
        yield x
        if x.lstrip().startswith("{"):
            try:
                yield from json_leaves(json.loads(x))
            except ValueError:
                pass


def source_texts(src):
    """What an excerpt from `src` is checked against: the file's normalized
    text (text files), or every string value in it (JSON, JSON lines)."""
    path = P[src]
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith(".jsonl"):
        return "json", {s for l in raw.splitlines() if l.strip() for s in json_leaves(json.loads(l))}
    if path.endswith(".json"):
        return "json", set(json_leaves(json.loads(raw)))
    return "text", report.norm(raw)


def verify_excerpts(excerpts):
    """Every excerpt, word for word in its source file. Returns failures."""
    cache, bad = {}, []
    for src, text in excerpts:
        kind, got = cache.setdefault(src, source_texts(src))
        ok = (text in got) if kind == "json" else (report.norm(text) in got)
        if not ok:
            bad.append((src, text[:80]))
    return bad


def script_html(src_lines, a, z):
    """fog_full.txt lines a..z as script blocks (report.beat_text): cue and
    line kept as printed, wrapped lines joined."""
    h = ""
    for b in report.beat_text(src_lines, a, z, False):
        if "pre" in b:
            sys.exit(f"ABORT: lines {a}-{z} hold a two-column block; pick another excerpt")
        if b.get("cue"):
            h += f'<p><span class="cue">{ex("full", b["cue"])}</span>{ex("full", b["t"]) if b.get("t") else ""}</p>'
        elif b.get("slug"):
            h += f'<p class="slug">{ex("full", b["slug"])}</p>'
        else:
            h += f'<p>{ex("full", b["t"])}</p>'
    return f'<div class="script" data-locked="{LOCK["script"]}">{h}</div>'


def script_span(h):
    """Script text inside a label/value list: set in the script face."""
    return f'<span class="script-text">{h}</span>'


def rows(pairs, lock):
    """A label/value list of excerpts: every value is locked (`lock`, or a
    pair's own third item). A label given as (text, chip class) is shown as
    that chip (chip-ai for the AI, chip-human for human review)."""
    def dt(k):
        return f'<span class="{k[1]}">{report.e(k[0])}</span>' if isinstance(k, tuple) else report.e(k)
    return '<dl class="rows">' + "".join(
        f'<dt>{dt(p[0])}</dt><dd data-locked="{LOCK[p[2] if len(p) > 2 else lock]}">{p[1]}</dd>' for p in pairs) + "</dl>"


def excerpt_box(caption, body):
    return f'<figure class="ex"><figcaption>{report.e(caption)}</figcaption>{body}</figure>'


def stage_excerpts(N, lines):
    """The excerpts for each stage, read from the real files."""
    out = []
    # 1. Reading the script: the scream, then part of scene 7 as parsed.
    sc = next(s for s in load("parsed") if s["scene_id"] == SCREAM_SCENE)
    els = sc["elements"][PARSED_ELEMENTS[0]:PARSED_ELEMENTS[1]]
    out.append(excerpt_box(CAP["scream"].format(**N), script_html(lines, *SCREAM_LINES))
               + excerpt_box(CAP["parsed"], rows([(ROW["slugline"], script_span(ex("parsed", sc["slugline"])))]
                                                  + [(ROW[x["type"]], script_span(ex("parsed", x["text"]))) for x in els],
                                                  "parsed")))
    # 2. Finding the moments: the beat that closes on Beth's text, the one that opens on the scream.
    beats = load("scaffold")["beats"]
    b2, b3 = beats[f"scene{SCREAM_SCENE}_beat2"], beats[f"scene{SCREAM_SCENE}_beat3"]
    last = b2["source_evidence"]["turns"][-1]
    reasons = b2["source_evidence"]["evidence"]["closing_signal"]["reasons"]
    first = b3["source_evidence"]["turns"][0]
    out.append(excerpt_box(CAP["beat_end"],
                           f'<div class="script" data-locked="{LOCK["scaffold"]}"><p><span class="cue">{ex("scaffold", last["speaker"])}</span>'
                           f'{ex("scaffold", last["text"])}</p></div>'
                           + f'<ul class="sig" data-locked="{LOCK["scaffold"]}">' + "".join(f"<li>{ex('scaffold', r)}</li>" for r in reasons) + "</ul>")
               + excerpt_box(CAP["beat_next"], f'<div class="script" data-locked="{LOCK["scaffold"]}"><p>{ex("scaffold", first["text"])}</p></div>'))
    # 3. The AI calls the archetypes: Holly's head start, and the AI's saved response.
    with open(P["calls"], encoding="utf-8") as f:
        call = next(json.loads(l) for l in f if json.loads(l)["beat_id"] == HOLLY_BEAT)
    holly = next(c for c in json.loads(call["raw_text"])["per_character"] if c["character"] == "HOLLY")
    out.append(excerpt_box(CAP["holly_script"].format(**N), script_html(lines, *HOLLY_LINES))
               + excerpt_box(CAP["holly_ai"], rows([
                   (ROW["character"], ex("calls", holly["character"])),
                   (ROW["archetype"], ex("calls", holly["archetypes"][0])),
                   (ROW["audience"], ex("calls", holly["audience_perceived"][0])),
                   (ROW["self"].format(name="Holly"), ex("calls", holly["self_perceived"][0]))], "ai")))
    # 4. The AI traces how characters change: the grab, and Mackie's synthesis.
    syn = load("syn_mackie")
    tp = next(t for t in syn["turning_points"] if t["beat_id"] == MACKIE_BEAT)
    trait = syn["synthesis"][MACKIE_TRAIT]["trait"]
    if tp["trait_it_relates_to"] != trait:
        sys.exit("ABORT: Mackie's turning point no longer relates to the trait shown")
    out.append(excerpt_box(CAP["mackie_script"].format(**N), script_html(lines, *MACKIE_LINES))
               + excerpt_box(CAP["mackie_ai"], rows([
                   (ROW["trait"], ex("syn_mackie", trait)),
                   (ROW["turn"], ex("syn_mackie", tp["turning_point_type"])),
                   (ROW["changes"], ex("syn_mackie", tp["what_changes"]))], "ai")))
    # 5. The report is written: the development read.
    d = load("devread")
    out.append(excerpt_box(CAP["devread"], rows([(ROW["genre"], ex("devread", d["genre"])),
                                                 (ROW["logline"], ex("devread", d["logline"]))], "devread")))
    return out


def track_html(N):
    model = load("model")
    pick = {v: next(x for x in model["views"][v] if x["beat_id"] == MACKIE_BEAT and x["character"] == "MACKIE")
            for v in ("cold", "reviewed")}
    tpr = next(t for t in load("tpr")["turns"] if t["beat_id"] == MACKIE_BEAT and t["character"] == "MACKIE")
    change = report.CHANGE_LINES[f"{MACKIE_BEAT}|MACKIE"][0]
    cards = []
    for c in CARDS:
        path = os.path.join(ROOT, "demo_prototype", c)
        with open(path, encoding="utf-8") as f:
            title = html.unescape(re.search(r"<title>(.*?)</title>", f.read(), re.S).group(1))
        cards.append(f'<li><a href="demo_prototype/{c}" data-locked="{LOCK["card"]}">{report.e(title)}</a></li>')
    body = rows([
        ((TRACK["ai_call"], "chip-ai"), "<b>" + ex("model", pick["cold"]["archetypes"][0]) + "</b><br>"
         + ex("model", pick["cold"]["audience_perceived"][0]), "ai"),
        ((TRACK["review_call"], "chip-human"), "<b>" + ex("model", pick["reviewed"]["archetypes"][0]) + "</b><br>"
         + ex("model", pick["reviewed"]["audience_perceived"][0]), "review"),
        (TRACK["change"], ex("report_py", change), "report"),
        (TRACK["turn"], ex("tpr", tpr["reviewed"]["trait"]), "review"),
    ], "review")
    t = TRACK
    return (f'<section class="panel rtrack" aria-labelledby="track-h"><p class="chip-lab"><span class="chip-human">{report.e(t["chip"])}</span></p>'
            f'<h2 id="track-h">{report.e(t["title"])}</h2><p>{report.e(t["lead"])}</p>'
            f'<p class="figure">{report.e(t["kept"].format(**N))}</p><p>{report.e(t["ordinary"].format(**N))}</p>'
            + excerpt_box(t["example"].format(**N), body)
            + f'<p>{report.e(t["cards"].format(**N))}</p><ul class="cards">{"".join(cards)}</ul></section>')


# --- under the hood: the ten real steps ------------------------------------------------
PDF = "PDF"   # shown as "the script PDF"
STEPS = [
    ("Text extraction", ["pdftotext -layout"], [PDF], ["fog_full.txt"]),
    ("Parsing and hand patches", ["build_fog_scaffold.py", "parser.py", "fog_hand_patches.py"],
     ["fog_full.txt"], ["fog_parsed_scenes.json"]),
    ("Beat detection", ["build_fog_scaffold.py", "beat_detector.py", "signals.py", "suspense_signals.py"],
     ["fog_parsed_scenes.json"], ["fog_scaffold.json"]),
    ("Pass 1 tagging (AI)", ["fog_tagging_harness.py", "llm_orchestration.py", "integration.py", "tagging_schema.py"],
     ["fog_scaffold.json"], ["fog_tagged.json", "fog_tagging_calls.jsonl"]),
    ("Human archetype review", [], ["fog_tagged.json"], ["fog_tagged.json", "FOG_*_REVIEW.md"]),
    ("Pass 2 (AI)", ["fog_pass2_runner.py", "pass2_orchestration.py"], ["fog_tagged.json"],
     ["fog_pass2_calls/", "fog_tagged.json"]),
    ("Human Pass 2 review", ["build_fog_turning_points_reviewed.py"],
     ["fog_tagged.json", "fog_pass2_calls/", "FOG_*_REVIEW.md"],
     ["fog_tagged.json", "FOG_*_REVIEW.md", "FOG_PASS2_CLOSEOUT.md", "fog_turning_points_reviewed.json"]),
    ("Development read (AI)", ["fog_dev_read_runner.py", "report_guard.py"], ["fog_full.txt"],
     ["fog_dev_read.json", "fog_dev_read_call.json", "fog_dev_read_archive/"]),
    ("Report data", ["report_data.py"], ["fog_tagged.json", "fog_full.txt"],
     ["fog_line_index.json", "fog_report_model.json"]),
    ("Story Report", ["report.py", "report_guard.py"],
     ["fog_report_model.json", "fog_line_index.json", "fog_full.txt", "fog_tagged.json",
      "fog_turning_points_reviewed.json", "fog_dev_read.json", "FOG_*_REVIEW.md"], [REPORT_HTML]),
]


def file_list(items):
    out = []
    for x in items:
        if x == PDF:
            out.append("the script PDF")
            continue
        if not x.startswith("pdftotext") and not glob.glob(os.path.join(ROOT, x.rstrip("/"))):
            sys.exit(f"ABORT: under the hood names {x}, which doesn't exist")
        out.append(f"<code>{report.e(x)}</code>")
    return ", ".join(out) or "by hand"


def hood_html(N, po, model):
    stage_of = {st: i for i, s in enumerate(STAGES, 1) for st in s["steps"]}
    steps = ""
    for i, (name, run, ins, outs) in enumerate(STEPS, 1):
        where = f"stage {stage_of[i]}" if i in stage_of else "the human review track"
        steps += (f"<li><b>{report.e(name)}</b> ({where}). Run: {file_list(run)}. In: {file_list(ins)}. "
                  f"Out: {file_list(outs)}.</li>")
    return f"""<details class="more hood"><summary>{report.e(HOOD)}</summary>
<p><b>The {len(STEPS)} real steps.</b> The stages above group these; the human steps are the review track.</p>
<ol class="steps">{steps}</ol>
<p><b>When Pass 2 ran.</b> The first {po["n"]} corrections-log entries (commits <code>{po["first"]}</code> to <code>{po["before"]}</code>) are human corrections, all in <code>fog_tagged.json</code> before the {po["drafts"]} Pass 2 drafts were applied (<code>{po["partial"]}</code>, partial; <code>{po["complete"]}</code>, complete). The log now holds {N["corrections"]} entries.</p>
<p><b>A side step: plot facts.</b> After the cold run, <code>fog_plot_facts_runner.py</code> pulled {N["plot_facts"]} settled plot facts from the script into <code>fog_tagged.json</code>. They were not available to the AI when it called the archetypes, and nothing in the report uses them.</p>
<p><b>Page and line numbers.</b> The pipeline counts by PDF page (the title page first), by the script’s own printed page number ({N["printed_first"]}–{N["printed_last"]}), and by line in <code>fog_full.txt</code> ({N["lines"]} lines). Holly’s scream is line {N["scream_line"]}: PDF page {N["scream_pdf"]}, printed page {N["scream_printed"]}. This page and the report show printed pages only.</p>
<p><b>John and Young John.</b> {report.e(model["labels"]["aliases"])} This page shows them as one person, as the report does.</p>
<p><b>How this page is checked.</b> Every number is computed from the data when the page is built, every excerpt is checked word for word against its file, and the wording passes the report’s own checks. Built by <code>walkthrough.py</code>; no API call.</p>
</details>"""


CSS = r"""
main { max-width: 760px; }
.wt-head { margin: 8px 0 24px; }
.wt-head h1 { font-size: 24px; }
.wt-head p { margin: 8px 0 0; max-width: 60ch; color: var(--muted); }
.stage { position: relative; }
.stage .num { display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 50%;
  background: var(--ink); color: var(--panel); font-weight: 650; font-size: 14px; margin-right: 10px; flex: none; }
.stage h2 { display: flex; align-items: center; margin-bottom: 12px; }
.io { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 12px; }
.io > div { background: var(--lane); border-radius: 6px; padding: 9px 12px; }
.io h3, .does h3 { margin: 0 0 3px; font-family: var(--font-body); font-size: 12.5px; font-weight: 500; color: var(--muted);
  text-transform: uppercase; letter-spacing: .04em; }
.io p, .does p { margin: 0; font-size: 14px; }
.does { margin: 0 0 12px; }
.does p + p { margin-top: 8px; }
.plain { border-left: 4px solid var(--ink); padding-left: 10px; }
.ex { margin: 14px 0 0; }
.ex figcaption { font-size: 13px; color: var(--muted); margin: 0 0 6px; }
.ex .script { overflow-wrap: break-word; }
.rows { margin: 0; display: grid; gap: 8px; background: var(--lane); border-radius: 6px; padding: 10px 14px; }
.rows dt { font-size: 12.5px; color: var(--muted); font-weight: 600; }
.rows dd { margin: 0; overflow-wrap: break-word; }
.sig { list-style: none; padding: 0; margin: 8px 0 0; display: flex; flex-wrap: wrap; gap: 6px; }
.sig li { font-size: 12.5px; border: 1px solid var(--rule); background: var(--panel); border-radius: 999px; padding: 2px 9px; }
.wnote { margin: 14px 0 0; font-size: 14px; border-left: 4px solid var(--claim); background: var(--lane);
  border-radius: 6px; padding: 9px 12px; }
.wnote b { display: block; font-size: 12.5px; color: var(--muted); }
.connector { width: 2px; height: 22px; background: var(--rule); margin: 0 auto; }
.panel + .connector { margin-top: 0; }
.connector + .panel { margin-top: 0; }
.rtrack { margin-top: 36px; border: 2px dashed var(--human-rule); box-shadow: none; }
.chip-lab { margin: 0 0 8px; }
.rtrack > p { max-width: 64ch; }
.rtrack .figure { font-size: 18px; font-weight: 650; }
.cards { margin: 6px 0 0; padding-left: 20px; }
.cards li { margin: 0 0 6px; }
a { color: var(--ink); text-underline-offset: 2px; }
.close-link { margin: 28px 0 0; font-size: 16px; font-weight: 650; }
.steps { padding-left: 20px; }
.hoodwrap details.more { margin-top: 0; border-top: 0; padding-top: 0; }
.steps li { margin: 0 0 8px; overflow-wrap: anywhere; }
@media (max-width: 640px) {
  .io { grid-template-columns: 1fr; }
  .panel { padding: 16px 14px 18px; }
}
"""


def page(N, po, lines, review=False):
    model = load("model")
    exs = stage_excerpts(N, lines)
    stages = ""
    for i, (s, exh) in enumerate(zip(STAGES, exs), 1):
        plain = f'<p class="plain">{report.e(s["plain"].format(**N))}</p>' if "plain" in s else ""
        stages += (f'{"<div class=\"connector\" aria-hidden=\"true\"></div>" if i > 1 else ""}'
                   f'<section class="panel stage" aria-labelledby="st{i}-h">'
                   f'<h2 id="st{i}-h"><span class="num" aria-hidden="true">{i}</span><span class="ttl">{report.e(s["title"])}</span></h2>'
                   f'<div class="io"><div><h3>{report.e(LBL["in"])}</h3><p>{report.e(s["in"].format(**N))}</p></div>'
                   f'<div><h3>{report.e(LBL["out"])}</h3><p>{report.e(s["out"].format(**N))}</p></div></div>'
                   f'<div class="does"><h3>{report.e(LBL["does"])}</h3><p>{report.e(s["does"].format(**N))}</p>{plain}</div>'
                   f'{exh}'
                   f'<p class="wnote"><b>{report.e(LBL["note"])}</b>{report.e(s["note"].format(**N))}</p></section>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numen Walkthrough</title>
<style>{numen_theme.css(ROOT)}{report.CSS}{CSS}{review_mode.CSS if review else ""}</style></head>
<body><main>
<header class="wt-head"><h1>{wordmark_h1()}</h1><p>{report.e(OPENING)}</p></header>
{stages}
{track_html(N)}
<p class="close-link"><a href="{REPORT_HTML}">{report.e(CLOSE)}</a></p>
<section class="panel hoodwrap" aria-label="{report.e(HOOD)}" style="margin-top:24px">
{hood_html(N, po, model)}
</section>
<footer>Built by walkthrough.py. No API call was made to build this page.</footer>
</main>
{review_bar(N) if review else ""}
</body></html>
"""


# Review mode (local only): the shared implementation in review_mode.py.
REVIEW_STORE = "numen-review-edits:walkthrough"
REVIEW_CAND = "h1, .ttl, #track-h, h3, p, li, dt, figcaption"
REVIEW_SKIP = "button, #review-bar, .num, .script, footer, summary"


def review_bar(N):
    """The review bar for this page, with every framing line mapped to its
    constant and walkthrough.py line."""
    entries = [("TAGLINE", TAGLINE, None), ("OPENING", OPENING, None),
               ("CLOSE", CLOSE, None), ("HOOD", HOOD, None)]
    for name, d in (("LBL", LBL), ("CAP", CAP), ("ROW", ROW), ("TRACK", TRACK)):
        entries += [(f"{name}[{k!r}]", v.format(**N, name="Holly"), v) for k, v in d.items()]
    for i, st in enumerate(STAGES):
        entries += [(f"STAGES[{i}][{k!r}]", st[k].format(**N), st[k])
                    for k in ("title", "in", "out", "does", "plain", "note") if k in st]
    return review_mode.bar("walkthrough", REVIEW_STORE, REVIEW_CAND, REVIEW_SKIP,
                           review_mode.source_map(entries, os.path.abspath(__file__)),
                           "not in the source map: search walkthrough.py for the original text")


def wordmark_h1():
    """The tagline, with "Numen" set as the wordmark (same words, same order)."""
    name, rest = TAGLINE.split(":", 1)
    if name != "Numen":
        sys.exit("ABORT: the tagline no longer starts with the Numen wordmark")
    return f'<span class="wordmark">{report.e(name)}</span>:{report.e(rest)}'


def excerpt_labels(N):
    """The excerpt captions, as shown: the label of the verbatim class. The
    final scan exempts excerpts from the word checks only while every one
    of these is on the page word for word."""
    return [c.format(**N) for c in CAP.values()] + [TRACK["example"].format(**N)]


def framing_lines(N):
    """Every framing line as shown (templates filled)."""
    return [t.format(**N, name="Holly") for t in framing_templates()]


def check(html_out, N):
    """The build's checks; returns a list of problems (empty = pass)."""
    bad = []
    for t in framing_templates():
        if re.search(r"\d", re.sub(r"\{\w+\}", "", t)):
            bad.append(f"typed digit in framing: {t!r}")
    for s in framing_lines(N):
        for pat in report.FORBIDDEN + report.GRADING:
            if re.search(pat, s, re.I):
                bad.append(f"report word check {pat!r}: {s!r}")
        bad += [f"guard: {v} in {s!r}" for v in report_guard.check_text(s, "text", evaluation=True)
                if v.check in ("banned", "pipeline")]
        bad += [f"model: {s!r}" for _ in report_guard.model_word_hits(s)]
    bad += [f"excerpt not in {src}: {t!r}" for src, t in verify_excerpts(EXCERPTS)]
    texts = sorted({t for _, t in EXCERPTS}, key=len, reverse=True)
    findings = report_guard.final_scan(html_out, [], (), verbatim={"label": excerpt_labels(N), "texts": texts})
    bad += [f"final scan: {x}" for x in findings]
    bad += [f"model word: {h}" for h in report_guard.model_word_hits(report_guard.all_visible_text(html_out), texts)]
    bad += [f"old name: {h}" for h in report_guard.old_name_hits(html_out)]
    if "95.1" in html_out:
        bad.append("the 95.1% figure is on the page")
    if re.search(r"Full of Grace - |\.pdf", report_guard.all_visible_text(html_out)):
        bad.append("the script PDF is named by its filename")
    return bad


def build():
    EXCERPTS.clear()
    N, po, lines = numbers()
    html_out = page(N, po, lines)
    return html_out, N


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", action="store_true",
                    help="also write the local review page, numen_walkthrough_review.html (git-ignored)")
    args = ap.parse_args()
    html_out, N = build()
    review_mode.assert_public(html_out, "walkthrough")
    bad = check(html_out, N)
    if bad:
        for b in bad:
            print("  ", b)
        sys.exit(f"ABORT: {len(bad)} problem(s); page not written")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"checks: {len(EXCERPTS)} excerpts verified word for word; {len(framing_lines(N))} framing lines pass "
          "report.check_plain, report_guard, the model check and the old-name check; final scan 0 findings")
    print("numbers:", N)
    print(f"wrote {os.path.basename(OUT)} ({os.path.getsize(OUT) // 1024} KB)")
    if args.review:
        rv = build_review()
        with open(REVIEW_OUT, "w", encoding="utf-8") as f:
            f.write(rv)
        print(f"review build (local only, git-ignored): {os.path.basename(REVIEW_OUT)}")


def build_review():
    """The review page, with the old-name and model checks the public page gets."""
    EXCERPTS.clear()
    N, po, lines = numbers()
    rv = page(N, po, lines, review=True)
    review_mode.assert_review(rv, "walkthrough")
    texts = [t for _, t in EXCERPTS]
    bad = [f"old name: {h}" for h in report_guard.old_name_hits(rv)]
    bad += [f"model word: {h}" for h in report_guard.model_word_hits(report_guard.all_visible_text(rv), texts)]
    if bad:
        raise SystemExit("ABORT: review page: " + "; ".join(bad))
    return rv


if __name__ == "__main__":
    main()
