from aura_risk_engine.light_intelligence.utils import validate_normalized_light


def generate_light_reason(light_risk: float) -> str:
    """Generate an explainable reason based on darkness risk."""
    if not isinstance(light_risk, (int, float)):
        raise TypeError("light_risk must be a number")
    light_risk = max(0.0, min(1.0, float(light_risk)))

    if light_risk >= 0.8:
        return "Dark area detected"
    if light_risk >= 0.5:
        return "Low visibility environment"
    if light_risk >= 0.2:
        return "Moderately lit area"
    return "Well-lit environment"
