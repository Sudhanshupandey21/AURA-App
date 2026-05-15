import '/components/button/button_widget.dart';
import '/components/risk_badge2/risk_badge2_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'hud_card_child7_widget.dart' show HudCardChild7Widget;
import 'package:flutter/material.dart';

class HudCardChild7Model extends FlutterFlowModel<HudCardChild7Widget> {
  ///  State fields for stateful widgets in this component.

  // Model for RiskBadge2.
  late RiskBadge2Model riskBadge2Model;
  // Model for Button.
  late ButtonModel buttonModel;

  @override
  void initState(BuildContext context) {
    riskBadge2Model = createModel(context, () => RiskBadge2Model());
    buttonModel = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    riskBadge2Model.dispose();
    buttonModel.dispose();
  }
}
