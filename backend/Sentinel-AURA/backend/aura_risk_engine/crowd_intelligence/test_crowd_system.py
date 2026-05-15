import pytest
from aura_risk_engine.crowd_intelligence.aggregation import build_crowd_feature
from aura_risk_engine.crowd_intelligence.ble_engine import estimate_ble_crowd
from aura_risk_engine.crowd_intelligence.poi_engine import estimate_poi_density
from aura_risk_engine.crowd_intelligence.time_crowd import estimate_time_crowd
from aura_risk_engine.crowd_intelligence.risk import get_crowd_risk
from aura_risk_engine.crowd_intelligence.explain import generate_crowd_reason


def test_empty_isolated_area():
    feature = build_crowd_feature(device_count=0, area_type="isolated", hour=2)
    assert feature["ble_density"] == 0.15
    assert feature["poi_density"] == 0.15
    assert feature["time_density"] == 0.1
    assert feature["crowd_density"] <= 0.2
    assert feature["crowd_risk"] >= 0.8
    assert feature["reason"] == "Very low crowd density detected"


def test_market_evening_crowd():
    feature = build_crowd_feature(device_count=10, area_type="market", hour=19)
    assert feature["ble_density"] == 0.9
    assert feature["poi_density"] == 0.85
    assert feature["time_density"] == 0.95
    assert 0.8 <= feature["crowd_density"] <= 1.0
    assert feature["crowd_risk"] <= 0.2
    assert feature["reason"] == "High public activity detected"


def test_residential_daytime():
    feature = build_crowd_feature(device_count=3, area_type="residential", hour=14)
    assert feature["ble_density"] == 0.55
    assert feature["poi_density"] == 0.5
    assert feature["time_density"] == 0.45
    assert 0.45 <= feature["crowd_density"] <= 0.6
    assert feature["reason"] in {"Moderate crowd presence", "High public activity detected", "Low public activity detected"}


def test_transport_hub_rush_hour():
    feature = build_crowd_feature(device_count=12, area_type="transport_hub", hour=8)
    assert feature["poi_density"] == 0.75
    assert feature["time_density"] == 0.9
    assert feature["crowd_density"] >= 0.8
    assert feature["crowd_risk"] <= 0.2
    assert feature["reason"] == "High public activity detected"


def test_late_night_isolated_zone():
    feature = build_crowd_feature(device_count=1, area_type="isolated", hour=23)
    assert feature["time_density"] == 0.1
    assert feature["crowd_density"] < 0.3
    assert feature["crowd_risk"] > 0.7
    assert feature["reason"] == "Very low crowd density detected"


def test_risk_and_reason_match():
    density = 0.25
    assert get_crowd_risk(density) == 0.75
    assert generate_crowd_reason(density) == "Low public activity detected"


def test_poi_density_market_is_high():
    assert estimate_poi_density("market") == 0.85


def test_time_crowd_residential_day_moderate():
    assert estimate_time_crowd(15, "residential") == 0.45
