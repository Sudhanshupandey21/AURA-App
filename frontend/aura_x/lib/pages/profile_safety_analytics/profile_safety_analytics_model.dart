import '/components/button/button_widget.dart';
import '/components/glass_card2/glass_card2_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'profile_safety_analytics_widget.dart' show ProfileSafetyAnalyticsWidget;
import 'package:flutter/material.dart';

class ProfileSafetyAnalyticsModel
    extends FlutterFlowModel<ProfileSafetyAnalyticsWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for GlassCard2.
  late GlassCard2Model glassCard2Model1;
  // Model for GlassCard2.
  late GlassCard2Model glassCard2Model2;
  // Model for GlassCard2.
  late GlassCard2Model glassCard2Model3;
  // Model for Button.
  late ButtonModel buttonModel1;
  // Model for Button.
  late ButtonModel buttonModel2;

  @override
  void initState(BuildContext context) {
    glassCard2Model1 = createModel(context, () => GlassCard2Model());
    glassCard2Model2 = createModel(context, () => GlassCard2Model());
    glassCard2Model3 = createModel(context, () => GlassCard2Model());
    buttonModel1 = createModel(context, () => ButtonModel());
    buttonModel2 = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    glassCard2Model1.dispose();
    glassCard2Model2.dispose();
    glassCard2Model3.dispose();
    buttonModel1.dispose();
    buttonModel2.dispose();
  }
}
