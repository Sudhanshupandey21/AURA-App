import '/components/button/button_widget.dart';
import '/components/onboarding_step/onboarding_step_widget.dart';
import '/components/step_indicator/step_indicator_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'onboarding_widget.dart' show OnboardingWidget;
import 'package:flutter/material.dart';

class OnboardingModel extends FlutterFlowModel<OnboardingWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for Button.
  late ButtonModel buttonModel1;
  // Model for OnboardingStep.
  late OnboardingStepModel onboardingStepModel;
  // Model for StepIndicator.
  late StepIndicatorModel stepIndicatorModel;
  // Model for Button.
  late ButtonModel buttonModel2;

  @override
  void initState(BuildContext context) {
    buttonModel1 = createModel(context, () => ButtonModel());
    onboardingStepModel = createModel(context, () => OnboardingStepModel());
    stepIndicatorModel = createModel(context, () => StepIndicatorModel());
    buttonModel2 = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    buttonModel1.dispose();
    onboardingStepModel.dispose();
    stepIndicatorModel.dispose();
    buttonModel2.dispose();
  }
}
