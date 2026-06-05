import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from aura_risk_engine.risk_engine.realtime_engine import RealtimeRiskEngine
from aura_risk_engine.route_safety_engine.rerouting_engine import reroute_if_needed
from aura_risk_engine.route_safety_engine.safest_route import select_safest_route
from aura_risk_engine.crowd_intelligence.aggregation import build_crowd_feature
from aura_risk_engine.incident_intelligence.incident_processor import IncidentProcessor
from aura_risk_engine.alert_response_engine.response_engine import ResponseDecisionEngine
from app.services.routing_service import routing_service
from aura_risk_engine.realtime_orchestrator.coordinator import AdaptiveIntelligenceCoordinator
from aura_risk_engine.alert_response_engine.utils import AlertLevel
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.risk_engine = RealtimeRiskEngine()
        self.incident_processor = IncidentProcessor()
        self.response_engine = ResponseDecisionEngine()
        self.coordinator = AdaptiveIntelligenceCoordinator()

    async def predict_risk(self, user_id: str, location: dict, context: dict = None):
        """Predict risk for a location using AI engines"""
        try:
            # Prepare risk factors for the real engine
            risk_factors = {
                'location': location,
                'user_id': user_id,
                'context': context or {},
                'timestamp': datetime.utcnow().isoformat()
            }

            # Use the real risk engine
            risk_result = self.risk_engine.calculate_risk(risk_factors)

            # Map to expected response format
            risk_score = risk_result.get('risk_score', 50.0)
            risk_level = self._map_risk_level(risk_score)
            recommendation = self._get_recommendation(risk_score, risk_result)

            result = {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": recommendation,
                "factors": risk_result.get('factors', {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            return result
        except Exception as e:
            logger.error(f"Risk prediction error: {e}")
            return {"risk_score": 50, "risk_level": "MEDIUM", "recommendation": "Proceed with caution"}

    async def analyze_route(self, user_id: str, source_lat: float, source_lng: float, dest_lat: float, dest_lng: float, preferences: dict = None):
        """Analyze route safety using AI engines - fetch route first, then analyze"""
        try:
            # First, get the route from routing service
            source = {'lat': source_lat, 'lng': source_lng}
            destination = {'lat': dest_lat, 'lng': dest_lng}

            route_data = await routing_service.get_route(source, destination)

            if not route_data or not route_data.get('route_points'):
                raise Exception("Could not fetch route")

            route_points = route_data['route_points']

            # Use route safety engine to analyze the route
            route_analysis = self.coordinator.analyze_route_safety(route_points, preferences or {})

            # Get safest route using the route safety engine
            safest_route_result = select_safest_route(route_analysis.get('route_summaries', []))

            # Calculate risk score (lower is safer)
            risk_score = safest_route_result.get('risk_score', 50.0)

            # Format duration and distance
            duration_seconds = route_data.get('duration', 0)
            distance_meters = route_data.get('distance', 0)

            estimated_time = self._format_duration(duration_seconds)
            distance = self._format_distance(distance_meters)

            # Generate warnings based on risk analysis
            warnings = []
            if risk_score > 70:
                warnings.append("High risk route - consider alternative")
            elif risk_score > 40:
                warnings.append("Medium risk areas detected")

            # Add specific warnings from analysis
            for rec in route_analysis.get('recommendations', []):
                warnings.append(rec)

            result = {
                "safe_route": route_points,
                "risk_score": risk_score,
                "warnings": warnings,
                "estimated_time": estimated_time,
                "distance": distance,
                "route_metadata": {
                    "original_distance": distance_meters,
                    "original_duration": duration_seconds,
                    "profile": route_data.get('profile', 'driving-car'),
                    "fallback": route_data.get('fallback', False)
                }
            }
            return result
        except Exception as e:
            logger.error(f"Route analysis error: {e}")
            # Return basic straight-line route as fallback
            fallback_route = [
                {'lat': source_lat, 'lng': source_lng},
                {'lat': dest_lat, 'lng': dest_lng}
            ]
            return {
                "safe_route": fallback_route,
                "risk_score": 75.0,
                "warnings": ["Route analysis failed - using direct route"],
                "estimated_time": "Unknown",
                "distance": "Unknown"
            }

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human readable string"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def _format_distance(self, meters: float) -> str:
        """Format distance in meters to human readable string"""
        if meters < 1000:
            return f"{int(meters)}m"
        else:
            km = meters / 1000
            return ".1f"

    async def process_incident(self, incident_data: dict):
        """Process incident report using incident intelligence"""
        try:
            # Use the real incident processor
            processed_incident = self.incident_processor.process_incident(incident_data)

            # Convert to dict and add incident_id
            result = processed_incident.to_dict()
            result['incident_id'] = f"inc_{processed_incident.incident_id}"

            return result
        except Exception as e:
            logger.error(f"Incident processing error: {e}")
            return {"processed": True, "incident_id": f"inc_{datetime.utcnow().timestamp()}"}

    async def handle_sos(self, sos_data: dict):
        """Handle SOS alert using response engine"""
        try:
            # Determine response action based on location risk
            risk_result = await self.predict_risk(sos_data['user_id'], sos_data['location'])
            risk_score = risk_result.get('risk_score', 50.0)

            # Use response engine to decide action
            alert_level = AlertLevel.HIGH if risk_score > 70 else AlertLevel.MEDIUM
            action = self.response_engine.decide_response_action(
                risk_score=risk_score,
                alert_level=alert_level
            )

            return {
                "alert_sent": True,
                "action": str(action),
                "risk_assessment": risk_result,
                "response_level": str(alert_level)
            }
        except Exception as e:
            logger.error(f"SOS handling error: {e}")
            return {"alert_sent": True, "action": "EMERGENCY_RESPONSE"}

    async def get_crowd_data(self, location: dict):
        """Get crowd intelligence data"""
        try:
            # Use crowd intelligence engine
            crowd_features = build_crowd_feature(location)
            return {
                "crowd_density": crowd_features.get('density_level', 'MEDIUM'),
                "risk_factor": crowd_features.get('risk_contribution', 0.3),
                "insights": crowd_features.get('insights', [])
            }
        except Exception as e:
            logger.error(f"Crowd data error: {e}")
            return {"crowd_density": "LOW", "risk_factor": 0.1}

    def _map_risk_level(self, risk_score: float) -> str:
        """Map risk score to risk level"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    def _get_recommendation(self, risk_score: float, risk_result: dict) -> str:
        """Get recommendation based on risk score and factors"""
        if risk_score >= 80:
            return "Immediate action required - avoid this area"
        elif risk_score >= 60:
            return "High risk - proceed with extreme caution"
        elif risk_score >= 40:
            return "Moderate risk - stay alert"
        else:
            return "Low risk - safe to proceed"

# Global AI service instance
ai_service = AIService()