import '/components/switch_component/switch_component_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'setting_toggle_widget.dart' show SettingToggleWidget;
import 'package:flutter/material.dart';

class SettingToggleModel extends FlutterFlowModel<SettingToggleWidget> {
  ///  State fields for stateful widgets in this component.

  // Model for SwitchComponent.
  late SwitchComponentModel switchComponentModel;

  @override
  void initState(BuildContext context) {
    switchComponentModel = createModel(context, () => SwitchComponentModel());
  }

  @override
  void dispose() {
    switchComponentModel.dispose();
  }
}
