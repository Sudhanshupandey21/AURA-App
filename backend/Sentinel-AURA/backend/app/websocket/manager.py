import asyncio
from typing import Dict, Set
import json
from fastapi import WebSocket, WebSocketDisconnect
from app.services.ai_service import ai_service
from app.utils.logger import logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_locations: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info("User connected", user_id=user_id)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_locations:
            del self.user_locations[user_id]
        logger.info("User disconnected", user_id=user_id)

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast(self, message: dict, exclude_user: str = None):
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error("Broadcast error", user_id=user_id, error=str(e))

    async def handle_live_location(self, user_id: str, location_data: dict):
        """Handle live location updates and trigger AI risk assessment"""
        self.user_locations[user_id] = location_data

        # Trigger AI risk prediction
        risk_result = await ai_service.predict_risk(user_id, location_data)

        # Send risk update back to user
        risk_message = {
            "type": "risk_update",
            "data": risk_result,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        await self.send_personal_message(risk_message, user_id)

        # Broadcast to nearby users if high risk
        if risk_result.get("risk_level") == "HIGH":
            alert_message = {
                "type": "emergency_alert",
                "data": {
                    "location": location_data,
                    "alert_type": "high_risk_area"
                }
            }
            await self.broadcast(alert_message, exclude_user=user_id)

    async def send_emergency_alert(self, user_id: str, alert_data: dict):
        """Send emergency alert to all connected users"""
        emergency_message = {
            "type": "emergency_alert",
            "data": alert_data
        }
        await self.broadcast(emergency_message)

# Global WebSocket manager
ws_manager = WebSocketManager()