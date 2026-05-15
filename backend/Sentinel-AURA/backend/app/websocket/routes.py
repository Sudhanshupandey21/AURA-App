from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import ws_manager
from app.utils.logger import logger
import json

router = APIRouter()

@router.websocket("/ws/live-tracking")
async def live_tracking_websocket(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time location tracking and risk updates"""
    await ws_manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type")

                if message_type == "location_update":
                    location_data = message.get("data", {})
                    await ws_manager.handle_live_location(user_id, location_data)

                elif message_type == "heartbeat":
                    # Respond to heartbeat
                    await websocket.send_json({"type": "heartbeat_ack"})

            except json.JSONDecodeError:
                logger.warning("Invalid JSON received", user_id=user_id, data=data)

    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)
    except Exception as e:
        logger.error("WebSocket error", user_id=user_id, error=str(e))
        ws_manager.disconnect(user_id)