"""Testing & Simulation Framework for AURA X System Validation."""

from aura_risk_engine.testing_framework.utils import (
    AreaType,
    IncidentSeverity,
    RiskLevel,
    SystemStatus,
    TestScenario,
    SimulatedIncident,
    TestResult,
    TestReport,
    classify_time_period,
    normalize_score,
)

from aura_risk_engine.testing_framework.scenario_generator import (
    ScenarioGenerator,
    get_predefined_scenarios,
    generate_custom_scenario,
)

from aura_risk_engine.testing_framework.environment_simulator import (
    EnvironmentSimulator,
    simulate_environment,
)

from aura_risk_engine.testing_framework.incident_simulator import (
    IncidentSimulator,
    simulate_incidents,
    generate_incident_spike,
)

from aura_risk_engine.testing_framework.realtime_simulator import (
    RealtimeSimulator,
    simulate_realtime_updates,
)

from aura_risk_engine.testing_framework.risk_validator import (
    RiskValidator,
    validate_risk_calculation,
    validate_trend_calculation,
)

from aura_risk_engine.testing_framework.route_validator import (
    RouteValidator,
    validate_route_risk_calculation,
    validate_safest_route_selection,
    validate_rerouting_decision,
)

from aura_risk_engine.testing_framework.alert_validator import (
    AlertValidator,
    validate_alert_triggering,
    validate_severity_classification,
    validate_response_action,
)

from aura_risk_engine.testing_framework.stress_tester import (
    StressTester,
    run_incident_burst_test,
    run_high_frequency_update_test,
    run_concurrent_events_test,
)

from aura_risk_engine.testing_framework.report_generator import (
    ReportGenerator,
    generate_test_report,
    generate_scenario_report,
    generate_validation_type_report,
)

from aura_risk_engine.testing_framework.run_all_tests import (
    TestOrchestrator,
    main,
)

__version__ = "1.0.0"
__all__ = [
    # Data models and enums
    "AreaType",
    "IncidentSeverity",
    "RiskLevel",
    "SystemStatus",
    "TestScenario",
    "SimulatedIncident",
    "TestResult",
    "TestReport",
    "classify_time_period",
    "normalize_score",

    # Scenario generation
    "ScenarioGenerator",
    "get_predefined_scenarios",
    "generate_custom_scenario",

    # Environment simulation
    "EnvironmentSimulator",
    "simulate_environment",

    # Incident simulation
    "IncidentSimulator",
    "simulate_incidents",
    "generate_incident_spike",

    # Realtime simulation
    "RealtimeSimulator",
    "simulate_realtime_updates",

    # Risk validation
    "RiskValidator",
    "validate_risk_calculation",
    "validate_trend_calculation",

    # Route validation
    "RouteValidator",
    "validate_route_risk_calculation",
    "validate_safest_route_selection",
    "validate_rerouting_decision",

    # Alert validation
    "AlertValidator",
    "validate_alert_triggering",
    "validate_severity_classification",
    "validate_response_action",

    # Stress testing
    "StressTester",
    "run_incident_burst_test",
    "run_high_frequency_update_test",
    "run_concurrent_events_test",

    # Report generation
    "ReportGenerator",
    "generate_test_report",
    "generate_scenario_report",
    "generate_validation_type_report",

    # Test orchestration
    "TestOrchestrator",
    "main",
]
