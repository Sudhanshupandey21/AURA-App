import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'step_indicator_model.dart';
export 'step_indicator_model.dart';

class StepIndicatorWidget extends StatefulWidget {
  const StepIndicatorWidget({
    super.key,
    String? activeStep,
  }) : activeStep = activeStep ?? 'option_2';

  final String activeStep;

  @override
  State<StepIndicatorWidget> createState() => _StepIndicatorWidgetState();
}

class _StepIndicatorWidgetState extends State<StepIndicatorWidget> {
  late StepIndicatorModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StepIndicatorModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Container(
          width: widget.activeStep == 'option_1' ? 32.0 : 8.0,
          height: 8.0,
          decoration: BoxDecoration(
            color: widget.activeStep == 'option_1'
                ? FlutterFlowTheme.of(context).primary
                : FlutterFlowTheme.of(context).surfaceVariant,
            borderRadius: BorderRadius.circular(9999.0),
            shape: BoxShape.rectangle,
          ),
        ),
        Container(
          width: () {
            if (widget.activeStep == 'option_1') {
              return 8.0;
            } else if (widget.activeStep == 'option_3') {
              return 8.0;
            } else {
              return 32.0;
            }
          }(),
          height: 8.0,
          decoration: BoxDecoration(
            color: () {
              if (widget.activeStep == 'option_1') {
                return FlutterFlowTheme.of(context).surfaceVariant;
              } else if (widget.activeStep == 'option_3') {
                return FlutterFlowTheme.of(context).surfaceVariant;
              } else {
                return FlutterFlowTheme.of(context).primary;
              }
            }(),
            borderRadius: BorderRadius.circular(9999.0),
            shape: BoxShape.rectangle,
          ),
        ),
        Container(
          width: widget.activeStep == 'option_3' ? 32.0 : 8.0,
          height: 8.0,
          decoration: BoxDecoration(
            color: widget.activeStep == 'option_3'
                ? FlutterFlowTheme.of(context).primary
                : FlutterFlowTheme.of(context).surfaceVariant,
            borderRadius: BorderRadius.circular(9999.0),
            shape: BoxShape.rectangle,
          ),
        ),
      ].divide(const SizedBox(width: 8.0)),
    );
  }
}
