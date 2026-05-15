"""Aggregate segment-level route risk into a single normalized route score."""

import numpy as np

from aura_risk_engine.route_safety_engine.utils import normalize_score


def calculate_route_risk(segment_risks: list[int]) -> int:
    """Calculate a normalized route risk score from segment-level risks."""
    if not isinstance(segment_risks, list) or len(segment_risks) == 0:
        raise ValueError("segment_risks must be a non-empty list of risk scores.")

    scores = np.asarray(segment_risks, dtype=float)
    if np.any(scores < 0) or np.any(scores > 100):
        raise ValueError("Segment risk scores must be between 0 and 100.")

    average_segment_risk = float(np.mean(scores))
    max_segment_risk = float(np.max(scores))
    high_spike_count = int(np.sum(scores >= 80))

    spike_penalty = min(12.0, high_spike_count * 2.5)
    route_risk = (0.7 * average_segment_risk) + (0.3 * max_segment_risk) + spike_penalty

    return normalize_score(route_risk)
