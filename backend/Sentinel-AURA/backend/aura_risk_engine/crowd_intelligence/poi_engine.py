from aura_risk_engine.crowd_intelligence.utils import clamp, validate_area_type


def estimate_poi_density(area_type: str) -> float:
    """Estimate crowd density from the density of nearby points of interest."""
    area_type = validate_area_type(area_type)

    if area_type == "market":
        density = 0.85
    elif area_type == "transport_hub":
        density = 0.75
    elif area_type == "residential":
        density = 0.5
    else:
        density = 0.15

    return clamp(density)
