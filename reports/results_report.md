# Results Report

## Main Finding

The full APEX-II DAG/TAM model separates strongly from APEX-I on the internal
simulation metric and gives a more useful task-level view of presales exposure.
The key practical result is that AI pressure is concentrated in repeatable
artifact-heavy work such as RFP response and technical demonstration, while
discovery, objection handling, and champion development remain more
human-anchored. The model does not beat the single-regime logistic baseline on
coarse external employment RMSE, so the work should be used as a presales
exposure audit and scenario tool rather than as a standalone employment
forecast.

## Headline Metrics

| Metric | Value |
| --- | ---: |
| Full APEX-II primary metric | 13787.40 |
| APEX-I additive sigmoid primary metric | 4922.41 |
| Expert-prior APEX-II primary metric | 13040.19 |
| No-DAG primary metric | 7887.01 |
| No-TAM primary metric | 8991.60 |
| Uniform-topology primary metric | 8271.16 |
| Linear-displacement primary metric | 9217.74 |
| Single-regime logistic primary metric | 5948.90 |
| Full APEX-II final RSI | 0.649303 |
| APEX-I final RSI | 0.773805 |
| Single-regime logistic final RSI | 0.634293 |
| Full model external RMSE | 0.021094 |
| Single-regime logistic external RMSE | 0.00608 |
| Kendall tau for condition ranking | 1.0 |
| 20-seed BCa-style coverage | 0.916667 |

## Interpretation

APEX-II changes the simulation output in a meaningful way. The full model is not
a cosmetic rewrite of APEX-I. DAG coupling, TAM feedback, segment structure, and
calibration interact to produce different survival trajectories.

The practical reading is straightforward: use AI first where work is structured,
reviewable, and artifact-heavy; keep stronger human control where work depends
on ambiguity, customer trust, and political alignment. The richer model has a
worse external RMSE than the single-regime logistic baseline, so it should be
treated as a planning and stress-testing framework rather than a validated
employment forecasting model.

## Segment Result

The Enterprise/SMB coefficient-of-variation ratio is reported as 1.413188 in
the paper evidence ledger, while the committed summary metric file reports
1.648806945876928 for the final metric fixture. Both values point in the same
direction: segment behavior differs enough to justify deal-size stratification.

## Coverage Result

The 20-seed coverage estimate is approximately 0.92. This improves on the
APEX-I three-seed design but remains below nominal 95 percent coverage. A future
version should test larger seed counts and more formal confidence interval
procedures.

## Negative Results

The negative results are part of the contribution:

- External RMSE favors a simpler baseline.
- Topology explains only modest variance.
- TAM feedback changes scale more than condition ranking.
- SOC-level employment data are too broad for presales-specific validation.
