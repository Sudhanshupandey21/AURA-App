import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/config/api_config.dart';

class ApiRepository {
  static final ApiRepository _instance = ApiRepository._internal();
  factory ApiRepository() => _instance;
  ApiRepository._internal();

  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> get(String endpoint) async {
    try {
      final response = await _client.get(
        Uri.parse('${ApiConfig.baseUrl}$endpoint'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('HTTP ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      throw Exception('GET request failed: $e');
    }
  }

  Future<Map<String, dynamic>> post(
      String endpoint, Map<String, dynamic> data) async {
    try {
      final response = await _client
          .post(
            Uri.parse('${ApiConfig.baseUrl}$endpoint'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(data),
          )
          .timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('HTTP ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      throw Exception('POST request failed: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}
