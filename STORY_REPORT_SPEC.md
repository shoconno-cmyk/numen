# Numen Story Report Spec

*Renamed 2026-10-05 from "Health Report" (file was HEALTH_REPORT_SPEC.md). The output files were renamed the same day, to `fog_story_report.html` and `fog_story_report_review.html`.*

Oct 3, 2026 · @Shane

## Purpose

The story report is what a development team receives when a script goes into Numen: an evidence-based read of how the story's characters and structure hold together, built to inform one question every exec asks, *should we move forward with this project?*

- **Who it's for:** development execs, assistants and readers, and the writers they work with.
- **What it replaces and adds to:** traditional coverage gives one reader's impression and ends in Recommend / Consider / Pass. The story report gives no grade. It offers what coverage can't: line-cited evidence for every observation, a per-character, per-beat map of character function, and the scope of each observation (a moment, a sequence, a throughline).
- **What it is not:** a predictor of box office or critical success. A strong archetype presence does not guarantee a hit, so the report never scores a script's odds.

## Design principle: consultant, not judge

The model is an outside observer, never a judge of the writer. It points at what it sees on the page; the development team, who know the story, decide what it means and what to do. Every line of the report follows these rules:

- **Observations, not verdicts.** "John's reversal has no visible cause in the preceding pages" (checkable fact), never "John's reversal is unearned" (judgment of the work).
- **No directives.** The report never says what to write. (Development questions are not in the first release; see Future features.)
- **No grading language.** No "problems," "flaws," "weaknesses," "needs work," or verdicts. Scope is described neutrally: an observation touches *a moment*, *a sequence*, or *a character's throughline*.
- **Evidence on every claim.** Each observation cites pages and lines so anyone can check it in minutes.
- **What is on the page, not opinion** (author, 2026-10-05). The report states what is on the page, with evidence, and leaves opinions to the people reading it. Nothing in it should be something a reasonable reader could staunchly disagree with as a matter of taste or judgment.
- **Honest humility.** The model is still often wrong, so its tone is "here's what I noticed; you know your story." That is diplomacy and accuracy at once.

**Scoping the guard** (author ruling, 2026-10-05). `report_guard.py` enforces these rules on everything a reader sees. The banned-word checks (grading words, directives, coverage verdicts) are scoped by text type:

- **Report-voice text** (observations, questions, the development read, plain-language wording): every check applies in full. One exception: "needs to" is allowed inside a question, never in a statement. The question checks still apply, including the imperative-opener check.
- **Author-written static copy and fixed templates:** exempt from the banned-word check only through an explicit approved list of exact strings (`APPROVED_STATIC` in `report.py`). Approved so far: "Why should I care?", "It gives no grade.", "The report doesn't grade the script or tell anyone what to write.", the "A limit revealed" template ("…a limit, a weakness, or a strength not seen before."), and "And it never decides whether a story is good." (2026-10-05). The same list also governs `report.py`'s own grading-word check. Any new static text is checked until it is approved.
- **Demo-card page captions** ("Full of Grace, page N" under each rendered script page; author approval 2026-10-06): exempt from report_guard's citation rule, which forbids AI text from naming its own location. They get the plain-text checks only (pipeline terms, grading words), on one condition: N is read from the page image's own source page (its page-number header in the PDF, `demo_prototype/card_kit.printed_number`), never typed or hard-coded. `test_demo_cards.py` fails if a caption's number doesn't match the page it sits under.
- **The AI's stored per-moment reads**, shown verbatim in panels (how an audience would see it, how the character sees it, what they feel, what they want, the role they fill): exempt from banned words as a class, because rewording them would misrepresent the AI's output. They must be clearly labelled as the AI's read, and the build checks that the labels are on the page.

- **The published Big Seven definitions** (the appendix "The Big Seven: full definitions", author ruling 2026-10-05): a verbatim class, exempt from both the banned-word and the pipeline-term checks, but only if every definition is on the page exactly as it was given to the AI in the cold run (`tagging_schema.py` at `7a6e69e`, verified identical to the current file) and the appendix's label lines are present. If either fails, the build stops.

Pipeline-term checks apply to every other text type. Any finding stops the build; nothing is left pending.

*Example (illustrative only):* "Between pages 54 and 88, nothing on the page shows what changes John's mind. Is that something the audience needs to see, or is it meant to stay hidden?"

## Report structure

The report gives a development team what is on the page, with evidence; opinions and the ways forward stay with the people in the room. Four sections, in reading order, after a short "Why should I care?" introduction:

1. **Development read:** the title (from the title page), the genre, and a logline of one or two sentences (premise, protagonist, stakes; no ending). Below it, collapsed under "Read the full synopsis", a synopsis of 3-4 paragraphs (about 300-400 words) that includes the ending. Written by the AI from the script text only, and labelled so; states only what is on the page. No grade. (Was a one-paragraph synopsis until 2026-10-05.)
2. **Character arcs: where characters change, and where they don't:** where characters change or show something new, and where they hold steady, with page evidence. (Titled "What's landing" until 2026-10-05; described as "the story's strengths" until the 2026-10-05 "what is on the page, not opinion" principle.)
3. **Character function map:** the archetype breakdown per character and per beat, read as development insight rather than a score.
4. **Archetype timeline** (added 2026-10-06): one lane per Big Seven archetype across the script's pages (1-125), each archetype call a mark at its moment's first line, labelled with the character. Same AI Output / Human Reviewed switch; in Human Reviewed, Great Mother marks are filled for the dark pole and hollow where review named none (pole read from review verdicts and author rulings, not a stored field). It shows where archetypes are called, not how much they matter: no pattern reading, no counts in the framing.

The page closes with a static "What this report doesn't measure" note (see below).

## Section detail

Each section draws on data the pipeline already produces; what's new is how it's selected, phrased and presented.

| Section | What it shows | Pipeline data it draws from |
| --- | --- | --- |
| Development read | Title, genre, logline; full synopsis on request | The script text only (one model call, structured output, checked by `report_guard.py`); the title by code from the title page |
| Character arcs: where characters change, and where they don't | Characters whose reactions hold together; turns with a visible cause; character functions carried consistently | Pass 2 consistent and proportionate verdicts; earned turning points; stable archetype runs |
| Character function map | Per character: which functions they carry, beat by beat; where functions appear, shift or vanish across the script | Pass 1 archetype tags per beat and character; archetypal standing |
| Archetype timeline | Per archetype: where it is called across the script's pages, and for which character | The same archetype calls as the map; Great Mother pole from the review records (verdicts and author rulings) |

**Comparison beats stay under the hood** (author decision, 2026-10-05). A turning point's comparison beat (`comparison_beat_id` in `fog_turning_points_reviewed.json`) is data-layer only: it may sit in the model, the JSON and any developer view, but the report's plain-language text never names or shows it.

**Why the character function map matters.** Archetypes are character function, and character function is what development notes are about: "the mentor disappears after act one," "the love interest has nothing to do," "we never see her vulnerable side." The map makes function visible with page numbers, shows a role's range at a glance (relevant to attaching talent), and tracks whether a rewrite actually changed a character's function. No reader produces this map; it takes an expert weeks by hand.

## What the report does not measure

The report says plainly what's outside its scope, so its observations are read for what they are. The page carries this as a static, always-visible note near the end, in the author's wording: "What this report doesn't measure: dialogue and voice; marketability, audience appeal and comparable titles; castability and budget; box-office or critical success. And it never decides whether a story is good. That call stays with the people reading it."

- Dialogue quality and voice
- Marketability, audience appeal and comparable titles
- Castability and budget
- Box-office or critical success
- Whether the story is *good*: that call stays with the people reading it

## Built today vs. needs building

The data behind the report exists for Full of Grace; the report itself does not yet. The main build is the report generator (Stage 6, report.py, currently missing).

| Piece | Status | Notes |
| --- | --- | --- |
| Pass 1 archetype tags per beat and character | Built | Cold accuracy: 57 of 82 cold archetype tags kept after review (69.5%) |
| Pass 2 consistency and proportionality verdicts | Built | Cold run over-claims change: 98 of 134 change-claims ruled no change on review |
| Archetypal standing | Script exists | 23\_compute\_archetype\_standing.py needs its hardcoded path changed |
| Emotional wave | Function exists | compute\_script\_wave() exists; FOG's wave is empty |
| Plot facts | Stage exists | Never run on the FOG cold run; can't be shown as informing its tags |
| Report generator (Stage 6) | Built | All four sections and the static sections (`report.py`). Section 3, the consistency check, is built but switched off (`SHOW_CONSISTENCY_CHECK`); see Future features |
| Plain-language phrasing layer | Decided: templates | Section 2 (and the disabled consistency check) keep their fixed template wording. The planned LLM rewording of them is skipped (author decision, 2026-10-05) |
| Development read (section 1) | Built | The only LLM-written text in the report, gated by `report_guard.py`. Logline + full synopsis (prompt version 5) dry-run only so far; the live page shows the author-checked one-paragraph synopsis until that run |

**Cold or reviewed?** For the demo, the report shows the cold output by default (what a user would get today), clearly labeled, with a toggle to the human-reviewed version. The gap between them is the bridge to the demo's "Promise of the Premise" section.

## The longer vision: an always-on development agent

The story report is the first skill of a larger product: a development agent that stays with a project across every draft and becomes a working member of the team.

- **Memory across drafts:** it has read every version and knows every note the project received.
- **Did the note land?** It checks whether each note was addressed, and whether a fix introduced a new inconsistency elsewhere.
- **Function over time:** it tracks whether a rewrite actually changed a character's arc or function, or just the dialogue.
- **Holding the whole story:** finding 21 (the JOHN / YOUNG JOHN secret) was invisible to the per-character pipeline and caught only because the author held the whole story in mind. On a long project, nobody does. The agent's job is to be that memory.

The agent serves the team: writer, exec and reader. It never replaces the writer's judgment, consistent with the design principle above.

For the first release, this appears in the README as the roadmap, not as a demo claim. A draft-comparison example would be added if an earlier draft of Full of Grace is available.

## Future features

**Consistency check: a second look** (dropped from the first public release, author decision 2026-10-05). It was section 3: possible inconsistencies the AI flagged, each with page evidence and a scope (a moment, a sequence, a throughline). Reason for removal: flagged "inconsistencies" are subjective judgment calls that read as implied development notes, which conflicts with the "what is on the page, not opinion" principle above. In Full of Grace the AI flagged 7 possible inconsistencies, and none were upheld on human review. The code and data stay in the repo, switched off (`SHOW_CONSISTENCY_CHECK = False` in `report.py`); turning it on restores the section, and the section numbers adjust.

**Questions for the next draft** (dropped from the first release, author decision 2026-10-05). It was planned as section 4: one question per observation, pointing at what the story may need. Reasons for dropping it:

- Generating development questions risks crowding out the contributions of creative execs, writers and assistants. Asking those questions is their own craft.
- "Next draft" presumes the script will be revised.
- A leading question can carry judgment that word checks can't catch.
- In Full of Grace, every consistency flag the AI raised was overturned on review.

Whether questions would help is a hypothesis to test later with real development people (see the utility test under Open questions). `report_guard.py` keeps its question checks, so the feature can return without new guard work.

## Open questions

- [ ] Draft comparison: no earlier complete drafts of Full of Grace exist; unfinished drafts might serve for a partial comparison. Vision stays in words for the first release.
- [x] Plot facts: DONE. Run post-hoc on FOG 2026-10-03 (3 facts), all three human-corrected (corrections log 845-847). Labeled as a separate stage that did not inform the cold-run tags.
- [ ] How much of the character function map fits in the report versus a linked full view?
- [ ] Which development notes do execs give most often? The answer may reshape the section list.
- [ ] Utility test for later: do the model's observations line up with real studio notes your scripts actually received? Fold in the questions hypothesis: would development people find generated questions useful, or would they crowd out their own? (See Future features.)
