import '/components/switch_component/switch_component_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'setting_toggle_model.dart';
export 'setting_toggle_model.dart';

class SettingToggleWidget extends StatefulWidget {
  const SettingToggleWidget({
    super.key,
    bool? active,
    String? subtitle,
    String? title,
  })  : active = active ?? true,
        subtitle = subtitle ?? 'Monitors heart rate via wearable',
        title = title ?? 'Biometric Distress Detection';

  final bool active;
  final String subtitle;
  final String title;

  @override
  State<SettingToggleWidget> createState() => _SettingToggleWidgetState();
}

class _SettingToggleWidgetState extends State<SettingToggleWidget> {
  late SettingToggleModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => SettingToggleModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(0.0, 8.0, 0.0, 8.0),
      child: Row(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            flex: 1,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  valueOrDefault<String>(
                    widget.title,
                    'Biometric Distress Detection',
                  ),
                  style: FlutterFlowTheme.of(context).bodyMedium.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight: FontWeight.w500,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).primaryText,
                        letterSpacing: 0.0,
                        fontWeight: FontWeight.w500,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                        lineHeight: 1.5,
                      ),
                ),
                Text(
                  valueOrDefault<String>(
                    widget.subtitle,
                    'Monitors heart rate via wearable',
                  ),
                  maxLines: 1,
                  style: FlutterFlowTheme.of(context).bodySmall.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight:
                              FlutterFlowTheme.of(context).bodySmall.fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).bodySmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        lineHeight: 1.5,
                      ),
                  overflow: TextOverflow.ellipsis,
                ),
              ].divide(const SizedBox(height: 2.0)),
            ),
          ),
          wrapWithModel(
            model: _model.switchComponentModel,
            updateCallback: () => safeSetState(() {}),
            child: SwitchComponentWidget(
              label: '',
              labelPresent: false,
              variant: 'iOS 26+',
              active: valueOrDefault<bool>(
                widget.active,
                true,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
