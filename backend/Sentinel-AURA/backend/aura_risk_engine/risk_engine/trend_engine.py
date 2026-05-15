"""
Trend Prediction Engine

Handles:
- Risk trend analysis and prediction
- Temporal risk patterns
- Trend classification
- Forecasting and anomaly detection
"""

import logging
from typing import Dict, List, Optional, Tuple
from collections import deque
from datetime import datetime, timezone, timedelta

from aura_risk_engine.risk_engine.utils import TREND_THRESHOLDS, TREND_WINDOW_SHORT, TREND_WINDOW_MEDIUM

logger = logging.getLogger(__name__)


class TrendEngine:
    """
    Analyzes and predicts risk trends.
    
    Responsibilities:
    - Track risk changes over time
    - Detect increasing/decreasing/stable trends
    - Forecast risk direction
    - Identify trend anomalies
    
    Trend Classification:
    - Decreasing: > 15% risk reduction
    - Stable: Within 15% change
    - Increasing: > 15% risk increase
    """
    
    def __init__(self, history_size: int = 100, thresholds: Dict[str, float] = None):
        """
        Initialize trend engine.
        
        Args:
            history_size: Number of historical points to maintain
            thresholds: Optional custom trend thresholds
        """
        self.history_size = history_size
        self.thresholds = thresholds or TREND_THRESHOLDS.copy()
        
        # Store historical data: (timestamp, score)
        self.risk_history: deque = deque(maxlen=history_size)
        self.factor_history: deque = deque(maxlen=history_size)
        
        self.logger = logger
        self._predictions_count = 0
    
    def add_data_point(
        self,
        risk_score: float,
        factors: Dict[str, float] = None,
        timestamp: float = None
    ) -> None:
        """
        Add a risk data point to history.
        
        Args:
            risk_score: Current risk score (0-100)
            factors: Risk factors dictionary
            timestamp: Data timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).timestamp()
        
        self.risk_history.append((timestamp, risk_score))
        if factors:
            self.factor_history.append((timestamp, factors))
        
        self.logger.debug(
            f"Added data point: score={risk_score:.1f} at {timestamp}"
        )
    
    def predict_trend(
        self,
        current_score: float,
        previous_score: float = None,
        lookback_minutes: int = 10
    ) -> str:
        """
        Predict risk trend direction.
        
        Args:
            current_score: Current risk score
            previous_score: Optional previous score (uses history if not provided)
            lookback_minutes: Minutes to look back for comparison
        
        Returns:
            str: Trend prediction ("increasing", "stable", "decreasing")
            
        Example:
            >>> engine = TrendEngine()
            >>> engine.add_data_point(35.0)
            >>> engine.add_data_point(42.0)
            >>> engine.add_data_point(38.0)
            >>> trend = engine.predict_trend(35.0)
            >>> trend
            "decreasing"
        """
        # Use provided previous score or look back in history
        if previous_score is None:
            if len(self.risk_history) < 2:
                self.logger.warning("Insufficient history for trend prediction")
                return "stable"
            
            # Get score from lookback window
            previous_score = self._get_historical_score(lookback_minutes)
        
        if previous_score is None:
            return "stable"
        
        # Calculate percent change
        if previous_score == 0:
            percent_change = 0 if current_score == 0 else 1.0
        else:
            percent_change = (current_score - previous_score) / previous_score
        
        # Classify trend
        if percent_change <= self.thresholds["decreasing"]:
            trend = "decreasing"
        elif percent_change >= self.thresholds["increasing"]:
            trend = "increasing"
        else:
            trend = "stable"
        
        self._predictions_count += 1
        
        self.logger.debug(
            f"Trend predicted: {trend} "
            f"(change: {percent_change:+.1%}, "
            f"{previous_score:.1f} → {current_score:.1f})"
        )
        
        return trend
    
    def _get_historical_score(self, lookback_minutes: int) -> Optional[float]:
        """
        Get average score from lookback window.
        
        Args:
            lookback_minutes: Minutes to look back
        
        Returns:
            float: Average score or None if no history
        """
        if not self.risk_history:
            return None
        
        current_time = datetime.now(timezone.utc).timestamp()
        lookback_time = current_time - (lookback_minutes * 60)
        
        matching_scores = [
            score for timestamp, score in self.risk_history
            if timestamp >= lookback_time
        ]
        
        if not matching_scores:
            return None
        
        return sum(matching_scores) / len(matching_scores)
    
    def get_trend_velocity(self, window_size: int = 5) -> float:
        """
        Calculate trend velocity (rate of change).
        
        Args:
            window_size: Number of recent points to analyze
        
        Returns:
            float: Velocity (points per observation)
                  Positive = increasing
                  Negative = decreasing
        """
        if len(self.risk_history) < window_size:
            return 0.0
        
        recent_scores = [
            score for _, score in list(self.risk_history)[-window_size:]
        ]
        
        # Calculate linear regression slope
        velocities = [
            recent_scores[i+1] - recent_scores[i]
            for i in range(len(recent_scores) - 1)
        ]
        
        return sum(velocities) / len(velocities) if velocities else 0.0
    
    def get_trend_acceleration(self) -> str:
        """
        Determine if trend is accelerating.
        
        Returns:
            str: "accelerating", "stable", or "decelerating"
        """
        if len(self.risk_history) < 6:
            return "stable"
        
        # Get last 6 points
        recent = [score for _, score in list(self.risk_history)[-6:]]
        
        # Split into two halves
        first_half = recent[:3]
        second_half = recent[3:]
        
        # Calculate average velocity in each half
        first_velocity = sum(
            first_half[i+1] - first_half[i]
            for i in range(len(first_half) - 1)
        ) / 2
        
        second_velocity = sum(
            second_half[i+1] - second_half[i]
            for i in range(len(second_half) - 1)
        ) / 2
        
        # Compare velocities
        acceleration = second_velocity - first_velocity
        
        if acceleration > 5:
            return "accelerating"
        elif acceleration < -5:
            return "decelerating"
        else:
            return "stable"
    
    def forecast_score(
        self,
        current_score: float,
        forecast_minutes: int = 15
    ) -> Tuple[float, str]:
        """
        Forecast risk score for future time.
        
        Args:
            current_score: Current risk score
            forecast_minutes: Minutes to forecast
        
        Returns:
            Tuple: (predicted_score, confidence_level)
        """
        if len(self.risk_history) < 3:
            return current_score, "low"
        
        # Get velocity
        velocity = self.get_trend_velocity()
        
        # Extrapolate
        number_of_observations = forecast_minutes / 5  # Assume 5-minute intervals
        forecast_score = current_score + (velocity * number_of_observations)
        
        # Clip to valid range
        forecast_score = max(0, min(100, forecast_score))
        
        # Confidence depends on history consistency
        confidence = self._calculate_forecast_confidence()
        
        self.logger.debug(
            f"Forecast: {current_score:.1f} → {forecast_score:.1f} "
            f"(+{forecast_minutes} min, velocity={velocity:.2f})"
        )
        
        return forecast_score, confidence
    
    def _calculate_forecast_confidence(self) -> str:
        """
        Calculate forecast confidence based on history stability.
        
        Returns:
            str: "low", "medium", or "high"
        """
        if len(self.risk_history) < 5:
            return "low"
        
        recent_scores = [score for _, score in list(self.risk_history)[-10:]]
        
        # Calculate variance
        if len(recent_scores) < 2:
            return "low"
        
        mean = sum(recent_scores) / len(recent_scores)
        variance = sum((x - mean) ** 2 for x in recent_scores) / len(recent_scores)
        std_dev = variance ** 0.5
        
        # Low variance = high confidence
        if std_dev < 5:
            return "high"
        elif std_dev < 15:
            return "medium"
        else:
            return "low"
    
    def detect_anomaly(
        self,
        current_score: float,
        std_dev_threshold: float = 2.0
    ) -> bool:
        """
        Detect if current score is anomalous.
        
        Args:
            current_score: Current risk score
            std_dev_threshold: Number of standard deviations for anomaly
        
        Returns:
            bool: True if anomalous
        """
        if len(self.risk_history) < 10:
            return False
        
        recent_scores = [score for _, score in list(self.risk_history)[-20:]]
        mean = sum(recent_scores) / len(recent_scores)
        variance = sum((x - mean) ** 2 for x in recent_scores) / len(recent_scores)
        std_dev = variance ** 0.5
        
        # Check if current is more than threshold std devs from mean
        if std_dev == 0:
            # When the historical data has zero variance, use a stable absolute threshold
            absolute_threshold = std_dev_threshold * 5
            is_anomaly = abs(current_score - mean) > absolute_threshold
            z_score = float('inf') if is_anomaly else 0.0
        else:
            z_score = abs(current_score - mean) / std_dev
            is_anomaly = z_score > std_dev_threshold
        
        if is_anomaly:
            self.logger.warning(
                f"Anomalous score detected: {current_score:.1f} "
                f"(z-score: {z_score:.2f})"
            )
        
        return is_anomaly
    
    def get_trend_statistics(self) -> Dict:
        """
        Get trend analysis statistics.
        
        Returns:
            Dict: Statistics about trends
        """
        if not self.risk_history:
            return {
                "data_points": 0,
                "trend": None,
                "velocity": 0.0,
            }
        
        scores = [score for _, score in self.risk_history]
        
        return {
            "data_points": len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "average_score": sum(scores) / len(scores),
            "velocity": self.get_trend_velocity(),
            "acceleration": self.get_trend_acceleration(),
        }
    
    def clear_history(self):
        """Clear all historical data."""
        self.risk_history.clear()
        self.factor_history.clear()
        self.logger.info("Trend engine history cleared")
