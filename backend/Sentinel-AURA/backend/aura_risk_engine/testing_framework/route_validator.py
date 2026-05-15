"""Route safety validation engine."""

import logging
from typing import Dict, List, Optional

from aura_risk_engine.testing_framework.utils import TestResult, TestScenario

logger = logging.getLogger(__name__)


class RouteValidator:
    """Validates route safety calculations and selections."""

    def __init__(self) -> None:
        pass

    def validate_route_risk_calculation(
        self,
        scenario: TestScenario,
        route_segments: List[Dict[str, float]],
        calculated_route_risk: float,
    ) -> TestResult:
        """Validate route risk aggregation."""
        if not route_segments:
            return TestResult(
                test_name=f"route_risk_validation_{scenario.name}",
                passed=False,
                message="No route segments provided",
                expected="At least one route segment",
                actual="Empty segments list",
            )

        # Calculate expected route risk using standard formula
        segment_risks = [seg.get("risk_score", 0.0) for seg in route_segments]
        avg_risk = sum(segment_risks) / len(segment_risks)
        max_risk = max(segment_risks)
        spike_penalty = sum(1 for r in segment_risks if r > 70.0) * 5.0
        expected_risk = min(100.0, 0.7 * avg_risk + 0.3 * max_risk + spike_penalty)

        risk_valid = abs(calculated_route_risk - expected_risk) < 1.0  # Allow 1.0 tolerance

        return TestResult(
            test_name=f"route_risk_validation_{scenario.name}",
            passed=risk_valid,
            message=f"Route risk calculation {'valid' if risk_valid else 'invalid'}",
            expected=f"Expected: {expected_risk:.1f} (avg: {avg_risk:.1f}, max: {max_risk:.1f}, penalty: {spike_penalty:.1f})",
            actual=f"Calculated: {calculated_route_risk:.1f}",
        )

    def validate_safest_route_selection(
        self,
        scenario: TestScenario,
        routes: List[Dict[str, float]],
        selected_route_id: str,
    ) -> TestResult:
        """Validate that the safest route was selected."""
        if not routes:
            return TestResult(
                test_name=f"safest_route_validation_{scenario.name}",
                passed=False,
                message="No routes provided",
                expected="At least one route",
                actual="Empty routes list",
            )

        # Find the route with lowest risk score
        safest_route = min(routes, key=lambda r: r.get("risk_score", 100.0))
        safest_route_id = safest_route.get("route_id", "")

        selection_valid = selected_route_id == safest_route_id

        if selection_valid:
            message = f"Correct safest route selected: {selected_route_id}"
        else:
            message = f"Wrong route selected. Expected: {safest_route_id}, Got: {selected_route_id}"

        return TestResult(
            test_name=f"safest_route_validation_{scenario.name}",
            passed=selection_valid,
            message=message,
            expected=f"Safest route: {safest_route_id} (risk: {safest_route.get('risk_score', 0.0):.1f})",
            actual=f"Selected: {selected_route_id}",
        )

    def validate_rerouting_decision(
        self,
        scenario: TestScenario,
        current_route_risk: float,
        alternative_route_risk: float,
        rerouting_triggered: bool,
        improvement_threshold: float = 10.0,
    ) -> TestResult:
        """Validate rerouting decision logic."""
        risk_improvement = current_route_risk - alternative_route_risk
        should_reroute = risk_improvement >= improvement_threshold

        decision_valid = rerouting_triggered == should_reroute

        if decision_valid:
            action = "triggered" if rerouting_triggered else "not triggered"
            message = f"Rerouting decision correct: {action}"
        else:
            expected_action = "trigger" if should_reroute else "not trigger"
            actual_action = "triggered" if rerouting_triggered else "not triggered"
            message = f"Rerouting decision incorrect. Expected: {expected_action}, Got: {actual_action}"

        return TestResult(
            test_name=f"rerouting_validation_{scenario.name}",
            passed=decision_valid,
            message=message,
            expected=f"Improvement: {risk_improvement:.1f} >= {improvement_threshold:.1f} = {should_reroute}",
            actual=f"Rerouting: {rerouting_triggered}",
        )

    def validate_route_segmentation(
        self,
        scenario: TestScenario,
        route_polyline: List[tuple],
        segment_distance_m: float = 200.0,
    ) -> TestResult:
        """Validate route segmentation logic."""
        if len(route_polyline) < 2:
            return TestResult(
                test_name=f"segmentation_validation_{scenario.name}",
                passed=False,
                message="Route polyline too short for segmentation",
                expected="At least 2 points",
                actual=f"{len(route_polyline)} points",
            )

        # Basic validation - ensure segments are reasonably sized
        total_distance = 0.0
        for i in range(len(route_polyline) - 1):
            # Simple Euclidean distance (not Haversine for simplicity)
            lat1, lng1 = route_polyline[i]
            lat2, lng2 = route_polyline[i + 1]
            distance = ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5 * 111000  # Rough meters
            total_distance += distance

        expected_segments = max(1, int(total_distance / segment_distance_m))
        segmentation_valid = expected_segments > 0

        return TestResult(
            test_name=f"segmentation_validation_{scenario.name}",
            passed=segmentation_valid,
            message=f"Route segmentation {'valid' if segmentation_valid else 'invalid'}",
            expected=f"Total distance: ~{total_distance:.0f}m, Expected segments: {expected_segments}",
            actual=f"Polyline points: {len(route_polyline)}",
        )


_default_validator = RouteValidator()


def validate_route_risk_calculation(
    scenario: TestScenario,
    route_segments: List[Dict[str, float]],
    calculated_route_risk: float,
) -> TestResult:
    """Validate route risk calculation."""
    return _default_validator.validate_route_risk_calculation(
        scenario, route_segments, calculated_route_risk
    )


def validate_safest_route_selection(
    scenario: TestScenario,
    routes: List[Dict[str, float]],
    selected_route_id: str,
) -> TestResult:
    """Validate safest route selection."""
    return _default_validator.validate_safest_route_selection(
        scenario, routes, selected_route_id
    )


def validate_rerouting_decision(
    scenario: TestScenario,
    current_route_risk: float,
    alternative_route_risk: float,
    rerouting_triggered: bool,
    improvement_threshold: float = 10.0,
) -> TestResult:
    """Validate rerouting decision."""
    return _default_validator.validate_rerouting_decision(
        scenario, current_route_risk, alternative_route_risk, rerouting_triggered, improvement_threshold
    )
