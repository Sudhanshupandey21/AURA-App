import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class RouteService {
  static final RouteService _instance = RouteService._internal();
  factory RouteService() => _instance;
  RouteService._internal();

  final http.Client _client = http.Client();

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

  Future<List<Map<String, double>>> getSafeRoute(
    List<Map<String, double>> originalRoute, {
    required String userId,
  }) async {
    try {
      final analysis = await analyzeRoute(
        userId: userId,
        routePoints: originalRoute,
      );

      if (analysis['success'] == true) {
        return List<Map<String, double>>.from(analysis['safest_route']);
      } else {
        throw Exception('Route analysis unsuccessful');
      }
    } catch (e) {
      // Return original route if analysis fails
      return originalRoute;
    }
  }

  void dispose() {
    _client.close();
  }
}
