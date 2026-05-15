from aura_risk_engine.crowd_intelligence.utils import validate_density


def generate_crowd_reason(crowd_density: float) -> str:
    """Generate a human-readable reason based on crowd density."""
    crowd_density = validate_density(crowd_density)

    if crowd_density >= 0.8:
        return "High public activity detected"
    if crowd_density >= 0.5:
        return "Moderate crowd presence"
    if crowd_density >= 0.2:
        return "Low public activity detected"
    return "Very low crowd density detected"
