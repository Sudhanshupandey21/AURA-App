"""Continuous background monitoring engine for realtime alert detection."""

import asyncio
import logging
from typing import Callable, Dict, List, Optional

from aura_risk_engine.alert_response_engine.alert_detector import AlertDetector
from aura_risk_engine.alert_response_engine.explainability import generate_alert_message
from aura_risk_engine.alert_response_engine.response_engine import ResponseDecisionEngine
from aura_risk_engine.alert_response_engine.severity_classifier import SeverityClassifier
from aura_risk_engine.alert_response_engine.utils import AlertEvent, ResponseAction, RiskSnapshot, AlertLevel

logger = logging.getLogger(__name__)


class ContinuousMonitoringEngine:
    """Monitors route safety in real time and generates adaptive alerts."""

    def __init__(
        self,
        check_interval_seconds: float = 5.0,
    ) -> None:
        self.check_interval_seconds = check_interval_seconds
        self._monitoring_active = False
        self._alert_detector = AlertDetector()
        self._classifier = SeverityClassifier()
        self._response_engine = ResponseDecisionEngine()
        self._alert_callbacks: List[Callable] = []
        self._risk_history: List[RiskSnapshot] = []

    def register_alert_callback(self, callback: Callable) -> None:
        """Register a callback function to handle generated alerts."""
        self._alert_callbacks.append(callback)
        logger.debug(f"Registered alert callback: {callback.__name__}")

    async def continuous_monitoring_loop(
        self,
        risk_provider: Callable,
        stop_event: asyncio.Event,
        location_provider: Optional[Callable] = None,
    ) -> None:
        """Run continuous monitoring loop."""
        self._monitoring_active = True
        logger.info("Continuous monitoring started.")

        try:
            while not stop_event.is_set():
                try:
                    # Get current risk snapshot
                    risk_snapshot = await self._fetch_risk_snapshot(risk_provider)
                    self._risk_history.append(risk_snapshot)

                    # Keep history bounded
                    if len(self._risk_history) > 100:
                        self._risk_history.pop(0)

                    # Check for alert condition
                    alert_triggered = self._alert_detector.detect_from_snapshot(risk_snapshot)

                    if alert_triggered:
                        alert_event = self._generate_alert_event(risk_snapshot, location_provider)
                        await self._dispatch_alert(alert_event)

                except Exception as e:
                    logger.exception(f"Error during monitoring iteration: {e}")

                # Wait for next check
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=self.check_interval_seconds)
                    break
                except asyncio.TimeoutError:
                    continue

        finally:
            self._monitoring_active = False
            logger.info("Continuous monitoring stopped.")

    async def _fetch_risk_snapshot(self, risk_provider: Callable) -> RiskSnapshot:
        """Fetch current risk snapshot from provider."""
        if asyncio.iscoroutinefunction(risk_provider):
            data = await risk_provider()
        else:
            data = risk_provider()

        if isinstance(data, RiskSnapshot):
            return data

        if isinstance(data, dict):
            return RiskSnapshot(
                risk_score=float(data.get("risk_score", 0.0)),
                risk_level=data.get("risk_level", "SAFE"),
                trend=data.get("trend", "stable"),
                timestamp=data.get("timestamp", 0.0),
                active_incidents=data.get("active_incidents", 0),
                crowd_risk=data.get("crowd_risk", 0.0),
                light_risk=data.get("light_risk", 0.0),
                area_type=data.get("area_type", "urban"),
            )

        raise ValueError(f"Invalid risk snapshot format: {type(data)}")

    def _generate_alert_event(
        self,
        snapshot: RiskSnapshot,
        location_provider: Optional[Callable],
    ) -> AlertEvent:
        """Generate an alert event from a risk snapshot."""
        alert_level = self._classifier.classify_alert_level(snapshot.risk_score)
        response_action = self._response_engine.decide_response_action(
            risk_score=snapshot.risk_score,
            alert_level=alert_level,
            risk_trend=snapshot.trend,
            active_incidents=snapshot.active_incidents,
        )

        message = generate_alert_message(alert_level, snapshot.risk_score, f"Trend: {snapshot.trend}.")

        location = None
        if location_provider:
            if asyncio.iscoroutinefunction(location_provider):
                location = asyncio.run(location_provider())
            else:
                location = location_provider()

        import uuid

        alert_event = AlertEvent(
            alert_id=str(uuid.uuid4()),
            alert_level=alert_level,
            risk_score=snapshot.risk_score,
            message=message,
            recommended_action=response_action,
            timestamp=snapshot.timestamp,
            current_location=location,
        )

        return alert_event

    async def _dispatch_alert(self, alert_event: AlertEvent) -> None:
        """Dispatch alert to registered callbacks."""
        logger.info(f"Dispatching alert: {alert_event.alert_level} ({alert_event.risk_score:.0f})")

        tasks = []
        for callback in self._alert_callbacks:
            if asyncio.iscoroutinefunction(callback):
                tasks.append(callback(alert_event))
            else:
                try:
                    callback(alert_event)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def is_monitoring_active(self) -> bool:
        """Check if monitoring is currently active."""
        return self._monitoring_active

    def get_risk_history(self, limit: int = 10) -> List[RiskSnapshot]:
        """Get recent risk history."""
        return self._risk_history[-limit:] if self._risk_history else []


_default_monitoring_engine = ContinuousMonitoringEngine()


async def continuous_monitoring_loop(
    risk_provider: Callable,
    stop_event: asyncio.Event,
    location_provider: Optional[Callable] = None,
    check_interval_seconds: float = 5.0,
) -> None:
    """Start continuous monitoring."""
    engine = ContinuousMonitoringEngine(check_interval_seconds=check_interval_seconds)
    await engine.continuous_monitoring_loop(risk_provider, stop_event, location_provider)
