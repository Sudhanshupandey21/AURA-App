"""Scenario generator for test simulations."""

import logging
import uuid
from typing import List

from aura_risk_engine.testing_framework.utils import AreaType, TestScenario

logger = logging.getLogger(__name__)


class ScenarioGenerator:
    """Generates predefined and random test scenarios."""

    def __init__(self) -> None:
        self._predefined_scenarios: List[TestScenario] = self._build_predefined_scenarios()

    def _build_predefined_scenarios(self) -> List[TestScenario]:
        """Build a set of common test scenarios."""
        return [
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Safe Daytime Market",
                hour=14,
                crowd_density=0.8,
                light_intensity=0.95,
                incident_severity=0.0,
                area_type=AreaType.MARKET,
                description="Crowded market in broad daylight, excellent visibility and public activity.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Isolated Dark Street",
                hour=23,
                crowd_density=0.1,
                light_intensity=0.1,
                incident_severity=0.0,
                area_type=AreaType.STREET,
                description="Empty street at night with poor lighting and minimal public presence.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Nighttime Low Crowd Zone",
                hour=22,
                crowd_density=0.2,
                light_intensity=0.15,
                incident_severity=0.0,
                area_type=AreaType.RESIDENTIAL,
                description="Residential area at night with few people and dim street lighting.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Recent Assault Nearby",
                hour=21,
                crowd_density=0.3,
                light_intensity=0.25,
                incident_severity=0.9,
                area_type=AreaType.STREET,
                description="Area with recent violent incident reports, elevated caution.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Sudden Incident Spike",
                hour=20,
                crowd_density=0.5,
                light_intensity=0.5,
                incident_severity=0.7,
                area_type=AreaType.COMMERCIAL,
                description="Multiple incidents reported suddenly in commercial district.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Crowded Transport Hub",
                hour=8,
                crowd_density=0.95,
                light_intensity=0.8,
                incident_severity=0.0,
                area_type=AreaType.TRANSPORT_HUB,
                description="Rush hour at transport hub with high foot traffic and adequate lighting.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Early Morning Empty Street",
                hour=5,
                crowd_density=0.05,
                light_intensity=0.0,
                incident_severity=0.0,
                area_type=AreaType.STREET,
                description="Pre-dawn street with no people and complete darkness.",
            ),
            TestScenario(
                scenario_id=str(uuid.uuid4()),
                name="Sunset Emergency Zone",
                hour=18,
                crowd_density=0.4,
                light_intensity=0.4,
                incident_severity=0.85,
                area_type=AreaType.ISOLATED,
                description="Isolated area at sunset with recent critical incident.",
            ),
        ]

    def get_predefined_scenarios(self) -> List[TestScenario]:
        """Get all predefined scenarios."""
        return self._predefined_scenarios

    def generate_custom_scenario(
        self,
        name: str,
        hour: int,
        crowd_density: float,
        light_intensity: float,
        incident_severity: float,
        area_type: AreaType,
        description: str = "",
    ) -> TestScenario:
        """Generate a custom scenario."""
        scenario = TestScenario(
            scenario_id=str(uuid.uuid4()),
            name=name,
            hour=hour % 24,
            crowd_density=max(0.0, min(1.0, crowd_density)),
            light_intensity=max(0.0, min(1.0, light_intensity)),
            incident_severity=max(0.0, min(1.0, incident_severity)),
            area_type=area_type,
            description=description,
        )
        logger.info(f"Generated custom scenario: {name}")
        return scenario

    def get_scenario_by_name(self, name: str) -> TestScenario:
        """Get a predefined scenario by name."""
        for scenario in self._predefined_scenarios:
            if scenario.name.lower() == name.lower():
                return scenario
        raise ValueError(f"Scenario not found: {name}")


_default_generator = ScenarioGenerator()


def get_predefined_scenarios() -> List[TestScenario]:
    """Get all predefined test scenarios."""
    return _default_generator.get_predefined_scenarios()


def generate_custom_scenario(
    name: str,
    hour: int,
    crowd_density: float,
    light_intensity: float,
    incident_severity: float,
    area_type: AreaType,
    description: str = "",
) -> TestScenario:
    """Generate a custom test scenario."""
    return _default_generator.generate_custom_scenario(
        name,
        hour,
        crowd_density,
        light_intensity,
        incident_severity,
        area_type,
        description,
    )
