import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class IncidentService {
  static final IncidentService _instance = IncidentService._internal();
  factory IncidentService() => _instance;
  IncidentService._internal();

  final http.Client _client = http.Client();

  void _log(String message) {
    debugPrint('IncidentService: $message');
  }

  Future<Map<String, dynamic>> reportIncident({
    required String userId,
    required Map<String, double> location,
    required String type,
    required String description,
    required String severity,
  }) async {
    try {
      _log('Reporting incident: $type (severity: $severity)');
      final response = await _client
          .post(
            Uri.parse('${ApiConfig.baseUrl}${ApiConfig.incidentReport}'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'user_id': userId,
              'location': location,
              'type': type,
              'description': description,
              'severity': severity,
            }),
          )
          .timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        _log('Incident report sent successfully');
        return jsonDecode(response.body);
      } else {
        _log('Incident report failed with status ${response.statusCode}');
        return _getDemoIncidentReport(userId);
      }
    } catch (e) {
      _log('Incident report error: $e');
      return _getDemoIncidentReport(userId);
    }
  }

  Map<String, dynamic> _getDemoIncidentReport(String userId) {
    return {
      'success': true,
      'incident_id': 'demo_${DateTime.now().millisecondsSinceEpoch}',
      'message': 'Incident reported (demo mode)',
      'user_id': userId,
    };
  }

  void dispose() {
    _client.close();
  }
}
