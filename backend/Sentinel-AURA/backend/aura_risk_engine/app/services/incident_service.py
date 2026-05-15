from typing import Tuple
from aura_risk_engine.app.models.incident_model import get_incident_risk


def evaluate_incident_risk(incident_severity: float, incident_timestamp: int) -> Tuple[float, str]:
    """Evaluate the incident risk component and return a reason string."""
    incident_risk, explanation = get_incident_risk(incident_severity, incident_timestamp)
    return incident_risk, explanation
