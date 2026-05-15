from aura_risk_engine.app.utils.scoring import clamp_score


def get_crowd_risk(crowd_density: float) -> float:
    """Calculate crowd intelligence risk.

    Low crowd density raises risk because isolated areas are less safe.
    """
    crowd_density = clamp_score(crowd_density, 0.0, 1.0)
    # Invert crowd density so low density produces higher risk.
    return (1.0 - crowd_density) * 100.0
