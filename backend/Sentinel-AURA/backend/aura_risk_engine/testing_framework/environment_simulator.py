"""Environmental simulation engine."""

import logging
from typing import Dict, Optional

from aura_risk_engine.testing_framework.utils import TestScenario, classify_time_period, normalize_score

logger = logging.getLogger(__name__)


class EnvironmentSimulator:
    """Simulates changing environmental conditions."""

    def __init__(self) -> None:
        self._current_hour: int = 12
        self._current_crowd: float = 0.5
        self._current_light: float = 0.7
        self._simulation_step: int = 0

    def simulate_environment(self, scenario: TestScenario, steps: int = 1) -> Dict[str, float]:
        """Simulate environmental conditions over time steps."""
        self._current_hour = (self._current_hour + steps) % 24
        time_period = classify_time_period(self._current_hour)

        # Adjust crowd density based on time
        if time_period == "morning":
            self._current_crowd = normalize_score(scenario.crowd_density + 0.1)
        elif time_period == "afternoon":
            self._current_crowd = normalize_score(scenario.crowd_density + 0.15)
        elif time_period == "evening":
            self._current_crowd = normalize_score(scenario.crowd_density + 0.05)
        else:  # night
            self._current_crowd = normalize_score(scenario.crowd_density - 0.3)

        # Adjust light based on hour and scenario
        hour_offset = (self._current_hour - 12) / 24.0
        natural_light = max(0.0, 0.7 + 0.3 * (1 - abs(hour_offset * 2)))
        self._current_light = normalize_score(natural_light * scenario.light_intensity)

        self._simulation_step += steps

        result = {
            "hour": self._current_hour,
            "time_period": time_period,
            "crowd_density": self._current_crowd,
            "light_intensity": self._current_light,
            "simulation_step": self._simulation_step,
        }

        logger.debug(
            f"Environment simulated: hour={self._current_hour}, crowd={self._current_crowd:.2f}, light={self._current_light:.2f}"
        )
        return result

    def advance_time_hours(self, hours: int) -> Dict[str, float]:
        """Advance time by specified hours."""
        self._current_hour = (self._current_hour + hours) % 24
        self._simulation_step += hours

        logger.info(f"Time advanced to hour {self._current_hour}")
        return {
            "hour": self._current_hour,
            "time_period": classify_time_period(self._current_hour),
            "simulation_step": self._simulation_step,
        }

    def adjust_crowd_density(self, change: float) -> float:
        """Adjust crowd density by an amount."""
        self._current_crowd = normalize_score(self._current_crowd + change)
        logger.info(f"Crowd density adjusted to {self._current_crowd:.2f}")
        return self._current_crowd

    def adjust_light_intensity(self, change: float) -> float:
        """Adjust light intensity by an amount."""
        self._current_light = normalize_score(self._current_light + change)
        logger.info(f"Light intensity adjusted to {self._current_light:.2f}")
        return self._current_light

    def get_current_state(self) -> Dict[str, float]:
        """Get current environmental state."""
        return {
            "hour": self._current_hour,
            "crowd_density": self._current_crowd,
            "light_intensity": self._current_light,
            "time_period": classify_time_period(self._current_hour),
        }

    def reset(self) -> None:
        """Reset simulator to initial state."""
        self._current_hour = 12
        self._current_crowd = 0.5
        self._current_light = 0.7
        self._simulation_step = 0
        logger.info("Environment simulator reset")


_default_simulator = EnvironmentSimulator()


def simulate_environment(scenario: TestScenario, steps: int = 1) -> Dict[str, float]:
    """Simulate environmental conditions."""
    return _default_simulator.simulate_environment(scenario, steps)
