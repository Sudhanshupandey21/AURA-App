"""Incident simulation engine."""

import logging
import random
import uuid
from datetime import datetime
from typing import List

from aura_risk_engine.testing_framework.utils import SimulatedIncident, IncidentSeverity

logger = logging.getLogger(__name__)


class IncidentSimulator:
    """Simulates realistic incident events."""

    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)
        self._incidents: List[SimulatedIncident] = []

    def simulate_incidents(
        self,
        scenario_severity: float,
        base_location: tuple = (37.7749, -122.4194),
        count: int = 1,
    ) -> List[SimulatedIncident]:
        """Generate simulated incidents based on severity level."""
        incidents: List[SimulatedIncident] = []

        for _ in range(count):
            # Determine incident severity
            if scenario_severity > 0.8:
                severity = random.choice([IncidentSeverity.HIGH, IncidentSeverity.CRITICAL])
            elif scenario_severity > 0.5:
                severity = random.choice([IncidentSeverity.MEDIUM, IncidentSeverity.HIGH])
            elif scenario_severity > 0.2:
                severity = random.choice([IncidentSeverity.LOW, IncidentSeverity.MEDIUM])
            else:
                severity = IncidentSeverity.LOW

            severity_value = {
                IncidentSeverity.LOW: 0.3,
                IncidentSeverity.MEDIUM: 0.6,
                IncidentSeverity.HIGH: 0.85,
                IncidentSeverity.CRITICAL: 0.95,
            }[severity]

            # Generate random location near base
            lat_offset = random.uniform(-0.01, 0.01)
            lng_offset = random.uniform(-0.01, 0.01)

            incident = SimulatedIncident(
                incident_id=str(uuid.uuid4()),
                severity=severity_value,
                location_lat=base_location[0] + lat_offset,
                location_lng=base_location[1] + lng_offset,
                timestamp=datetime.now().timestamp(),
                description=f"{severity.value.capitalize()} severity incident",
            )

            incidents.append(incident)
            self._incidents.append(incident)
            logger.info(f"Generated {severity.value} incident: {incident.incident_id}")

        return incidents

    def generate_incident_spike(
        self,
        base_location: tuple = (37.7749, -122.4194),
        count: int = 5,
    ) -> List[SimulatedIncident]:
        """Generate a sudden spike of multiple incidents."""
        incidents = []
        for _ in range(count):
            severity_value = random.uniform(0.6, 1.0)

            lat_offset = random.uniform(-0.02, 0.02)
            lng_offset = random.uniform(-0.02, 0.02)

            incident = SimulatedIncident(
                incident_id=str(uuid.uuid4()),
                severity=severity_value,
                location_lat=base_location[0] + lat_offset,
                location_lng=base_location[1] + lng_offset,
                timestamp=datetime.now().timestamp(),
                description=f"Spike incident - severity {severity_value:.0%}",
            )

            incidents.append(incident)
            self._incidents.append(incident)

        logger.warning(f"Generated incident spike: {count} incidents")
        return incidents

    def get_all_incidents(self) -> List[SimulatedIncident]:
        """Get all simulated incidents."""
        return self._incidents.copy()

    def get_recent_incidents(self, count: int = 10) -> List[SimulatedIncident]:
        """Get the most recent incidents."""
        return self._incidents[-count:] if self._incidents else []

    def clear_incidents(self) -> None:
        """Clear all incidents."""
        self._incidents.clear()
        logger.info("Incident history cleared")


_default_simulator = IncidentSimulator()


def simulate_incidents(
    scenario_severity: float,
    base_location: tuple = (37.7749, -122.4194),
    count: int = 1,
) -> List[SimulatedIncident]:
    """Simulate incidents."""
    return _default_simulator.simulate_incidents(scenario_severity, base_location, count)


def generate_incident_spike(
    base_location: tuple = (37.7749, -122.4194),
    count: int = 5,
) -> List[SimulatedIncident]:
    """Generate an incident spike."""
    return _default_simulator.generate_incident_spike(base_location, count)
