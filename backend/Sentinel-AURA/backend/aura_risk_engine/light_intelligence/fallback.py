from typing import Literal
from aura_risk_engine.light_intelligence.utils import validate_hour, validate_area_type, clamp

AreaType = Literal["market", "residential", "isolated"]


def estimate_light_from_time(hour: int, area_type: str) -> float:
    """Estimate normalized brightness when the light sensor is unavailable.

    This fallback system uses time of day and area type to infer ambient lighting.
    """
    hour = validate_hour(hour)
    area_type = validate_area_type(area_type)

    if 6 <= hour < 18:
        # Daytime is generally bright across all area types.
        estimated = 0.9 if area_type != "isolated" else 0.7
    elif 18 <= hour < 22:
        if area_type == "market":
            estimated = 0.65
        elif area_type == "residential":
            estimated = 0.45
        else:
            estimated = 0.2
    else:
        # Late night is dim or dark depending on the area.
        if area_type == "market":
            estimated = 0.35
        elif area_type == "residential":
            estimated = 0.18
        else:
            estimated = 0.05

    return clamp(estimated)
