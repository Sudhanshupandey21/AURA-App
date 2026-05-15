from aura_risk_engine.light_intelligence.utils import validate_normalized_light


def get_light_risk(normalized_light: float) -> float:
    """Calculate darkness risk from normalized ambient brightness.

    A lower normalized light value produces a higher darkness risk.
    """
    normalized_light = validate_normalized_light(normalized_light)
    return 1.0 - normalized_light
