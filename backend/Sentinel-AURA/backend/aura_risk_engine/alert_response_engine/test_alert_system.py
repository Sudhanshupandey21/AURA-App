"""Unit tests for the Alert & Response Engine."""

import asyncio
import unittest
from datetime import datetime

from aura_risk_engine.alert_response_engine import (
    AlertDetector,
    AlertLevel,
    AnchorType,
    ContinuousMonitoringEngine,
    ResponseAction,
    ResponseDecisionEngine,
    ReroutingEngine,
    RiskSnapshot,
    SafeAnchor,
    SafeAnchorGuidanceEngine,
    SeverityClassifier,
    SOSEngine,
    classify_alert_level,
    continuous_monitoring_loop,
    detect_alert_condition,
    decide_response_action,
    find_nearest_safe_anchor,
    generate_alert_message,
    generate_contextual_alert,
    generate_response_message,
    generate_rerouting_explanation,
    handle_sos,
    is_sos_active,
    trigger_rerouting,
)


class TestAlertDetection(unittest.TestCase):
    def setUp(self):
        self.detector = AlertDetector()

    def test_detects_danger_threshold(self):
        alert = self.detector.detect_alert_condition(current_risk=80, risk_trend="stable")
        self.assertTrue(alert)

    def test_detects_incident_spike(self):
        alert = self.detector.detect_alert_condition(
            current_risk=30, risk_trend="stable", active_incidents=3
        )
        self.assertTrue(alert)

    def test_no_alert_on_low_stable_risk(self):
        alert = self.detector.detect_alert_condition(
            current_risk=25, risk_trend="stable", active_incidents=0
        )
        self.assertFalse(alert)

    def test_detects_increasing_trend(self):
        self.detector._previous_risk = 30.0
        alert = self.detector.detect_alert_condition(
            current_risk=50, risk_trend="increasing", active_incidents=0
        )
        self.assertTrue(alert)


class TestSeverityClassification(unittest.TestCase):
    def setUp(self):
        self.classifier = SeverityClassifier()

    def test_classify_low_risk(self):
        level = self.classifier.classify_alert_level(25)
        self.assertEqual(level, AlertLevel.LOW)

    def test_classify_medium_risk(self):
        level = self.classifier.classify_alert_level(55)
        self.assertEqual(level, AlertLevel.MEDIUM)

    def test_classify_high_risk(self):
        level = self.classifier.classify_alert_level(80)
        self.assertEqual(level, AlertLevel.HIGH)

    def test_classify_critical_risk(self):
        level = self.classifier.classify_alert_level(95)
        self.assertEqual(level, AlertLevel.CRITICAL)

    def test_alert_color_mapping(self):
        color = self.classifier.get_alert_color(AlertLevel.CRITICAL)
        self.assertEqual(color, "red")

    def test_alert_priority_ranking(self):
        priority_critical = self.classifier.get_alert_priority(AlertLevel.CRITICAL)
        priority_low = self.classifier.get_alert_priority(AlertLevel.LOW)
        self.assertLess(priority_critical, priority_low)


class TestResponseDecisions(unittest.TestCase):
    def setUp(self):
        self.response_engine = ResponseDecisionEngine()

    def test_sos_at_critical_level(self):
        action = self.response_engine.decide_response_action(
            risk_score=96, alert_level=AlertLevel.CRITICAL
        )
        self.assertEqual(action, ResponseAction.ACTIVATE_SOS)

    def test_emergency_at_high_level(self):
        action = self.response_engine.decide_response_action(
            risk_score=85, alert_level=AlertLevel.HIGH
        )
        self.assertEqual(action, ResponseAction.TRIGGER_EMERGENCY)

    def test_reroute_recommendation(self):
        action = self.response_engine.decide_response_action(
            risk_score=72, alert_level=AlertLevel.HIGH, risk_trend="increasing"
        )
        self.assertEqual(action, ResponseAction.RECOMMEND_REROUTE)

    def test_caution_alert(self):
        action = self.response_engine.decide_response_action(
            risk_score=50, alert_level=AlertLevel.MEDIUM
        )
        self.assertEqual(action, ResponseAction.ISSUE_CAUTION)

    def test_continue_monitoring_low_risk(self):
        action = self.response_engine.decide_response_action(
            risk_score=25, alert_level=AlertLevel.LOW
        )
        self.assertEqual(action, ResponseAction.CONTINUE_MONITORING)


class TestRerouting(unittest.TestCase):
    def setUp(self):
        self.rerouting_engine = ReroutingEngine()

    def test_reroute_at_high_risk(self):
        alternatives = [
            {"route_id": "Alt1", "risk_score": 45.0},
            {"route_id": "Alt2", "risk_score": 50.0},
        ]
        result = self.rerouting_engine.trigger_rerouting(
            current_route_risk=72, available_alternatives=alternatives
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["route_id"], "Alt1")

    def test_no_reroute_stable_low_risk(self):
        alternatives = [
            {"route_id": "Alt1", "risk_score": 65.0},
        ]
        result = self.rerouting_engine.trigger_rerouting(
            current_route_risk=30, available_alternatives=alternatives
        )
        self.assertIsNone(result)

    def test_reroute_on_incident_ahead(self):
        alternatives = [
            {"route_id": "Alt1", "risk_score": 55.0},
        ]
        result = self.rerouting_engine.trigger_rerouting(
            current_route_risk=72,
            available_alternatives=alternatives,
            incident_ahead=True,
        )
        self.assertIsNotNone(result)


class TestSOSEngine(unittest.TestCase):
    def setUp(self):
        self.sos_engine = SOSEngine()

    def test_activate_sos(self):
        sos = self.sos_engine.handle_sos_activation(
            location={"latitude": 37.7749, "longitude": -122.4194},
            reason="Test emergency",
        )
        self.assertIsNotNone(sos)
        self.assertTrue(sos.active)
        self.assertEqual(sos.reason, "Test emergency")

    def test_sos_status_while_active(self):
        self.sos_engine.handle_sos_activation(
            location={"latitude": 37.7749, "longitude": -122.4194}
        )
        self.assertTrue(self.sos_engine.is_sos_active())

    def test_deactivate_sos(self):
        self.sos_engine.handle_sos_activation(
            location={"latitude": 37.7749, "longitude": -122.4194}
        )
        deactivated = self.sos_engine.handle_sos_deactivation()
        self.assertTrue(deactivated)
        self.assertFalse(self.sos_engine.is_sos_active())

    def test_emergency_payload_generation(self):
        self.sos_engine.handle_sos_activation(
            location={"latitude": 37.7749, "longitude": -122.4194}
        )
        payload = self.sos_engine.generate_emergency_payload()
        self.assertIn("sos_id", payload)
        self.assertIn("location", payload)
        self.assertTrue(payload["location_shared"])


class TestSafeAnchorGuidance(unittest.TestCase):
    def setUp(self):
        self.guidance_engine = SafeAnchorGuidanceEngine()

        # Register test anchors
        self.guidance_engine.register_anchor(
            SafeAnchor(
                anchor_id="police-1",
                anchor_type=AnchorType.POLICE_STATION,
                name="Downtown Police",
                latitude=37.7749,
                longitude=-122.4194,
                distance_m=0.0,
            )
        )
        self.guidance_engine.register_anchor(
            SafeAnchor(
                anchor_id="hospital-1",
                anchor_type=AnchorType.HOSPITAL,
                name="General Hospital",
                latitude=37.7760,
                longitude=-122.4200,
                distance_m=0.0,
            )
        )

    def test_find_nearest_anchor(self):
        current = {"latitude": 37.7749, "longitude": -122.4194}
        anchor = self.guidance_engine.find_nearest_safe_anchor(current, max_distance_m=2000)
        self.assertIsNotNone(anchor)
        self.assertEqual(anchor.name, "Downtown Police")

    def test_no_anchor_too_far(self):
        current = {"latitude": 37.0, "longitude": -120.0}
        anchor = self.guidance_engine.find_nearest_safe_anchor(current, max_distance_m=100)
        self.assertIsNone(anchor)

    def test_find_multiple_anchors(self):
        current = {"latitude": 37.7749, "longitude": -122.4194}
        anchors = self.guidance_engine.find_all_safe_anchors_nearby(
            current, max_distance_m=2000, limit=5
        )
        self.assertGreater(len(anchors), 0)


class TestExplainability(unittest.TestCase):
    def test_alert_message_low(self):
        message = generate_alert_message(AlertLevel.LOW, 25.0)
        self.assertIn("safe", message.lower())

    def test_alert_message_critical(self):
        message = generate_alert_message(AlertLevel.CRITICAL, 95.0)
        self.assertIn("critical", message.lower())

    def test_response_message(self):
        message = generate_response_message(ResponseAction.ACTIVATE_SOS)
        self.assertIn("SOS", message)

    def test_contextual_alert_with_incidents(self):
        message = generate_contextual_alert(
            risk_score=75, risk_trend="increasing", active_incidents=2
        )
        self.assertIn("incident", message.lower())

    def test_rerouting_explanation(self):
        message = generate_rerouting_explanation(
            current_route_risk=75, new_route_risk=45, reason="incident"
        )
        self.assertIn("safer", message.lower())


class TestContinuousMonitoring(unittest.IsolatedAsyncioTestCase):
    async def test_monitoring_loop_initialization(self):
        engine = ContinuousMonitoringEngine(check_interval_seconds=0.1)
        self.assertFalse(engine.is_monitoring_active())

    async def test_monitoring_with_alert_callback(self):
        engine = ContinuousMonitoringEngine(check_interval_seconds=0.05)
        alerts_received = []

        def callback(alert):
            alerts_received.append(alert)

        engine.register_alert_callback(callback)

        def risk_provider():
            return RiskSnapshot(
                risk_score=80.0,
                risk_level="HIGH",
                trend="increasing",
                timestamp=datetime.now().timestamp(),
                active_incidents=1,
            )

        stop_event = asyncio.Event()

        async def stop_after_brief():
            await asyncio.sleep(0.2)
            stop_event.set()

        await asyncio.gather(
            engine.continuous_monitoring_loop(risk_provider, stop_event),
            stop_after_brief(),
        )

        self.assertGreater(len(alerts_received), 0)


class TestIntegration(unittest.TestCase):
    def test_full_alert_workflow_medium_risk(self):
        # Detect (using incident spike instead, as default danger threshold is 75)
        detected = detect_alert_condition(
            current_risk=55, risk_trend="stable", active_incidents=2
        )
        self.assertTrue(detected)

        # Classify
        level = classify_alert_level(55)
        self.assertEqual(level, AlertLevel.MEDIUM)

        # Decide response
        action = decide_response_action(risk_score=55, alert_level=level)
        self.assertEqual(action, ResponseAction.ISSUE_CAUTION)

        # Generate message
        message = generate_response_message(action)
        self.assertIn("Caution", message)

    def test_full_alert_workflow_high_risk_rerouting(self):
        detected = detect_alert_condition(
            current_risk=78, risk_trend="increasing", active_incidents=0
        )
        self.assertTrue(detected)

        level = classify_alert_level(78)
        self.assertEqual(level, AlertLevel.HIGH)

        action = decide_response_action(risk_score=78, alert_level=level, risk_trend="increasing")
        self.assertEqual(action, ResponseAction.RECOMMEND_REROUTE)

        alternatives = [
            {"route_id": "Alt1", "risk_score": 50.0},
        ]
        reroute = trigger_rerouting(
            current_route_risk=78, available_alternatives=alternatives
        )
        self.assertIsNotNone(reroute)
        self.assertEqual(reroute["route_id"], "Alt1")

    def test_full_alert_workflow_critical_sos(self):
        level = classify_alert_level(97)
        self.assertEqual(level, AlertLevel.CRITICAL)

        action = decide_response_action(risk_score=97, alert_level=level)
        self.assertEqual(action, ResponseAction.ACTIVATE_SOS)

        # Activate SOS (using default engine)
        sos = handle_sos(
            location={"latitude": 37.7749, "longitude": -122.4194},
            reason="Critical danger",
        )
        self.assertIsNotNone(sos)
        self.assertTrue(is_sos_active())


if __name__ == "__main__":
    unittest.main()
