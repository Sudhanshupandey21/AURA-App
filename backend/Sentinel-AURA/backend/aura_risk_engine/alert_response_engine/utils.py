"""Utility helpers and data models for the Alert & Response Engine."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """Alert severity levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ResponseAction(str, Enum):
    """Possible response actions."""

    CONTINUE_MONITORING = "continue_monitoring"
    ISSUE_CAUTION = "issue_caution"
    RECOMMEND_REROUTE = "recommend_reroute"
    TRIGGER_EMERGENCY = "trigger_emergency"
    ACTIVATE_SOS = "activate_sos"


class AnchorType(str, Enum):
    """Types of safe anchors."""

    POLICE_STATION = "police_station"
    HOSPITAL = "hospital"
    SAFE_ZONE = "safe_zone"
    EMERGENCY_CENTER = "emergency_center"
    PUBLIC_SHELTER = "public_shelter"


@dataclass(frozen=True)
class RiskSnapshot:
    """Snapshot of current risk metrics."""

    risk_score: float
    risk_level: str
    trend: str
    timestamp: float
    active_incidents: int = 0
    crowd_risk: float = 0.0
    light_risk: float = 0.0
    area_type: str = "urban"


@dataclass(frozen=True)
class AlertEvent:
    """An alert event triggered by the system."""

    alert_id: str
    alert_level: AlertLevel
    risk_score: float
    message: str
    recommended_action: ResponseAction
    timestamp: float
    route_id: Optional[str] = None
    current_location: Optional[Dict[str, float]] = None


@dataclass(frozen=True)
class SafeAnchor:
    """A safe location or point of refuge."""

    anchor_id: str
    anchor_type: AnchorType
    name: str
    latitude: float
    longitude: float
    distance_m: float
    verified: bool = True
    contact_info: Optional[str] = None


@dataclass(frozen=True)
class SOSEvent:
    """An SOS emergency event."""

    sos_id: str
    active: bool
    timestamp: float
    location: Dict[str, float]
    location_shared: bool
    emergency_contacts_notified: bool
    authorities_alerted: bool
    reason: Optional[str] = None


def classify_alert_level(risk_score: float) -> AlertLevel:
    """Classify a risk score into an alert level."""
    if risk_score < 40:
        return AlertLevel.LOW
    elif risk_score < 70:
        return AlertLevel.MEDIUM
    elif risk_score < 90:
        return AlertLevel.HIGH
    else:
        return AlertLevel.CRITICAL


def validate_risk_score(score: float) -> float:
    """Validate and normalize a risk score."""
    try:
        score = float(score)
        if not (0.0 <= score <= 100.0):
            raise ValueError(f"Risk score {score} out of range [0.0, 100.0].")
        return score
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid risk score: {e}")


def validate_coordinate(lat: float, lng: float) -> tuple:
    """Validate geographic coordinates."""
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        raise ValueError("Coordinates must be numeric.")

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        raise ValueError(f"Coordinates out of bounds: ({lat}, {lng}).")

    return lat, lng
