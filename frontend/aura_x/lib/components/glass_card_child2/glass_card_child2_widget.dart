import '/components/metric_item/metric_item_widget.dart';
import '/flutter_flow/flutter_flow_charts.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'glass_card_child2_model.dart';
export 'glass_card_child2_model.dart';

class GlassCardChild2Widget extends StatefulWidget {
  const GlassCardChild2Widget({super.key});

  @override
  State<GlassCardChild2Widget> createState() => _GlassCardChild2WidgetState();
}

class _GlassCardChild2WidgetState extends State<GlassCardChild2Widget> {
  late GlassCardChild2Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCardChild2Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            wrapWithModel(
              model: _model.metricItemModel1,
              updateCallback: () => safeSetState(() {}),
              child: MetricItemWidget(
                color: FlutterFlowTheme.of(context).primary,
                label: 'SAFE KM',
                value: '1,284',
              ),
            ),
            Container(
              width: 1.0,
              height: 30.0,
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).divider30,
              ),
            ),
            wrapWithModel(
              model: _model.metricItemModel2,
              updateCallback: () => safeSetState(() {}),
              child: MetricItemWidget(
                color: FlutterFlowTheme.of(context).success,
                label: 'RISK AVOIDED',
                value: '42',
              ),
            ),
            Container(
              width: 1.0,
              height: 30.0,
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).divider30,
              ),
            ),
            wrapWithModel(
              model: _model.metricItemModel3,
              updateCallback: () => safeSetState(() {}),
              child: MetricItemWidget(
                color: FlutterFlowTheme.of(context).tertiary,
                label: 'SHIELD HRS',
                value: '312',
              ),
            ),
          ],
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Row(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'Weekly Safety Score',
                  style: FlutterFlowTheme.of(context).bodySmall.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight:
                              FlutterFlowTheme.of(context).bodySmall.fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).bodySmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        lineHeight: 1.5,
                      ),
                ),
                Text(
                  'Avg 94%',
                  style: FlutterFlowTheme.of(context).bodySmall.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight:
                              FlutterFlowTheme.of(context).bodySmall.fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).success,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).bodySmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        lineHeight: 1.5,
                      ),
                ),
              ],
            ),
            SizedBox(
              height: 120.0,
              child: Padding(
                padding:
                    const EdgeInsetsDirectional.fromSTEB(16.0, 0.0, 0.0, 0.0),
                child: Container(
                  child: SizedBox(
                    height: 120.0,
                    child: FlutterFlowLineChart(
                      data: [
                        FFLineChartData(
                          xData: ([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
                          yData: ([85.0, 88.0, 92.0, 90.0, 96.0, 98.0, 94.0]),
                          settings: LineChartBarData(
                            color: FlutterFlowTheme.of(context).primary,
                            barWidth: 2.0,
                            isCurved: true,
                            dotData: const FlDotData(show: false),
                            belowBarData: BarAreaData(
                              show: true,
                              color: FlutterFlowTheme.of(context).primary20,
                            ),
                          ),
                        )
                      ],
                      chartStylingInfo: const ChartStylingInfo(
                        backgroundColor: Colors.transparent,
                        showBorder: false,
                      ),
                      axisBounds: const AxisBounds(
                        minX: 0.0,
                        minY: 0.0,
                        maxX: 6.0,
                        maxY: 117.6,
                      ),
                      xLabels: (const ['M', 'T', 'W', 'T', 'F', 'S', 'S']),
                      xAxisLabelInfo: AxisLabelInfo(
                        showLabels: true,
                        labelTextStyle: FlutterFlowTheme.of(context)
                            .bodySmall
                            .override(
                              font: TextStyle(
                                fontFamily: 'Inter',
                                fontWeight: FlutterFlowTheme.of(context)
                                    .bodySmall
                                    .fontWeight,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .bodySmall
                                    .fontStyle,
                              ),
                              color: FlutterFlowTheme.of(context).secondaryText,
                              fontSize: 10.0,
                              letterSpacing: 0.0,
                              fontWeight: FlutterFlowTheme.of(context)
                                  .bodySmall
                                  .fontWeight,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .bodySmall
                                  .fontStyle,
                              lineHeight: 1.0,
                            ),
                        reservedSize: 28.0,
                      ),
                      yAxisLabelInfo: const AxisLabelInfo(
                        reservedSize: 0.0,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ].divide(const SizedBox(height: 8.0)),
        ),
      ],
    );
  }
}
