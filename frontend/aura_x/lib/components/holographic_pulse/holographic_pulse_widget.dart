import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'holographic_pulse_model.dart';
export 'holographic_pulse_model.dart';

class HolographicPulseWidget extends StatefulWidget {
  const HolographicPulseWidget({super.key});

  @override
  State<HolographicPulseWidget> createState() => _HolographicPulseWidgetState();
}

class _HolographicPulseWidgetState extends State<HolographicPulseWidget>
    with SingleTickerProviderStateMixin {
  late HolographicPulseModel _model;
  late AnimationController _animationController;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HolographicPulseModel());

    // Initialize animation controller for smooth pulse effect
    _animationController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _model.maybeDispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: SizedBox(
        width: 280.0,
        height: 280.0,
        child: Stack(
          alignment: const AlignmentDirectional(0.0, 0.0),
          children: [
            _buildCircleBorder(280.0, 0.3),
            _buildCircleBorder(200.0, 0.6),
            _buildInnerCircle(),
          ],
        ),
      ),
    );
  }

  Widget _buildCircleBorder(double size, double opacity) {
    return Opacity(
      opacity: opacity,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(9999.0),
          shape: BoxShape.rectangle,
          border: Border.all(
            color: size == 280.0
                ? FlutterFlowTheme.of(context).primary20
                : FlutterFlowTheme.of(context).primary40,
            width: size == 280.0 ? 1.0 : 2.0,
          ),
        ),
      ),
    );
  }

  Widget _buildInnerCircle() {
    return AnimatedBuilder(
      animation: _animationController,
      builder: (context, child) {
        return Transform.scale(
          scale: 0.9 + (0.1 * _animationController.value),
          child: child,
        );
      },
      child: Container(
        width: 120.0,
        height: 120.0,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(9999.0),
          shape: BoxShape.rectangle,
          color: FlutterFlowTheme.of(context).primary20,
          border: Border.all(
            color: FlutterFlowTheme.of(context).primary,
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              blurRadius: 15.0,
              color: FlutterFlowTheme.of(context).primary.withOpacity(0.5),
              spreadRadius: 1.0,
            )
          ],
        ),
      ),
    );
  }
}
