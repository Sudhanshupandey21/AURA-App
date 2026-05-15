"""Risk recalculation engine for realtime orchestration."""

import asyncio
import logging
from typing import Any, Dict

from aura_risk_engine.risk_engine import (
    ExplainabilityEngine,
    RiskAggregator,
    RiskClassifier,
    RiskScorer,
    TrendEngine,
)

from aura_risk_engine.realtime_orchestrator.broadcaster import BroadcastEngine
from aura_risk_engine.realtime_orchestrator.state_manager import EnvironmentState
from aura_risk_engine.realtime_orchestrator.utils import EventType, RealtimeEvent, current_timestamp

logger = logging.getLogger(__name__)


class RealtimeRiskRecalculator:
    """Recalculates final risk in response to realtime events."""

    def __init__(
        self,
        state_manager: EnvironmentState,
        broadcaster: BroadcastEngine,
    ) -> None:
        self.state_manager = state_manager
        self.broadcaster = broadcaster
        self.aggregator = RiskAggregator()
        self.scorer = RiskScorer(self.aggregator)
        self.classifier = RiskClassifier()
        self.explainer = ExplainabilityEngine()
        self.trend_engine = TrendEngine(history_size=200)
        self._event_lock = asyncio.Lock()

    async def handle_event(self, event: RealtimeEvent) -> Dict[str, Any]:
        """Process event, update environment state, and recalculate risk."""
        async with self._event_lock:
            self._apply_event_to_state(event)
            output = await self.recalculate_risk()
            return output

    def _apply_event_to_state(self, event: RealtimeEvent) -> None:
        payload = event.payload

        if event.event_type == EventType.INCIDENT_UPDATE:
            severity = float(payload.get("severity", 0.0))
            self.state_manager.update_incident_risk(severity)
        elif event.event_type == EventType.CROWD_UPDATE:
            density = float(payload.get("crowd_risk", payload.get("density", 0.0)))
            self.state_manager.update_crowd_risk(density)
        elif event.event_type == EventType.LIGHT_UPDATE:
            light_value = float(payload.get("light_risk", payload.get("intensity", 0.0)))
            self.state_manager.update_light_risk(light_value)
        elif event.event_type == EventType.TIME_UPDATE:
            time_value = float(payload.get("time_risk", 0.0))
            self.state_manager.update_time_risk(time_value)
        elif event.event_type == EventType.SENSOR_UPDATE:
            sensor_values = payload.get("sensor_values", {})
            self._merge_sensor_readings(sensor_values)
        else:
            logger.warning("Unhandled event type %s", event.event_type)

    def _merge_sensor_readings(self, sensor_values: Dict[str, Any]) -> None:
        if "crowd_risk" in sensor_values:
            self.state_manager.update_crowd_risk(float(sensor_values["crowd_risk"]))
        if "light_risk" in sensor_values:
            self.state_manager.update_light_risk(float(sensor_values["light_risk"]))
        if "incident_risk" in sensor_values:
            self.state_manager.update_incident_risk(float(sensor_values["incident_risk"]))
        if "area_risk" in sensor_values:
            self.state_manager.update_area_risk(float(sensor_values["area_risk"]))
        if "time_risk" in sensor_values:
            self.state_manager.update_time_risk(float(sensor_values["time_risk"]))

    async def recalculate_risk(self) -> Dict[str, Any]:
        current_features = self.state_manager.get_feature_vector()
        previous_score = self.state_manager.get_snapshot().get("current_final_risk", 0)

        final_score = self.scorer.calculate_final_risk_score(**current_features)
        risk_level = self.classifier.classify_risk(final_score)

        trend = self.trend_engine.predict_trend(
            float(final_score),
            previous_score=float(previous_score) if previous_score is not None else None,
        )

        self.trend_engine.add_data_point(float(final_score), current_features)

        reasons = self.explainer.generate_reasons(**current_features)
        component_scores = self.aggregator.calculate_component_scores(**current_features)

        output = {
            "risk_score": final_score,
            "risk_level": risk_level,
            "trend": trend,
            "reasons": reasons,
            "component_scores": component_scores,
            "timestamp": current_timestamp(),
        }

        self.state_manager.update_full_output(output)
        await self.broadcaster.broadcast_risk_update(output)

        logger.info("Recalculated risk: %s", output)
        return output
