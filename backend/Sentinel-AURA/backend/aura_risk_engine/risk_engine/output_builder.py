"""
Output Builder Module

Handles:
- Final risk output formatting
- Report generation
- Alert formatting
- Multiple output formats
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from aura_risk_engine.risk_engine.utils import RiskOutput, get_current_timestamp

logger = logging.getLogger(__name__)


class OutputBuilder:
    """
    Builds and formats risk engine output.
    
    Responsibilities:
    - Format final risk scores
    - Generate reports
    - Create alert messages
    - Support multiple output formats
    """
    
    def __init__(self):
        """Initialize output builder."""
        self.logger = logger
        self._outputs_generated = 0
    
    def build_final_output(
        self,
        risk_score: int,
        risk_level: str,
        trend: str,
        reasons: List[str],
        component_scores: Dict[str, int] = None,
        include_timestamp: bool = True
    ) -> Dict[str, Any]:
        """
        Build final output dictionary.
        
        Args:
            risk_score: Risk score (0-100)
            risk_level: Risk level ("SAFE", "MEDIUM", "HIGH")
            trend: Trend prediction ("increasing", "stable", "decreasing")
            reasons: List of reason strings
            component_scores: Component risk scores
            include_timestamp: Include timestamp in output
        
        Returns:
            Dict: Final output in standard format
            
        Example:
            >>> builder = OutputBuilder()
            >>> output = builder.build_final_output(
            ...     risk_score=82,
            ...     risk_level="HIGH",
            ...     trend="increasing",
            ...     reasons=["Recent incident nearby", "Dark conditions"],
            ... )
            >>> output
            {
                'risk_score': 82,
                'risk_level': 'HIGH',
                'trend': 'increasing',
                'reasons': [...],
                'timestamp': '2024-01-15T10:30:45.123Z'
            }
        """
        output = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "trend": trend,
            "reasons": reasons or [],
        }
        
        if component_scores:
            output["component_scores"] = component_scores
        
        if include_timestamp:
            output["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        self._outputs_generated += 1
        
        self.logger.debug(f"Generated final output: score={risk_score}")
        
        return output
    
    def build_detailed_report(
        self,
        risk_output: RiskOutput,
        additional_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Build detailed risk report.
        
        Args:
            risk_output: RiskOutput instance
            additional_context: Additional context to include
        
        Returns:
            Dict: Detailed report
        """
        report = {
            "summary": {
                "risk_score": risk_output.risk_score,
                "risk_level": risk_output.risk_level,
                "trend": risk_output.trend,
                "timestamp": risk_output.timestamp,
            },
            "analysis": {
                "component_scores": risk_output.component_scores,
                "top_reasons": risk_output.reasons,
                "confidence": risk_output.confidence,
            },
            "metadata": {
                "report_generated": datetime.now(timezone.utc).isoformat(),
                "version": "1.0",
            }
        }
        
        if additional_context:
            report["context"] = additional_context
        
        self._outputs_generated += 1
        
        return report
    
    def build_alert_message(
        self,
        risk_score: int,
        risk_level: str,
        top_reasons: List[str],
        include_recommendations: bool = True
    ) -> str:
        """
        Build human-readable alert message.
        
        Args:
            risk_score: Risk score (0-100)
            risk_level: Risk level
            top_reasons: Top risk reasons
            include_recommendations: Include recommendations
        
        Returns:
            str: Formatted alert message
        """
        # Header with emoji
        emoji_map = {
            "HIGH": "🚨",
            "MEDIUM": "⚠️",
            "SAFE": "✅",
        }
        emoji = emoji_map.get(risk_level, "ℹ️")
        
        message_parts = [
            f"{emoji} {risk_level} RISK",
            f"Risk Score: {risk_score}/100",
            "",
        ]
        
        # Reasons
        if top_reasons:
            message_parts.append("Key Factors:")
            for reason in top_reasons:
                message_parts.append(f"  • {reason}")
            message_parts.append("")
        
        # Recommendations
        if include_recommendations:
            recommendations = self._get_recommendations(risk_level)
            message_parts.append(recommendations)
        
        message = "\n".join(message_parts)
        
        self._outputs_generated += 1
        
        return message
    
    def build_json_output(
        self,
        risk_score: int,
        risk_level: str,
        trend: str,
        reasons: List[str],
        component_scores: Dict[str, int] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Build JSON-serializable output.
        
        Args:
            risk_score: Risk score
            risk_level: Risk level
            trend: Trend
            reasons: Reasons list
            component_scores: Component scores
            metadata: Optional metadata
        
        Returns:
            Dict: JSON-serializable output
        """
        output = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "trend": trend,
            "reasons": reasons,
        }
        
        if component_scores:
            output["component_scores"] = component_scores
        
        if metadata:
            output["metadata"] = metadata
        
        output["generated_at"] = datetime.now(timezone.utc).isoformat()
        
        return output
    
    def build_csv_row(
        self,
        risk_score: int,
        risk_level: str,
        trend: str,
        time_risk: float = None,
        crowd_risk: float = None,
        light_risk: float = None,
        incident_risk: float = None,
        area_risk: float = None
    ) -> str:
        """
        Build CSV-formatted row.
        
        Args:
            risk_score: Risk score
            risk_level: Risk level
            trend: Trend
            time_risk: Time risk factor
            crowd_risk: Crowd risk factor
            light_risk: Light risk factor
            incident_risk: Incident risk factor
            area_risk: Area risk factor
        
        Returns:
            str: CSV row
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        fields = [
            timestamp,
            str(risk_score),
            risk_level,
            trend,
        ]
        
        if time_risk is not None:
            fields.extend([
                f"{time_risk:.2f}",
                f"{crowd_risk:.2f}",
                f"{light_risk:.2f}",
                f"{incident_risk:.2f}",
                f"{area_risk:.2f}",
            ])
        
        return ",".join(fields)
    
    def _get_recommendations(self, risk_level: str) -> str:
        """Get recommendations for risk level."""
        recommendations = {
            "SAFE": "✓ Continue normal operations. Environment appears safe.",
            "MEDIUM": "⚠️ Maintain awareness. Consider additional precautions. " +
                     "Monitor for changes.",
            "HIGH": "🚨 Exercise caution. Consider alternative actions. " +
                   "Alert authorities if appropriate.",
        }
        
        return recommendations.get(
            risk_level,
            "Assess situation and take appropriate precautions."
        )
    
    def build_webhook_payload(
        self,
        risk_output: RiskOutput,
        location: Dict[str, float] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Build webhook payload for external systems.
        
        Args:
            risk_output: RiskOutput instance
            location: Location info (lat, lon)
            user_id: User identifier
        
        Returns:
            Dict: Webhook payload
        """
        payload = {
            "event": "risk_assessment",
            "severity": risk_output.risk_level,
            "score": risk_output.risk_score,
            "trend": risk_output.trend,
            "reasons": risk_output.reasons,
            "timestamp": risk_output.timestamp,
        }
        
        if location:
            payload["location"] = location
        
        if user_id:
            payload["user_id"] = user_id
        
        return payload
    
    def format_for_display(
        self,
        risk_output: RiskOutput,
        max_width: int = 80
    ) -> str:
        """
        Format output for console/display.
        
        Args:
            risk_output: RiskOutput instance
            max_width: Maximum line width
        
        Returns:
            str: Formatted display output
        """
        lines = []
        
        # Title
        emoji_map = {"HIGH": "🚨", "MEDIUM": "⚠️", "SAFE": "✅"}
        emoji = emoji_map.get(risk_output.risk_level, "ℹ️")
        title = f"{emoji} Risk Assessment: {risk_output.risk_level}"
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")
        
        # Score
        lines.append(f"Risk Score: {risk_output.risk_score}/100")
        lines.append(f"Trend: {risk_output.trend.upper()}")
        lines.append("")
        
        # Reasons
        if risk_output.reasons:
            lines.append("Contributing Factors:")
            for reason in risk_output.reasons:
                lines.append(f"  • {reason}")
            lines.append("")
        
        # Components
        if risk_output.component_scores:
            lines.append("Component Breakdown:")
            for name, score in risk_output.component_scores.items():
                bar_length = int(score / 5)  # Scale to ~20 chars max
                bar = "█" * bar_length + "░" * (20 - bar_length)
                lines.append(f"  {name:20s} {bar} {score:3d}/100")
        
        return "\n".join(lines)
    
    def get_statistics(self) -> Dict:
        """Get output builder statistics."""
        return {
            "outputs_generated": self._outputs_generated,
        }
    
    def reset_statistics(self):
        """Reset statistics."""
        self._outputs_generated = 0
