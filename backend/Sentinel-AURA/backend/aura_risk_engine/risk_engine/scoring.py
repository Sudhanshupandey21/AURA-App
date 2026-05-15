"""
Risk Scoring Module

Handles:
- Final risk score calculation
- Score normalization
- Score validation
- Score statistics and trending
"""

import logging
from typing import Dict, Optional

from aura_risk_engine.risk_engine.aggregator import RiskAggregator
from aura_risk_engine.risk_engine.utils import (
    MIN_RISK_SCORE, MAX_RISK_SCORE, clip_score,
    normalize_to_range, log_risk_calculation,
)

logger = logging.getLogger(__name__)


class RiskScorer:
    """
    Calculates final risk scores from aggregated factors.
    
    Responsibilities:
    - Perform final risk score calculation
    - Validate score ranges
    - Apply score adjustments
    - Track scoring statistics
    """
    
    def __init__(self, aggregator: RiskAggregator = None):
        """
        Initialize risk scorer.
        
        Args:
            aggregator: RiskAggregator instance (creates default if None)
        """
        self.aggregator = aggregator or RiskAggregator()
        self.logger = logger
        
        self._scores_history = []
        self._calculations_count = 0
    
    def calculate_final_risk_score(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float,
        apply_boost: bool = False,
        boost_factor: float = 1.0
    ) -> int:
        """
        Calculate final risk score from all factors.
        
        Args:
            time_risk: Time-based risk (0-1)
            crowd_risk: Crowd risk (0-1)
            light_risk: Light risk (0-1)
            incident_risk: Incident risk (0-1)
            area_risk: Area risk (0-1)
            apply_boost: Whether to apply risk boost
            boost_factor: Boost multiplier (> 1.0)
        
        Returns:
            int: Final risk score (0-100)
            
        Example:
            >>> scorer = RiskScorer()
            >>> score = scorer.calculate_final_risk_score(
            ...     time_risk=0.8,
            ...     crowd_risk=0.3,
            ...     light_risk=0.9,
            ...     incident_risk=0.7,
            ...     area_risk=0.2
            ... )
            >>> score
            64
        """
        # Aggregate all factors
        aggregated_score = self.aggregator.calculate_weighted_risk(
            time_risk, crowd_risk, light_risk, incident_risk, area_risk
        )
        
        # Apply boost if needed (e.g., for high-risk incidents)
        if apply_boost and boost_factor > 1.0:
            aggregated_score = aggregated_score * boost_factor
            self.logger.debug(
                f"Applied boost factor {boost_factor}: "
                f"{aggregated_score / boost_factor:.1f} → {aggregated_score:.1f}"
            )
        
        # Ensure within valid range
        final_score = int(clip_score(aggregated_score))
        
        self._calculations_count += 1
        self._scores_history.append(final_score)
        
        self.logger.debug(
            f"Final risk score calculated: {final_score}/100"
        )
        
        return final_score
    
    def calculate_with_weights(
        self,
        factors: Dict[str, float],
        weights: Dict[str, float] = None
    ) -> int:
        """
        Calculate risk score with specific weights.
        
        Args:
            factors: Dictionary with all risk factors
            weights: Optional custom weights
        
        Returns:
            int: Final risk score
        """
        if weights:
            temp_aggregator = RiskAggregator(weights)
        else:
            temp_aggregator = self.aggregator
        
        score = temp_aggregator.calculate_weighted_risk(
            time_risk=factors.get("time_risk", 0.5),
            crowd_risk=factors.get("crowd_risk", 0.5),
            light_risk=factors.get("light_risk", 0.5),
            incident_risk=factors.get("incident_risk", 0.5),
            area_risk=factors.get("area_risk", 0.5)
        )
        
        return int(clip_score(score))
    
    def calculate_incremental_score(
        self,
        previous_score: int,
        new_factors: Dict[str, float],
        learning_rate: float = 0.3
    ) -> int:
        """
        Calculate risk score with consideration of previous score.
        
        Uses exponential moving average to smooth score changes.
        
        Args:
            previous_score: Previous risk score
            new_factors: New risk factors
            learning_rate: Weight for new score (0-1)
        
        Returns:
            int: Smoothed risk score
        """
        # Calculate new score
        new_score = self.calculate_final_risk_score(
            time_risk=new_factors.get("time_risk", 0.5),
            crowd_risk=new_factors.get("crowd_risk", 0.5),
            light_risk=new_factors.get("light_risk", 0.5),
            incident_risk=new_factors.get("incident_risk", 0.5),
            area_risk=new_factors.get("area_risk", 0.5)
        )
        
        # Apply exponential moving average
        smoothed_score = int(
            (1 - learning_rate) * previous_score + learning_rate * new_score
        )
        
        self.logger.debug(
            f"Incremental score: {previous_score} → {new_score} "
            f"(smoothed: {smoothed_score}) with α={learning_rate}"
        )
        
        return smoothed_score
    
    def apply_sensitivity_adjustment(
        self,
        base_score: int,
        sensitivity: float = 1.0
    ) -> int:
        """
        Apply sensitivity adjustment to risk score.
        
        Args:
            base_score: Base risk score
            sensitivity: Sensitivity factor
                        < 1.0 = less sensitive (dampen changes)
                        > 1.0 = more sensitive (amplify changes)
        
        Returns:
            int: Adjusted risk score
        """
        # Adjust from center (50)
        deviation = base_score - 50
        adjusted = 50 + int(deviation * sensitivity)
        
        final_score = int(clip_score(adjusted))
        
        self.logger.debug(
            f"Applied sensitivity {sensitivity}: "
            f"{base_score} → {final_score}"
        )
        
        return final_score
    
    def get_score_change(
        self,
        current_score: int,
        previous_score: int
    ) -> Dict[str, float]:
        """
        Calculate score change metrics.
        
        Args:
            current_score: Current risk score
            previous_score: Previous risk score
        
        Returns:
            Dict with change metrics
        """
        absolute_change = current_score - previous_score
        percent_change = (
            (current_score - previous_score) / previous_score
            if previous_score != 0 else 0.0
        )
        
        return {
            "absolute_change": absolute_change,
            "percent_change": percent_change,
            "direction": "increasing" if absolute_change > 0 else
                        "decreasing" if absolute_change < 0 else
                        "stable",
        }
    
    def get_score_statistics(self) -> Dict:
        """
        Get scoring statistics.
        
        Returns:
            Dict: Statistics about scores calculated
        """
        if not self._scores_history:
            return {
                "total_scores": 0,
                "min_score": None,
                "max_score": None,
                "average_score": None,
            }
        
        scores = self._scores_history
        
        return {
            "total_scores": len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "average_score": sum(scores) / len(scores),
            "last_score": scores[-1],
            "last_10_scores": scores[-10:],
        }
    
    def reset_statistics(self):
        """Reset scoring statistics."""
        self._scores_history = []
        self._calculations_count = 0
        self.logger.info("Risk scorer statistics reset")
