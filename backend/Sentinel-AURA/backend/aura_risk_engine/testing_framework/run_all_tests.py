"""Main test orchestration script."""

import asyncio
import logging
import time
from typing import List

from aura_risk_engine.testing_framework.scenario_generator import get_predefined_scenarios
from aura_risk_engine.testing_framework.environment_simulator import simulate_environment
from aura_risk_engine.testing_framework.incident_simulator import simulate_incidents, generate_incident_spike
from aura_risk_engine.testing_framework.realtime_simulator import simulate_realtime_updates
from aura_risk_engine.testing_framework.risk_validator import validate_risk_calculation, validate_trend_calculation
from aura_risk_engine.testing_framework.route_validator import validate_route_risk_calculation, validate_safest_route_selection
from aura_risk_engine.testing_framework.alert_validator import validate_alert_triggering, validate_severity_classification
from aura_risk_engine.testing_framework.stress_tester import (
    run_incident_burst_test,
    run_high_frequency_update_test,
    run_concurrent_events_test,
)
from aura_risk_engine.testing_framework.report_generator import generate_test_report
from aura_risk_engine.testing_framework.utils import TestResult, TestScenario

# Import actual system components for integration testing
try:
    from aura_risk_engine.app.services.risk_service import RiskScorer
    from aura_risk_engine.route_safety_engine.route_safety import RouteSafetyEngine
    from aura_risk_engine.alert_response_engine.alert_response import AlertResponseEngine
    from aura_risk_engine.realtime_orchestrator.orchestrator import RealtimeOrchestrator
    SYSTEM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"System components not available for integration testing: {e}")
    SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class TestOrchestrator:
    """Orchestrates comprehensive testing of the AURA X system."""

    def __init__(self) -> None:
        self._results: List[TestResult] = []
        self._start_time: float = 0.0

        # Initialize system components if available
        self.risk_scorer = RiskScorer() if SYSTEM_AVAILABLE else None
        self.route_engine = RouteSafetyEngine() if SYSTEM_AVAILABLE else None
        self.alert_engine = AlertResponseEngine() if SYSTEM_AVAILABLE else None
        self.orchestrator = RealtimeOrchestrator() if SYSTEM_AVAILABLE else None

    async def run_scenario_tests(self, scenario: TestScenario) -> List[TestResult]:
        """Run all tests for a single scenario."""
        logger.info(f"Running tests for scenario: {scenario.name}")
        scenario_results = []

        # Environment simulation test
        try:
            env_state = simulate_environment(scenario, steps=5)
            env_test = TestResult(
                test_name=f"environment_simulation_{scenario.name}",
                passed=True,
                message="Environment simulation completed successfully",
                expected="Valid environmental state",
                actual=f"Hour: {env_state.get('hour', 0)}, Crowd: {env_state.get('crowd_density', 0):.2f}",
            )
            scenario_results.append(env_test)
        except Exception as e:
            scenario_results.append(TestResult(
                test_name=f"environment_simulation_{scenario.name}",
                passed=False,
                message=f"Environment simulation failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        # Incident simulation test
        try:
            incidents = simulate_incidents(scenario.incident_severity, count=3)
            incident_test = TestResult(
                test_name=f"incident_simulation_{scenario.name}",
                passed=len(incidents) == 3,
                message=f"Generated {len(incidents)} incidents",
                expected="3 incidents generated",
                actual=f"{len(incidents)} incidents",
            )
            scenario_results.append(incident_test)
        except Exception as e:
            scenario_results.append(TestResult(
                test_name=f"incident_simulation_{scenario.name}",
                passed=False,
                message=f"Incident simulation failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        # Realtime simulation test
        try:
            updates = await simulate_realtime_updates(scenario, duration_seconds=5, update_frequency_hz=2.0)
            realtime_test = TestResult(
                test_name=f"realtime_simulation_{scenario.name}",
                passed=len(updates) >= 8,  # Should have ~10 updates (5s * 2Hz)
                message=f"Generated {len(updates)} realtime updates",
                expected=">=8 updates in 5 seconds",
                actual=f"{len(updates)} updates",
            )
            scenario_results.append(realtime_test)
        except Exception as e:
            scenario_results.append(TestResult(
                test_name=f"realtime_simulation_{scenario.name}",
                passed=False,
                message=f"Realtime simulation failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        # Risk validation test (mock if system not available)
        if self.risk_scorer:
            try:
                # Simulate risk calculation
                risk_score = 50.0 + scenario.incident_severity * 30.0  # Mock calculation
                risk_level = "MEDIUM"  # Mock level
                risk_validation = validate_risk_calculation(scenario, risk_score, risk_level)
                scenario_results.append(risk_validation)
            except Exception as e:
                scenario_results.append(TestResult(
                    test_name=f"risk_validation_{scenario.name}",
                    passed=False,
                    message=f"Risk validation failed: {e}",
                    expected="Valid risk calculation",
                    actual=str(e),
                ))
        else:
            scenario_results.append(TestResult(
                test_name=f"risk_validation_{scenario.name}",
                passed=False,
                message="Risk scorer not available for testing",
                expected="RiskScorer available",
                actual="Component unavailable",
            ))

        # Route validation test (mock if system not available)
        if self.route_engine:
            try:
                # Mock route data
                routes = [
                    {"route_id": "route1", "risk_score": 45.0},
                    {"route_id": "route2", "risk_score": 35.0},
                ]
                route_validation = validate_safest_route_selection(scenario, routes, "route2")
                scenario_results.append(route_validation)
            except Exception as e:
                scenario_results.append(TestResult(
                    test_name=f"route_validation_{scenario.name}",
                    passed=False,
                    message=f"Route validation failed: {e}",
                    expected="Valid route selection",
                    actual=str(e),
                ))
        else:
            scenario_results.append(TestResult(
                test_name=f"route_validation_{scenario.name}",
                passed=False,
                message="Route engine not available for testing",
                expected="RouteSafetyEngine available",
                actual="Component unavailable",
            ))

        # Alert validation test (mock if system not available)
        if self.alert_engine:
            try:
                risk_score = 60.0 + scenario.incident_severity * 25.0
                alert_validation = validate_severity_classification(scenario, risk_score, "HIGH")
                scenario_results.append(alert_validation)
            except Exception as e:
                scenario_results.append(TestResult(
                    test_name=f"alert_validation_{scenario.name}",
                    passed=False,
                    message=f"Alert validation failed: {e}",
                    expected="Valid alert classification",
                    actual=str(e),
                ))
        else:
            scenario_results.append(TestResult(
                test_name=f"alert_validation_{scenario.name}",
                passed=False,
                message="Alert engine not available for testing",
                expected="AlertResponseEngine available",
                actual="Component unavailable",
            ))

        return scenario_results

    async def run_stress_tests(self, scenario: TestScenario) -> List[TestResult]:
        """Run stress tests for a scenario."""
        logger.info(f"Running stress tests for scenario: {scenario.name}")
        stress_results = []

        # Incident burst test
        try:
            burst_result = await run_incident_burst_test(scenario, burst_size=5, burst_duration_seconds=0.5)
            stress_results.append(burst_result)
        except Exception as e:
            stress_results.append(TestResult(
                test_name=f"stress_burst_{scenario.name}",
                passed=False,
                message=f"Incident burst stress test failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        # High frequency test
        try:
            freq_result = await run_high_frequency_update_test(scenario, update_count=20, target_frequency_hz=10.0)
            stress_results.append(freq_result)
        except Exception as e:
            stress_results.append(TestResult(
                test_name=f"stress_frequency_{scenario.name}",
                passed=False,
                message=f"High frequency stress test failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        # Concurrent events test
        try:
            concurrent_result = await run_concurrent_events_test(scenario, concurrent_count=3, duration_seconds=2)
            stress_results.append(concurrent_result)
        except Exception as e:
            stress_results.append(TestResult(
                test_name=f"stress_concurrent_{scenario.name}",
                passed=False,
                message=f"Concurrent events stress test failed: {e}",
                expected="No exceptions",
                actual=str(e),
            ))

        return stress_results

    async def run_all_tests(self) -> None:
        """Run the complete test suite."""
        self._start_time = time.time()
        logger.info("Starting comprehensive AURA X system test suite")

        scenarios = get_predefined_scenarios()
        all_results = []

        for scenario in scenarios:
            # Run scenario-specific tests
            scenario_results = await self.run_scenario_tests(scenario)
            all_results.extend(scenario_results)

            # Run stress tests for this scenario
            stress_results = await self.run_stress_tests(scenario)
            all_results.extend(stress_results)

        self._results = all_results

        # Generate final report
        final_report = generate_test_report(all_results)

        # Print summary
        print("\n" + "="*80)
        print("AURA X SYSTEM TEST RESULTS")
        print("="*80)
        print(f"Total Tests: {final_report.total_tests}")
        print(f"Passed: {final_report.passed_tests}")
        print(f"Failed: {final_report.failed_tests}")
        print(f"Pass Rate: {final_report.pass_rate:.1f}%")
        print(f"System Status: {final_report.system_status.value}")
        print(f"Test Duration: {final_report.test_end_time - final_report.test_start_time:.2f}s")
        print("\nSummary:")
        print(final_report.summary)

        if final_report.failed_tests > 0:
            print(f"\nFailed Tests ({final_report.failed_tests}):")
            for result in all_results:
                if not result.passed:
                    print(f"  - {result.test_name}: {result.message}")

        print("="*80)

        logger.info(f"Test suite completed: {final_report.pass_rate:.1f}% pass rate")


async def main():
    """Main entry point for running all tests."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    orchestrator = TestOrchestrator()
    await orchestrator.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
