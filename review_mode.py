"""
review_mode.py -- the one review-mode implementation, shared by the Story
Report (report.py --review), the walkthrough (walkthrough.py --review) and
the demo cards (demo_prototype/build_archetype_cards.py --review).

A review page is a local-only copy of a public page with a "Review mode"
switch: reader-facing framing becomes editable in the browser, locked text
(the AI's text, script excerpts, verbatim review notes and author rulings:
anything marked data-ai, data-locked or data-verbatim) is outlined and
never editable, and "Copy my edits" lists every change as
  page, section, element, source (constant or builder line), original, new
so it can be applied to the source by hand. Edits in the browser never
change the source by themselves. Each page has its own storage key.

Public pages must never contain MARKER or the review bar
(assert_public); review pages must (assert_review). Review pages are
git-ignored and never linked from a public page.
"""
import datetime
import html
import json
import os
import re

MARKER = "a-score-review-mode"  # in the review bar's data-mode attribute only

# Locked text: never editable, outlined, with its reason shown.
LOCKED = "[data-ai], [data-locked], [data-verbatim]"

CSS = r"""
#review-bar { position: fixed; right: 16px; bottom: 16px; z-index: 30; background: var(--panel); color: var(--ink);
  border: 1px solid var(--rule); border-radius: 10px; box-shadow: var(--shadow); padding: 10px 12px;
  font-size: 13px; width: min(420px, calc(100vw - 32px)); }
#review-bar .row1 { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
#review-bar label { display: inline-flex; align-items: center; gap: 6px; font-weight: 650; cursor: pointer; }
#review-bar button { font: inherit; padding: 4px 10px; border-radius: 6px; border: 1px solid var(--rule);
  background: var(--lane); color: var(--ink); cursor: pointer; }
#review-bar .count { color: var(--muted); }
#review-bar textarea { display: none; width: 100%; height: 180px; margin-top: 8px; font: 12px/1.4 ui-monospace, Consolas, monospace;
  background: var(--bg); color: var(--ink); border: 1px solid var(--rule); border-radius: 6px; padding: 6px; }
#review-bar textarea.show { display: block; }
#review-bar .msg { color: var(--muted); margin-top: 6px; }
.review-on [contenteditable="true"] { outline: 1px dotted var(--muted); outline-offset: 2px; cursor: text; }
.review-on [contenteditable="true"]:focus { outline: 2px solid var(--verdict); }
.review-on .rv-edited { background: color-mix(in srgb, var(--verdict) 16%, transparent); }
.review-on [data-ai], .review-on [data-locked], .review-on [data-verbatim] { outline: 2px dashed var(--claim); outline-offset: 3px; position: relative; }
.review-on [data-ai]::before, .review-on [data-locked]::before, .review-on [data-verbatim]::before { display: block; width: max-content;
  max-width: 100%; margin: 0 0 4px; font: 600 11px/1.4 ui-sans-serif, system-ui, sans-serif; color: var(--claim); }
.review-on [data-verbatim]::before { content: "Verbatim text: locked, not editable"; }
.review-on [data-ai]::before { content: "AI output: locked, not editable"; }
.review-on [data-locked]::before { content: attr(data-locked) ": locked, not editable"; }
"""

JS = r"""
// Review mode (local build only). Edits live here and in localStorage; the
// source changes only when the edit list is applied to the builder.
(function () {
  const bar = document.getElementById('review-bar'), box = bar.querySelector('textarea'), msg = bar.querySelector('.msg');
  const PAGE = bar.dataset.page, STORE = bar.dataset.store, CAND = bar.dataset.cand;
  const LOCKED = bar.dataset.locked, SKIP = bar.dataset.skip + ', ' + LOCKED;
  let SOURCES = {};
  try { SOURCES = JSON.parse(document.getElementById('rv-sources').textContent); } catch (e) { SOURCES = {}; }
  let on = false, edits = {};
  try { edits = JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) { edits = {}; }
  const norm = t => t.replace(/\s+/g, ' ').trim();
  const save = () => { try { localStorage.setItem(STORE, JSON.stringify(edits)); } catch (e) {} };
  // Where a line comes from: an exact match in the page's source map, else the
  // longest mapped line it contains or is part of, else the builder to search.
  function sourceOf(orig) {
    if (SOURCES[orig]) return SOURCES[orig];
    let best = null;
    for (const [t, s] of Object.entries(SOURCES))
      if (t.length >= 12 && (orig.includes(t) || t.includes(orig)) && (!best || t.length > best[0].length)) best = [t, s];
    return best ? best[1] + (orig.includes(best[0]) && orig !== best[0] ? ', with more text around it' : ', part of it')
                : bar.dataset.fallback;
  }
  function sectionOf(el) {
    if (el.closest('#sheet')) return 'Detail panel';
    const sec = el.closest('section');
    if (!sec) return 'Page header';
    const h = sec.querySelector('h2');
    return h ? (h.dataset.orig || norm(h.textContent)) : (sec.getAttribute('aria-label') || 'Section');
  }
  const describe = el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
    ? '.' + el.className.trim().split(/\s+/).filter(c => !c.startsWith('rv-')).join('.') : '');
  function mark(root) {
    if (!on) return;
    root.querySelectorAll(CAND).forEach(el => {
      if (el.closest(SKIP) || el.matches('.gl') || !norm(el.textContent)) return;  // .gl: edit its .gtxt only
      if (el.querySelector(LOCKED)) return;   // holds locked text: editing it would unlock that text
      if (el.parentElement && el.parentElement.closest('[contenteditable="true"]')) return;
      if (!el.dataset.orig) el.dataset.orig = norm(el.textContent);
      el.setAttribute('contenteditable', 'true');
      el.setAttribute('spellcheck', 'true');
      const k = sectionOf(el) + '\u0001' + el.dataset.orig, ed = edits[k];
      if (ed && el !== document.activeElement && norm(el.textContent) !== ed.new) el.textContent = ed.new;
      el.classList.toggle('rv-edited', !!ed);
    });
  }
  function unmark() {
    document.querySelectorAll('[contenteditable="true"]').forEach(el => el.removeAttribute('contenteditable'));
  }
  document.addEventListener('input', ev => {
    const el = ev.target.closest && ev.target.closest('[contenteditable="true"]');
    if (!el || !el.dataset.orig) return;
    const sec = sectionOf(el), k = sec + '\u0001' + el.dataset.orig, now = norm(el.innerText);
    if (now === el.dataset.orig) delete edits[k];
    else edits[k] = {section: sec, element: describe(el), source: sourceOf(el.dataset.orig), original: el.dataset.orig, new: now};
    el.classList.toggle('rv-edited', !!edits[k]);
    save(); count();
  });
  // Keep toggle switches and panel buttons working inside editable text.
  document.addEventListener('keydown', ev => {
    if (on && ev.key === 'Enter' && ev.target.closest && ev.target.closest('[contenteditable="true"]')) ev.preventDefault();
  });
  new MutationObserver(() => { if (on) mark(document); }).observe(document.body, {childList: true, subtree: true});
  function count() { bar.querySelector('.count').textContent = Object.keys(edits).length + ' edit(s)'; }
  function list() {
    const es = Object.values(edits);
    let t = `Numen review edits (${PAGE}): ${es.length} change(s)\n` +
      `Built: ${bar.dataset.built}\n\n`;
    es.forEach((x, i) => {
      t += `${i + 1}. Section: ${x.section}\n   Element: ${x.element}\n   Source: ${x.source || sourceOf(x.original)}\n` +
        `   Original: ${x.original}\n   New: ${x.new}\n\n`;
    });
    return t;
  }
  bar.querySelector('#rv-on').addEventListener('change', ev => {
    on = ev.target.checked;
    document.body.classList.toggle('review-on', on);
    on ? mark(document) : unmark();
  });
  bar.querySelector('#rv-copy').addEventListener('click', async () => {
    const t = list();
    box.value = t; box.classList.add('show'); box.focus(); box.select();
    let ok = false;
    try { await navigator.clipboard.writeText(t); ok = true; } catch (e) {
      try { ok = document.execCommand('copy'); } catch (e2) { ok = false; }
    }
    msg.textContent = ok ? 'Copied to the clipboard. The list is also in the box above.'
                         : 'Could not copy automatically: select the text in the box and copy it.';
  });
  bar.querySelector('#rv-clear').addEventListener('click', () => {
    if (!confirm('Clear all edits on this page? The page goes back to the built text.')) return;
    edits = {}; save(); location.reload();
  });
  count();
})();
"""

BAR = """<div id="review-bar" data-mode="{marker}" data-built="{built}" data-page="{page}" data-store="{store}"
 data-cand="{cand}" data-skip="{skip}" data-locked="{locked}" data-fallback="{fallback}" role="region" aria-label="Review mode">
<div class="row1"><label><input type="checkbox" id="rv-on"> Review mode</label>
<span class="count"></span>
<button type="button" id="rv-copy">Copy my edits</button>
<button type="button" id="rv-clear">Clear edits</button></div>
<textarea readonly aria-label="Your edits, as a list"></textarea>
<div class="msg">Local build only. Edits stay in this browser until you copy them.</div>
</div>"""


def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def source_map(entries, builder_path):
    """{shown text: "label (builder.py:line)"} for framing entries given as
    (label, shown text, template or None). The line is the first builder line
    holding the start of the template (the text before any {field})."""
    with open(builder_path, encoding="utf-8") as f:
        src_lines = f.read().split("\n")
    base = os.path.basename(builder_path)
    out = {}
    for label, shown, template in entries:
        if not isinstance(shown, str) or not shown.strip():
            continue
        head = (template or shown).split("{")[0].strip()
        line = None
        for n in (32, 20, 12):
            probe = head[:n]
            if len(probe) >= 8:
                line = next((i for i, l in enumerate(src_lines, 1) if probe in l), None)
                if line:
                    break
        out.setdefault(_norm(shown), f"{label} ({base}:{line})" if line else f"{label} ({base})")
    return out


def bar(page, store, cand, skip, sources, fallback):
    """The review bar, its source map and the review script, for one page."""
    built = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    a = {k: html.escape(v, quote=True) for k, v in dict(
        marker=MARKER, built=built, page=page, store=store, cand=cand, skip=skip, locked=LOCKED,
        fallback=fallback).items()}
    data = json.dumps(sources, ensure_ascii=False).replace("</", "<\\/")
    return (BAR.format(**a) + f'<script type="application/json" id="rv-sources">{data}</script>'
            + f"<script>{JS}</script>")


def assert_public(page_html, label):
    if MARKER in page_html or "review-bar" in page_html or "rv-sources" in page_html:
        raise SystemExit(f"ABORT: Review mode found in the public {label}")


def assert_review(page_html, label):
    if MARKER not in page_html:
        raise SystemExit(f"ABORT: the review build of the {label} is missing Review mode")


def review_path(public_path):
    """foo.html -> foo_review.html, next to it."""
    root, ext = os.path.splitext(public_path)
    return root + "_review" + ext
