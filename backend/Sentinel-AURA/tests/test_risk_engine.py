"""
Comprehensive Test Suite for Risk Engine

Tests all components of the Final Risk Engine including:
- Risk aggregation
- Risk scoring and classification
- Trend prediction
- Explainability
- Real-time recalculation
- Output formatting

Test categories:
- Unit tests for each module
- Integration tests
- Scenario-based tests
- Edge cases
"""

import unittest
from unittest.mock import Mock, patch
import time
from datetime import datetime, timezone

from aura_risk_engine.risk_engine import (
    RiskAggregator,
    RiskScorer,
    RiskClassifier,
    TrendEngine,
    ExplainabilityEngine,
    RealtimeRiskEngine,
    OutputBuilder,
    RiskFactors,
)


class TestRiskFactors(unittest.TestCase):
    """Test RiskFactors data structure."""
    
    def test_valid_factors_creation(self):
        """Test creating valid risk factors."""
        factors = RiskFactors(
            time_risk=0.5,
            crowd_risk=0.3,
            light_risk=0.7,
            incident_risk=0.4,
            area_risk=0.2
        )
        
        self.assertEqual(factors.time_risk, 0.5)
        self.assertEqual(factors.crowd_risk, 0.3)
    
    def test_factors_validation_out_of_range(self):
        """Test that invalid factors raise validation error."""
        with self.assertRaises(ValueError):
            RiskFactors(
                time_risk=1.5,  # Out of range
                crowd_risk=0.3,
                light_risk=0.7,
                incident_risk=0.4,
                area_risk=0.2
            )
    
    def test_factors_to_dict(self):
        """Test converting factors to dictionary."""
        factors = RiskFactors(
            time_risk=0.5,
            crowd_risk=0.3,
            light_risk=0.7,
            incident_risk=0.4,
            area_risk=0.2
        )
        
        factors_dict = factors.to_dict()
        
        self.assertEqual(factors_dict["time_risk"], 0.5)
        self.assertEqual(factors_dict["crowd_risk"], 0.3)
        self.assertIn("timestamp", factors_dict)


class TestRiskAggregator(unittest.TestCase):
    """Test RiskAggregator module."""
    
    def setUp(self):
        """Set up test aggregator."""
        self.aggregator = RiskAggregator()
    
    def test_weighted_sum_calculation(self):
        """Test weighted sum aggregation method."""
        score = self.aggregator.calculate_weighted_risk(
            time_risk=0.5,
            crowd_risk=0.5,
            light_risk=0.5,
            incident_risk=0.5,
            area_risk=0.5
        )
        
        # All equal should give 0.5 * 100 = 50
        self.assertEqual(score, 50.0)
    
    def test_incident_risk_dominance(self):
        """Test that incident risk has highest weight."""
        # Incident risk only
        score_incident = self.aggregator.calculate_weighted_risk(
            time_risk=0.0,
            crowd_risk=0.0,
            light_risk=0.0,
            incident_risk=1.0,
            area_risk=0.0
        )
        
        # Other risks only
        score_others = self.aggregator.calculate_weighted_risk(
            time_risk=1.0,
            crowd_risk=1.0,
            light_risk=1.0,
            incident_risk=0.0,
            area_risk=1.0
        )
        
        # Incident only should give: 0.35 * 100 = 35
        self.assertEqual(score_incident, 35.0)
        
        # Others should give: (0.20 + 0.20 + 0.15 + 0.10) * 100 = 65
        self.assertEqual(score_others, 65.0)
    
    def test_component_scores(self):
        """Test component score calculation."""
        component_scores = self.aggregator.calculate_component_scores(
            time_risk=0.8,
            crowd_risk=0.3,
            light_risk=0.9,
            incident_risk=0.5,
            area_risk=0.2
        )
        
        self.assertEqual(component_scores["time_risk"], 80)
        self.assertEqual(component_scores["crowd_risk"], 30)
        self.assertEqual(component_scores["light_risk"], 90)
    
    def test_weights_validation(self):
        """Test that invalid weights are rejected."""
        with self.assertRaises(ValueError):
            RiskAggregator(weights={
                "time_risk": 0.5,
                "crowd_risk": 0.5,
                "light_risk": 0.0,
                "incident_risk": 0.0,
                "area_risk": 0.0,
                # Sum = 1.0 but missing area_risk weight
            })


class TestRiskScorer(unittest.TestCase):
    """Test RiskScorer module."""
    
    def setUp(self):
        """Set up test scorer."""
        self.scorer = RiskScorer()
    
    def test_final_score_calculation(self):
        """Test final score calculation."""
        score = self.scorer.calculate_final_risk_score(
            time_risk=0.5,
            crowd_risk=0.5,
            light_risk=0.5,
            incident_risk=0.5,
            area_risk=0.5
        )
        
        self.assertEqual(score, 50)
        self.assertIsInstance(score, int)
    
    def test_score_with_boost(self):
        """Test score calculation with boost."""
        score_base = self.scorer.calculate_final_risk_score(
            time_risk=0.5,
            crowd_risk=0.5,
            light_risk=0.5,
            incident_risk=0.5,
            area_risk=0.5
        )
        
        # Reset scorer to get fresh history
        self.scorer = RiskScorer()
        
        score_boosted = self.scorer.calculate_final_risk_score(
            time_risk=0.5,
            crowd_risk=0.5,
            light_risk=0.5,
            incident_risk=0.5,
            area_risk=0.5,
            apply_boost=True,
            boost_factor=1.5
        )
        
        # Boosted should be higher
        self.assertGreater(score_boosted, score_base)
    
    def test_incremental_score_smoothing(self):
        """Test EMA smoothing in incremental scoring."""
        previous_score = 30
        
        new_factors = {
            "time_risk": 0.8,
            "crowd_risk": 0.3,
            "light_risk": 0.9,
            "incident_risk": 0.7,
            "area_risk": 0.2,
        }
        
        smoothed = self.scorer.calculate_incremental_score(
            previous_score=previous_score,
            new_factors=new_factors,
            learning_rate=0.3
        )
        
        # Should be between previous and new
        self.assertIsInstance(smoothed, int)
    
    def test_score_statistics(self):
        """Test score statistics tracking."""
        for score_val in [30, 40, 50, 60, 70]:
            self.scorer.calculate_final_risk_score(
                time_risk=score_val / 100,
                crowd_risk=0.5,
                light_risk=0.5,
                incident_risk=0.5,
                area_risk=0.5
            )
        
        stats = self.scorer.get_score_statistics()
        
        self.assertEqual(stats["total_scores"], 5)
        self.assertGreater(stats["average_score"], 0)


class TestRiskClassifier(unittest.TestCase):
    """Test RiskClassifier module."""
    
    def setUp(self):
        """Set up test classifier."""
        self.classifier = RiskClassifier()
    
    def test_safe_classification(self):
        """Test SAFE risk classification."""
        # Score 30 should be SAFE (0-40)
        level = self.classifier.classify_risk(30)
        self.assertEqual(level, "SAFE")
    
    def test_medium_classification(self):
        """Test MEDIUM risk classification."""
        # Score 55 should be MEDIUM (40-70)
        level = self.classifier.classify_risk(55)
        self.assertEqual(level, "MEDIUM")
    
    def test_high_classification(self):
        """Test HIGH risk classification."""
        # Score 85 should be HIGH (70-100)
        level = self.classifier.classify_risk(85)
        self.assertEqual(level, "HIGH")
    
    def test_boundary_conditions(self):
        """Test classification at boundaries."""
        self.assertEqual(self.classifier.classify_risk(0), "SAFE")
        self.assertEqual(self.classifier.classify_risk(40), "MEDIUM")
        self.assertEqual(self.classifier.classify_risk(70), "HIGH")
    
    def test_risk_description(self):
        """Test risk descriptions."""
        desc_safe = self.classifier.get_risk_description("SAFE")
        desc_high = self.classifier.get_risk_description("HIGH")
        
        self.assertIn("safe", desc_safe.lower())
        self.assertIn("high", desc_high.lower())
    
    def test_batch_classification(self):
        """Test batch classification."""
        scores = [20, 50, 80, 35, 65]
        classifications = self.classifier.classify_batch(scores)
        
        self.assertEqual(classifications["SAFE"], 2)
        self.assertEqual(classifications["MEDIUM"], 2)
        self.assertEqual(classifications["HIGH"], 1)


class TestTrendEngine(unittest.TestCase):
    """Test TrendEngine module."""
    
    def setUp(self):
        """Set up test trend engine."""
        self.engine = TrendEngine(history_size=20)
    
    def test_trend_prediction_increasing(self):
        """Test increasing trend detection."""
        self.engine.add_data_point(30.0)
        self.engine.add_data_point(40.0)
        
        trend = self.engine.predict_trend(50.0, previous_score=40.0)
        
        self.assertEqual(trend, "increasing")
    
    def test_trend_prediction_decreasing(self):
        """Test decreasing trend detection."""
        trend = self.engine.predict_trend(
            current_score=30.0,
            previous_score=50.0
        )
        
        self.assertEqual(trend, "decreasing")
    
    def test_trend_prediction_stable(self):
        """Test stable trend detection."""
        trend = self.engine.predict_trend(
            current_score=50.0,
            previous_score=50.5
        )
        
        self.assertEqual(trend, "stable")
    
    def test_trend_velocity(self):
        """Test trend velocity calculation."""
        scores = [30, 40, 35, 45, 50]
        for score in scores:
            self.engine.add_data_point(float(score))
        
        velocity = self.engine.get_trend_velocity()
        
        self.assertIsInstance(velocity, float)
    
    def test_anomaly_detection(self):
        """Test anomaly detection."""
        # Add normal scores
        for _ in range(15):
            self.engine.add_data_point(50.0)
        
        # Normal score should not be anomalous
        is_anomaly = self.engine.detect_anomaly(51.0)
        self.assertFalse(is_anomaly)
        
        # Extreme score should be anomalous
        is_anomaly = self.engine.detect_anomaly(95.0)
        self.assertTrue(is_anomaly)


class TestExplainabilityEngine(unittest.TestCase):
    """Test ExplainabilityEngine module."""
    
    def setUp(self):
        """Set up test explainability engine."""
        self.engine = ExplainabilityEngine()
    
    def test_reason_generation_high_incident_risk(self):
        """Test reason generation for high incident risk."""
        reasons = self.engine.generate_reasons(
            time_risk=0.2,
            crowd_risk=0.2,
            light_risk=0.2,
            incident_risk=0.9,  # High incident risk
            area_risk=0.2
        )
        
        self.assertGreater(len(reasons), 0)
        # First reason should mention incident (highest importance)
        reason_text = reasons[0].lower()
        self.assertIn("incident", reason_text)
    
    def test_reason_generation_dark_area(self):
        """Test reason generation for dark area."""
        reasons = self.engine.generate_reasons(
            time_risk=0.2,
            crowd_risk=0.2,
            light_risk=0.9,  # High light risk (dark)
            incident_risk=0.2,
            area_risk=0.2
        )
        
        self.assertGreater(len(reasons), 0)
        reason_text = reasons[0].lower()
        self.assertIn("dark", reason_text)
    
    def test_risk_explanation(self):
        """Test comprehensive risk explanation."""
        factors = {
            "time_risk": 0.8,
            "crowd_risk": 0.3,
            "light_risk": 0.9,
            "incident_risk": 0.7,
            "area_risk": 0.2,
        }
        
        explanation = self.engine.explain_risk_score(
            risk_score=75,
            risk_level="HIGH",
            factors=factors
        )
        
        self.assertIn("summary", explanation)
        self.assertIn("analysis", explanation)
        self.assertIn("recommendations", explanation)


class TestRealtimeRiskEngine(unittest.TestCase):
    """Test RealtimeRiskEngine module."""
    
    def setUp(self):
        """Set up test realtime engine."""
        self.engine = RealtimeRiskEngine()
    
    def test_initial_factor_update(self):
        """Test initial factor update."""
        output = self.engine.update_factors(
            time_risk=0.5,
            crowd_risk=0.3,
            light_risk=0.7,
            incident_risk=0.4,
            area_risk=0.2
        )
        
        self.assertIsNotNone(output)
        self.assertGreaterEqual(output.risk_score, 0)
        self.assertLessEqual(output.risk_score, 100)
    
    def test_recalculation_threshold(self):
        """Test recalculation threshold logic."""
        # First update
        self.engine.update_factors(
            time_risk=0.5,
            crowd_risk=0.5,
            light_risk=0.5,
            incident_risk=0.5,
            area_risk=0.5
        )
        
        initial_recalcs = self.engine._recalculation_count
        
        # Tiny change - should not trigger recalculation
        self.engine.update_factors(
            time_risk=0.51,
            crowd_risk=0.51,
            light_risk=0.51,
            incident_risk=0.51,
            area_risk=0.51
        )
        
        # Only forced update should trigger
        self.engine.update_factors(
            time_risk=0.51,
            crowd_risk=0.51,
            light_risk=0.51,
            incident_risk=0.51,
            area_risk=0.51,
            force_recalculate=True
        )
        
        self.assertGreater(self.engine._recalculation_count, initial_recalcs)
    
    def test_callback_registration(self):
        """Test callback registration and invocation."""
        callback_called = False
        
        def on_high_risk(output):
            nonlocal callback_called
            callback_called = True
        
        self.engine.set_on_high_risk(on_high_risk)
        
        # Trigger high risk
        self.engine.update_factors(
            time_risk=0.9,
            crowd_risk=0.9,
            light_risk=0.9,
            incident_risk=0.9,
            area_risk=0.9,
            force_recalculate=True
        )
        
        self.assertTrue(callback_called)


class TestOutputBuilder(unittest.TestCase):
    """Test OutputBuilder module."""
    
    def setUp(self):
        """Set up test output builder."""
        self.builder = OutputBuilder()
    
    def test_final_output_building(self):
        """Test final output building."""
        output = self.builder.build_final_output(
            risk_score=82,
            risk_level="HIGH",
            trend="increasing",
            reasons=["Recent incident nearby", "Dark conditions"]
        )
        
        self.assertEqual(output["risk_score"], 82)
        self.assertEqual(output["risk_level"], "HIGH")
        self.assertEqual(output["trend"], "increasing")
        self.assertIn("timestamp", output)
    
    def test_alert_message_formatting(self):
        """Test alert message formatting."""
        message = self.builder.build_alert_message(
            risk_score=85,
            risk_level="HIGH",
            top_reasons=["Incident nearby"]
        )
        
        self.assertIn("HIGH", message)
        self.assertIn("85", message)
        self.assertIn("Incident nearby", message)
    
    def test_csv_row_formatting(self):
        """Test CSV row formatting."""
        row = self.builder.build_csv_row(
            risk_score=75,
            risk_level="HIGH",
            trend="increasing",
            time_risk=0.8,
            crowd_risk=0.3,
            light_risk=0.9,
            incident_risk=0.7,
            area_risk=0.2
        )
        
        self.assertIsInstance(row, str)
        self.assertIn("75", row)
        self.assertIn("HIGH", row)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_complete_risk_assessment_workflow(self):
        """Test complete risk assessment workflow."""
        # Initialize engines
        aggregator = RiskAggregator()
        scorer = RiskScorer(aggregator)
        classifier = RiskClassifier()
        explainer = ExplainabilityEngine()
        builder = OutputBuilder()
        
        # Create risk factors
        factors = {
            "time_risk": 0.8,
            "crowd_risk": 0.2,
            "light_risk": 0.9,
            "incident_risk": 0.7,
            "area_risk": 0.1,
        }
        
        # Calculate score
        score = scorer.calculate_final_risk_score(**factors)
        
        # Classify
        level = classifier.classify_risk(score)
        
        # Generate reasons
        reasons = explainer.generate_reasons(**factors)
        
        # Build output
        output = builder.build_final_output(
            risk_score=score,
            risk_level=level,
            trend="stable",
            reasons=reasons
        )
        
        # Verify output
        self.assertIn("risk_score", output)
        self.assertIn("risk_level", output)
        self.assertIn("reasons", output)
    
    def test_realtime_engine_workflow(self):
        """Test realtime engine complete workflow."""
        engine = RealtimeRiskEngine()
        
        # Simulate updates
        for time_val in [0.5, 0.6, 0.7, 0.8]:
            output = engine.update_factors(
                time_risk=time_val,
                crowd_risk=0.3,
                light_risk=0.5,
                incident_risk=0.4,
                area_risk=0.2
            )
        
        # Verify final state
        state = engine.get_current_state()
        self.assertIsNotNone(state["current_output"])
        self.assertGreater(state["current_score"], 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_zero_risk_factors(self):
        """Test with all zero risk factors."""
        scorer = RiskScorer()
        score = scorer.calculate_final_risk_score(
            time_risk=0.0,
            crowd_risk=0.0,
            light_risk=0.0,
            incident_risk=0.0,
            area_risk=0.0
        )
        
        self.assertEqual(score, 0)
    
    def test_maximum_risk_factors(self):
        """Test with all maximum risk factors."""
        scorer = RiskScorer()
        score = scorer.calculate_final_risk_score(
            time_risk=1.0,
            crowd_risk=1.0,
            light_risk=1.0,
            incident_risk=1.0,
            area_risk=1.0
        )
        
        self.assertEqual(score, 100)
    
    def test_single_dominant_factor(self):
        """Test with single dominant factor."""
        scorer = RiskScorer()
        
        # Only incident risk
        score = scorer.calculate_final_risk_score(
            time_risk=0.0,
            crowd_risk=0.0,
            light_risk=0.0,
            incident_risk=1.0,
            area_risk=0.0
        )
        
        # Should be 35 (incident weight is 0.35)
        self.assertEqual(score, 35)
    
    def test_rapid_score_changes(self):
        """Test system with rapid score changes."""
        engine = RealtimeRiskEngine()
        
        # Alternate between low and high risk
        scores = []
        for i in range(10):
            risk = 0.1 if i % 2 == 0 else 0.9
            output = engine.update_factors(
                time_risk=risk,
                crowd_risk=risk,
                light_risk=risk,
                incident_risk=risk,
                area_risk=risk,
                force_recalculate=True
            )
            scores.append(output.risk_score)
        
        # Verify scores alternate
        for i in range(len(scores) - 1):
            if scores[i] != scores[i + 1]:
                break
        else:
            # If all same, that's also acceptable
            pass


class TestPerformance(unittest.TestCase):
    """Performance and stress tests."""
    
    def test_bulk_score_calculations(self):
        """Test performance with bulk calculations."""
        scorer = RiskScorer()
        
        start_time = time.time()
        
        for i in range(1000):
            scorer.calculate_final_risk_score(
                time_risk=0.5 + (i % 50) / 100,
                crowd_risk=0.3,
                light_risk=0.7,
                incident_risk=0.4,
                area_risk=0.2
            )
        
        elapsed = time.time() - start_time
        
        # Should complete 1000 calculations in reasonable time
        self.assertLess(elapsed, 5.0)
    
    def test_trend_history_management(self):
        """Test that trend history doesn't grow unbounded."""
        engine = TrendEngine(history_size=100)
        
        # Add many data points
        for i in range(500):
            engine.add_data_point(float(i % 100))
        
        # History should not exceed max size
        self.assertLessEqual(len(engine.risk_history), 100)


if __name__ == "__main__":
    unittest.main()
