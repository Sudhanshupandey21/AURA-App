from pydantic import BaseModel


class Settings(BaseModel):
    """Application-wide configuration and risk weights."""

    time_weight: float = 0.25
    crowd_weight: float = 0.25
    light_weight: float = 0.20
    incident_weight: float = 0.30

    # Risk thresholds for final level classification.
    safe_threshold: int = 35
    medium_threshold: int = 70
