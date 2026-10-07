"""
report_guard.py -- Stage 6, step 3: the guard on AI-generated report text.

Every piece of AI-generated text is checked here before it can appear in
the story report (STORY_REPORT_SPEC.md, "consultant, not judge"). A
failing response is rejected, never loosely accepted -- the same rule as
llm_orchestration.py. No API call is made here: the caller passes in the
function that produces text, so the guard is testable offline.

Checks (check_text):
  1. banned    -- grading words, directives and coverage verdicts
                  (word-boundary, case-insensitive; verdicts case-sensitive).
                  Quoted script text is masked first: a character can say
                  "should". Only a quote that verifies word for word against
                  fog_full.txt is masked; any other quoted text is checked
                  like normal text. "needs to" is allowed inside a question only
                  (author ruling 2026-10-05); it stays banned in statements.
  2. question  -- a question ends with "?" and doesn't open with an
                  imperative, "Consider", "Try", or "What if you".
  3. pipeline  -- no pipeline terms: snake_case enum values and enum class
                  names from tagging_schema.py, "Principle N", beat IDs,
                  "Pass 1/2", and similar internal labels.
  4. citation  -- the model cites only evidence IDs ([E1], [E2] ...), which
                  code resolves to page and line (resolve_citations). It
                  writes no page or line numbers itself. An observation
                  needs at least one citation, and every cited ID must exist.
  5. quote     -- every quoted phrase appears verbatim in the fog_full.txt
                  lines of the evidence the text cites (CLAUDE.md
                  quote-verification rule); for a summary (the development
                  read), anywhere in fog_full.txt. The match is on whole
                  words ("baptize" does not match "baptized"). Only
                  whitespace runs, straight vs. curly apostrophes, and
                  trailing , . ; : ! ? inside the quotation marks are
                  normalized.
  Report-voice text (observation, question, summary) is also checked
  against EVALUATION: praise and critique words ("no evaluation in either
  direction").

guard_generate runs the retry policy (6): one retry with the list of
violations; if that fails too, deterministic template text is used and the
item is logged. final_scan (7) checks the whole built HTML page at build
time, scoped by text type (author ruling 2026-10-05, STORY_REPORT_SPEC.md):
  report_voice -- text written in the report's own voice (observations,
                  questions, development read, plain-language wording):
                  every check applies.
  static       -- author-written copy and fixed templates: pipeline terms
                  always checked; banned words checked unless the exact
                  string is on the caller's approved list.
  ai_read      -- the AI's stored per-moment reads shown verbatim and
                  labelled as the AI's read: exempt from banned words
                  (rewording would misrepresent the AI's output); pipeline
                  terms still checked.

Tests: python -m unittest test_report_guard
"""
import html as htmlmod
import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import tagging_schema  # noqa: E402

FULL_TXT = os.path.join(ROOT, "fog_full.txt")
LINE_INDEX = os.path.join(ROOT, "fog_line_index.json")
GUARD_LOG = os.path.join(ROOT, "report_guard_log.jsonl")

# observation: report voice, needs a citation. question: report voice, the
# question rules, citations optional. summary: report voice with no
# citations (the development read); quotes are checked against the whole
# script. text: no citation rules, no evaluation list (used by the final
# scan for static copy and the AI's stored reads).
KINDS = ("observation", "question", "summary", "text")
REPORT_VOICE_KINDS = ("observation", "question", "summary")

# --- 1. banned words ----------------------------------------------------------
BANNED = {
    "grading": [r"problems?", r"flaws?", r"flawed", r"weak", r"weakness(?:es)?", r"needs work",
                r"unearned", r"fail(?:s|ed|ing)?", r"failures?", r"broken", r"mistakes?",
                r"poorly", r"grades?", r"graded", r"scores?", r"scored", r"ratings?"],
    "directive": [r"should", r"must", r"needs? to", r"fix(?:es|ed)?", r"cut", r"add"],
    "verdict": [r"recommend(?:s|ed|ation|ations)?", r"(?:I|we)(?:'|’)d pass", r"(?:I|we) would pass",
                r"pass on (?:this|the|it)"],
}
QUESTION_ALLOWED = r"needs? to"  # allowed in questions, banned in statements
BANNED_RE = [(cat, w, re.compile(rf"\b{w}\b", re.I)) for cat, ws in BANNED.items() for w in ws]

# Evaluation words, banned in report-voice text only (author request
# 2026-10-05, for the development read: "no evaluation in either
# direction"). Praise first; then critique words not already in BANNED.
# Words with an ordinary plot meaning ("moving", "rich", "dark", "slow",
# "intense", "haunted") are left out on purpose.
EVALUATION = {
    "praise": [r"compelling", r"gripping", r"powerful(?:ly)?", r"masterful(?:ly)?", r"masterpiece",
               r"brilliant(?:ly)?", r"stunning(?:ly)?", r"riveting", r"must-read", r"beautiful(?:ly)?",
               r"captivating", r"poignant(?:ly)?", r"heartbreaking", r"heart-wrenching", r"gut-wrenching",
               r"searing", r"tour[- ]de[- ]force", r"exceptional(?:ly)?", r"outstanding", r"superb(?:ly)?",
               r"excellent", r"impressive(?:ly)?", r"engaging", r"thrilling", r"electrifying",
               r"unforgettable", r"breathtaking", r"extraordinary", r"profound(?:ly)?", r"nuanced",
               r"deft(?:ly)?", r"skilful(?:ly)?", r"skillful(?:ly)?", r"expert(?:ly)?", r"well-crafted",
               r"well-written", r"well-drawn", r"page-turner", r"standout", r"award-worthy",
               r"Oscar-worthy", r"remarkabl[ey]", r"wonderful(?:ly)?", r"terrific", r"assured",
               r"accomplished", r"elegant(?:ly)?", r"evocative", r"resonant"],
    "critique": [r"clich[eé]d?", r"clich[eé]s", r"predictabl[ey]", r"derivative", r"contrived", r"tedious",
                 r"meandering", r"overwrought", r"melodramatic", r"heavy-handed", r"formulaic", r"uneven",
                 r"flat", r"thin", r"underdeveloped", r"one-dimensional", r"implausibl[ey]", r"clumsy",
                 r"clunky", r"muddled", r"confusing", r"overlong", r"bloated", r"generic", r"forgettable",
                 r"dull", r"boring", r"lackluster", r"lacklustre"],
}
EVALUATION_RE = [(cat, w, re.compile(rf"(?<![\w-]){w}(?![\w-])", re.I))
                 for cat, ws in EVALUATION.items() for w in ws]
# Coverage verdicts as a standalone capitalized word ("Recommend / Consider /
# Pass", "Verdict: Pass", "Consider."). Case-sensitive, so the verb "pass"
# and a question's "consider" in mid-sentence are not caught here.
VERDICT_WORD_RE = re.compile(
    r"(?:(?<=[:/|])\s*|^\s*|(?<=\s))(Recommend|Consider|Pass)(?=\s*(?:$|[.!:;,/|)\]\[]))", re.M)

# Quoted spans: straight or curly double quotes. Single quotes are not
# treated as quotes (they collide with apostrophes).
QUOTE_RE = re.compile(r"“([^”]+)”|\"([^\"]+)\"")


def quoted_spans(text):
    return [(m.start(), m.end(), m.group(1) if m.group(1) is not None else m.group(2))
            for m in QUOTE_RE.finditer(text)]


def mask_quotes(text, full_lines=None):
    """Replace each quoted span that verifies word for word against
    fog_full.txt with a neutral placeholder. A quote that does not verify
    is left in place, so the word checks see it like any other text
    (author ruling 2026-10-05: quotation marks alone exempt nothing)."""
    def sub(m):
        q = m.group(1) if m.group(1) is not None else m.group(2)
        return "“…”" if _quote_found(q, script_source(full_lines)) else m.group(0)
    return QUOTE_RE.sub(sub, text)


_SCRIPT_SOURCE = {}


def script_source(full_lines=None):
    """The whole script, normalized for quote matching (cached)."""
    if full_lines is None:
        if "default" not in _SCRIPT_SOURCE:
            _SCRIPT_SOURCE["default"] = _norm(" ".join(load_full_lines()))
        return _SCRIPT_SOURCE["default"]
    key = id(full_lines)
    if key not in _SCRIPT_SOURCE:
        _SCRIPT_SOURCE[key] = _norm(" ".join(full_lines))
    return _SCRIPT_SOURCE[key]


# --- 2. questions --------------------------------------------------------------
IMPERATIVES = {
    "add", "cut", "fix", "make", "give", "show", "change", "remove", "rewrite", "revise", "think",
    "ask", "look", "let", "keep", "move", "clarify", "explain", "tell", "take", "use", "find",
    "note", "imagine", "reconsider", "drop", "trim", "expand", "build", "set", "put", "start",
    "stop", "focus", "have", "be", "don't", "don’t", "go", "write", "lose", "tighten", "raise",
    "lower", "replace", "swap", "establish", "ensure", "decide", "remember", "picture",
    "consider", "try",
}
QUESTION_OPENERS_BANNED = [re.compile(r"^\s*what\s+if\s+you\b", re.I)]

# --- 3. pipeline terms -----------------------------------------------------------


def _schema_terms():
    """snake_case enum values and member names, enum class names, and the
    snake_case field names of the schema's dataclasses."""
    import dataclasses
    values, names = set(), set()
    for obj in vars(tagging_schema).values():
        if isinstance(obj, type) and issubclass(obj, Enum) and obj is not Enum:
            names.add(obj.__name__)
            for m in obj:
                if isinstance(m.value, str) and "_" in m.value:
                    values.add(m.value)
                if "_" in m.name:
                    values.add(m.name.lower())
        if isinstance(obj, type) and dataclasses.is_dataclass(obj):
            values.update(f.name for f in dataclasses.fields(obj) if "_" in f.name)
    return sorted(values), sorted(names)


ENUM_VALUES, ENUM_NAMES = _schema_terms()
PIPELINE_RE = [re.compile(rf"\b{re.escape(v)}\b", re.I) for v in ENUM_VALUES] + \
              [re.compile(rf"\b{re.escape(n)}\b") for n in ENUM_NAMES] + [
    re.compile(r"\bPrinciple\s+\d+[a-z]?\b", re.I),
    re.compile(r"\bscene\d+_beat\d+\b", re.I),
    re.compile(r"\bscene\d+\b", re.I),
    re.compile(r"\bPass\s*[12]\b"),
    re.compile(r"\bfinding\s+\d+\b", re.I),
    re.compile(r"\btrait\s+\d+\b", re.I),
    re.compile(r"\bllm_\w+", re.I),
    re.compile(r"\bprovenance\b", re.I),
    re.compile(r"\bcorrections?[- ]log\b", re.I),
    re.compile(r"\b(?:causal[_ ]integrity|chain[_ ]soundness)\b", re.I),
]

# --- 4. citations -----------------------------------------------------------------
CITE_RE = re.compile(r"\[(E\d+)\]")
LOOSE_CITE_RE = re.compile(r"(?<!\[)\bE\d+\b(?!\])")
RAW_LOC_RE = re.compile(r"\b(?:pp?\.|pages?|lines?)\s*\d+", re.I)


@dataclass
class Evidence:
    """One citable beat. Code builds these; the model only sees the ID."""
    id: str
    beat_id: str
    first_line: int
    last_line: int
    pages: list


def evidence_table(beat_ids, index=None):
    """{"E1": Evidence, ...} for the given beats, in the order given."""
    if index is None:
        with open(LINE_INDEX, encoding="utf-8") as f:
            index = json.load(f)["beats"]
    out = {}
    for i, b in enumerate(beat_ids, 1):
        r = index[b]
        out[f"E{i}"] = Evidence(f"E{i}", b, r["first_line"], r["last_line"], r["printed_pages"])
    return out


def load_full_lines():
    with open(FULL_TXT, encoding="utf-8") as f:
        return f.read().split("\n")


def _pages_text(pages):
    return f"p. {pages[0]}" if pages[0] == pages[-1] else f"pp. {pages[0]}–{pages[-1]}"


def resolve_citations(text, evidence):
    """Replace each [E1] with a page citation built by code. Call only on
    text that passed check_text (every ID resolves)."""
    return CITE_RE.sub(lambda m: f"({_pages_text(evidence[m.group(1)].pages)})", text)


# --- 5. quotes -----------------------------------------------------------------------

def _norm(s):
    s = s.replace("\f", " ").replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip()


# Trailing punctuation inside the quotation marks is the writer's sentence
# punctuation, not the script's ("El Vaquero," in American style), so it is
# stripped before the verbatim match (author ruling 2026-10-05).
QUOTE_TRAILING_PUNCT = ",.;:!?"


def _quote_norm(q):
    return _norm(q).rstrip(QUOTE_TRAILING_PUNCT).rstrip()


def _quote_found(q, source):
    """The normalized quote appears in the normalized source as whole words:
    a quote that starts or ends with a letter or digit may not continue a
    longer word there ("baptize" is not in "baptized"). Author ruling
    2026-10-05."""
    q = _quote_norm(q)
    if not q:
        return False
    pat = (r"(?<!\w)" if re.match(r"\w", q) else "") + re.escape(q) + (r"(?!\w)" if re.search(r"\w$", q) else "")
    return re.search(pat, source) is not None


# --- check_text -------------------------------------------------------------------------

@dataclass
class Violation:
    check: str      # banned | question | pipeline | citation | quote | malformed
    detail: str

    def __str__(self):
        return f"[{self.check}] {self.detail}"


def check_text(text, kind="observation", evidence=None, full_lines=None, evaluation=None):
    """All violations in one piece of AI text. Empty list = it passes.
    kind: see KINDS. evaluation: check the praise/critique lists; defaults
    to True for report-voice kinds."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    if not isinstance(text, str) or not text.strip():
        return [Violation("malformed", "empty or not a string")]
    evidence = evidence or {}
    out = []
    masked = mask_quotes(text, full_lines)

    # 1. banned words (quotes masked)
    for cat, w, rx in BANNED_RE:
        if kind == "question" and w == QUESTION_ALLOWED:
            continue
        for m in rx.finditer(masked):
            out.append(Violation("banned", f"{cat} word {m.group(0)!r}"))
    if evaluation is None:
        evaluation = kind in REPORT_VOICE_KINDS
    if evaluation:
        for cat, w, rx in EVALUATION_RE:
            for m in rx.finditer(masked):
                out.append(Violation("banned", f"{cat} word {m.group(0)!r}"))
    for m in VERDICT_WORD_RE.finditer(masked):
        # A question may not open with "Consider" either; that's reported there.
        if not (kind == "question" and m.start(1) == len(masked) - len(masked.lstrip())):
            out.append(Violation("banned", f"coverage verdict {m.group(1)!r}"))

    # 2. questions
    if kind == "question":
        if not text.rstrip().endswith("?"):
            out.append(Violation("question", "does not end with '?'"))
        first = re.match(r"\s*[“\"]?([A-Za-z’']+)", masked)
        if first and first.group(1).lower() in IMPERATIVES:
            out.append(Violation("question", f"opens with an imperative ({first.group(1)!r})"))
        for rx in QUESTION_OPENERS_BANNED:
            if rx.search(masked):
                out.append(Violation("question", "opens with 'What if you'"))

    # 3. pipeline terms (quotes masked: script text is not pipeline text)
    for rx in PIPELINE_RE:
        for m in rx.finditer(masked):
            out.append(Violation("pipeline", f"pipeline term {m.group(0)!r}"))

    # 4. citations
    cited = CITE_RE.findall(text)
    if kind == "summary":
        for c in cited:
            out.append(Violation("citation", f"cites {c}; a summary takes no citations"))
    if kind != "text":
        for m in RAW_LOC_RE.finditer(masked):
            out.append(Violation("citation", f"writes its own location {m.group(0)!r}; cite evidence IDs only"))
        for m in LOOSE_CITE_RE.finditer(masked):
            out.append(Violation("citation", f"evidence ID {m.group(0)!r} not in [E#] form"))
        for c in cited:
            if c not in evidence:
                out.append(Violation("citation", f"cites {c}, which is not in the evidence given"))
        if kind == "observation" and not any(c in evidence for c in cited):
            out.append(Violation("citation", "an observation needs at least one citation that resolves"))

    # 5. quotes: against the cited lines, or the whole script for a summary
    spans = quoted_spans(text)
    if spans and kind == "summary":
        if full_lines is None:
            full_lines = load_full_lines()
        source = _norm(" ".join(full_lines))
        for _, _, q in spans:
            if not _quote_found(q, source):
                out.append(Violation("quote", f"quoted text {q!r} is not verbatim in fog_full.txt"))
    elif spans:
        good = [evidence[c] for c in dict.fromkeys(cited) if c in evidence]
        if not good:
            out.append(Violation("quote", "quotes script text but cites no evidence to check it against"))
        else:
            if full_lines is None:
                full_lines = load_full_lines()
            source = _norm(" ".join(" ".join(full_lines[ev.first_line - 1:ev.last_line]) for ev in good))
            for _, _, q in spans:
                if not _quote_found(q, source):
                    out.append(Violation("quote", f"quoted text {q!r} is not verbatim in the cited lines"))
    return out


# --- 6. retry policy ------------------------------------------------------------------------

@dataclass
class GuardResult:
    item_id: str
    text: str                 # the accepted text, citations still as [E#]
    source: str               # "ai" | "ai_retry" | "fallback"
    violations: list = field(default_factory=list)  # from rejected attempts

    def rendered(self, evidence):
        return resolve_citations(self.text, evidence)


def guard_generate(item_id, generate, fallback, kind="observation", evidence=None,
                   full_lines=None, log_path=GUARD_LOG):
    """generate(violations) -> text. It is called once with None, and at
    most once more with the first attempt's violations. If both attempts
    fail, fallback() supplies deterministic template text, which must pass
    the same checks, and the item is logged to log_path."""
    rejected = []

    def attempt(violations):
        try:
            text = generate(violations)
        except Exception as ex:  # a failed call is a rejected response
            return None, [Violation("malformed", f"generate raised {type(ex).__name__}: {ex}")]
        return text, check_text(text, kind, evidence, full_lines)

    text, v = attempt(None)
    if not v:
        return GuardResult(item_id, text, "ai")
    rejected.append({"attempt": 1, "text": text, "violations": [str(x) for x in v]})
    text, v2 = attempt([str(x) for x in v])
    if not v2:
        return GuardResult(item_id, text, "ai_retry", [str(x) for x in v])
    rejected.append({"attempt": 2, "text": text, "violations": [str(x) for x in v2]})

    fb = fallback()
    vfb = check_text(fb, kind, evidence, full_lines)
    if vfb:
        raise ValueError(f"{item_id}: fallback template text fails the guard: {[str(x) for x in vfb]}")
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"item": item_id, "kind": kind, "fallback": fb, "rejected": rejected},
                               ensure_ascii=False) + "\n")
    return GuardResult(item_id, fb, "fallback", [s for r in rejected for s in r["violations"]])


# --- 7. final scan of the built page ------------------------------------------------------

HOOD_RE = re.compile(r"<details class=\"[^\"]*\bhood\b[^\"]*\">.*?</details>", re.S)


BLOCK_END_RE = re.compile(r"</(?:h[1-6]|p|li|dt|dd|th|td|summary|div|section)>", re.I)


def visible_text(page_html):
    """The page's static reader-facing text: no scripts, styles, data or
    "Under the hood" blocks. Each block element (heading, paragraph, list
    item ...) ends on its own line, so a heading is never run together
    with the paragraph after it."""
    body = page_html.split("<body>", 1)[-1]
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
    body = HOOD_RE.sub(" ", body)
    body = BLOCK_END_RE.sub("\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    lines = (re.sub(r"\s+", " ", l).strip() for l in htmlmod.unescape(body).split("\n"))
    return "\n".join(l for l in lines if l)


# The product is called Numen (author decision 2026-10-06). The old working
# name must not reach a reader: internal names (folder, modules, storage
# keys, attributes) are fine, visible text is not.
OLD_NAME_RE = re.compile(r"a-?score", re.I)


def all_visible_text(page_html):
    """Everything a reader can see, including "Under the hood" blocks once
    opened: the page minus scripts, styles and tag attributes, one line."""
    body = page_html.split("<body>", 1)[-1]
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", body)))


def old_name_hits(page_html):
    """Every place the old name ("a-score", "ascore", any case) appears in
    text a reader can see, including "Under the hood" blocks once opened."""
    text = all_visible_text(page_html)
    return [text[max(0, m.start() - 40):m.end() + 40].strip() for m in OLD_NAME_RE.finditer(text)]


# Framing says "AI", never "model" (author, 2026-10-06). One exception: the
# line that names the model ID ("model claude-sonnet-5").
MODEL_WORD_RE = re.compile(r"\bmodels?\b", re.I)
MODEL_ID_RE = re.compile(r"\bmodel\s+claude-[\w.-]+")


def model_word_hits(text, locked=()):
    """Places "model" appears in framing text. `locked` strings (the AI's own
    text, the author's verbatim review text) are removed first; the model-ID
    phrase is the one exception."""
    t = re.sub(r"\s+", " ", text)
    for s in sorted(locked, key=len, reverse=True):
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            t = t.replace(s, " ")
    t = MODEL_ID_RE.sub(" ", t)
    return [t[max(0, m.start() - 50):m.end() + 40].strip() for m in MODEL_WORD_RE.finditer(t)]


# Sentence ends: . ? ! : optionally followed by a closing quotation mark or
# bracket, then whitespace; and every line break (a block element's end).
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.?!:])\s+|(?<=[.?!:][\"”’)])\s+|\n")


def sentences(text):
    return [x.strip() for x in SENTENCE_SPLIT_RE.split(text) if x and x.strip()]


@dataclass
class Finding:
    where: str
    violation: str
    context: str

    def __str__(self):
        return f"{self.where}: {self.violation} in {self.context!r}"


TEXT_CLASSES = ("report_voice", "static", "ai_read")


def final_scan(page_html, reader_strings=(), approved_static=(), verbatim=None):
    """Banned words and pipeline terms in the built page's static text and
    in the reader-facing strings the page renders from its data, scoped by
    text class (see the module docstring). Returns findings; the caller
    stops the build on any.
    reader_strings: iterable of (where, text, text_class). The page's own
    static text is class "static", checked sentence by sentence.
    approved_static: exact strings of static copy approved by the author;
    only these are exempt from the banned-word check.
    verbatim: {"label": [strings], "texts": [strings]} for a verbatim class
    (author ruling 2026-10-05: the published Big Seven definitions). Its
    texts are exempt from every word check, but only if each one appears
    on the page exactly (whitespace aside) and every label string is
    present too; otherwise each failure is a finding, so the build stops."""
    approved = set(approved_static)
    out = []
    vis = visible_text(page_html)
    if verbatim:
        for kind in ("label", "texts"):
            for t in verbatim.get(kind, []):
                n = re.sub(r"\s+", " ", t).strip()
                if n in vis:
                    vis = vis.replace(n, "\n")
                else:
                    out.append(Finding("verbatim class", f"[verbatim] {kind[:-1] if kind == 'texts' else kind} "
                                       "not on the page exactly", n[:157] + ("..." if len(n) > 157 else "")))
    items = [("static page text", s, "static") for s in sentences(vis)]
    items += list(reader_strings)
    for where, s, cls in items:
        if cls not in TEXT_CLASSES:
            raise ValueError(f"{where}: unknown text class {cls!r}")
        skip_banned = cls == "ai_read" or (cls == "static" and s in approved)
        for v in check_text(s, "text", evaluation=(cls == "report_voice")):
            if v.check == "pipeline" or (v.check == "banned" and not skip_banned):
                out.append(Finding(where, str(v), s if len(s) < 160 else s[:157] + "..."))
    return out
