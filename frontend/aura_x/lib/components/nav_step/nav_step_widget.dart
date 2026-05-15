import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'nav_step_model.dart';
export 'nav_step_model.dart';

class NavStepWidget extends StatefulWidget {
  const NavStepWidget({
    super.key,
    Color? bg,
    String? distance,
    this.icon,
    String? instruction,
  })  : bg = bg ?? const Color(0x00000000),
        distance = distance ?? '250m',
        instruction = instruction ?? 'Turn right on Lexington Ave';

  final Color bg;
  final String distance;
  final Widget? icon;
  final String instruction;

  @override
  State<NavStepWidget> createState() => _NavStepWidgetState();
}

class _NavStepWidgetState extends State<NavStepWidget> {
  late NavStepModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => NavStepModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.max,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Container(
          width: 44.0,
          height: 44.0,
          decoration: BoxDecoration(
            color: valueOrDefault<Color>(
              widget.bg,
              FlutterFlowTheme.of(context).primary,
            ),
            borderRadius: BorderRadius.circular(9999.0),
            shape: BoxShape.rectangle,
          ),
          alignment: const AlignmentDirectional(0.0, 0.0),
          child: widget.icon!,
        ),
        Expanded(
          flex: 1,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                valueOrDefault<String>(
                  widget.distance,
                  '250m',
                ),
                style: FlutterFlowTheme.of(context).labelSmall.override(
                      font: TextStyle(
                        fontFamily: 'Orbitron',
                        fontWeight:
                            FlutterFlowTheme.of(context).labelSmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelSmall.fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).secondaryText,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).labelSmall.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelSmall.fontStyle,
                      lineHeight: 1.2,
                    ),
              ),
              Text(
                valueOrDefault<String>(
                  widget.instruction,
                  'Turn right on Lexington Ave',
                ),
                maxLines: 1,
                style: FlutterFlowTheme.of(context).titleMedium.override(
                      font: TextStyle(
                        fontFamily: 'Inter',
                        fontWeight:
                            FlutterFlowTheme.of(context).titleMedium.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).titleMedium.fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).primaryText,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).titleMedium.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).titleMedium.fontStyle,
                      lineHeight: 1.4,
                    ),
                overflow: TextOverflow.ellipsis,
              ),
            ].divide(const SizedBox(height: 2.0)),
          ),
        ),
      ].divide(const SizedBox(width: 16.0)),
    );
  }
}
