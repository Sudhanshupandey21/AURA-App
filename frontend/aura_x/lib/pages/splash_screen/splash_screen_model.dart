import '/components/button/button_widget.dart';
import '/components/holographic_pulse/holographic_pulse_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'splash_screen_widget.dart' show SplashScreenWidget;
import 'package:flutter/material.dart';

class SplashScreenModel extends FlutterFlowModel<SplashScreenWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for HolographicPulse.
  late HolographicPulseModel holographicPulseModel;
  // Model for Button.
  late ButtonModel buttonModel;

  @override
  void initState(BuildContext context) {
    holographicPulseModel = createModel(context, () => HolographicPulseModel());
    buttonModel = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    holographicPulseModel.dispose();
    buttonModel.dispose();
  }
}
