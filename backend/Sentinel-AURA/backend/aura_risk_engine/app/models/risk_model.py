from typing import List, Literal
from pydantic import BaseModel


class RiskResult(BaseModel):
    """Output schema for the risk intelligence engine."""

    risk_score: int
    risk_level: Literal["SAFE", "MEDIUM", "HIGH"]
    trend: Literal["increasing", "stable", "decreasing"]
    reasons: List[str]


class RiskComponents(BaseModel):
    """Internal risk component values used for scoring."""

    time_risk: float
    crowd_risk: float
    light_risk: float
    incident_risk: float
