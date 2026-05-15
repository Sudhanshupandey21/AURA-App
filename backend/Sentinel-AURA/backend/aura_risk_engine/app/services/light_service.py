from aura_risk_engine.app.utils.scoring import clamp_score


def get_light_risk(light_intensity: float) -> float:
    """Calculate light intelligence risk.

    Darker environments increase risk while brighter surroundings lower it.
    """
    light_intensity = clamp_score(light_intensity, 0.0, 1.0)
    return (1.0 - light_intensity) * 100.0
