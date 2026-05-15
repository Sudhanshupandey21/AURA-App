from pydantic import BaseModel, Field, conint, confloat


class RiskAnalysisRequest(BaseModel):
    """Input schema for risk analysis requests."""

    hour: conint(ge=0, le=23) = Field(..., description="Hour of the day in 24-hour format")
    crowd_density: confloat(ge=0.0, le=1.0) = Field(..., description="Crowd density normalized between 0 and 1")
    light_intensity: confloat(ge=0.0, le=1.0) = Field(..., description="Ambient light intensity normalized between 0 and 1")
    incident_severity: confloat(ge=0.0, le=1.0) = Field(..., description="Incident severity normalized between 0 and 1")
    incident_timestamp: int = Field(..., description="UNIX timestamp of the incident event")
