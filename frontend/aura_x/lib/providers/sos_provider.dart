import 'package:flutter/foundation.dart';
import '../core/services/sos_service.dart';
import '../models/models.dart';

class SOSProvider with ChangeNotifier {
  final SOSService _sosService = SOSService();
  bool _isSending = false;

  bool get isSending => _isSending;

  Future<SOSResponse?> sendSOSAlert({
    required String userId,
    required Map<String, double> location,
    String? message,
  }) async {
    _isSending = true;
    notifyListeners();

    try {
      final response = await _sosService.sendSOSAlert(
        userId: userId,
        location: location,
        message: message,
      );

      return SOSResponse.fromJson(response);
    } catch (e) {
      return null;
    } finally {
      _isSending = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _sosService.dispose();
    super.dispose();
  }
}
