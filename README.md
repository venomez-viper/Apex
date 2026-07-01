# APEX-II / STAM

**Deal-Stratified Survival Modeling for AI Presales Exposure**

This repository contains the APEX-II research paper and experiment artifacts by
**Akash Anipakalu Giridhar**.

APEX-II extends the original AI Presales Exposure Index with **STAM**: a
Segmented Task-coupled Adoption-Market Role Survival Index model for studying
how AI automation and augmentation pressure may propagate through SaaS presales
engineering work.

The project is intentionally framed as a simulation and diagnostic framework,
not as a definitive labor-market forecast.

## Paper

The final paper is provided in IEEE conference format.

| Artifact | Path |
| --- | --- |
| Final IEEE PDF | [`apex2_artifacts/paper/paper.pdf`](apex2_artifacts/paper/paper.pdf) |
| LaTeX source | [`apex2_artifacts/paper/paper.tex`](apex2_artifacts/paper/paper.tex) |
| Bibliography | [`apex2_artifacts/paper/references.bib`](apex2_artifacts/paper/references.bib) |
| Artifact manifest | [`apex2_artifacts/paper/manifest.json`](apex2_artifacts/paper/manifest.json) |

## Abstract

The first AI Presales Exposure Index (APEX-I) introduced a Role Survival Index
for estimating the exposure of SaaS presales engineering work to AI augmentation
and replacement. APEX-II addresses six limitations in that first framework:
deal-size homogeneity, prior-driven task weights, limited subtask mechanism
testing, post-hoc market-value coupling, low seed count, and informal scenario
mapping.

STAM decomposes presales work into six subtasks, separates Enterprise and SMB
sales motions, propagates automation exposure through task-dependency structure,
integrates condition-sensitive total addressable market dynamics into survival
computation, and evaluates 20-seed uncertainty across six AI adoption
conditions.

## Core Contributions

- Introduces a deal-size-stratified extension of the APEX Role Survival Index.
- Models six presales subtasks: discovery, technical demonstration, proof of
  concept coordination, RFP response, objection handling, and champion
  development.
- Adds task-dependency propagation through Enterprise and SMB topology variants.
- Integrates TAM feedback into the primary survival computation.
- Compares the full DAG/TAM model against APEX-I, no-DAG, no-TAM,
  uniform-topology, linear-displacement, expert-prior, and single-regime
  logistic baselines.
- Reports both positive and negative findings to avoid overstating predictive
  validity.

## Headline Results

| Result | Value |
| --- | ---: |
| Full APEX-II primary metric | 13787.40 |
| APEX-I additive sigmoid primary metric | 4922.41 |
| Full APEX-II final RSI | 0.649303 |
| APEX-I final RSI | 0.773805 |
| Full model external RMSE | 0.021094 |
| Single-regime logistic external RMSE | 0.00608 |
| Full-model topology R-squared | 0.065793 |
| Kendall tau for condition ranking | 1.0 |
| 20-seed BCa-style coverage | 0.916667 |

The strongest interpretation is conservative: APEX-II/STAM is a stronger
simulation and diagnostic framework than APEX-I, but the available calibration
data are not sufficient to claim validated labor-market prediction.

## Artifact Layout

```text
apex2_artifacts/
  checkpoint.json
  experiment/
    apex2_simulation.py
    apex2_metrics.json
    apex2_model_comparison.csv
    apex2_final_rsi_summary.csv
    apex2_results_timeseries.csv
  paper/
    paper.pdf
    paper.tex
    references.bib
    manifest.json
  stage12_runs/
    results.json
    run-1.json
  stage14_analysis/
    analysis.md
    experiment_summary.json
    results_table.tex
  stage14_charts/
    ablation_analysis.png
    experiment_comparison.png
    method_comparison.png
    metric_heatmap.png
    metric_trajectory.png
  stage16_outline/
    outline.md
  stage17_draft/
    paper_draft.md
  stage18_review/
    reviews.md
  stage19_revision/
    paper_revised.md
    revision_notes_internal.md
  stage20_quality/
    quality_report.json
    fabrication_flags.json
```

## Reproducibility

The main experiment script is:

```bash
python apex2_artifacts/experiment/apex2_simulation.py
```

The committed artifacts include the generated time-series output, model
comparison tables, summary metrics, charts, paper source, and quality-gate
outputs from the completed AutoResearchClaw run.

The pipeline checkpoint records completion through stage 20:

```text
last_completed_stage: 20
last_completed_name: QUALITY_GATE
```

## Quality Gate

The Stage 20 quality report is available at:

[`apex2_artifacts/stage20_quality/quality_report.json`](apex2_artifacts/stage20_quality/quality_report.json)

Summary:

- Verdict: `proceed`
- Score: `6.8 / 10`
- Word count audited: `4161`
- Core metrics present: `true`
- Real experiment data present: `true`

## Important Interpretation Notes

This repository includes real experiment artifacts and the final IEEE paper, but
the research claim is deliberately bounded:

- The full APEX-II model improves the internal simulation score relative to
  APEX-I.
- The single-regime logistic baseline performs better on the coarse external
  employment RMSE.
- BLS SOC 41-9031 is too broad to validate SaaS presales-specific dynamics by
  itself.
- The work should be read as a falsifiable simulation framework and research
  scaffold, not as a production-grade employment forecasting system.

## Citation

If you reference this work, cite:

```bibtex
@misc{giridhar2026apex2,
  author = {Akash Anipakalu Giridhar},
  title = {{STAM}: Deal-Stratified Survival Modeling for AI Presales Exposure},
  year = {2026},
  howpublished = {\url{https://github.com/venomez-viper/Apex}},
  note = {APEX-II research paper and experiment artifacts}
}
```

## Author

**Akash Anipakalu Giridhar**

Project repository: <https://github.com/venomez-viper/Apex>
