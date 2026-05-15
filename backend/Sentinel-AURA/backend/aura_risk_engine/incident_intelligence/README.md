# Incident Intelligence Module - AURA X

## Overview

The **Incident Intelligence Module** is a production-grade real-time incident analysis and risk assessment system for the AURA X urban safety platform. It processes, analyzes, and aggregates incident reports to dynamically determine their impact on urban safety risk.

## Key Features

✅ **Real-Time Incident Processing** - Validates and normalizes incident data streams
✅ **Severity Modeling** - Maps incident types to severity scores with custom overrides
✅ **Time Decay Engine** - Models temporal relevance using exponential decay
✅ **Geographic Impact** - Calculates distance-based impact using Haversine formula
✅ **Integrated Risk Scoring** - Combines severity, decay, and geographic factors
✅ **Real-Time Aggregation** - Clusters and aggregates nearby incidents
✅ **Explainability** - Generates human-readable explanations for all decisions

## Architecture

```
incident_intelligence/
├── __init__.py                    # Module exports
├── utils.py                       # Constants, validation, utilities
├── incident_processor.py          # Input validation & processing
├── severity_engine.py             # Incident type → severity mapping
├── decay_engine.py                # Time decay modeling
├── geo_engine.py                  # Geographic impact calculation
├── risk_engine.py                 # Integrated risk scoring
├── aggregation.py                 # Real-time incident aggregation
├── explain.py                     # Explainability engine
└── test_incident_system.py        # Comprehensive test suite
```

## Core Components

### 1. Incident Processor

**Validates and normalizes incident input data**

```python
from incident_intelligence import IncidentProcessor

processor = IncidentProcessor()

incident = {
    "type": "harassment",
    "severity": 0.8,
    "timestamp": 1715154600,
    "latitude": 21.25,
    "longitude": 81.62
}

result = processor.process_incident(incident)
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.validation_errors}")
```

**Validation Rules:**
- Severity: 0.0 to 1.0
- Coordinates: Valid lat/lon ranges
- Timestamp: Not too old (< 7 days), not future
- Incident Type: In supported list

### 2. Severity Engine

**Maps incident types to severity scores**

```python
from incident_intelligence import SeverityEngine

engine = SeverityEngine()

# Get severity for incident type
severity = engine.get_severity_score("violence")  # → 1.0

# Supported types and default scores:
# - suspicious_activity → 0.3
# - harassment → 0.6
# - theft → 0.7
# - assault → 0.85
# - violence → 1.0

# Custom override
custom_severity = engine.get_severity_score(
    "assault",
    custom_override=0.95
)

# Classify severity
category = engine.classify_severity(0.85)  # → "Critical"

# Aggregate multiple severities
severities = [0.5, 0.7, 0.6]
aggregated = engine.aggregate_severities(severities, method="maximum")
```

### 3. Time Decay Engine

**Models how incident relevance decreases over time**

Uses exponential decay formula: `decay = exp(-λ * t)`

```python
from incident_intelligence import TimeDecayEngine

engine = TimeDecayEngine()

# Calculate decay for timestamp
decay = engine.decay_incident(old_timestamp)  # → 0.61 (for 1 hour ago)

# Examples:
# - 5 min old → 0.92 impact
# - 30 min old → 0.61 impact
# - 60 min old → 0.37 impact
# - 2 hours old → 0.14 impact

# Classify temporal relevance
relevance = engine.classify_temporal_relevance(timestamp)
# → "Fresh", "Recent", "Aging", "Stale"

# Time to reach decay level
minutes = engine.time_to_decay(0.1)  # Time to 10% impact

# Get decay curve
curve = engine.get_decay_curve(max_minutes=480, step_minutes=15)
```

### 4. Geographic Engine

**Calculates geographic impact using Haversine distance**

```python
from incident_intelligence import GeoEngine

engine = GeoEngine()

# Haversine distance calculation
distance = engine.haversine_distance(
    lat1=21.25, lon1=81.62,
    lat2=21.26, lon2=81.63
)  # → distance in meters

# Geographic impact calculation
impact = engine.calculate_geo_impact(
    incident_lat=21.25,
    incident_lon=81.62,
    target_lat=21.26,
    target_lon=81.63,
    decay_model="threshold"  # or "linear", "exponential"
)  # → 0.0 to 1.0

# Distance-based impact levels:
# 0-50m → 1.0 (very high)
# 50-200m → 0.7 (high)
# 200-500m → 0.4 (medium)
# 500m-1km → 0.1 (low)
# 1km+ → 0.0 (negligible)

# Classify geographic relevance
relevance = engine.classify_geo_relevance(...)
# → "Immediate", "Nearby", "Adjacent", "Close", "Distant"

# Find nearby incidents
nearby = engine.get_nearby_incidents(
    incidents=incident_list,
    center_lat=21.25,
    center_lon=81.62,
    radius_meters=500
)
```

### 5. Risk Engine

**Integrated risk scoring combining all factors**

```python
from incident_intelligence import RiskEngine

engine = RiskEngine()

# Calculate integrated risk
result = engine.calculate_incident_risk(
    incident_type="assault",
    timestamp=1715154600,
    incident_lat=21.25,
    incident_lon=81.62,
    target_lat=21.26,
    target_lon=81.63,
    include_components=True
)

# Result structure:
# {
#     "risk": 0.595,
#     "severity": 0.85,
#     "decay": 0.60,
#     "geo_impact": 0.70,
#     "distance_meters": 1234.5,
#     "incident_type": "assault"
# }

# Risk formula:
# risk = severity * decay * geo_impact

# Batch risk calculation
results = engine.calculate_batch_risk(
    incidents=incident_list,
    target_lat=21.25,
    target_lon=81.62
)

# Aggregate risks
risks = [0.3, 0.5, 0.7]
aggregated = engine.aggregate_incident_risks(
    risks,
    method="quadratic"  # or "maximum", "average", "weighted_sum"
)

# Classify risk level
level = engine.classify_risk_level(0.75)
# → "Minimal", "Low", "Moderate", "High", "Critical"
```

### 6. Incident Aggregator

**Real-time aggregation of multiple incidents**

```python
from incident_intelligence import IncidentAggregator

aggregator = IncidentAggregator(cluster_radius_meters=500)

# Add incidents
incident_id = aggregator.add_incident({
    "type": "harassment",
    "timestamp": current_time - 300,
    "latitude": 21.25,
    "longitude": 81.62,
})

# Aggregate active incidents
result = aggregator.aggregate_incidents(
    target_lat=21.25,
    target_lon=81.62
)

# Result:
# {
#     "active_incidents": 3,
#     "nearby_incidents_count": 2,
#     "aggregated_risk": 0.82,
#     "dominant_incident_type": "assault",
#     "reason": "3 active incidents → 2 nearby → high aggregated risk",
#     "nearby_incidents": [...]
# }

# Get regional aggregate
regional = aggregator.get_regional_aggregate(
    region_id="sector_5",
    region_lat=21.25,
    region_lon=81.62
)

# Clean up stale incidents
removed = aggregator.cleanup_stale_incidents()
```

### 7. Explainability Engine

**Generate human-readable explanations**

```python
from incident_intelligence import ExplainabilityEngine

engine = ExplainabilityEngine()

# Incident explanation
explanation = engine.explain_incident(
    incident_type="harassment",
    timestamp=1715154600,
    latitude=21.25,
    longitude=81.62
)
# → "Recent harassment incident at location (21.25, 81.62) - reported 2.5 hours ago"

# Risk component breakdown
components = engine.explain_risk_components(
    severity=0.85,
    decay=0.60,
    geo_impact=0.70,
    integrated_risk=0.357
)
# Returns detailed explanations for each component

# Distance impact explanation
distance_exp = engine.explain_distance_impact(
    distance_meters=150,
    impact_factor=0.70
)
# → "Close (150.0m) - High impact (70% factor)"

# Temporal relevance explanation
temporal_exp = engine.explain_temporal_relevance(
    timestamp=1715154600,
    decay_factor=0.60
)
# → "Incident occurred 1 hour(s) ago - Moderate relevance (60% impact remaining)"

# Full incident report
report = engine.generate_incident_report(
    incident_data=incident,
    risk_components=risk_result
)
```

## Usage Examples

### Example 1: Process Single Incident

```python
from incident_intelligence import IncidentProcessor, RiskEngine, ExplainabilityEngine

# Initialize engines
processor = IncidentProcessor()
risk_engine = RiskEngine()
explain_engine = ExplainabilityEngine()

# Raw incident data
incident = {
    "type": "assault",
    "severity": 0.85,
    "timestamp": 1715154600,
    "latitude": 21.25,
    "longitude": 81.62,
    "description": "Street altercation"
}

# Process incident
processed = processor.process_incident(incident)
if not processed.is_valid:
    print(f"Invalid: {processed.validation_errors}")
else:
    # Calculate risk at target location
    risk = risk_engine.calculate_incident_risk(
        incident_type=processed.incident_type,
        timestamp=processed.timestamp,
        incident_lat=processed.latitude,
        incident_lon=processed.longitude,
        target_lat=21.26,
        target_lon=81.63,
        include_components=True
    )
    
    # Generate explanation
    explanation = explain_engine.explain_incident(
        processed.incident_type,
        processed.timestamp,
        processed.latitude,
        processed.longitude,
        processed.severity
    )
    
    print(f"Risk Score: {risk['risk']:.3f}")
    print(f"Explanation: {explanation}")
```

### Example 2: Real-Time Aggregation

```python
from incident_intelligence import IncidentAggregator

aggregator = IncidentAggregator()

# Simulate incident stream
incidents = [
    {"type": "harassment", "timestamp": now - 300, "latitude": 21.25, "longitude": 81.62},
    {"type": "assault", "timestamp": now - 600, "latitude": 21.2501, "longitude": 81.6201},
    {"type": "theft", "timestamp": now - 900, "latitude": 21.2502, "longitude": 81.6202},
]

# Add to aggregator
for incident in incidents:
    aggregator.add_incident(incident)

# Query aggregated risk
result = aggregator.aggregate_incidents(21.25, 81.62)

print(f"Active Incidents: {result['active_incidents']}")
print(f"Aggregated Risk: {result['aggregated_risk']:.3f}")
print(f"Nearby Count: {result['nearby_incidents_count']}")
print(f"Reason: {result['reason']}")
```

### Example 3: Geographic Analysis

```python
from incident_intelligence import GeoEngine

engine = GeoEngine()

# Create a risk heatmap
locations = [
    (21.25, 81.62),
    (21.26, 81.63),
    (21.27, 81.64),
    (21.35, 81.72),  # Far away
]

incident_lat, incident_lon = 21.25, 81.62

for target_lat, target_lon in locations:
    impact = engine.calculate_geo_impact(
        incident_lat, incident_lon,
        target_lat, target_lon
    )
    distance = engine.haversine_distance(
        incident_lat, incident_lon,
        target_lat, target_lon
    )
    print(f"({target_lat}, {target_lon}): {distance/1000:.2f}km → {impact:.3f} impact")
```

## Testing

Run the comprehensive test suite:

```bash
cd incident_intelligence
python test_incident_system.py
```

**Test Coverage:**
- Incident validation (valid, invalid, edge cases)
- Severity modeling (all types, custom overrides, aggregation)
- Time decay (fresh, old, half-life calculations)
- Geographic calculations (distance, impact, classifications)
- Risk scoring (single, batch, aggregation)
- Real-time aggregation (add, cleanup, regional)
- Explainability (all explanation types)
- Integration (full workflows)

**Test Output:**
- Unit tests for each component
- Integration tests for complete workflows
- Example scenarios demonstrating real-world usage
- Performance metrics and statistics

## Data Structures

### ProcessedIncident

```python
@dataclass
class ProcessedIncident:
    incident_id: str
    incident_type: str
    severity: float
    timestamp: float
    latitude: float
    longitude: float
    custom_severity_override: Optional[float] = None
    description: str = ""
    source: str = "unknown"
    is_valid: bool = True
    validation_errors: List[str] = None
```

### AggregatedIncidentInfo

```python
@dataclass
class AggregatedIncidentInfo:
    region_id: str
    center_lat: float
    center_lon: float
    active_incidents: int
    aggregated_risk: float
    dominant_incident_type: str
    incident_types: Dict[str, int]
    geographic_spread_meters: float
    oldest_incident_age_minutes: float
    newest_incident_age_minutes: float
    incidents: List[Dict[str, Any]]
```

## Configuration

### Default Parameters

```python
# Severity Scores (can be customized)
INCIDENT_TYPES = {
    "suspicious_activity": 0.3,
    "harassment": 0.6,
    "theft": 0.7,
    "assault": 0.85,
    "violence": 1.0,
}

# Time Decay
TIME_DECAY_LAMBDA = 1.0 / 60  # Decay factor per minute
TIME_DECAY_HALF_LIFE_MINUTES = 60  # Half-life

# Geographic Impact
GEO_IMPACT_THRESHOLDS = {
    "very_high": (0, 50),      # 0-50m
    "high": (50, 200),         # 50-200m
    "medium": (200, 500),      # 200-500m
    "low": (500, 1000),        # 500m-1km
    "negligible": (1000, ∞)    # 1km+
}

# Aggregation
CLUSTER_RADIUS_METERS = 500  # Grouping distance
MAX_INCIDENT_AGE_MINUTES = 480  # 8 hours
```

## Mathematical Models

### Time Decay (Exponential)

```
decay(t) = exp(-λ * t)

where:
  t = time elapsed in minutes
  λ = decay constant (default 1/60)
  
At half-life (60 minutes): decay = 0.5
After 2 hours: decay ≈ 0.135
After 4 hours: decay ≈ 0.018
```

### Geographic Impact (Threshold-based)

```
Impact by distance:
  0-50m:     1.0 (very high)
  50-200m:   0.7 (high)
  200-500m:  0.4 (medium)
  500m-1km:  0.1 (low)
  1km+:      0.0 (negligible)
```

### Integrated Risk (Multi-factor)

```
incident_risk = severity × decay × geo_impact

where:
  severity ∈ [0, 1]  - incident type severity
  decay ∈ [0, 1]     - temporal relevance
  geo_impact ∈ [0, 1] - geographic proximity
```

## Performance Characteristics

- **Incident Processing**: O(1) validation per incident
- **Risk Calculation**: O(1) for single incident
- **Batch Risk**: O(n) for n incidents
- **Aggregation**: O(n) incident clustering + O(m log m) sorting (m nearby)
- **Memory**: O(n) for n active incidents in aggregator
- **Geographic Queries**: O(n) distance calculations

## Best Practices

1. **Incident Validation**
   - Always check `is_valid` before using processed incidents
   - Handle validation errors gracefully
   - Use custom severity overrides for special cases

2. **Risk Assessment**
   - Request `include_components=True` for explainability
   - Always normalize to [0, 1] range
   - Use aggregation methods appropriate for your use case

3. **Real-Time Operations**
   - Call `cleanup_stale_incidents()` periodically
   - Use appropriate cluster radius for your area
   - Monitor aggregator statistics

4. **Explainability**
   - Always generate explanations for high-risk events
   - Log component breakdowns for audit trails
   - Use explanations in user-facing reports

## Error Handling

All components include comprehensive error handling:

```python
from incident_intelligence import IncidentProcessor

processor = IncidentProcessor()

try:
    result = processor.process_incident(incident)
    if not result.is_valid:
        print(f"Validation errors: {result.validation_errors}")
except Exception as e:
    print(f"Processing error: {e}")

# Get statistics
stats = processor.get_statistics()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

## Extension Points

The system is designed for extensibility:

```python
# Custom severity mapping
custom_severities = {
    "cyber_attack": 0.95,
    "infrastructure_failure": 0.90,
    "other": 0.40,
}

severity_engine = SeverityEngine(custom_severity_map=custom_severities)

# Custom decay function
decay_engine = TimeDecayEngine(lambda_decay=0.02)  # Longer half-life

# Custom geographic thresholds
custom_thresholds = {
    "critical": (0, 100),
    "high": (100, 300),
    "medium": (300, 800),
    "low": (800, 2000),
    "none": (2000, float('inf')),
}

geo_engine = GeoEngine(impact_thresholds=custom_thresholds)
```

## Dependencies

- Python 3.8+
- Standard library only (no external dependencies)
  - `math`: Mathematical calculations
  - `logging`: Event logging
  - `datetime`: Timestamp handling
  - `dataclasses`: Data structures
  - `typing`: Type hints

## License & Attribution

AURA X Incident Intelligence Module
Production-grade incident analysis system
Version 1.0.0

## Support & Maintenance

For issues, questions, or improvements:
1. Check the test cases for usage examples
2. Review the component docstrings
3. Check validation error messages
4. Enable debug logging for detailed diagnostics

---

**Last Updated**: May 2026
**Status**: Production Ready
