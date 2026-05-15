"""
Real-Time Risk Engine

Handles:
- Real-time risk recalculation
- Dynamic updates on factor changes
- Event-driven updates
- Continuous monitoring
"""

import logging
from typing import Dict, Optional, Callable, Any, List
from datetime import datetime, timezone

from aura_risk_engine.risk_engine.aggregator import RiskAggregator
from aura_risk_engine.risk_engine.scoring import RiskScorer
from aura_risk_engine.risk_engine.classifier import RiskClassifier
from aura_risk_engine.risk_engine.trend_engine import TrendEngine
from aura_risk_engine.risk_engine.explainability import ExplainabilityEngine
from aura_risk_engine.risk_engine.utils import RiskFactors, RiskOutput, get_current_timestamp

logger = logging.getLogger(__name__)


class RealtimeRiskEngine:
    """
    Real-time risk engine for continuous monitoring and updates.
    
    Responsibilities:
    - Handle incoming factor updates
    - Trigger recalculation on significant changes
    - Maintain real-time state
    - Support event callbacks
    - Manage update frequency
    """
    
    def __init__(
        self,
        aggregator: RiskAggregator = None,
        scorer: RiskScorer = None,
        classifier: RiskClassifier = None,
        trend_engine: TrendEngine = None,
        explainability_engine: ExplainabilityEngine = None,
        recalculation_threshold: float = 2.0
    ):
        """
        Initialize real-time risk engine.
        
        Args:
            aggregator: RiskAggregator instance
            scorer: RiskScorer instance
            classifier: RiskClassifier instance
            trend_engine: TrendEngine instance
            explainability_engine: ExplainabilityEngine instance
            recalculation_threshold: % change threshold for recalculation
        """
        self.aggregator = aggregator or RiskAggregator()
        self.scorer = scorer or RiskScorer(self.aggregator)
        self.classifier = classifier or RiskClassifier()
        self.trend_engine = trend_engine or TrendEngine()
        self.explainability_engine = explainability_engine or ExplainabilityEngine()
        
        self.recalculation_threshold = recalculation_threshold
        
        # Current state
        self.current_factors: Optional[RiskFactors] = None
        self.current_score: Optional[int] = None
        self.current_output: Optional[RiskOutput] = None
        self.last_update_time: float = get_current_timestamp()
        
        # Callbacks
        self.on_risk_changed: Optional[Callable] = None
        self.on_level_changed: Optional[Callable] = None
        self.on_high_risk: Optional[Callable] = None
        
        self.logger = logger
        self._update_count = 0
        self._recalculation_count = 0
    
    def update_factors(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float,
        force_recalculate: bool = False
    ) -> RiskOutput:
        """
        Update risk factors and recalculate if needed.
        
        Args:
            time_risk: Time-based risk (0-1)
            crowd_risk: Crowd risk (0-1)
            light_risk: Light risk (0-1)
            incident_risk: Incident risk (0-1)
            area_risk: Area risk (0-1)
            force_recalculate: Force recalculation even if change small
        
        Returns:
            RiskOutput: Updated risk output
        """
        self._update_count += 1
        
        # Create new factors
        new_factors = RiskFactors(
            time_risk=time_risk,
            crowd_risk=crowd_risk,
            light_risk=light_risk,
            incident_risk=incident_risk,
            area_risk=area_risk
        )
        
        # Check if recalculation needed
        should_recalculate = force_recalculate or self._should_recalculate(new_factors)
        
        if should_recalculate:
            self._recalculation_count += 1
            output = self._calculate_risk(new_factors)
            
            # Check for changes
            old_score = self.current_score
            old_level = self.current_output.risk_level if self.current_output else None
            
            # Update state
            self.current_factors = new_factors
            self.current_score = output.risk_score
            self.current_output = output
            self.last_update_time = get_current_timestamp()
            
            # Trigger callbacks
            if old_score is not None and old_score != output.risk_score:
                self._trigger_on_risk_changed(old_score, output.risk_score)
            
            if old_level is not None and old_level != output.risk_level:
                self._trigger_on_level_changed(old_level, output.risk_level)
            
            if output.risk_level == "HIGH":
                self._trigger_on_high_risk(output)
            
            self.logger.info(
                f"Risk recalculated: {output.risk_score}/100 ({output.risk_level})"
            )
        else:
            self.logger.debug("Update below recalculation threshold, skipped")
        
        return self.current_output
    
    def _should_recalculate(self, new_factors: RiskFactors) -> bool:
        """
        Determine if recalculation needed based on factor changes.
        
        Args:
            new_factors: New risk factors
        
        Returns:
            bool: True if recalculation needed
        """
        if self.current_factors is None:
            return True
        
        # Calculate weighted change
        change = (
            abs(new_factors.time_risk - self.current_factors.time_risk) * 0.20
            + abs(new_factors.crowd_risk - self.current_factors.crowd_risk) * 0.20
            + abs(new_factors.light_risk - self.current_factors.light_risk) * 0.15
            + abs(new_factors.incident_risk - self.current_factors.incident_risk) * 0.35
            + abs(new_factors.area_risk - self.current_factors.area_risk) * 0.10
        )
        
        return change > (self.recalculation_threshold / 100)
    
    def _calculate_risk(self, factors: RiskFactors) -> RiskOutput:
        """
        Perform complete risk calculation.
        
        Args:
            factors: Risk factors
        
        Returns:
            RiskOutput: Complete risk output
        """
        # Calculate score
        risk_score = self.scorer.calculate_final_risk_score(
            time_risk=factors.time_risk,
            crowd_risk=factors.crowd_risk,
            light_risk=factors.light_risk,
            incident_risk=factors.incident_risk,
            area_risk=factors.area_risk
        )
        
        # Classify risk
        risk_level = self.classifier.classify_risk(risk_score)
        
        # Predict trend
        if self.current_score is not None:
            trend = self.trend_engine.predict_trend(
                float(risk_score),
                float(self.current_score)
            )
        else:
            trend = "stable"
        
        # Add to trend history
        self.trend_engine.add_data_point(float(risk_score), factors.to_dict())
        
        # Generate reasons
        reasons = self.explainability_engine.generate_reasons(
            time_risk=factors.time_risk,
            crowd_risk=factors.crowd_risk,
            light_risk=factors.light_risk,
            incident_risk=factors.incident_risk,
            area_risk=factors.area_risk,
            max_reasons=3
        )
        
        # Get component scores
        component_scores = self.aggregator.calculate_component_scores(
            time_risk=factors.time_risk,
            crowd_risk=factors.crowd_risk,
            light_risk=factors.light_risk,
            incident_risk=factors.incident_risk,
            area_risk=factors.area_risk
        )
        
        # Create output
        output = RiskOutput(
            risk_score=risk_score,
            risk_level=risk_level,
            trend=trend,
            reasons=reasons,
            component_scores=component_scores
        )
        
        return output
    
    def _trigger_on_risk_changed(self, old_score: int, new_score: int) -> None:
        """Trigger risk changed callback."""
        if self.on_risk_changed:
            try:
                self.on_risk_changed(old_score, new_score)
            except Exception as e:
                self.logger.error(f"Error in on_risk_changed callback: {e}")
    
    def _trigger_on_level_changed(self, old_level: str, new_level: str) -> None:
        """Trigger level changed callback."""
        if self.on_level_changed:
            try:
                self.on_level_changed(old_level, new_level)
            except Exception as e:
                self.logger.error(f"Error in on_level_changed callback: {e}")
    
    def _trigger_on_high_risk(self, output: RiskOutput) -> None:
        """Trigger high risk callback."""
        if self.on_high_risk:
            try:
                self.on_high_risk(output)
            except Exception as e:
                self.logger.error(f"Error in on_high_risk callback: {e}")
    
    def set_on_risk_changed(self, callback: Callable) -> None:
        """Register callback for risk changes."""
        self.on_risk_changed = callback
    
    def set_on_level_changed(self, callback: Callable) -> None:
        """Register callback for level changes."""
        self.on_level_changed = callback
    
    def set_on_high_risk(self, callback: Callable) -> None:
        """Register callback for high risk alerts."""
        self.on_high_risk = callback
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current engine state.
        
        Returns:
            Dict: Current state information
        """
        return {
            "current_score": self.current_score,
            "current_output": self.current_output.to_dict() if self.current_output else None,
            "current_factors": self.current_factors.to_dict() if self.current_factors else None,
            "last_update_time": self.last_update_time,
        }
    
    def get_statistics(self) -> Dict:
        """Get real-time engine statistics."""
        return {
            "total_updates": self._update_count,
            "total_recalculations": self._recalculation_count,
            "recalculation_rate": (
                self._recalculation_count / self._update_count * 100
                if self._update_count > 0 else 0
            ),
            "recalculation_threshold": self.recalculation_threshold,
        }
    
    def reset_statistics(self):
        """Reset statistics."""
        self._update_count = 0
        self._recalculation_count = 0
