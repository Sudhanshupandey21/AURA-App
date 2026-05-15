from typing import List
import numpy as np
import pandas as pd

from aura_risk_engine.app.config import Settings
from aura_risk_engine.app.models.risk_model import RiskResult
from aura_risk_engine.app.services.crowd_service import get_crowd_risk
from aura_risk_engine.app.services.light_service import get_light_risk
from aura_risk_engine.app.services.incident_service import evaluate_incident_risk
from aura_risk_engine.app.services.prediction_service import evaluate_trend
from aura_risk_engine.app.utils.explain import build_explanation_reasons
from aura_risk_engine.app.utils.scoring import clamp_score
from aura_risk_engine.risk_engine import RiskScorer as CoreRiskScorer


def get_time_risk(hour: int) -> float:
    """Calculate risk based on hour of day.

    Daytime is lower risk, evening is medium, and late night is high risk.
    """
    if hour < 0 or hour > 23:
        raise ValueError("hour must be between 0 and 23")

    if 6 <= hour < 18:
        return 20.0
    if 18 <= hour < 22:
        return 55.0
    return 85.0


def get_risk_level(risk_score: int, settings: Settings) -> str:
    """Choose risk category from the final score."""
    if risk_score < settings.safe_threshold:
        return "SAFE"
    if risk_score < settings.medium_threshold:
        return "MEDIUM"
    return "HIGH"


def analyze_risk(
    hour: int,
    crowd_density: float,
    light_intensity: float,
    incident_severity: float,
    incident_timestamp: int,
    settings: Settings,
) -> RiskResult:
    """Compute the full risk result using modular intelligence components."""
    crowd_density = clamp_score(crowd_density, 0.0, 1.0)
    light_intensity = clamp_score(light_intensity, 0.0, 1.0)
    incident_severity = clamp_score(incident_severity, 0.0, 1.0)

    time_risk = get_time_risk(hour)
    crowd_risk = get_crowd_risk(crowd_density)
    light_risk = get_light_risk(light_intensity)
    incident_risk, incident_reason = evaluate_incident_risk(incident_severity, incident_timestamp)

    # Use pandas DataFrame for a structured explanation of weights and values.
    component_df = pd.DataFrame(
        {
            "component": ["time", "crowd", "light", "incident"],
            "value": [time_risk, crowd_risk, light_risk, incident_risk],
            "weight": [
                settings.time_weight,
                settings.crowd_weight,
                settings.light_weight,
                settings.incident_weight,
            ],
        }
    )
    weighted_values = np.dot(component_df["value"].values, component_df["weight"].values)
    aggregated_score = float(weighted_values)

    final_score = int(round(clamp_score(aggregated_score, 0.0, 100.0)))
    risk_level = get_risk_level(final_score, settings)
    trend = evaluate_trend(hour, crowd_density, incident_risk)

    reasons = build_explanation_reasons(
        time_risk=time_risk,
        crowd_density=crowd_density,
        light_intensity=light_intensity,
        incident_reason=incident_reason,
    )

    return RiskResult(
        risk_score=final_score,
        risk_level=risk_level,
        trend=trend,
        reasons=reasons,
    )


class RiskScorer(CoreRiskScorer):
    """Application-level risk scorer wrapper for AURA X service layer."""

    def calculate_risk(
        self,
        hour: int,
        crowd_density: float,
        light_intensity: float,
        incident_severity: float,
        incident_timestamp: int,
        settings: Settings = None,
    ) -> RiskResult:
        """Calculate a full risk result using the service layer."""
        return analyze_risk(
            hour=hour,
            crowd_density=crowd_density,
            light_intensity=light_intensity,
            incident_severity=incident_severity,
            incident_timestamp=incident_timestamp,
            settings=settings or Settings(),
        )
