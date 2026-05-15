"""
Risk Classification Module

Handles:
- Risk level classification
- Risk category definitions
- Classification thresholds
- Risk hierarchy
"""

import logging
from typing import Dict, List, Optional

from aura_risk_engine.risk_engine.utils import RISK_THRESHOLDS, MIN_RISK_SCORE, MAX_RISK_SCORE

logger = logging.getLogger(__name__)


class RiskClassifier:
    """
    Classifies risk scores into meaningful risk levels.
    
    Risk Levels:
    - SAFE: 0-40 (Lower risk area)
    - MEDIUM: 40-70 (Moderate risk area)
    - HIGH: 70-100 (High risk area)
    
    Responsibilities:
    - Map scores to risk levels
    - Provide risk descriptions
    - Track classification statistics
    """
    
    def __init__(self, thresholds: Dict[str, tuple] = None):
        """
        Initialize risk classifier.
        
        Args:
            thresholds: Optional custom risk thresholds.
                       Maps level name to (min, max) tuple.
        """
        self.thresholds = thresholds or RISK_THRESHOLDS.copy()
        self.logger = logger
        self._classifications_count = 0
    
    def classify_risk(self, score: int) -> str:
        """
        Classify a risk score into a risk level.
        
        Args:
            score: Risk score (0-100)
        
        Returns:
            str: Risk level ("SAFE", "MEDIUM", or "HIGH")
            
        Example:
            >>> classifier = RiskClassifier()
            >>> classifier.classify_risk(35)
            "SAFE"
            >>> classifier.classify_risk(55)
            "MEDIUM"
            >>> classifier.classify_risk(85)
            "HIGH"
        """
        if not (MIN_RISK_SCORE <= score <= MAX_RISK_SCORE):
            self.logger.warning(
                f"Score {score} out of range [{MIN_RISK_SCORE}, {MAX_RISK_SCORE}]"
            )
        
        for level, (min_val, max_val) in self.thresholds.items():
            if min_val <= score < max_val:
                self._classifications_count += 1
                self.logger.debug(
                    f"Classified score {score} as {level}"
                )
                return level
        
        # Default to highest level if score equals max
        if score >= max(max_val for _, (_, max_val) in self.thresholds.items()):
            self._classifications_count += 1
            return max(self.thresholds.keys(), 
                      key=lambda k: self.thresholds[k][0])
        
        # Fallback
        self._classifications_count += 1
        return "MEDIUM"
    
    def get_risk_description(self, risk_level: str) -> str:
        """
        Get human-readable description for risk level.
        
        Args:
            risk_level: Risk level ("SAFE", "MEDIUM", "HIGH")
        
        Returns:
            str: Description
        """
        descriptions = {
            "SAFE": "Lower risk area - Safe conditions detected",
            "MEDIUM": "Moderate risk area - Monitor situation",
            "HIGH": "High risk area - Elevated caution recommended",
        }
        
        return descriptions.get(
            risk_level,
            f"Unknown risk level: {risk_level}"
        )
    
    def get_risk_recommendation(self, risk_level: str) -> str:
        """
        Get recommended action for risk level.
        
        Args:
            risk_level: Risk level
        
        Returns:
            str: Recommended action
        """
        recommendations = {
            "SAFE": "Continue normal operations. Monitor environment regularly.",
            "MEDIUM": "Maintain awareness. Increase monitoring frequency. " +
                     "Consider additional precautions.",
            "HIGH": "Exercise heightened caution. Increase security measures. " +
                   "Alert appropriate authorities if needed.",
        }
        
        return recommendations.get(
            risk_level,
            "Assess situation and take appropriate precautions."
        )
    
    def get_score_range_for_level(self, risk_level: str) -> tuple:
        """
        Get score range for a risk level.
        
        Args:
            risk_level: Risk level ("SAFE", "MEDIUM", "HIGH")
        
        Returns:
            tuple: (min_score, max_score)
        """
        return self.thresholds.get(risk_level, (None, None))
    
    def classify_batch(self, scores: List[int]) -> Dict[str, int]:
        """
        Classify multiple scores.
        
        Args:
            scores: List of risk scores
        
        Returns:
            Dict: Classification counts by level
        """
        classifications = {level: 0 for level in self.thresholds.keys()}
        
        for score in scores:
            level = self.classify_risk(score)
            classifications[level] += 1
        
        return classifications
    
    def is_safe(self, score: int) -> bool:
        """Check if score is in SAFE range."""
        return self.classify_risk(score) == "SAFE"
    
    def is_medium(self, score: int) -> bool:
        """Check if score is in MEDIUM range."""
        return self.classify_risk(score) == "MEDIUM"
    
    def is_high(self, score: int) -> bool:
        """Check if score is in HIGH range."""
        return self.classify_risk(score) == "HIGH"
    
    def get_risk_color(self, risk_level: str) -> str:
        """
        Get suggested color for risk level (for UI).
        
        Args:
            risk_level: Risk level
        
        Returns:
            str: Color name
        """
        colors = {
            "SAFE": "green",
            "MEDIUM": "yellow",
            "HIGH": "red",
        }
        
        return colors.get(risk_level, "gray")
    
    def get_risk_icon(self, risk_level: str) -> str:
        """
        Get suggested icon for risk level (for UI).
        
        Args:
            risk_level: Risk level
        
        Returns:
            str: Icon/emoji
        """
        icons = {
            "SAFE": "✓",
            "MEDIUM": "⚠",
            "HIGH": "⛔",
        }
        
        return icons.get(risk_level, "?")
    
    def update_threshold(
        self,
        level: str,
        min_val: int,
        max_val: int
    ) -> None:
        """
        Update threshold for a risk level.
        
        Args:
            level: Risk level name
            min_val: Minimum score
            max_val: Maximum score
        """
        if min_val >= max_val:
            raise ValueError("min_val must be less than max_val")
        
        old_threshold = self.thresholds.get(level)
        self.thresholds[level] = (min_val, max_val)
        
        self.logger.info(
            f"Updated threshold for {level}: {old_threshold} → ({min_val}, {max_val})"
        )
    
    def get_statistics(self) -> Dict:
        """
        Get classifier statistics.
        
        Returns:
            Dict: Statistics about classifications
        """
        return {
            "total_classifications": self._classifications_count,
            "thresholds": {k: v for k, v in self.thresholds.items()},
        }
    
    def reset_statistics(self):
        """Reset classifier statistics."""
        self._classifications_count = 0
        self.logger.info("Risk classifier statistics reset")
