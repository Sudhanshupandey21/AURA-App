import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class RiskService {
  static final RiskService _instance = RiskService._internal();
  factory RiskService() => _instance;
  RiskService._internal();

  final http.Client _client = http.Client();

  void _log(String message) {
    debugPrint('RiskService: $message');
  }

  Future<Map<String, dynamic>> predictRisk({
    required String userId,
    required Map<String, double> location,
    Map<String, dynamic>? context,
  }) async {
    try {
      _log('Predicting risk for user: $userId at ${location}');
      final response = await _client
          .post(
            Uri.parse('${ApiConfig.baseUrl}${ApiConfig.predictRisk}'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'user_id': userId,
              'location': location,
              'context': context ?? {},
            }),
          )
          .timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        _log('Risk prediction received');
        return jsonDecode(response.body);
      } else {
        _log('Risk prediction failed with status ${response.statusCode}');
        return _getDemoRiskResponse();
      }
    } catch (e) {
      _log('Risk prediction error: $e');
      return _getDemoRiskResponse();
    }
  }

  Future<Map<String, dynamic>> analyzeRoute({
    required String userId,
    required double sourceLat,
    required double sourceLng,
    required double destLat,
    required double destLng,
    Map<String, dynamic>? preferences,
  }) async {
    try {
      _log('Analyzing route for user: $userId');
      final response = await _client
          .post(
            Uri.parse('${ApiConfig.baseUrl}${ApiConfig.routeAnalysis}'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'user_id': userId,
              'source_lat': sourceLat,
              'source_lng': sourceLng,
              'dest_lat': destLat,
              'dest_lng': destLng,
              'preferences': preferences ?? {},
            }),
          )
          .timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        _log('Route analysis received');
        return jsonDecode(response.body);
      } else {
        _log('Route analysis failed with status ${response.statusCode}');
        return _getDemoRouteResponse();
      }
    } catch (e) {
      _log('Route analysis error: $e');
      return _getDemoRouteResponse();
    }
  }

  Map<String, dynamic> _getDemoRiskResponse() {
    return {
      'success': true,
      'risk_score': 2,
      'risk_level': 'LOW',
      'recommendation': 'Area appears safe (demo data)',
    };
  }

  Map<String, dynamic> _getDemoRouteResponse() {
    return {
      'success': true,
      'safe_route': [],
      'risk_score': 1.5,
      'warnings': ['Backend unavailable - using demo route'],
      'estimated_time': 'N/A',
      'distance': 'N/A',
    };
  }

  void dispose() {
    _client.close();
  }
}
