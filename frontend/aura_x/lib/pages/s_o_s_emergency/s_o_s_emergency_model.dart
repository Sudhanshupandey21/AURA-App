import '/components/button/button_widget.dart';
import '/components/emergency_stat_card/emergency_stat_card_widget.dart';
import '/components/pulsing_sos_button/pulsing_sos_button_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 's_o_s_emergency_widget.dart' show SOSEmergencyWidget;
import 'package:flutter/material.dart';

class SOSEmergencyModel extends FlutterFlowModel<SOSEmergencyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for PulsingSosButton.
  late PulsingSosButtonModel pulsingSosButtonModel;
  // Model for EmergencyStatCard.
  late EmergencyStatCardModel emergencyStatCardModel1;
  // Model for EmergencyStatCard.
  late EmergencyStatCardModel emergencyStatCardModel2;
  // Model for EmergencyStatCard.
  late EmergencyStatCardModel emergencyStatCardModel3;
  // Model for Button.
  late ButtonModel buttonModel1;
  // Model for Button.
  late ButtonModel buttonModel2;

  @override
  void initState(BuildContext context) {
    pulsingSosButtonModel = createModel(context, () => PulsingSosButtonModel());
    emergencyStatCardModel1 =
        createModel(context, () => EmergencyStatCardModel());
    emergencyStatCardModel2 =
        createModel(context, () => EmergencyStatCardModel());
    emergencyStatCardModel3 =
        createModel(context, () => EmergencyStatCardModel());
    buttonModel1 = createModel(context, () => ButtonModel());
    buttonModel2 = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    pulsingSosButtonModel.dispose();
    emergencyStatCardModel1.dispose();
    emergencyStatCardModel2.dispose();
    emergencyStatCardModel3.dispose();
    buttonModel1.dispose();
    buttonModel2.dispose();
  }
}
