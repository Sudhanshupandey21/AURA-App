"""
Explainability Engine

Handles:
- Generation of human-readable explanations
- Risk factor ranking and analysis
- Reason articulation
- Transparency and auditability
"""

import logging
from typing import Dict, List, Tuple, Optional

from aura_risk_engine.risk_engine.utils import (
    COMPONENT_IMPORTANCE, normalize_to_range,
    MIN_RISK_SCORE, MAX_RISK_SCORE,
)

logger = logging.getLogger(__name__)


class ExplainabilityEngine:
    """
    Generates human-readable explanations for risk assessments.
    
    Provides:
    - Ranked list of risk contributors
    - Natural language explanations
    - Component analysis
    - Transparency reports
    
    Responsibilities:
    - Identify dominant risk factors
    - Generate reason strings
    - Rank reasons by importance
    - Explain risk decisions
    """
    
    def __init__(self):
        """Initialize explainability engine."""
        self.logger = logger
        self._explanations_generated = 0
    
    def generate_reasons(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float,
        max_reasons: int = 5
    ) -> List[str]:
        """
        Generate ranked list of reasons for risk level.
        
        Args:
            time_risk: Time-based risk (0-1)
            crowd_risk: Crowd risk (0-1)
            light_risk: Light risk (0-1)
            incident_risk: Incident risk (0-1)
            area_risk: Area risk (0-1)
            max_reasons: Maximum number of reasons to return
        
        Returns:
            List[str]: Ranked list of human-readable reasons
            
        Example:
            >>> engine = ExplainabilityEngine()
            >>> reasons = engine.generate_reasons(
            ...     time_risk=0.8,
            ...     crowd_risk=0.2,
            ...     light_risk=0.9,
            ...     incident_risk=0.7,
            ...     area_risk=0.1
            ... )
            >>> reasons
            ['Recent high severity incident nearby',
             'Dark environment detected',
             'Late night elevated risk']
        """
        factors = {
            "time_risk": time_risk,
            "crowd_risk": crowd_risk,
            "light_risk": light_risk,
            "incident_risk": incident_risk,
            "area_risk": area_risk,
        }
        
        # Generate reason for each factor
        all_reasons = []
        
        for factor_name, value in factors.items():
            reason = self._generate_reason_for_factor(factor_name, value)
            if reason:
                importance = COMPONENT_IMPORTANCE.get(factor_name, 0.1)
                all_reasons.append((reason, value * importance))
        
        # Sort by contribution (value * importance)
        all_reasons.sort(key=lambda x: x[1], reverse=True)
        
        # Extract just the reason strings
        ranked_reasons = [reason for reason, _ in all_reasons]
        
        # Return top N reasons
        result = ranked_reasons[:max_reasons]
        
        self._explanations_generated += 1
        
        self.logger.debug(f"Generated {len(result)} reasons")
        
        return result
    
    def _generate_reason_for_factor(
        self,
        factor_name: str,
        value: float
    ) -> Optional[str]:
        """
        Generate reason string for a risk factor.
        
        Args:
            factor_name: Name of risk factor
            value: Factor value (0-1)
        
        Returns:
            str: Reason or None if factor is low
        """
        if value < 0.3:
            return None  # Factor not significant
        
        reasons_map = {
            "time_risk": {
                "high": [
                    "Late night elevated risk",
                    "Early morning reduced visibility",
                    "Dusk increased vulnerability",
                ],
                "medium": [
                    "Non-peak hour detected",
                    "Time-based risk detected",
                ],
            },
            "crowd_risk": {
                "high": [
                    "Low public activity detected",
                    "Sparse crowd conditions",
                ],
                "medium": [
                    "Reduced crowd density",
                    "Lower than normal activity",
                ],
            },
            "light_risk": {
                "high": [
                    "Dark environment detected",
                    "Poor illumination levels",
                    "Low visibility conditions",
                ],
                "medium": [
                    "Moderate light conditions",
                    "Reduced visibility",
                ],
            },
            "incident_risk": {
                "high": [
                    "Recent high severity incident nearby",
                    "Multiple incidents in vicinity",
                    "Recent violent incident reported",
                ],
                "medium": [
                    "Recent incident activity",
                    "Recent incident in area",
                ],
            },
            "area_risk": {
                "high": [
                    "High-risk area characteristics detected",
                    "Area with historical incidents",
                ],
                "medium": [
                    "Area-based risk factors present",
                    "Mixed area characteristics",
                ],
            },
        }
        
        factor_reasons = reasons_map.get(factor_name, {})
        
        if value >= 0.7:
            reasons = factor_reasons.get("high", [])
        else:
            reasons = factor_reasons.get("medium", [])
        
        if reasons:
            return reasons[0]  # Return first reason
        
        return None
    
    def explain_risk_score(
        self,
        risk_score: int,
        risk_level: str,
        factors: Dict[str, float]
    ) -> Dict[str, str]:
        """
        Generate comprehensive explanation for risk score.
        
        Args:
            risk_score: Final risk score (0-100)
            risk_level: Risk level classification
            factors: Risk factors dictionary
        
        Returns:
            Dict with multiple explanation views
        """
        # Generate summary
        summary = self._generate_summary(risk_score, risk_level)
        
        # Generate detailed analysis
        analysis = self._generate_analysis(factors)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, factors)
        
        return {
            "summary": summary,
            "analysis": analysis,
            "recommendations": recommendations,
            "factors": self._explain_factors(factors),
        }
    
    def _generate_summary(self, risk_score: int, risk_level: str) -> str:
        """Generate summary explanation."""
        summaries = {
            "SAFE": f"Area is relatively safe with a risk score of {risk_score}/100.",
            "MEDIUM": f"Area has moderate risk with a score of {risk_score}/100. " +
                     "Monitor the situation.",
            "HIGH": f"Area has high risk with a score of {risk_score}/100. " +
                   "Increased caution recommended.",
        }
        
        return summaries.get(risk_level, f"Risk score: {risk_score}/100")
    
    def _generate_analysis(self, factors: Dict[str, float]) -> str:
        """Generate detailed factor analysis."""
        components = []
        
        for name, value in factors.items():
            pct = int(value * 100)
            components.append(f"{name}: {pct}%")
        
        return "Risk composition: " + ", ".join(components)
    
    def _generate_recommendations(
        self,
        risk_level: str,
        factors: Dict[str, float]
    ) -> str:
        """Generate recommendations based on risk level and factors."""
        recommendations = {
            "SAFE": "Continue normal operations. Routine monitoring sufficient.",
            "MEDIUM": "Maintain heightened awareness. Increase monitoring " +
                     "if conditions worsen.",
            "HIGH": "Exercise extreme caution. Consider alternative routes. " +
                   "Contact authorities if needed.",
        }
        
        base_rec = recommendations.get(risk_level, "Assess situation carefully.")
        
        # Add specific recommendations based on high factors
        high_factors = [
            name for name, value in factors.items()
            if value >= 0.7
        ]
        
        if "incident_risk" in high_factors:
            base_rec += " Avoid recent incident locations."
        if "light_risk" in high_factors:
            base_rec += " Use well-lit routes."
        if "crowd_risk" in high_factors:
            base_rec += " Seek areas with higher public presence."
        
        return base_rec
    
    def _explain_factors(self, factors: Dict[str, float]) -> Dict[str, str]:
        """Generate explanation for each factor."""
        explanations = {}
        
        factor_descriptions = {
            "time_risk": "Risk based on time of day and temporal patterns",
            "crowd_risk": "Risk based on public activity and crowd density",
            "light_risk": "Risk based on illumination and visibility",
            "incident_risk": "Risk based on recent incident reports",
            "area_risk": "Risk based on area characteristics and history",
        }
        
        for name, value in factors.items():
            base_desc = factor_descriptions.get(name, "Unknown factor")
            pct = int(value * 100)
            
            if value < 0.3:
                level = "Low"
            elif value < 0.6:
                level = "Medium"
            else:
                level = "High"
            
            explanations[name] = f"{base_desc} ({level}: {pct}%)"
        
        return explanations
    
    def get_factor_contribution(
        self,
        factor_name: str,
        factor_value: float,
        aggregated_score: float
    ) -> Dict[str, float]:
        """
        Calculate contribution of factor to final score.
        
        Args:
            factor_name: Name of factor
            factor_value: Value of factor (0-1)
            aggregated_score: Final aggregated score
        
        Returns:
            Dict with contribution metrics
        """
        importance = COMPONENT_IMPORTANCE.get(factor_name, 0.1)
        contribution = factor_value * importance
        
        percent_of_total = (
            (contribution / aggregated_score * 100)
            if aggregated_score > 0 else 0
        )
        
        return {
            "absolute_contribution": contribution,
            "percent_of_total": percent_of_total,
            "importance_weight": importance,
            "factor_value": factor_value,
        }
    
    def generate_alert_message(
        self,
        risk_score: int,
        risk_level: str,
        top_reasons: List[str]
    ) -> str:
        """
        Generate alert message for high-risk situations.
        
        Args:
            risk_score: Risk score
            risk_level: Risk level
            top_reasons: Top reasons for risk
        
        Returns:
            str: Alert message
        """
        if risk_level == "HIGH":
            message = f"🚨 HIGH RISK ALERT - Score: {risk_score}/100\n"
        elif risk_level == "MEDIUM":
            message = f"⚠️ MEDIUM RISK - Score: {risk_score}/100\n"
        else:
            message = f"✓ SAFE - Score: {risk_score}/100\n"
        
        if top_reasons:
            message += "\nKey factors:\n"
            for i, reason in enumerate(top_reasons, 1):
                message += f"  {i}. {reason}\n"
        
        return message.strip()
    
    def get_statistics(self) -> Dict:
        """Get explainability engine statistics."""
        return {
            "explanations_generated": self._explanations_generated,
        }
    
    def reset_statistics(self):
        """Reset statistics."""
        self._explanations_generated = 0
