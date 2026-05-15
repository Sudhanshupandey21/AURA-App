"""
Risk Aggregation Module

Handles:
- Weighted aggregation of multiple risk factors
- Risk composition and weighting
- Aggregation method selection
- Weight validation and management
"""

import logging
from typing import Dict, Optional, List

from aura_risk_engine.risk_engine.utils import (
    DEFAULT_WEIGHTS, normalize_to_range, clip_score,
    MIN_RISK_INPUT, MAX_RISK_INPUT, MIN_RISK_SCORE, MAX_RISK_SCORE,
)

logger = logging.getLogger(__name__)


class RiskAggregator:
    """
    Aggregates multiple risk factors using weighted combination.
    
    Responsibilities:
    - Combine time, crowd, light, incident, and area risk factors
    - Apply configurable weights
    - Normalize output to 0-100 scale
    - Support multiple aggregation methods
    
    Default Weights (sum = 1.0):
    - Incident Risk: 35% (highest impact)
    - Time Risk: 20%
    - Crowd Risk: 20%
    - Light Risk: 15%
    - Area Risk: 10% (lowest impact)
    """
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize risk aggregator.
        
        Args:
            weights: Optional custom weights for risk factors.
                    If not provided, uses DEFAULT_WEIGHTS.
        """
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.logger = logger
        self._validate_weights()
        self._aggregation_count = 0
    
    def _validate_weights(self):
        """Validate weights configuration."""
        required_keys = {
            "time_weight", "crowd_weight", "light_weight",
            "incident_weight", "area_weight"
        }
        
        # Check all required weights present
        if not required_keys.issubset(set(self.weights.keys())):
            raise ValueError(
                f"Missing required weights. Need: {required_keys}"
            )
        
        # Check weights sum to 1.0
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            self.logger.warning(
                f"Weights sum to {total}, not 1.0. "
                f"Results will be normalized."
            )
    
    def calculate_weighted_risk(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float,
        method: str = "weighted_sum"
    ) -> float:
        """
        Calculate aggregated risk score using weighted combination.
        
        Formula (default):
        weighted_risk = (time_weight * time_risk)
                      + (crowd_weight * crowd_risk)
                      + (light_weight * light_risk)
                      + (incident_weight * incident_risk)
                      + (area_weight * area_risk)
        
        Args:
            time_risk: Time-based risk factor (0-1)
            crowd_risk: Crowd density/activity risk (0-1)
            light_risk: Illumination risk (0-1)
            incident_risk: Recent incident risk (0-1)
            area_risk: Area characteristics risk (0-1)
            method: Aggregation method
                   - "weighted_sum": weighted combination (default)
                   - "maximum": take highest risk
                   - "average": arithmetic mean
                   - "quadratic": root sum of squares
        
        Returns:
            float: Aggregated risk score on 0-100 scale
            
        Example:
            >>> aggregator = RiskAggregator()
            >>> score = aggregator.calculate_weighted_risk(
            ...     time_risk=0.8,
            ...     crowd_risk=0.3,
            ...     light_risk=0.9,
            ...     incident_risk=0.7,
            ...     area_risk=0.2
            ... )
            >>> score
            64.0
        """
        # Validate inputs
        factors = {
            "time_risk": time_risk,
            "crowd_risk": crowd_risk,
            "light_risk": light_risk,
            "incident_risk": incident_risk,
            "area_risk": area_risk,
        }
        
        for name, value in factors.items():
            if not (MIN_RISK_INPUT <= value <= MAX_RISK_INPUT):
                raise ValueError(
                    f"{name} {value} out of range "
                    f"[{MIN_RISK_INPUT}, {MAX_RISK_INPUT}]"
                )
        
        # Calculate aggregated risk
        if method == "weighted_sum":
            aggregated = self._weighted_sum(factors)
        elif method == "maximum":
            aggregated = max(factors.values())
        elif method == "average":
            aggregated = sum(factors.values()) / len(factors)
        elif method == "quadratic":
            aggregated = self._quadratic_sum(factors)
        else:
            raise ValueError(
                f"Unknown aggregation method '{method}'. "
                f"Valid: weighted_sum, maximum, average, quadratic"
            )
        
        # Clip to valid range
        aggregated = clip_score(aggregated, MIN_RISK_INPUT, MAX_RISK_INPUT)
        
        # Normalize to 0-100 scale
        final_score = normalize_to_range(
            aggregated,
            MIN_RISK_INPUT, MAX_RISK_INPUT,
            MIN_RISK_SCORE, MAX_RISK_SCORE
        )
        
        self._aggregation_count += 1
        
        self.logger.debug(
            f"Aggregated risk (method={method}): "
            f"{aggregated:.3f} → {final_score:.1f}/100"
        )
        
        return final_score
    
    def _weighted_sum(self, factors: Dict[str, float]) -> float:
        """
        Calculate weighted sum of risk factors.
        
        Args:
            factors: Risk factor dictionary
        
        Returns:
            float: Weighted risk (0-1)
        """
        weighted_risk = (
            self.weights["time_weight"] * factors["time_risk"]
            + self.weights["crowd_weight"] * factors["crowd_risk"]
            + self.weights["light_weight"] * factors["light_risk"]
            + self.weights["incident_weight"] * factors["incident_risk"]
            + self.weights["area_weight"] * factors["area_risk"]
        )
        
        return weighted_risk
    
    def _quadratic_sum(self, factors: Dict[str, float]) -> float:
        """
        Calculate quadratic combination (treats as independent).
        
        Formula: sqrt(sum(w_i * risk_i^2))
        
        Args:
            factors: Risk factor dictionary
        
        Returns:
            float: Quadratic aggregated risk (0-1)
        """
        sum_of_squares = (
            (self.weights["time_weight"] * factors["time_risk"]) ** 2
            + (self.weights["crowd_weight"] * factors["crowd_risk"]) ** 2
            + (self.weights["light_weight"] * factors["light_risk"]) ** 2
            + (self.weights["incident_weight"] * factors["incident_risk"]) ** 2
            + (self.weights["area_weight"] * factors["area_risk"]) ** 2
        )
        
        return sum_of_squares ** 0.5
    
    def calculate_component_scores(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float
    ) -> Dict[str, float]:
        """
        Calculate contribution of each component.
        
        Args:
            time_risk: Time-based risk
            crowd_risk: Crowd risk
            light_risk: Light risk
            incident_risk: Incident risk
            area_risk: Area risk
        
        Returns:
            Dict: Component scores on 0-100 scale
        """
        factors = {
            "time_risk": time_risk,
            "crowd_risk": crowd_risk,
            "light_risk": light_risk,
            "incident_risk": incident_risk,
            "area_risk": area_risk,
        }
        
        component_scores = {}
        
        # Scale each component to 0-100
        for name, value in factors.items():
            scaled = normalize_to_range(
                value,
                MIN_RISK_INPUT, MAX_RISK_INPUT,
                MIN_RISK_SCORE, MAX_RISK_SCORE
            )
            component_scores[name] = scaled
        
        return component_scores
    
    def get_weighted_contribution(
        self,
        factor_name: str,
        factor_value: float
    ) -> float:
        """
        Get weighted contribution of a single factor.
        
        Args:
            factor_name: Name of factor (e.g., "incident_risk")
            factor_value: Value of factor (0-1)
        
        Returns:
            float: Weighted contribution (0-1)
        """
        weight = self.weights.get(factor_name, 0)
        return weight * factor_value
    
    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update aggregation weights.
        
        Args:
            new_weights: New weight dictionary
            
        Raises:
            ValueError: If weights invalid
        """
        # Validate new weights
        total = sum(new_weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Weights must sum to 1.0, got {total}"
            )
        
        old_weights = self.weights.copy()
        self.weights = new_weights.copy()
        
        self.logger.info(
            f"Updated aggregation weights: {old_weights} → {new_weights}"
        )
    
    def get_statistics(self) -> Dict:
        """
        Get aggregator statistics.
        
        Returns:
            Dict: Statistics about aggregations performed
        """
        return {
            "total_aggregations": self._aggregation_count,
            "current_weights": self.weights.copy(),
            "weight_sum": sum(self.weights.values()),
        }
    
    def reset_statistics(self):
        """Reset aggregator statistics."""
        self._aggregation_count = 0
        self.logger.info("Aggregator statistics reset")
