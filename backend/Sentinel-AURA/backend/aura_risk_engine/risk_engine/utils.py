"""
Utility functions and constants for the Final Risk Engine.

Provides:
- Constants and configuration
- Validation helpers
- Data transformation utilities
- Logging utilities
"""

import logging
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass
import math

# Configure logging
logger = logging.getLogger(__name__)

# ==================== CONSTANTS ====================

# Risk Score Range
MIN_RISK_SCORE = 0
MAX_RISK_SCORE = 100

# Risk Level Thresholds
RISK_THRESHOLDS = {
    "SAFE": (0, 40),
    "MEDIUM": (40, 70),
    "HIGH": (70, 100),
}

# Risk Factors and Default Weights
DEFAULT_WEIGHTS = {
    "time_weight": 0.20,      # Temporal risk (night, dawn, etc.)
    "crowd_weight": 0.20,     # Crowd density and activity
    "light_weight": 0.15,     # Illumination levels
    "incident_weight": 0.35,  # Recent incident impact
    "area_weight": 0.10,      # Area characteristics
}

# Validate weights sum to 1.0
TOTAL_WEIGHT = sum(DEFAULT_WEIGHTS.values())
if not math.isclose(TOTAL_WEIGHT, 1.0):
    logger.warning(f"Weights do not sum to 1.0: {TOTAL_WEIGHT}")

# Trend Classification Thresholds
TREND_THRESHOLDS = {
    "decreasing": -0.15,      # More than 15% decrease = decreasing
    "stable": 0.15,            # Within 15% = stable
    "increasing": 0.15,        # More than 15% increase = increasing
}

# Risk Input Validation
MIN_RISK_INPUT = 0.0
MAX_RISK_INPUT = 1.0

# Time Windows for Trend Analysis (minutes)
TREND_WINDOW_SHORT = 10    # 10 minutes
TREND_WINDOW_MEDIUM = 30   # 30 minutes
TREND_WINDOW_LONG = 60     # 1 hour

# Temporal Risk Factors
TEMPORAL_FACTORS = {
    "night": 0.8,          # 22:00 - 05:59 (High risk)
    "dawn": 0.6,           # 06:00 - 07:59 (Medium-high)
    "day": 0.4,            # 08:00 - 17:59 (Lower risk)
    "dusk": 0.7,           # 18:00 - 21:59 (High risk)
}

# Risk Component Importance for Explanation
COMPONENT_IMPORTANCE = {
    "incident_risk": 0.35,
    "time_risk": 0.20,
    "crowd_risk": 0.20,
    "light_risk": 0.15,
    "area_risk": 0.10,
}

# ==================== DATA STRUCTURES ====================

@dataclass
class RiskFactors:
    """Container for risk input factors."""
    time_risk: float
    crowd_risk: float
    light_risk: float
    incident_risk: float
    area_risk: float
    timestamp: float = None
    
    def __post_init__(self):
        """Validate and normalize risk factors."""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).timestamp()
        
        errors = self.validate()
        if errors:
            raise ValueError("Invalid risk factors: " + "; ".join(errors))
    
    def validate(self) -> List[str]:
        """Validate risk factors are in valid range."""
        errors = []
        
        factors = {
            "time_risk": self.time_risk,
            "crowd_risk": self.crowd_risk,
            "light_risk": self.light_risk,
            "incident_risk": self.incident_risk,
            "area_risk": self.area_risk,
        }
        
        for name, value in factors.items():
            if not (MIN_RISK_INPUT <= value <= MAX_RISK_INPUT):
                errors.append(
                    f"{name} {value} out of range [{MIN_RISK_INPUT}, {MAX_RISK_INPUT}]"
                )
        
        return errors
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "time_risk": self.time_risk,
            "crowd_risk": self.crowd_risk,
            "light_risk": self.light_risk,
            "incident_risk": self.incident_risk,
            "area_risk": self.area_risk,
            "timestamp": self.timestamp,
        }


@dataclass
class RiskOutput:
    """Final risk engine output."""
    risk_score: int
    risk_level: str
    trend: str
    reasons: List[str]
    component_scores: Dict[str, float]
    confidence: float = 1.0
    timestamp: float = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "trend": self.trend,
            "reasons": self.reasons,
            "component_scores": self.component_scores,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }


# ==================== VALIDATION FUNCTIONS ====================

def validate_risk_factor(value: float, name: str = "risk_factor") -> bool:
    """
    Validate a risk factor is in valid range.
    
    Args:
        value: Risk factor value
        name: Name of factor for error messages
    
    Returns:
        bool: True if valid
    """
    return MIN_RISK_INPUT <= value <= MAX_RISK_INPUT


def validate_risk_factors(factors: Dict[str, float]) -> List[str]:
    """
    Validate all risk factors.
    
    Args:
        factors: Dictionary of risk factors
    
    Returns:
        List[str]: List of validation errors (empty if valid)
    """
    errors = []
    
    required_factors = [
        "time_risk", "crowd_risk", "light_risk", "incident_risk", "area_risk"
    ]
    
    for factor in required_factors:
        if factor not in factors:
            errors.append(f"Missing required factor: {factor}")
        elif not validate_risk_factor(factors[factor], factor):
            errors.append(
                f"{factor} {factors[factor]} out of valid range "
                f"[{MIN_RISK_INPUT}, {MAX_RISK_INPUT}]"
            )
    
    return errors


def clip_score(score: float, min_val: float = MIN_RISK_SCORE, 
               max_val: float = MAX_RISK_SCORE) -> float:
    """
    Clip score to valid range.
    
    Args:
        score: Score to clip
        min_val: Minimum value
        max_val: Maximum value
    
    Returns:
        float: Clipped score
    """
    return max(min_val, min(max_val, score))


def normalize_to_range(value: float, old_min: float, old_max: float,
                      new_min: float, new_max: float) -> float:
    """
    Normalize value from one range to another.
    
    Args:
        value: Value to normalize
        old_min: Old range minimum
        old_max: Old range maximum
        new_min: New range minimum
        new_max: New range maximum
    
    Returns:
        float: Normalized value
    """
    if old_max == old_min:
        return new_min
    
    normalized = (value - old_min) / (old_max - old_min)
    return new_min + normalized * (new_max - new_min)


# ==================== UTILITY FUNCTIONS ====================

def get_current_timestamp() -> float:
    """Get current Unix timestamp."""
    return datetime.now(timezone.utc).timestamp()


def get_time_period(hour: int) -> str:
    """
    Classify hour into time period.
    
    Args:
        hour: Hour of day (0-23)
    
    Returns:
        str: Time period name
    """
    if 22 <= hour or hour < 6:
        return "night"
    elif 6 <= hour < 8:
        return "dawn"
    elif 8 <= hour < 18:
        return "day"
    else:  # 18-21
        return "dusk"


def calculate_time_risk_baseline(hour: int) -> float:
    """
    Calculate baseline time risk for hour of day.
    
    Args:
        hour: Hour of day (0-23)
    
    Returns:
        float: Baseline time risk (0-1)
    """
    period = get_time_period(hour)
    return TEMPORAL_FACTORS.get(period, 0.5)


def rank_risk_components(components: Dict[str, float]) -> List[Tuple[str, float]]:
    """
    Rank risk components by magnitude.
    
    Args:
        components: Dictionary of component scores
    
    Returns:
        List[Tuple]: Sorted list of (component_name, score) by score descending
    """
    return sorted(
        components.items(),
        key=lambda x: x[1],
        reverse=True
    )


# ==================== LOGGING UTILITIES ====================

def log_risk_calculation(
    risk_score: int,
    risk_level: str,
    components: Dict[str, float],
    weights: Dict[str, float]
):
    """
    Log risk calculation details.
    
    Args:
        risk_score: Final risk score
        risk_level: Risk classification
        components: Individual risk components
        weights: Weights used in calculation
    """
    logger.info(
        f"Risk calculation: score={risk_score}, level={risk_level}"
    )
    logger.debug(f"Components: {components}")
    logger.debug(f"Weights: {weights}")


def log_trend_prediction(
    current_risk: float,
    previous_risk: float,
    trend: str,
    change_percent: float
):
    """
    Log trend prediction.
    
    Args:
        current_risk: Current risk value
        previous_risk: Previous risk value
        trend: Predicted trend
        change_percent: Percentage change
    """
    logger.debug(
        f"Trend prediction: {trend} "
        f"(change: {change_percent:+.1%}, "
        f"current={current_risk:.3f}, previous={previous_risk:.3f})"
    )
