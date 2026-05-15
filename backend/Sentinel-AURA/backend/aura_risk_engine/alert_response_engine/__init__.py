"""Alert & Response Engine for AURA X.

This package provides real-time alert detection, severity classification,
response decision-making, dynamic rerouting, SOS escalation, safe anchor guidance,
continuous monitoring, and explainable messaging for urban safety systems.
"""

from aura_risk_engine.alert_response_engine.alert_detector import AlertDetector, detect_alert_condition
from aura_risk_engine.alert_response_engine.severity_classifier import SeverityClassifier, classify_alert_level
from aura_risk_engine.alert_response_engine.response_engine import ResponseDecisionEngine, decide_response_action
from aura_risk_engine.alert_response_engine.rerouting import ReroutingEngine, trigger_rerouting
from aura_risk_engine.alert_response_engine.sos_engine import SOSEngine, handle_sos, is_sos_active, get_sos_status
from aura_risk_engine.alert_response_engine.safe_anchor import (
    SafeAnchorGuidanceEngine,
    find_nearest_safe_anchor,
    find_all_safe_anchors_nearby,
)
from aura_risk_engine.alert_response_engine.monitoring import ContinuousMonitoringEngine, continuous_monitoring_loop
from aura_risk_engine.alert_response_engine.explainability import (
    AlertMessageGenerator,
    generate_alert_message,
    generate_response_message,
    generate_contextual_alert,
    generate_rerouting_explanation,
)
from aura_risk_engine.alert_response_engine.utils import (
    AlertLevel,
    ResponseAction,
    AnchorType,
    RiskSnapshot,
    AlertEvent,
    SafeAnchor,
    SOSEvent,
)

__all__ = [
    "AlertDetector",
    "detect_alert_condition",
    "SeverityClassifier",
    "classify_alert_level",
    "ResponseDecisionEngine",
    "decide_response_action",
    "ReroutingEngine",
    "trigger_rerouting",
    "SOSEngine",
    "handle_sos",
    "is_sos_active",
    "get_sos_status",
    "SafeAnchorGuidanceEngine",
    "find_nearest_safe_anchor",
    "find_all_safe_anchors_nearby",
    "ContinuousMonitoringEngine",
    "continuous_monitoring_loop",
    "AlertMessageGenerator",
    "generate_alert_message",
    "generate_response_message",
    "generate_contextual_alert",
    "generate_rerouting_explanation",
    "AlertLevel",
    "ResponseAction",
    "AnchorType",
    "RiskSnapshot",
    "AlertEvent",
    "SafeAnchor",
    "SOSEvent",
]
