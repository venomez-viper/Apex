## Metrics Summary

Result quality rating: **4/10**.

The experiment is a useful simulation and ablation testbed, but not yet strong empirical evidence for APEX-II’s core claims.

Key metrics:

| Metric | Value | Interpretation |
|---|---:|---|
| `success_rate` | `1.0` | Pipeline runs reliably; not evidence of validity. |
| `apex2_dag_tam_coupled/primary_metric` | `13787.40` | Strong model-output gain, but likely TAM-scale sensitive. |
| `apex1_additive_sigmoid/primary_metric` | `4922.41` | APEX-II full model is ~2.8x higher, but comparability is unclear. |
| `single_regime_logistic/holdout_employment_rmse` | `0.00608` | Best external-employment fit among reported models. |
| `apex2_dag_tam_coupled/holdout_employment_rmse` | `0.021094` | Full model underperforms simpler model on holdout RMSE. |
| `apex2_dag_tam_coupled/topology_r_squared` | `0.065793` | Topology explains only modest variance. |
| Overall `topology_r_squared` | `0.003032` | Does not support “primary determinant” framing. |
| `kendall_tau_condition_ranking` | `1.0` | Stable condition ordering, but may be mechanically imposed. |
| `bca_coverage_n20` | `0.916667` | Below nominal 95%; encouraging but not sufficient. |

## Consensus Findings

High-confidence conclusions:

1. **The experimental pipeline executed successfully.**  
   All perspectives agree that APEX-II now runs across multiple variants, seeds, segments, scenarios, and ablations.

2. **APEX-II produces differentiated trajectories.**  
   The full DAG/TAM model, no-DAG model, no-TAM model, uniform-topology model, and single-regime model produce meaningfully different outputs.

3. **The full DAG/TAM model dominates on the reported `primary_metric`.**  
   `13787.40` versus `4922.41` for APEX-I and `7887.01-9217.74` for several ablations is a real numerical separation.

4. **The empirical-validity claim is not yet established.**  
   The full model’s weaker holdout RMSE versus `single_regime_logistic` is a major constraint.

5. **The central H1 claim is overstated.**  
   Current `topology_r_squared` values do not support “subtask coupling topology is the primary RSI determinant.”

## Contested Points

The optimist treats the full DAG/TAM model’s high `primary_metric` as evidence that DAG coupling and TAM feedback are doing explanatory work. The skeptic and methodologist argue that this may be scale inflation. The skeptical interpretation is stronger: without a clear, normalized definition of `primary_metric`, the 2.8x gain cannot be treated as empirical validation.

The optimist views `kendall_tau_condition_ranking = 1.0` as robustness. The more cautious interpretation is that condition order may be hard-coded through scenario assumptions. It is useful as a sanity check, not as independent evidence.

The optimist suggests lower APEX-II RSI values may be “more realistic.” That is plausible, but not proven. Lower RSI is only meaningful if externally validated against employment, hiring, task mix, or compensation outcomes.

The strongest conflict is RMSE versus `primary_metric`. If the goal is external empirical calibration, the simpler `single_regime_logistic` model currently wins with `0.00608` RMSE. If the goal is richer simulation structure, the full DAG/TAM model is more expressive. These are different claims and must not be conflated.

## Statistical Checks

The statistical evidence is weak.

Most aggregate results report `n=1`, so there are no valid standard errors, confidence intervals, or hypothesis tests for the main comparisons. Seed-level outputs exist, but they are not summarized as paired model comparisons.

The 20 seeds improve simulation stability, but they do not create independent empirical observations. If seeds only perturb stochastic simulation noise, the study risks pseudoreplication.

Multiple-comparison risk is high: models, segments, scenarios, seeds, RSI, RMSE, bimodality, topology R², condition ranking, and TAM-derived metrics are all inspected. No correction or pre-registered primary endpoint is evident.

`bca_coverage_n20 = 0.916667` is below 95%, and because it is reported as a single aggregate, it should be treated as preliminary.

Needed checks:

- Paired bootstrap CIs for full DAG/TAM versus each ablation.
- Effect sizes for `primary_metric`, `final_rsi`, RMSE, and segment divergence.
- Multiple-comparison correction or a pre-specified primary hypothesis.
- Sensitivity to seed count beyond 20.
- Variance decomposition showing how much is due to topology, TAM, calibration, segment weights, and scenarios.

## Methodology Audit

The baseline suite is directionally good but not yet fair. It includes APEX-I, no-DAG, no-TAM, uniform topology, expert priors, linear displacement, and single-regime logistic. However, the full model changes multiple components simultaneously, making causal attribution impossible.

The biggest methodology problem is that the flagship model wins on an unclear `primary_metric` while losing on holdout employment RMSE. This suggests either:

- `primary_metric` is not measuring external validity, or
- the full model is over-structured for the available empirical signal, or
- the simpler model exploits temporal smoothness better.

The evaluation protocol also has possible leakage. BLS, hiring proxies, and adoption bands appear to inform calibration, scenario design, and validation. These roles need to be separated.

Required improvements:

- Define the primary estimand: employment survival, task survival, hiring demand, market-adjusted role value, or RSI trajectory.
- Normalize TAM-sensitive metrics.
- Retune all baselines under equal calibration budgets.
- Add clean train/validation/test splits by time and source.
- Add subtask-level validation for discovery, demo, POC, RFP, objection handling, and champion development.
- Run component-isolating ablations: DAG-only, TAM-only, calibration-only, segment-only.
- Test alternative DAGs and edge weights.
- Report full reproducibility artifacts, not `stdout_parsed` summaries.

## Limitations

The experiment currently supports a simulation claim, not a labor-market validity claim.

Major limitations:

- `primary_metric` is undefined or insufficiently interpretable.
- Aggregate metrics mostly have `n=1`.
- External validation is incomplete.
- Full model underperforms simpler model on holdout RMSE.
- Topology effect is modest, not dominant.
- Scenario rankings may be imposed by construction.
- Subtask-level evidence is missing despite being central to APEX-II.
- TAM feedback may inflate outputs mechanically.
- Reproducibility artifacts are incomplete or truncated.

## Conclusion

Recommendation: **REFINE**.

Do not pivot away from APEX-II. The framework is promising, the ablation structure is useful, and the system now produces differentiated model behavior. But do not proceed to strong NeurIPS/ICML-style claims yet.

The defensible current claim is:

> APEX-II is a richer simulation framework that generates distinct Enterprise/SMB and scenario-conditioned RSI trajectories, and its DAG/TAM specification materially changes outputs relative to simpler baselines.

The not-yet-defensible claim is:

> DAG subtask topology is the primary determinant of real-world presales role survival.

To move forward, reframe the next iteration around empirical validation: define the target outcome, normalize TAM-sensitive metrics, fairly retune baselines, report paired uncertainty, and directly validate subtask-level mechanisms.