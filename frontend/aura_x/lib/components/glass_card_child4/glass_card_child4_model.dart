import '/components/setting_toggle/setting_toggle_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'glass_card_child4_widget.dart' show GlassCardChild4Widget;
import 'package:flutter/material.dart';

class GlassCardChild4Model extends FlutterFlowModel<GlassCardChild4Widget> {
  ///  State fields for stateful widgets in this component.

  // Model for SettingToggle.
  late SettingToggleModel settingToggleModel1;
  // Model for SettingToggle.
  late SettingToggleModel settingToggleModel2;
  // Model for SettingToggle.
  late SettingToggleModel settingToggleModel3;

  @override
  void initState(BuildContext context) {
    settingToggleModel1 = createModel(context, () => SettingToggleModel());
    settingToggleModel2 = createModel(context, () => SettingToggleModel());
    settingToggleModel3 = createModel(context, () => SettingToggleModel());
  }

  @override
  void dispose() {
    settingToggleModel1.dispose();
    settingToggleModel2.dispose();
    settingToggleModel3.dispose();
  }
}
