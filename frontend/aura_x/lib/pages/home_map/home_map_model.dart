import '/components/button/button_widget.dart';
import '/components/hud_card/hud_card_widget.dart';
import '/components/map_action/map_action_widget.dart';
import '/components/risk_badge/risk_badge_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'home_map_widget.dart' show HomeMapWidget;
import 'package:flutter/material.dart';

class HomeMapModel extends FlutterFlowModel<HomeMapWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for HudCard.
  late HudCardModel hudCardModel1;
  // Model for RiskBadge.
  late RiskBadgeModel riskBadgeModel;
  // Model for MapAction.
  late MapActionModel mapActionModel1;
  // Model for MapAction.
  late MapActionModel mapActionModel2;
  // Model for MapAction.
  late MapActionModel mapActionModel3;
  // Model for HudCard.
  late HudCardModel hudCardModel2;
  // Model for Button.
  late ButtonModel buttonModel;
  // Model for HudCard.
  late HudCardModel hudCardModel3;

  @override
  void initState(BuildContext context) {
    hudCardModel1 = createModel(context, () => HudCardModel());
    riskBadgeModel = createModel(context, () => RiskBadgeModel());
    mapActionModel1 = createModel(context, () => MapActionModel());
    mapActionModel2 = createModel(context, () => MapActionModel());
    mapActionModel3 = createModel(context, () => MapActionModel());
    hudCardModel2 = createModel(context, () => HudCardModel());
    buttonModel = createModel(context, () => ButtonModel());
    hudCardModel3 = createModel(context, () => HudCardModel());
  }

  @override
  void dispose() {
    hudCardModel1.dispose();
    riskBadgeModel.dispose();
    mapActionModel1.dispose();
    mapActionModel2.dispose();
    mapActionModel3.dispose();
    hudCardModel2.dispose();
    buttonModel.dispose();
    hudCardModel3.dispose();
  }
}
