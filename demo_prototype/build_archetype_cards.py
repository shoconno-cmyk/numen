"""
Build the four demo cards from the Full of Grace review:

  1. mackie_scene140_beat6_card.html  MACKIE scene140_beat6: the AI's
     Great Mother, overturned to Shadow in review.
  2. holly_scene3_beat2_card.html     HOLLY scene3_beat2: Trickster, upheld
     unchanged.
  3. protected_protector_card.html    "The protected becomes the protector":
     MACKIE scene75_beat3 and YOUNG JOHN scene75_beat5 (then), JOHN
     scene217_beat1 (now).
  4. pete_scene122_beat1_card.html    PETE scene122_beat1, a turning-point
     card: the AI's stored Pass 2 claim (a limit revealed), overturned to
     character-consistent.

Sources, all read at build time:
- The AI's read: fog_tagged.json at the cold-run commit (7a6e69e),
  checked against the corrections log's llm_value where a field changed.
- Human review: the current fog_tagged.json (reviewed values) and the
  character's FOG_*_REVIEW.md archetype row (verdict and note, verbatim).
- Script text: rendered PDF pages, every highlighted line matched to
  fog_full.txt first (card_kit.locate). Every quotation in a review note is
  checked word for word against fog_full.txt.

The AI gave no written argument for any archetype: its output has only
the stored fields shown as "The AI's read". Reader-facing text says "AI",
never "model"; code names keep "model".

Run from the repo root:  python demo_prototype/build_archetype_cards.py
"""
import ast
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import card_kit as K  # noqa: E402
from card_kit import e  # noqa: E402

sys.path.insert(0, K.ROOT)
from tagging_schema import BIG_SEVEN_DEFINITIONS  # noqa: E402
import report  # noqa: E402
import review_mode  # noqa: E402
import git_snapshots  # noqa: E402

COLD_COMMIT = "7a6e69e"   # the Full of Grace cold run (report_data.COLD_PASS1_COMMIT)
FIELDS = [("self_perceived", "Self-perceived"), ("audience_perceived", "Audience-perceived"),
          ("emotion", "Emotion"), ("goal", "Goal")]
REVIEW_FILES = {"MACKIE": "FOG_MACKIE_REVIEW.md", "HOLLY": "FOG_HOLLY_REVIEW.md",
                "YOUNG JOHN": "FOG_YOUNGJOHN_REVIEW.md", "JOHN": "FOG_JOHN_REVIEW.md"}

cold = git_snapshots.show_json(COLD_COMMIT, "fog_tagged.json")
now = json.load(open(os.path.join(K.ROOT, "fog_tagged.json"), encoding="utf-8"))
model = json.load(open(os.path.join(K.ROOT, "fog_report_model.json"), encoding="utf-8"))


def logged(v):
    """Corrections-log values are sometimes stored as the repr of a list."""
    if isinstance(v, str) and v.startswith("["):
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
    return v


def entry(tagged, beat_id, character):
    b = next(x for x in tagged["beats"].values() if x["beat_id"] == beat_id)
    return next(c for c in b["per_character"] if c["character"] == character)


def review_row(character, beat_id):
    """The archetype-review row for this beat in the character's review
    record (the part before the Pass 2 review): (verdict, note), verbatim."""
    text = open(os.path.join(K.ROOT, REVIEW_FILES[character]), encoding="utf-8").read()
    rows = [l for l in re.split(r"\n## Pass 2", text)[0].split("\n") if l.startswith(f"| {beat_id} |")]
    if len(rows) != 1:
        sys.exit(f"ABORT: {len(rows)} archetype rows for {beat_id} in {REVIEW_FILES[character]}")
    cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    return cells[1], cells[2]


def moment(beat_id, character):
    """Everything a card shows for one character on one beat, from the records."""
    a, r = entry(cold, beat_id, character), entry(now, beat_id, character)
    for arch in a["archetypes"] + r["archetypes"]:
        assert arch in BIG_SEVEN_DEFINITIONS, arch      # names as in the Big Seven definitions
    changed = [k for k, _ in FIELDS if a[k] != r[k]]
    log = [(i + 1, c) for i, c in enumerate(now["corrections"])
           if c["beat_id"] == beat_id and c["character"] == character]
    # A changed field must be logged, with the cold value as the model's value.
    for k in changed + (["archetypes"] if a["archetypes"] != r["archetypes"] else []):
        hit = [(n, c) for n, c in log if c["field_name"] == k]
        if not hit or logged(hit[0][1]["llm_value"]) != a[k] or logged(hit[-1][1]["human_value"]) != r[k]:
            sys.exit(f"ABORT: {beat_id} {character} {k}: corrections log does not match the cold/reviewed values")
    verdict, note = review_row(character, beat_id)
    K.verify_note_quotes(f"{beat_id} {character}", note)
    shown, internal = K.split_note(note)
    rng = model["beats"][beat_id]
    assert rng["printed_pages"] == [p - 1 for p in rng["pdf_pages"]], rng
    return {"beat": beat_id, "character": character, "model": a, "review": r, "changed": changed,
            "verdict": verdict, "note": shown, "note_internal": internal, "dark": "dark pole" in verdict,
            "log": [n for n, _ in log], "lines": (rng["first_line"], rng["last_line"]),
            "pdf_pages": rng["pdf_pages"]}


def name(c):
    return c.title()   # MACKIE -> Mackie, YOUNG JOHN -> Young John


def joined(v):
    return "; ".join(v) if isinstance(v, list) else v


# Elements marked data-verbatim hold locked AI text or the author's verbatim
# review text; the framing checks on the built card skip them.
V = ' data-verbatim="1"'


def ai_side(m):
    a = m["model"]
    rows = "".join(f"<dt>{label}</dt><dd{V}>{e(joined(a[k]))}</dd>" for k, label in FIELDS)
    return f'''<section class="claim">
  <h2><span class="chip-ai">{e(H_AI)}</span></h2>
  <div class="value">{e(" + ".join(a["archetypes"]))}</div>
  <dl class="fields">{rows}</dl>
</section>'''


def review_side(m, badge, basis=None, author_note=None):
    r = m["review"]
    fixed = ("".join(f"<dt>{label}</dt><dd>{e(joined(r[k]))}</dd>" for k, label in FIELDS if k in m["changed"]))
    corrected = (f'<p class="basis">{e(L_CORRECTED)}</p><dl class="fields">{fixed}</dl>' if fixed else "")
    basis_html = ""
    if basis:
        label, b_note = basis
        basis_html = f'<p class="basis">{e(label)}</p><p class="note"{V}>{e(b_note)}</p>'
    author_html = ""
    if author_note:
        label, text = author_note
        author_html = (f'<p class="basis author-label">{e(label)}</p>'
                       f'<p class="note author-note" data-locked="Author\'s note, verbatim">{e(text)}</p>')
    return f'''<section class="verdict">
  <h2><span class="chip-human">{e(H_REVIEW)}</span></h2>
  <div class="value">{e(" + ".join(r["archetypes"]))}</div>
  <dl class="fields"><dt>{e(L_VERDICT)}</dt><dd{V}>{e(m["verdict"])}</dd></dl>
  <p class="note"{V}>{e(" ".join(m["note"]))}</p>
  {basis_html}
  {author_html}
  {corrected}
</section>
<div class="badge{" changed" if m["model"]["archetypes"] != r["archetypes"] else ""}">{e(badge)}</div>'''


def hood_block(parts, small):
    return f'''<details>
<summary>Under the hood</summary>
<div class="hood">
{"".join(parts)}
<p class="small">{e(small)} Script text: fog_full.txt (pdftotext -layout).</p>
</div>
</details>'''


def hood(moments, extra=""):
    parts = []
    for m in moments:
        rest = (f'<p><b>{e(L_REST)} ({e(name(m["character"]))}).</b> <span{V}>{e(" ".join(m["note_internal"]))}</span></p>'
                if m["note_internal"] else "")
        parts.append(f'''<p><b>{e(name(m["character"]))}, {e(m["beat"])}.</b> fog_full.txt lines {m["lines"][0]}–{m["lines"][1]}.
The AI's read comes from fog_tagged.json at the cold-run commit {COLD_COMMIT}; the human review from the current
fog_tagged.json and {e(REVIEW_FILES[m["character"]])} (archetype review row, verbatim). Corrections log entries
naming this character on this beat: {", ".join(f"#{n}" for n in m["log"]) or "none"}.</p>{rest}''')
    return hood_block(parts + [extra], SMALL_ARCH)


def legend(items):
    return '<div class="legend">' + "".join(
        f'<span><span class="sw" style="background:var(--{k})"></span>{e(t)}</span>' for k, t in items) + "</div>"


FRAMING = []   # (where, text): every framing line written for these cards


def f(where, text):
    FRAMING.append((where, text))
    return text


REVIEW = "--review" in sys.argv[1:]   # also write each card's local review page
PAGES = []    # (file name, title, body, required labels), for the review pages


def write(fname, title, body, required):
    path = os.path.join(K.OUT_DIR, fname)
    page = K.page_shell(title, body)
    review_mode.assert_public(page, fname)
    PAGES.append((fname, title, body, required))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote", path, f"({os.path.getsize(path) // 1024} KB)")
    return path, required


# Shared labels (framing).
H_AI = f("section heading", "The AI's read")
H_REVIEW = f("section heading", "Human review")
L_VERDICT = f("field label", "Verdict")
L_CORRECTED = f("label", "Corrected fields:")
L_REST = f("label", "Rest of the review note")
L_MOMENT = f("legend", "Highlighted: the moment")
L_CONTEXT = f("legend", "Grey: lead-in lines, shown for context and not part of the moment")
SMALL_ARCH = f("hood", "The AI gave no written argument for its archetype; the card shows the fields it stored. "
                       "Highlighted lines are matched word for word against the script text before they are drawn, "
                       "and every quotation in a review note is checked against the same file when the card is built.")

CARD1, CARD2, CARD3, CARD4 = ("mackie_scene140_beat6_card.html", "holly_scene3_beat2_card.html",
                              "protected_protector_card.html", "pete_scene122_beat1_card.html")
T1 = f("card 1 title", "Mackie: Great Mother or Shadow Archetype?")
T2 = f("card 2 title", "Holly: Trickster Archetype")
T3 = f("card 3 title", "The Protected Becomes the Protector")

built = []

# --- card 1: MACKIE scene140_beat6 ----------------------------------------------
m1 = moment("scene140_beat6", "MACKIE")
assert (m1["model"]["archetypes"], m1["review"]["archetypes"]) == (["Great Mother"], ["Shadow"])
assert m1["changed"] == ["self_perceived", "audience_perceived", "emotion", "goal"]
print("card 1")
pages1 = K.render_pages(m1["pdf_pages"], [("context", 4470, 4471), ("beat", *m1["lines"])])
S1 = f("card 1 sentence", "The AI read Mackie in this moment as Great Mother; the human review changed the "
                          "call to Shadow and rewrote the AI's read.")
B1 = f("card 1 badge", "Overturned: Great Mother to Shadow, with the read rewritten.")
LINK1 = f("card 1 link", "Mackie also appears in the card The protected becomes the protector.")
# Author's note, added 2026-10-06 (author text: a framing line, guard-checked).
AUTHOR1 = (f("card 1 author's note label", "Author's note (Oct 6, 2026)"),
           f("card 1 author's note", "This moment could also be read as Great Mother, dark pole. "
                                     "I judged Shadow the better fit."))
body1 = f'''<header class="top"><h1>{e(T1)}</h1><p>{e(S1)}</p></header>
<main class="card">
  <div class="pages">{K.pages_html(pages1, "c1")}</div>
  <aside>
    <p class="who">{e(name(m1["character"]))}</p>
    {legend([("beat", L_MOMENT), ("context", L_CONTEXT)])}
    {ai_side(m1)}
    {review_side(m1, B1, author_note=AUTHOR1)}
    {hood([m1], "<p>Lead-in: fog_full.txt lines 4470–4471, the end of the moment before.</p>")}
  </aside>
  <p class="link"><a href="{CARD3}">{e(LINK1)}</a></p>
</main>'''
built.append(write(CARD1, T1, body1, [H_AI, H_REVIEW, LINK1, *AUTHOR1]))

# --- card 2: HOLLY scene3_beat2 -----------------------------------------------------
m2 = moment("scene3_beat2", "HOLLY")
assert m2["model"]["archetypes"] == m2["review"]["archetypes"] == ["Trickster"] and not m2["changed"]
print("card 2")
pages2 = K.render_pages(m2["pdf_pages"], [("context", 63, 64), ("beat", *m2["lines"])])
S2 = f("card 2 sentence", "The AI read Holly in this moment as Trickster, and the human review kept the call "
                          "and the AI's read unchanged.")
B2 = f("card 2 badge", "Upheld: Trickster, with no field changes.")
body2 = f'''<header class="top"><h1>{e(T2)}</h1><p>{e(S2)}</p></header>
<main class="card">
  <div class="pages">{K.pages_html(pages2, "c2")}</div>
  <aside>
    <p class="who">{e(name(m2["character"]))}</p>
    {legend([("beat", L_MOMENT), ("context", L_CONTEXT)])}
    {ai_side(m2)}
    {review_side(m2, B2)}
    {hood([m2], "<p>Lead-in: fog_full.txt lines 63–64, the speaker of the line the moment opens on.</p>")}
  </aside>
</main>'''
built.append(write(CARD2, T2, body2, [H_AI, H_REVIEW]))

# --- card 3: the protected becomes the protector ------------------------------------
m3a, m3b, m3c = moment("scene75_beat3", "MACKIE"), moment("scene75_beat5", "YOUNG JOHN"), moment("scene217_beat1", "JOHN")
assert m3a["model"]["archetypes"] == m3a["review"]["archetypes"] == ["Great Mother"] and m3a["dark"] and not m3a["changed"]
assert m3b["model"]["archetypes"] == m3b["review"]["archetypes"] == ["Hero"] and not m3b["changed"]
assert m3c["model"]["archetypes"] == m3c["review"]["archetypes"] == ["Great Mother"] and not m3c["dark"] and m3c["changed"]
# "Same basis" in 75_3's note points to the scene-75 row before it (75_1).
basis_verdict, basis_note = review_row("MACKIE", "scene75_beat1")
assert m3a["note"] == ["Same basis (scene 75 cover-up arc)."] and "dark pole" in basis_verdict
K.verify_note_quotes("scene75_beat1 MACKIE", basis_note)
print("card 3, then")
pages3a = K.render_pages(sorted(set(m3a["pdf_pages"] + m3b["pdf_pages"])),
                         [("beat", *m3a["lines"]), ("context", 2357, 2364), ("beat2", *m3b["lines"])])
print("card 3, now")
pages3c = K.render_pages(m3c["pdf_pages"], [("beat", *m3c["lines"])])
S3 = f("card 3 sentence", "In a flashback scene, the AI read Mackie as Great Mother over his son and Young John "
                          "as Hero. Then, near the end of the script, the AI read John as Great Mother over his "
                          "sister Trudy. The human review kept all three calls.")
P_THEN = f("card 3 panel label", "Then")
P_NOW = f("card 3 panel label", "Now")
B3a = f("card 3 badge, Mackie", "Upheld: Great Mother, marked dark pole.")
B3b = f("card 3 badge, Young John", "Upheld: Hero.")
B3c = f("card 3 badge, John", "Upheld: Great Mother, with fields corrected; not marked dark pole.")
BASIS = f("card 3 basis label", "The basis this note points to, from the review of Mackie's first moment in this scene:")
L_GM = f("card 3 legend", "Amber: the Great Mother moments, Mackie then and John now.")
L_YJ = f("card 3 legend", "Blue: the moment the AI tagged for Young John")
LINK3 = f("card 3 link", "Mackie also appears in the card Mackie: Great Mother or Shadow?")
# The author confirmed (2026-10-06) that "Same basis" in the 75_3 note refers
# to the 75_1 note shown with it.
BASIS_CONFIRMED = f("card 3 hood", "The 75_3 review note refers to an earlier note; the author confirmed which one.")
body3 = f'''<header class="top"><h1>{e(T3)}</h1><p>{e(S3)}</p>
  {legend([("beat", L_GM), ("beat2", L_YJ), ("context", L_CONTEXT)])}</header>
<main class="card" id="then">
  <h2 class="panel-label">{e(P_THEN)}</h2>
  <div class="pages">{K.pages_html(pages3a, "c3a")}</div>
  <aside>
    <div class="moment">
      <p class="who">{e(name(m3a["character"]))}</p>
      {ai_side(m3a)}
      {review_side(m3a, B3a, (BASIS, basis_note))}
    </div>
    <div class="moment">
      <p class="who">{e(name(m3b["character"]))}</p>
      {ai_side(m3b)}
      {review_side(m3b, B3b)}
    </div>
    {hood([m3a, m3b], f"<p>Lead-in: fog_full.txt lines 2357–2364, the moment between the two. "
                      f"Basis row: {e(REVIEW_FILES['MACKIE'])}, scene75_beat1, verdict "
                      f"<span{V}>“{e(basis_verdict)}”</span>.</p><p>{e(BASIS_CONFIRMED)}</p>")}
  </aside>
</main>
<main class="card" id="now">
  <h2 class="panel-label">{e(P_NOW)}</h2>
  <div class="pages">{K.pages_html(pages3c, "c3c")}</div>
  <aside>
    <div class="moment">
      <p class="who">{e(name(m3c["character"]))}</p>
      {ai_side(m3c)}
      {review_side(m3c, B3c)}
    </div>
    {hood([m3c])}
  </aside>
  <p class="link"><a href="{CARD1}">{e(LINK3)}</a></p>
</main>'''
built.append(write(CARD3, T3, body3, [H_AI, H_REVIEW, P_THEN, P_NOW, LINK3]))

# --- card 4: PETE scene122_beat1, a turning-point card ---------------------------------
# The AI's side is its stored Pass 2 claim, verbatim (the synthesis turning
# point), not the four read fields. The human side is the verdict in the
# Pass 2 table of FOG_PETE_REVIEW.md and the note block under it, verbatim.
syn = json.load(open(os.path.join(K.ROOT, "fog_pass2_calls", "synthesis_PETE.json"), encoding="utf-8"))
tp = next(t for t in syn["turning_points"] if t["beat_id"] == "scene122_beat1")
assert tp["likely_category"] == "boundary_revealed", tp
raw_syn = open(os.path.join(K.ROOT, "fog_pass2_calls", "synthesis_raw_PETE.json"), encoding="utf-8").read()
if json.dumps(tp["what_changes"], ensure_ascii=False)[1:-1] not in raw_syn and \
        json.dumps(json.dumps(tp["what_changes"])[1:-1])[1:-1] not in raw_syn:
    sys.exit("ABORT: stored what_changes is not verbatim in synthesis_raw_PETE.json")
pete_now = entry(now, "scene122_beat1", "PETE")["causal_integrity"]["characterization_consistency"]
corr = [(i + 1, c) for i, c in enumerate(now["corrections"]) if c["beat_id"] == "scene122_beat1"
        and c["character"] == "PETE" and c["field_name"] == "characterization_consistency"]
assert len(corr) == 1 and logged(corr[0][1]["llm_value"]) == "boundary_revealed" \
    and logged(corr[0][1]["human_value"]) == "consistent" == pete_now, corr
log_no = corr[0][0]

pete_text = open(os.path.join(K.ROOT, "FOG_PETE_REVIEW.md"), encoding="utf-8").read()
rows = [l for l in pete_text.split("\n") if l.startswith("| scene122_beat1 |")]
assert len(rows) == 1, rows
p_draft, p_reviewed, p_record = [c.strip() for c in rows[0].strip().strip("|").split("|")][1:]
assert p_reviewed == "**consistent**" and p_record == f"log ({log_no})", (p_reviewed, p_record)
blk = re.search(r"^\*\*scene122_beat1, consistent \(author-confirmed\)\.\*\*\n((?:- .*\n(?:  .*\n)*)+)",
                pete_text, re.M)
if not blk:
    sys.exit("ABORT: PETE scene122_beat1 note block not found in FOG_PETE_REVIEW.md")
bullets = [" ".join(x.split()) for x in re.split(r"^- ", blk.group(1), flags=re.M) if x.strip()]
assert len(bullets) == 4, bullets
for b in bullets:
    K.verify_note_quotes("scene122_beat1 PETE", b)
b_shown = [b for b in bullets if not K.INTERNAL_RE.search(b)]
b_internal = [b for b in bullets if K.INTERNAL_RE.search(b)]


def md(s):
    """The record's own markdown bold, rendered; the words are unchanged."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(s))


# How many of the AI's change-claims the review overturned: counted per queue
# entry (fog_pass2_queue.json drafts vs. fog_tagged.json now) and checked
# against the before/after table in FOG_PASS2_CLOSEOUT.md.
CHANGE = ("throughline_evolution", "boundary_revealed")
by_id = {b["beat_id"]: b for b in now["beats"].values()}
queue = json.load(open(os.path.join(K.ROOT, "fog_pass2_queue.json"), encoding="utf-8"))["needs_correction_review"]
drafted, final, overturned = {}, {}, 0
for q in queue:
    pcq = next(c for c in by_id[q["beat_id"]]["per_character"] if c["character"] == q["character"])
    d, fv = q["characterization_consistency"], pcq["causal_integrity"]["characterization_consistency"]
    drafted[d] = drafted.get(d, 0) + 1
    final[fv] = final.get(fv, 0) + 1
    overturned += d in CHANGE and fv == "consistent"
claims = sum(drafted.get(k, 0) for k in CHANGE)
closeout = open(os.path.join(K.ROOT, "FOG_PASS2_CLOSEOUT.md"), encoding="utf-8").read()
table = {m[0]: (int(m[1]), int(m[2])) for m in re.findall(
    r"^\s*\| (throughline_evolution|boundary_revealed|consistent) \| (\d+) \| (\d+) \|", closeout, re.M)}
assert len(table) == 3 and all((drafted.get(k, 0), final.get(k, 0)) == v for k, v in table.items()), table
assert (claims, overturned) == (sum(table[k][0] for k in CHANGE), table["consistent"][1] - table["consistent"][0])

print("card 4")
pages4 = K.render_pages([74, 75], [("beat2", 3942, 3948), ("beat", 3953, 3980)])
TURN = report.TURN_LABEL["boundary_revealed"]     # the report's plain label: "A limit revealed"
# Wording for the reviewed value: the author's (2026-10-06).
T4 = f("card 4 title", "Pete: Limit Revealed or Character-Consistent?")
S4 = f("card 4 sentence", "The AI read this moment as Pete reaching a limit not seen before; the human review "
                          "changed the call to consistent with his character.")
V4_REVIEW = f("card 4 review value", "Character-consistent")
B4 = f("card 4 badge", "Overturned: a limit revealed to character-consistent.")
L_PUNCH = f("card 4 legend", "Blue: the punch, in an earlier moment")
CONTEXT4 = f("card 4 hood", f"One of {overturned} change-claims (out of {claims}) that the human review overturned.")
ID = "scene121_beat2"
ID_NOTE = f("card 4 hood, scene ID note",
            f"{ID} is the system's ID for an earlier moment, in scene 121, that the AI is pointing back to.")
assert ID in tp["what_changes"] and ID == tp["comparison_beat_id"], tp
SMALL_TP = f("card 4 hood", "The AI's read here is its stored turning-point claim, shown word for word. Highlighted "
                            "lines are matched word for word against the script text before they are drawn, and "
                            "every quotation in the review note is checked against the same file when the card is "
                            "built.")
hood4 = hood_block([
    f"<p>{e(ID_NOTE)}</p>",
    f'''<p><b>Pete, scene122_beat1.</b> fog_full.txt lines 3953–3980; the punch is lines 3942–3948
(scene121_beat3). Stored value: characterization_consistency {e(corr[0][1]["llm_value"])} → {e(pete_now)}
(corrections log #{log_no}). The AI's claim is the Pass 2 synthesis turning point in
fog_pass2_calls/synthesis_PETE.json ({e(tp["turning_point_type"])} vs. {e(tp["comparison_beat_id"])}, likely
category {e(tp["likely_category"])}, trait: <span{V}>“{e(tp["trait_it_relates_to"])}”</span>), checked against
the raw response.</p>''',
    f'''<p>Review record: FOG_PETE_REVIEW.md, Pass 2 table: draft <span{V}>“{e(p_draft)}”</span>, reviewed
<span{V}>{e(p_reviewed.strip("*"))}</span>, <span{V}>{e(p_record)}</span>; note block “scene122_beat1, consistent
(author-confirmed)”.</p>''',
    (f'<p><b>{e(L_REST)} (Pete).</b> <span{V}>{md(" ".join(b_internal))}</span></p>' if b_internal else ""),
    f"<p>{e(CONTEXT4)} Counted per queue entry (fog_pass2_queue.json drafts vs. fog_tagged.json) and checked "
    f"against FOG_PASS2_CLOSEOUT.md.</p>",
], SMALL_TP)
body4 = f'''<header class="top"><h1>{e(T4)}</h1><p>{e(S4)}</p></header>
<main class="card">
  <div class="pages">{K.pages_html(pages4, "c4")}</div>
  <aside>
    <p class="who">Pete</p>
    {legend([("beat", L_MOMENT), ("beat2", L_PUNCH)])}
    <section class="claim">
      <h2><span class="chip-ai">{e(H_AI)}</span></h2>
      <div class="value">{e(TURN)}</div>
      <p class="note claimtext"{V}>{e(tp["what_changes"])}</p>
    </section>
    <section class="verdict">
      <h2><span class="chip-human">{e(H_REVIEW)}</span></h2>
      <div class="value">{e(V4_REVIEW)}</div>
      <dl class="fields"><dt>{e(L_VERDICT)}</dt><dd{V}>{e(p_reviewed.strip("*"))}</dd></dl>
      <ul class="note"{V}>{"".join(f"<li>{md(b)}</li>" for b in b_shown)}</ul>
    </section>
    <div class="badge changed">{e(B4)}</div>
    {hood4}
  </aside>
</main>'''
built.append(write(CARD4, T4, body4, [H_AI, H_REVIEW, ID_NOTE]))

# --- checks --------------------------------------------------------------------------
# Fixed labels and template text on every card are framing too.
for where, text in [("field label", "Self-perceived"), ("field label", "Audience-perceived"),
                    ("field label", "Emotion"), ("field label", "Goal"),
                    ("label", "Under the hood"), ("footer", "Tap a page to enlarge it.")]:
    f(where, text)
# The scene ID is quoted from the AI's locked claim (author ruling 2026-10-06).
K.check_framing(FRAMING, locked_text=tp["what_changes"], locked_terms=[ID])
# The caption under each rendered page names its page number, which the
# report-voice citation rule forbids in AI text. Exemption approved by the
# author 2026-10-06 (STORY_REPORT_SPEC.md, Scoping the guard): plain-text
# checks only, and N is read from the page itself (card_kit.printed_number);
# test_demo_cards checks every caption against the page it sits under.
report.check_plain("page caption", "Full of Grace, page 84")
FRAMING.append(("page caption (plain-text checks only; names the page shown)", "Full of Grace, page N"))
for path, required in built:
    K.check_card(path, required)
if REVIEW:
    # Every framing line, named by where it is registered and its builder line.
    sources = review_mode.source_map([(f"f({w!r})", t, None) for w, t in FRAMING],
                                     os.path.abspath(__file__))
    sources.update(review_mode.source_map([("page caption", "Full of Grace, page", "<figcaption>Full of Grace, page")],
                                          os.path.join(K.OUT_DIR, "card_kit.py")))
    for fname, title, body, required in PAGES:
        page = K.page_shell(title, body, review={"page": "card " + fname[:-len(".html")],
                                                 "store": "numen-review-edits:card:" + fname, "sources": sources})
        review_mode.assert_review(page, fname)
        rpath = review_mode.review_path(os.path.join(K.OUT_DIR, fname))
        with open(rpath, "w", encoding="utf-8") as fh:
            fh.write(page)
        K.check_card(rpath, required)
        print("review build (local only, git-ignored):", rpath)
print("\nFRAMING LINES:")
for where, s in FRAMING:
    print(f"  [{where}] {s}")
