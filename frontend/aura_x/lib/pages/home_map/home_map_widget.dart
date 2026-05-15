import '/components/button/button_widget.dart';
import '/components/hud_card/hud_card_widget.dart';
import '/components/hud_card_child/hud_card_child_widget.dart';
import '/components/hud_card_child2/hud_card_child2_widget.dart';
import '/components/hud_card_child3/hud_card_child3_widget.dart';
import '/components/map_action/map_action_widget.dart';
import '/components/aura_live_map.dart';
import '/components/risk_badge/risk_badge_widget.dart';
import 'dart:async';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/core/services/websocket_service.dart';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'home_map_model.dart';
export 'home_map_model.dart';

class HomeMapWidget extends StatefulWidget {
  const HomeMapWidget({super.key});

  static String routeName = 'HomeMap';
  static String routePath = '/homeMap';

  @override
  State<HomeMapWidget> createState() => _HomeMapWidgetState();
}

class _HomeMapWidgetState extends State<HomeMapWidget> {
  static const String _defaultUserId = 'demo_user';
  final WebSocketService _wsService = WebSocketService();
  StreamSubscription<Map<String, dynamic>>? _wsSubscription;
  late HomeMapModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HomeMapModel());
    _initializeRealtime();
  }

  @override
  void dispose() {
    _wsSubscription?.cancel();
    _wsService.disconnect();
    _model.dispose();

    super.dispose();
  }

  Future<void> _initializeRealtime() async {
    await _wsService.connect(_defaultUserId);
    _wsSubscription = _wsService.messages.listen((message) {
      if (!mounted) return;
      final messageText = message['message'] ??
          message['alert'] ??
          message['type'] ??
          message.toString();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Realtime update: $messageText'),
          duration: const Duration(seconds: 4),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        resizeToAvoidBottomInset: false,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: Stack(
          alignment: const AlignmentDirectional(-1.0, -1.0),
          children: [
            const Positioned.fill(
              child: AuraLiveMap(
                userId: _defaultUserId,
                followCurrentLocation: true,
                showStatusPill: true,
                showControls: true,
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, -1.0),
              child: SafeArea(
                child: Container(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Container(
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(4.0),
                            child: wrapWithModel(
                              model: _model.hudCardModel1,
                              updateCallback: () => safeSetState(() {}),
                              child: HudCardWidget(
                                margin: 16.0,
                                padding: 'xs',
                                child: () => const HudCardChildWidget(),
                              ),
                            ),
                          ),
                          wrapWithModel(
                            model: _model.riskBadgeModel,
                            updateCallback: () => safeSetState(() {}),
                            child: const RiskBadgeWidget(
                              label: 'SAFE ZONE',
                              level: 'low',
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(1.0, 0.0),
              child: Container(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Container(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        wrapWithModel(
                          model: _model.mapActionModel1,
                          updateCallback: () => safeSetState(() {}),
                          child: MapActionWidget(
                            icon: Icon(
                              Icons.layers_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
                              size: 22.0,
                            ),
                          ),
                        ),
                        wrapWithModel(
                          model: _model.mapActionModel2,
                          updateCallback: () => safeSetState(() {}),
                          child: MapActionWidget(
                            icon: Icon(
                              Icons.my_location_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
                              size: 22.0,
                            ),
                          ),
                        ),
                        wrapWithModel(
                          model: _model.mapActionModel3,
                          updateCallback: () => safeSetState(() {}),
                          child: MapActionWidget(
                            icon: Icon(
                              Icons.view_in_ar_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
                              size: 22.0,
                            ),
                          ),
                        ),
                      ].divide(const SizedBox(height: 16.0)),
                    ),
                  ),
                ),
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 1.0),
              child: SafeArea(
                child: Container(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Container(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          wrapWithModel(
                            model: _model.hudCardModel2,
                            updateCallback: () => safeSetState(() {}),
                            child: HudCardWidget(
                              margin: 16.0,
                              padding: 'xs',
                              child: () => const HudCardChild2Widget(),
                            ),
                          ),
                          Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Expanded(
                                flex: 1,
                                child: InkWell(
                                  splashColor: Colors.transparent,
                                  focusColor: Colors.transparent,
                                  hoverColor: Colors.transparent,
                                  highlightColor: Colors.transparent,
                                  onTap: () async {
                                    context.goNamed(
                                        RouteComparisonWidget.routeName);
                                  },
                                  child: wrapWithModel(
                                    model: _model.buttonModel,
                                    updateCallback: () => safeSetState(() {}),
                                    child: ButtonWidget(
                                      content: 'START SAFE ROUTE',
                                      icon: Icon(
                                        Icons.navigation_rounded,
                                        color: FlutterFlowTheme.of(context)
                                            .onPrimary,
                                        size: 16.0,
                                      ),
                                      iconPresent: true,
                                      iconEndPresent: false,
                                      variant: 'primary',
                                      size: 'large',
                                      fullWidth: false,
                                      loading: false,
                                      disabled: false,
                                    ),
                                  ),
                                ),
                              ),
                              InkWell(
                                splashColor: Colors.transparent,
                                focusColor: Colors.transparent,
                                hoverColor: Colors.transparent,
                                highlightColor: Colors.transparent,
                                onTap: () async {
                                  context.goNamed(SOSEmergencyWidget.routeName);
                                },
                                child: Container(
                                  width: 64.0,
                                  height: 64.0,
                                  decoration: BoxDecoration(
                                    color: FlutterFlowTheme.of(context).error,
                                    boxShadow: [
                                      BoxShadow(
                                        blurRadius: 20.0,
                                        color:
                                            FlutterFlowTheme.of(context).error,
                                        offset: const Offset(
                                          0.0,
                                          0.0,
                                        ),
                                        spreadRadius: 0.0,
                                      )
                                    ],
                                    borderRadius: BorderRadius.circular(9999.0),
                                    shape: BoxShape.rectangle,
                                  ),
                                  alignment:
                                      const AlignmentDirectional(0.0, 0.0),
                                  child: Stack(
                                    alignment:
                                        const AlignmentDirectional(0.0, 0.0),
                                    children: [
                                      Lottie.asset(
                                        'assets/lottie/radial_pulse.json',
                                        width: 120.0,
                                        height: 120.0,
                                        fit: BoxFit.contain,
                                        animate: true,
                                      ),
                                      Text(
                                        'SOS',
                                        style: FlutterFlowTheme.of(context)
                                            .bodyMedium
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Inter',
                                                fontWeight: FontWeight.w900,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .bodyMedium
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .onError,
                                              fontSize: 16.0,
                                              letterSpacing: 0.0,
                                              fontWeight: FontWeight.w900,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .bodyMedium
                                                      .fontStyle,
                                              lineHeight: 1.5,
                                            ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ].divide(const SizedBox(width: 16.0)),
                          ),
                        ].divide(const SizedBox(height: 16.0)),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 1.0),
              child: SizedBox(
                height: 80.0,
                child: Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(
                      24.0, 0.0, 24.0, 24.0),
                  child: Container(
                    child: wrapWithModel(
                      model: _model.hudCardModel3,
                      updateCallback: () => safeSetState(() {}),
                      child: HudCardWidget(
                        margin: 16.0,
                        padding: '0',
                        child: () => const HudCardChild3Widget(),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
