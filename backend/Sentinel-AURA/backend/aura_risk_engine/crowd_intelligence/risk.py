from aura_risk_engine.crowd_intelligence.utils import validate_density


def get_crowd_risk(crowd_density: float) -> float:
    """Convert normalized crowd density into crowd risk.

    Higher crowd density means safer conditions; lower density raises risk.
    """
    crowd_density = validate_density(crowd_density)
    return 1.0 - crowd_density
