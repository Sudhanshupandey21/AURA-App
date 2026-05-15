import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'incident_type_card_model.dart';
export 'incident_type_card_model.dart';

class IncidentTypeCardWidget extends StatefulWidget {
  const IncidentTypeCardWidget({
    super.key,
    this.icon,
    String? label,
    String? onTap,
    bool? selected,
  })  : label = label ?? 'Harassment',
        onTap = onTap ?? 'On Tap',
        selected = selected ?? true;

  final Widget? icon;
  final String label;
  final String onTap;
  final bool selected;

  @override
  State<IncidentTypeCardWidget> createState() => _IncidentTypeCardWidgetState();
}

class _IncidentTypeCardWidgetState extends State<IncidentTypeCardWidget> {
  late IncidentTypeCardModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => IncidentTypeCardModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: widget.selected
            ? FlutterFlowTheme.of(context).error20
            : FlutterFlowTheme.of(context).secondaryBackground,
        borderRadius: BorderRadius.circular(16.0),
        shape: BoxShape.rectangle,
        border: Border.all(
          color: widget.selected
              ? FlutterFlowTheme.of(context).error
              : FlutterFlowTheme.of(context).alternate,
          width: widget.selected ? 1.0 : 1.0,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Container(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              widget.icon!,
              Text(
                valueOrDefault<String>(
                  widget.label,
                  'Harassment',
                ),
                textAlign: TextAlign.center,
                style: FlutterFlowTheme.of(context).labelMedium.override(
                      font: TextStyle(
                        fontFamily: 'Orbitron',
                        fontWeight:
                            FlutterFlowTheme.of(context).labelMedium.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelMedium.fontStyle,
                      ),
                      color: widget.selected
                          ? FlutterFlowTheme.of(context).error
                          : FlutterFlowTheme.of(context).primaryText,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).labelMedium.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelMedium.fontStyle,
                      lineHeight: 1.3,
                    ),
              ),
            ].divide(const SizedBox(height: 8.0)),
          ),
        ),
      ),
    );
  }
}
