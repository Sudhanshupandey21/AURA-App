class RiskData {
  final double riskScore;
  final String riskLevel;
  final String recommendation;
  final Map<String, dynamic>? factors;
  final DateTime timestamp;

  RiskData({
    required this.riskScore,
    required this.riskLevel,
    required this.recommendation,
    this.factors,
    required this.timestamp,
  });

  factory RiskData.fromJson(Map<String, dynamic> json) {
    return RiskData(
      riskScore: json['risk_score']?.toDouble() ?? 0.0,
      riskLevel: json['risk_level'] ?? 'UNKNOWN',
      recommendation: json['recommendation'] ?? '',
      factors: json['factors'],
      timestamp:
          DateTime.parse(json['timestamp'] ?? DateTime.now().toIso8601String()),
    );
  }
}

class RouteAnalysis {
  final bool success;
  final List<Map<String, double>> safestRoute;
  final Map<String, dynamic> riskAssessment;
  final List<dynamic>? alternatives;

  RouteAnalysis({
    required this.success,
    required this.safestRoute,
    required this.riskAssessment,
    this.alternatives,
  });

  factory RouteAnalysis.fromJson(Map<String, dynamic> json) {
    return RouteAnalysis(
      success: json['success'] ?? false,
      safestRoute: List<Map<String, double>>.from(
        json['safest_route']?.map((point) => Map<String, double>.from(point)) ??
            [],
      ),
      riskAssessment: json['risk_assessment'] ?? {},
      alternatives: json['alternatives'],
    );
  }
}

class IncidentReport {
  final bool success;
  final String incidentId;
  final String message;

  IncidentReport({
    required this.success,
    required this.incidentId,
    required this.message,
  });

  factory IncidentReport.fromJson(Map<String, dynamic> json) {
    return IncidentReport(
      success: json['success'] ?? false,
      incidentId: json['incident_id'] ?? '',
      message: json['message'] ?? '',
    );
  }
}

class SOSResponse {
  final bool success;
  final String alertId;
  final String message;

  SOSResponse({
    required this.success,
    required this.alertId,
    required this.message,
  });

  factory SOSResponse.fromJson(Map<String, dynamic> json) {
    return SOSResponse(
      success: json['success'] ?? false,
      alertId: json['alert_id'] ?? '',
      message: json['message'] ?? '',
    );
  }
}
