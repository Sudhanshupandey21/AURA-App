import pytest
from aura_risk_engine.light_intelligence.feature_builder import build_light_feature
from aura_risk_engine.light_intelligence.sensor import SensorUnavailableError, read_light_sensor
from aura_risk_engine.light_intelligence.normalization import normalize_light
from aura_risk_engine.light_intelligence.risk import get_light_risk
from aura_risk_engine.light_intelligence.fallback import estimate_light_from_time


def test_very_dark_area_sensor_mode():
    output = build_light_feature(hour=23, area_type="isolated", sensor_available=True, override_lux=1.0)
    assert output["lux"] == 1.0
    assert output["normalized_light"] == 0.001
    assert output["light_risk"] == 0.999
    assert output["reason"] == "Dark area detected"
    assert output["source"] == "sensor"


def test_moderate_lighting_sensor_mode():
    output = build_light_feature(hour=20, area_type="market", sensor_available=True, override_lux=80.0)
    assert output["lux"] == 80.0
    assert output["normalized_light"] == 0.08
    assert output["light_risk"] == 0.92
    assert output["reason"] == "Dark area detected"


def test_bright_daylight_sensor_mode():
    output = build_light_feature(hour=12, area_type="residential", sensor_available=True, override_lux=1000.0)
    assert output["lux"] == 1000.0
    assert output["normalized_light"] == 1.0
    assert output["light_risk"] == 0.0
    assert output["reason"] == "Well-lit environment"


def test_fallback_estimation_mode_market():
    output = build_light_feature(hour=19, area_type="market", sensor_available=False)
    assert output["lux"] is None
    assert output["source"] == "fallback"
    assert 0.0 <= output["normalized_light"] <= 1.0
    assert output["reason"] in {
        "Dark area detected",
        "Low visibility environment",
        "Moderately lit area",
        "Well-lit environment",
    }


def test_sensor_unavailable_exception():
    with pytest.raises(SensorUnavailableError):
        read_light_sensor(sensor_available=False)


def test_normalization_bounds():
    assert normalize_light(0.0) == 0.0
    assert normalize_light(1000.0) == 1.0
    assert normalize_light(1500.0) == 1.0


def test_risk_calculation_bounds():
    assert get_light_risk(0.0) == 1.0
    assert get_light_risk(1.0) == 0.0


def test_fallback_estimation_edge_cases():
    assert estimate_light_from_time(23, "isolated") == 0.05
    assert estimate_light_from_time(14, "residential") == 0.9
