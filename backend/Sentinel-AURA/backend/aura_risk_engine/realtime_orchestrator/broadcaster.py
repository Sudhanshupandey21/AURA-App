"""Broadcast engine for realtime risk outputs."""

import asyncio
import logging
from typing import Any, Dict, Set

logger = logging.getLogger(__name__)


class BroadcastEngine:
    """Broadcast updates to multiple realtime subscribers."""

    def __init__(self) -> None:
        self._listeners: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def register_listener(self, listener: asyncio.Queue) -> None:
        """Register a subscriber queue for broadcast messages."""
        async with self._lock:
            self._listeners.add(listener)
            logger.debug("Registered broadcast listener %s", listener)

    async def unregister_listener(self, listener: asyncio.Queue) -> None:
        """Unregister a subscriber queue."""
        async with self._lock:
            self._listeners.discard(listener)
            logger.debug("Unregistered broadcast listener %s", listener)

    async def broadcast_risk_update(self, payload: Dict[str, Any]) -> None:
        """Broadcast risk update payload to all listeners."""
        async with self._lock:
            listeners = list(self._listeners)

        if not listeners:
            logger.debug("No broadcast listeners registered")
            return

        logger.info("Broadcasting risk update to %d listeners", len(listeners))
        tasks = [listener.put(payload) for listener in listeners]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_named_targets(
        self,
        payload: Dict[str, Any],
        target_callbacks: Dict[str, Any],
    ) -> None:
        """Broadcast to additional named targets or external systems."""
        if not target_callbacks:
            return

        tasks = []
        for name, callback in target_callbacks.items():
            try:
                tasks.append(callback(payload))
            except Exception:
                logger.exception("Failed to enqueue callback for %s", name)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
