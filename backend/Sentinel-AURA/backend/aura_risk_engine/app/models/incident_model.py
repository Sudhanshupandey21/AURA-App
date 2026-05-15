import time
from typing import Tuple
from aura_risk_engine.app.utils.decay import exponential_decay


def get_incident_risk(incident_severity: float, incident_timestamp: int, current_timestamp: int | None = None) -> Tuple[float, str]:
    """Calculate incident risk using severity and exponential decay based on age."""
    if current_timestamp is None:
        current_timestamp = int(time.time())

    age_seconds = max(0, current_timestamp - incident_timestamp)
    # older incidents reduce their contribution exponentially
    decay_factor = exponential_decay(age_seconds, half_life_seconds=3600)

    incident_risk = max(0.0, min(100.0, incident_severity * 100.0 * decay_factor))
    explanation = "Recent incident nearby" if age_seconds < 3600 else "Older incident data with reduced impact"
    return incident_risk, explanation
