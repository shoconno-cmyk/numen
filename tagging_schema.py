"""
tagging_schema.py -- structured data model for the archetype /
causal-integrity tagging layer (v6 schema), built from 15+ real
ground-truth findings across six works (Mystic River, Obsession,
Contact, Lethal Weapon, What Has To Be Done, plus supporting scenes).

CRITICAL DESIGN PRINCIPLE, non-negotiable:
  This module NEVER computes a judgment. Every judgment field here
  (archetype, chain_soundness, characterization_consistency, etc.) is
  populated by an external caller -- a human or an LLM doing real
  reading comprehension -- never derived by logic inside this module.
  This mirrors the beat-detection module's own honesty: signals.py
  detects textual PATTERNS (regex, sentiment scores); nothing in this
  project has ever claimed to detect MEANING. Tagging archetype and
  causal integrity requires understanding motive, consequence, and
  psychology -- categorically different from pattern-matching, and no
  amount of clever code turns one into the other.

  This module's actual job -- and its actual value, per direct
  discussion -- is to FORCE THE DISCIPLINE that unstructured judgment
  reliably fails to maintain on its own: the two-pass workflow, the
  evidence-citation requirement, honest non-tags over forced ones, and
  auditable state that survives past a single conversation. A populated
  ScriptAnalysis is a reusable asset; a paragraph of AI-generated
  coverage is not.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re


def beat_id_sort_key(beat_id):
    """Parse a 'sceneN_beatM' beat_id into a (scene_number, beat_number)
    integer tuple for TRUE narrative-order sorting.

    Confirmed via a real, live bug: plain string sorting of beat_ids
    (Python's default sorted()) scrambles narrative order, because
    'scene100' sorts before 'scene2' as a string comparison. In one
    real cold-run batch, this caused 'scene9_beat1' -- a beat from
    early in the film -- to be processed dead last, after scenes 95-99.
    Use this as the `key=` argument to sorted() anywhere beats need to
    be processed in genuine story sequence (e.g. before registry_context
    can meaningfully accumulate 'as of this beat' state -- that only
    means anything if beats are actually visited in story order first).
    Unparseable ids sort last rather than raising, so malformed/legacy
    beat_ids don't break a whole batch."""
    m = re.match(r'scene(\d+)_beat(\d+)', beat_id)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (float('inf'), beat_id)


# ---------------------------------------------------------------------
# Enums: every terminal/status state earned through real ground-truth
# beats this session. Comments cite the finding that produced each one.
# ---------------------------------------------------------------------

class LinkageType(Enum):
    PLOT_SETUP_PAYOFF = "plot_setup_payoff"
    THEMATIC_MOTIF = "thematic_motif"          # LW: a repeated line used as a callback


class LinkageConfidence(Enum):
    TEXTUALLY_CONFIRMED = "textually_confirmed"
    HIGH_CONFIDENCE_INFERRED = "high_confidence_inferred"
    ANALYTICALLY_DISCOVERED = "analytically_discovered"  # WHTBD: VA denial <-> discharge


class LinkageStatus(Enum):
    RESOLVED = "resolved"
    OPEN = "open"
    UNRESOLVED_NO_PAYOFF_FOUND = "unresolved_no_payoff_found"  # LW: Dick Lloyd photo, cut from film


class ResolutionDistance(Enum):
    SAME_SCENE = "same_scene"
    FEW_SCENES = "few_scenes"
    ACT_LEVEL = "act_level"
    WHOLE_SCRIPT = "whole_script"
    NONE_FOUND = "none_found"


class CommitmentStatus(Enum):
    OPEN = "open"
    FULFILLED = "fulfilled"
    BROKEN = "broken"
    MOOTED_BY_DEATH = "mooted_by_death"                      # LW: Lloyd dies before Murtaugh's vow is tested
    UNRESOLVED_NO_PAYOFF_FOUND = "unresolved_no_payoff_found"
    INTENTIONALLY_AMBIGUOUS = "intentionally_ambiguous"       # WHTBD: Cortes's true affiliation, author-confirmed


class KnowledgeState(Enum):
    KNOWN = "known"
    UNSTATED_AMBIGUOUS = "unstated_ambiguous"   # default for PRE-STORY facts (WHTBD fix)
    EXPLICITLY_IGNORANT = "explicitly_ignorant"  # only when text shows surprise/denial


class ChainSoundness(Enum):
    INTACT = "intact"
    BROKEN = "broken"
    UNDETERMINED = "undetermined"


class WeightProportionality(Enum):
    MATCHED = "matched"
    MISMATCH = "mismatch"                        # Obsession: an outsized wish for a small prompt
    REQUIRES_SECOND_PASS = "requires_second_pass"


class AgencyAlignment(Enum):
    ALIGNED = "aligned"
    DISPLACED = "displaced"                      # Contact: Hadden solves the primer, not Ellie


class CharacterizationConsistency(Enum):
    CONSISTENT = "consistent"
    CONTRADICTED = "contradicted"                # LW pier scene: studio-mandated Save the Cat beat
    THROUGHLINE_EVOLUTION = "throughline_evolution"  # LW ending: Riggs relinquishes the pills
    BOUNDARY_REVEALED = "boundary_revealed"      # WHTBD: Brianna's capitulation to Cortes
    REQUIRES_SECOND_PASS = "requires_second_pass"


class ConfidenceFlag(Enum):
    GROUNDED_IN_TEXT = "grounded_in_text"
    INTERPRETIVE_JUDGMENT = "interpretive_judgment"


class ArchetypeTagKind(Enum):
    """Most beats get a real archetype (Hero, Shadow, Trickster, Mentor,
    Great Mother, Chorus, Persona) as free-text from the Big Seven.
    These two are honest NON-tags, earned from real cast members this
    session, not placeholders:

    NO_CONFIDENT_ARCHETYPE vs ORDINARY_REACTION: NO_CONFIDENT_ARCHETYPE is
    for beats where the material itself is genuinely thin or minor -- not
    enough content to support a confident read of any kind. It is NOT a
    hedge for "this character might be doing something archetypal (e.g.
    Trickster) off-page, in a way the text doesn't show." Per the
    plot-facts boundary principle (never assert an archetype for action
    the beat's own text doesn't depict), the ABSENCE of on-page evidence
    for a specific archetype should increase confidence that a beat is
    non-archetypal, not decrease it. When the beat's visible, on-page
    content is otherwise clear and legible, that confident exclusion
    resolves to ORDINARY_REACTION, not NO_CONFIDENT_ARCHETYPE -- even when
    a structurally similar beat elsewhere (same character, same kind of
    action) DID earn an archetype tag. A nearby beat's Trickster tag does
    not create doubt about THIS beat's kind; each beat is judged only on
    what it actually shows."""
    NO_CONFIDENT_ARCHETYPE = "no_confident_archetype"   # WHTBD: Bud -- thin AND minor
    FUNCTIONAL_ROLE_ONLY = "functional_role_only"        # WHTBD: O'Neil/Betts -- major but psychologically opaque
    ORDINARY_REACTION = "ordinary_reaction"              # WHTBD: Jay discovering the truth -- legible emotion, not archetypal


# Explicit one-line criteria for each of the Big Seven, added after the
# Good Will Hunting full-script automated pass revealed a systemic
# over-application of Hero: without a written definition, the tagger
# (human or LLM) drifts toward using Hero as a stand-in for "this is a
# nice/admirable/growth-positive moment" rather than its actual, narrower
# meaning. Concrete examples of the bug this fixes: GWH scene63_beat1
# (two characters silently solving math together, zero stakes -- tagged
# Hero) and scene103_beat2 (Will's "it's not your fault" breakdown --
# tagged Hero when the beat is actually collapse/surrender, the opposite
# register). The fix is the same discipline as everything else in this
# schema: a criterion the tagger has to actually check against, not a
# vibe.
GENERAL_TAGGING_PRINCIPLES = (
    "NOT EVERY ARCHETYPE BELONGS IN EVERY STORY. A well-tagged script "
    "will often come back with zero, or near-zero, honest instances of "
    "one or more of the Big Seven -- this is an expected, healthy "
    "outcome, not a sign that the tagger missed something or needs to "
    "look harder. A story built entirely on adult peer relationships "
    "(partners, colleagues, an ensemble with no caregiver/dependent "
    "bond anywhere in the cast) may legitimately have no real home for "
    "Great Mother at all; a story where every character stays in "
    "controlled, deliberate command of themselves may legitimately have "
    "almost no Shadow. Do not treat a low or zero count for an "
    "archetype as evidence that the bar was set too high, and do not "
    "reach for a thinner, more marginal beat just to avoid an empty "
    "category. The count for each archetype should track what the "
    "story actually contains, not an assumption that all seven must be "
    "meaningfully represented. When in doubt, the honest answer is "
    "no_confident_archetype, not a strained fit.\n\n"
    "HEDGED NARRATIVE LANGUAGE IS NOT EVIDENCE OF THE THING IT HEDGES. "
    "Screenwriters routinely describe a moment through suggestive, "
    "unverified framing -- 'looks like he could,' 'seems to,' 'as if,' "
    "'almost' -- as a stylistic gloss on how a beat might read, not as "
    "a confirmed action or a confirmed internal state. 'Frank looks "
    "like he could leap across the table and strangle Richard' is NOT "
    "textual evidence that Frank feels murderous rage, wants to attack "
    "Richard, or is barely restraining violence -- it is the writer's "
    "own hedged suggestion of how the moment might land, and Frank "
    "never acts on it. This is a DIFFERENT failure from over-tagging: "
    "a tagger can look appropriately conservative by raw count while "
    "still resting the archetypes it DOES assign on this kind of "
    "misread evidence -- low volume does not mean the surviving tags "
    "are well-grounded, and this exact trap has produced confidently- "
    "argued Shadow, Hero, and Persona tags for moments the text never "
    "actually confirms. Contrast: an actual depicted action ('Frank "
    "lunges') or an explicit, unhedged internal-state note (a "
    "parenthetical like '(furious)', or a direct statement 'Frank is "
    "enraged') IS real evidence. A hedge is not a downgraded version "
    "of the same evidence -- it is the absence of evidence for the "
    "hedged claim, dressed in language that reads as if it were "
    "confirmation.\n\n"
    "PLOT FACTS AND ALREADY-DEPICTED PERFORMANCES: a later-confirmed plot "
    "fact (e.g. a confrontation was staged) licenses correcting an "
    "earlier beat's archetype tags and psychological fields when that "
    "earlier beat's own text already fully and specifically depicts the "
    "relevant exchange (real dialogue, real described behavior) -- the "
    "plot fact then supplies the TRUE NATURE of content already shown in "
    "full, which is interpreting depicted action, not asserting hidden "
    "action. It does NOT license retagging a beat whose text is "
    "genuinely thin or non-committal about what physically occurred (an "
    "unelaborated gesture, an ambiguous contact) -- there, the plot fact "
    "would be supplying the missing ACT itself, not just its meaning, "
    "which asserts content the beat's own text doesn't show. Test: does "
    "the earlier beat depict the actual exchange completely, such that "
    "the plot fact only supplies its valence? Or does it merely gesture "
    "at something ambiguous, such that using the plot fact would mean "
    "asserting an act the text never depicted? Example: a fully "
    "dramatized staged confrontation can be correctly retagged as a "
    "performance once later confirmed -- nothing invented, only "
    "correctly understood. A vague, uncommitted physical contact cannot "
    "be confidently retagged as the specific mechanism of an offscreen "
    "theft just because a theft is later confirmed nearby in time -- the "
    "text never depicted a taking, so locating the act there asserts "
    "more than the text shows.\n\n"
    "SHARED CONCEALMENT, DIFFERENT MOTIVES: two characters can jointly "
    "maintain the same concealed fact (e.g. hiding that they know each "
    "other) while earning different archetype tags, because the "
    "archetype tracks WHY each character conceals it, not the shared "
    "act of concealment itself. Ordinary self-protective motives "
    "(reputation, professional standing, a real relationship) point to "
    "Persona; opportunistic exploitation of a specific target for gain "
    "points to Trickster. The same scene, even the same beat, can "
    "require different tags per character for what looks like "
    "identical behavior on the surface. Relatedly: when two characters "
    "who share real history discuss it honestly with each other on the "
    "page -- even sardonically, even defensively -- that exchange is "
    "not automatically Trickster or Persona just because bystanders are "
    "being kept in the dark by its existence; per the Persona "
    "definition's own DEFENSIVE vs MASKED distinction, real feeling "
    "deployed for a self-protective purpose is not a mask if nothing "
    "about the feeling itself is false. The deceptive/concealing "
    "archetype, when warranted, attaches to the act of concealment from "
    "the uninformed party, not to genuine content exchanged between two "
    "people who already know the truth."
)
BIG_SEVEN_DEFINITIONS = {
    "Hero": (
        "Genuine courage or sacrifice under REAL, OUTWARD stakes/risk, in "
        "service of a goal or another person. NOT a stand-in for 'this "
        "moment is admirable, sympathetic, or growth-positive' -- a "
        "character quietly enjoying a stakes-free moment of connection, "
        "or breaking down in grief, is not thereby a Hero beat. Ask: is "
        "this character facing down a real external risk or opposition "
        "right now? If the only thing happening is an internal, "
        "vulnerable, or pleasant moment, Hero does not apply. FOR-ANOTHER "
        "TEST (per the actual Jungian hero archetype: courageous, "
        "determined, and selfless, sacrificing one's own safety to "
        "protect others): the courage must be in service of someone or "
        "something beyond the self, not self-preservation alone. Fleeing "
        "danger, escaping capture, or defending yourself when no one "
        "else is protected by the act -- however brave, clever, or "
        "successful -- does not clear this bar; that's ordinary_reaction "
        "or Trickster (if the method is resourceful/deceptive), not "
        "Hero. SUCCESS IS NOT REQUIRED: a genuine for-another attempt "
        "that fails or backfires still counts -- the Jungian hero's "
        "journey is defined by process and confrontation, not a "
        "flawless outcome; failure, defeat, and humility are as much a "
        "part of the archetype as victory. Judge whether the attempt "
        "was genuinely for another and genuinely courageous, not "
        "whether it worked. A sequence of actions in service of the "
        "same rescue/protection goal (subdue a threat, then approach to "
        "help) can count as one continuous Hero arc even when an early "
        "step is also immediately self-defensive. DECLARED INTENT IS NOT "
        "THE ACT ITSELF: a character voicing resolve, defiance, or a "
        "decision to act courageously -- however determined the words -- "
        "is not yet a Hero beat on its own. The tag belongs on the beat "
        "where the courageous action is actually taken or enacted, not "
        "merely announced. A beat can contain real emotional truth (a "
        "crack, a rupture, recomposing oneself) on the way toward a Hero "
        "moment without itself qualifying as one -- that earlier beat may "
        "be Shadow (the crack) and/or Persona (recomposing), with Hero "
        "landing on the later beat where the resolve actually becomes "
        "action."
    ),
    "Shadow": (
        "A repressed, denied, or disowned part of the self surfacing -- "
        "aggression, envy, cruelty, or a dark impulse breaking through a "
        "controlled exterior. The surfacing itself is the point, not "
        "just negative emotion in general. CHILD CHARACTERS: per actual "
        "Jungian developmental theory, Shadow requires a sufficiently "
        "formed ego to split FROM -- a young child's psyche is still "
        "assembling that ego, not yet organizing repressed material into "
        "something a Shadow could break through. A child's rage, "
        "obsessive fear, or violent outburst -- however severe -- is NOT "
        "Shadow, regardless of intensity; severity is the wrong axis to "
        "check. It's raw, undifferentiated distress, the future material "
        "Shadow will eventually be built from once the ego forms, not yet "
        "organized content breaking through one. Default to "
        "ordinary_reaction (however intense) for a young child's "
        "emotional/behavioral extremes. This scales with apparent "
        "developmental maturity, not a hard age cutoff -- an older "
        "child/teen with a more formed sense of self may legitimately "
        "earn Shadow; a young child (roughly pre-adolescent) essentially "
        "never should, no matter how dark the moment reads on the page. "
        "REQUIRES the surfacing to "
        "happen DESPITE the character's control -- a consciously chosen, "
        "openly-owned expression of anger or aggression (even if intense "
        "or confrontational) is NOT automatically Shadow; that's "
        "ordinary_reaction (if proportionate) or Trickster (if wielded "
        "as a deliberate test/tool). Edge case: content can surface "
        "'despite control' even while outward composure holds, if it's "
        "being compelled from somewhere beneath ordinary agency (e.g. "
        "repression, or -- script-specific -- supernatural influence) "
        "rather than freely chosen; a hypothetical/testing frame can "
        "itself be the tell of half-owned material being tried out, not "
        "yet consciously claimed. CONSCIOUSLY-EXAMINED pain is not "
        "Shadow either, even when passionately expressed and even when "
        "it doubles as projection onto someone else: if the character is "
        "aware of the material and actively working through it (not "
        "denying or repressing it), drawing on it -- however heatedly -- "
        "is a choice, not a surfacing. That's Mentor (if in service of "
        "someone else's growth) or ordinary_reaction, not Shadow. "
        "DOMAIN TEST for characters in a caregiving/parental bond "
        "(Babadook finding, ratified): Shadow is PERSONAL, individual-ego "
        "material -- grief, desire, isolation, trauma memory that exists "
        "independent of the caregiving relationship. If the darkness is "
        "instead enacted THROUGH, BECAUSE OF, or IN DEFENSE OF that "
        "relationship (reacting to the dependent's behavior, endangering "
        "them, aggression toward or on their behalf, a violent impulse "
        "toward the person being cared for), that belongs to Great "
        "Mother's dark pole instead -- even at the caregiver's total loss "
        "of control. The test is NOT composure vs. breakdown, it's whose "
        "domain the content belongs to: the personal unconscious (Shadow) "
        "or the caregiving bond itself (Great Mother, collective/"
        "archetypal, per the actual Jungian distinction between the "
        "personal Shadow and the Terrible/Devouring Mother). A caregiver "
        "screaming at, striking, or hunting the person they care for is "
        "Great Mother's dark pole even mid-collapse; the SAME caregiver's "
        "unrelated grief, sexuality, or personal trauma is Shadow."
    ),
    "Trickster": (
        "Mischief, deception, or boundary-testing that destabilizes a "
        "situation or social order -- deliberate misdirection, games, "
        "or provocation. Distinct from ordinary humor or banter, which "
        "is usually just ordinary_reaction. BULLYING IS NOT TRICKSTER: "
        "mockery whose only function is to demean a less-powerful or "
        "vulnerable target -- with no wit, no self-aware transgression, "
        "and nothing being destabilized beyond the victim's own "
        "standing -- is bullying, not Trickster, however playful or "
        "gleeful the perpetrator's own framing of it. Confirmed via two "
        "independent beats (pageant peers mocking a new girl's "
        "appearance; boys heckling a child mid-performance) where the "
        "cruelty served no purpose beyond humiliating the target. "
        "Trickster's mischief punches at a norm, an authority figure, "
        "or a social order; bullying just punches down at a person. "
        "Default to ordinary_reaction for the mocking party in these "
        "cases (or Shadow, if a genuine repressed-cruelty case is "
        "separately earned). "
        "NEGOTIATION/PRESSURE IS NOT TRICKSTER: Trickster requires an "
        "unaware mark -- someone who does not know, for at least this "
        "beat, that something is being done to them. Ask specifically "
        "WHO the mark is and whether THAT PERSON is unaware, not just "
        "whether deception exists anywhere in the scene; a character can "
        "knowingly watch a trick land on someone else without themselves "
        "being tricked. Leverage, ultimatums, or manipulative-but-"
        "transparent pressure applied to someone who fully understands "
        "what's happening and why is not Trickster, however sharp-elbowed "
        "the tactic -- that's ordinary_reaction, or a different archetype "
        "if separately earned. Confirmed via four beats in one connected "
        "sequence (Ocean's Eleven): a pickpocketing mark unaware his "
        "wallet is being lifted, a thief unaware his own haul is being "
        "re-stolen, and a recruiter unaware his own ticket is being "
        "lifted from under his hand -- versus, in the same sequence, a "
        "recruitment pitch built on ultimatums and invoked trust, where "
        "the target is fully aware of every move being made against him "
        "in real time. The first three are Trickster; the last is not, "
        "no matter how manipulative the pressure is."
    ),
    "Mentor": (
        "Guiding, teaching, or challenging another character's growth, "
        "usually from a position of earned experience or wisdom -- "
        "including flawed or self-interested mentorship. REQUIRES an "
        "actual piece of guidance or earned wisdom being transmitted "
        "toward the other character's growth or understanding -- NOT "
        "just speaking from a position of confidence, authority, or "
        "experience in general. REQUIRES the mentee to actually be "
        "present and addressed in the beat -- discussing your approach "
        "to helping someone, or defending your method, with a THIRD "
        "PARTY while the mentee isn't there is not Mentor, no matter how "
        "much genuine wisdom or conviction is on display. That's "
        "ordinary_reaction (or another archetype if one is earned by the "
        "actual content of the exchange with whoever IS present). Mentor "
        "and Trickster/Shadow are not mutually exclusive: a character "
        "can genuinely guide someone while also manipulating, testing, "
        "or extracting information from them in the same beat -- tag "
        "both when both are earned. But Mentor is never earned by tone "
        "of authority alone, and never earned by advocacy delivered to "
        "someone other than the mentee. PEER PLANNING vs. MENTORSHIP "
        "(ensemble/heist/team stories): a character sharing operational "
        "knowledge, technical explanations, or strategic ideas with "
        "fellow teammates as part of collaborative planning is NOT "
        "automatically Mentor, even when delivered with real expertise "
        "and even when a genuine skill gap exists between speaker and "
        "listener. The test stays the same as everywhere else: is THIS "
        "specific exchange oriented toward the listener's growth or "
        "understanding (Mentor), or is it operational information being "
        "shared/pooled as part of the team's shared task -- a technical "
        "explanation to the group, delegating who does what, briefing "
        "the crew on a target's layout? That's ordinary collaborative "
        "work (or Chorus, if genuinely stepping back to a detached "
        "verdict; or another archetype if separately earned), not "
        "mentorship, however much confidence or authority colors the "
        "delivery. Sustained, hands-on training of ONE specific person "
        "(drilling a rookie's cover story, correcting their form in real "
        "time) is a different thing from a competent leader briefing the "
        "whole team -- the former can be Mentor, the latter usually "
        "isn't."
    ),
    "Chorus": (
        "Commentary or context-providing function -- observing, "
        "narrating, or reacting on behalf of a group perspective, rather "
        "than being the one with something personally at stake in the "
        "moment. NOT the same as requiring the character to lack all "
        "personal stakes in the protagonist's story -- classic Chorus "
        "figures are very often the protagonist's close friend or "
        "intimate (the best friend, the confidant). What disqualifies a "
        "beat from Chorus is the character reacting from IMMEDIATE, LOCAL "
        "self-interest in that specific exchange (their own spouse, their "
        "own trauma, their own crisis unfolding right now) -- not whether "
        "they love or are personally connected to the protagonist in "
        "general. The real test: is this character stepping back to "
        "articulate something bigger than the moment -- a truth, a "
        "pattern, a verdict on the protagonist's whole trajectory -- even "
        "when delivered through real love and personal investment? That's "
        "Chorus. A character just reacting, in real time, to their own "
        "stake in what's unfolding right now is not, even if they're the "
        "protagonist's best friend. Passive/reactive witnessing of an "
        "unfolding personal crisis (watching someone you love break down "
        "right now) stays ordinary_reaction; a stepped-back verdict on "
        "their whole arc is Chorus, and can coexist with Mentor when the "
        "same words are also genuine guidance. TEAMMATE vs. OUTSIDER "
        "(ensemble/heist/mission stories): a character relaying "
        "operational information to a FELLOW active participant in the "
        "SAME shared mission (a crew member briefing another crew member "
        "on a target's habits, a colleague's background, the plan's "
        "risks) is not Chorus even when the content sounds expository --  "
        "they are inside the enterprise, personally invested in its "
        "success, not a detached voice commenting on it from outside. "
        "Chorus in this shape requires genuine outsider standing: a "
        "stranger with no stake in the mission volunteering a warning, or "
        "a character stepping back from the CURRENT mission to a "
        "genuinely separate context (past history, unrelated lore) rather "
        "than briefing a teammate on the operation itself. AMBIENT MEDIA: "
        "background television, radio, or news broadcast content that no "
        "character in the beat is shown actually receiving or reacting to "
        "is not Chorus (or any archetype) -- it's environmental texture, "
        "not commentary delivered to anyone in the story. Commentary "
        "requires an actual recipient engaging with it, even if that "
        "recipient is just the audience via a character's visible "
        "reaction."
    ),
    "Great Mother": (
        "Nurturing, protective, or all-encompassing care -- creating "
        "safety, holding space, or offering unconditional support. "
        "DUAL-POLE archetype (LOTB Tatakala finding, ratified): its dark "
        "inversion -- predatory, consuming, sacrifice-demanding, or "
        "possessively controlling (sometimes called the 'Terrible' or "
        "'Devouring' Mother in Jungian terms) -- belongs to the SAME "
        "archetype. ALWAYS write the tag value as \"Great Mother\" even "
        "for the dark pole -- never write \"Terrible Mother\" or "
        "\"Devouring Mother\" as the archetype value itself, those are "
        "descriptive terms for this beat's specific quality, not separate "
        "tag names. Tag Great Mother, not Shadow, when a caretaking "
        "figure's function turns devouring, consuming, or destructively "
        "possessive (a giver reclaiming/consuming what was given; "
        "protection curdling into control or predation). DOMAIN TEST "
        "(Babadook finding, ratified): the dark pole covers ANY darkness "
        "arising THROUGH the caregiving relationship itself -- fear, "
        "rage, violence, dissociation, or possessive control enacted "
        "toward, because of, or in defense of the dependent -- even at "
        "total loss of composure. Breakdown that happens WITHIN the "
        "caregiving relationship is still Great Mother's domain, not "
        "Shadow's, per the actual Jungian distinction between the "
        "personal Shadow (individual repressed ego material) and the "
        "Terrible/Devouring Mother (a collective, relational force). "
        "Reserve Shadow strictly for darkness that exists in the "
        "caregiver's own life independent of that bond -- grief, desire, "
        "isolation, or trauma memory unconnected to the dependent. "
        "Passing this domain test is NECESSARY but NOT SUFFICIENT for "
        "the dark pole -- ordinary, proportionate parental frustration "
        "or disappointment at a child's behavior does not automatically "
        "curdle into Great Mother's dark pole just because it's "
        "relationally-triggered. THE DARK POLE IS AN OVERCORRECTION OF "
        "THE LIGHT POLE, not a separate category of maternal-adjacent "
        "violence: it must be traceable to an actual caregiving/"
        "protective impulse (wanting to keep the dependent safe, close, "
        "compliant, or dependent) taken to a smothering, controlling, or "
        "harmful extreme -- possessively preventing their independent "
        "growth, punishing them for seeking outside help or connection, "
        "demanding compliance as proof of loyalty, controlling their "
        "access to others. If the darkness has NO connection to a "
        "caretaking motive -- if it's really unrelated personal rage, "
        "grief, or (script-specific) possession by an external force "
        "simply finding its outlet through the dependent -- that's "
        "Shadow, even when it's enacted toward them and even when it "
        "involves literal violence or predation. Predation or violence "
        "toward a dependent is NOT automatically the dark pole just "
        "because of who it's aimed at; ask whether it grew out of a "
        "caregiving impulse gone too far, or whether it's a separate "
        "darkness (rage, grief, an invasive force) that has nothing to "
        "do with care and is merely using the dependent as its target. "
        "An extreme but ORDINARY outburst -- even a genuinely ugly one, "
        "born of exhaustion or momentary loss of temper, that doesn't "
        "functionally control or endanger the child -- is NOT the dark "
        "pole either; it's just ordinary_reaction at high intensity. A "
        "parent's ordinary exasperation at a child breaking something is "
        "ordinary_reaction, not the dark pole, even though it's about "
        "the child specifically. WITNESSED vs. ENACTED: a character "
        "reading, watching, or being shown fictional-within-fiction "
        "imagery of devouring-mother content (a scary book, a film, a "
        "story) is NOT themselves exhibiting the dark pole -- archetypal "
        "weight belongs to what a character actually DOES, not to "
        "content they passively perceive, however thematically "
        "prophetic. That's ordinary_reaction (fear/dread at something "
        "disturbing), not Great Mother."
    ),
    "Persona": (
        "A controlled, curated front maintained over real feeling -- the "
        "mask a character wears, deliberately or habitually, to manage "
        "how they're perceived. CHILD CHARACTERS: per actual Jungian "
        "theory, the Persona (the social mask adapted to school/work/"
        "society's expectations) is only beginning to seed in a young "
        "child, not yet the differentiated structure it becomes in an "
        "adult. Apply significant extra skepticism -- a simple, "
        "instinctive gesture (a brief smile for a tired parent, "
        "trembling while still saying something brave, flatly relaying a "
        "fact the way it was always explained to them) is basic comfort-"
        "seeking or social mirroring, NOT a strategic social mask. "
        "Reserve Persona for a child only when there's a clearly "
        "articulated, sustained, DELIBERATE performance -- an elaborate "
        "trick, a maintained lie, active concealment the child is "
        "consciously managing (which still lands on Trickster if it's "
        "behavioral deception rather than concealing a felt emotional "
        "state) -- not a momentary, unselfconscious reaction. This scales "
        "with apparent developmental maturity like Shadow's child clause, "
        "not a hard age cutoff. REQUIRES a textually evident GAP between "
        "what's felt and what's shown. Quiet, withdrawn, reserved, "
        "vulnerable, or deflecting behavior is NOT automatically Persona "
        "-- check whether the surface reaction is congruent with the "
        "character's actual state (then it's ordinary_reaction) or is "
        "genuinely covering something different (then it's Persona). "
        "The moment a mask BREAKS or cracks is not itself Persona -- "
        "that's the reveal of whatever's underneath (which may be "
        "ordinary emotion, or a different archetype entirely), not the "
        "performance. DEFENSIVE is not the same as MASKED: a character "
        "can weaponize their own genuine, unhidden truth for a "
        "self-protective purpose (e.g. preemptively pushing someone away "
        "with real pain to avoid future abandonment) without that being "
        "Persona -- if the feeling on display IS the real feeling, "
        "there's no gap to tag, no matter how strategic or defensive its "
        "deployment is. Persona requires concealment, not just strategy. "
        "CAREGIVING UNDER STRAIN vs. PERSONA: pushing through genuine "
        "difficulty -- exhaustion, grief, fear -- to still show up for a "
        "dependent (forced brightness, strained reassurance, a tight but "
        "present 'I love you too') is Great Mother's light pole or "
        "ordinary_reaction, NOT Persona, when it's a direct exchange WITH "
        "the dependent themselves. Persona requires managing PERCEPTION, "
        "which implies an audience whose view of you is being curated -- "
        "typically a third party, not the person you're actively caring "
        "for in the moment. The test: is this a front managed for how "
        "someone perceives you (Persona), or is it the caregiving bond "
        "itself straining under real difficulty, directed at the "
        "dependent (Great Mother)? 'As bright as she can,' 'as sincerely "
        "as she can' -- delivered to the child being cared for -- are the "
        "caregiving function itself under strain, not calculated "
        "self-presentation. DECEPTIVE TOOL vs. SOCIAL MASK: per the "
        "actual Jungian Persona -- the mask worn to meet ORDINARY "
        "society's demands (personal dignity, institutional presentation, "
        "a real relationship) -- a disguise or false identity built "
        "SPECIFICALLY as a tool to deceive a particular mark or target "
        "(a fake name, a fabricated profession, a costume assumed for a "
        "con or undercover operation, rehearsing an accent to fool "
        "someone) is Trickster's domain, not Persona's, even though both "
        "loosely involve 'wearing a mask.' The test: is this presentation "
        "serving ordinary social function (navigating normal life, "
        "relationships, or institutions), or is it a deliberately "
        "engineered deceptive tool built to manipulate a specific target "
        "as part of a scheme? A character rehearsing a false name to fool "
        "a mark is Trickster; the same character's genuine social "
        "awkwardness or personal front with people who actually know them "
        "is Persona. The two can coexist in the same beat when a "
        "scheme-directed deception and a separate, genuine personal "
        "concealment are both happening at once, but neither is assumed "
        "just because the other is present."
    ),
}


class Provenance(Enum):
    """Who actually produced a beat's judgment fields. Coarse-grained,
    at the BeatTag level -- the fine-grained record of WHAT was
    corrected lives separately in the Correction log, since corrections
    in practice (this whole session) were almost always about specific
    fields, not a beat's entire tagging being wrong."""
    HUMAN = "human"
    LLM_UNREVIEWED = "llm_unreviewed"
    LLM_HUMAN_CONFIRMED = "llm_human_confirmed"
    LLM_HUMAN_CORRECTED = "llm_human_corrected"


# ---------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------

@dataclass
class ScriptVersion:
    """Every analysis is scoped to ONE specific draft, never to 'the
    story' as an abstraction -- a Linkage confirmed in one draft can be
    cut in a later one without being a contradiction (LW: Dick Lloyd
    photo, confirmed in this draft, absent from the released film)."""
    title: str
    stage: str  # "spec" | "rewrite" | "mid-development draft" | "shooting script" | "released film"
    identifying_features: list = field(default_factory=list)

    def to_dict(self):
        return {"title": self.title, "stage": self.stage,
                "identifying_features": self.identifying_features}

    @classmethod
    def from_dict(cls, d):
        return cls(title=d["title"], stage=d["stage"],
                    identifying_features=d.get("identifying_features", []))


@dataclass
class Commitment:
    """An explicit promise/contract between characters, or a flagged
    open informational thread, tracked as a discrete object across the
    whole script -- never assessed from a single beat in isolation."""
    commitment_id: str
    made_by: str
    made_to: str
    content: str
    beat_made: str
    status: CommitmentStatus = CommitmentStatus.OPEN
    beat_resolved: Optional[str] = None
    notes: str = ""

    def to_dict(self):
        return {
            "commitment_id": self.commitment_id, "made_by": self.made_by,
            "made_to": self.made_to, "content": self.content, "beat_made": self.beat_made,
            "status": self.status.value, "beat_resolved": self.beat_resolved, "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            commitment_id=d["commitment_id"], made_by=d["made_by"], made_to=d["made_to"],
            content=d["content"], beat_made=d["beat_made"],
            status=CommitmentStatus(d["status"]), beat_resolved=d.get("beat_resolved"),
            notes=d.get("notes", ""),
        )


@dataclass
class BeatLinkage:
    """A connection between two non-adjacent beats -- a plot setup/
    payoff, or a thematic motif restated later. Confidence and status
    history are preserved, not overwritten, since the SAME linkage can
    be high_confidence_inferred at one point in a read-through and
    textually_confirmed later (LW: Dick Lloyd photo, resolved this way
    within the same draft)."""
    beat_a: str
    beat_b: str
    linkage_type: LinkageType
    confidence: LinkageConfidence
    status: LinkageStatus = LinkageStatus.OPEN
    resolution_distance: Optional[ResolutionDistance] = None
    author_ratified: Optional[bool] = None # required (not None) when confidence == ANALYTICALLY_DISCOVERED
    resolution_history: list = field(default_factory=list)  # [{"as_of_beat": ..., "confidence_at_that_point": ...}]
    notes: str = ""

    def validate(self):
        if self.confidence == LinkageConfidence.ANALYTICALLY_DISCOVERED and self.author_ratified is None:
            raise ValueError(
                f"Linkage {self.beat_a}<->{self.beat_b}: analytically_discovered "
                "linkages MUST have author_ratified set (True or False) -- "
                "this cannot be presented as fact until the author confirms it."
            )

    def to_dict(self):
        return {
            "beat_a": self.beat_a, "beat_b": self.beat_b,
            "linkage_type": self.linkage_type.value, "confidence": self.confidence.value,
            "status": self.status.value,
            "resolution_distance": self.resolution_distance.value if self.resolution_distance else None,
            "author_ratified": self.author_ratified,
            "resolution_history": self.resolution_history, "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            beat_a=d["beat_a"], beat_b=d["beat_b"],
            linkage_type=LinkageType(d["linkage_type"]),
            confidence=LinkageConfidence(d["confidence"]),
            status=LinkageStatus(d["status"]),
            resolution_distance=ResolutionDistance(d["resolution_distance"]) if d.get("resolution_distance") else None,
            author_ratified=d.get("author_ratified"),
            resolution_history=d.get("resolution_history", []),
            notes=d.get("notes", ""),
        )

@dataclass
class HeldValue:
    """A value or duty a character holds, tracked across the whole
    script. Built because 'boundary_revealed' depends on a RELATIONAL
    fact a flat throughline entry cannot express: not just 'character
    holds value X,' but 'has X ever been forced into direct conflict
    with Y before, when, and how did it resolve' -- plus a SEPARATE
    fact: has this value's own legitimacy been quietly undermined by
    something the character learned, independent of any direct
    conflict, changing the weight it carries once a conflict does
    arrive (WHTBD: Brianna discovering her own institution's corruption
    didn't create her final conflict with Cortes, but made professional
    duty easier to set aside once that conflict actually happened)."""
    character: str
    value_name: str
    established_scene_id: int
    description: str
    tested_against: list = field(default_factory=list)
    # each entry: {"opposing_value": str, "scene_id": int,
    #              "in_direct_conflict": bool, "outcome": str, "trigger": str | None}
    undermined_by: list = field(default_factory=list)
    # each entry: {"scene_id": int, "description": str}
    # -- events that erode this value's perceived legitimacy WITHOUT
    # directly testing it against another value yet

    def record_conflict(self, opposing_value, scene_id, in_direct_conflict, outcome, trigger=None):
        self.tested_against.append({
            "opposing_value": opposing_value, "scene_id": scene_id,
            "in_direct_conflict": in_direct_conflict, "outcome": outcome, "trigger": trigger,
        })

    def record_undermining(self, scene_id, description):
        self.undermined_by.append({"scene_id": scene_id, "description": description})

    def has_ever_conflicted_with(self, opposing_value, before_scene_id=None):
        """Has this value been placed in direct conflict with the named
        opposing value BEFORE the given scene? Defaults to checking
        across all recorded history if no scene is given, but when
        checking FROM WITHIN a scene, before_scene_id must be passed --
        otherwise a conflict recorded for the current scene itself
        would make this return True even when asking 'was this the
        first time,' which is the opposite of what's needed."""
        return any(
            t["opposing_value"] == opposing_value and t["in_direct_conflict"]
            and (before_scene_id is None or t["scene_id"] < before_scene_id)
            for t in self.tested_against
        )

    def to_dict(self):
        return {
            "character": self.character, "value_name": self.value_name,
            "established_scene_id": self.established_scene_id, "description": self.description,
            "tested_against": self.tested_against, "undermined_by": self.undermined_by,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            character=d["character"], value_name=d["value_name"],
            established_scene_id=d["established_scene_id"], description=d["description"],
            tested_against=d.get("tested_against", []), undermined_by=d.get("undermined_by", []),
        )


@dataclass
class CharacterRegistryEntry:
    """Persistent per-character record, built incrementally across the
    whole read-through, never finalized from a single beat."""
    character: str
    defining_activity: str = ""  # what this character's arc is characteristically FOR
    # beat-indexed, NOT a single fixed string (LW: Riggs' throughline
    # genuinely changes mid-script; treating it as one static value
    # would have made his ending read as a contradiction of his start).
    #
    # Each entry: {"scene_id": int, "beat_number": int, "state": str}.
    # CONFIRMED BUG (caught via real WHTBD testing): using free-text
    # beat-id strings (e.g. "scene66", "scene147_death") for ordering
    # is unsafe -- "scene147_death" <= "scene66" is TRUE as a plain
    # string comparison (since '1' < '6' character-by-character), even
    # though scene 147 comes narratively after scene 66. Ordering must
    # be tied to the actual numeric scene_id the parser already
    # establishes, never to an opaque label's lexicographic order.
    established_goal_throughline: list = field(default_factory=list)
    psychological_state_notes: list = field(default_factory=list)
    # facts predating the story's own timeline default to UNSTATED_AMBIGUOUS,
    # never EXPLICITLY_IGNORANT, unless the text shows real surprise/denial
    relationship_knowledge: dict = field(default_factory=dict)  # {other_character: {fact: KnowledgeState}}
    held_values: dict = field(default_factory=dict)  # {value_name: HeldValue}

    def throughline_as_of(self, scene_id, beat_number=0):
        """Return the most recent throughline entry at or before
        (scene_id, beat_number), for checking a beat against the
        character's state AT THAT POINT, not their final/eventual
        state. Compares numeric tuples, never strings."""
        target = (scene_id, beat_number)
        applicable = [
            e for e in self.established_goal_throughline
            if (e["scene_id"], e.get("beat_number", 0)) <= target
        ]
        if not applicable:
            return None
        applicable.sort(key=lambda e: (e["scene_id"], e.get("beat_number", 0)))
        return applicable[-1]["state"]

    def add_held_value(self, value_name, established_scene_id, description):
        self.held_values[value_name] = HeldValue(
            character=self.character, value_name=value_name,
            established_scene_id=established_scene_id, description=description,
        )
        return self.held_values[value_name]

    def get_held_value(self, value_name):
        return self.held_values.get(value_name)

    def to_dict(self):
        return {
            "character": self.character, "defining_activity": self.defining_activity,
            "established_goal_throughline": self.established_goal_throughline,
            "psychological_state_notes": self.psychological_state_notes,
            "relationship_knowledge": {
                other: {fact: state.value for fact, state in facts.items()}
                for other, facts in self.relationship_knowledge.items()
            },
            "held_values": {name: hv.to_dict() for name, hv in self.held_values.items()},
        }

    @classmethod
    def from_dict(cls, d):
        entry = cls(
            character=d["character"], defining_activity=d.get("defining_activity", ""),
            established_goal_throughline=d.get("established_goal_throughline", []),
            psychological_state_notes=d.get("psychological_state_notes", []),
        )
        entry.relationship_knowledge = {
            other: {fact: KnowledgeState(state) for fact, state in facts.items()}
            for other, facts in d.get("relationship_knowledge", {}).items()
        }
        entry.held_values = {
            name: HeldValue.from_dict(hv) for name, hv in d.get("held_values", {}).items()
        }
        return entry  


@dataclass
class ArchetypeTag:
    """Per-character archetype read for one beat. Multi-valued,
    perspective-split, and layered by design (Finding 1-3): a single
    beat can give one character several archetypes at once, and the
    character's own read of their action can differ from the
    audience's (Finding 2).

    causal_integrity lives HERE, per character, not on BeatTag.
    Migrated after real data loss was found: a shared beat with
    multiple present characters can genuinely diverge on
    weight_proportionality/characterization_consistency (Richard's
    ice-cream lecture was a real 'mismatch' while Sheryl's own
    reaction in the SAME beat was proportionate) -- a single
    beat-level field can only hold one character's true read,
    silently discarding any other's the moment a second character's
    pass touches the same beat. Confirmed via real LMS data: 8 of 17
    beats shared across this session's Pass 2 work had a genuine
    conflict, not a rare edge case."""
    character: str
    kind: Optional[ArchetypeTagKind] = None  # set ONLY for the two honest non-tags
    archetypes: list = field(default_factory=list)  # e.g. ["Hero", "Shadow"] -- empty if kind is set
    self_perceived: list = field(default_factory=list)
    audience_perceived: list = field(default_factory=list)
    emotion: list = field(default_factory=list)  # layered/compound, e.g. ["bloodlust", "proxy revenge"]
    goal: Optional[str] = None  # None/"goalless" is a valid, real value (Chigurh)
    goal_status: Optional[str] = None  # achieved | violated | deferred | none -- per character, asymmetric
    agency_role: Optional[str] = None  # active | passive
    moral_coloring: Optional[str] = None  # deliberately separate from archetype label (Finding 8)
    embodies: Optional[str] = None  # required when kind == FUNCTIONAL_ROLE_ONLY, e.g. "institutional Shadow"
    causal_integrity: Optional["CausalIntegrityTag"] = None  # per-character; see class docstring above

    def validate(self):
        if self.kind == ArchetypeTagKind.FUNCTIONAL_ROLE_ONLY and not self.embodies:
            raise ValueError(f"{self.character}: functional_role_only requires 'embodies' to be set.")
        if self.kind and self.archetypes:
            raise ValueError(
                f"{self.character}: a character gets EITHER real archetypes OR a "
                "kind (no_confident_archetype/functional_role_only), never both -- "
                "forcing a label alongside a non-tag defeats the point of the non-tag."
            )
        invalid = [a for a in self.archetypes if not isinstance(a, str) or a not in BIG_SEVEN_DEFINITIONS]
        if invalid:
            raise ValueError(
                f"{self.character}: archetypes must be Big Seven values only, got "
                f"invalid value(s) {invalid!r} -- non-tag verdicts (e.g. 'ordinary_reaction') "
                "belong in 'kind', never inside 'archetypes'."
            )
        if self.causal_integrity:
            self.causal_integrity.validate()

    def to_dict(self):
        return {
            "character": self.character, "kind": self.kind.value if self.kind else None,
            "archetypes": self.archetypes, "self_perceived": self.self_perceived,
            "audience_perceived": self.audience_perceived, "emotion": self.emotion,
            "goal": self.goal, "goal_status": self.goal_status, "agency_role": self.agency_role,
            "moral_coloring": self.moral_coloring, "embodies": self.embodies,
            "causal_integrity": self.causal_integrity.to_dict() if self.causal_integrity else None,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            character=d["character"],
            kind=ArchetypeTagKind(d["kind"]) if d.get("kind") else None,
            archetypes=d.get("archetypes", []), self_perceived=d.get("self_perceived", []),
            audience_perceived=d.get("audience_perceived", []), emotion=d.get("emotion", []),
            goal=d.get("goal"), goal_status=d.get("goal_status"), agency_role=d.get("agency_role"),
            moral_coloring=d.get("moral_coloring"), embodies=d.get("embodies"),
            causal_integrity=CausalIntegrityTag.from_dict(d["causal_integrity"]) if d.get("causal_integrity") else None,
        )


CAUSAL_INTEGRITY_PRINCIPLES = (
    "Eleven principles earned through real Pass 2 review, LMS full-cast session, the "
    "Ocean's Eleven LINUS pilot and the Full of Grace cold run -- read "
    "carefully before resolving weight_proportionality or characterization_consistency. "
    "Each corrects a specific, real error the model made on a first-pass draft before "
    "author review, not a hypothetical concern:\n\n"

    "1. ADAPTING TO DIFFERENT PEOPLE IS NOT EVOLUTION. A character who calibrates HOW they "
    "express an established trait to fit each specific person or situation (blunt crude "
    "advice for a teenager, gentle reassurance for a frightened child, direct honesty about "
    "a hard truth for a grieving adult) has NOT changed -- this is the trait working "
    "correctly, not developing. Real error caught: an early draft read a character's shift "
    "from broad, provocative mischief (with peers/adults) toward focused tenderness (with a "
    "child in crisis) as gradual evolution. The correct read: one integrated trait, "
    "consistently well-calibrated throughout, mistaken for change only because the story "
    "gives the character more scenes with the one person who needed the gentler register.\n\n"

    "2. A VALUE'S FIRST FULL EXPRESSION IS NOT THE SAME AS THE VALUE FORMING. A character "
    "voicing or acting on a belief for the first time in the text does not mean that belief "
    "is new to them. Check whether the STORY is giving the character its first genuine "
    "OPPORTUNITY (the right listener, the right moment) rather than manufacturing a new "
    "capacity. Real error caught: a character's fullest articulation of a hard-won "
    "philosophy about suffering, delivered to someone finally ready to hear it, was "
    "initially read as new growth. The correct read: he'd always held this; the story "
    "simply hadn't yet given him someone to say it to.\n\n"

    "3. RESOLUTION CAN BE CONVERSION OR RELEASE, NOT ONLY VICTORY. When a HeldValue is "
    "tested against reality itself (not another character's competing value), the character "
    "does not need to WIN the conflict for it to resolve. Internalizing what the "
    "conflict revealed, and releasing the need to control what was never controllable, is a "
    "complete and positive resolution in its own right -- do not force a 'defeated vs. "
    "triumphant' framing onto every conflict.\n\n"

    "4. A CHARACTER CAN BE THE FIXED POINT OTHERS' ARCS ORBIT, WITHOUT AN ARC OF THEIR OWN. "
    "Especially plausible for child characters or any character established as an authentic "
    "core from their first appearance: 'consistent' across every single beat, including the "
    "story's climax, is not an under-analyzed or lazy result -- it can be the correct, "
    "load-bearing structural finding. Check whether OTHER characters' arcs are tested "
    "against or triggered by this character's unmoving presence before assuming a beat this "
    "prominent must represent the character's own change.\n\n"

    "5. THE SAME NAMED TRAIT CAN ESCALATE INTO SOMETHING QUALITATIVELY DIFFERENT. Correctly "
    "identifying a stable underlying impulse does NOT mean every instance of it is "
    "interchangeable -- the SCALE, COST, or RISK of a specific instance can itself be the "
    "signal of genuine evolution, even while the trait's own NAME stays constant. Real error "
    "caught: a synthesis correctly named a character's 'takes decisive charge in family "
    "crises' trait from an early, low-stakes beat (routine household logistics), then used "
    "that SAME trait label to wave through a much later beat where the character broke the "
    "law and physically risked real consequences to protect that same crisis -- missing that "
    "the magnitude jump between 'organizing logistics' and 'criminal risk-taking' IS the "
    "evolution, not evidence against one. Before marking a beat 'consistent' because it "
    "matches an established trait's name, check whether its actual scale/cost/stakes are "
    "comparable to the beat where that trait was first established. A trait escalating past "
    "what it has ever previously cost the character is itself evidence FOR throughline_"
    "evolution, not against it.\n\n"

    "6. EXHAUSTIVE SEARCH DOES NOT MEAN A LOWER BAR FOR WHAT COUNTS. Searching every beat "
    "thoroughly for a turning point is not the same as finding one in every beat you search. "
    "A strong, resonant, even emotionally costly INSTANCE of an already-established trait is "
    "still just 'consistent' -- it only becomes throughline_evolution or boundary_revealed if "
    "you can name a SPECIFIC comparison (see Principle 7 for the three valid shapes this can "
    "take) that concretely justifies it, not just that the beat feels significant in "
    "isolation. Real error caught: a synthesis pass tuned (via Principle 5's own lesson) to "
    "hunt harder for genuine escalation on one character -- whose arc did have several real "
    "ones -- applied the exact same hunting posture to a different character whose arc "
    "genuinely doesn't have many, and manufactured four false positives: each one an "
    "emotionally resonant but ordinary instance of an already-established value in action (a "
    "mother keeping a promise, correcting harmful messaging, giving a son space, defending a "
    "daughter's autonomy), not a real escalation past anything. Quantified cost: the "
    "resulting causal-integrity resolution scored WORSE than a trivial baseline that just "
    "guesses 'consistent' every time. If you cannot name a concrete comparison, it is not a "
    "turning point -- it's the trait working correctly, which happens throughout a story "
    "without each instance being remarkable. A short or even EMPTY turning_points list is not "
    "evidence of an insufficiently thorough search -- for a character whose narrative role is "
    "to remain a stable, reliable presence others' arcs are tested against (Principle 4), "
    "finding almost nothing IS the correct, honest result of real thoroughness, not a sign to "
    "keep looking until something turns up.\n\n"

    "7. NOT EVERY TURNING POINT IS AN ESCALATION -- CONTINUATION AND ECHO ARE EQUALLY REAL. "
    "Requiring every turning point to 'exceed' a specific earlier beat in scale/cost/risk "
    "correctly filters out the manufactured false positives Principle 6 describes, but also "
    "filters out two other genuine shapes of significance. A CONTINUATION beat is the direct, "
    "unbroken extension of an already-identified turning point -- not a separate escalation "
    "past it, the same event simply continuing (a body-smuggling plan and the physical act of "
    "climbing out the window carrying the body are one sequence, not two independent "
    "escalations). An ECHO beat concretely reverses or answers an earlier established "
    "statement, rule, or motif WITHOUT needing to be bigger or costlier than what it's "
    "answering -- its significance is in being a precise, textually concrete answer (the same "
    "prop, the same phrase, the opposite of a rule the character themselves stated), not in "
    "scale. A single quiet line can outweigh an elaborate earlier scene if it's a precise "
    "answer to it. Real error caught: fixing Principle 6's false-positive problem by requiring "
    "an escalation-shaped comparison for every turning point cost real recall on a character "
    "whose gains had already been validated -- a genuine sequence-continuation and the film's "
    "own closing line (a single understated sentence reversing an established motif) were "
    "both lost, specifically because neither fits the escalation shape, even though each is "
    "independently well-evidenced. Classify every turning point by which of the three shapes "
    "it actually is -- escalation, continuation, or echo -- and apply that shape's own test, "
    "not one shape's test to all three.\n\n"

    "8. BOUNDARY_REVEALED REQUIRES A NEW LIMIT, NOT JUST HIGH STAKES. A beat "
    "where a character succeeds at something harder, riskier, or more "
    "dangerous than anything they've attempted before is not automatically "
    "boundary_revealed -- success at an escalated version of an established "
    "capacity is throughline_evolution (an escalation-shaped turning point, "
    "Principle 7), not a boundary. boundary_revealed requires the beat to "
    "expose something previously unknown that recontextualizes or limits the "
    "character -- a genuine capitulation, breaking point, or discovered "
    "weakness -- not merely elevated stakes. Real error caught: a Pass 2 "
    "pilot run predicted boundary_revealed on 8 of a character's beats where "
    "the human-verified read was throughline_evolution or consistent -- "
    "every one of them a case of the character succeeding at increasingly "
    "risky action, never actually failing or being limited by anything. "
    "Test: does this beat teach us something genuinely new about what the "
    "character is capable of -- whether a limit, a weakness, or a "
    "strength/capacity never previously shown -- that changes how we read "
    "them going forward? Or did an established strength simply extend "
    "further while still working?\n\n"

    "8a. ORDINARY TRAIT DEBUT VS. SINGULAR CLIMACTIC ACTION. Principle 2 "
    "('a value's first full expression is not the same as the value "
    "forming') governs the ordinary debut of a baseline personality trait "
    "-- devotion, deflection, camaraderie, habitual coping. Those traits "
    "exist to establish who someone normally is, so their first on-page "
    "appearance is, by design, not dramatically significant. But a "
    "singular, climactic action -- personally committing violence, "
    "crossing into legal obstruction, declaring an irreversible intention "
    "-- is a different kind of thing even when it is trivially 'the first "
    "time we see it.' The test for THIS kind of beat is not 'has this "
    "exact capacity been shown before' but 'did the character's broader "
    "established pattern make this plausible, foreseeable, "
    "already-in-motion?' If nothing about the character's prior behavior "
    "made this crossing predictable, boundary_revealed stands even at the "
    "beat that is also that capacity's first instance in the script. "
    "Relationship to the default first-showing rule: an ordinary trait's "
    "first appearance stays consistent (Principle 2; the trait-identity "
    "gate, where a standalone trait's first showing is consistent) -- 8a "
    "is the deliberate EXCEPTION to that default for singular climactic "
    "actions specifically, which are judged on foreseeability from the "
    "character's broader pattern even when the beat is also that "
    "capacity's first or only instance. Worked example: TRUDY scene214_beat4 (Full of Grace; personally "
    "forcing Holly underwater) is the first instance of this specific "
    "capacity in her arc -- the later strikes at scene216_beat5 escalate "
    "it -- and correctly stands as boundary_revealed rather than being "
    "demoted to a mundane first-showing under Principle 2: nothing in her "
    "prior caregiving or faith behavior made this foreseeable.\n\n"

    "8b. CHECK THAT THE 'ESTABLISHED CAPACITY' BEING ESCALATED IS ACTUALLY "
    "THE SAME CAPACITY. Before scoring a beat as an escalation of an "
    "established trait, verify the comparison beat's capacity is genuinely "
    "the SAME kind of thing, not a different capacity smuggled in under a "
    "shared surface theme (danger, defiance, risk, loyalty). Real error "
    "caught: JOHN's synthesis (Full of Grace) tracked 'willing to defy "
    "direct orders/warnings and escalate physical risk' as one continuous "
    "trait running from reckless risk TO HIMSELF (tackling a fleeing "
    "suspect, forcing his own locked door, carrying a weapon for "
    "readiness) all the way through willingness to use LETHAL FORCE "
    "AGAINST ANOTHER PERSON (scene172_beat6). These share a surface theme "
    "(danger, defiance of caution) but are not the same capacity -- risk "
    "to self and willingness to kill another person are different in "
    "kind, and nothing in John's own history tested the second one before "
    "scene172_beat6. The beat was initially mis-scored as "
    "throughline_evolution (an escalation of the combined trait) when it "
    "should have been boundary_revealed under 8a (a singular climactic "
    "action with no prior foreseeable basis, once the conflated trait is "
    "correctly split).\n\n"

    "9. A PLOT PAYOFF IS NOT THE SAME AS A CHARACTER TURNING POINT. A beat "
    "can be dramatically loud because it's the moment a scheme's mechanism "
    "is finally revealed to the reader/audience (a PLOT_SETUP_PAYOFF "
    "cashing in) without anything about the character's own behavior "
    "actually shifting -- the drama belongs to the plot's construction, "
    "not to the character's arc. Test: strip away what the READER now "
    "understands and ask what the CHARACTER is actually doing differently "
    "in this beat compared to the beats immediately before it. If the "
    "answer is 'nothing -- they're still doing the same thing, we just "
    "finally see why' or 'what it accomplishes,' this is consistent (or a "
    "continuation of an already-identified turning point), not a new "
    "boundary_revealed or throughline_evolution. Real error caught three "
    "times across two characters: LINUS's Sheldon Wills con payoff (the "
    "mask visibly dropping, the stolen combination finally shown), and "
    "RUSTY's cage-extraction payoff and exact cash-count reveal during the "
    "Benedict call -- in all three, the character's own composure and "
    "method never changed; only the audience's information did.\n\n"

    "10. AN ECHO NEEDS THE CHARACTER'S OWN EVIDENCE, NOT JUST ANOTHER "
    "CHARACTER'S LINE. A beat where only another character acts or speaks, "
    "with no corresponding action or line from the character being tracked, "
    "does not qualify as a turning point on its own -- even if it "
    "thematically answers an earlier beat of theirs. Another character's "
    "line can support an echo reading, but the tracked character's own "
    "action or line in that same beat must be the primary evidence. Real "
    "error caught: TRUDY's synthesis (Full of Grace) listed scene217_beat1 "
    "as an echo of her baptismal liturgy on the strength of JOHN's closing "
    "line alone.\n\n"

    "11. AN ACT CAN BE A TURNING POINT THROUGH IRREVERSIBILITY ALONE, EVEN "
    "WITHOUT VIOLENCE OR ESCALATED INTENSITY. Test: could the character "
    "still turn back from this specific action once taken, or has something "
    "been crossed that cannot be undone? This applies to physical acts and "
    "verbal acts alike -- speech is itself a form of action (the body "
    "producing it is a physical event), but unlike a purely physical act (a "
    "gunshot's irreversibility is self-evident from the act itself), a "
    "verbal act's finality depends on WHAT KIND of statement it is. The test "
    "is CONTINGENT vs. UNCONDITIONAL, not physical vs. verbal: an ultimatum "
    "or conditional threat ('do X or I will do Y') leaves a real way back -- "
    "the other party can still comply, so nothing has been crossed yet. An "
    "unconditional declaration of a fixed future event ('there is something "
    "I have to tell you') forecloses the alternative outright, the same way "
    "pulling a trigger does -- it is not a threat contingent on someone "
    "else's response, it is a flat statement that the thing will now "
    "happen. Real error caught: scene172_beat5's 'Or I'll be forced to "
    "defend myself' is an ultimatum (conditional, leaves Reggie a real way "
    "out) and correctly stays declared-intent-only, not a turning point. "
    "scene223_beat1's 'There's something I have to tell you,' spoken after "
    "Andy's mother has recognized and named him, is unconditional -- it "
    "does not depend on the Murphys' response, it is John's own act of "
    "committing to a fixed future. The recognition moment itself ('Johnny? "
    "Johnny Kierstead? My God.') is not the crossing -- it belongs to "
    "another character, not the one being tracked, and every "
    "point-of-no-return instance confirmed so far rests on the tracked "
    "character's OWN action or declaration, physical or verbal (see "
    "Principle 10). Recognition is the precondition that makes John's "
    "subsequent declaration costly to walk back, not the crossing itself. "
    "A character needs sufficient established arc/traits for the crossing "
    "to carry dramaturgical weight -- an anonymous or minimally-established "
    "character's irreversible act does not qualify, since there is no "
    "baseline for the audience (or the model) to register a change against. "
    "Note: ratified from Full of Grace cold-run finding 19 "
    "(FOG_COLD_RUN_FINDINGS.md), four confirmed instances across three "
    "characters, all boundary_revealed: TRUDY scene214_beat4, JOHN "
    "scene172_beat6, REGGIE scene172_beat6, JOHN scene223_beat1. A fifth "
    "was confirmed after ratification: MACKIE scene140_beat6 (a father's "
    "chokehold on his son), the first PHYSICAL instance whose "
    "irreversibility is relational rather than lethal -- a non-lethal "
    "physical act can still close the way back through what it does to a "
    "relationship. This "
    "principle operates at the causal-integrity layer only: it does NOT "
    "relax the archetype layer's 'declared intent is not the act itself' "
    "rule (Hero), which deliberately stays strict.\n\n"

    "OPERATIONAL NOTE: when resolving a character's causal integrity, gather every beat "
    "where the character is PRESENT, not only beats that carry an archetype tag. Real error "
    "caught twice: a character's actual resolution beat, and a character's single most "
    "load-bearing causal action in the whole script, both lived in beats with no archetype "
    "tag at all and were nearly missed entirely by only checking tagged beats."
)


@dataclass
class CausalIntegrityTag:
    """Per-CHARACTER causal-integrity assessment for one beat -- see
    ArchetypeTag's docstring for why this moved off BeatTag. Two of
    the remaining fields legitimately cannot be assessed on a first
    read and MUST default to REQUIRES_SECOND_PASS --
    weight_proportionality (Obsession/LW ending) and
    characterization_consistency (LW pier scene/WHTBD Brianna) both
    require knowing the whole work first, PER CHARACTER."""
    weight_proportionality: WeightProportionality = WeightProportionality.REQUIRES_SECOND_PASS
    agency_alignment: Optional[AgencyAlignment] = None
    displacement_mechanism: Optional[dict] = None  # {"enabling_character":..., "convenient_capability":...}
    characterization_consistency: CharacterizationConsistency = CharacterizationConsistency.REQUIRES_SECOND_PASS
    contradiction_trace: Optional[dict] = None  # {"suspected_external_note":..., "craft_evidence":[...]}

    def validate(self):
        if self.agency_alignment == AgencyAlignment.DISPLACED and not self.displacement_mechanism:
            raise ValueError("agency_alignment=DISPLACED requires displacement_mechanism to be set.")
        if self.characterization_consistency == CharacterizationConsistency.CONTRADICTED and not self.contradiction_trace:
            raise ValueError("characterization_consistency=CONTRADICTED requires contradiction_trace to be set.")

    def to_dict(self):
        return {
            "weight_proportionality": self.weight_proportionality.value,
            "agency_alignment": self.agency_alignment.value if self.agency_alignment else None,
            "displacement_mechanism": self.displacement_mechanism,
            "characterization_consistency": self.characterization_consistency.value,
            "contradiction_trace": self.contradiction_trace,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            weight_proportionality=WeightProportionality(d["weight_proportionality"]),
            agency_alignment=AgencyAlignment(d["agency_alignment"]) if d.get("agency_alignment") else None,
            displacement_mechanism=d.get("displacement_mechanism"),
            characterization_consistency=CharacterizationConsistency(d["characterization_consistency"]),
            contradiction_trace=d.get("contradiction_trace"),
        )


@dataclass
class BeatTag:
    """The full tag package for one beat -- references the beat_id from
    the existing package_scene_for_interpretation() output rather than
    duplicating turn text, so this stays a thin layer on top of the
    already-validated beat-detection pipeline, not a parallel one.

    chain_soundness lives HERE (beat-level) because it's a judgment
    about the STORY's own causal logic -- is the plot mechanically
    sound -- not any one character's psychology. It's the one
    causal-integrity axis that genuinely doesn't diverge per character
    the way weight_proportionality/characterization_consistency can;
    see ArchetypeTag for those two and why they moved there instead.

    chain_soundness is OPTIONAL, not defaulted to a fresh value. Some
    beats legitimately only need archetype tagging (a thin/minor beat,
    per the altitude-based approach used throughout this whole
    project) and were never meant to receive causal-integrity scrutiny
    at all. Defaulting to UNDETERMINED would make those beats
    indistinguishable from ones where causal-integrity assessment
    genuinely started but is still pending -- confirmed as a real
    ambiguity when Bud's and O'Neil/Betts's archetype-only tags both
    wrongly surfaced in beats_requiring_second_pass()."""
    beat_id: str
    scene_id: Optional[int] = None
    per_character: list = field(default_factory=list)  # list[ArchetypeTag]
    chain_soundness: Optional[ChainSoundness] = None
    confidence_flag: ConfidenceFlag = ConfidenceFlag.INTERPRETIVE_JUDGMENT
    provenance: Provenance = Provenance.HUMAN
    # Raw evidence dict from package_scene_for_interpretation()'s beat
    # entry (turns, emotion evidence, suspense evidence). Stored for
    # AUDIT ONLY -- "what did the algorithm actually detect that a
    # human/LLM was looking at when they made this judgment call" --
    # never read by any validation or query logic in this module.
    source_evidence: Optional[dict] = None

    def validate(self):
        for tag in self.per_character:
            tag.validate()

    def to_dict(self):
        return {
            "beat_id": self.beat_id, "scene_id": self.scene_id,
            "per_character": [t.to_dict() for t in self.per_character],
            "chain_soundness": self.chain_soundness.value if self.chain_soundness else None,
            "confidence_flag": self.confidence_flag.value,
            "provenance": self.provenance.value,
            "source_evidence": self.source_evidence,  # already plain JSON-safe data, no enums
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            beat_id=d["beat_id"], scene_id=d.get("scene_id"),
            per_character=[ArchetypeTag.from_dict(t) for t in d.get("per_character", [])],
            chain_soundness=ChainSoundness(d["chain_soundness"]) if d.get("chain_soundness") else None,
            confidence_flag=ConfidenceFlag(d["confidence_flag"]),
            provenance=Provenance(d["provenance"]) if d.get("provenance") else Provenance.HUMAN,
            source_evidence=d.get("source_evidence"),
        )


@dataclass
class Correction:
    """One field-level correction: an LLM produced a value, a human
    (or a more authoritative source, e.g. the author directly) changed
    it. Append-only, never edited or deleted -- this log IS the
    calibration data for the eventual anchor-script workflow: not an
    impression of 'the LLM seems pretty good,' but a real, queryable
    record of exactly which kinds of judgment it gets wrong."""
    beat_id: str
    field_name: str  # e.g. "characterization_consistency", "archetypes", "goal"
    llm_value: str
    human_value: str
    character: Optional[str] = None
    notes: str = ""

    def to_dict(self):
        return {
            "beat_id": self.beat_id, "field_name": self.field_name,
            "llm_value": self.llm_value, "human_value": self.human_value,
            "character": self.character, "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            beat_id=d["beat_id"], field_name=d["field_name"],
            llm_value=d["llm_value"], human_value=d["human_value"],
            character=d.get("character"), notes=d.get("notes", ""),
        )


@dataclass
class PlotFact:
    """An objective, structural fact about the story's own construction
    -- what TYPE an event is (staged vs. genuine), a character's cover
    identity, a confirmed factual reveal about an object/event.
    Established once via a dedicated whole-script read and available
    OMNISCIENTLY to every beat within its scope, regardless of that
    beat's own position in the story.

    Deliberately separate from CharacterRegistryEntry, which stays
    temporally scoped ('as of this beat') by design -- collapsing a
    character's evolving psychological throughline with hindsight would
    reintroduce exactly the anachronistic-reading error this project has
    repeatedly corrected against (a character's beat-3 sincerity isn't
    retroactively fake just because beat-50 reveals a strategic arc).
    PlotFact exists specifically for facts that are NOT about anyone's
    felt experience or motive -- only about what kind of event is
    objectively occurring.

    SCOPE TEST (deliberately narrow, confirmed against real Ocean's
    Eleven corrections): a fact belongs here only if it changes what
    CATEGORY an observable action belongs to (genuine vs. staged/
    performed), not if it describes an underlying feeling or motive. A
    character's true feelings, even once eventually revealed, stay OUT
    of this registry and belong to CharacterRegistryEntry instead. Real
    example of the distinction holding under pressure: Danny's timing at
    Tess's table is a PlotFact (he deliberately engineered the risk of
    being caught by Benedict); Tess's own shock and anger in that same
    beat are NOT a PlotFact (she is not complicit, her reaction is
    genuine) -- one beat can contain both a plot fact and ordinary,
    unstaged psychology side by side.

    KNOWING vs. TAGGING (a second, separate boundary, confirmed against
    a real near-miss): a plot fact licenses correctly INTERPRETING
    action that is actually depicted in a beat's own evidence -- it
    never licenses ASSERTING an archetype for an action the beat's own
    text doesn't depict at all. A covert action established by this
    fact (planting an object, activating a device) should only be
    tagged in the SPECIFIC beat where the text itself shows some sign
    of it -- a gesture, an aside, anything a reader of just that beat
    could point to. Knowing an omniscient fact is true is not the same
    as that fact's evidence being present in every beat its scope
    happens to cover."""
    fact: str
    category: str  # "staged_vs_genuine" | "identity_cover" | "confirmed_reveal"
    scope_scenes: list  # scene_id ints this fact governs
    established_by_scene: int = 0  # where in the story this becomes TRUE -- reference/audit only, never used to gate visibility (facts are omniscient from beat 1 within their scope)
    confidence: str = "high"  # high | moderate | low
    notes: str = ""
    # Same vocabulary as BeatTag's Provenance enum. Plot facts are not
    # beats, so a fact's own review status is recorded here; the field-level
    # record of what changed still lives in the Correction log, under
    # beat_id "plot_facts[N]" (added 2026-10-03 for the FOG plot-facts
    # corrections). Files written before this field default to
    # llm_unreviewed on load.
    provenance: str = "llm_unreviewed"

    def applies_to_scene(self, scene_id):
        return scene_id in self.scope_scenes

    def validate(self):
        Provenance(self.provenance)  # raises ValueError on an unknown value

    def to_dict(self):
        return {
            "fact": self.fact, "category": self.category,
            "scope_scenes": self.scope_scenes,
            "established_by_scene": self.established_by_scene,
            "confidence": self.confidence, "notes": self.notes,
            "provenance": self.provenance,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            fact=d["fact"], category=d["category"],
            scope_scenes=d.get("scope_scenes", []),
            established_by_scene=d.get("established_by_scene", 0),
            confidence=d.get("confidence", "high"),
            notes=d.get("notes", ""),
            provenance=d.get("provenance", "llm_unreviewed"),
        )


class ScriptAnalysis:
    """Top-level container for one script_version's full tagging pass.
    Holds the Registry, Ledger, Linkages, and per-beat tags; provides
    query helpers. Contains NO judgment logic -- every add_* method
    below takes already-decided values from the caller (human or LLM)
    and simply stores them, validated for internal consistency only
    (e.g. 'if displaced, a mechanism must be given'), never for whether
    the judgment itself is correct."""

    def __init__(self, script_version: ScriptVersion):
        self.script_version = script_version
        self.registry: dict[str, CharacterRegistryEntry] = {}
        self.ledger: list[Commitment] = []
        self.linkages: list[BeatLinkage] = []
        self.beats: dict[str, BeatTag] = {}
        self.corrections: list[Correction] = []
        self.emotional_wave = []  # per-scene valence ("the wave"), see integration.compute_and_attach_wave
        self.plot_facts: list[PlotFact] = []

    # --- Plot Facts ---
    def add_plot_fact(self, plot_fact: PlotFact):
        self.plot_facts.append(plot_fact)

    def plot_facts_for_scene(self, scene_id):
        """All plot facts whose scope includes this scene -- omniscient
        by design, NOT filtered by the scene's position in the story.
        A scene early in the script can and should see a fact that only
        becomes narratively TRUE much later, if that fact's scope
        includes this scene (e.g. the SWAT-disguise extraction fact
        governs the whole climax sequence from its own first scene
        onward, not progressively as it's 'discovered')."""
        return [pf for pf in self.plot_facts if pf.applies_to_scene(scene_id)]

    # --- Registry ---
    def get_or_create_character(self, name) -> CharacterRegistryEntry:
        if name not in self.registry:
            self.registry[name] = CharacterRegistryEntry(character=name)
        return self.registry[name]

    def update_throughline(self, character, scene_id, state, beat_number=0):
        entry = self.get_or_create_character(character)
        entry.established_goal_throughline.append(
            {"scene_id": scene_id, "beat_number": beat_number, "state": state}
        )

    # --- Ledger ---
    def add_commitment(self, commitment: Commitment):
        self.ledger.append(commitment)

    def resolve_commitment(self, commitment_id, status: CommitmentStatus, beat_resolved=None):
        for c in self.ledger:
            if c.commitment_id == commitment_id:
                c.status = status
                c.beat_resolved = beat_resolved
                return c
        raise KeyError(f"No commitment with id {commitment_id}")

    # --- Corrections (LLM calibration data) ---
    def log_correction(self, beat_id, field_name, llm_value, human_value, character=None, notes=""):
        """Record a field-level correction and mark the beat's
        provenance accordingly. This is the actual calibration
        mechanism for the anchor-script workflow: not an impression,
        a queryable log of exactly what the LLM got wrong and how.

        Requires the beat to already be tagged (tag_beat() called
        first) -- confirmed as a real silent-failure risk in testing:
        logging a correction before the beat existed in self.beats
        silently no-op'd the provenance update, with no error at all.

        IDEMPOTENT on exact duplicates (same beat_id, field_name,
        character, llm_value, human_value) -- confirmed as a real risk
        via testing: rerunning the same script against the same
        persisted analysis silently inflated the tally (2 entries for
        one real event). A given beat can only have one true LLM
        output and one true human correction for a given field, so an
        identical repeat is a rerun artifact, not a second independent
        data point -- calling this twice with the same arguments now
        produces the same end state as calling it once. A DIFFERENT
        correction on the same beat/field (e.g. the human revises their
        own earlier correction) is legitimate and still recorded.

        Returns the Correction that is now on record (either newly
        created, or the pre-existing identical one), and a bool
        indicating whether a NEW entry was actually added."""
        if beat_id not in self.beats:
            raise KeyError(
                f"Cannot log a correction for beat '{beat_id}': it hasn't been "
                "tagged yet (call tag_beat() first). Logging a correction before "
                "the beat exists would silently fail to update its provenance."
            )
        for existing in self.corrections:
            if (existing.beat_id == beat_id and existing.field_name == field_name
                    and existing.character == character and existing.llm_value == llm_value
                    and existing.human_value == human_value):
                self.beats[beat_id].provenance = Provenance.LLM_HUMAN_CORRECTED
                return existing, False

        new_correction = Correction(
            beat_id=beat_id, field_name=field_name, llm_value=llm_value,
            human_value=human_value, character=character, notes=notes,
        )
        self.corrections.append(new_correction)
        self.beats[beat_id].provenance = Provenance.LLM_HUMAN_CORRECTED
        return new_correction, True

    def correction_tally(self):
        """Breakdown of corrections by field -- the calibration report.
        Confirms or refutes patterns like 'the LLM tends to get
        inferred Linkages wrong more than mechanical fields' with real
        counts, not impression."""
        from collections import Counter
        return dict(Counter(c.field_name for c in self.corrections))
    
    def set_emotional_wave(self, wave_data):
        """Store the emotional arc ('the wave') -- per-scene valence
        (mean/min/max sentiment) computed by
        beat_detector.compute_script_wave(). This was built months ago
        but never wired into the tagging schema until now. The actual
        computation lives in integration.py, not here, to keep this
        module free of any dependency on beat_detector.py internals."""
        self.emotional_wave = wave_data

    def wave_for_scene(self, scene_id):
        for entry in self.emotional_wave:
            if entry.get('scene_id') == scene_id:
                return entry
        return None

    def open_threads(self):
        """Query helper: every commitment and linkage still genuinely
        open -- the kind of cross-script view a single AI-generated
        coverage paragraph can't reproduce, since it doesn't persist."""
        open_commitments = [c for c in self.ledger if c.status == CommitmentStatus.OPEN]
        open_linkages = [l for l in self.linkages if l.status == LinkageStatus.OPEN]
        return {"commitments": open_commitments, "linkages": open_linkages}

    # --- Linkages ---
    def add_linkage(self, linkage: BeatLinkage):
        linkage.validate()
        self.linkages.append(linkage)

    # --- Beats ---
    def tag_beat(self, beat_tag: BeatTag):
        beat_tag.validate()
        self.beats[beat_tag.beat_id] = beat_tag

    def beats_requiring_second_pass(self):
        """Every beat where AT LEAST ONE present character has an
        unresolved deferred field -- the explicit worklist for Pass 2,
        so nothing gets silently left half-tagged.

        Checks per-character now, not beat-level (see ArchetypeTag's
        docstring for why) -- a beat only counts as done once EVERY
        character carrying a causal_integrity assessment has resolved
        both fields, not just whichever character happened to be
        checked. A character with causal_integrity=None was never
        meant to receive that assessment (archetype-only tagging) and
        is correctly excluded, same principle as the old beat-level
        check."""
        return [
            b for b in self.beats.values()
            if any(
                tag.causal_integrity is not None and (
                    tag.causal_integrity.weight_proportionality == WeightProportionality.REQUIRES_SECOND_PASS
                    or tag.causal_integrity.characterization_consistency == CharacterizationConsistency.REQUIRES_SECOND_PASS
                )
                for tag in b.per_character
            )
        ]

    def finalize_check(self):
        """Sanity check before treating an analysis as complete: no
        REQUIRES_SECOND_PASS fields should remain if the caller believes
        Pass 2 is done. Returns a list of problems, empty if clean."""
        problems = []
        remaining = self.beats_requiring_second_pass()
        if remaining:
            problems.append(f"{len(remaining)} beat(s) still REQUIRES_SECOND_PASS: "
                             f"{[b.beat_id for b in remaining]}")
        for l in self.linkages:
            if l.confidence == LinkageConfidence.ANALYTICALLY_DISCOVERED and l.author_ratified is None:
                problems.append(f"Linkage {l.beat_a}<->{l.beat_b} never got author ratification.")
        return problems

    # --- Persistence ---
    # The whole point: real tagging work happens across many separate
    # sessions over days or weeks (confirmed directly -- the WHTBD
    # dry run itself spanned multiple days across this project). A
    # ScriptAnalysis has to survive between them, not reset to empty
    # every time a new script/process starts.

    def to_dict(self):
        return {
            "script_version": self.script_version.to_dict(),
            "registry": { name: entry.to_dict() for name, entry in self.registry.items()},
            "ledger": [c.to_dict() for c in self.ledger],
            "linkages": [l.to_dict() for l in self.linkages],
            "beats": {beat_id: bt.to_dict() for beat_id, bt in self.beats.items()},
            "corrections": [c.to_dict() for c in self.corrections],
            "emotional_wave": self.emotional_wave,
            "plot_facts": [pf.to_dict() for pf in self.plot_facts],
        }

    @classmethod
    def from_dict(cls, d):
        analysis = cls(ScriptVersion.from_dict(d["script_version"]))
        analysis.registry = {
            name: CharacterRegistryEntry.from_dict(entry) for name, entry in d.get("registry", {}).items()
        }
        analysis.ledger = [Commitment.from_dict(c) for c in d.get("ledger", [])]
        analysis.linkages = [BeatLinkage.from_dict(l) for l in d.get("linkages", [])]
        analysis.beats = {beat_id: BeatTag.from_dict(bt) for beat_id, bt in d.get("beats", {}).items()}
        analysis.corrections = [Correction.from_dict(c) for c in d.get("corrections", [])]
        analysis.emotional_wave = d.get("emotional_wave", [])
        analysis.plot_facts = [PlotFact.from_dict(pf) for pf in d.get("plot_facts", [])]
        return analysis

    def save(self, filepath):
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath):
        import json
        with open(filepath, encoding='utf-8') as f:
            d = json.load(f)
        return cls.from_dict(d)
