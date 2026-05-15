"""Testing framework utilities and data models."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AreaType(str, Enum):
    """Types of urban areas."""

    MARKET = "market"
    STREET = "street"
    TRANSPORT_HUB = "transport_hub"
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    ISOLATED = "isolated"


class IncidentSeverity(str, Enum):
    """Incident severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    """Risk assessment levels."""

    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertLevel(str, Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SystemStatus(str, Enum):
    """Overall system health status."""

    STABLE = "stable"
    DEGRADED = "degraded"
    CRITICAL = "critical"


@dataclass(frozen=True)
class TestScenario:
    """A test scenario with environmental conditions."""

    scenario_id: str
    name: str
    hour: int
    crowd_density: float
    light_intensity: float
    incident_severity: float
    area_type: AreaType
    description: str


@dataclass(frozen=True)
class SimulatedIncident:
    """A simulated incident event."""

    incident_id: str
    severity: float
    location_lat: float
    location_lng: float
    timestamp: float
    description: str


@dataclass(frozen=True)
class TestResult:
    """Result of a single test."""

    test_name: str
    passed: bool
    message: str
    expected: str
    actual: str
    timestamp: float = 0.0


@dataclass(frozen=True)
class TestReport:
    """Aggregated test report."""

    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    system_status: SystemStatus
    average_response_time: float
    median_response_time: float
    min_response_time: float
    max_response_time: float
    test_start_time: float
    test_end_time: float
    detailed_results: List[TestResult]
    summary: str


def normalize_score(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Normalize a value to a numeric range."""
    return float(max(minimum, min(maximum, value)))


def time_hour_to_string(hour: int) -> str:
    """Convert hour (0-23) to readable string."""
    if hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"


def classify_time_period(hour: int) -> str:
    """Classify hour into time period."""
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def calculate_distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Simple distance approximation in meters."""
    import math

    lat_diff = (lat2 - lat1) * 111000  # 1 degree ≈ 111km
    lng_diff = (lng2 - lng1) * 111000 * math.cos(math.radians(lat1))
    return math.sqrt(lat_diff**2 + lng_diff**2)
