# Methodology Report

## Objective

APEX-II extends the original AI Presales Exposure Index by testing whether a
deal-size-stratified and task-coupled model gives a more useful diagnostic view
of SaaS presales AI exposure than the original additive RSI formulation.

The target role is SaaS presales engineering. The model treats the role as a
bundle of subtasks rather than as a single occupational label.

## Model Name

The implemented model is STAM: Segmented Task-coupled Adoption-Market RSI.

STAM has four main additions over APEX-I:

- Deal-size stratification between Enterprise and SMB sales motions.
- Six-task substructure for presales work.
- Directed task-coupling through segment-specific topology.
- TAM feedback inside the survival computation.

## Subtasks

The model decomposes presales work into six subtasks:

| Subtask | Interpretation |
| --- | --- |
| Discovery | Understanding buyer context, constraints, and success criteria |
| Technical demonstration | Preparing and adapting product demonstrations |
| POC coordination | Managing proof-of-concept scope, timeline, and validation |
| RFP response | Producing structured technical and commercial responses |
| Objection handling | Responding to technical, commercial, and trust objections |
| Champion development | Building internal buyer support and political alignment |

The decomposition is important because AI exposure is not uniform across the
role. RFP response is more automatable than champion development, while POC
coordination and objection handling mix procedural and relational work.

## Segments

The experiment models two deal-size segments:

- Enterprise: serial, dependency-rich topology.
- SMB: more standardized and parallel topology.

The point is not to assign Enterprise work a blanket resilience bonus. The point
is to test whether dependency structure changes survival dynamics.

## Conditions

Six adoption conditions are evaluated:

| Condition | Interpretation |
| --- | --- |
| AFC | AI-free or near-AI-free counterfactual |
| CAB | Current AI copilot baseline |
| C24 | Conservative 2024 baseline |
| PAR | Partial automation of structured presales work |
| HAO | High adoption with human override |
| FAR | Full AI replacement pressure |

These are scenario levers. They are not probability-weighted forecasts.

## Baselines and Ablations

The full model is compared with:

- APEX-I additive sigmoid.
- Expert-prior APEX-II.
- No DAG coupling.
- No TAM feedback.
- Uniform topology.
- Linear displacement.
- Single-regime logistic.

This design separates three questions:

- Does APEX-II behave differently from APEX-I?
- Which added mechanisms are responsible for the change?
- Does a simpler model outperform the richer framework on external fit?

## Interpretation Boundary

The model is a simulation framework. It is suitable for mechanism testing,
scenario analysis, and sensitivity analysis. It is not presented as a validated
employment forecasting system.
