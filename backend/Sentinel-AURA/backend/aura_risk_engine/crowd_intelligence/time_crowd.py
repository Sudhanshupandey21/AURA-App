from aura_risk_engine.crowd_intelligence.utils import clamp, validate_area_type, validate_hour


def estimate_time_crowd(hour: int, area_type: str) -> float:
    """Estimate crowd density using time of day and area type."""
    hour = validate_hour(hour)
    area_type = validate_area_type(area_type)

    if area_type == "market":
        if 18 <= hour < 22:
            density = 0.95
        elif 22 <= hour or hour < 6:
            density = 0.35
        else:
            density = 0.8
    elif area_type == "transport_hub":
        if 7 <= hour < 10 or 16 <= hour < 19:
            density = 0.9
        elif 22 <= hour or hour < 5:
            density = 0.4
        else:
            density = 0.7
    elif area_type == "residential":
        if 6 <= hour < 10 or 17 <= hour < 21:
            density = 0.6
        elif 22 <= hour or hour < 6:
            density = 0.25
        else:
            density = 0.45
    else:
        if 22 <= hour or hour < 6:
            density = 0.1
        elif 18 <= hour < 22:
            density = 0.2
        else:
            density = 0.15

    return clamp(density)
