"""Segment-level risk analysis for route safety scoring."""

from aura_risk_engine.risk_engine.scoring import RiskScorer

from aura_risk_engine.route_safety_engine.utils import RouteRiskProfile, normalize_score, validate_risk_factors


class SegmentRiskEngine:
    """Engine that converts feature risks into a normalized segment risk score."""

    def __init__(self) -> None:
        self.scorer = RiskScorer()

    def analyze_segment_risk(
        self,
        time_risk: float,
        crowd_risk: float,
        light_risk: float,
        incident_risk: float,
        area_risk: float,
        profile: RouteRiskProfile = None,
    ) -> int:
        """Analyze the local risk for an individual route segment."""
        profile = profile or RouteRiskProfile(
            time_risk=time_risk,
            crowd_risk=crowd_risk,
            light_risk=light_risk,
            incident_risk=incident_risk,
            area_risk=area_risk,
        )
        validate_risk_factors(
            time_risk=profile.time_risk,
            crowd_risk=profile.crowd_risk,
            light_risk=profile.light_risk,
            incident_risk=profile.incident_risk,
            area_risk=profile.area_risk,
        )

        apply_boost = bool(profile.incident_risk >= 0.6 or profile.light_risk >= 0.85)
        boost_factor = 1.15 if profile.incident_risk >= 0.6 else 1.0

        raw_score = self.scorer.calculate_final_risk_score(
            time_risk=profile.time_risk,
            crowd_risk=profile.crowd_risk,
            light_risk=profile.light_risk,
            incident_risk=profile.incident_risk,
            area_risk=profile.area_risk,
            apply_boost=apply_boost,
            boost_factor=boost_factor,
        )

        return normalize_score(raw_score)


_default_segment_risk_engine = SegmentRiskEngine()


def analyze_segment_risk(
    time_risk: float,
    crowd_risk: float,
    light_risk: float,
    incident_risk: float,
    area_risk: float,
    profile: RouteRiskProfile = None,
) -> int:
    """Calculate the risk score for a specific route segment."""
    return _default_segment_risk_engine.analyze_segment_risk(
        time_risk,
        crowd_risk,
        light_risk,
        incident_risk,
        area_risk,
        profile,
    )
