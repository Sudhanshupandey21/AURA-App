"""Alert detection engine for identifying dangerous conditions."""

import logging
from typing import Optional

from aura_risk_engine.alert_response_engine.utils import AlertLevel, ResponseAction, RiskSnapshot, validate_risk_score

logger = logging.getLogger(__name__)


class AlertDetector:
    """Detects alert conditions based on risk metrics and trends."""

    def __init__(
        self,
        danger_threshold: float = 75.0,
        incident_spike_threshold: int = 2,
        trend_acceleration_threshold: float = 0.15,
    ) -> None:
        self.danger_threshold = validate_risk_score(danger_threshold)
        self.incident_spike_threshold = incident_spike_threshold
        self.trend_acceleration_threshold = trend_acceleration_threshold
        self._previous_risk: Optional[float] = None
        self._previous_incidents: int = 0

    def detect_alert_condition(
        self,
        current_risk: float,
        risk_trend: str,
        active_incidents: int = 0,
        route_safety_change: float = 0.0,
    ) -> bool:
        """Detect if an alert condition is triggered."""
        current_risk = validate_risk_score(current_risk)

        # Danger threshold
        if current_risk > self.danger_threshold:
            logger.info(f"Alert triggered: risk {current_risk} exceeds danger threshold {self.danger_threshold}.")
            return True

        # Sudden incident spike
        incident_delta = active_incidents - self._previous_incidents
        if incident_delta >= self.incident_spike_threshold:
            logger.info(f"Alert triggered: incident spike detected (+{incident_delta} incidents).")
            self._previous_incidents = active_incidents
            return True

        # Rapidly increasing trend
        if risk_trend == "increasing" and self._previous_risk is not None:
            trend_acceleration = (current_risk - self._previous_risk) / max(1.0, self._previous_risk)
            if trend_acceleration >= self.trend_acceleration_threshold:
                logger.info(f"Alert triggered: rapid risk increase detected ({trend_acceleration:.1%}).")
                self._previous_risk = current_risk
                return True

        # Route safety degradation
        if route_safety_change > 0.2:
            logger.info(f"Alert triggered: route safety degraded by {route_safety_change:.1%}.")
            return True

        self._previous_risk = current_risk
        self._previous_incidents = active_incidents
        return False

    def detect_from_snapshot(self, snapshot: RiskSnapshot) -> bool:
        """Detect alert condition from a risk snapshot."""
        return self.detect_alert_condition(
            current_risk=snapshot.risk_score,
            risk_trend=snapshot.trend,
            active_incidents=snapshot.active_incidents,
        )


_default_detector = AlertDetector()


def detect_alert_condition(
    current_risk: float,
    risk_trend: str,
    active_incidents: int = 0,
    route_safety_change: float = 0.0,
) -> bool:
    """Detect if an alert condition is triggered."""
    return _default_detector.detect_alert_condition(
        current_risk,
        risk_trend,
        active_incidents,
        route_safety_change,
    )
