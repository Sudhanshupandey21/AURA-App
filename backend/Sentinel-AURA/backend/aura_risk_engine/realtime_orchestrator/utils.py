"""Utility helpers and event models for realtime orchestration."""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    INCIDENT_UPDATE = "incident_update"
    CROWD_UPDATE = "crowd_update"
    LIGHT_UPDATE = "light_update"
    TIME_UPDATE = "time_update"
    SENSOR_UPDATE = "sensor_update"


class EventPriority(int, Enum):
    HIGH = 10
    MEDIUM = 50
    LOW = 90


def current_timestamp() -> float:
    """Return current UTC timestamp in seconds."""
    return datetime.now(timezone.utc).timestamp()


def build_event_id(event_type: str, timestamp: float, payload: Dict[str, Any]) -> str:
    """Build deterministic event id from payload for deduplication."""
    source = f"{event_type}:{timestamp}:{payload.get('source', '')}:{payload.get('severity', '')}"
    return uuid.uuid5(uuid.NAMESPACE_URL, source).hex


def validate_event_payload(raw_event: Dict[str, Any]) -> None:
    """Validate raw event structure and raise ValueError when invalid."""
    if not isinstance(raw_event, dict):
        raise ValueError("Realtime event must be a dictionary")

    if "event_type" not in raw_event:
        raise ValueError("Realtime event missing event_type")

    if "timestamp" not in raw_event:
        raise ValueError("Realtime event missing timestamp")

    if "payload" not in raw_event:
        raise ValueError("Realtime event missing payload")

    if raw_event["event_type"] not in {et.value for et in EventType}:
        raise ValueError(f"Unsupported event_type: {raw_event['event_type']}")

    if not isinstance(raw_event["payload"], dict):
        raise ValueError("Realtime event payload must be a dictionary")


def compute_event_priority(event_type: EventType, payload: Dict[str, Any]) -> int:
    """Return numeric priority for the event. Lower value means higher processing priority."""
    if event_type == EventType.INCIDENT_UPDATE:
        severity = float(payload.get("severity", 0.0))
        if severity >= 0.75:
            return EventPriority.HIGH
        return EventPriority.MEDIUM

    if event_type == EventType.SENSOR_UPDATE:
        return EventPriority.MEDIUM

    return EventPriority.LOW


@dataclass
class RealtimeEvent:
    """Serialized realtime event with normalized metadata."""
    event_type: EventType
    timestamp: float
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: "")
    priority: int = field(default=EventPriority.LOW)

    def __post_init__(self) -> None:
        if isinstance(self.event_type, str):
            self.event_type = EventType(self.event_type)

        if not isinstance(self.payload, dict):
            raise ValueError("RealtimeEvent payload must be a dictionary")

        if self.timestamp <= 0:
            raise ValueError("RealtimeEvent timestamp must be a positive number")

        if not self.event_id:
            self.event_id = build_event_id(self.event_type.value, self.timestamp, self.payload)

        self.priority = compute_event_priority(self.event_type, self.payload)
        logger.debug("RealtimeEvent initialized: %s", self)

    @classmethod
    def from_raw(cls, raw_event: Dict[str, Any]) -> "RealtimeEvent":
        validate_event_payload(raw_event)
        event_type = EventType(raw_event["event_type"])
        timestamp = float(raw_event["timestamp"])
        payload = raw_event["payload"]
        event_id = raw_event.get("event_id", "")
        return cls(event_type=event_type, timestamp=timestamp, payload=payload, event_id=event_id)
