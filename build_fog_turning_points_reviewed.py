"""
build_fog_turning_points_reviewed.py -- writes fog_turning_points_reviewed.json.

The 36 FOG character turns that stand after human Pass 2 review (18
boundary_revealed + 18 throughline_evolution in fog_tagged.json), each with
its REVIEWED anchor and trait. The reviewed anchors and traits were never
stored as data: re-anchors, retired and new traits, and record corrections
live only in the FOG_*_REVIEW.md files, while fog_pass2_calls/synthesis_*.json
stays the cold record. This file puts them in one place for the report
(author decision D2, 2026-10-04).

Per entry:
- pulled automatically: the stored verdict (asserted against fog_tagged.json),
  the cold Pass 2 draft (8079f93, via fog_report_model.json), the cold
  synthesis turning point(s) and resolver checked_against, and the
  characterization_consistency log numbers;
- hand-entered from the review files: status, comparison beat, shape,
  trait, and a one-line note. Every hand-entered entry carries citations,
  and the build asserts that each cited file:line exists and contains the
  given phrase.

The hand-entered fields are Claude's reading of the cited lines and are
marked author_checked: false until the author checks them.

Run from the repo root:  python build_fog_turning_points_reviewed.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from tagging_schema import beat_id_sort_key  # noqa: E402

OUT = os.path.join(ROOT, "fog_turning_points_reviewed.json")
SYN_NAME = {"O’SHEA": "O_SHEA", "YOUNG JOHN": "YOUNG_JOHN"}

# (character, beat_id, status, comparison_beat or None, shape, trait, note,
#  [(file, line, must_contain), ...])
J, T, D, C, R = ("FOG_JOHN_REVIEW.md", "FOG_TRUDY_REVIEW.md", "FOG_DOUG_REVIEW.md",
                 "FOG_CHEYENNE_REVIEW.md", "FOG_REGGIE_REVIEW.md")
ENTRIES = [
    ("BETH", "scene85_beat2", "confirmed, factual correction", "scene3_beat1", "escalation",
     "trait 1: bossy, impatient, dismissive toward friends' fears or objections",
     "Confirmed as drafted; a factual detail in the record was corrected.",
     [("FOG_BETH_REVIEW.md", 125, "scene85_beat2"), ("FOG_BETH_REVIEW.md", 150, "confirmed, with a factual")]),
    ("CHEYENNE", "scene133_beat1", "confirmed", "scene98_beat1", "escalation",
     "trait 3: visible strain and substance use beneath a functioning exterior",
     "Confirmed as drafted.",
     [(C, 75, "scene133_beat1"), (C, 80, "confirmed (author-confirmed)")]),
    ("CHEYENNE", "scene155_beat5", "re-anchored", "scene155_beat3", "escalation",
     "advocacy for Holly (untracked by the synthesis; origin scene155_beat3)",
     "From expressing worry to material commitment (“I'll hire you.”). Was trait 2 vs. scene64_beat7/155_3.",
     [(C, 149, "advocacy-for-Holly thread"), (C, 175, "confirmed and re-anchored"),
      (C, 186, "advocacy-for-Holly thread vs. its origin scene155_beat3")]),
    ("CHEYENNE", "scene155_beat11", "verdict changed, re-anchored", "scene152_beat1/2", "first failure of the trait's function",
     "trait 4: when cornered, manipulation, false threats or denial to escape",
     "The avoidance mechanism does not activate; she confesses instead. Was an echo of scene152_beat2's denial (fails 8b on content).",
     [(C, 151, "first failure of trait 4"), (C, 208, "Re-anchored"),
      (C, 230, "the trait-4 avoidance mechanism (function, not content), vs."), (C, 231, "scene152_beat1/2")]),
    ("DOUG", "scene101_beat1", "confirmed, reasoning corrected", "scene71_beat1", "escalation",
     "trait 5: uses his police access and initiative to assist John's investigation",
     "Claim (a) confirmed. The model's secondary claim (b), trait 4 vs. scene57_beat3, does not hold.",
     [(D, 71, "Claim b **does not hold**"), (D, 74, "claim (a): throughline_evolution, confirmed"),
      (D, 93, "claim (b), trait 4 vs. scene57_beat3: does not hold")]),
    ("DOUG", "scene118_beat1", "confirmed", "scene101_beat1", "escalation",
     "trait 5: uses his police access and initiative to assist John's investigation",
     "Confirmed as drafted.",
     [(D, 72, "scene118_beat1 | throughline_evolution (trait 5)"), (D, 127, "escalation within trait 5")]),
    ("DOUG", "scene123_beat7", "confirmed, reasoning corrected", "scene56_beat1", "escalation",
     "trait 2: gentle companionship and consideration for John's emotional state",
     "Value confirmed; two factual details corrected (the cigarette; the cut-off line).",
     [(D, 164, "trait 2 vs. scene56_beat1"), (D, 169, "Two"), (D, 455, "Cigarette and cut-off line corrected")]),
    ("DOUG", "scene123_beat14", "confirmed, reasoning corrected", "scene86_beat3", "escalation",
     "trait 7: calm, composed demeanor when personally challenged or insulted",
     "Value confirmed; the escalation is in severity, not in having witnesses.",
     [(D, 166, "trait 7 vs. scene86_beat3"), (D, 194, "confirmed with corrected reasoning"),
      (D, 457, "Severity, not witnessing")]),
    ("DOUG", "scene123_beat15", "re-anchored", "scene123_beat9", "echo",
     "trait 2 thread: diagnosis restated as flat pity (“I feel sorry for you, John.”)",
     "Was a trait-3 echo of scene56_beat2; now an echo of scene123_beat9 inside the trait-2 thread.",
     [(D, 167, "echo of scene123_beat9"), (D, 224, "confirmed and re-anchored"),
      (D, 477, "diagnosis-into-pity echo"), (D, 482, "It replaces scene123_beat15's trait-3 anchor")]),
    ("JOHN", "scene119_beat3", "confirmed", "scene19_beat1", "escalation",
     "persuasion/extraction: the consent-based wager becomes institutional coercion (the ICE threat)",
     "Confirmed as drafted.",
     [(J, 285, "scene119_beat3 | throughline_evolution | **throughline_evolution, confirmed**"),
      (J, 911, "scene119_beat3 (escalation: institutional coercion")]),
    ("JOHN", "scene138_beat2", "confirmed, reasoning corrected", "scene13_beat1", "boundary: composure gives way",
     "composure under cumulative, unprocessed weight (first shown scene13_beat1)",
     "No trigger and no target; not an escalation of the reactive-anger beats (scene119_beat7, scene123_beat13). The claim that composure had “never before cracked” is struck.",
     [(J, 801, "scene138_beat2, reasoning corrected"), (J, 925, "Composure under cumulative, unprocessed weight"),
      (J, 926, "gives way at scene138_beat2")]),
    ("JOHN", "scene152_beat1", "confirmed, citation corrected", "scene119_beat3", "escalation",
     "persuasion/extraction: institutional coercion becomes physical coercion (pinning Cheyenne)",
     "Resolver's checked_against corrected from scene19_beat1 to scene119_beat3 (the synthesis already named it).",
     [(J, 370, "scene152_beat1 | throughline_evolution | **throughline_evolution, confirmed**"),
      (J, 393, "scene19_beat1 -> scene119_beat3"), (J, 911, "scene152_beat1 (escalation: physical coercion")]),
    ("JOHN", "scene154_beat1", "confirmed, reasoning corrected", "scene152_beat1", "escalation",
     "persuasion/extraction: psychological pressure layered onto the pin",
     "The resolver called it a continuation; review recorded it as an escalation vs. scene152_beat1.",
     [(J, 371, "confirmed, with corrected reasoning"), (J, 386, "escalation vs. scene152_beat1"),
      (J, 911, "scene154_beat1 (escalation: psychological pressure")]),
    ("JOHN", "scene163_beat1", "confirmed, reasoning corrected", "scene115_beat1", "escalation",
     "armed pursuit: arming for an expected confrontation",
     "Not breaking-and-entering: the cabin is John's and the locks had been changed on him.",
     [(J, 496, "scene163_beat1 | throughline_evolution | **throughline_evolution, confirmed"),
      (J, 503, "scene163_beat1, corrected reasoning"), (J, 912, "scene163_beat1 (escalation: arming for an expected confrontation")]),
    ("JOHN", "scene172_beat6", "verdict changed", "scene163_beat1", "type change (boundary)",
     "armed pursuit: from armed and prepared to lethal force used against a person",
     "Was throughline_evolution (batch 3 no-op); changed to boundary_revealed under finding 19's two-axis test. No prior JOHN beat shows lethal force at a person.",
     [(J, 974, "scene172_beat6 | throughline_evolution | **boundary_revealed**"), (J, 1027, "scene172_beat6 -> boundary_revealed")]),
    ("JOHN", "scene175_beat1", "confirmed, reasoning corrected", "scene172_beat7", "boundary",
     "life-preserving instinct, extended to his attacker",
     "“Let me make a call.” read (author's reading, not stated text) as asking for his phone back to call help for Reggie.",
     [(J, 501, "scene175_beat1 | boundary_revealed | **boundary_revealed, confirmed"),
      (J, 576, "scene175_beat1, confirmed, with corrected reasoning"),
      (J, 912, "scene175_beat1 (boundary: the life-preserving instinct extended to his attacker)")]),
    ("JOHN", "scene217_beat1", "verdict changed", "scene185_beat2", "type change (boundary)",
     "justice treated as independent of his own action (rooted in guilt over Andy): omission becomes commission",
     "Was throughline_evolution (batch 4 no-op). First active intervention: handing Trudy the car keys.",
     [(J, 973, "scene217_beat1 | throughline_evolution | **boundary_revealed**"), (J, 1010, "scene217_beat1 -> boundary_revealed"),
      (J, 1018, "is its first **commission**")]),
    ("JOHN", "scene223_beat1", "verdict changed twice", "scene213_beat3", "type change (boundary)",
     "reciprocal honesty under the right conditions (first shown scene213_beat3)",
     "Draft throughline_evolution -> consistent (log 750) -> boundary_revealed (log 763): the first proactive, unilateral disclosure. The echo of scene14_beat4 stays rejected.",
     [(J, 975, "scene223_beat1 | consistent | **boundary_revealed**"), (J, 1049, "scene223_beat1 -> boundary_revealed"),
      (J, 1053, "scored against the trait first shown at scene213_beat3")]),
    ("MACKIE", "scene140_beat6", "re-anchored", None, "own origin (8a)",
     "a previously untested capacity for physical violence against his own son",
     "Was a trait-2 continuation of scene140_beat5. No comparison beat; Principle 11 instance. weight_proportionality mismatch -> matched (log 809).",
     [("FOG_MACKIE_REVIEW.md", 86, "re-anchored as its own origin"),
      ("FOG_MACKIE_REVIEW.md", 115, "re-anchored as its own"), ("FOG_MACKIE_REVIEW.md", 128, "its own origin, no")]),
    ("O’SHEA", "scene154_beat2", "verdict changed", "scene153_beat1", "escalation",
     "trait 1: uses a firearm and aggressive posture against a perceived threat to Cheyenne",
     "Drafted boundary_revealed; the claimed limit rested on John's act (disarming him), not O'Shea's own.",
     [("FOG_OSHEA_REVIEW.md", 112, "scene154_beat2 | boundary_revealed"), ("FOG_OSHEA_REVIEW.md", 117, "scene154_beat2, throughline_evolution"),
      ("FOG_OSHEA_REVIEW.md", 124, "escalation of trait 1")]),
    ("O’SHEA", "scene155_beat12", "re-anchored", "scene155_beat8", "escalation",
     "trait 3: genuine tenderness and concern for Cheyenne beneath the tough exterior",
     "Was a trait-1 echo of scene155_beat1; the gun hand-back is John's act. Now: verbal gentleness becomes demonstrated physical care.",
     [("FOG_OSHEA_REVIEW.md", 189, "re-anchored to trait 3 escalation vs. 155_8"),
      ("FOG_OSHEA_REVIEW.md", 254, "throughline_evolution confirmed, re-anchored"),
      ("FOG_OSHEA_REVIEW.md", 271, "Comparison 155_1 -> **155_8**")]),
    ("RAYMOND", "scene205_beat1", "re-anchored", None, "own origin",
     "genuine break under interrogation: escalating self-harm",
     "Was a continuation of scene201_beat5 (trait 4); 201_5 never cracked anything. No comparison beat.",
     [("FOG_RAYMOND_REVIEW.md", 72, "re-anchored as its own origin"),
      ("FOG_RAYMOND_REVIEW.md", 119, "re-anchored as its own origin"), ("FOG_RAYMOND_REVIEW.md", 131, "Not a continuation of 201_5")]),
    ("REGGIE", "scene134_beat2", "verdict changed, re-anchored", None, "own origin (8a)",
     "trait 8 (as now recorded): premeditated violence, with concealment inherent to it",
     "Drafted throughline_evolution (trait 7 escalation vs. scene132_beat1). Trait 7 was later retired into trait 8, which originates here.",
     [(R, 275, "scene134_beat2 | throughline_evolution"), (R, 585, "Trait 8 is premeditated violence"),
      (R, 592, "**trait 8 origin**"), (R, 981, "scene134_beat2: confirmed as trait 8's origin")]),
    ("REGGIE", "scene172_beat1", "verdict changed, re-scored", "scene134_beat2", "type change (boundary)",
     "trait 8: premeditated violence, first confrontational use (obstructing the 911 call)",
     "Drafted throughline_evolution (trait 5 escalation vs. scene95_beat1); re-scored to trait 8 under 8b. The comparison beat is the trait 8 origin, derived from the review's reasoning (396-414).",
     [(R, 370, "re-scored to the premeditated-violence capacity"), (R, 396, "scene172_beat1, boundary_revealed"),
      (R, 595, "trait 8, first confrontational use"), (R, 976, "comparison scene134_beat2 confirmed")]),
    ("REGGIE", "scene172_beat6", "verdict changed, re-anchored", "scene95_beat1", "type change (boundary)",
     "loyalty to Mackie personally (planted scene95_beat1); trait 8 is the mechanism",
     "Drafted throughline_evolution (continuation vs. scene172_beat5). Anchor moved from synthesis trait 1 (scene53_beat1) to the Mackie-personally thread.",
     [(R, 596, "traits 1+5 jointly, trait 8 as mechanism"),
      (R, 755, "scene172_beat6 anchors on the Mackie-personally thread, scene95_beat1"), (R, 763, "planted at **scene95_beat1**")]),
    ("RICARDO", "scene119_beat9", "re-anchored", "scene119_beat1", "escalation",
     "trait 4: cooperates with basic, low-risk factual answers once caught",
     "Was a trait-5 (denial) continuation of scene119_beat7. Naming the two men is cooperation, from low-risk answers to consequential disclosure.",
     [("FOG_RICARDO_REVIEW.md", 201, "re-anchored to trait 4"), ("FOG_RICARDO_REVIEW.md", 245, "re-anchored from trait"),
      ("FOG_RICARDO_REVIEW.md", 251, "trait 4's origin")]),
    ("TRUDY", "scene40_beat3", "confirmed", "scene32_beat2", "boundary",
     "steady caretaker of the family: who cares for whom reverses",
     "Confirmed as drafted.",
     [(T, 205, "scene40_beat3 | boundary_revealed | **boundary_revealed, confirmed**")]),
    ("TRUDY", "scene143_beat7", "confirmed; trait reworded", "scene143_beat6", "boundary (depth reveal)",
     "resentment/jealousy over the family's favoritism toward Cheyenne and Holly (reworded trait 6)",
     "Confirmed. The synthesis trait was split: concealment went to scene57_beat2, resentment re-anchored at scene143_beat6.",
     [(T, 207, "scene143_beat7 | boundary_revealed | **boundary_revealed, confirmed**"),
      (T, 319, "resentment/jealousy over the family's favoritism"), (T, 356, "Comparison chain after the split, confirmed")]),
    ("TRUDY", "scene188_beat1", "verdict changed", None, "boundary (untested register)",
     "her faith: the first private, solitary devotional act",
     "Drafted throughline_evolution vs. scene131_beat1; review set that comparison aside (every earlier faith beat is public or social).",
     [(T, 289, "scene188_beat1 | throughline_evolution | **boundary_revealed**"), (T, 396, "scene188_beat1: boundary_revealed"),
      (T, 541, "comparison beat. The human-reviewed scene188_beat1 verdict"), (T, 593, "scene188_beat1: confirmed, no comparison")]),
    ("TRUDY", "scene213_beat2", "confirmed", "scene34_beat2", "boundary",
     "calm, faith-based acceptance of personal pain: her faith cracking",
     "Confirmed as drafted.",
     [(T, 208, "scene213_beat2 | boundary_revealed | **boundary_revealed, confirmed**")]),
    ("TRUDY", "scene213_beat7", "confirmed, re-anchored", None, "own origin",
     "arranging harm: hiring Raymond to take Holly (finding 18 limit E)",
     "Confirmed. The turning point is her act of confessing, not only the past hiring; limit E is first shown here. The cold comparison scene30_beat1 is dropped. The synthesis trait's “under religious justification” is not on the page at this beat.",
     [(T, 133, "scene213_beat7 | boundary_revealed | **boundary_revealed, confirmed**"),
      (T, 160, "the hiring/arranging capacity"), (T, 107, "It has no religious content"),
      (T, 585, "scene213_beat7: re-anchored as its own origin")]),
    ("TRUDY", "scene214_beat4", "confirmed as a new limit", "scene213_beat7", "boundary",
     "personal physical violence overriding a victim's visible resistance",
     "The synthesis called it a continuation of the arranging limit; review split it out as its own limit.",
     [(T, 136, "confirmed as a NEW limit"), (T, 162, "physical violence overriding a victim's visible resistance"),
      (T, 167, "beat is scene213_beat7, still the prior reference point")]),
    ("TRUDY", "scene216_beat5", "verdict changed", "scene214_beat4", "escalation",
     "personal physical violence (the scene214_beat4 limit): strikes after forced submersion",
     "Drafted boundary_revealed; recorded as throughline_evolution, an escalation of the scene214_beat4 limit.",
     [(T, 141, "escalation of the scene214_beat4 limit"), (T, 183, "recorded as `throughline_evolution`")]),
    ("TRUDY", "scene216_beat7", "confirmed", "scene216_beat6", "boundary",
     "composure cracking into real horror",
     "Confirmed; distinct from both premeditated-violence limits. The comparison beat was carried from the AI draft and confirmed by the author.",
     [(T, 143, "scene216_beat7 | boundary_revealed | **boundary_revealed, confirmed**"), (T, 174, "genuine break anchored in the text"),
      (T, 591, "comparison scene216_beat6 confirmed")]),
    ("YOUNG JOHN", "scene75_beat3", "confirmed, reasoning corrected", "scene75_beat2", "escalation",
     "trait 4: takes the blame himself to protect Andy",
     "It is a true account, not a false confession: from arguing with his father to offering to tell the authorities himself.",
     [("FOG_YOUNGJOHN_REVIEW.md", 85, "reasoning corrected"), ("FOG_YOUNGJOHN_REVIEW.md", 99, "scene75_beat3, throughline_evolution, confirmed"),
      ("FOG_YOUNGJOHN_REVIEW.md", 101, "Not a false confession")]),
    ("YOUNG JOHN", "scene140_beat2", "verdict changed", "scene67_beat1", "escalation",
     "trait 3: shock and distress when a situation exceeds his coping capacity",
     "Drafted boundary_revealed; quiet shock becomes a full panic attack, triggered by the funeral.",
     [("FOG_YOUNGJOHN_REVIEW.md", 278, "scene140_beat2 | boundary_revealed"),
      ("FOG_YOUNGJOHN_REVIEW.md", 294, "scene140_beat2, throughline_evolution"), ("FOG_YOUNGJOHN_REVIEW.md", 301, "real intensification of trait 3")]),
]

# Author check, 2026-10-05: the seven flagged entries, each with where its
# comparison beat comes from (None = no comparison beat).
AUTHOR_CHECKED = {
    ("REGGIE", "scene172_beat1"): "derived from the review's reasoning (FOG_REGGIE_REVIEW.md:396-414)",
    ("TRUDY", "scene213_beat7"): None,
    ("TRUDY", "scene216_beat7"): "carried from the AI draft, confirmed by the author",
    ("TRUDY", "scene188_beat1"): None,
    ("MACKIE", "scene140_beat6"): None,
    ("RAYMOND", "scene205_beat1"): None,
    ("REGGIE", "scene134_beat2"): None,
}
AUTHOR_CHECK_DATE = "2026-10-05"
TRANSCRIBED = "transcribed from author-confirmed review records"
CARRIED = "carried from the AI draft, not restated in review"


def norm(text):
    text = text.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'}))
    return re.sub(r"\s+", " ", text).strip()


def paragraph(lines, n):
    a = n - 1
    while a > 0 and lines[a - 1].strip():
        a -= 1
    b = n - 1
    while b < len(lines) - 1 and lines[b + 1].strip():
        b += 1
    return "\n".join(lines[a:b + 1])


def consistency_check(entry, cites, files, full, index, draft_text):
    """The automated check for entries the author did not check line by line.
    Returns (comparison_source, [failures])."""
    bid, comp = entry["beat_id"], entry["reviewed"]["comparison_beat_id"]
    fails = []
    # 1. The stored verdict is named in the cited review passages.
    paras = [paragraph(files[f], n) for f, n, _ in cites]
    if not any(entry["verdict"] in p for p in paras):
        fails.append(f"stored verdict {entry['verdict']} not named in any cited review passage")
    # 2. The comparison beat traces to the review record or to the cold draft.
    source = None
    if comp:
        scene, beats = comp.split("_beat")
        ids = [f"{scene}_beat{b}" for b in beats.split("/")]
        cited_text = "\n".join(paras)
        cold_ids = {t["comparison_beat_id"] for t in entry["cold"]["synthesis_turning_points"]}
        if all(i in cited_text for i in ids):
            source = "stated in the review record"
        elif set(ids) <= cold_ids:
            source = CARRIED
        else:
            fails.append(f"comparison {comp} is neither in the cited passages nor the cold draft")
        fails += [f"comparison {i} not in fog_line_index.json" for i in ids if i not in index]
    # 3. Script lines: the beat's range exists, quoted script text in the
    #    entry is in fog_full.txt, and script line numbers cited next to a
    #    quote in the cited review lines hold that quote.
    span = index.get(bid)
    if not span or span["first_line"] < 1 or span["last_line"] > len(full):
        fails.append(f"beat line range missing or outside fog_full.txt: {span}")
    whole = norm(" ".join(full))
    for q in re.findall(r"“([^”]+)”", entry["reviewed"]["trait"] + " " + entry["reviewed"]["note"]):
        q_n = norm(q).rstrip(".,!?")
        if q_n in whole:
            continue
        if q_n in draft_text:  # the AI draft's own wording, quoted by review; not script text
            continue
        fails.append(f"quoted text in neither fog_full.txt nor the AI draft: {q!r}")
    for f, n, _ in cites:
        for q, a, b in re.findall(r'"([^"]{4,})"[,.]? \((\d{3,4})(?:-(\d{3,4}))?\)', files[f][n - 1]):
            a, b = int(a), int(b or a)
            if b > len(full):
                fails.append(f"{f}:{n} cites script line {b}, past the end of fog_full.txt")
            elif norm(q).rstrip(".,") not in norm(" ".join(full[a - 1:b])):
                fails.append(f"{f}:{n} quote {q!r} not found at fog_full.txt {a}-{b}")
    return source, fails


def main():
    cur = json.load(open(os.path.join(ROOT, "fog_tagged.json"), encoding="utf-8"))
    model = json.load(open(os.path.join(ROOT, "fog_report_model.json"), encoding="utf-8"))
    cold = {(e["beat_id"], e["character"]): e for e in model["views"]["cold"]}
    full = open(os.path.join(ROOT, "fog_full.txt"), encoding="utf-8").read().split("\n")
    index = json.load(open(os.path.join(ROOT, "fog_line_index.json"), encoding="utf-8"))["beats"]

    stored = {}
    for b in cur["beats"].values():
        for p in b["per_character"]:
            cc = (p.get("causal_integrity") or {}).get("characterization_consistency")
            if cc in ("boundary_revealed", "throughline_evolution"):
                stored[(b["beat_id"], p["character"])] = cc
    keys = [(e[1], e[0]) for e in ENTRIES]
    if set(keys) != set(stored) or len(keys) != len(set(keys)):
        sys.exit(f"ABORT: entries {sorted(set(keys) ^ set(stored))} do not match the stored turns")

    files = {}
    errors = []
    out = []
    for ch, bid, status, comp, shape, trait, note, cites in ENTRIES:
        for f, n, phrase in cites:
            lines = files.setdefault(f, open(os.path.join(ROOT, f), encoding="utf-8").read().split("\n"))
            if n > len(lines) or phrase not in lines[n - 1]:
                errors.append(f"{ch} {bid}: {f}:{n} does not contain {phrase!r}")
        syn = json.load(open(os.path.join(ROOT, "fog_pass2_calls",
                                          f"synthesis_{SYN_NAME.get(ch, ch.replace(' ', '_'))}.json"),
                             encoding="utf-8"))
        draft = next(e for e in cur["corrections"] if e["beat_id"] == bid and e.get("character") == ch
                     and e["field_name"].startswith("causal_integrity ("))
        ca = re.search(r"checked_against: (.*?)\): ", draft["notes"])
        logs = [i for i, e in enumerate(cur["corrections"], 1)
                if e["beat_id"] == bid and e.get("character") == ch
                and e["field_name"] == "characterization_consistency"]
        cold_cc = cold[(bid, ch)]["characterization_consistency"] if (bid, ch) in cold else None
        out.append({
            "character": ch,
            "beat_id": bid,
            "verdict": stored[(bid, ch)],
            "cold": {
                "draft_verdict": cold_cc,
                "synthesis_turning_points": [
                    {k: t.get(k) for k in ("turning_point_type", "comparison_beat_id", "trait_it_relates_to")}
                    for t in syn["turning_points"] if t["beat_id"] == bid],
                "resolver_checked_against": ca.group(1) if ca else None,
            },
            "reviewed": {
                "status": status,
                "comparison_beat_id": comp,
                "shape": shape,
                "trait": trait,
                "note": note,
                "sources": [f"{f}:{n}" for f, n, _ in cites],
            },
            "characterization_consistency_logs": logs,
        })
    if errors:
        for e in errors:
            print("  BAD CITATION", e)
        sys.exit(f"ABORT: {len(errors)} citations do not match their source lines")

    cites_by_key = {(e[0], e[1]): e[7] for e in ENTRIES}
    # The AI draft's wording for each entry: the character's synthesis and the
    # Pass 2 resolver note.
    draft_texts = {}
    for ch, bid, *_ in ENTRIES:
        syn = json.dumps(json.load(open(os.path.join(ROOT, "fog_pass2_calls",
                                f"synthesis_{SYN_NAME.get(ch, ch.replace(' ', '_'))}.json"), encoding="utf-8")),
                         ensure_ascii=False)
        notes = " ".join(e["notes"] for e in cur["corrections"] if e["beat_id"] == bid and e.get("character") == ch
                         and e["field_name"].startswith("causal_integrity ("))
        draft_texts[(ch, bid)] = norm(syn + " " + notes)
    failures = []
    for x in out:
        key = (x["character"], x["beat_id"])
        r = x["reviewed"]
        if key in AUTHOR_CHECKED:
            if (AUTHOR_CHECKED[key] is None) != (r["comparison_beat_id"] is None):
                sys.exit(f"ABORT: {key} comparison does not match the author check")
            r["comparison_source"] = AUTHOR_CHECKED[key]
            r["author_checked"] = True
            r["verification"] = f"author-checked {AUTHOR_CHECK_DATE}"
            continue
        source, fails = consistency_check(x, cites_by_key[key], files, full, index, draft_texts[key])
        failures += [f"{key[0]} {key[1]}: {m}" for m in fails]
        r["comparison_source"] = source
        r["author_checked"] = False
        r["verification"] = None
    if failures:
        for m in failures:
            print("  CHECK FAILED", m)
        print(f"{len(failures)} consistency failures; the {len(out) - len(AUTHOR_CHECKED)} "
              "unchecked entries are left without a verification mark")
    else:
        for x in out:
            if not x["reviewed"]["author_checked"]:
                x["reviewed"]["verification"] = TRANSCRIBED

    out.sort(key=lambda x: (x["character"], beat_id_sort_key(x["beat_id"])))
    doc = {
        "description": "The 36 FOG character turns standing after human Pass 2 review, with the "
                       "reviewed comparison beat and trait taken from the FOG_*_REVIEW.md records. "
                       "'cold' is pulled automatically; 'reviewed' fields are Claude's reading of the "
                       "cited lines. author_checked true = the author checked the entry line by line "
                       f"({AUTHOR_CHECK_DATE}, the 7 flagged entries). verification "
                       f"'{TRANSCRIBED}' = not checked line by line, but it passed the automated "
                       "consistency check (verdict named in the cited passages, comparison beat "
                       "traceable to the review or the cold draft, quoted script text and cited "
                       "script lines found in fog_full.txt). Comparison beats are data-layer only; "
                       "the report's plain-language text never shows them.",
        "built_by": "build_fog_turning_points_reviewed.py",
        "counts": {"boundary_revealed": sum(x["verdict"] == "boundary_revealed" for x in out),
                   "throughline_evolution": sum(x["verdict"] == "throughline_evolution" for x in out)},
        "turns": out,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"{len(out)} turns, {doc['counts']}, every citation verified -> {os.path.basename(OUT)}")


if __name__ == "__main__":
    main()
