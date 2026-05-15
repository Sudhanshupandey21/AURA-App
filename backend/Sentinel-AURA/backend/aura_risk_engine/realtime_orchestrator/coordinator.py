"""Coordinator to synchronize realtime orchestration engines."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from aura_risk_engine.realtime_orchestrator.broadcaster import BroadcastEngine
from aura_risk_engine.realtime_orchestrator.event_listener import listen_for_events
from aura_risk_engine.realtime_orchestrator.event_queue import EventQueueEngine
from aura_risk_engine.realtime_orchestrator.risk_recalculator import RealtimeRiskRecalculator
from aura_risk_engine.realtime_orchestrator.scheduler import TimeScheduler
from aura_risk_engine.realtime_orchestrator.state_manager import EnvironmentState
from aura_risk_engine.realtime_orchestrator.utils import RealtimeEvent, current_timestamp

logger = logging.getLogger(__name__)


@dataclass
class CoordinatorConfig:
    event_queue_size: int = 0
    scheduler_interval_seconds: float = 10.0
    backpressure_threshold: int = 20
    max_concurrent_tasks: int = 4


class AdaptiveIntelligenceCoordinator:
    """Central coordinator for live AURA X orchestration."""

    def __init__(self, config: Optional[CoordinatorConfig] = None) -> None:
        self.config = config or CoordinatorConfig()
        self.stop_event = asyncio.Event()
        self.incoming_queue: asyncio.Queue = asyncio.Queue()
        self.event_queue_engine = EventQueueEngine(maxsize=self.config.event_queue_size)
        self.state_manager = EnvironmentState()
        self.broadcaster = BroadcastEngine()
        self.recalculator = RealtimeRiskRecalculator(self.state_manager, self.broadcaster)
        self.scheduler = TimeScheduler(self.event_queue_engine, interval_seconds=self.config.scheduler_interval_seconds)
        self._tasks = []
        self._monitor_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start all realtime orchestration tasks."""
        logger.info("Starting Adaptive Intelligence Coordinator")
        self.stop_event.clear()

        self._tasks = [
            asyncio.create_task(listen_for_events(self.incoming_queue, self.event_queue_engine, self.stop_event)),
            asyncio.create_task(self.event_queue_engine.process_event_queue(self.state_manager, self.recalculator, self.broadcaster, self.stop_event)),
            asyncio.create_task(self.scheduler.start(self.stop_event)),
        ]
        self._monitor_task = asyncio.create_task(self._monitor_system())

    async def stop(self) -> None:
        """Stop all realtime orchestration tasks."""
        logger.info("Stopping Adaptive Intelligence Coordinator")
        self.stop_event.set()
        if self._monitor_task:
            await self._monitor_task
        await asyncio.gather(*self._tasks, return_exceptions=True)

    async def _monitor_system(self) -> None:
        """Monitor queue backlog and adapt scheduling behavior."""
        while not self.stop_event.is_set():
            queue_size = self.event_queue_engine._queue.qsize()
            if queue_size > self.config.backpressure_threshold:
                old_interval = self.scheduler.interval_seconds
                self.scheduler.interval_seconds = max(1.0, old_interval * 0.75)
                logger.warning(
                    "Backpressure detected (queue=%d). Accelerating scheduler interval from %.1f to %.1f",
                    queue_size,
                    old_interval,
                    self.scheduler.interval_seconds,
                )
            await asyncio.sleep(1.0)

    async def submit_event(self, raw_event: Dict[str, Any]) -> None:
        """Submit a raw event into the incoming pipeline."""
        await self.incoming_queue.put(raw_event)
        logger.debug("Submitted raw event to incoming queue: %s", raw_event)

    async def get_state_snapshot(self) -> Dict[str, Any]:
        """Return current snapshot of environment state."""
        return self.state_manager.get_snapshot()

    async def register_frontend_listener(self, listener: asyncio.Queue) -> None:
        """Register a frontend listener for realtime risk broadcasts."""
        await self.broadcaster.register_listener(listener)

    async def unregister_frontend_listener(self, listener: asyncio.Queue) -> None:
        """Unregister a frontend listener."""
        await self.broadcaster.unregister_listener(listener)


async def coordinate_realtime_intelligence(config: Optional[CoordinatorConfig] = None) -> AdaptiveIntelligenceCoordinator:
    """Create and start the Adaptive Intelligence Coordinator."""
    coordinator = AdaptiveIntelligenceCoordinator(config)
    await coordinator.start()
    logger.info("Realtime intelligence coordination started at %s", current_timestamp())
    return coordinator
