from typing import List


def build_explanation_reasons(
    time_risk: float,
    crowd_density: float,
    light_intensity: float,
    incident_reason: str,
) -> List[str]:
    """Build a list of human-readable reasons explaining the risk score."""
    reasons: List[str] = []

    if time_risk >= 80:
        reasons.append("Nighttime conditions increase risk")
    elif time_risk >= 50:
        reasons.append("Evening hours add moderate risk")
    else:
        reasons.append("Daytime reduces risk")

    if crowd_density < 0.3:
        reasons.append("Low crowd density may increase isolation risk")
    elif crowd_density < 0.7:
        reasons.append("Moderate crowd density provides balanced safety")
    else:
        reasons.append("High crowd density reduces isolation risk")

    if light_intensity < 0.3:
        reasons.append("Dark area detected")
    elif light_intensity < 0.7:
        reasons.append("Low light conditions present")
    else:
        reasons.append("Well-lit environment reduces risk")

    reasons.append(incident_reason)
    return reasons
