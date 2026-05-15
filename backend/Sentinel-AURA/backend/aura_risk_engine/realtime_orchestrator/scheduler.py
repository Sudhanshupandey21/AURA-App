"""Scheduler for periodic time updates in realtime orchestration."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from aura_risk_engine.realtime_orchestrator.event_queue import EventQueueEngine
from aura_risk_engine.realtime_orchestrator.utils import EventType, RealtimeEvent, current_timestamp

logger = logging.getLogger(__name__)


class TimeScheduler:
    """Scheduler that emits time update events at a configured interval."""

    def __init__(
        self,
        event_queue: EventQueueEngine,
        interval_seconds: float = 10.0,
    ) -> None:
        self.event_queue = event_queue
        self.interval_seconds = max(1.0, float(interval_seconds))
        self._task: Optional[asyncio.Task] = None

    async def start(self, stop_event: asyncio.Event) -> None:
        """Start the scheduler loop."""
        logger.info("Time scheduler starting with interval=%s", self.interval_seconds)
        while not stop_event.is_set():
            event = self._build_time_event()
            await self.event_queue.enqueue(event)
            await asyncio.sleep(self.interval_seconds)

    def _build_time_event(self) -> RealtimeEvent:
        utc_now = datetime.now(timezone.utc)
        payload = {"time_risk": self._time_risk_from_clock(utc_now)}
        return RealtimeEvent(
            event_type=EventType.TIME_UPDATE,
            timestamp=current_timestamp(),
            payload=payload,
        )

    @staticmethod
    def _time_risk_from_clock(now: datetime) -> float:
        hour = now.hour
        if 0 <= hour < 5:
            return 0.85
        if 5 <= hour < 8:
            return 0.65
        if 8 <= hour < 18:
            return 0.25
        if 18 <= hour < 22:
            return 0.60
        return 0.75


async def start_scheduler(
    event_queue: EventQueueEngine,
    stop_event: asyncio.Event,
    interval_seconds: float = 10.0,
) -> None:
    """Create and start the scheduler task."""
    scheduler = TimeScheduler(event_queue, interval_seconds=interval_seconds)
    await scheduler.start(stop_event)
