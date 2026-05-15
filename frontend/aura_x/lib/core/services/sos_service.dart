import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class SOSService {
  static final SOSService _instance = SOSService._internal();
  factory SOSService() => _instance;
  SOSService._internal();

  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> sendSOSAlert({
    required String userId,
    required Map<String, double> location,
    String? message,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.sos}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'location': location,
          'message': message ?? 'Emergency SOS',
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to send SOS: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('SOS alert failed: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}
