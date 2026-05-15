import 'package:flutter/foundation.dart';
import '../core/services/risk_service.dart';
import '../models/models.dart';

class RiskProvider with ChangeNotifier {
  final RiskService _riskService = RiskService();
  RiskData? _currentRisk;
  bool _isLoading = false;

  RiskData? get currentRisk => _currentRisk;
  bool get isLoading => _isLoading;

  Future<void> predictRisk({
    required String userId,
    required Map<String, double> location,
    Map<String, dynamic>? context,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await _riskService.predictRisk(
        userId: userId,
        location: location,
        context: context,
      );

      _currentRisk = RiskData.fromJson(response);
    } catch (e) {
      // Handle error
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<RouteAnalysis?> analyzeRoute({
    required String userId,
    required List<Map<String, double>> routePoints,
    Map<String, dynamic>? preferences,
  }) async {
    try {
      final response = await _riskService.analyzeRoute(
        userId: userId,
        routePoints: routePoints,
        preferences: preferences,
      );

      return RouteAnalysis.fromJson(response);
    } catch (e) {
      return null;
    }
  }

  @override
  void dispose() {
    _riskService.dispose();
    super.dispose();
  }
}
