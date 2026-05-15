import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'pulsing_sos_button_model.dart';
export 'pulsing_sos_button_model.dart';

class PulsingSosButtonWidget extends StatefulWidget {
  const PulsingSosButtonWidget({super.key});

  @override
  State<PulsingSosButtonWidget> createState() => _PulsingSosButtonWidgetState();
}

class _PulsingSosButtonWidgetState extends State<PulsingSosButtonWidget> {
  late PulsingSosButtonModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => PulsingSosButtonModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 280.0,
      height: 280.0,
      child: Stack(
        alignment: const AlignmentDirectional(0.0, 0.0),
        children: [
          Container(
            width: 280.0,
            height: 280.0,
            decoration: BoxDecoration(
              color: const Color(0x1AFF0000),
              borderRadius: BorderRadius.circular(9999.0),
              shape: BoxShape.rectangle,
              border: Border.all(
                color: const Color(0x33FF0000),
                width: 2.0,
              ),
            ),
          ),
          Align(
            alignment: const AlignmentDirectional(0.0, 0.0),
            child: Container(
              width: 240.0,
              height: 240.0,
              decoration: BoxDecoration(
                color: const Color(0x26FF0000),
                borderRadius: BorderRadius.circular(9999.0),
                shape: BoxShape.rectangle,
                border: Border.all(
                  color: const Color(0x4DFF0000),
                  width: 1.0,
                ),
              ),
            ),
          ),
          Container(
            width: 200.0,
            height: 200.0,
            decoration: BoxDecoration(
              boxShadow: const [
                BoxShadow(
                  blurRadius: 40.0,
                  color: Color(0x66FF0000),
                  offset: Offset(
                    0.0,
                    0.0,
                  ),
                  spreadRadius: 10.0,
                )
              ],
              gradient: const RadialGradient(
                colors: [Color(0xFFFF1744), Color(0xFFB71C1C)],
                stops: [0.0, 1.0],
                center: Alignment(0.0, 0.0),
                radius: 0.5,
              ),
              borderRadius: BorderRadius.circular(9999.0),
              shape: BoxShape.rectangle,
            ),
            alignment: const AlignmentDirectional(0.0, 0.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Lottie.asset(
                  'assets/lottie/ripple_pulse.json',
                  width: 80.0,
                  height: 80.0,
                  fit: BoxFit.contain,
                  animate: true,
                ),
                Text(
                  'SOS',
                  style: FlutterFlowTheme.of(context).headlineLarge.override(
                        font: TextStyle(
                          fontFamily: 'Orbitron',
                          fontWeight: FontWeight.w900,
                          fontStyle: FlutterFlowTheme.of(context)
                              .headlineLarge
                              .fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).onPrimaryContainer,
                        letterSpacing: 0.0,
                        fontWeight: FontWeight.w900,
                        fontStyle: FlutterFlowTheme.of(context)
                            .headlineLarge
                            .fontStyle,
                        lineHeight: 1.2,
                      ),
                ),
              ].divide(const SizedBox(height: 4.0)),
            ),
          ),
        ],
      ),
    );
  }
}
