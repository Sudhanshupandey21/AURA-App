import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'voice_assistant_service.dart';

class AiAssistantOverlay extends StatelessWidget {
  const AiAssistantOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    final assistant = context.watch<VoiceAssistantService>();
    return Positioned.fill(
      child: Material(
        color: Colors.transparent,
        child: IgnorePointer(
          ignoring: false,
          child: Stack(
            children: [
              if (!assistant.closed &&
                  (assistant.assistantActive || assistant.processing))
                Positioned(
                  top: 20,
                  right: 20,
                  child: _buildStatusCard(context, assistant),
                ),
              Positioned(
                bottom: 24,
                right: 20,
                child: _buildActionButton(context, assistant),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusCard(
      BuildContext context, VoiceAssistantService assistant) {
    final theme = Theme.of(context);
    return Container(
      width: 300,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color.fromRGBO(0, 0, 0, 0.75),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: const Color.fromRGBO(0, 255, 255, 0.8),
          width: 1.4,
        ),
        boxShadow: const [
          BoxShadow(
            color: Color.fromRGBO(0, 255, 255, 0.28),
            blurRadius: 16,
            spreadRadius: 1,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 10,
                height: 10,
                decoration: BoxDecoration(
                  color: assistant.assistantActive
                      ? Colors.greenAccent
                      : Colors.deepPurpleAccent,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  'AURA ASSISTANT',
                  style: theme.textTheme.labelLarge?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.1,
                  ),
                ),
              ),
              IconButton(
                visualDensity: VisualDensity.compact,
                padding: EdgeInsets.zero,
                icon: const Icon(
                  Icons.close,
                  color: Colors.white70,
                  size: 22,
                ),
                onPressed: assistant.closeAssistant,
              ),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            assistant.statusText,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: Colors.white70,
            ),
          ),
          const SizedBox(height: 10),
          Visibility(
            visible: assistant.processing,
            child: Text(
              assistant.processing ? 'Processing command...' : '',
              style: theme.textTheme.bodySmall?.copyWith(
                color: Colors.cyanAccent,
              ),
            ),
          ),
          const SizedBox(height: 14),
          _buildWaveform(assistant.soundLevel),
          const SizedBox(height: 12),
          if (assistant.recognizedText.isNotEmpty)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Heard:',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: Colors.white60,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  assistant.recognizedText,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 12),
              ],
            ),
          Text(
            assistant.assistantResponse,
            maxLines: 3,
            overflow: TextOverflow.ellipsis,
            style: theme.textTheme.bodySmall?.copyWith(
              color: Colors.cyanAccent,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWaveform(double level) {
    final bars = List<Widget>.generate(5, (index) {
      final height = 8.0 + (level * 3).clamp(0, 40) * ((index + 1) / 5);
      return AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        margin: const EdgeInsets.symmetric(horizontal: 2),
        width: 6,
        height: height,
        decoration: BoxDecoration(
          color: Colors.cyanAccent,
          borderRadius: BorderRadius.circular(3),
        ),
      );
    });
    return Row(children: bars);
  }

  Widget _buildActionButton(
      BuildContext context, VoiceAssistantService assistant) {
    return AvatarGlow(
      endRadius: 80.0,
      animate: assistant.assistantActive || assistant.listening,
      glowColor: Colors.cyanAccent,
      duration: const Duration(milliseconds: 2000),
      repeat: true,
      showTwoGlows: true,
      child: GestureDetector(
        onTap: assistant.toggleAssistant,
        child: Container(
          width: 66,
          height: 66,
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFF03E8F5), Color(0xFF7B44FF)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            boxShadow: const [
              BoxShadow(
                color: Color.fromRGBO(0, 255, 255, 0.5),
                blurRadius: 20,
                spreadRadius: 2,
              ),
            ],
            borderRadius: BorderRadius.circular(36),
          ),
          child: Center(
            child: Icon(
              assistant.assistantActive ? Icons.mic : Icons.mic_none,
              color: Colors.white,
              size: 30,
            ),
          ),
        ),
      ),
    );
  }
}
