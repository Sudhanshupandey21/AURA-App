import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'package:flutter/material.dart';
import 'hud_card_child3_model.dart';
export 'hud_card_child3_model.dart';

class HudCardChild3Widget extends StatefulWidget {
  const HudCardChild3Widget({super.key});

  @override
  State<HudCardChild3Widget> createState() => _HudCardChild3WidgetState();
}

class _HudCardChild3WidgetState extends State<HudCardChild3Widget> {
  late HudCardChild3Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild3Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 60.0,
      child: Row(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          FlutterFlowIconButton(
            borderRadius: 8.0,
            buttonSize: 44.0,
            fillColor: Colors.transparent,
            icon: Icon(
              Icons.home_rounded,
              color: FlutterFlowTheme.of(context).primary,
              size: 28.0,
            ),
            onPressed: () {
              print('IconButton pressed ...');
            },
          ),
          FlutterFlowIconButton(
            borderRadius: 8.0,
            buttonSize: 44.0,
            fillColor: Colors.transparent,
            icon: Icon(
              Icons.directions_rounded,
              color: FlutterFlowTheme.of(context).secondaryText,
              size: 28.0,
            ),
            onPressed: () async {
              context.goNamed(RouteComparisonWidget.routeName);
            },
          ),
          FlutterFlowIconButton(
            borderRadius: 8.0,
            buttonSize: 44.0,
            fillColor: Colors.transparent,
            icon: Icon(
              Icons.report_problem_rounded,
              color: FlutterFlowTheme.of(context).secondaryText,
              size: 28.0,
            ),
            onPressed: () async {
              context.goNamed(IncidentReportingWidget.routeName);
            },
          ),
          FlutterFlowIconButton(
            borderRadius: 8.0,
            buttonSize: 44.0,
            fillColor: Colors.transparent,
            icon: Icon(
              Icons.person_rounded,
              color: FlutterFlowTheme.of(context).secondaryText,
              size: 28.0,
            ),
            onPressed: () async {
              context.goNamed(ProfileSafetyAnalyticsWidget.routeName);
            },
          ),
        ],
      ),
    );
  }
}
