import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class RouteService {
  static final RouteService _instance = RouteService._internal();
  factory RouteService() => _instance;
  RouteService._internal();

  final http.Client _client = http.Client();

  void _log(String message) {
    debugPrint('RouteService: $message');
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
        return _getDemoRouteAnalysis();
      }
    } catch (e) {
      _log('Route analysis error: $e');
      return _getDemoRouteAnalysis();
    }
  }

  Future<List<Map<String, double>>> getSafeRoute({
    required double sourceLat,
    required double sourceLng,
    required double destLat,
    required double destLng,
    required String userId,
  }) async {
    try {
      _log(
          'Getting safe route from $sourceLat,$sourceLng to $destLat,$destLng');
      final analysis = await analyzeRoute(
        userId: userId,
        sourceLat: sourceLat,
        sourceLng: sourceLng,
        destLat: destLat,
        destLng: destLng,
      );

      if (analysis['success'] == true && analysis['safe_route'] != null) {
        _log('Safe route retrieved');
        return List<Map<String, double>>.from(analysis['safe_route']);
      } else {
        _log('Route analysis unsuccessful, using fallback');
        // Return straight line route if analysis fails
        return [
          {'lat': sourceLat, 'lng': sourceLng},
          {'lat': destLat, 'lng': destLng}
        ];
      }
    } catch (e) {
      _log('Error getting safe route: $e');
      // Return straight line route as fallback
      return [
        {'lat': sourceLat, 'lng': sourceLng},
        {'lat': destLat, 'lng': destLng}
      ];
    }
  }

  Map<String, dynamic> _getDemoRouteAnalysis() {
    return {
      'success': true,
      'safe_route': [],
      'risk_score': 1.5,
      'warnings': ['Using demo route (backend unavailable)'],
      'estimated_time': 'N/A',
      'distance': 'N/A',
    };
  }

  void dispose() {
    _client.close();
  }
}
