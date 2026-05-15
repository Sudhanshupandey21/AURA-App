"""
Comprehensive Test Suite for Incident Intelligence Module

Tests:
- Fresh high severity incidents
- Old incident decay
- Multiple nearby incidents
- Distant incidents
- Overlapping incidents
- Invalid data handling
- Real-time aggregation scenarios
- Geographic impact calculations
- Risk scoring accuracy
"""

import unittest
import time
from datetime import datetime, timezone, timedelta
import logging

from incident_processor import IncidentProcessor
from severity_engine import SeverityEngine
from decay_engine import TimeDecayEngine
from geo_engine import GeoEngine
from aura_risk_engine.risk_engine import RiskEngine
from aggregation import IncidentAggregator
from explain import ExplainabilityEngine
from utils import get_current_timestamp

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestIncidentProcessor(unittest.TestCase):
    """Test incident input processing and validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = IncidentProcessor()
        self.current_time = get_current_timestamp()
    
    def test_valid_incident_processing(self):
        """Test processing of valid incident."""
        incident = {
            "type": "harassment",
            "severity": 0.8,
            "timestamp": self.current_time - 300,  # 5 minutes ago
            "latitude": 21.25,
            "longitude": 81.62
        }
        
        result = self.processor.process_incident(incident)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.incident_type, "harassment")
        self.assertEqual(result.severity, 0.8)
        self.assertEqual(len(result.validation_errors), 0)
    
    def test_invalid_severity(self):
        """Test rejection of invalid severity."""
        incident = {
            "type": "harassment",
            "severity": 1.5,  # Out of range
            "timestamp": self.current_time,
            "latitude": 21.25,
            "longitude": 81.62
        }
        
        result = self.processor.process_incident(incident)
        
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Severity" in e for e in result.validation_errors))
    
    def test_invalid_coordinates(self):
        """Test rejection of invalid coordinates."""
        incident = {
            "type": "harassment",
            "severity": 0.8,
            "timestamp": self.current_time,
            "latitude": 91.0,  # Out of range
            "longitude": 81.62
        }
        
        result = self.processor.process_incident(incident)
        
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Coordinates" in e for e in result.validation_errors))
    
    def test_missing_required_fields(self):
        """Test rejection of missing required fields."""
        incident = {
            "type": "harassment",
            # Missing severity
            "timestamp": self.current_time,
            "latitude": 21.25,
            "longitude": 81.62
        }
        
        result = self.processor.process_incident(incident)
        
        self.assertFalse(result.is_valid)
        self.assertTrue(any("severity" in e.lower() for e in result.validation_errors))
    
    def test_custom_severity_override(self):
        """Test custom severity override."""
        incident = {
            "type": "harassment",
            "severity": 0.6,
            "timestamp": self.current_time,
            "latitude": 21.25,
            "longitude": 81.62,
            "custom_severity_override": 0.9
        }
        
        result = self.processor.process_incident(incident)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.custom_severity_override, 0.9)


class TestSeverityEngine(unittest.TestCase):
    """Test severity modeling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SeverityEngine()
    
    def test_get_severity_scores(self):
        """Test severity scores for different incident types."""
        test_cases = [
            ("suspicious_activity", 0.3),
            ("harassment", 0.6),
            ("theft", 0.7),
            ("assault", 0.85),
            ("violence", 1.0),
        ]
        
        for incident_type, expected_severity in test_cases:
            severity = self.engine.get_severity_score(incident_type)
            self.assertEqual(severity, expected_severity)
    
    def test_custom_override(self):
        """Test custom severity override."""
        severity = self.engine.get_severity_score("harassment", custom_override=0.95)
        self.assertEqual(severity, 0.95)
    
    def test_classify_severity(self):
        """Test severity classification."""
        test_cases = [
            (0.1, "Low"),
            (0.4, "Medium"),
            (0.7, "High"),
            (0.9, "Critical"),
        ]
        
        for severity, expected_class in test_cases:
            classification = self.engine.classify_severity(severity)
            self.assertEqual(classification, expected_class)
    
    def test_aggregate_severities(self):
        """Test severity aggregation."""
        severities = [0.5, 0.7, 0.6]
        
        # Test maximum
        max_severity = self.engine.aggregate_severities(severities, "maximum")
        self.assertEqual(max_severity, 0.7)
        
        # Test average
        avg_severity = self.engine.aggregate_severities(severities, "average")
        self.assertAlmostEqual(avg_severity, 0.6, places=5)


class TestTimeDecayEngine(unittest.TestCase):
    """Test time decay modeling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = TimeDecayEngine()
        self.current_time = get_current_timestamp()
    
    def test_fresh_incident(self):
        """Test decay for fresh incident."""
        # Just occurred
        decay = self.engine.decay_incident(self.current_time, self.current_time)
        self.assertAlmostEqual(decay, 1.0, places=2)
    
    def test_one_hour_old(self):
        """Test decay for 1 hour old incident."""
        one_hour_ago = self.current_time - 3600
        decay = self.engine.decay_incident(one_hour_ago, self.current_time)
        
        # Should be roughly 37% (e^(-1/60 * 60) = e^-1)
        self.assertGreater(decay, 0.3)
        self.assertLess(decay, 0.4)
    
    def test_three_hours_old(self):
        """Test decay for 3 hours old incident."""
        three_hours_ago = self.current_time - 3 * 3600
        decay = self.engine.decay_incident(three_hours_ago, self.current_time)
        
        # Should be very low
        self.assertLess(decay, 0.1)
    
    def test_time_to_decay(self):
        """Test inverse decay calculation."""
        # Time to reach 50% decay (half-life)
        time_to_half = self.engine.time_to_decay(0.5)
        self.assertAlmostEqual(time_to_half, 60, places=0)


class TestGeoEngine(unittest.TestCase):
    """Test geographic impact calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GeoEngine()
    
    def test_haversine_distance(self):
        """Test Haversine distance calculation."""
        # Two nearby points in Mumbai
        lat1, lon1 = 19.0760, 72.8777  # Colaba
        lat2, lon2 = 19.0761, 72.8778  # Very close
        
        distance = GeoEngine.haversine_distance(lat1, lon1, lat2, lon2)
        
        # Should be roughly 100-200 meters
        self.assertGreater(distance, 100)
        self.assertLess(distance, 300)
    
    def test_geo_impact_very_close(self):
        """Test geographic impact for very close location."""
        incident_lat, incident_lon = 21.25, 81.62
        # 50m away (approximate)
        target_lat, target_lon = 21.2505, 81.6205
        
        impact = self.engine.calculate_geo_impact(
            incident_lat, incident_lon,
            target_lat, target_lon,
            decay_model="threshold"
        )
        
        # Should be high impact (close)
        self.assertGreater(impact, 0.6)
    
    def test_geo_impact_far(self):
        """Test geographic impact for far location."""
        incident_lat, incident_lon = 21.25, 81.62
        # About 50km away
        target_lat, target_lon = 21.25, 82.62
        
        impact = self.engine.calculate_geo_impact(
            incident_lat, incident_lon,
            target_lat, target_lon,
            decay_model="threshold"
        )
        
        # Should be low/negligible impact
        self.assertLess(impact, 0.1)
    
    def test_classify_geo_relevance(self):
        """Test geographic relevance classification."""
        incident_lat, incident_lon = 21.25, 81.62
        target_lat, target_lon = 21.2501, 81.6201
        
        relevance = self.engine.classify_geo_relevance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        
        self.assertEqual(relevance, "Immediate")


class TestRiskEngine(unittest.TestCase):
    """Test integrated risk calculation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = RiskEngine()
        self.current_time = get_current_timestamp()
    
    def test_fresh_high_severity_nearby(self):
        """Test risk for fresh, high severity incident nearby."""
        result = self.engine.calculate_incident_risk(
            incident_type="violence",
            timestamp=self.current_time - 60,  # 1 minute ago
            incident_lat=21.25,
            incident_lon=81.62,
            target_lat=21.2501,
            target_lon=81.6201,
            current_time=self.current_time,
            include_components=True
        )
        
        # Should have high risk
        self.assertGreater(result["risk"], 0.7)
        self.assertAlmostEqual(result["severity"], 1.0, places=1)
        self.assertGreater(result["decay"], 0.95)
    
    def test_old_low_severity_far(self):
        """Test risk for old, low severity incident far away."""
        result = self.engine.calculate_incident_risk(
            incident_type="suspicious_activity",
            timestamp=self.current_time - 14400,  # 4 hours ago
            incident_lat=21.25,
            incident_lon=81.62,
            target_lat=21.35,  # ~11km away
            target_lon=81.72,
            current_time=self.current_time,
            include_components=True
        )
        
        # Should have low risk
        self.assertLess(result["risk"], 0.2)
        self.assertAlmostEqual(result["severity"], 0.3, places=1)
        self.assertLess(result["decay"], 0.05)
    
    def test_aggregate_multiple_risks(self):
        """Test aggregation of multiple risks."""
        risks = [0.3, 0.5, 0.7]
        
        max_risk = self.engine.aggregate_incident_risks(risks, "maximum")
        self.assertEqual(max_risk, 0.7)
        
        avg_risk = self.engine.aggregate_incident_risks(risks, "average")
        self.assertAlmostEqual(avg_risk, 0.5, places=5)
    
    def test_classify_risk_level(self):
        """Test risk level classification."""
        test_cases = [
            (0.1, "Minimal"),
            (0.3, "Low"),
            (0.5, "Moderate"),
            (0.7, "High"),
            (0.9, "Critical"),
        ]
        
        for risk, expected_class in test_cases:
            classification = self.engine.classify_risk_level(risk)
            self.assertEqual(classification, expected_class)


class TestIncidentAggregator(unittest.TestCase):
    """Test real-time incident aggregation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aggregator = IncidentAggregator()
        self.current_time = get_current_timestamp()
    
    def test_add_and_aggregate_single_incident(self):
        """Test adding and aggregating a single incident."""
        incident = {
            "type": "assault",
            "timestamp": self.current_time - 300,
            "latitude": 21.25,
            "longitude": 81.62,
        }
        
        incident_id = self.aggregator.add_incident(incident)
        
        result = self.aggregator.aggregate_incidents(
            21.25, 81.62,
            self.current_time
        )
        
        self.assertEqual(result["active_incidents"], 1)
        self.assertGreater(result["aggregated_risk"], 0.5)
        self.assertEqual(result["dominant_incident_type"], "assault")
    
    def test_multiple_nearby_incidents(self):
        """Test aggregating multiple nearby incidents."""
        incidents = [
            {
                "type": "harassment",
                "timestamp": self.current_time - 300,
                "latitude": 21.25,
                "longitude": 81.62,
            },
            {
                "type": "assault",
                "timestamp": self.current_time - 600,
                "latitude": 21.2501,
                "longitude": 81.6201,
            },
            {
                "type": "theft",
                "timestamp": self.current_time - 900,
                "latitude": 21.2502,
                "longitude": 81.6202,
            },
        ]
        
        for incident in incidents:
            self.aggregator.add_incident(incident)
        
        result = self.aggregator.aggregate_incidents(
            21.25, 81.62,
            self.current_time
        )
        
        self.assertEqual(result["active_incidents"], 3)
        self.assertEqual(result["nearby_incidents_count"], 3)
        self.assertGreater(result["aggregated_risk"], 0.5)
    
    def test_cleanup_stale_incidents(self):
        """Test cleanup of old incidents."""
        old_incident = {
            "type": "suspicious_activity",
            "timestamp": self.current_time - 36000,  # 10 hours ago
            "latitude": 21.25,
            "longitude": 81.62,
        }
        
        self.aggregator.add_incident(old_incident)
        initial_count = len(self.aggregator.active_incidents)
        self.assertEqual(initial_count, 1)
        
        # Clean up (default max age is 480 minutes = 8 hours)
        removed = self.aggregator.cleanup_stale_incidents(self.current_time)
        
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.aggregator.active_incidents), 0)


class TestExplainabilityEngine(unittest.TestCase):
    """Test explainability and reasoning."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = ExplainabilityEngine()
        self.current_time = get_current_timestamp()
    
    def test_explain_incident(self):
        """Test incident explanation generation."""
        explanation = self.engine.explain_incident(
            incident_type="harassment",
            timestamp=self.current_time - 300,
            latitude=21.25,
            longitude=81.62,
            severity=0.6,
            current_time=self.current_time
        )
        
        self.assertIn("harassment", explanation.lower())
        self.assertIn("medium", explanation.lower())
        self.assertTrue(len(explanation) > 50)
    
    def test_explain_risk_components(self):
        """Test risk component explanation."""
        explanations = self.engine.explain_risk_components(
            severity=0.85,
            decay=0.6,
            geo_impact=0.7,
            integrated_risk=0.357
        )
        
        self.assertIn("severity", explanations)
        self.assertIn("decay", explanations)
        self.assertIn("geo_impact", explanations)
        self.assertIn("integrated_risk", explanations)
        
        # Check content
        self.assertIn("Critical", explanations["severity"])
        self.assertIn("85%", explanations["severity"])
    
    def test_explain_aggregation(self):
        """Test aggregation explanation."""
        explanation = self.engine.explain_aggregation(
            active_incidents=3,
            nearby_incidents=2,
            aggregated_risk=0.75,
            dominant_incident_type="assault",
            incident_distribution={"assault": 2, "harassment": 1}
        )
        
        self.assertIn("3 active", explanation)
        self.assertIn("assault", explanation)
        self.assertIn("high", explanation.lower())


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.current_time = get_current_timestamp()
    
    def test_full_incident_workflow(self):
        """Test complete incident processing workflow."""
        # 1. Process incident
        processor = IncidentProcessor()
        raw_incident = {
            "type": "assault",
            "severity": 0.85,
            "timestamp": self.current_time - 600,
            "latitude": 21.25,
            "longitude": 81.62,
        }
        
        processed = processor.process_incident(raw_incident)
        self.assertTrue(processed.is_valid)
        
        # 2. Calculate risk
        risk_engine = RiskEngine()
        risk_result = risk_engine.calculate_incident_risk(
            incident_type=processed.incident_type,
            timestamp=processed.timestamp,
            incident_lat=processed.latitude,
            incident_lon=processed.longitude,
            target_lat=21.26,
            target_lon=81.63,
            include_components=True,
            current_time=self.current_time
        )
        
        self.assertGreater(risk_result["risk"], 0.0)
        self.assertLess(risk_result["risk"], 1.0)
        
        # 3. Generate explanation
        explain_engine = ExplainabilityEngine()
        explanation = explain_engine.explain_incident(
            processed.incident_type,
            processed.timestamp,
            processed.latitude,
            processed.longitude,
            processed.severity,
            self.current_time
        )
        
        self.assertTrue(len(explanation) > 0)
        self.assertIn("assault", explanation.lower())
    
    def test_real_time_aggregation_scenario(self):
        """Test realistic real-time scenario."""
        # Simulate incoming incident stream
        aggregator = IncidentAggregator()
        
        # Incident 1: Recent assault nearby
        aggregator.add_incident({
            "type": "assault",
            "timestamp": self.current_time - 300,
            "latitude": 21.25,
            "longitude": 81.62,
        })
        
        # Incident 2: Recent harassment nearby
        aggregator.add_incident({
            "type": "harassment",
            "timestamp": self.current_time - 450,
            "latitude": 21.2503,
            "longitude": 81.6203,
        })
        
        # Incident 3: Old theft far away
        aggregator.add_incident({
            "type": "theft",
            "timestamp": self.current_time - 14400,
            "latitude": 21.35,
            "longitude": 81.72,
        })
        
        # Query aggregation at location near incidents 1 and 2
        result = aggregator.aggregate_incidents(
            21.25, 81.62,
            self.current_time
        )
        
        # Should have 3 total incidents
        self.assertEqual(result["active_incidents"], 3)
        
        # Should have 2 nearby incidents
        self.assertEqual(result["nearby_incidents_count"], 2)
        
        # Risk should be significant
        self.assertGreater(result["aggregated_risk"], 0.5)
        
        # Dominant type should be assault or harassment
        self.assertIn(
            result["dominant_incident_type"],
            ["assault", "harassment"]
        )


# ==================== EXAMPLE SCENARIOS ====================

def run_example_scenarios():
    """Run example scenarios demonstrating the system."""
    
    print("\n" + "="*80)
    print("INCIDENT INTELLIGENCE SYSTEM - EXAMPLE SCENARIOS")
    print("="*80)
    
    current_time = get_current_timestamp()
    
    # Initialize engines
    processor = IncidentProcessor()
    risk_engine = RiskEngine()
    aggregator = IncidentAggregator()
    explain_engine = ExplainabilityEngine()
    
    # ==================== SCENARIO 1 ====================
    print("\n[SCENARIO 1] Fresh High Severity Incident Analysis")
    print("-" * 80)
    
    incident1 = {
        "type": "violence",
        "severity": 1.0,
        "timestamp": current_time - 60,  # 1 minute ago
        "latitude": 21.25,
        "longitude": 81.62,
        "description": "Street altercation reported"
    }
    
    processed1 = processor.process_incident(incident1)
    print(f"✓ Processed: {processed1.incident_type} (valid={processed1.is_valid})")
    
    risk1 = risk_engine.calculate_incident_risk(
        incident_type=processed1.incident_type,
        timestamp=processed1.timestamp,
        incident_lat=processed1.latitude,
        incident_lon=processed1.longitude,
        target_lat=21.26,  # 1.1km away
        target_lon=81.63,
        current_time=current_time,
        include_components=True
    )
    
    print(f"✓ Risk Score: {risk1['risk']:.3f}")
    print(f"  - Severity: {risk1['severity']:.3f} (Critical)")
    print(f"  - Time Decay: {risk1['decay']:.3f} (Fresh)")
    print(f"  - Geo Impact: {risk1['geo_impact']:.3f}")
    print(f"  - Distance: {risk1['distance_meters']/1000:.2f} km")
    
    explanation1 = explain_engine.explain_incident(
        processed1.incident_type,
        processed1.timestamp,
        processed1.latitude,
        processed1.longitude,
        processed1.severity,
        current_time
    )
    print(f"✓ Explanation: {explanation1}")
    
    # ==================== SCENARIO 2 ====================
    print("\n[SCENARIO 2] Multiple Nearby Incidents Aggregation")
    print("-" * 80)
    
    incidents_batch = [
        {
            "type": "harassment",
            "timestamp": current_time - 300,
            "latitude": 21.25,
            "longitude": 81.62,
        },
        {
            "type": "assault",
            "timestamp": current_time - 600,
            "latitude": 21.2502,
            "longitude": 81.6202,
        },
        {
            "type": "suspicious_activity",
            "timestamp": current_time - 900,
            "latitude": 21.2504,
            "longitude": 81.6204,
        },
    ]
    
    for incident in incidents_batch:
        aggregator.add_incident(incident)
    
    print(f"✓ Added {len(incidents_batch)} incidents to aggregator")
    
    agg_result = aggregator.aggregate_incidents(
        21.25, 81.62,
        current_time
    )
    
    print(f"✓ Aggregated Results:")
    print(f"  - Active Incidents: {agg_result['active_incidents']}")
    print(f"  - Nearby Incidents: {agg_result['nearby_incidents_count']}")
    print(f"  - Aggregated Risk: {agg_result['aggregated_risk']:.3f}")
    print(f"  - Dominant Type: {agg_result['dominant_incident_type']}")
    print(f"  - Reason: {agg_result['reason']}")
    
    # ==================== SCENARIO 3 ====================
    print("\n[SCENARIO 3] Old Incident Decay Analysis")
    print("-" * 80)
    
    decay_engine = TimeDecayEngine()
    old_incident_time = current_time - 14400  # 4 hours ago
    
    decay = decay_engine.decay_incident(old_incident_time, current_time)
    temporal_class = decay_engine.classify_temporal_relevance(old_incident_time, current_time)
    
    print(f"✓ Old Incident (4 hours ago):")
    print(f"  - Time Decay: {decay:.4f} ({temporal_class})")
    print(f"  - Half-life: {decay_engine.half_life_minutes:.1f} minutes")
    
    # Get decay curve
    decay_curve = decay_engine.get_decay_curve(max_minutes=240, step_minutes=30)
    print(f"✓ Decay Curve Sample:")
    for minutes in sorted(decay_curve.keys())[::2]:
        bar = "█" * int(decay_curve[minutes] * 20)
        print(f"  {minutes:3d}m: {decay_curve[minutes]:.3f} {bar}")
    
    # ==================== SCENARIO 4 ====================
    print("\n[SCENARIO 4] Geographic Impact Analysis")
    print("-" * 80)
    
    geo_engine = GeoEngine()
    incident_lat, incident_lon = 21.25, 81.62
    
    test_locations = [
        ("Very Close (50m)", 21.25009, 81.62009),
        ("Close (200m)", 21.25036, 81.62036),
        ("Nearby (500m)", 21.25089, 81.62089),
        ("Far (1km)", 21.25179, 81.62179),
    ]
    
    print(f"✓ Incident Location: ({incident_lat}, {incident_lon})")
    print(f"✓ Geographic Impact at Different Distances:")
    
    for desc, target_lat, target_lon in test_locations:
        distance = geo_engine.haversine_distance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        impact = geo_engine.calculate_geo_impact(
            incident_lat, incident_lon,
            target_lat, target_lon,
            decay_model="threshold"
        )
        relevance = geo_engine.classify_geo_relevance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        
        bar = "█" * int(impact * 20)
        print(f"  {desc}: {distance:.0f}m → {impact:.3f} impact ({relevance}) {bar}")
    
    print("\n" + "="*80)
    print("SCENARIO DEMONSTRATION COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Run unit tests
    print("\n" + "="*80)
    print("RUNNING UNIT TESTS")
    print("="*80 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestIncidentProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestSeverityEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeDecayEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestGeoEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestIncidentAggregator))
    suite.addTests(loader.loadTestsFromTestCase(TestExplainabilityEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run example scenarios
    if result.wasSuccessful():
        run_example_scenarios()
    else:
        print("\n❌ Some tests failed. Fix before running scenarios.")
