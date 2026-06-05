import 'dart:convert';

import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

import '/core/config/api_config.dart';
import '/core/providers/navigation_provider.dart';
import '/core/services/route_service.dart';
import '/core/services/websocket_service.dart';
import '/flutter_flow/nav/nav.dart';
import '/pages/home_map/home_map_widget.dart';
import '/pages/route_comparison/route_comparison_widget.dart';

enum VoiceCommand {
  unknown,
  activate,
  sendSos,
  callPolice,
  callEmergencyContact,
  startSafeRoute,
  unsafeAreaAlert,
  stopListening,
  whereAmI,
  navigateHome,
}

class CommandResponse {
  final String message;
  final VoiceCommand command;
  final bool success;

  const CommandResponse({
    required this.message,
    required this.command,
    required this.success,
  });
}

class CommandProcessor {
  final http.Client _client = http.Client();
  final WebSocketService _wsService = WebSocketService();
  final RouteService _routeService = RouteService();
  DateTime? _lastCommandAt;
  VoiceCommand? _lastCommand;

  String _normalize(String value) {
    return value
        .toLowerCase()
        .replaceAll(RegExp(r'[^a-z0-9 ]'), ' ')
        .replaceAll(RegExp(r'\s+'), ' ')
        .trim();
  }

  bool _hasToken(Set<String> tokens, String target) {
    if (tokens.contains(target)) {
      return true;
    }

    return tokens.any((token) {
      if ((token.length - target.length).abs() > 2) {
        return false;
      }
      return _levenshtein(token, target) <= (target.length <= 4 ? 1 : 2);
    });
  }

  int _levenshtein(String a, String b) {
    if (a == b) {
      return 0;
    }
    if (a.isEmpty) {
      return b.length;
    }
    if (b.isEmpty) {
      return a.length;
    }

    final previous = List<int>.generate(b.length + 1, (index) => index);
    final current = List<int>.filled(b.length + 1, 0);

    for (var i = 0; i < a.length; i++) {
      current[0] = i + 1;
      for (var j = 0; j < b.length; j++) {
        final cost = a.codeUnitAt(i) == b.codeUnitAt(j) ? 0 : 1;
        current[j + 1] = [
          current[j] + 1,
          previous[j + 1] + 1,
          previous[j] + cost,
        ].reduce((value, element) => value < element ? value : element);
      }
      for (var j = 0; j < previous.length; j++) {
        previous[j] = current[j];
      }
    }

    return previous[b.length];
  }

  VoiceCommand parseCommand(String transcript) {
    final normalized = _normalize(transcript);
    final tokens =
        normalized.split(' ').where((token) => token.isNotEmpty).toSet();

    bool phrase(List<String> terms) => terms.any(normalized.contains);
    bool word(List<String> terms) =>
        terms.any((term) => _hasToken(tokens, term));
    bool hasIntent(List<String> terms) => phrase(terms) || word(terms);

    if (phrase([
          'stop listening',
          'stop assistant',
          'close assistant',
          'pause assistant',
          'shut down assistant',
        ]) ||
        word(['deactivate', 'sleep', 'stop', 'close'])) {
      return VoiceCommand.stopListening;
    }

    if (word(['aura', 'ora', 'aurah']) ||
        (word(['assistant']) && word(['activate', 'start', 'wake', 'open']))) {
      return VoiceCommand.activate;
    }

    if (phrase(['emergency contact', 'trusted contact']) ||
        (word(['contact', 'guardian', 'family']) &&
            word(['call', 'dial', 'phone']))) {
      return VoiceCommand.callEmergencyContact;
    }

    if (hasIntent(['police', 'cop', 'cops', '911', 'help'])) {
      return VoiceCommand.callPolice;
    }

    if (hasIntent(['sos', 's o s', 'emergency', 'save me', 'send help'])) {
      return VoiceCommand.sendSos;
    }

    if (phrase(['unsafe area', 'danger zone', 'unsafe area alert']) ||
        word(['danger', 'risk', 'unsafe', 'alert', 'scan'])) {
      return VoiceCommand.unsafeAreaAlert;
    }

    if (phrase([
          'safe route',
          'safest route',
          'navigation route',
          'start route',
          'route analysis',
        ]) ||
        (word(['route', 'navigate', 'navigation']) &&
            word(['safe', 'safest']))) {
      return VoiceCommand.startSafeRoute;
    }

    if (phrase(['navigate to home', 'go home', 'home route', 'take me home'])) {
      return VoiceCommand.navigateHome;
    }

    if (phrase(
        ['where am i', 'my location', 'location is', 'current location'])) {
      return VoiceCommand.whereAmI;
    }

    return VoiceCommand.unknown;
  }

  Future<CommandResponse> execute(String transcript) async {
    final command = parseCommand(transcript);

    if (command == VoiceCommand.unknown) {
      return const CommandResponse(
        message: 'Unknown command',
        command: VoiceCommand.unknown,
        success: false,
      );
    }

    if (_lastCommandAt != null &&
        _lastCommand == command &&
        DateTime.now().difference(_lastCommandAt!) <
            const Duration(seconds: 3)) {
      return CommandResponse(
        message: '',
        command: command,
        success: true,
      );
    }
    _lastCommandAt = DateTime.now();
    _lastCommand = command;

    switch (command) {
      case VoiceCommand.activate:
        return const CommandResponse(
          message: 'Aura assistant activated',
          command: VoiceCommand.activate,
          success: true,
        );
      case VoiceCommand.sendSos:
        return await _sendSos();
      case VoiceCommand.callPolice:
        return await _callPolice();
      case VoiceCommand.callEmergencyContact:
        return await _callEmergencyContact();
      case VoiceCommand.startSafeRoute:
        return await _startSafeRoute();
      case VoiceCommand.navigateHome:
        return await _navigateHome();
      case VoiceCommand.whereAmI:
        return await _whereAmI();
      case VoiceCommand.unsafeAreaAlert:
        return await _unsafeAreaAlert();
      case VoiceCommand.stopListening:
        return const CommandResponse(
          message: 'Stopped listening.',
          command: VoiceCommand.stopListening,
          success: true,
        );
      case VoiceCommand.unknown:
        return const CommandResponse(
          message: 'Unknown command',
          command: VoiceCommand.unknown,
          success: false,
        );
    }
  }

  Future<Position?> _getCurrentPosition() async {
    try {
      final serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        return null;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        return null;
      }
      return await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
    } catch (_) {
      return null;
    }
  }

  Future<bool> _openPhoneDialer(String phoneNumber) async {
    final sanitized = phoneNumber.replaceAll(RegExp(r'[^0-9+]'), '');
    if (sanitized.isEmpty) {
      return false;
    }
    final uri = Uri(scheme: 'tel', path: sanitized);
    try {
      return await launchUrl(uri, mode: LaunchMode.externalApplication);
    } catch (_) {
      if (!await canLaunchUrl(uri)) {
        return false;
      }
      await launchUrl(uri, mode: LaunchMode.externalApplication);
      return true;
    }
  }

  Future<String> _loadEmergencyContact() async {
    final prefs = await SharedPreferences.getInstance();
    final contact = prefs.getString('emergency_contact_number');
    if (contact != null && contact.isNotEmpty) {
      return contact;
    }
    return '112';
  }

  Future<CommandResponse> _sendSos() async {
    final position = await _getCurrentPosition();
    if (position == null) {
      return const CommandResponse(
        message: 'Unable to access location. SOS failed.',
        command: VoiceCommand.sendSos,
        success: false,
      );
    }

    final payload = {
      'user_id': 'demo_user',
      'timestamp': DateTime.now().toIso8601String(),
      'location': {
        'lat': position.latitude,
        'lng': position.longitude,
      },
      'message': 'SOS alert triggered by voice assistant',
    };

    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.sos}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': payload['user_id'],
          'location': payload['location'],
          'message': payload['message'],
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        _wsService.sendMessage({
          'type': 'sos_alert',
          'user_id': 'demo_user',
          'location': payload['location'],
          'timestamp': payload['timestamp'],
        });
        return const CommandResponse(
          message: 'Emergency SOS sent successfully.',
          command: VoiceCommand.sendSos,
          success: true,
        );
      }
      return const CommandResponse(
        message: 'SOS request failed. Please try again.',
        command: VoiceCommand.sendSos,
        success: false,
      );
    } catch (e) {
      return CommandResponse(
        message: 'SOS request failed: $e',
        command: VoiceCommand.sendSos,
        success: false,
      );
    }
  }

  Future<CommandResponse> _callPolice() async {
    const phoneNumber = '112';
    final launched = await _openPhoneDialer(phoneNumber);
    if (!launched) {
      return const CommandResponse(
        message: 'Unable to launch police dialer.',
        command: VoiceCommand.callPolice,
        success: false,
      );
    }
    return const CommandResponse(
      message: 'Calling police emergency services.',
      command: VoiceCommand.callPolice,
      success: true,
    );
  }

  Future<CommandResponse> _callEmergencyContact() async {
    final contactNumber = await _loadEmergencyContact();
    final launched = await _openPhoneDialer(contactNumber);
    if (!launched) {
      return const CommandResponse(
        message: 'Unable to dial emergency contact.',
        command: VoiceCommand.callEmergencyContact,
        success: false,
      );
    }
    return CommandResponse(
      message: 'Calling emergency contact $contactNumber.',
      command: VoiceCommand.callEmergencyContact,
      success: true,
    );
  }

  Future<CommandResponse> _startSafeRoute() async {
    final position = await _getCurrentPosition();
    if (position == null) {
      return const CommandResponse(
        message: 'Unable to access location. Cannot start safe route.',
        command: VoiceCommand.startSafeRoute,
        success: false,
      );
    }

    final destinationLat = position.latitude + 0.01;
    final destinationLng = position.longitude + 0.01;
    final navigatorState = appNavigatorKey.currentState;
    if (navigatorState == null || !navigatorState.mounted) {
      return const CommandResponse(
        message: 'Unable to start safe route.',
        command: VoiceCommand.startSafeRoute,
        success: false,
      );
    }

    final navigatorContext = navigatorState.context;
    // ignore: use_build_context_synchronously
    final navigationProvider = Provider.of<NavigationProvider>(
      navigatorContext,
      listen: false,
    );

    final routeResponse = await _routeService.analyzeRoute(
      userId: 'demo_user',
      sourceLat: position.latitude,
      sourceLng: position.longitude,
      destLat: destinationLat,
      destLng: destinationLng,
    );

    if (routeResponse['success'] != true) {
      return const CommandResponse(
        message: 'Safe route analysis failed. Please try again.',
        command: VoiceCommand.startSafeRoute,
        success: false,
      );
    }

    await navigationProvider.updateCurrentLocation(position);
    final success = await navigationProvider.startNavigation(
      destLat: destinationLat,
      destLng: destinationLng,
      destinationAddress: 'Safest route',
    );

    if (success) {
      final router = GoRouter.of(navigatorState.context);
      router.go(RouteComparisonWidget.routePath);
      return const CommandResponse(
        message: 'Calculating safest route.',
        command: VoiceCommand.startSafeRoute,
        success: true,
      );
    }

    return const CommandResponse(
      message: 'Unable to start safe route.',
      command: VoiceCommand.startSafeRoute,
      success: false,
    );
  }

  Future<CommandResponse> _navigateHome() async {
    final context = appNavigatorKey.currentContext;
    if (context != null) {
      GoRouter.of(context).go(HomeMapWidget.routePath);
      return const CommandResponse(
        message: 'Navigating home.',
        command: VoiceCommand.navigateHome,
        success: true,
      );
    }
    return const CommandResponse(
      message: 'Unable to navigate home.',
      command: VoiceCommand.navigateHome,
      success: false,
    );
  }

  Future<CommandResponse> _whereAmI() async {
    final position = await _getCurrentPosition();
    if (position == null) {
      return const CommandResponse(
        message: 'Unable to determine your location.',
        command: VoiceCommand.whereAmI,
        success: false,
      );
    }

    return CommandResponse(
      message:
          'You are at latitude ${position.latitude.toStringAsFixed(5)}, longitude ${position.longitude.toStringAsFixed(5)}.',
      command: VoiceCommand.whereAmI,
      success: true,
    );
  }

  Future<CommandResponse> _unsafeAreaAlert() async {
    final position = await _getCurrentPosition();
    if (position == null) {
      return const CommandResponse(
        message: 'Unable to access location. Unsafe area alert failed.',
        command: VoiceCommand.unsafeAreaAlert,
        success: false,
      );
    }

    final payload = {
      'user_id': 'demo_user',
      'timestamp': DateTime.now().toIso8601String(),
      'location': {
        'lat': position.latitude,
        'lng': position.longitude,
      },
      'message': 'Unsafe area alert from voice assistant',
    };

    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.predictRisk}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': payload['user_id'],
          'location': payload['location'],
          'context': {
            'source': 'voice_assistant',
            'trigger': 'unsafe_area_alert',
            'timestamp': payload['timestamp'],
          },
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final riskLevel = data['risk_level'] as String? ?? 'UNKNOWN';
        final recommendation = data['recommendation'] as String? ??
            'Nearby danger zones reported.';
        final message = riskLevel == 'LOW'
            ? 'Area scan complete. Current risk appears low.'
            : 'Unsafe area alert. Risk level $riskLevel. $recommendation';
        _wsService.sendMessage({
          'type': 'risk_alert',
          'user_id': 'demo_user',
          'location': payload['location'],
          'timestamp': payload['timestamp'],
        });
        return CommandResponse(
          message: message,
          command: VoiceCommand.unsafeAreaAlert,
          success: true,
        );
      }

      return const CommandResponse(
        message: 'Unable to send unsafe area alert. Please try again.',
        command: VoiceCommand.unsafeAreaAlert,
        success: false,
      );
    } catch (e) {
      return CommandResponse(
        message: 'Unable to send unsafe area alert: $e',
        command: VoiceCommand.unsafeAreaAlert,
        success: false,
      );
    }
  }

  void dispose() {
    _client.close();
    _wsService.disconnect();
  }
}
