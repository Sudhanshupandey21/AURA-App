import '/components/button/button_widget.dart';
import '/components/glass_card/glass_card_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'login_register_widget.dart' show LoginRegisterWidget;
import 'package:flutter/material.dart';

class LoginRegisterModel extends FlutterFlowModel<LoginRegisterWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for GlassCard.
  late GlassCardModel glassCardModel;
  // Model for Button.
  late ButtonModel buttonModel;

  @override
  void initState(BuildContext context) {
    glassCardModel = createModel(context, () => GlassCardModel());
    buttonModel = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    glassCardModel.dispose();
    buttonModel.dispose();
  }
}
