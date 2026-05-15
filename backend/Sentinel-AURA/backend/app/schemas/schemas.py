from pydantic import BaseModel
from typing import Optional, Dict, Any

class RiskPredictionRequest(BaseModel):
    user_id: str
    location: Dict[str, float]  # {"lat": float, "lng": float}
    context: Optional[Dict[str, Any]] = None

class RiskPredictionResponse(BaseModel):
    success: bool
    risk_score: float
    risk_level: str
    recommendation: str
    timestamp: str

class RouteAnalysisRequest(BaseModel):
    user_id: str
    route_points: list[Dict[str, float]]  # List of {"lat": float, "lng": float}
    preferences: Optional[Dict[str, Any]] = None

class RouteAnalysisResponse(BaseModel):
    success: bool
    safest_route: list[Dict[str, float]]
    risk_assessment: Dict[str, Any]
    alternatives: Optional[list] = None

class IncidentReportRequest(BaseModel):
    user_id: str
    location: Dict[str, float]
    type: str
    description: str
    severity: str

class IncidentReportResponse(BaseModel):
    success: bool
    incident_id: str
    message: str

class SOSRequest(BaseModel):
    user_id: str
    location: Dict[str, float]
    message: Optional[str] = "Emergency SOS"

class SOSResponse(BaseModel):
    success: bool
    alert_id: str
    message: str

class LiveLocationRequest(BaseModel):
    user_id: str
    location: Dict[str, float]
    speed: Optional[float] = None
    heading: Optional[float] = None

class LiveLocationResponse(BaseModel):
    success: bool
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

class SystemStatusResponse(BaseModel):
    status: str
    uptime: str
    active_connections: int
    ai_engines_status: Dict[str, str]