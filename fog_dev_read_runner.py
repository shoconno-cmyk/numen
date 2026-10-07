"""
fog_dev_read_runner.py -- section 1 of the story report, the development
read, for Full of Grace: title, genre, a logline, and a full synopsis.

- Title: taken by code from the script's title page (page 1 of
  fog_full.txt), never generated.
- Genre, logline and synopsis: written by the model in one call, from the
  script text itself (fog_full.txt, page 2 on). No plot facts, tags, review
  data or corrections are sent. The title page is not sent either (it
  carries the writer's name and email, which the read doesn't need).
- The logline is 1-2 sentences (premise, protagonist, stakes; no ending).
  The synopsis is 3-4 paragraphs including the ending; the report shows it
  collapsed under "Read the full synopsis".
- Every response goes through report_guard.py as report-voice text (kind
  "summary": banned words, praise and critique words, pipeline terms, no
  citations or page numbers, every quote verbatim in fog_full.txt), plus
  the shape checks here. Length is a soft target: going over the prompt's
  target logs a "length over target" note, and only a wide malfunction
  bound rejects. A failing response is rejected, never
  loosely accepted: one retry with the list of violations; if that fails
  too, the read falls back to the title plus whichever of genre and
  logline passed, and the item is logged to report_guard_log.jsonl.

Model: claude-sonnet-5, the pipeline's model (author decision D4), at the
pipeline's pricing ($2 / $10 per million tokens, pass2_orchestration.py;
confirmed against the Claude API model table, cached 2026-09-25). Thinking
is left at the model default (adaptive), as in the pipeline; max_tokens
leaves room for it. No prompt caching: the only repeat is an immediate
retry, and a cache write would cost more on the usual single call.

Response format: structured outputs (output_config.format, a JSON schema
with exactly "genre", "logline" and "synopsis"), so the reply is always
parseable JSON. Short quotations are allowed (prompt v6 on); each one must
match fog_full.txt word for word.

Modes (run from the repo root):
  python fog_dev_read_runner.py --dry-run   # free: full prompt (script text
                                            # truncated in the printout),
                                            # token count, cost estimate
  python fog_dev_read_runner.py --run       # billed: at most 2 calls
  python fog_dev_read_runner.py --rerun     # billed: as --run when an earlier
                                            # result exists; the earlier files
                                            # are archived (never deleted) when
                                            # the new result is stored
  python fog_dev_read_runner.py --accept-saved N --reason "..."
                                            # free: re-checks saved attempt N in
                                            # fog_dev_read_call.json with the
                                            # current rules; stores it only if it
                                            # passes every check, and logs why

--run needs ANTHROPIC_API_KEY in the environment of the shell that runs
it. Before calling, it counts the exact input tokens (count_tokens, free)
and aborts if the worst case for both calls exceeds COST_CAP. During a run
each raw response and its usage are written to fog_dev_read_call.new.json
BEFORE parsing, so a rejected or truncated response is never lost. Only
when the new result is stored are the earlier fog_dev_read.json and
fog_dev_read_call.json moved into fog_dev_read_archive/ and the new files
put in their place; if a run stops partway, the earlier result stays live
and the partial record stays in fog_dev_read_call.new.json for inspection.
report.py renders fog_dev_read.json as section 1.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import report_guard  # noqa: E402
from pass2_orchestration import _SONNET_5_INPUT_PER_MTOK, _SONNET_5_OUTPUT_PER_MTOK  # noqa: E402

FULL_TXT = os.path.join(ROOT, "fog_full.txt")
CALL_PATH = os.path.join(ROOT, "fog_dev_read_call.json")
NEW_CALL_PATH = os.path.join(ROOT, "fog_dev_read_call.new.json")
OUT_PATH = os.path.join(ROOT, "fog_dev_read.json")
ARCHIVE_DIR = os.path.join(ROOT, "fog_dev_read_archive")
# 1: first run 2026-10-05 (archived); 2: no quotations, under 110 words,
# structured output; 3: actions exactly as shown, no stated beliefs or
# intentions unless the script shows them, complete grammatical sentences;
# 4: "at most five sentences" (hard limit 70-170); 5: genre + logline +
# full synopsis in one call (author decision 2026-10-05); 2026-10-06: the
# synopsis target became about 300-380 words, the hard limit 250-500.
# 6 (2026-10-06): short quotations allowed (each verified word for word);
# length is a soft target, with only a wide malfunction bound enforced.
# The quotation line ("You may quote the script briefly. Keep each
# quotation short and copy it word for word.") was drafted by Claude Code
# and approved by the author on 2026-10-06.
# Each run saves the exact prompt it sent to ARCHIVE_DIR
# (fog_dev_read_prompt.v{N}.{system sha256[:8]}.json), and the result names
# the version that produced its text (generated_by_prompt_version), which
# can differ from PROMPT_VERSION once the prompt moves on.
PROMPT_VERSION = 6
MODEL = "claude-sonnet-5"
MAX_TOKENS = 16000
MAX_CALLS = 2                 # first attempt + one retry
COST_CAP = 2.00
GENRE_MAX_WORDS = 6
# Length (author, 2026-10-06): the prompt's targets are soft. Going over one
# logs a "length over target" note, never a rejection; only the wide
# malfunction bounds reject.
LOGLINE_BOUNDS = (8, 120)              # words
SYNOPSIS_BOUNDS = (100, 1000)          # words
LOGLINE_TARGET_SENTENCES = 2           # the prompt asks for one or two sentences
SYNOPSIS_TARGET_WORDS = (300, 380)     # the prompt asks for about 300-380
SYNOPSIS_PARAGRAPHS_ASKED = (3, 4)   # asked for, reported, not enforced
FIELDS = ("genre", "logline", "synopsis")

SYSTEM = """You are reading a feature screenplay for a film development team. You write the development read that opens a report on the script: its genre, a logline, and a full synopsis, the way a reader summarizes a script for an executive.

Rules for the logline:
- One or two sentences.
- Give the premise, the protagonist, and the stakes. Do not reveal the ending.

Rules for the synopsis:
- Three or four paragraphs, about 300 to 380 words in all. Separate the paragraphs with a blank line.
- Describe the story's premise, its main characters, its key turns, and its ending. Include the ending.

Rules for both the logline and the synopsis:
- State only what happens on the page. Do not infer motives or hidden meanings beyond what the script shows.
- Describe actions exactly as the page shows them. Do not characterize an act as accidental, intentional, mistaken, or justified unless the script states it or unmistakably shows it through action.
- Do not state what a character believes or intends unless the script states it or unmistakably shows it through action.
- No evaluation in either direction: do not praise or criticize the script, its writing, or its story, and make no recommendation.
- Do not suggest changes or tell anyone what to write.
- Refer to characters by the names the script uses, in normal capitalization.
- Do not give page numbers, line numbers, or scene numbers.
- You may quote the script briefly. Keep each quotation short and copy it word for word.
- Write complete, grammatical sentences.

Rules for the genre: one short phrase of one to five words, as a reader would put it on a coverage cover page.

Give the genre, the logline, and the synopsis in the response format provided."""

# Structured outputs: the reply is constrained to this schema.
OUTPUT_CONFIG = {"format": {"type": "json_schema", "schema": {
    "type": "object",
    "properties": {k: {"type": "string"} for k in FIELDS},
    "required": list(FIELDS),
    "additionalProperties": False,
}}}

USER_HEAD = ("Here is the screenplay, as text extracted from the PDF with its layout kept. "
             "The title page is left out.\n\n<screenplay>\n")
USER_TAIL = "\n</screenplay>"
RETRY_NOTE = ("\n\nAn earlier response to this request was rejected by the report's checks for these "
              "reasons:\n{violations}\nWrite a new response that follows every rule above.")


# --- inputs -------------------------------------------------------------------

def read_script():
    with open(FULL_TXT, encoding="utf-8") as f:
        return f.read()


def extract_title(text=None):
    """The title from the title page: the first non-empty line of page 1,
    above "Written by". Returns (title as printed, title for display)."""
    text = read_script() if text is None else text
    page1 = [l.strip() for l in text.split("\f")[0].split("\n")]
    lines = [l for l in page1 if l]
    if not lines or "written by" not in [l.lower() for l in lines]:
        raise ValueError(f"title page not in the expected shape: {lines[:4]}")
    stop = [l.lower() for l in lines].index("written by")
    printed = " ".join(lines[:stop])
    if not printed or not printed.isupper():
        raise ValueError(f"unexpected title line(s): {lines[:stop]}")
    small = {"of", "a", "an", "the", "and", "or", "in", "on", "at", "to", "for"}
    words = printed.lower().split()
    display = " ".join(w if (i and w in small) else w.capitalize() for i, w in enumerate(words))
    return printed, display


def script_body(text=None):
    """The script from page 2 on, exactly as extracted (title page left out)."""
    text = read_script() if text is None else text
    return text.split("\f", 1)[1]


def build_user(body, violations=None):
    msg = USER_HEAD + body + USER_TAIL
    if violations:
        msg += RETRY_NOTE.format(violations="\n".join(f"- {v}" for v in violations))
    return msg


def paragraphs(text):
    return [p.strip() for p in text.replace("\r\n", "\n").split("\n\n") if p.strip()]


# --- cost -------------------------------------------------------------------------

def cost_of(input_tokens, output_tokens):
    return input_tokens / 1e6 * _SONNET_5_INPUT_PER_MTOK + output_tokens / 1e6 * _SONNET_5_OUTPUT_PER_MTOK


def worst_case(input_tokens):
    # Both calls at full input price; the retry also carries the violation note
    # (allow 500 tokens); every call spends its whole max_tokens.
    return cost_of(input_tokens, MAX_TOKENS) + cost_of(input_tokens + 500, MAX_TOKENS)


def count_input_tokens(user):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    r = client.messages.count_tokens(model=MODEL, system=SYSTEM, output_config=OUTPUT_CONFIG,
                                     messages=[{"role": "user", "content": user}])
    return r.input_tokens


# --- checks -------------------------------------------------------------------------

def check_response(raw, stop_reason, full_lines):
    """(parsed dict or None, all violations, {field: its own violations})."""
    if stop_reason != "end_turn":
        v = [f"[malformed] stop_reason {stop_reason!r}, expected 'end_turn'"]
        return None, v, {k: v for k in FIELDS}
    try:
        obj = json.loads(raw.strip())
    except json.JSONDecodeError as ex:
        v = [f"[malformed] response is not a JSON object ({ex.msg})"]
        return None, v, {k: v for k in FIELDS}
    if not isinstance(obj, dict) or set(obj) != set(FIELDS) or not all(isinstance(obj[k], str) for k in obj):
        v = ['[malformed] expected exactly {"genre": string, "logline": string, "synopsis": string}']
        return None, v, {k: v for k in FIELDS}
    parsed = {k: obj[k].strip() for k in FIELDS}
    per = {}
    for k in FIELDS:
        per[k] = [f"[{k}] {v}" for v in report_guard.check_text(parsed[k], "summary", full_lines=full_lines)]
    g = parsed["genre"]
    if not g or len(g.split()) > GENRE_MAX_WORDS or "\n" in g:
        per["genre"].append(f"[genre] [shape] one phrase of at most {GENRE_MAX_WORDS} words")
    n = len(parsed["logline"].split())
    if not LOGLINE_BOUNDS[0] <= n <= LOGLINE_BOUNDS[1]:
        per["logline"].append(f"[logline] [length] {n} words; outside the malfunction bound "
                              f"{LOGLINE_BOUNDS[0]}-{LOGLINE_BOUNDS[1]}")
    if "\n" in parsed["logline"]:
        per["logline"].append("[logline] [shape] must be one paragraph")
    n = len(parsed["synopsis"].split())
    if not SYNOPSIS_BOUNDS[0] <= n <= SYNOPSIS_BOUNDS[1]:
        per["synopsis"].append(f"[synopsis] [length] {n} words; outside the malfunction bound "
                               f"{SYNOPSIS_BOUNDS[0]}-{SYNOPSIS_BOUNDS[1]}")
    return parsed, [v for k in FIELDS for v in per[k]], per


def sentence_count(text):
    """Approximate: splits after . ! or ? (and any closing quote or bracket)
    when a capital letter follows. Used only for the soft-target note."""
    return len([x for x in re.split(r'(?<=[.!?])["”’)]?\s+(?=["“‘(]?[A-Z])', text.strip()) if x])


def length_notes(parsed):
    """Soft targets: a note for each part over its target, never a rejection."""
    notes = []
    if parsed.get("logline"):
        n = sentence_count(parsed["logline"])
        if n > LOGLINE_TARGET_SENTENCES:
            notes.append(f"[logline] length over target: {n} sentences; the prompt asks for one or two")
    if parsed.get("synopsis"):
        n = len(parsed["synopsis"].split())
        if n > SYNOPSIS_TARGET_WORDS[1]:
            notes.append(f"[synopsis] length over target: {n} words; the prompt asks for about "
                         f"{SYNOPSIS_TARGET_WORDS[0]}-{SYNOPSIS_TARGET_WORDS[1]}")
    return notes


def log_length_notes(notes, attempt_no, prompt_version):
    if notes:
        with open(report_guard.GUARD_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"item": "fog development read", "kind": "summary", "event": "length over target",
                                "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                "attempt": attempt_no, "prompt_version": prompt_version, "notes": notes},
                               ensure_ascii=False) + "\n")


# --- generating prompt ---------------------------------------------------------------

def prompt_file_name(version, system_sha):
    return f"fog_dev_read_prompt.v{version}.{system_sha[:8]}.json"


def archive_prompt():
    """Save the exact prompt this version sends (write once; an existing file
    must match). Returns its path, relative to the repo root when under it."""
    sha = hashlib.sha256(SYSTEM.encode("utf-8")).hexdigest()
    rec = {"prompt_version": PROMPT_VERSION, "model": MODEL, "source": "fog_dev_read_runner.py at run time",
           "system_sha256": sha, "system": SYSTEM, "user_head": USER_HEAD, "user_tail": USER_TAIL,
           "retry_note": RETRY_NOTE, "output_config": OUTPUT_CONFIG,
           "user_message": "user_head + fog_full.txt page 2 on + user_tail; on a retry, + retry_note "
                           "filled with the previous attempt's violations"}
    path = os.path.join(ARCHIVE_DIR, prompt_file_name(PROMPT_VERSION, sha))
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        if any(old.get(k) != rec[k] for k in ("prompt_version", "system", "user_head", "user_tail", "retry_note")):
            sys.exit(f"ABORT: {path} exists with a different prompt; not overwriting an archive")
    else:
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)
    rel = os.path.relpath(path, ROOT) if os.path.splitdrive(path)[0] == os.path.splitdrive(ROOT)[0] else path
    return path if rel.startswith("..") else rel.replace("\\", "/")


def check_generating_prompt(d):
    """The record's generating prompt version must match the archived prompt
    file it points to, and the call record. ValueError otherwise."""
    v, p = d.get("generated_by_prompt_version"), d.get("generating_prompt_file")
    if v is None or not p:
        raise ValueError("record must name both generated_by_prompt_version and generating_prompt_file")
    path = os.path.join(ROOT, p)
    if not os.path.exists(path):
        raise ValueError(f"generating prompt file {p} is missing")
    with open(path, encoding="utf-8") as f:
        pf = json.load(f)
    if pf.get("prompt_version") != v or d.get("prompt_version") != v:
        raise ValueError(f"record says prompt v{v} (prompt_version {d.get('prompt_version')}); "
                         f"{p} is v{pf.get('prompt_version')}")
    if hashlib.sha256(pf["system"].encode("utf-8")).hexdigest() != pf.get("system_sha256"):
        raise ValueError(f"{p}: system prompt does not match its own sha256")
    with open(CALL_PATH, encoding="utf-8") as f:
        call = json.load(f)
    if (call.get("prompt_version"), call.get("system_sha256")) != (v, pf["system_sha256"]):
        raise ValueError(f"call record (v{call.get('prompt_version')}) does not match {p}")


# --- formatting repair ---------------------------------------------------------------

def _compact(text):
    return re.sub(r"\s+", "", text)


def check_repair(original, old, new):
    """The one edit allowed to stored AI text: a formatting repair. `old`
    must occur exactly once in the AI's original; `new` may differ from it
    only by whitespace (e.g. a restored paragraph break) and at most one
    removed stray character; and every word must be unchanged except the one
    that loses that character. Returns the repaired text; ValueError otherwise."""
    if original.count(old) != 1:
        raise ValueError(f"repair: {old!r} occurs {original.count(old)} times in the AI text, not once")
    a, b = _compact(old), _compact(new)
    if not (a == b or (len(a) == len(b) + 1 and any(a[:i] + a[i + 1:] == b for i in range(len(a))))):
        raise ValueError(f"repair: {old!r} -> {new!r} is more than whitespace plus one removed character")
    repaired = original.replace(old, new)
    w0, w1 = original.split(), repaired.split()
    changed = [(x, y) for x, y in zip(w0, w1) if x != y]
    # The one character removed must be a stray glued on after a word's
    # closing punctuation ("silent.a" -> "silent."), never a letter of a word.
    if len(w0) != len(w1) or len(changed) > 1 or (changed and not (
            changed[0][0][:-1] == changed[0][1] and changed[0][1][-1:] in tuple(".!?,;:\"”’)"))):
        raise ValueError(f"repair: words changed: {changed}")
    return repaired


def apply_formatting_repair(field, old, new, note):
    """Store a formatting repair of the accepted AI text, keeping the AI's
    original verbatim beside it, and log it. No API call."""
    with open(OUT_PATH, encoding="utf-8") as f:
        d = json.load(f)
    if d.get("formatting_repair"):
        sys.exit("ABORT: a formatting repair is already stored; not stacking another")
    with open(CALL_PATH, encoding="utf-8") as f:
        saved = next(a for a in json.load(f)["attempts"] if a["attempt"] == d["accepted_attempt"])
    original = json.loads(saved["raw_text"])[field].strip()
    if d[field] != original:
        sys.exit(f"ABORT: stored {field} is not the saved AI text, word for word")
    repaired = check_repair(original, old, new)
    d[field] = repaired
    d["formatting_repair"] = {"field": field, "date": datetime.date.today().isoformat(), "old": old, "new": new,
                              "note": note, "ai_original": original}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    with open(report_guard.GUARD_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"item": "fog development read", "kind": "summary", "event": "formatting repair",
                            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "field": field, "old": old, "new": new, "note": note,
                            "attempt": d["accepted_attempt"]}, ensure_ascii=False) + "\n")
    return d


def describe(parsed):
    """Word and paragraph counts, for the printout."""
    if not parsed:
        return "unparsed"
    return (f"logline {len(parsed['logline'].split())} words; synopsis {len(parsed['synopsis'].split())} words "
            f"in {len(paragraphs(parsed['synopsis']))} paragraph(s)")


# --- modes ----------------------------------------------------------------------------

def preflight(verbose=True):
    text = read_script()
    printed, display = extract_title(text)
    body = script_body(text)
    user = build_user(body)
    key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    n_in = count_input_tokens(user) if key else None
    est = n_in if n_in is not None else int(len(SYSTEM + user) / 3.0)
    if verbose:
        lines = body.split("\n")
        shown = "\n".join(lines[:20]) + f"\n\n[... {len(lines) - 40} lines omitted from this printout; " \
            "the call sends the full text ...]\n\n" + "\n".join(lines[-20:])
        print("=" * 78)
        print(f"TITLE (code, from the title page): printed {printed!r} -> shown as {display!r}")
        print("=" * 78)
        print(f"MODEL {MODEL}   max_tokens {MAX_TOKENS}   calls: at most {MAX_CALLS} (1 + one retry)   "
              f"prompt version {PROMPT_VERSION}")
        print(f"soft targets (over -> note, not rejection): logline {LOGLINE_TARGET_SENTENCES} sentences; "
              f"synopsis about {SYNOPSIS_TARGET_WORDS[0]}-{SYNOPSIS_TARGET_WORDS[1]} words")
        print(f"malfunction bounds (reject): logline {LOGLINE_BOUNDS[0]}-{LOGLINE_BOUNDS[1]} words; synopsis "
              f"{SYNOPSIS_BOUNDS[0]}-{SYNOPSIS_BOUNDS[1]} words; genre at most {GENRE_MAX_WORDS} words")
        print("=" * 78)
        print("SYSTEM PROMPT (sent in full):\n")
        print(SYSTEM)
        print("=" * 78)
        print("USER MESSAGE (script text truncated in this printout only):\n")
        print(USER_HEAD + shown + USER_TAIL)
        print("=" * 78)
        print("OUTPUT FORMAT (structured outputs, output_config):\n")
        print(json.dumps(OUTPUT_CONFIG, indent=2))
        print("=" * 78)
        print("RETRY NOTE (appended to the user message on a retry only):")
        print(RETRY_NOTE.format(violations="- <each violation from the first attempt>"))
        print("=" * 78)
        print(f"script text sent: fog_full.txt page 2 on, {len(lines)} lines, {len(body)} characters; "
              f"title page (page 1) not sent")
        print(f"user message sha256: {hashlib.sha256(user.encode('utf-8')).hexdigest()[:16]}")
        if n_in is None:
            print(f"input tokens: ESTIMATE ~{est} (characters / 3.0; ANTHROPIC_API_KEY not set here, so no "
                  f"count_tokens call). --run counts them exactly before any billed call.")
        else:
            print(f"input tokens: {n_in} exact (count_tokens)")
        w = worst_case(est)
        typical = cost_of(est, 3500)
        print(f"pricing: ${_SONNET_5_INPUT_PER_MTOK}/M in, ${_SONNET_5_OUTPUT_PER_MTOK}/M out")
        print(f"cost: typical one call (~3,500 output tokens incl. thinking) ~${typical:.2f}; "
              f"worst case, 2 calls each using all {MAX_TOKENS} output tokens: ${w:.2f}; cap ${COST_CAP:.2f} "
              f"-> {'OK' if w <= COST_CAP else 'ABOVE CAP, --run would abort'}")
        print("=" * 78)
        earlier = [os.path.basename(p) for p in (CALL_PATH, OUT_PATH) if os.path.exists(p)]
        print("To run the billed call from your own terminal (the key stays in your shell):")
        print(f"  cd {ROOT}")
        if earlier:
            print("  python fog_dev_read_runner.py --rerun")
            print(f"(an earlier result exists: {', '.join(earlier)}; it stays live until the new result is "
                  f"stored, then moves into {os.path.basename(ARCHIVE_DIR)}/; nothing is deleted)")
        else:
            print("  python fog_dev_read_runner.py --run")
        print("(with ANTHROPIC_API_KEY set in that terminal, as for fog_plot_facts_runner.py)")
    return text, (printed, display), body, n_in


def archive_earlier():
    """Move the earlier result's files into ARCHIVE_DIR, named by the time of
    archiving. Nothing is deleted. Returns the archived paths."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    moved = []
    for p in (CALL_PATH, OUT_PATH):
        if os.path.exists(p):
            os.makedirs(ARCHIVE_DIR, exist_ok=True)
            stem, ext = os.path.splitext(os.path.basename(p))
            dest = os.path.join(ARCHIVE_DIR, f"{stem}.{stamp}{ext}")
            if os.path.exists(dest):
                sys.exit(f"ABORT: {dest} already exists; not overwriting an archive")
            os.replace(p, dest)
            moved.append(dest)
    return moved


def run(rerun=False):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ABORT: ANTHROPIC_API_KEY is not set in this shell")
    if os.path.exists(NEW_CALL_PATH):
        sys.exit(f"ABORT: {os.path.basename(NEW_CALL_PATH)} exists: an earlier run stopped partway. "
                 "Inspect it (it holds billed responses) and move it aside before running again.")
    earlier = [p for p in (CALL_PATH, OUT_PATH) if os.path.exists(p)]
    if earlier and not rerun:
        sys.exit(f"ABORT: {', '.join(os.path.basename(p) for p in earlier)} exists; a call was already made. "
                 "Inspect it, then use --rerun to run again (the earlier files are archived when the new "
                 "result is stored).")
    if rerun and not earlier:
        sys.exit("ABORT: --rerun given but there is no earlier result; use --run")
    text, (printed, display), body, n_in = preflight(verbose=False)
    w = worst_case(n_in)
    print(f"input tokens {n_in} (exact); worst case ${w:.4f}; cap ${COST_CAP:.2f}")
    if w > COST_CAP:
        sys.exit(f"ABORT: worst case ${w:.4f} exceeds the ${COST_CAP:.2f} cap; no call made")

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    full_lines = text.split("\n")
    record = {"model": MODEL, "max_tokens": MAX_TOKENS, "prompt_version": PROMPT_VERSION,
              "system_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest(), "output_config": OUTPUT_CONFIG,
              "attempts": []}
    violations, accepted, kept, total = None, None, {}, 0.0
    for attempt in range(1, MAX_CALLS + 1):
        user = build_user(body, violations)
        resp = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM,
                                      output_config=OUTPUT_CONFIG,
                                      messages=[{"role": "user", "content": user}])
        raw = "".join(b.text for b in resp.content if b.type == "text")
        u = resp.usage
        cost = cost_of(u.input_tokens, u.output_tokens)
        total += cost
        record["attempts"].append({
            "attempt": attempt,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "request_id": getattr(resp, "_request_id", None),
            "model_returned": resp.model, "stop_reason": resp.stop_reason,
            "user_sha256": hashlib.sha256(user.encode("utf-8")).hexdigest(),
            "retry_violations": violations,
            "usage": {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens},
            "cost_usd": round(cost, 4), "raw_text": raw,
        })
        # Saved before parsing, every attempt (to the .new file until stored).
        with open(NEW_CALL_PATH, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        print(f"[attempt {attempt}] in={u.input_tokens} out={u.output_tokens} stop={resp.stop_reason} "
              f"cost=${cost:.4f} -- saved {os.path.basename(NEW_CALL_PATH)}")
        parsed, violations, per = check_response(raw, resp.stop_reason, full_lines)
        print(f"[attempt {attempt}] {describe(parsed)}")
        for k in ("genre", "logline"):
            if parsed and not per[k]:
                kept[k] = parsed[k]   # the latest attempt in which this part passed
        if not violations:
            accepted = parsed
            break
        print(f"[attempt {attempt}] rejected: {violations}")

    result = {"title": display, "title_printed": printed, "title_source": "code: fog_full.txt title page",
              "genre": None, "logline": None, "synopsis": None, "model": MODEL,
              "call_file": os.path.basename(CALL_PATH), "attempts": len(record["attempts"]),
              "total_cost_usd": round(total, 4), "prompt_version": PROMPT_VERSION,
              "inputs": "fog_full.txt page 2 on only; no plot facts, tags or review data"}
    if accepted:
        result.update(accepted, source="ai" if len(record["attempts"]) == 1 else "ai_retry")
    else:
        result.update(kept, source="fallback", missing=[k for k in FIELDS if k not in kept])
        with open(report_guard.GUARD_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"item": "fog development read", "kind": "summary", "prompt_version": PROMPT_VERSION,
                                "fallback": {"kept": sorted(kept), "missing": result["missing"]},
                                "rejected": [{"attempt": a["attempt"], "raw_text": a["raw_text"]}
                                             for a in record["attempts"]],
                                "last_violations": violations}, ensure_ascii=False) + "\n")
    # Store: archive the earlier result now (never before), then put the new files in place.
    for p in archive_earlier():
        print(f"archived earlier result: {os.path.join(os.path.basename(ARCHIVE_DIR), os.path.basename(p))}")
    notes = length_notes(result)
    if notes:
        result["length_notes"] = notes
    result["generated_by_prompt_version"] = PROMPT_VERSION
    result["generating_prompt_file"] = archive_prompt()
    os.replace(NEW_CALL_PATH, CALL_PATH)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    log_length_notes(notes, len(record["attempts"]), PROMPT_VERSION)
    for n in notes:
        print(f"note: {n}")
    print(f"total cost ${total:.4f}; result ({result['source']}) -> {os.path.basename(OUT_PATH)}")
    print(json.dumps({k: result[k] for k in ("title",) + FIELDS}, indent=2, ensure_ascii=False))


def accept_saved(attempt_no, reason):
    """Re-check a saved attempt against the current guard and limits, with
    no API call. If it passes every check, store it as the result and log
    that it was accepted after a rule change; otherwise report and stop."""
    with open(CALL_PATH, encoding="utf-8") as f:
        record = json.load(f)
    with open(OUT_PATH, encoding="utf-8") as f:
        current = json.load(f)
    if not current["source"].startswith("fallback"):
        sys.exit(f"ABORT: the stored result is {current['source']!r}, not a fallback; not replacing it")
    a = next((x for x in record["attempts"] if x["attempt"] == attempt_no), None)
    if a is None:
        sys.exit(f"ABORT: no attempt {attempt_no} in {os.path.basename(CALL_PATH)}")
    text = read_script()
    printed, display = extract_title(text)
    parsed, violations, _ = check_response(a["raw_text"], a["stop_reason"], text.split("\n"))
    print(f"attempt {attempt_no}: {describe(parsed)}; violations under the current rules: {violations or 'none'}")
    if violations:
        sys.exit("NOT ACCEPTED: the saved attempt fails the current checks; result unchanged")
    result = dict(current)
    result.pop("missing", None)
    result.update(parsed, source="ai_accepted_after_rule_change", accepted_attempt=attempt_no, accepted_note=reason,
                  accepted_under={"logline_bounds": list(LOGLINE_BOUNDS), "synopsis_bounds": list(SYNOPSIS_BOUNDS),
                                  "prompt_version_of_attempt": record.get("prompt_version")})
    if (result["title_printed"], result["title"]) != (printed, display):
        sys.exit("ABORT: stored title does not match the title page")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    with open(report_guard.GUARD_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"item": "fog development read", "kind": "summary",
                            "event": "saved attempt accepted after a rule change, no API call",
                            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "attempt": attempt_no, "counts": describe(parsed),
                            "reason": reason, "previous_result": current["source"]}, ensure_ascii=False) + "\n")
    print(f"accepted: stored attempt {attempt_no} in {os.path.basename(OUT_PATH)}; logged to "
          f"{os.path.basename(report_guard.GUARD_LOG)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # the script's curly quotes survive redirection
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--rerun", action="store_true",
                   help="run when an earlier result exists; it is archived when the new result is stored")
    g.add_argument("--accept-saved", type=int, metavar="N",
                   help="re-check saved attempt N with the current rules (no API call); store it if it passes")
    ap.add_argument("--reason", help="why a saved attempt is being re-checked (required with --accept-saved)")
    args = ap.parse_args()
    if args.dry_run:
        preflight()
    elif args.accept_saved is not None:
        if not args.reason:
            ap.error("--accept-saved needs --reason")
        accept_saved(args.accept_saved, args.reason)
    else:
        run(rerun=args.rerun)
