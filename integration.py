"""
integration.py -- reconstructed evidence_summary(), matching the
untruncated format confirmed in the Theresa/O'Neil fix (the [:70]
slice removed so full dialogue reaches the model), formatting a
BeatTag's stored source_evidence dict into the plain-text block the
harness sends to the API.
"""

def evidence_summary(beat_tag):
    ev = beat_tag.source_evidence or {}
    lines = []
    lines.append(f"Beat: {beat_tag.beat_id}")
    chars = ev.get("characters_present", [])
    if chars:
        lines.append(f"Characters present: {', '.join(chars)}")
    lines.append("")
    lines.append("Turns:")
    for t in ev.get("turns", []):
        speaker = t.get("speaker") or "-"
        paren = f" {t['paren']}" if t.get("paren") else ""
        lines.append(f"  [{t['kind']:9}] {speaker:12}{paren} {t['text']}")
        if t.get("suspense_signals"):
            lines.append(f"      suspense: {', '.join(t['suspense_signals'])}")

    evidence = ev.get("evidence", {})
    closing = evidence.get("closing_signal")
    if closing:
        lines.append("")
        lines.append(f"Closing signal (turn {closing['turn_index']}, score {closing['score']}): "
                      f"{', '.join(closing.get('reasons', []))}")
    notable = evidence.get("notable_signals", [])
    if notable:
        for n in notable:
            lines.append(f"Notable signal (turn {n['turn_index']}, score {n['score']}): "
                          f"{', '.join(n.get('reasons', []))}")

    suspense_ev = ev.get("suspense_evidence", [])
    if suspense_ev:
        for s in suspense_ev:
            lines.append(f"Suspense (turn {s['turn_index']}, score {s['suspense_score']}): "
                          f"{', '.join(s.get('reasons', []))}")

    preceding = ev.get("preceding_context")
    if preceding:
        lines.append("")
        lines.append(f"Preceding context: {preceding}")

    return "\n".join(lines)
