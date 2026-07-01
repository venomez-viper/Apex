# Limitations Report

## Internal Validity

The model combines multiple mechanisms: DAG coupling, TAM feedback, calibration
scaling, segment topology, and nonlinear survival. Targeted ablations are
included, but the full model still contains interactions. The ablation results
should therefore be interpreted as mechanism sensitivity rather than clean
causal isolation.

## External Validity

The external calibration signal is coarse. BLS SOC 41-9031 covers sales
engineers broadly and does not isolate SaaS presales. It also does not split
Enterprise and SMB motions. This limits the strength of any employment
forecasting claim.

## Construct Validity

The internal primary metric is useful for comparing model variants inside the
same simulation harness. It is not itself an employment count, revenue estimate,
or headcount forecast. The paper reports RMSE and final RSI to avoid relying on
one internal score.

## Statistical Limitations

The 20-seed design improves on APEX-I, but coverage remains below the nominal 95
percent target. Future work should test larger seed counts and report more
formal uncertainty intervals.

## Data Limitations

The strongest future dataset would include:

- Official occupational employment pulls.
- SaaS-specific presales hiring series.
- Enterprise versus SMB segment labels.
- Firm-level AI adoption indicators.
- Process metrics such as RFP turnaround, POC staffing, demo preparation time,
  technical win rate, and sales-cycle variance.
