from fastapi import APIRouter, Depends, HTTPException, Request
from aura_risk_engine.app.schemas.request_schema import RiskAnalysisRequest
from aura_risk_engine.app.services.risk_service import analyze_risk
from aura_risk_engine.app.config import Settings
from aura_risk_engine.app.models.risk_model import RiskResult

router = APIRouter(prefix="", tags=["Risk Analysis"])


def get_settings(request: Request) -> Settings:
    """Retrieve application settings from the FastAPI state."""
    return request.app.state.settings

@router.post(
    "/analyze-risk",
    summary="Analyze real-time safety risk",
    response_model=RiskResult,
)
def analyze_risk_route(
    payload: RiskAnalysisRequest,
    settings: Settings = Depends(get_settings),
) -> dict:
    """Analyze risk and return the score, risk level, trend, and reasons."""
    try:
        result = analyze_risk(
            hour=payload.hour,
            crowd_density=payload.crowd_density,
            light_intensity=payload.light_intensity,
            incident_severity=payload.incident_severity,
            incident_timestamp=payload.incident_timestamp,
            settings=settings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return result.model_dump()
