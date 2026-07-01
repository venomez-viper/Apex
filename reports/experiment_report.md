# Experiment Report

## Run Summary

| Field | Value |
| --- | --- |
| Run ID | `rc-20260630-202809-308c01` |
| Completed stage | Stage 20, `QUALITY_GATE` |
| Paper format | IEEEtran conference |
| Main script | `experiments/apex2_simulation.py` |
| Primary results | `experiments/apex2_metrics.json` |
| Full time series | `experiments/apex2_results_timeseries.csv` |

The completed run produced experiment outputs, analysis reports, charts, an IEEE
paper, and a quality-gate report. The repository keeps both polished artifacts
and raw pipeline evidence.

## Execution Scope

The experiment evaluates:

- 2 deal-size segments.
- 6 AI adoption conditions.
- 20 seeds.
- 8 model variants and ablations.

The model variants include the full APEX-II DAG/TAM model, APEX-I additive
sigmoid, expert-prior APEX-II, no-DAG, no-TAM, uniform-topology,
linear-displacement, and single-regime logistic baselines.

## Primary Artifacts

| Artifact | Path |
| --- | --- |
| Simulation code | `experiments/apex2_simulation.py` |
| Summary metrics | `experiments/apex2_metrics.json` |
| Model comparison | `experiments/apex2_model_comparison.csv` |
| RSI summary | `experiments/apex2_final_rsi_summary.csv` |
| Full time series | `experiments/apex2_results_timeseries.csv` |
| Stage 12 run result | `reports/pipeline/stage12_runs/results.json` |
| Stage 14 experiment summary | `reports/pipeline/stage14_analysis/experiment_summary.json` |

## Figures

| Figure | Path |
| --- | --- |
| Method comparison | `figures/method_comparison.png` |
| Ablation analysis | `figures/ablation_analysis.png` |
| Experiment comparison | `figures/experiment_comparison.png` |
| Metric trajectory | `figures/metric_trajectory.png` |
| Metric heatmap | `figures/metric_heatmap.png` |

## Notes on Pipeline Reliability

The numerical experiment and analysis artifacts completed. Later narrative
stages required deterministic fallbacks when the ACP narrative call was
unreliable. The paper therefore keeps claims tied to completed artifacts and
does not invent additional experiment results.
