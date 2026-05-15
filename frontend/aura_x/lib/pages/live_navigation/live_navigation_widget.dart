import '/components/aura_live_map.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'live_navigation_model.dart';
export 'live_navigation_model.dart';

class LiveNavigationWidget extends StatefulWidget {
  const LiveNavigationWidget({super.key});

  static const String routeName = 'LiveNavigation';
  static const String routePath = '/live-navigation';

  @override
  State<LiveNavigationWidget> createState() => _LiveNavigationWidgetState();
}

class _LiveNavigationWidgetState extends State<LiveNavigationWidget> {
  late LiveNavigationModel _model;

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => LiveNavigationModel());
  }

  @override
  void dispose() {
    _model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          const Positioned.fill(
            child: AuraLiveMap(
              initialZoom: 17,
              followCurrentLocation: true,
              showControls: true,
              showStatusPill: true,
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  FlutterFlowIconButton(
                    borderColor: Colors.cyanAccent.withValues(alpha: 0.45),
                    borderRadius: 30,
                    borderWidth: 1,
                    buttonSize: 44,
                    fillColor: const Color(0xD9081018),
                    icon: const Icon(
                      Icons.arrow_back,
                      color: Colors.cyanAccent,
                      size: 24,
                    ),
                    onPressed: () => context.goNamed('HomeMap'),
                  ),
                  const SizedBox(width: 12),
                  DecoratedBox(
                    decoration: BoxDecoration(
                      color: const Color(0xD9081018),
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(
                        color: Colors.cyanAccent.withValues(alpha: 0.45),
                      ),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 10,
                      ),
                      child: Text(
                        'LIVE NAVIGATION',
                        style:
                            FlutterFlowTheme.of(context).labelMedium.override(
                                  font: TextStyle(
                                    fontFamily: 'Orbitron',
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelMedium
                                        .fontStyle,
                                  ),
                                  color: Colors.cyanAccent,
                                  letterSpacing: 0,
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .labelMedium
                                      .fontStyle,
                                ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 82, 24),
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: const Color(0xD9081018),
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(
                      color: Colors.cyanAccent.withValues(alpha: 0.35),
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.route_rounded,
                          color: Colors.cyanAccent,
                          size: 22,
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            'Tracking your live safety corridor',
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontStyle,
                                  ),
                                  color: Colors.white,
                                  letterSpacing: 0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontStyle,
                                ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
