"""Realtime simulation engine."""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from aura_risk_engine.testing_framework.utils import TestScenario, SimulatedIncident

logger = logging.getLogger(__name__)


class RealtimeSimulator:
    """Simulates realtime events and updates."""

    def __init__(self) -> None:
        self._running: bool = False
        self._update_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._incident_callbacks: List[Callable[[SimulatedIncident], None]] = []

    async def simulate_realtime_updates(
        self,
        scenario: TestScenario,
        duration_seconds: int = 60,
        update_frequency_hz: float = 1.0,
    ) -> List[Dict[str, Any]]:
        """Simulate realtime updates over a duration."""
        self._running = True
        updates: List[Dict[str, Any]] = []
        interval = 1.0 / update_frequency_hz

        try:
            for step in range(int(duration_seconds * update_frequency_hz)):
                if not self._running:
                    break

                # Simulate environmental changes
                hour = (scenario.hour + step // int(3600 * update_frequency_hz)) % 24
                crowd_variation = (step % 100) / 100.0 * 0.2 - 0.1  # ±10% variation
                light_variation = (step % 200) / 200.0 * 0.1 - 0.05  # ±5% variation

                update = {
                    "timestamp": asyncio.get_event_loop().time(),
                    "step": step,
                    "hour": hour,
                    "crowd_density": max(0.0, min(1.0, scenario.crowd_density + crowd_variation)),
                    "light_intensity": max(0.0, min(1.0, scenario.light_intensity + light_variation)),
                    "incident_severity": scenario.incident_severity,
                }

                updates.append(update)

                # Notify callbacks
                for callback in self._update_callbacks:
                    try:
                        callback(update)
                    except Exception as e:
                        logger.error(f"Update callback error: {e}")

                await asyncio.sleep(interval)

        finally:
            self._running = False

        logger.info(f"Realtime simulation completed: {len(updates)} updates")
        return updates

    def register_update_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for realtime updates."""
        self._update_callbacks.append(callback)
        logger.debug("Update callback registered")

    def register_incident_callback(self, callback: Callable[[SimulatedIncident], None]) -> None:
        """Register a callback for incident events."""
        self._incident_callbacks.append(callback)
        logger.debug("Incident callback registered")

    async def trigger_incident_event(self, incident: SimulatedIncident) -> None:
        """Trigger an incident event."""
        for callback in self._incident_callbacks:
            try:
                callback(incident)
            except Exception as e:
                logger.error(f"Incident callback error: {e}")

        logger.info(f"Incident event triggered: {incident.incident_id}")

    def stop_simulation(self) -> None:
        """Stop the current simulation."""
        self._running = False
        logger.info("Realtime simulation stopped")

    def is_running(self) -> bool:
        """Check if simulation is running."""
        return self._running


_default_simulator = RealtimeSimulator()


async def simulate_realtime_updates(
    scenario: TestScenario,
    duration_seconds: int = 60,
    update_frequency_hz: float = 1.0,
) -> List[Dict[str, Any]]:
    """Simulate realtime updates."""
    return await _default_simulator.simulate_realtime_updates(
        scenario, duration_seconds, update_frequency_hz
    )
