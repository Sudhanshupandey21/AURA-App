from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.schemas.schemas import (
    RiskPredictionRequest, RiskPredictionResponse,
    RouteAnalysisRequest, RouteAnalysisResponse,
    IncidentReportRequest, IncidentReportResponse,
    SOSRequest, SOSResponse,
    LiveLocationRequest, LiveLocationResponse,
    HealthResponse, SystemStatusResponse
)
from app.services.ai_service import ai_service
from app.database.connection import get_database
from app.websocket.manager import ws_manager
from app.models.models import Incident, LocationHistory, SOSAlert, PredictionHistory
from app.utils.logger import logger
import psutil
import time
from app.config.settings import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=settings.app_version
    )

@router.get("/system-status", response_model=SystemStatusResponse)
async def system_status():
    """System status and monitoring"""
    try:
        # Get system metrics
        uptime = time.time() - psutil.boot_time()
        active_connections = len(ws_manager.active_connections)

        # Check AI engines status
        ai_engines_status = {
            "risk_engine": "operational",
            "incident_processor": "operational",
            "response_engine": "operational",
            "coordinator": "operational"
        }

        return SystemStatusResponse(
            status="operational",
            uptime=f"{uptime:.0f}s",
            active_connections=active_connections,
            ai_engines_status=ai_engines_status
        )
    except Exception as e:
        logger.error("System status check failed", error=str(e))
        raise HTTPException(status_code=500, detail="System status check failed")

@router.post("/predict-risk", response_model=RiskPredictionResponse)
async def predict_risk(request: RiskPredictionRequest, db=Depends(get_database)):
    """AI-powered risk prediction for location"""
    try:
        result = await ai_service.predict_risk(request.user_id, request.location, request.context)

        # Store prediction history
        prediction = PredictionHistory(
            user_id=request.user_id,
            location=request.location,
            risk_score=result.get("risk_score", 0),
            risk_level=result.get("risk_level", "UNKNOWN"),
            recommendation=result.get("recommendation", "")
        )
        await db.prediction_history.insert_one(prediction.dict(by_alias=True))

        response = RiskPredictionResponse(
            success=True,
            risk_score=result.get("risk_score", 0),
            risk_level=result.get("risk_level", "UNKNOWN"),
            recommendation=result.get("recommendation", ""),
            timestamp=datetime.utcnow().isoformat()
        )
        return response
    except Exception as e:
        logger.error("Risk prediction failed", error=str(e))
        raise HTTPException(status_code=500, detail="Risk prediction failed")

@router.post("/route-analysis", response_model=RouteAnalysisResponse)
async def analyze_route(request: RouteAnalysisRequest, db=Depends(get_database)):
    """Analyze route safety using AI engines"""
    try:
        result = await ai_service.analyze_route(request.user_id, request.route_points, request.preferences)

        response = RouteAnalysisResponse(
            success=True,
            safest_route=result.get("safest_route", request.route_points),
            risk_assessment=result.get("risk_assessment", {}),
            alternatives=result.get("alternatives", [])
        )
        return response
    except Exception as e:
        logger.error("Route analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail="Route analysis failed")

@router.post("/incident-report", response_model=IncidentReportResponse)
async def report_incident(request: IncidentReportRequest, db=Depends(get_database)):
    """Report an incident"""
    try:
        incident_data = {
            "user_id": request.user_id,
            "location": request.location,
            "type": request.type,
            "description": request.description,
            "severity": request.severity
        }

        await ai_service.process_incident(incident_data)

        # Store incident
        incident = Incident(**incident_data)
        result = await db.incidents.insert_one(incident.dict(by_alias=True))

        response = IncidentReportResponse(
            success=True,
            incident_id=str(result.inserted_id),
            message="Incident reported successfully"
        )
        return response
    except Exception as e:
        logger.error("Incident report failed", error=str(e))
        raise HTTPException(status_code=500, detail="Incident report failed")

@router.post("/sos", response_model=SOSResponse)
async def sos_alert(request: SOSRequest, db=Depends(get_database)):
    """Handle SOS emergency alerts"""
    try:
        sos_data = {
            "user_id": request.user_id,
            "location": request.location,
            "message": request.message
        }

        await ai_service.handle_sos(sos_data)

        # Store SOS alert
        sos_alert = SOSAlert(**sos_data)
        result = await db.sos_alerts.insert_one(sos_alert.dict(by_alias=True))

        # Send emergency alert via WebSocket
        await ws_manager.send_emergency_alert(request.user_id, sos_data)

        response = SOSResponse(
            success=True,
            alert_id=str(result.inserted_id),
            message="SOS alert sent successfully"
        )
        return response
    except Exception as e:
        logger.error("SOS alert failed", error=str(e))
        raise HTTPException(status_code=500, detail="SOS alert failed")

@router.post("/live-location", response_model=LiveLocationResponse)
async def update_live_location(request: LiveLocationRequest, db=Depends(get_database)):
    """Update live location and trigger real-time risk assessment"""
    try:
        location_data = {
            "location": request.location,
            "speed": request.speed,
            "heading": request.heading,
            "timestamp": datetime.utcnow()
        }

        # Store location history
        location_history = LocationHistory(
            user_id=request.user_id,
            location=request.location
        )
        await db.location_history.insert_one(location_history.dict(by_alias=True))

        # Handle via WebSocket manager
        await ws_manager.handle_live_location(request.user_id, location_data)

        response = LiveLocationResponse(
            success=True,
            message="Location updated successfully"
        )
        return response
    except Exception as e:
        logger.error("Live location update failed", error=str(e))
        raise HTTPException(status_code=500, detail="Location update failed")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

@router.get("/system-status", response_model=SystemStatusResponse)
async def system_status():
    """System status endpoint"""
    return SystemStatusResponse(
        status="operational",
        uptime="unknown",  # Could be calculated from startup time
        active_connections=len(ws_manager.active_connections),
        ai_engines_status={
            "risk_engine": "active",
            "route_engine": "active",
            "crowd_engine": "active",
            "incident_engine": "active",
            "alert_engine": "active"
        }
    )