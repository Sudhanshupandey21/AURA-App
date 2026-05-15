import 'package:flutter/foundation.dart';
import '../core/services/incident_service.dart';
import '../models/models.dart';

class IncidentProvider with ChangeNotifier {
  final IncidentService _incidentService = IncidentService();
  bool _isSubmitting = false;

  bool get isSubmitting => _isSubmitting;

  Future<IncidentReport?> reportIncident({
    required String userId,
    required Map<String, double> location,
    required String type,
    required String description,
    required String severity,
  }) async {
    _isSubmitting = true;
    notifyListeners();

    try {
      final response = await _incidentService.reportIncident(
        userId: userId,
        location: location,
        type: type,
        description: description,
        severity: severity,
      );

      return IncidentReport.fromJson(response);
    } catch (e) {
      return null;
    } finally {
      _isSubmitting = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _incidentService.dispose();
    super.dispose();
  }
}
