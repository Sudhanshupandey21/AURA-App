import '/components/nav_step/nav_step_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'hud_card_child4_widget.dart' show HudCardChild4Widget;
import 'package:flutter/material.dart';

class HudCardChild4Model extends FlutterFlowModel<HudCardChild4Widget> {
  ///  State fields for stateful widgets in this component.

  // Model for NavStep.
  late NavStepModel navStepModel;

  @override
  void initState(BuildContext context) {
    navStepModel = createModel(context, () => NavStepModel());
  }

  @override
  void dispose() {
    navStepModel.dispose();
  }
}
