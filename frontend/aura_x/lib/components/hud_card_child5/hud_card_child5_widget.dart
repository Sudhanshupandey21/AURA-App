import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'hud_card_child5_model.dart';
export 'hud_card_child5_model.dart';

class HudCardChild5Widget extends StatefulWidget {
  const HudCardChild5Widget({super.key});

  @override
  State<HudCardChild5Widget> createState() => _HudCardChild5WidgetState();
}

class _HudCardChild5WidgetState extends State<HudCardChild5Widget> {
  late HudCardChild5Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild5Model());
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
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Icon(
          Icons.light_mode_rounded,
          color: FlutterFlowTheme.of(context).warning,
          size: 20.0,
        ),
        Text(
          '85%',
          style: FlutterFlowTheme.of(context).labelSmall.override(
                font: TextStyle(
                  fontFamily: 'Orbitron',
                  fontWeight:
                      FlutterFlowTheme.of(context).labelSmall.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).primaryText,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).labelSmall.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                lineHeight: 1.2,
              ),
        ),
        Text(
          'LUX',
          style: FlutterFlowTheme.of(context).bodyMedium.override(
                font: TextStyle(
                  fontFamily: 'Inter',
                  fontWeight:
                      FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).secondaryText,
                fontSize: 10.0,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                lineHeight: 1.5,
              ),
        ),
      ].divide(const SizedBox(height: 4.0)),
    );
  }
}
