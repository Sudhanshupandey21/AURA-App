import '/components/button/button_widget.dart';
import '/components/reroute_option/reroute_option_widget.dart';
import '/components/risk_stat/risk_stat_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'risk_alert_widget.dart' show RiskAlertWidget;
import 'package:flutter/material.dart';

class RiskAlertModel extends FlutterFlowModel<RiskAlertWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for RiskStat.
  late RiskStatModel riskStatModel1;
  // Model for RiskStat.
  late RiskStatModel riskStatModel2;
  // Model for RiskStat.
  late RiskStatModel riskStatModel3;
  // Model for RerouteOption.
  late RerouteOptionModel rerouteOptionModel1;
  // Model for RerouteOption.
  late RerouteOptionModel rerouteOptionModel2;
  // Model for Button.
  late ButtonModel buttonModel1;
  // Model for Button.
  late ButtonModel buttonModel2;
  // Model for Button.
  late ButtonModel buttonModel3;

  @override
  void initState(BuildContext context) {
    riskStatModel1 = createModel(context, () => RiskStatModel());
    riskStatModel2 = createModel(context, () => RiskStatModel());
    riskStatModel3 = createModel(context, () => RiskStatModel());
    rerouteOptionModel1 = createModel(context, () => RerouteOptionModel());
    rerouteOptionModel2 = createModel(context, () => RerouteOptionModel());
    buttonModel1 = createModel(context, () => ButtonModel());
    buttonModel2 = createModel(context, () => ButtonModel());
    buttonModel3 = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    riskStatModel1.dispose();
    riskStatModel2.dispose();
    riskStatModel3.dispose();
    rerouteOptionModel1.dispose();
    rerouteOptionModel2.dispose();
    buttonModel1.dispose();
    buttonModel2.dispose();
    buttonModel3.dispose();
  }
}
