from typing import Dict
from aura_risk_engine.light_intelligence.sensor import SensorUnavailableError, read_light_sensor
from aura_risk_engine.light_intelligence.normalization import normalize_light
from aura_risk_engine.light_intelligence.risk import get_light_risk
from aura_risk_engine.light_intelligence.fallback import estimate_light_from_time
from aura_risk_engine.light_intelligence.explain import generate_light_reason
from aura_risk_engine.light_intelligence.utils import validate_hour, validate_area_type


def build_light_feature(
    hour: int,
    area_type: str,
    sensor_available: bool = True,
    override_lux: float | None = None,
) -> Dict[str, object]:
    """Build a complete light feature vector for the AURA X safety engine."""
    validate_hour(hour)
    validate_area_type(area_type)

    try:
        lux = read_light_sensor(sensor_available=sensor_available, override_lux=override_lux)
        normalized_light = normalize_light(lux)
        source = "sensor"
    except SensorUnavailableError:
        # Fall back to time-based estimation when sensor data is unavailable.
        normalized_light = estimate_light_from_time(hour, area_type)
        lux = None
        source = "fallback"

    light_risk = get_light_risk(normalized_light)
    reason = generate_light_reason(light_risk)

    return {
        "lux": lux,
        "normalized_light": round(normalized_light, 3),
        "light_risk": round(light_risk, 3),
        "reason": reason,
        "source": source,
        "area_type": area_type,
        "hour": hour,
    }
