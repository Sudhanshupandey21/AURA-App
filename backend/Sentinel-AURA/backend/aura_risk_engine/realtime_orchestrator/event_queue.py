"""Async event queue engine with prioritization and deduplication."""

import asyncio
import logging
import time
from typing import Any, Dict

from aura_risk_engine.realtime_orchestrator.state_manager import EnvironmentState
from aura_risk_engine.realtime_orchestrator.risk_recalculator import RealtimeRiskRecalculator
from aura_risk_engine.realtime_orchestrator.broadcaster import BroadcastEngine
from aura_risk_engine.realtime_orchestrator.utils import RealtimeEvent

logger = logging.getLogger(__name__)


class EventQueueEngine:
    """Priority-based queue engine for realtime events."""

    def __init__(self, maxsize: int = 0):
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize)
        self._lock = asyncio.Lock()
        self._processed_event_ids: Dict[str, float] = {}
        self._duplicate_ttl_seconds = 120.0

    async def enqueue(self, event: RealtimeEvent) -> None:
        """Enqueue a realtime event based on computed priority."""
        async with self._lock:
            existing = self._processed_event_ids.get(event.event_id)
            if existing is not None and event.timestamp <= existing:
                logger.debug("Duplicate event skipped: %s", event.event_id)
                return

            await self._queue.put((event.priority, event.timestamp, event))
            self._processed_event_ids[event.event_id] = event.timestamp
            logger.debug("Event queued: %s [%s]", event.event_id, event.event_type)

    async def process_event_queue(
        self,
        state_manager: EnvironmentState,
        risk_recalculator: RealtimeRiskRecalculator,
        broadcaster: BroadcastEngine,
        stop_event: asyncio.Event,
    ) -> None:
        """Process queued events and trigger risk recalculation."""
        while not stop_event.is_set():
            try:
                _, _, event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                await self._cleanup_processed_ids()
                continue

            try:
                await risk_recalculator.handle_event(event)
            except Exception:
                logger.exception("Error handling event %s", event.event_id)
            finally:
                self._queue.task_done()

        logger.info("Event queue processor stopped")

    async def _cleanup_processed_ids(self) -> None:
        """Remove stale event IDs from deduplication cache."""
        cutoff = time.time() - self._duplicate_ttl_seconds
        stale = [
            event_id
            for event_id, timestamp in self._processed_event_ids.items()
            if timestamp < cutoff
        ]
        for event_id in stale:
            del self._processed_event_ids[event_id]
