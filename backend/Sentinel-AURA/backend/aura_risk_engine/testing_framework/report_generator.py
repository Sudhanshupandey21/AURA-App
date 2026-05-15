"""Test report generation engine."""

import logging
import time
from statistics import mean, median
from typing import List

from aura_risk_engine.testing_framework.utils import TestReport, TestResult, SystemStatus

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates comprehensive test reports."""

    def __init__(self) -> None:
        pass

    def generate_test_report(self, results: List[TestResult]) -> TestReport:
        """Generate a comprehensive test report from results."""
        if not results:
            return TestReport(
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                pass_rate=0.0,
                system_status=SystemStatus.CRITICAL,
                average_response_time=0.0,
                median_response_time=0.0,
                min_response_time=0.0,
                max_response_time=0.0,
                test_start_time=time.time(),
                test_end_time=time.time(),
                detailed_results=[],
                summary="No tests executed",
            )

        # Calculate basic statistics
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.passed)
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100.0

        # Determine system status
        if pass_rate >= 95.0:
            system_status = SystemStatus.STABLE
        elif pass_rate >= 80.0:
            system_status = SystemStatus.DEGRADED
        else:
            system_status = SystemStatus.CRITICAL

        # Calculate response times (if available in results)
        response_times = []
        for result in results:
            # Try to extract timing from message or actual field
            if "time" in result.actual.lower() or "hz" in result.actual.lower():
                try:
                    # Simple extraction - look for numbers that might be times
                    import re
                    time_matches = re.findall(r"(\d+\.?\d*)", result.actual)
                    if time_matches:
                        response_times.extend(float(t) for t in time_matches if float(t) > 0)
                except:
                    pass

        if response_times:
            average_response_time = mean(response_times)
            median_response_time = median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            average_response_time = 0.0
            median_response_time = 0.0
            min_response_time = 0.0
            max_response_time = 0.0

        # Generate summary
        summary_parts = []
        if system_status == SystemStatus.STABLE:
            summary_parts.append("System operating normally with high reliability.")
        elif system_status == SystemStatus.DEGRADED:
            summary_parts.append("System experiencing some issues but remains operational.")
        else:
            summary_parts.append("System experiencing critical failures requiring immediate attention.")

        summary_parts.append(f"Pass rate: {pass_rate:.1f}% ({passed_tests}/{total_tests})")

        if response_times:
            summary_parts.append(f"Average response time: {average_response_time:.3f}s")

        # Add failure highlights
        failed_results = [r for r in results if not r.passed]
        if failed_results:
            failure_types = {}
            for result in failed_results:
                test_type = result.test_name.split('_')[0] if '_' in result.test_name else 'unknown'
                failure_types[test_type] = failure_types.get(test_type, 0) + 1

            failure_summary = ", ".join(f"{k}: {v}" for k, v in failure_types.items())
            summary_parts.append(f"Failures by type: {failure_summary}")

        summary = " ".join(summary_parts)

        report = TestReport(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            pass_rate=pass_rate,
            system_status=system_status,
            average_response_time=average_response_time,
            median_response_time=median_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            test_start_time=min(r.timestamp for r in results) if results else time.time(),
            test_end_time=max(r.timestamp for r in results) if results else time.time(),
            detailed_results=results,
            summary=summary,
        )

        logger.info(f"Generated test report: {pass_rate:.1f}% pass rate, {system_status.value} status")
        return report

    def generate_scenario_report(self, scenario_name: str, results: List[TestResult]) -> TestReport:
        """Generate a report for a specific test scenario."""
        scenario_results = [r for r in results if scenario_name.lower() in r.test_name.lower()]
        return self.generate_test_report(scenario_results)

    def generate_validation_type_report(self, validation_type: str, results: List[TestResult]) -> TestReport:
        """Generate a report for a specific validation type (risk, route, alert, etc.)."""
        type_results = [r for r in results if validation_type.lower() in r.test_name.lower()]
        return self.generate_test_report(type_results)


_default_generator = ReportGenerator()


def generate_test_report(results: List[TestResult]) -> TestReport:
    """Generate a comprehensive test report."""
    return _default_generator.generate_test_report(results)


def generate_scenario_report(scenario_name: str, results: List[TestResult]) -> TestReport:
    """Generate a report for a specific scenario."""
    return _default_generator.generate_scenario_report(scenario_name, results)


def generate_validation_type_report(validation_type: str, results: List[TestResult]) -> TestReport:
    """Generate a report for a specific validation type."""
    return _default_generator.generate_validation_type_report(validation_type, results)
