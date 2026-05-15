import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class RiskService {
  static final RiskService _instance = RiskService._internal();
  factory RiskService() => _instance;
  RiskService._internal();

  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> predictRisk({
    required String userId,
    required Map<String, double> location,
    Map<String, dynamic>? context,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.predictRisk}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'location': location,
          'context': context ?? {},
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to predict risk: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Risk prediction failed: $e');
    }
  }

  Future<Map<String, dynamic>> analyzeRoute({
    required String userId,
    required List<Map<String, double>> routePoints,
    Map<String, dynamic>? preferences,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.routeAnalysis}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'route_points': routePoints,
          'preferences': preferences ?? {},
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to analyze route: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Route analysis failed: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}
