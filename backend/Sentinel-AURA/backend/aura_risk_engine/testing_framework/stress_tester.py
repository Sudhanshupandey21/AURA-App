"""Stress testing engine."""

import asyncio
import logging
import time
from typing import Dict, List, Optional

from aura_risk_engine.testing_framework.utils import TestResult, TestScenario, SimulatedIncident

logger = logging.getLogger(__name__)


class StressTester:
    """Performs stress testing on the AURA X system."""

    def __init__(self) -> None:
        self._results: List[TestResult] = []

    async def run_incident_burst_test(
        self,
        scenario: TestScenario,
        burst_size: int = 10,
        burst_duration_seconds: float = 1.0,
        callback: Optional[callable] = None,
    ) -> TestResult:
        """Test system response to rapid incident bursts."""
        start_time = time.time()
        incidents_created = 0

        try:
            # Generate burst of incidents
            for i in range(burst_size):
                incident = SimulatedIncident(
                    incident_id=f"stress_burst_{i}",
                    severity=0.8 + (i % 3) * 0.05,  # Vary severity
                    location_lat=37.7749 + (i % 5) * 0.001,
                    location_lng=-122.4194 + (i % 5) * 0.001,
                    timestamp=time.time(),
                    description=f"Stress test incident {i}",
                )

                if callback:
                    await callback(incident)

                incidents_created += 1
                if i < burst_size - 1:  # Don't sleep after last incident
                    await asyncio.sleep(burst_duration_seconds / burst_size)

            end_time = time.time()
            total_time = end_time - start_time
            avg_time_per_incident = total_time / burst_size

            # Validate performance
            max_allowed_time = burst_duration_seconds * 1.5  # Allow 50% overhead
            performance_valid = total_time <= max_allowed_time

            result = TestResult(
                test_name=f"incident_burst_stress_{scenario.name}",
                passed=performance_valid,
                message=f"Incident burst test {'passed' if performance_valid else 'failed'}",
                expected=f"Process {burst_size} incidents in <= {max_allowed_time:.2f}s",
                actual=f"Processed {incidents_created} in {total_time:.2f}s ({avg_time_per_incident:.3f}s per incident)",
            )

        except Exception as e:
            result = TestResult(
                test_name=f"incident_burst_stress_{scenario.name}",
                passed=False,
                message=f"Incident burst test failed with exception: {e}",
                expected="No exceptions during burst processing",
                actual=f"Exception: {e}",
            )

        self._results.append(result)
        return result

    async def run_high_frequency_update_test(
        self,
        scenario: TestScenario,
        update_count: int = 100,
        target_frequency_hz: float = 50.0,
        callback: Optional[callable] = None,
    ) -> TestResult:
        """Test system response to high-frequency updates."""
        start_time = time.time()
        updates_processed = 0
        interval = 1.0 / target_frequency_hz

        try:
            for i in range(update_count):
                update_data = {
                    "timestamp": time.time(),
                    "update_id": i,
                    "crowd_density": scenario.crowd_density + (i % 10) * 0.01,
                    "light_intensity": scenario.light_intensity + (i % 20) * 0.005,
                    "incident_severity": scenario.incident_severity,
                }

                if callback:
                    await callback(update_data)

                updates_processed += 1
                if i < update_count - 1:
                    await asyncio.sleep(interval)

            end_time = time.time()
            total_time = end_time - start_time
            actual_frequency = update_count / total_time

            # Validate frequency maintenance
            frequency_valid = actual_frequency >= target_frequency_hz * 0.8  # Allow 20% degradation

            result = TestResult(
                test_name=f"high_frequency_stress_{scenario.name}",
                passed=frequency_valid,
                message=f"High frequency test {'passed' if frequency_valid else 'failed'}",
                expected=f"Maintain >= {target_frequency_hz * 0.8:.1f} Hz",
                actual=f"Achieved {actual_frequency:.1f} Hz over {total_time:.2f}s",
            )

        except Exception as e:
            result = TestResult(
                test_name=f"high_frequency_stress_{scenario.name}",
                passed=False,
                message=f"High frequency test failed with exception: {e}",
                expected="No exceptions during high-frequency updates",
                actual=f"Exception: {e}",
            )

        self._results.append(result)
        return result

    async def run_concurrent_events_test(
        self,
        scenario: TestScenario,
        concurrent_count: int = 5,
        duration_seconds: int = 10,
        callback: Optional[callable] = None,
    ) -> TestResult:
        """Test system response to multiple concurrent events."""
        start_time = time.time()
        tasks = []

        async def generate_events(task_id: int):
            events_generated = 0
            for i in range(duration_seconds * 2):  # 2 events per second per task
                event = {
                    "task_id": task_id,
                    "event_id": f"concurrent_{task_id}_{i}",
                    "timestamp": time.time(),
                    "type": "concurrent_test",
                    "data": f"Test data {i}",
                }

                if callback:
                    await callback(event)

                events_generated += 1
                await asyncio.sleep(0.5)  # 2 Hz per task

            return events_generated

        try:
            # Create concurrent tasks
            for task_id in range(concurrent_count):
                task = asyncio.create_task(generate_events(task_id))
                tasks.append(task)

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)
            total_events = sum(results)

            end_time = time.time()
            total_time = end_time - start_time

            # Validate concurrency handling
            expected_events = concurrent_count * duration_seconds * 2
            events_valid = total_events >= expected_events * 0.9  # Allow 10% loss

            result = TestResult(
                test_name=f"concurrent_events_stress_{scenario.name}",
                passed=events_valid,
                message=f"Concurrent events test {'passed' if events_valid else 'failed'}",
                expected=f"Process >= {expected_events * 0.9:.0f} events from {concurrent_count} concurrent sources",
                actual=f"Processed {total_events} events in {total_time:.2f}s",
            )

        except Exception as e:
            result = TestResult(
                test_name=f"concurrent_events_stress_{scenario.name}",
                passed=False,
                message=f"Concurrent events test failed with exception: {e}",
                expected="No exceptions during concurrent processing",
                actual=f"Exception: {e}",
            )

        self._results.append(result)
        return result

    def get_test_results(self) -> List[TestResult]:
        """Get all stress test results."""
        return self._results.copy()

    def clear_results(self) -> None:
        """Clear test results."""
        self._results.clear()


_default_tester = StressTester()


async def run_incident_burst_test(
    scenario: TestScenario,
    burst_size: int = 10,
    burst_duration_seconds: float = 1.0,
    callback: Optional[callable] = None,
) -> TestResult:
    """Run incident burst stress test."""
    return await _default_tester.run_incident_burst_test(
        scenario, burst_size, burst_duration_seconds, callback
    )


async def run_high_frequency_update_test(
    scenario: TestScenario,
    update_count: int = 100,
    target_frequency_hz: float = 50.0,
    callback: Optional[callable] = None,
) -> TestResult:
    """Run high frequency update stress test."""
    return await _default_tester.run_high_frequency_update_test(
        scenario, update_count, target_frequency_hz, callback
    )


async def run_concurrent_events_test(
    scenario: TestScenario,
    concurrent_count: int = 5,
    duration_seconds: int = 10,
    callback: Optional[callable] = None,
) -> TestResult:
    """Run concurrent events stress test."""
    return await _default_tester.run_concurrent_events_test(
        scenario, concurrent_count, duration_seconds, callback
    )
