import '/components/aura_live_map.dart';
import '/core/providers/navigation_provider.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'route_comparison_model.dart';
export 'route_comparison_model.dart';

class RouteComparisonWidget extends StatefulWidget {
  const RouteComparisonWidget({super.key});

  static String routeName = 'RouteComparison';
  static String routePath = '/routeComparison';

  @override
  State<RouteComparisonWidget> createState() => _RouteComparisonWidgetState();
}

class _RouteComparisonWidgetState extends State<RouteComparisonWidget> {
  late RouteComparisonModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RouteComparisonModel());
  }

  @override
  void dispose() {
    _model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<NavigationProvider>(
      builder: (context, navigationProvider, child) {
        return GestureDetector(
          onTap: () {
            FocusScope.of(context).unfocus();
            FocusManager.instance.primaryFocus?.unfocus();
          },
          child: Scaffold(
            key: scaffoldKey,
            resizeToAvoidBottomInset: false,
            backgroundColor: const Color(0xFF080808),
            body: Stack(
              alignment: const AlignmentDirectional(-1.0, -1.0),
              children: [
                // Map with route display
                Positioned.fill(
                  child: AuraLiveMap(
                    userId: 'demo_user',
                    followCurrentLocation: false,
                    showStatusPill: true,
                    showControls: true,
                    routePoints: navigationProvider.currentRoute,
                    destination: navigationProvider.destination,
                  ),
                ),

                // Back button
                SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: FlutterFlowIconButton(
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
                  ),
                ),

                // Route info overlay
                if (navigationProvider.isNavigating)
                  Align(
                    alignment: Alignment.bottomCenter,
                    child: SafeArea(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color(0xD9081018),
                            borderRadius: BorderRadius.circular(18),
                            border: Border.all(
                              color: Colors.cyanAccent.withValues(alpha: 0.35),
                            ),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                // Risk score
                                Row(
                                  children: [
                                    Icon(
                                      navigationProvider.riskScore < 30
                                          ? Icons.shield
                                          : navigationProvider.riskScore < 70
                                              ? Icons.warning
                                              : Icons.dangerous,
                                      color: navigationProvider.riskScore < 30
                                          ? Colors.greenAccent
                                          : navigationProvider.riskScore < 70
                                              ? Colors.orangeAccent
                                              : Colors.redAccent,
                                      size: 20,
                                    ),
                                    const SizedBox(width: 8),
                                    Text(
                                      'Safety Score: ${navigationProvider.riskScore.toStringAsFixed(1)}%',
                                      style: FlutterFlowTheme.of(context)
                                          .bodyMedium
                                          .override(
                                            font: const TextStyle(
                                              fontFamily: 'Inter',
                                              color: Colors.white,
                                              fontWeight: FontWeight.w600,
                                            ),
                                          ),
                                    ),
                                  ],
                                ),

                                const SizedBox(height: 8),

                                // Route details
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.access_time,
                                      color: Colors.cyanAccent,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 6),
                                    Text(
                                      navigationProvider.estimatedTime,
                                      style: FlutterFlowTheme.of(context)
                                          .bodySmall
                                          .override(
                                            font: const TextStyle(
                                              fontFamily: 'Inter',
                                              color: Colors.white70,
                                            ),
                                          ),
                                    ),
                                    const SizedBox(width: 16),
                                    const Icon(
                                      Icons.straighten,
                                      color: Colors.cyanAccent,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 6),
                                    Text(
                                      navigationProvider.distance,
                                      style: FlutterFlowTheme.of(context)
                                          .bodySmall
                                          .override(
                                            font: const TextStyle(
                                              fontFamily: 'Inter',
                                              color: Colors.white70,
                                            ),
                                          ),
                                    ),
                                  ],
                                ),

                                // Warnings
                                if (navigationProvider.warnings.isNotEmpty) ...[
                                  const SizedBox(height: 12),
                                  Container(
                                    padding: const EdgeInsets.all(8),
                                    decoration: BoxDecoration(
                                      color: Colors.red.withValues(alpha: 0.1),
                                      borderRadius: BorderRadius.circular(8),
                                      border: Border.all(
                                        color: Colors.redAccent
                                            .withValues(alpha: 0.3),
                                      ),
                                    ),
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          children: [
                                            const Icon(
                                              Icons.warning,
                                              color: Colors.redAccent,
                                              size: 16,
                                            ),
                                            const SizedBox(width: 6),
                                            Text(
                                              'Safety Alerts',
                                              style:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .override(
                                                        font: const TextStyle(
                                                          fontFamily: 'Inter',
                                                          color:
                                                              Colors.redAccent,
                                                          fontWeight:
                                                              FontWeight.w600,
                                                        ),
                                                      ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 4),
                                        ...navigationProvider.warnings.map(
                                          (warning) => Padding(
                                            padding: const EdgeInsets.only(
                                                bottom: 2),
                                            child: Text(
                                              '• $warning',
                                              style:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .override(
                                                        font: const TextStyle(
                                                          fontFamily: 'Inter',
                                                          color: Colors.white70,
                                                          fontSize: 12,
                                                        ),
                                                      ),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],

                                const SizedBox(height: 12),

                                // Action buttons
                                Row(
                                  children: [
                                    Expanded(
                                      child: ElevatedButton.icon(
                                        onPressed: () {
                                          context.goNamed('LiveNavigation');
                                        },
                                        icon: const Icon(Icons.navigation,
                                            size: 16),
                                        label: const Text('Start Navigation'),
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.cyanAccent,
                                          foregroundColor: Colors.black,
                                          padding: const EdgeInsets.symmetric(
                                              vertical: 12),
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                                BorderRadius.circular(8),
                                          ),
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 12),
                                    TextButton.icon(
                                      onPressed:
                                          navigationProvider.stopNavigation,
                                      icon: const Icon(Icons.stop, size: 16),
                                      label: const Text('Stop'),
                                      style: TextButton.styleFrom(
                                        foregroundColor: Colors.redAccent,
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 12, horizontal: 16),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),

                // Loading overlay
                if (navigationProvider.isLoading)
                  Container(
                    color: Colors.black.withValues(alpha: 0.7),
                    child: const Center(
                      child: CircularProgressIndicator(
                        valueColor:
                            AlwaysStoppedAnimation<Color>(Colors.cyanAccent),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }
}
