import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';

typedef SpeechResultCallback = void Function(
    String recognizedText, bool isFinal);
typedef SpeechStatusCallback = void Function(String status);
typedef SpeechErrorCallback = void Function(String error);
typedef SpeechSoundLevelCallback = void Function(double level);

class SpeechService {
  final SpeechToText _speech = SpeechToText();
  bool _available = false;
  bool get available => _available;
  bool _listening = false;
  bool get isListening => _listening;
  bool _initialized = false;
  bool get initialized => _initialized;
  double lastSoundLevel = 0.0;

  SpeechResultCallback? onResult;
  SpeechStatusCallback? onStatus;
  SpeechErrorCallback? onError;
  SpeechSoundLevelCallback? onSoundLevel;

  void _log(String message) {
    debugPrint('SpeechService: $message');
  }

  Future<bool> initialize() async {
    if (_initialized) {
      return _available;
    }

    _available = await _speech.initialize(
      onStatus: _handleStatus,
      onError: _handleError,
      debugLogging: false,
      options: [
        SpeechToText.androidIntentLookup,
        SpeechToText.androidNoBluetooth,
      ],
    );

    _initialized = true;
    return _available;
  }

  Future<void> startListening() async {
    if (!_initialized) {
      await initialize();
    }

    if (!_available || _listening || _speech.isListening) {
      _log(
          'startListening skipped: available=$_available, listening=$_listening, speech.isListening=${_speech.isListening}');
      return;
    }

    try {
      _log('microphone started');
      await _speech.listen(
        onResult: _onRecognitionResult,
        listenFor: const Duration(minutes: 5),
        pauseFor: const Duration(seconds: 60),
        localeId: 'en_US',
        onSoundLevelChange: _onSoundLevelChanged,
        listenOptions: SpeechListenOptions(
          cancelOnError: false,
          listenMode: ListenMode.search,
          partialResults: true,
        ),
      );
      _listening = true;
      onStatus?.call('listening');
    } catch (e) {
      _log('Speech listen failed: $e');
      _listening = false;
      onError?.call('Speech listen failed: $e');
    }
  }

  Future<void> stopListening() async {
    if (!_available) {
      return;
    }

    try {
      _log('microphone stopped');
      await _speech.stop();
    } catch (_) {
      _log('stop failed, canceling listen()');
      await _speech.cancel();
    }

    _listening = false;
    onStatus?.call('notListening');
  }

  Future<void> cancelListening() async {
    if (!_available) {
      return;
    }

    try {
      _log('canceling listen()');
      await _speech.cancel();
    } catch (_) {
      _log('cancel failed');
    }

    _listening = false;
    onStatus?.call('notListening');
  }

  void _onRecognitionResult(SpeechRecognitionResult result) {
    _log('speech recognized: "${result.recognizedWords}"');
    onResult?.call(result.recognizedWords.trim(), result.finalResult);
  }

  void _handleStatus(String status) {
    _log('status: $status');
    if (status == 'notListening' || status == 'done') {
      _listening = false;
    }
    onStatus?.call(status);
  }

  void _handleError(SpeechRecognitionError error) {
    _log('error: ${error.errorMsg}');
    _listening = false;
    onError?.call(error.errorMsg);
  }

  void _onSoundLevelChanged(double level) {
    lastSoundLevel = level;
    _log('sound level: $level');
    onSoundLevel?.call(level);
  }
}
