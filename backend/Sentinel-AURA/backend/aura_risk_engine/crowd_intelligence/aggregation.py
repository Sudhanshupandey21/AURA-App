from typing import Dict
from aura_risk_engine.crowd_intelligence.ble_engine import estimate_ble_crowd
from aura_risk_engine.crowd_intelligence.poi_engine import estimate_poi_density
from aura_risk_engine.crowd_intelligence.time_crowd import estimate_time_crowd
from aura_risk_engine.crowd_intelligence.normalization import normalize_crowd_density
from aura_risk_engine.crowd_intelligence.risk import get_crowd_risk
from aura_risk_engine.crowd_intelligence.explain import generate_crowd_reason


def build_crowd_feature(
    device_count: int,
    area_type: str,
    hour: int,
    ble_weight: float = 0.4,
    poi_weight: float = 0.3,
    time_weight: float = 0.3,
) -> Dict[str, object]:
    """Build a hybrid crowd feature vector using BLE, POI, and time estimates."""
    ble_density = estimate_ble_crowd(device_count)
    poi_density = estimate_poi_density(area_type)
    time_density = estimate_time_crowd(hour, area_type)

    crowd_density = (
        ble_weight * ble_density
        + poi_weight * poi_density
        + time_weight * time_density
    )
    crowd_density = normalize_crowd_density(crowd_density)
    crowd_risk = get_crowd_risk(crowd_density)
    reason = generate_crowd_reason(crowd_density)

    return {
        "ble_density": round(ble_density, 3),
        "poi_density": round(poi_density, 3),
        "time_density": round(time_density, 3),
        "crowd_density": round(crowd_density, 3),
        "crowd_risk": round(crowd_risk, 3),
        "reason": reason,
        "area_type": area_type,
        "hour": hour,
    }
