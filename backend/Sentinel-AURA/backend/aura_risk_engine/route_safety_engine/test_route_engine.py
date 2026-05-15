"""Unit tests for the Route Safety Engine."""

import unittest

from aura_risk_engine.route_safety_engine import (
    RouteRiskProfile,
    analyze_route,
    choose_best_route,
    select_safest_route,
    reroute_if_needed,
    generate_route_explanation,
    process_routes,
    segment_route,
    analyze_segment_risk,
    calculate_route_risk,
)


class TestRouteSafetyEngine(unittest.TestCase):
    def setUp(self):
        self.safe_route = {
            "route_id": "SafeDay",
            "distance_km": 3.2,
            "duration_min": 10,
            "polyline": [
                [37.7749, -122.4194],
                [37.7760, -122.4186],
                [37.7771, -122.4178],
            ],
        }
        self.dark_route = {
            "route_id": "DarkRoad",
            "distance_km": 5.8,
            "duration_min": 17,
            "polyline": [
                [37.7749, -122.4194],
                [37.7756, -122.4205],
                [37.7762, -122.4214],
            ],
        }
        self.incident_route = {
            "route_id": "IncidentPath",
            "distance_km": 3.8,
            "duration_min": 11,
            "polyline": [
                [37.7749, -122.4194],
                [37.7759, -122.4208],
                [37.7768, -122.4220],
            ],
        }

    def test_process_routes_validates_input(self):
        with self.assertRaises(ValueError):
            process_routes([])
        with self.assertRaises(ValueError):
            process_routes([{"distance_km": 1.0, "duration_min": 5, "polyline": []}])

    def test_segment_route_creates_analyzable_segments(self):
        segments = segment_route(self.safe_route, segment_length_m=150.0)
        self.assertGreaterEqual(len(segments), 2)
        self.assertEqual(segments[0]["route_id"], "SafeDay")

    def test_analyze_segment_risk_safe_daytime(self):
        score = analyze_segment_risk(
            time_risk=0.1,
            crowd_risk=0.1,
            light_risk=0.1,
            incident_risk=0.0,
            area_risk=0.1,
        )
        self.assertLess(score, 40)

    def test_analyze_segment_risk_incident_heavy(self):
        score = analyze_segment_risk(
            time_risk=0.9,
            crowd_risk=0.5,
            light_risk=0.9,
            incident_risk=0.95,
            area_risk=0.7,
        )
        self.assertGreaterEqual(score, 70)

    def test_calculate_route_risk_handles_spikes(self):
        route_score = calculate_route_risk([18, 22, 88, 32, 45])
        self.assertGreaterEqual(route_score, 50)

    def test_select_safest_route_prefers_lowest_risk(self):
        summaries = [
            {"route_id": "A", "route_risk": 42, "distance_km": 5.0, "duration_min": 13},
            {"route_id": "B", "route_risk": 36, "distance_km": 5.4, "duration_min": 14},
        ]
        chosen = select_safest_route(summaries)
        self.assertEqual(chosen["recommended_route"], "B")
        self.assertEqual(chosen["risk_score"], 36.0)

    def test_choose_best_route_prefers_safe_daytime(self):
        risk_profile = RouteRiskProfile(time_risk=0.1, crowd_risk=0.1, light_risk=0.05, incident_risk=0.0, area_risk=0.1)
        recommendation = choose_best_route([self.safe_route, self.dark_route], segment_length_m=100.0, risk_profile=risk_profile)
        self.assertEqual(recommendation["recommended_route"], "SafeDay")
        self.assertLess(recommendation["risk_score"], 50)

    def test_reroute_if_needed_triggers_on_high_risk(self):
        active = {"route_id": "Active", "route_risk": 72.0, "distance_km": 4.0, "duration_min": 10}
        alt_one = {"route_id": "Alt1", "route_risk": 48.0, "distance_km": 4.4, "duration_min": 11}
        alt_two = {"route_id": "Alt2", "route_risk": 50.0, "distance_km": 4.1, "duration_min": 11}

        result = reroute_if_needed(active, [alt_one, alt_two], incident_new=True)
        self.assertTrue(result["rerouted"])
        self.assertEqual(result["recommended_route"], "Alt1")
        self.assertIn("Rerouted due to elevated route risk", result["explanation"])

    def test_route_with_sudden_risk_spike_reports_high_risk(self):
        summary = analyze_route(self.incident_route, segment_length_m=100.0, risk_profile=RouteRiskProfile(time_risk=0.4, crowd_risk=0.3, light_risk=0.9, incident_risk=0.8, area_risk=0.6))
        self.assertGreaterEqual(summary["route_risk"], 60)

    def test_generate_route_explanation_describes_route(self):
        explanation = generate_route_explanation({"route_id": "A", "route_risk": 35.0}, trigger="hold")
        self.assertIn("Route A selected", explanation)
        self.assertIn("safer passage", explanation)

    def test_end_to_end_multiple_route_comparison(self):
        safe_profile = RouteRiskProfile(time_risk=0.15, crowd_risk=0.15, light_risk=0.15, incident_risk=0.0, area_risk=0.12)
        summaries = [
            analyze_route(self.safe_route, segment_length_m=120.0, risk_profile=safe_profile),
            analyze_route(self.dark_route, segment_length_m=120.0, risk_profile=RouteRiskProfile(time_risk=0.6, crowd_risk=0.5, light_risk=0.9, incident_risk=0.2, area_risk=0.4)),
            analyze_route(self.incident_route, segment_length_m=120.0, risk_profile=RouteRiskProfile(time_risk=0.4, crowd_risk=0.6, light_risk=0.8, incident_risk=0.9, area_risk=0.7)),
        ]
        choice = select_safest_route(summaries)
        self.assertEqual(choice["recommended_route"], "SafeDay")


if __name__ == "__main__":
    unittest.main()
