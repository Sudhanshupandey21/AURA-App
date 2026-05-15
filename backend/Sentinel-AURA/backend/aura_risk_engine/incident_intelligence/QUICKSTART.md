# Incident Intelligence Module - Quick Start Guide

## Installation

### Option 1: Direct Import (No Installation Required)

The module uses only Python standard library, so you can use it immediately:

```python
import sys
sys.path.append('path/to/incident_intelligence')

from incident_processor import IncidentProcessor
from risk_engine import RiskEngine
```

### Option 2: Development Installation

```bash
cd incident_intelligence

# Run tests
python test_incident_system.py

# Run example scenarios
python -m test_incident_system
```

## 5-Minute Quick Start

```python
from incident_intelligence import (
    IncidentProcessor,
    RiskEngine,
    ExplainabilityEngine,
    IncidentAggregator,
)

# Initialize
processor = IncidentProcessor()
risk_engine = RiskEngine()
explain_engine = ExplainabilityEngine()
aggregator = IncidentAggregator()

# Process an incident
incident = {
    "type": "assault",
    "severity": 0.85,
    "timestamp": 1715154600,
    "latitude": 21.25,
    "longitude": 81.62
}

processed = processor.process_incident(incident)
print(f"Valid: {processed.is_valid}")

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

print(f"Risk Score: {risk['risk']:.3f}")

# Generate explanation
explanation = explain_engine.explain_incident(
    processed.incident_type,
    processed.timestamp,
    processed.latitude,
    processed.longitude,
    processed.severity
)
print(f"Explanation: {explanation}")

# Add to real-time aggregation
aggregator.add_incident(processed.to_dict())

# Get aggregated view
aggregation = aggregator.aggregate_incidents(21.25, 81.62)
print(f"Aggregated Risk: {aggregation['aggregated_risk']:.3f}")
```

## Real-World Example: Incident Monitoring Dashboard

```python
from incident_intelligence import (
    IncidentProcessor,
    RiskEngine,
    IncidentAggregator,
    ExplainabilityEngine,
)
from collections import defaultdict
import json

class IncidentMonitoringDashboard:
    """Real-time incident monitoring system."""
    
    def __init__(self, cluster_radius=500):
        self.processor = IncidentProcessor()
        self.risk_engine = RiskEngine()
        self.aggregator = IncidentAggregator(
            cluster_radius_meters=cluster_radius
        )
        self.explain_engine = ExplainabilityEngine()
    
    def process_incident_stream(self, incidents):
        """Process incoming incident stream."""
        for raw_incident in incidents:
            # Validate
            processed = self.processor.process_incident(raw_incident)
            
            if not processed.is_valid:
                print(f"⚠️ Invalid incident: {processed.validation_errors}")
                continue
            
            # Add to tracking
            self.aggregator.add_incident(processed.to_dict())
            
            # Calculate risk
            risk = self.risk_engine.calculate_incident_risk(
                incident_type=processed.incident_type,
                timestamp=processed.timestamp,
                incident_lat=processed.latitude,
                incident_lon=processed.longitude,
                target_lat=21.25,
                target_lon=81.62,
                include_components=True
            )
            
            # Generate report
            severity_class = self.risk_engine.severity_engine.classify_severity(
                risk['severity']
            )
            
            print(f"✓ {processed.incident_type.upper()}")
            print(f"  Severity: {severity_class} ({risk['severity']:.1%})")
            print(f"  Distance: {risk['distance_meters']/1000:.2f}km")
            print(f"  Risk Score: {risk['risk']:.3f}")
    
    def get_dashboard_view(self, center_lat, center_lon):
        """Get current dashboard state."""
        # Clean stale incidents
        self.aggregator.cleanup_stale_incidents()
        
        # Get aggregation
        aggregation = self.aggregator.aggregate_incidents(
            center_lat, center_lon
        )
        
        return {
            "active_incidents": aggregation["active_incidents"],
            "nearby_incidents": aggregation["nearby_incidents_count"],
            "aggregated_risk": aggregation["aggregated_risk"],
            "risk_level": self.risk_engine.classify_risk_level(
                aggregation["aggregated_risk"]
            ),
            "dominant_type": aggregation["dominant_incident_type"],
            "reason": aggregation["reason"],
        }

# Usage
dashboard = IncidentMonitoringDashboard()

# Simulate incident stream
incidents = [
    {
        "type": "harassment",
        "timestamp": 1715154600,
        "latitude": 21.25,
        "longitude": 81.62,
    },
    {
        "type": "assault",
        "timestamp": 1715154900,
        "latitude": 21.2501,
        "longitude": 81.6201,
    },
]

dashboard.process_incident_stream(incidents)

# Get view
view = dashboard.get_dashboard_view(21.25, 81.62)
print(json.dumps(view, indent=2))
```

## Common Patterns

### Pattern 1: Risk-Based Alerting

```python
from incident_intelligence import RiskEngine

risk_engine = RiskEngine()

def check_alert_needed(incident_data, target_lat, target_lon):
    """Determine if alert should be triggered."""
    risk = risk_engine.calculate_incident_risk(
        incident_type=incident_data["type"],
        timestamp=incident_data["timestamp"],
        incident_lat=incident_data["latitude"],
        incident_lon=incident_data["longitude"],
        target_lat=target_lat,
        target_lon=target_lon
    )
    
    if risk["risk"] >= 0.8:
        return "CRITICAL_ALERT"
    elif risk["risk"] >= 0.6:
        return "HIGH_ALERT"
    elif risk["risk"] >= 0.4:
        return "MEDIUM_ALERT"
    else:
        return None
```

### Pattern 2: Heatmap Generation

```python
from incident_intelligence import RiskEngine
import numpy as np

def generate_risk_heatmap(incidents, grid_size=10):
    """Generate risk heatmap for area."""
    risk_engine = RiskEngine()
    
    # Create grid
    lats = np.linspace(21.20, 21.30, grid_size)
    lons = np.linspace(81.60, 81.70, grid_size)
    
    heatmap = {}
    
    for lat in lats:
        for lon in lons:
            cell_risks = []
            
            for incident in incidents:
                risk = risk_engine.calculate_incident_risk(
                    incident_type=incident["type"],
                    timestamp=incident["timestamp"],
                    incident_lat=incident["latitude"],
                    incident_lon=incident["longitude"],
                    target_lat=lat,
                    target_lon=lon
                )
                cell_risks.append(risk["risk"])
            
            # Aggregate
            aggregated = risk_engine.aggregate_incident_risks(
                cell_risks,
                aggregation_method="maximum"
            )
            
            heatmap[f"{lat:.4f},{lon:.4f}"] = aggregated
    
    return heatmap
```

### Pattern 3: Incident Clustering

```python
from incident_intelligence import GeoEngine
from collections import defaultdict

def cluster_incidents(incidents, radius_meters=500):
    """Cluster incidents by geographic proximity."""
    geo_engine = GeoEngine()
    clusters = defaultdict(list)
    used = set()
    
    for i, incident in enumerate(incidents):
        if i in used:
            continue
        
        cluster_id = f"cluster_{i}"
        clusters[cluster_id].append(incident)
        used.add(i)
        
        # Find nearby incidents
        nearby = geo_engine.get_nearby_incidents(
            incidents,
            incident["latitude"],
            incident["longitude"],
            radius_meters
        )
        
        for nearby_incident in nearby:
            incident_idx = incidents.index(nearby_incident["incident"])
            if incident_idx not in used:
                clusters[cluster_id].append(nearby_incident["incident"])
                used.add(incident_idx)
    
    return clusters
```

### Pattern 4: Risk Trending

```python
from incident_intelligence import IncidentAggregator
from datetime import datetime, timedelta

def get_risk_trend(aggregator, time_windows):
    """Track risk trend over time windows."""
    trend = []
    
    for hours_ago in time_windows:
        target_time = datetime.now() - timedelta(hours=hours_ago)
        
        # Get aggregation at historical time
        result = aggregator.aggregate_incidents(
            center_lat=21.25,
            center_lon=81.62,
            current_time=target_time.timestamp()
        )
        
        trend.append({
            "hours_ago": hours_ago,
            "aggregated_risk": result["aggregated_risk"],
            "active_incidents": result["active_incidents"],
        })
    
    return trend
```

## API Reference Quick Look

### Incident Processor
- `process_incident(incident)` → ProcessedIncident
- `process_incidents(incidents)` → List[ProcessedIncident]
- `get_statistics()` → Dict

### Severity Engine
- `get_severity_score(type, override)` → float
- `classify_severity(score)` → str
- `aggregate_severities(scores, method)` → float

### Time Decay Engine
- `decay_incident(timestamp, current)` → float
- `classify_temporal_relevance(timestamp)` → str
- `time_to_decay(target_level)` → float
- `get_decay_curve(max_minutes, step)` → Dict

### Geographic Engine
- `haversine_distance(lat1, lon1, lat2, lon2)` → float
- `calculate_geo_impact(...)` → float
- `classify_geo_relevance(...)` → str
- `get_nearby_incidents(...)` → List

### Risk Engine
- `calculate_incident_risk(...)` → Dict
- `calculate_batch_risk(...)` → List[Dict]
- `aggregate_incident_risks(scores, method)` → float
- `classify_risk_level(score)` → str

### Incident Aggregator
- `add_incident(incident)` → str
- `remove_incident(incident_id)` → bool
- `aggregate_incidents(lat, lon, time)` → Dict
- `cleanup_stale_incidents(time)` → int

### Explainability Engine
- `explain_incident(...)` → str
- `explain_risk_components(...)` → Dict[str, str]
- `explain_aggregation(...)` → str
- `generate_incident_report(...)` → Dict[str, str]

## Troubleshooting

### Issue: Incident validation fails
**Solution**: Check validation_errors list in ProcessedIncident
```python
if not processed.is_valid:
    for error in processed.validation_errors:
        print(error)  # See specific validation error
```

### Issue: Risk scores always low
**Solution**: Check temporal decay - incidents decay with time
```python
decay = decay_engine.decay_incident(old_timestamp)
print(f"Decay factor: {decay}")  # Should decrease with age
```

### Issue: Geographic impact unexpected
**Solution**: Verify distance calculation
```python
distance = geo_engine.haversine_distance(lat1, lon1, lat2, lon2)
print(f"Distance: {distance}m")  # Check if matches expectation
```

### Issue: Aggregator memory growing
**Solution**: Call cleanup_stale_incidents periodically
```python
removed = aggregator.cleanup_stale_incidents()
print(f"Removed {removed} stale incidents")
```

## Performance Tips

1. **Batch Operations**: Use `process_incidents()` for multiple incidents
2. **Caching**: Store frequently calculated risks
3. **Cleanup**: Regular `cleanup_stale_incidents()` calls
4. **Aggregation Methods**: Use "maximum" for speed, "quadratic" for accuracy
5. **Geographic Queries**: Limit search radius appropriately

## Testing

Run comprehensive test suite:
```bash
python test_incident_system.py
```

Includes:
- 50+ unit tests
- Integration tests
- Example scenarios
- Performance validation

## Next Steps

1. ✅ Review the [README.md](README.md) for comprehensive documentation
2. ✅ Run `test_incident_system.py` to see all tests pass
3. ✅ Try the examples above in your own code
4. ✅ Integrate into your AURA X system
5. ✅ Customize severity mappings for your domain

## Support

- **Documentation**: See [README.md](README.md)
- **Examples**: Run [test_incident_system.py](test_incident_system.py)
- **Source Code**: Review component implementations
- **Logging**: Enable debug logging for diagnostics

---

**Happy Incident Intelligence Monitoring!** 🛡️
