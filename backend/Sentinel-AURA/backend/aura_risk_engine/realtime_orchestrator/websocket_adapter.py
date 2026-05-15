"""WebSocket-ready adapter for realtime broadcast integration."""

import asyncio
import logging
from typing import Any, Dict, Set

logger = logging.getLogger(__name__)


class WebSocketConnection:
    """Simulated WebSocket connection for send-only streaming."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._queue: asyncio.Queue = asyncio.Queue()

    async def send_json(self, payload: Dict[str, Any]) -> None:
        """Send JSON payload to the connection queue."""
        await self._queue.put(payload)
        logger.debug("Queued message for WebSocket %s", self.name)

    async def receive(self) -> Dict[str, Any]:
        """Receive the next message from the simulated connection."""
        return await self._queue.get()

    def __repr__(self) -> str:
        return f"WebSocketConnection(name={self.name})"


class WebSocketAdapter:
    """Adapter to manage WebSocket-style connections."""

    def __init__(self) -> None:
        self._connections: Set[WebSocketConnection] = set()
        self._lock = asyncio.Lock()

    async def register_connection(self, connection: WebSocketConnection) -> None:
        async with self._lock:
            self._connections.add(connection)
            logger.debug("Registered websocket connection %s", connection)

    async def unregister_connection(self, connection: WebSocketConnection) -> None:
        async with self._lock:
            self._connections.discard(connection)
            logger.debug("Unregistered websocket connection %s", connection)

    async def broadcast(self, payload: Dict[str, Any]) -> None:
        async with self._lock:
            connections = list(self._connections)

        if not connections:
            logger.debug("No websocket connections to broadcast")
            return

        tasks = []
        for connection in connections:
            tasks.append(connection.send_json(payload))

        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Broadcasted payload to %d websocket connections", len(connections))
