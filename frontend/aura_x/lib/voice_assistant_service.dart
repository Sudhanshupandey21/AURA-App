import 'dart:async';

import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';

import '/flutter_flow/nav/nav.dart';
import 'command_processor.dart';
import 'speech_service.dart';
import 'tts_service.dart';

class VoiceAssistantService extends ChangeNotifier {
  final SpeechService _speechService = SpeechService();
  final TtsService _ttsService = TtsService();
  final CommandProcessor _commandProcessor = CommandProcessor();

  bool _initialized = false;
  bool get initialized => _initialized;

  void _log(String message) {
    debugPrint('VoiceAssistantService: $message');
  }

  bool _assistantActive = false;
  bool get assistantActive => _assistantActive;

  bool _listening = false;
  bool get listening => _listening;

  bool _processing = false;
  bool get processing => _processing;

  bool _closed = false;
  bool get closed => _closed;

  String _statusText = 'Say "Aura Activate" to begin.';
  String get statusText => _statusText;

  String _recognizedText = '';
  String get recognizedText => _recognizedText;

  String _assistantResponse = '';
  String get assistantResponse => _assistantResponse;

  double _soundLevel = 0.0;
  double get soundLevel => _soundLevel;

  bool _shouldListen = false;
  bool _manuallyStopping = false;
  Timer? _restartTimer;
  Timer? _commandDebounce;
  DateTime? _lastRestartAttempt;

  VoiceAssistantService() {
    _initialize();
  }

  Future<void> _initialize() async {
    _statusText = 'Initializing voice assistant...';
    notifyListeners();

    final microphoneAllowed = await _ensureMicrophonePermission();
    await _ttsService.initialize();
    final speechReady = microphoneAllowed && await _speechService.initialize();

    _speechService.onResult = _handleSpeechResult;
    _speechService.onStatus = _handleSpeechStatus;
    _speechService.onError = _handleSpeechError;
    _speechService.onSoundLevel = _handleSoundLevel;

    _initialized = true;

    if (speechReady) {
      _closed = false;
      _assistantActive = false;
      _statusText = 'Listening for "Aura Activate"...';
      notifyListeners();
      await _startWakeWordListener();
    } else {
      _closed = true;
      _statusText = microphoneAllowed
          ? 'Speech recognition unavailable.'
          : 'Microphone permission is required.';
      notifyListeners();
    }
  }

  Future<bool> _ensureMicrophonePermission() async {
    final status = await Permission.microphone.status;
    if (status.isGranted) {
      _log('Microphone permission already granted.');
      return true;
    }

    if (status.isPermanentlyDenied) {
      _log('Microphone permission permanently denied.');
      return false;
    }

    final result = await Permission.microphone.request();
    final granted = result.isGranted;
    _log('Microphone permission request result: $result');
    return granted;
  }

  Future<void> _startWakeWordListener() async {
    _shouldListen = true;
    _closed = false;
    _assistantActive = false;
    _processing = false;
    _statusText = 'Listening for "Aura Activate"...';
    _assistantResponse = '';
    _recognizedText = '';
    _log('Starting wake word listener.');
    _updateState();
    await _ensureListening();
  }

  Future<void> _ensureListening({Duration delay = Duration.zero}) async {
    if (!_shouldListen || _manuallyStopping || _speechService.isListening) {
      return;
    }

    _log('Scheduling speech recognition start (delay: $delay).');
    final now = DateTime.now();
    final lastAttempt = _lastRestartAttempt;
    final throttleDelay = lastAttempt == null ||
            now.difference(lastAttempt) > const Duration(milliseconds: 700)
        ? delay
        : const Duration(milliseconds: 700);

    _restartTimer?.cancel();
    _restartTimer = Timer(throttleDelay, () async {
      if (!_shouldListen || _manuallyStopping || _speechService.isListening) {
        return;
      }

      _lastRestartAttempt = DateTime.now();
      _log('Invoking speech startListening()');
      await _speechService.startListening();
    });
  }

  Future<void> _pauseMicForSpeech() async {
    _log('Pausing microphone for speech output.');
    _manuallyStopping = true;
    _restartTimer?.cancel();
    await _speechService.cancelListening();
    _listening = false;
    _manuallyStopping = false;
    _updateState();
  }

  Future<void> _speakAndResume(String message) async {
    if (message.isEmpty) {
      if (_shouldListen) {
        await _ensureListening(delay: const Duration(milliseconds: 250));
      }
      return;
    }

    await _pauseMicForSpeech();
    await _ttsService.speak(message);

    if (_shouldListen && !_closed) {
      await _ensureListening(delay: const Duration(milliseconds: 250));
    }
  }

  void _handleSpeechResult(String recognizedText, bool isFinal) {
    final cleanText = recognizedText.trim();
    _log('Speech recognized: "$cleanText" (final=$isFinal).');
    if (cleanText.isEmpty) {
      return;
    }

    _recognizedText = cleanText;
    _assistantResponse = '';
    _soundLevel = _speechService.lastSoundLevel;
    _updateState();

    if (!_assistantActive) {
      if (_commandProcessor.parseCommand(cleanText) == VoiceCommand.activate) {
        _activateAssistant();
      }
      return;
    }

    if (_processing) {
      return;
    }

    _commandDebounce?.cancel();
    _commandDebounce = Timer(
      isFinal
          ? const Duration(milliseconds: 120)
          : const Duration(milliseconds: 750),
      () => _processCommand(cleanText),
    );
  }

  void _handleSpeechStatus(String status) {
    _log('Speech status update: $status');
    if (status == 'listening') {
      _listening = true;
      _statusText = _assistantActive
          ? 'Listening...'
          : 'Listening for "Aura Activate"...';
      _updateState();
      return;
    }

    if (status == 'notListening' || status == 'done') {
      _listening = false;
      _statusText =
          _assistantActive ? 'Waiting for command...' : 'Ready for wake word.';
      _updateState();
      if (_shouldListen && !_manuallyStopping && !_processing) {
        _ensureListening(delay: const Duration(milliseconds: 350));
      }
    }
  }

  void _handleSpeechError(String error) {
    _log('Speech error: $error');
    _listening = false;
    _processing = false;

    final isRecoverable = error.contains('error_speech_timeout') ||
        error.contains('error_no_match') ||
        error.contains('error_busy') ||
        error.contains('error_client') ||
        error.contains('error_server_disconnected');

    _statusText = isRecoverable
        ? 'Speech timeout, retrying...'
        : 'Speech recognition error.';
    _assistantResponse = isRecoverable ? '' : 'Speech recovery in progress.';
    _updateState();

    if (_shouldListen && !_manuallyStopping) {
      _ensureListening(
          delay: isRecoverable
              ? const Duration(milliseconds: 450)
              : const Duration(seconds: 1));
    }
  }

  void _handleSoundLevel(double level) {
    _soundLevel = level;
    if (_listening || _assistantActive) {
      _updateState();
    }
  }

  Future<void> _activateAssistant() async {
    if (!_initialized) {
      _log('Assistant activation attempted before initialization.');
      _statusText = 'Voice assistant starting...';
      _updateState();
      return;
    }

    if (_processing) {
      return;
    }

    _assistantActive = true;
    _closed = false;
    _shouldListen = true;
    _statusText = 'Aura assistant activated';
    _assistantResponse = 'Listening...';
    _log('Assistant activated.');
    _updateState();

    await _speakAndResume('Aura assistant activated');
    _statusText = 'Listening...';
    _updateState();
  }

  Future<void> closeAssistant() async {
    _shouldListen = false;
    _closed = true;
    _assistantActive = false;
    _processing = false;
    _statusText = 'Assistant closed.';
    _assistantResponse = '';
    _recognizedText = '';
    _restartTimer?.cancel();
    _commandDebounce?.cancel();
    await _pauseMicForSpeech();
    await _ttsService.stop();
    _updateState();
  }

  Future<void> _processCommand(String transcript) async {
    _processing = true;
    _statusText = 'Processing...';
    _assistantResponse = '';
    _updateState();

    await _pauseMicForSpeech();
    final response = await _commandProcessor.execute(transcript);

    if (response.command == VoiceCommand.stopListening) {
      _assistantResponse = response.message;
      _statusText = 'Command recognized';
      _updateState();
      await _ttsService.speak(response.message);
      await closeAssistant();
      return;
    }

    if (!response.success && response.command == VoiceCommand.unknown) {
      _assistantResponse =
          'Command not recognized. Try send SOS, start safe route, call police, call emergency contact, unsafe area alert, or stop listening.';
      _statusText = 'Command not recognized';
      _processing = false;
      _updateState();
      await _speakAndResume(_assistantResponse);
      return;
    }

    _assistantResponse = response.message;
    _statusText = response.success ? 'Command recognized' : 'Processing failed';
    _processing = false;
    _updateState();

    if (response.success) {
      _showSnackBar(response.message);
    }

    await _speakAndResume(response.message);
  }

  void toggleAssistant() {
    if (!_initialized) {
      _log('Voice assistant toggle ignored until initialization completes.');
      _statusText = 'Voice assistant initializing...';
      _updateState();
      return;
    }

    if (_assistantActive) {
      closeAssistant();
    } else {
      _activateAssistant();
    }
  }

  void _showSnackBar(String message) {
    final context = appNavigatorKey.currentContext;
    if (context == null || message.isEmpty) {
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  void _updateState() {
    notifyListeners();
  }

  @override
  void dispose() {
    _shouldListen = false;
    _restartTimer?.cancel();
    _commandDebounce?.cancel();
    _speechService.cancelListening();
    _ttsService.stop();
    _commandProcessor.dispose();
    super.dispose();
  }
}
