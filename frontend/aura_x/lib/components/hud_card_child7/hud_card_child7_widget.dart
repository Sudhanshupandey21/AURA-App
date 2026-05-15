import '/components/button/button_widget.dart';
import '/components/risk_badge2/risk_badge2_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'hud_card_child7_model.dart';
export 'hud_card_child7_model.dart';

class HudCardChild7Widget extends StatefulWidget {
  const HudCardChild7Widget({super.key});

  @override
  State<HudCardChild7Widget> createState() => _HudCardChild7WidgetState();
}

class _HudCardChild7WidgetState extends State<HudCardChild7Widget> {
  late HudCardChild7Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild7Model());
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
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        wrapWithModel(
          model: _model.riskBadge2Model,
          updateCallback: () => safeSetState(() {}),
          child: RiskBadge2Widget(
            color: FlutterFlowTheme.of(context).error,
            icon: Icon(
              Icons.warning_rounded,
              color: FlutterFlowTheme.of(context).error,
              size: 14.0,
            ),
            label: 'DANGER ZONE AHEAD',
          ),
        ),
        Text(
          'Unlit alleyway detected in 150m',
          maxLines: 2,
          style: FlutterFlowTheme.of(context).bodySmall.override(
                font: TextStyle(
                  fontFamily: 'Inter',
                  fontWeight: FlutterFlowTheme.of(context).bodySmall.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).bodySmall.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).primaryText,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).bodySmall.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).bodySmall.fontStyle,
                lineHeight: 1.5,
              ),
        ),
        wrapWithModel(
          model: _model.buttonModel,
          updateCallback: () => safeSetState(() {}),
          child: ButtonWidget(
            content: 'Reroute Now',
            icon: Icon(
              Icons.alt_route_rounded,
              color: FlutterFlowTheme.of(context).onError,
              size: 16.0,
            ),
            iconPresent: true,
            iconEndPresent: false,
            variant: 'destructive',
            size: 'small',
            fullWidth: false,
            loading: false,
            disabled: false,
          ),
        ),
      ].divide(const SizedBox(height: 8.0)),
    );
  }
}
