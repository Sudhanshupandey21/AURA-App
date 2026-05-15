"""Environment state manager for realtime risk orchestration."""

import logging
import threading
from typing import Any, Dict

logger = logging.getLogger(__name__)


class EnvironmentState:
    """Centralized environment state store with thread-safe access."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = {
            "current_time_risk": 0.0,
            "current_crowd_risk": 0.0,
            "current_light_risk": 0.0,
            "current_incident_risk": 0.0,
            "current_area_risk": 0.0,
            "current_final_risk": 0,
            "current_risk_level": "SAFE",
            "current_trend": "stable",
            "last_updated": None,
        }

    def update_time_risk(self, value: float) -> None:
        """Update time-based risk factor."""
        with self._lock:
            self._state["current_time_risk"] = self._clamp(value)
            self._state["last_updated"] = self._now()
            logger.debug("Updated time risk to %.3f", value)

    def update_crowd_risk(self, value: float) -> None:
        """Update crowd density risk factor."""
        with self._lock:
            self._state["current_crowd_risk"] = self._clamp(value)
            self._state["last_updated"] = self._now()
            logger.debug("Updated crowd risk to %.3f", value)

    def update_light_risk(self, value: float) -> None:
        """Update light intensity risk factor."""
        with self._lock:
            self._state["current_light_risk"] = self._clamp(value)
            self._state["last_updated"] = self._now()
            logger.debug("Updated light risk to %.3f", value)

    def update_incident_risk(self, value: float) -> None:
        """Update incident risk factor. Keeps the highest active severity."""
        with self._lock:
            current = self._state["current_incident_risk"]
            self._state["current_incident_risk"] = max(current, self._clamp(value))
            self._state["last_updated"] = self._now()
            logger.debug("Updated incident risk from %.3f to %.3f", current, self._state["current_incident_risk"])

    def update_area_risk(self, value: float) -> None:
        """Update area-level risk factor."""
        with self._lock:
            self._state["current_area_risk"] = self._clamp(value)
            self._state["last_updated"] = self._now()
            logger.debug("Updated area risk to %.3f", value)

    def update_full_output(self, output: Dict[str, Any]) -> None:
        """Update final risk output in state."""
        with self._lock:
            self._state["current_final_risk"] = int(output.get("risk_score", 0))
            self._state["current_risk_level"] = output.get("risk_level", "SAFE")
            self._state["current_trend"] = output.get("trend", "stable")
            self._state["last_updated"] = output.get("timestamp")
            self._state["last_output"] = output
            logger.debug("Updated final risk output: %s", output)

    def get_snapshot(self) -> Dict[str, Any]:
        """Return a thread-safe copy of current environment state."""
        with self._lock:
            return {**self._state}

    def get_feature_vector(self) -> Dict[str, float]:
        """Return the current normalized risk factors for recalculation."""
        with self._lock:
            return {
                "time_risk": self._state["current_time_risk"],
                "crowd_risk": self._state["current_crowd_risk"],
                "light_risk": self._state["current_light_risk"],
                "incident_risk": self._state["current_incident_risk"],
                "area_risk": self._state["current_area_risk"],
            }

    @staticmethod
    def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
        return max(minimum, min(maximum, float(value)))

    @staticmethod
    def _now() -> float:
        from time import time
        return time()

    def reset(self) -> None:
        """Reset environment state to initial values."""
        with self._lock:
            self.__init__()
            logger.info("Environment state reset")
