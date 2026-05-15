from typing import Literal


def predict_trend(hour: int, crowd_density: float, incident_risk: float) -> Literal["increasing", "stable", "decreasing"]:
    """Predict whether the risk trend is increasing, stable, or decreasing.

    Trend is inferred from recent incident impact and low crowd density during night hours.
    """
    # Night and incident-heavy contexts tend to indicate increasing risk.
    if incident_risk > 70 or (hour >= 22 or hour < 5) and crowd_density < 0.35:
        return "increasing"

    # Stable when incident impact is moderate and crowd density is balanced.
    if 30 <= incident_risk <= 70 and 0.35 <= crowd_density <= 0.75:
        return "stable"

    # Otherwise, assume the risk is decreasing.
    return "decreasing"
