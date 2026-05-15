import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class IncidentService {
  static final IncidentService _instance = IncidentService._internal();
  factory IncidentService() => _instance;
  IncidentService._internal();

  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> reportIncident({
    required String userId,
    required Map<String, double> location,
    required String type,
    required String description,
    required String severity,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.incidentReport}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'location': location,
          'type': type,
          'description': description,
          'severity': severity,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to report incident: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Incident report failed: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}
