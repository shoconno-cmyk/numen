# Numen

**Numen: Jungian Archetype and Character-Arc Analysis for Screenplays**

Numen reads a screenplay and maps where each character presents as one of seven recurring character patterns, beat by beat, with the page and the text behind every call.

---

## See it in 60 seconds

All built from one feature script, *Full of Grace*:

- **[The Walkthrough](https://shoconno-cmyk.github.io/numen/numen_walkthrough.html)**: the same script followed from PDF to report, stage by stage.
- **[The Story Report](https://shoconno-cmyk.github.io/numen/fog_story_report.html)**: the finished report, with an AI Output / Human Reviewed switch on each section.
- Four demo cards, one moment each, shown the way review checks it:
  - [Holly: Trickster Archetype](https://shoconno-cmyk.github.io/numen/demo_prototype/holly_scene3_beat2_card.html)
  - [Mackie: Great Mother or Shadow Archetype?](https://shoconno-cmyk.github.io/numen/demo_prototype/mackie_scene140_beat6_card.html)
  - [Pete: Limit Revealed or Character-Consistent?](https://shoconno-cmyk.github.io/numen/demo_prototype/pete_scene122_beat1_card.html)
  - [The Protected Becomes the Protector](https://shoconno-cmyk.github.io/numen/demo_prototype/protected_protector_card.html)

The links open the pages on GitHub Pages. To view them locally instead, open the `.html` files from a copy of the repo; they load their fonts from `fonts/`.

---

## Why archetypes

Development notes are often about what a character *does* in the story: the mentor who disappears after act one, the hero who never acts, the mother figure who controls rather than protects. Archetypes give those functions names and make them trackable across a whole script.

Numen uses **The Big Seven**: Persona, Shadow, Trickster, Hero, Mentor (Jung's Wise Old Man), Great Mother (six from Jung), plus the Chorus from Greek drama. Each has a written definition, and the AI applies those definitions to what is on the page. Every call links to its page, its text and the full definition, so a reader can check whether the rule was applied correctly.

The premise, stated plainly: archetypes are a lens on a script. They are not a predictor of box-office or critical success, and Numen makes no claim that they are.

---

## What it deliberately doesn't do

> Other tools cover structure, pacing and coverage. Numen does one thing: it tags the Big Seven Jungian archetypes beat by beat, with evidence from the page.

Numen is a consultant, not a judge:

- No grades, scores, rankings or pass/consider verdicts.
- No notes on what to write or how to fix the story.
- It doesn't measure dialogue and voice, marketability, castability, budget, or box-office potential.
- It never says whether a story is good or bad. That call stays with the people reading it.

---

## How it works

Five stages, each shown with real excerpts in the [walkthrough](https://shoconno-cmyk.github.io/numen/numen_walkthrough.html):

1. **The Script Read.** The text is pulled from the script PDF with its layout kept, split into scenes (223 in *Full of Grace*), and every line is labelled: scene heading, action, character name, dialogue or direction.
2. **Finding the Moments.** Each scene is split into moments (460 in all) wherever the text shifts: a pause, a line that stops short, a sharp swing in tone.
3. **The AI Labels the Archetypes.** The AI reads one moment at a time and says which of The Big Seven, if any, each character presents as. Any answer outside the allowed terms is rejected and asked for again. The run made 470 AI calls.
4. **The AI Tracks Character Changes.** The AI reads each character's full arc before judging any moment, then measures every moment against the traits it found: 524 judgments across 29 characters.
5. **The Story Report.** The AI writes a genre, logline and synopsis from the script alone; code assembles the rest; a check rejects any wording that passes judgment on the script.

The AI throughout is Claude (`claude-sonnet-5`).

---

## Where it stands today

The aim is an AI-only product, with no human review. Today, human review is how the AI is measured: a person checked its work on *Full of Grace*, call by call, and the report shows both versions side by side.

- **Archetypes:** 57 of the AI's 82 archetype calls were kept as made.
- **Consistency flags:** the AI flagged 7 possible inconsistencies; none were upheld on review. Because these flags are subjective judgment calls that read like development notes, that section was taken out of this release.
- **Order of the two passes:** the character-change stage ran after 196 human corrections to the archetype stage, so its judgments rest on reviewed archetype calls. The report says so on that section.
- **Emotional wave, tested and left out:** a sentiment 'wave' across the script read the words one at a time, not what they amount to. The scene where Holly disappears and the confession near the end both came out near-neutral, their averages hiding wide swings inside each scene. The archetype timeline ships on its own.

These are results for one script and one AI run.

---

## How it stays honest

- **The AI's text is locked.** Its stored reads are shown word for word and labelled as the AI's; they are never reworded.
- **Quotes and excerpts are checked.** Script text on every page is copied from the extracted script by line range, never typed; quotations in review notes and the cards' highlighted lines are matched word for word against the script text; every excerpt on the walkthrough is matched against its source file. A mismatch stops the build.
- **A judgment guard.** `report_guard.py` rejects grading words, directives, coverage verdicts, praise and critique words, and pipeline jargon in anything the report says in its own voice.
- **Clear labels.** The AI is marked in teal and human review in gray, on every page.
- **Numbers come from the data.** Every count on the walkthrough is computed at build time, and tests fail if one drifts.

---

## What's next

- **Running on a studio's own machines.** The pipeline is designed so the AI can be swapped. A next step is running it on an open-weight AI, so scripts never leave a studio's own machines. That sits alongside enterprise API agreements with no data retention as ways to keep scripts confidential.
- **Before that, a small comparison:** a few *Full of Grace* scenes through a smaller open-weight AI, checked against the current output.
- **Fields the tagging still lacks:** a one-line rationale for each archetype call, and the Great Mother's pole (light or dark), which today is read from the review records.
- **An emotion view built on the AI's own stored emotion for each moment**, in place of the dropped sentiment wave.
- **Self and audience:** each moment already stores how the character sees it and how the audience sees it. Where those two pull apart is where masks, irony and self-deception live, and a view built on that gap is a natural next section.
- **Longer term:** an always-on development partner that follows a script across drafts, remembers every note and development cycle, and works alongside a studio's development team.

---

## The name

In Jungian psychology, the numinous is the charge an archetype carries; Jung took the term from Rudolf Otto. **Numen** names that charge.

### Related work

- Han, Youngsue (2019). "Jungian Character Network in Growing Other Character Archetypes in Films." *International Journal of Contents* 15(2), 13–19. [doi:10.5392/IJoC.2019.15.2.013](https://doi.org/10.5392/IJoC.2019.15.2.013)
- Kabashkin, Igor; Zervina, Olga; Misnevs, Boriss (2025). "AI Narrative Modeling: How Machines' Intelligence Reproduces Archetypal Storytelling." *Information* 16(4), 319. [doi:10.3390/info16040319](https://doi.org/10.3390/info16040319)

---

## About the author

Story development teams read hundreds of scripts a year looking for something they often can't fully articulate: does this story resonate? As a produced screenwriter with an honours degree in psychology and many years behind the scenes at a film studio, I built Numen to test whether Jung's archetypes could make part of that search clearer, and whether AI could surface the evidence on the page. On the technical side, I completed Andrew Ng's Machine Learning Specialization (DeepLearning.AI) and the University of Michigan's Python for Everybody Specialization with Dr. Charles Severance. I work at Bridge Studios in Vancouver, British Columbia.

Certificates and contact: [LinkedIn](https://www.linkedin.com/in/shoconno)

---

## Repo layout and how to run it

**Pipeline** (Python, run as plain scripts from the repo root):
`parser.py`, `beat_detector.py`, `signals.py`, `suspense_signals.py`, `tagging_schema.py`, `llm_orchestration.py`, `pass2_orchestration.py`, with the *Full of Grace* runners `build_fog_scaffold.py`, `fog_tagging_harness.py` and `fog_pass2_runner.py`.

**Pages:**
`report_data.py` → `report.py` (the Story Report), `walkthrough.py`, `demo_prototype/build_archetype_cards.py`. Shared look: `numen_theme.css` and `fonts/` (SIL Open Font License). Checks: `report_guard.py`.

**Records:** `FOG_COLD_RUN_FINDINGS.md` (every finding), the `FOG_*_REVIEW.md` files (the human review), `STORY_REPORT_SPEC.md`, `WALKTHROUGH_MAP.md`.

**Rebuild the pages** (no API calls):

```
python report_data.py
python report.py
python walkthrough.py
python demo_prototype/build_archetype_cards.py
```

**Run the tests:** `python -m unittest discover -p "test_*.py"`. The layout checks use headless Chrome and are skipped without it. The card builder needs `pdfplumber` and `Pillow`.

**Live AI runs** need the `anthropic` package and an `ANTHROPIC_API_KEY` set in your own environment; no key is stored in the repo. The runners have free dry-run or plan modes.
