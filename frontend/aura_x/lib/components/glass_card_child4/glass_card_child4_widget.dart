import '/components/setting_toggle/setting_toggle_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'glass_card_child4_model.dart';
export 'glass_card_child4_model.dart';

class GlassCardChild4Widget extends StatefulWidget {
  const GlassCardChild4Widget({super.key});

  @override
  State<GlassCardChild4Widget> createState() => _GlassCardChild4WidgetState();
}

class _GlassCardChild4WidgetState extends State<GlassCardChild4Widget> {
  late GlassCardChild4Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCardChild4Model());
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
          model: _model.settingToggleModel1,
          updateCallback: () => safeSetState(() {}),
          child: const SettingToggleWidget(
            active: true,
            subtitle: 'Monitors heart rate via wearable',
            title: 'Biometric Distress Detection',
          ),
        ),
        Divider(
          height: 16.0,
          thickness: 1.0,
          indent: 0.0,
          endIndent: 0.0,
          color: FlutterFlowTheme.of(context).divider20,
        ),
        wrapWithModel(
          model: _model.settingToggleModel2,
          updateCallback: () => safeSetState(() {}),
          child: const SettingToggleWidget(
            active: true,
            subtitle: 'Listen for screams or glass breaking',
            title: 'Acoustic Threat Analysis',
          ),
        ),
        Divider(
          height: 16.0,
          thickness: 1.0,
          indent: 0.0,
          endIndent: 0.0,
          color: FlutterFlowTheme.of(context).divider20,
        ),
        wrapWithModel(
          model: _model.settingToggleModel3,
          updateCallback: () => safeSetState(() {}),
          child: const SettingToggleWidget(
            active: false,
            subtitle: 'Auto-SOS on sudden kinetic change',
            title: 'Fall & Impact Detection',
          ),
        ),
      ],
    );
  }
}
