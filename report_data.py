"""
report_data.py -- data layer for the story report (Stage 6), Full of Grace.

Builds three things, all deterministic, no API call:

  1. The two views the report toggles between:
       cold     -- what the pipeline produced with no human correction.
                   Pass 1 fields come from git snapshot 7a6e69e (460/460
                   tagged, 0 corrections). Pass 2 fields
                   (weight_proportionality, characterization_consistency)
                   come from 8079f93, the commit that applied all 524
                   Pass 2 drafts. Caveat, shown on the report's cold
                   label: the Pass 2 run happened after 196 Pass 1
                   corrections, so some tags it built on had already
                   been reviewed.
       reviewed -- the current fog_tagged.json.
  2. A replay audit: the corrections log is run backward from the
     reviewed data and compared with both snapshots. Every difference
     must fall into a known, named category, or the build stops. The
     snapshots are the source of truth; the replay only checks them.
  3. fog_line_index.json -- each beat's line range in fog_full.txt and
     its PDF / printed page numbers -- and fog_report_model.json, the
     combined model the report renders from.

Run from the repo root:  python report_data.py
"""
import ast
import copy
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from tagging_schema import beat_id_sort_key  # noqa: E402
import git_snapshots  # noqa: E402

TAGGED = os.path.join(ROOT, "fog_tagged.json")
FULL_TXT = os.path.join(ROOT, "fog_full.txt")
LINE_INDEX_OUT = os.path.join(ROOT, "fog_line_index.json")
MODEL_OUT = os.path.join(ROOT, "fog_report_model.json")

COLD_PASS1_COMMIT = "7a6e69e"
COLD_PASS2_COMMIT = "8079f93"

PASS1_FIELDS = ["kind", "archetypes", "self_perceived", "audience_perceived",
                "emotion", "goal", "goal_status", "agency_role", "embodies",
                "moral_coloring"]
PASS2_FIELDS = ["weight_proportionality", "characterization_consistency"]
KIND_VALUES = {"no_confident_archetype", "functional_role_only", "ordinary_reaction"}
DRAFT_FIELD = "causal_integrity (weight_proportionality + characterization_consistency)"

# Report-level identity merges (author decision D5, 2026-10-04). Applied
# for display in both views; the stored data keeps the separate names.
ALIASES = {"YOUNG JOHN": "JOHN", "YOUNG CHEYENNE": "CHEYENNE"}
ALIAS_NOTE = ("JOHN and YOUNG JOHN, and CHEYENNE and YOUNG CHEYENNE, are each "
              "shown as one character. The pipeline tracked the younger "
              "versions in the flashbacks as separate characters "
              "(FOG_COLD_RUN_FINDINGS.md finding 21).")

COLD_LABEL = ("Cold output: the AI's character-change judgments with no "
              "human correction. (Some character tags it built on had already "
              "been reviewed.)")


# --- loading ---------------------------------------------------------------

def load_snapshot(commit):
    return git_snapshots.show_json(commit, "fog_tagged.json")


def load_current():
    with open(TAGGED, encoding="utf-8") as f:
        return json.load(f)


def entries(data):
    """{(beat_id, character): per_character dict}"""
    return {(b["beat_id"], p["character"]): p
            for b in data["beats"].values() for p in b["per_character"]}


def ci_value(p, field):
    return (p.get("causal_integrity") or {}).get(field)


# --- cold view -------------------------------------------------------------

def build_cold(p1, p2):
    """Pass 1 fields from p1, Pass 2 fields from p2, keyed by p1's entries
    (the cold Pass 1 entity names). Entries that exist only in p2 were
    added or renamed by a human before the Pass 2 run; their Pass 2 draft
    is carried onto the matching cold entity where a log entry names the
    rename (see entity_renames)."""
    cold = copy.deepcopy(p1)
    P2 = entries(p2)
    renames = entity_renames(load_current())
    for b in cold["beats"].values():
        for p in b["per_character"]:
            key = (b["beat_id"], p["character"])
            src = P2.get(key) or P2.get((b["beat_id"], renames.get(key)))
            ci = p.setdefault("causal_integrity", None)
            if src is not None and src.get("causal_integrity") and ci is not None:
                for f in PASS2_FIELDS:
                    ci[f] = src["causal_integrity"][f]
    return cold


def entity_renames(cur):
    """{(beat_id, cold name): reviewed name} from the log's 'character'
    entries (finding 6 merges, finding 13 fix)."""
    return {(e["beat_id"], e["llm_value"]): e["human_value"]
            for e in cur["corrections"] if e["field_name"] == "character"}


# --- replay audit ----------------------------------------------------------

def parse_logged(v):
    """Some llm_values are Python-repr strings of lists ("['a', 'b']")."""
    if isinstance(v, str) and v.startswith("[") and v.endswith("]"):
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            return v
    return v


def replay(cur):
    """Reverse every non-draft, non-plot-fact log entry. Returns the
    replayed data plus the set of keys each known category touched."""
    rev = copy.deepcopy(cur)
    beats = rev["beats"]
    touched = defaultdict(set)
    for i in range(len(rev["corrections"]) - 1, -1, -1):
        e = rev["corrections"][i]
        f, log_no = e["field_name"], i + 1
        if f in (DRAFT_FIELD, "plot_fact"):
            continue
        b = beats[e["beat_id"]]
        pcs = {p["character"]: p for p in b["per_character"]}
        if f == "character":
            if "and removed" in e["notes"]:
                # The cold entry was deleted in a merge without its field
                # values being logged; the replay cannot recover it.
                touched["merge_removed_entry"].add((e["beat_id"], e["llm_value"]))
                touched["merge_removed_entry"].add((e["beat_id"], e["human_value"]))
                continue
            p = pcs[e["human_value"]]
            p["character"] = e["llm_value"]
            touched["entity_rename"].add((e["beat_id"], e["llm_value"]))
            continue
        p = pcs.get(e.get("character"))
        if p is None:
            sys.exit(f"ABORT: log {log_no} names {e.get('character')} on "
                     f"{e['beat_id']}, which has no such entry")
        old = parse_logged(e["llm_value"])
        key = (e["beat_id"], e["character"])
        if old is None and f == "archetypes":
            # archetypes is always a list on a real entry; None means the
            # entry did not exist before this log (a human-added entry).
            touched["human_added_entry"].add(key)
        if f in PASS2_FIELDS:
            if log_no <= 720 and f == "weight_proportionality":
                touched["finding4_wp_reset"].add(key)
            p["causal_integrity"][f] = old
        elif f == "archetypes" and isinstance(old, str) and old in KIND_VALUES:
            # Log recorded the old kind under 'archetypes'.
            p["kind"], p["archetypes"] = old, []
            touched["kind_logged_as_archetypes"].add(key)
        elif f == "archetypes":
            p["archetypes"] = old
            if old:  # restoring a real archetype means kind was None
                if p.get("kind") is not None:
                    touched["unlogged_kind_change"].add(key)
                p["kind"] = None
        elif f in PASS1_FIELDS:
            p[f] = old
        else:
            sys.exit(f"ABORT: log {log_no} has unhandled field {f!r}")
    # Entries a human added outright have no cold counterpart.
    for b in beats.values():
        b["per_character"] = [p for p in b["per_character"]
                              if (b["beat_id"], p["character"]) not in touched["human_added_entry"]]
    return rev, touched


def diff_entries(a, b, fields, in_ci):
    A, B = entries(a), entries(b)
    out = []
    for k in sorted(set(A) | set(B), key=lambda k: (beat_id_sort_key(k[0]), k[1])):
        if k not in A or k not in B:
            out.append((k, "<entry>", k in A, k in B))
            continue
        for f in fields:
            va = ci_value(A[k], f) if in_ci else A[k].get(f)
            vb = ci_value(B[k], f) if in_ci else B[k].get(f)
            if va != vb:
                out.append((k, f, va, vb))
    return out


def audit(cur, p1, p2):
    """Every replay-vs-snapshot difference must belong to a named category."""
    rev, touched = replay(cur)
    renamed_to = {(b, new) for (b, _old), new in entity_renames(cur).items()}

    def explained(d):
        k, f = d[0], d[1]
        if k in touched["merge_removed_entry"]:
            return True
        if f == "<entry>":
            # 8079f93 already carries the reviewed entity name, and the
            # human-added entry, both made before the Pass 2 run.
            return (k in renamed_to or k in touched["entity_rename"]
                    or k in touched["human_added_entry"])
        return f == "weight_proportionality" and k in touched["finding4_wp_reset"]

    unexplained = [("pass1", d) for d in diff_entries(rev, p1, PASS1_FIELDS, False)
                   if not (d[0] in touched["merge_removed_entry"])]
    unexplained += [("pass2", d) for d in diff_entries(rev, p2, PASS2_FIELDS, True)
                    if not explained(d)]
    summary = {cat: len(keys) for cat, keys in sorted(touched.items())}
    return unexplained, summary


# --- line index ------------------------------------------------------------

PAREN_RE = re.compile(r"\([^()]*\)")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\f", " ")).strip()


def page_tables(lines):
    """PDF page of each 1-indexed line (a form feed opens a new page), and
    {pdf page: printed page} read from the 'N.' header line."""
    page_of, pg = [], 1
    for line in lines:
        pg += line.count("\f")
        page_of.append(pg)
    printed = {}
    for i, line in enumerate(lines):
        m = re.match(r"^\f?\s*(\d+)\.\s*$", line)
        if m and page_of[i] not in printed:
            printed[page_of[i]] = int(m.group(1))
    return page_of, printed


def printed_page(pdf_page, printed):
    if pdf_page in printed:
        return printed[pdf_page]
    # Unnumbered pages: the title page (pdf 1) has none; pdf 2 is printed
    # page 1 by screenplay convention. Anything else is reported.
    if pdf_page == 1:
        return None
    if pdf_page == 2 and printed.get(3) == 2:
        return 1
    raise ValueError(f"PDF page {pdf_page} has no printed page number")


def build_line_index(cur):
    with open(FULL_TXT, encoding="utf-8") as f:
        lines = f.read().split("\n")
    page_of, printed = page_tables(lines)

    chars, owner = [], []
    for n, line in enumerate(lines, 1):
        t = norm(line)
        if not t:
            continue
        for ch in t + " ":
            chars.append(ch)
            owner.append(n)
    blob = "".join(chars)

    def find(seg, start):
        j = blob.find(seg, start)
        return j

    index, cursor, failures, pending = {}, 0, [], []
    unmatched = {}
    for bid in sorted(cur["beats"], key=beat_id_sort_key):
        turns = cur["beats"][bid]["source_evidence"]["turns"]
        first = last = None
        missed = []
        for ti, t in enumerate(turns):
            text = norm(t["text"])
            segs = [s.strip() for s in PAREN_RE.split(text)]
            segs += [p.strip("() ") for p in PAREN_RE.findall(text)]
            hit = False
            for s in sorted(set(x for x in segs if len(x) >= 2), key=text.find):
                j = find(s, cursor)
                # Short fragments ("Hey!") only count close to the cursor.
                limit = 600 if len(s) < 12 else 20000
                if j < 0 or j - cursor > limit:
                    continue
                a, z = owner[j], owner[j + len(s) - 1]
                first = a if first is None else min(first, a)
                last = z if last is None else max(last, z)
                cursor = j
                hit = True
            if not hit:
                missed.append(ti)
        if missed:
            unmatched[bid] = {"turns": missed, "of": len(turns)}
        if first is None:
            if turns:
                pending.append(bid)
            continue
        # extend upward to a speaker cue directly above the first line
        if turns and turns[0]["kind"] == "dialogue":
            k = first - 1
            while k >= 1 and not norm(lines[k - 1]):
                k -= 1
            if k >= 1 and turns[0]["speaker"] and norm(lines[k - 1]).startswith(turns[0]["speaker"]):
                first = k
        index[bid] = {"first_line": first, "last_line": last, "placement": "matched"}
        if missed:
            index[bid]["unmatched_turns"] = missed

    # Beats whose text can't be matched (dual-dialogue columns interleave
    # two speakers line by line) are bracketed between their neighbours.
    order = sorted(cur["beats"], key=beat_id_sort_key)
    for bid in pending:
        i = order.index(bid)
        prev = next((index[b] for b in reversed(order[:i]) if b in index
                     and index[b]["placement"] == "matched"), None)
        nxt = next((index[b] for b in order[i + 1:] if b in index
                    and index[b]["placement"] == "matched"), None)
        if prev is None or nxt is None or nxt["first_line"] - prev["last_line"] < 2:
            failures.append(bid)
            continue
        index[bid] = {"first_line": prev["last_line"] + 1, "last_line": nxt["first_line"] - 1,
                      "placement": "bracketed"}

    # A beat whose first or last turn did not match (garbled extraction,
    # e.g. finding 12's Creed line) is extended into the gap up to its
    # neighbours, so its range still holds that text.
    def is_blank_or_header(n):
        t = lines[n - 1].replace("\f", "").strip()
        return not t or re.match(r"^\d+\.$", t)
    for i, bid in enumerate(order):
        rec = index.get(bid)
        if not rec or "unmatched_turns" not in rec:
            continue
        n_turns = len(cur["beats"][bid]["source_evidence"]["turns"])
        if 0 in rec["unmatched_turns"]:
            rec["matched_first_line"] = rec["first_line"]
            prev = next((index[b]["last_line"] for b in reversed(order[:i]) if b in index), 0)
            k = prev + 1
            while k < rec["first_line"] and is_blank_or_header(k):
                k += 1
            rec["first_line"] = min(rec["first_line"], k)
            rec["placement"] = "extended"
        if n_turns - 1 in rec["unmatched_turns"]:
            nxt = next((index[b]["first_line"] for b in order[i + 1:] if b in index), len(lines) + 1)
            k = nxt - 1
            while k > rec["last_line"] and is_blank_or_header(k):
                k -= 1
            rec["last_line"] = max(rec["last_line"], k)
            rec["placement"] = "extended"

    # Matched ranges must run in story order.
    placed = [(b, index[b]) for b in order if b in index]
    for (a, ra), (b, rb) in zip(placed, placed[1:]):
        if rb["first_line"] < ra["first_line"]:
            failures.append(f"{b} starts before {a}")
    for rec in index.values():
        pp = sorted({page_of[rec["first_line"] - 1], page_of[rec["last_line"] - 1]})
        rec["pdf_pages"] = pp
        rec["printed_pages"] = [printed_page(p, printed) for p in pp]
    return index, failures, page_of, printed, unmatched


# Ranges verified by hand against the PDF (demo_prototype/build_pete_card.py).
CHECKS = {"scene122_beat1": (3953, 3980)}


# --- report model ----------------------------------------------------------

def view_entries(data):
    out = []
    for bid in sorted(data["beats"], key=beat_id_sort_key):
        b = data["beats"][bid]
        for p in b["per_character"]:
            ci = p.get("causal_integrity") or {}
            out.append({
                "beat_id": bid,
                "character": p["character"],
                "display_character": ALIASES.get(p["character"], p["character"]),
                "kind": p["kind"],
                "archetypes": p["archetypes"],
                "characterization_consistency": ci.get("characterization_consistency"),
                "weight_proportionality": ci.get("weight_proportionality"),
                "agency_alignment": ci.get("agency_alignment"),
                # The model's stored read of the moment. No field holds a
                # written rationale for the archetype choice itself.
                "self_perceived": p.get("self_perceived") or [],
                "audience_perceived": p.get("audience_perceived") or [],
                "emotion": p.get("emotion") or [],
                "goal": p.get("goal"),
                "embodies": p.get("embodies"),
            })
    return out


def build_model(cur, cold, line_index, audit_summary):
    views = {"cold": view_entries(cold), "reviewed": view_entries(cur)}
    counts = Counter(e["display_character"] for e in views["reviewed"])
    beats = {}
    for bid in sorted(cur["beats"], key=beat_id_sort_key):
        b = cur["beats"][bid]
        li = line_index.get(bid)
        beats[bid] = {"scene_id": b["scene_id"], **(li or {})}
    review_status = {}
    for i, e in enumerate(cur["corrections"], 1):
        if e["field_name"] in ("archetypes", "kind"):
            review_status.setdefault(f"{e['beat_id']}|{e.get('character')}", []).append(i)
    return {
        "script": cur["script_version"]["title"],
        "built_from": {
            "reviewed": "fog_tagged.json (working tree)",
            "cold_pass1": COLD_PASS1_COMMIT,
            "cold_pass2": COLD_PASS2_COMMIT,
            "corrections_log_entries": len(cur["corrections"]),
            "replay_audit": audit_summary,
        },
        "labels": {"cold": COLD_LABEL, "aliases": ALIAS_NOTE},
        "aliases": ALIASES,
        # [beat_id, cold name, reviewed name] from the log's 'character'
        # entries. The cold view keeps the cold names; the report only
        # uses this so a rename is not counted as a changed call.
        "entity_renames": [[b, old, new] for (b, old), new
                           in sorted(entity_renames(cur).items(),
                                     key=lambda kv: beat_id_sort_key(kv[0][0]))],
        "character_beat_counts": dict(counts.most_common()),
        "beats": beats,
        "views": views,
        "archetype_log_entries": review_status,
    }


def main():
    cur = load_current()
    p1 = load_snapshot(COLD_PASS1_COMMIT)
    p2 = load_snapshot(COLD_PASS2_COMMIT)

    unexplained, summary = audit(cur, p1, p2)
    print("Replay audit, known categories (entries touched):")
    for cat, n in summary.items():
        print(f"  {cat}: {n}")
    if unexplained:
        for side, d in unexplained[:20]:
            print("  UNEXPLAINED", side, d)
        sys.exit(f"ABORT: {len(unexplained)} unexplained replay differences")
    print("  0 unexplained differences")

    cold = build_cold(p1, p2)

    line_index, failures, page_of, printed, unmatched = build_line_index(cur)
    if failures:
        sys.exit(f"ABORT: {len(failures)} beats could not be placed in fog_full.txt: {failures[:10]}")
    with open(LINE_INDEX_OUT, "w", encoding="utf-8") as f:
        json.dump({"source": "fog_full.txt",
                   "page_rule": "PDF page = 1 + form feeds before the line; printed page "
                                "= the 'N.' header on that PDF page (pdf 2 = printed 1)",
                   "beats": line_index}, f, ensure_ascii=False, indent=1)
    empty = sum(1 for b in cur["beats"].values() if not b["source_evidence"]["turns"])
    bracketed = [b for b, r in line_index.items() if r["placement"] == "bracketed"]
    print(f"Line index: beats with an unmatched turn: {len(unmatched)}")
    for b, u in unmatched.items():
        print(f"    {b}: turn(s) {u['turns']} of {u['of']} -> {line_index.get(b, {}).get('placement')}")
    print(f"Line index: bracketed (not matched) beats: {bracketed}")
    for bid, (a, z) in CHECKS.items():
        r = line_index[bid]
        if (r["first_line"], r["last_line"]) != (a, z):
            sys.exit(f"ABORT: {bid} placed at {r['first_line']}-{r['last_line']}, expected {a}-{z}")
    print(f"Line index: hand-verified ranges match: {list(CHECKS)}")
    print(f"Line index: {len(line_index)} beats placed, {empty} beats with no turns, "
          f"{len(failures)} failures -> {os.path.basename(LINE_INDEX_OUT)}")

    model = build_model(cur, cold, line_index, summary)
    with open(MODEL_OUT, "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=1)
    for v in ("cold", "reviewed"):
        es = model["views"][v]
        print(f"View {v}: {len(es)} entries, {sum(len(e['archetypes']) for e in es)} archetype tags, "
              f"kinds {dict(Counter(e['kind'] for e in es))}")
    print(f"Model -> {os.path.basename(MODEL_OUT)}")


if __name__ == "__main__":
    main()
