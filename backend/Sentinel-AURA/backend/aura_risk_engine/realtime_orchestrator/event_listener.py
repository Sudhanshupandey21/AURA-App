"""Event listener system for realtime orchestration."""

import asyncio
import logging
from typing import Any

from aura_risk_engine.realtime_orchestrator.event_queue import EventQueueEngine
from aura_risk_engine.realtime_orchestrator.utils import RealtimeEvent, validate_event_payload

logger = logging.getLogger(__name__)


async def listen_for_events(
    incoming_queue: asyncio.Queue,
    queue_engine: EventQueueEngine,
    stop_event: asyncio.Event,
) -> None:
    """Continuously listen for raw events and enqueue validated realtime events."""
    while not stop_event.is_set():
        try:
            raw_event = await asyncio.wait_for(incoming_queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        try:
            validate_event_payload(raw_event)
            event = RealtimeEvent.from_raw(raw_event)
        except ValueError as exc:
            logger.warning("Skipping invalid incoming event: %s", exc)
            continue

        try:
            await queue_engine.enqueue(event)
            logger.debug("Enqueued event %s", event.event_id)
        except Exception as exc:
            logger.exception("Failed to enqueue event %s: %s", event.event_id, exc)

    logger.info("Event listener stopped")
