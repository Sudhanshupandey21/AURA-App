"""
Time Decay Engine

Handles:
- Exponential decay of incident relevance over time
- Configurable decay parameters
- Decay calculations and visualization
- Half-life calculations
"""

import logging
import math
from typing import Dict, Any, Optional

from aura_risk_engine.incident_intelligence.utils import (
    get_current_timestamp,
    minutes_elapsed,
    clip_probability,
    TIME_DECAY_LAMBDA,
    TIME_DECAY_HALF_LIFE_MINUTES,
)

logger = logging.getLogger(__name__)


class TimeDecayEngine:
    """
    Time decay modeling for incidents.
    
    Uses exponential decay to model how incident relevance decreases over time:
    
    decay(t) = exp(-λ * t)
    
    where:
    - t is time elapsed in minutes
    - λ is decay constant
    - decay approaches 0 as t increases
    
    Responsibilities:
    - Calculate decay factor for given timestamp
    - Configure decay parameters
    - Analyze decay curves
    - Provide decay statistics
    
    Typical Impact Timeline:
    - 5 minutes: 0.92 impact
    - 30 minutes: 0.61 impact
    - 60 minutes: 0.37 impact
    - 2 hours: 0.14 impact
    - 4 hours: 0.02 impact
    """
    
    def __init__(
        self,
        lambda_decay: float = TIME_DECAY_LAMBDA,
        half_life_minutes: float = TIME_DECAY_HALF_LIFE_MINUTES
    ):
        """
        Initialize time decay engine.
        
        Args:
            lambda_decay: Decay constant λ per minute
                         Default 1/60 means 60 minute decay period
            half_life_minutes: Time in minutes for decay to 50%
                             Used to calculate λ if lambda_decay provided
        
        Note:
            If both provided, lambda_decay takes precedence.
            half_life = ln(2) / λ
        """
        self.lambda_decay = lambda_decay
        self.half_life_minutes = half_life_minutes
        self.logger = logger
        
        # Recalculate half-life if custom lambda provided
        if lambda_decay != TIME_DECAY_LAMBDA:
            self.half_life_minutes = math.log(2) / lambda_decay
            self.logger.debug(
                f"Decay engine configured with λ={lambda_decay}, "
                f"half-life={self.half_life_minutes:.2f} minutes"
            )
    
    def decay_incident(
        self,
        timestamp: float,
        current_time: float = None
    ) -> float:
        """
        Calculate decay factor for incident.
        
        Uses exponential decay: decay = exp(-λ * minutes_elapsed)
        
        Args:
            timestamp: Unix timestamp of incident occurrence
            current_time: Current time for decay calculation (defaults to now)
        
        Returns:
            float: Decay factor between 0 and 1
                  1.0 = fresh incident
                  0.5 = at half-life
                  0.0 = very old incident
                  
        Example:
            >>> engine = TimeDecayEngine()
            >>> current = get_current_timestamp()
            >>> # 30 minutes ago
            >>> old_time = current - 30 * 60
            >>> decay = engine.decay_incident(old_time, current)
            >>> decay
            0.609...  # ~60% impact remaining
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Calculate time elapsed in minutes
        minutes = minutes_elapsed(timestamp, current_time)
        
        # Ensure non-negative time
        minutes = max(0.0, minutes)
        
        # Calculate exponential decay
        decay_factor = math.exp(-self.lambda_decay * minutes)
        
        # Clip to valid probability range
        decay_factor = clip_probability(decay_factor)
        
        self.logger.debug(
            f"Decay for timestamp {timestamp}: "
            f"{minutes:.2f} minutes elapsed, decay={decay_factor:.4f}"
        )
        
        return decay_factor
    
    def decay_batch(
        self,
        timestamps: list,
        current_time: float = None
    ) -> list:
        """
        Calculate decay for multiple timestamps.
        
        Args:
            timestamps: List of Unix timestamps
            current_time: Current time for calculation
        
        Returns:
            list: List of decay factors corresponding to input timestamps
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        return [
            self.decay_incident(ts, current_time)
            for ts in timestamps
        ]
    
    def time_to_decay(self, target_decay: float) -> float:
        """
        Calculate time (minutes) needed to reach target decay level.
        
        Inverse of decay function:
        t = -ln(decay) / λ
        
        Args:
            target_decay: Target decay factor (0 to 1)
        
        Returns:
            float: Time in minutes to reach this decay level
            
        Raises:
            ValueError: If target_decay not in valid range
            
        Example:
            >>> engine = TimeDecayEngine()
            >>> # How long until incident decays to 10% impact?
            >>> time = engine.time_to_decay(0.1)
            >>> time
            138.16...  # ~138 minutes or ~2.3 hours
        """
        if not (0.0 < target_decay <= 1.0):
            raise ValueError(
                f"Target decay {target_decay} out of range (0, 1]"
            )
        
        # Calculate inverse: t = -ln(decay) / λ
        time_minutes = -math.log(target_decay) / self.lambda_decay
        
        return time_minutes
    
    def get_decay_curve(
        self,
        max_minutes: int = 480,
        step_minutes: int = 15
    ) -> Dict[int, float]:
        """
        Generate decay curve over time.
        
        Args:
            max_minutes: Maximum time range (default 480 = 8 hours)
            step_minutes: Time step for calculation (default 15 minutes)
        
        Returns:
            Dict: Mapping of time (minutes) to decay factor
            
        Example:
            >>> engine = TimeDecayEngine()
            >>> curve = engine.get_decay_curve(max_minutes=120, step_minutes=30)
            >>> for time, decay in sorted(curve.items()):
            ...     print(f"{time:3d} min: {decay:.3f}")
              0 min: 1.000
             30 min: 0.609
             60 min: 0.368
             90 min: 0.223
            120 min: 0.135
        """
        curve = {}
        
        for minutes in range(0, max_minutes + step_minutes, max(1, step_minutes)):
            decay = math.exp(-self.lambda_decay * minutes)
            curve[minutes] = clip_probability(decay)
        
        return curve
    
    def classify_temporal_relevance(self, timestamp: float, current_time: float = None) -> str:
        """
        Classify incident temporal relevance.
        
        Args:
            timestamp: Unix timestamp of incident
            current_time: Current time for calculation
        
        Returns:
            str: Relevance category
        """
        decay = self.decay_incident(timestamp, current_time)
        
        if decay > 0.7:
            return "Fresh"
        elif decay > 0.4:
            return "Recent"
        elif decay > 0.15:
            return "Aging"
        else:
            return "Stale"
    
    def set_lambda_decay(self, lambda_decay: float) -> None:
        """
        Update decay constant.
        
        Args:
            lambda_decay: New decay constant λ
            
        Raises:
            ValueError: If lambda_decay not positive
        """
        if lambda_decay <= 0:
            raise ValueError(f"Decay constant must be positive, got {lambda_decay}")
        
        old_lambda = self.lambda_decay
        self.lambda_decay = lambda_decay
        self.half_life_minutes = math.log(2) / lambda_decay
        
        self.logger.info(
            f"Updated decay constant: {old_lambda} → {lambda_decay}, "
            f"new half-life: {self.half_life_minutes:.2f} minutes"
        )
    
    def set_half_life(self, half_life_minutes: float) -> None:
        """
        Set half-life and update lambda accordingly.
        
        Args:
            half_life_minutes: New half-life in minutes
            
        Raises:
            ValueError: If half_life_minutes not positive
        """
        if half_life_minutes <= 0:
            raise ValueError(
                f"Half-life must be positive, got {half_life_minutes}"
            )
        
        old_half_life = self.half_life_minutes
        self.half_life_minutes = half_life_minutes
        self.lambda_decay = math.log(2) / half_life_minutes
        
        self.logger.info(
            f"Updated half-life: {old_half_life} → {half_life_minutes} minutes, "
            f"new lambda: {self.lambda_decay:.6f}"
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get decay engine statistics and configuration.
        
        Returns:
            Dict: Statistics including decay parameters and key milestones
        """
        return {
            "lambda_decay": self.lambda_decay,
            "half_life_minutes": self.half_life_minutes,
            "decay_at_1_hour": self.decay_incident(
                get_current_timestamp() - 60 * 60
            ),
            "decay_at_3_hours": self.decay_incident(
                get_current_timestamp() - 3 * 60 * 60
            ),
            "decay_at_8_hours": self.decay_incident(
                get_current_timestamp() - 8 * 60 * 60
            ),
            "time_to_10_percent": self.time_to_decay(0.1),
            "time_to_5_percent": self.time_to_decay(0.05),
            "time_to_1_percent": self.time_to_decay(0.01),
        }
