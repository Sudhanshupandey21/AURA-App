import '/components/nav_step/nav_step_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'hud_card_child4_model.dart';
export 'hud_card_child4_model.dart';

class HudCardChild4Widget extends StatefulWidget {
  const HudCardChild4Widget({super.key});

  @override
  State<HudCardChild4Widget> createState() => _HudCardChild4WidgetState();
}

class _HudCardChild4WidgetState extends State<HudCardChild4Widget> {
  late HudCardChild4Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild4Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        wrapWithModel(
          model: _model.navStepModel,
          updateCallback: () => safeSetState(() {}),
          child: NavStepWidget(
            bg: FlutterFlowTheme.of(context).primary,
            distance: '250m',
            icon: Icon(
              Icons.turn_right_rounded,
              color: FlutterFlowTheme.of(context).onPrimary,
              size: 24.0,
            ),
            instruction: 'Turn right on Lexington Ave',
          ),
        ),
        LinearPercentIndicator(
          percent: 0.65,
          lineHeight: 4.0,
          animation: true,
          animateFromLastPercent: true,
          progressColor: FlutterFlowTheme.of(context).primary,
          backgroundColor: FlutterFlowTheme.of(context).onSurface10,
          barRadius: const Radius.circular(2.0),
          padding: EdgeInsets.zero,
        ),
      ].divide(const SizedBox(height: 16.0)),
    );
  }
}
