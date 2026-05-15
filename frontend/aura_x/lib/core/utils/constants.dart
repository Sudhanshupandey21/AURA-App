class AppConstants {
  static const String appName = 'AURA X';
  static const String defaultUserId = 'user_001'; // For demo purposes

  // Risk levels
  static const String riskLow = 'LOW';
  static const String riskMedium = 'MEDIUM';
  static const String riskHigh = 'HIGH';
  static const String riskCritical = 'CRITICAL';

  // Incident types
  static const List<String> incidentTypes = [
    'Theft',
    'Assault',
    'Accident',
    'Suspicious Activity',
    'Medical Emergency',
    'Other'
  ];

  // Severity levels
  static const List<String> severityLevels = [
    'Low',
    'Medium',
    'High',
    'Critical'
  ];

  // Map settings
  static const double defaultZoom = 15.0;
  static const double minZoom = 10.0;
  static const double maxZoom = 18.0;
}
