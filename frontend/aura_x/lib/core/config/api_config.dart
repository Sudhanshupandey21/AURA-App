class ApiConfig {
  static const String baseUrl = "http://10.0.2.2:8000";
  static const String wsUrl = "ws://10.0.2.2:8000/ws/live-tracking";

  // API Endpoints
  static const String health = "/api/health";
  static const String systemStatus = "/api/system-status";
  static const String predictRisk = "/api/predict-risk";
  static const String routeAnalysis = "/api/route-analysis";
  static const String incidentReport = "/api/incident-report";
  static const String sos = "/api/sos";
  static const String liveLocation = "/api/live-location";

  // WebSocket endpoint
  static const String liveTracking = "/ws/live-tracking";

  // Timeout configurations
  static const Duration connectionTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
