# Conclusion Validation Report

This report validates the main conclusions in the APEX-II / STAM paper against
the committed experiment and pipeline artifacts.

## Validation Summary

| Paper conclusion | Validation status | Supporting artifacts |
| --- | --- | --- |
| APEX-II separates from APEX-I on the internal primary metric. | Supported | `reports/pipeline/stage16_outline/outline.md`, `experiments/apex2_model_comparison.csv`, `reports/pipeline/stage14_analysis/experiment_summary.json` |
| APEX-II lowers final RSI relative to APEX-I. | Supported | `reports/pipeline/stage16_outline/outline.md`, `experiments/apex2_final_rsi_summary.csv`, `figures/final_rsi_by_condition.png` |
| The richer model should not be described as a validated labor-market predictor. | Supported | `reports/pipeline/stage16_outline/outline.md`, `reports/limitations_report.md`, `figures/coverage_and_calibration.png` |
| Segment stratification is justified. | Supported with caution | `experiments/apex2_metrics.json`, `experiments/apex2_final_rsi_summary.csv`, `figures/segment_gap_by_condition.png` |
| Task-level decomposition is useful for mechanism inspection. | Supported as simulation evidence | `experiments/apex2_results_timeseries.csv`, `figures/subtask_survival_profile.png` |
| More seeds improve coverage, but uncertainty remains below nominal 95 percent coverage. | Supported | `experiments/apex2_metrics.json`, `figures/coverage_and_calibration.png` |
| TAM and DAG components materially affect internal outcomes. | Supported for internal simulation metrics | `reports/pipeline/stage16_outline/outline.md`, `figures/bic_model_ranking.png`, `figures/ablation_analysis.png` |
| External calibration remains weak. | Supported | `experiments/apex2_metrics.json`, `reports/pipeline/stage16_outline/outline.md`, `figures/coverage_and_calibration.png` |

## Claim-by-Claim Notes

### Internal separation from APEX-I

The Stage 16 evidence ledger reports a full APEX-II primary metric of 13787.40
and an APEX-I additive sigmoid primary metric of 4922.41. This supports the
claim that APEX-II changes internal simulation behavior relative to APEX-I.

### Final RSI shift

The Stage 16 evidence ledger reports final RSI values of 0.773805 for APEX-I,
0.649303 for full APEX-II, and 0.634293 for the single-regime baseline. The
final RSI figure generated from `experiments/apex2_final_rsi_summary.csv`
supports the same qualitative conclusion: stronger adoption conditions reduce
survival more sharply under the richer model family than under the original
APEX-I additive formulation.

### Segment stratification

The paper's evidence ledger reports an Enterprise/SMB coefficient-of-variation
ratio of 1.413188. The committed metrics file reports
1.648806945876928 for the final metric fixture. These values are not identical
because they come from different artifact summaries, but they point in the same
direction: segment behavior differs enough to justify reporting Enterprise and
SMB separately.

### Subtask mechanism

The subtask profile figure shows the strongest survival decline in RFP response
and technical demonstration under higher adoption pressure, while champion
development remains relatively resilient. This supports the mechanism claim that
presales exposure is task-dependent rather than uniform across the role.

### External validation boundary

The conclusion is deliberately bounded. Stage 16 reports that the single-regime
logistic baseline has better external employment RMSE than the full model
(0.00608 versus 0.021094). The committed metrics file also shows a calibration
stress-test weakness: calibrated fixture RMSE is higher than expert-prior RMSE.
These findings validate the decision to present STAM as a simulation framework,
not a production employment forecaster.

## Practical Conclusion

The useful conclusion is not that APEX-II predicts exact presales employment.
The useful conclusion is that STAM turns presales AI exposure into an auditable
task and segment analysis.

The validated takeaways are:

- APEX-I is too coarse for presales planning because it hides task-level
  exposure differences.
- RFP response and technical demonstration are the most exposed work surfaces in
  the current simulation.
- Discovery, objection handling, and champion development remain more
  human-anchored because they depend on buyer ambiguity, trust, and political
  context.
- Enterprise and SMB motions should not be modeled with one aggregate survival
  score.
- APEX-II is suitable for workflow stress testing and presales AI rollout
  planning, but not yet for standalone employment forecasting.

## Validation Judgment

The paper's conclusions are supported as claims about simulation behavior,
mechanism inspection, workflow-risk analysis, and scenario stress testing. They
are not supported as claims of externally validated labor-market forecasting
accuracy.
