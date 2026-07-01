# APEX-II Paper Outline

## Candidate Titles

Method name: **STAM** = **S**egmented **T**ask-coupled **A**doption-**M**arket RSI model.

| Candidate Title | Memorability | Specificity | Novelty Signal | Notes |
|---|---:|---:|---:|---|
| **STAM: Deal-Stratified Survival Modeling for AI Presales Exposure** | 4 | 5 | 4 | Best balance; clearly extends APEX RSI. |
| **STAM: Empirically Calibrated Presales Exposure Across SaaS Deal Sizes** | 3 | 5 | 4 | Strong empirical-calibration signal. |
| **STAM: Task-Coupled RSI Forecasts for Enterprise and SMB Presales** | 4 | 4 | 5 | Highlights subtask topology and segmentation. |

Recommended title: **STAM: Deal-Stratified Survival Modeling for AI Presales Exposure**

---

## Evidence Ledger

- **E1: Model differentiation**: APEX-II DAG/TAM model produces distinct trajectories from APEX-I, no-DAG, no-TAM, uniform-topology, expert-prior, linear-displacement, and single-regime baselines.
- **E2: Full-model primary score**: `apex2_dag_tam_coupled/primary_metric = 13787.40`.
- **E3: APEX-I baseline**: `apex1_additive_sigmoid/primary_metric = 4922.41`; apparent 2.8x separation, but TAM-scale sensitivity prevents validity claims.
- **E4: External-fit weakness**: full model holdout RMSE `0.021094`; single-regime logistic RMSE `0.00608`.
- **E5: Weak topology evidence**: full-model topology R² `0.065793`; overall topology R² `0.003032`.
- **E6: Stable condition ordering**: `kendall_tau_condition_ranking = 1.0`, treated as scenario sanity check, not independent validation.
- **E7: Bootstrap coverage**: `bca_coverage_n20 = 0.916667`, below nominal 95%.
- **E8: Segment divergence**: `apex2_dag_tam_coupled/enterprise_smb_cov_ratio = 1.413188`, supporting deal-size stratification as behaviorally meaningful.
- **E9: Final RSI shift**: APEX-I final RSI `0.773805`; APEX-II DAG/TAM final RSI `0.649303`; single-regime final RSI `0.634293`.
- **E10: TAM-coupling effect**: no-TAM primary score `8991.60` versus DAG/TAM `13787.40`, suggesting large market-feedback sensitivity.
- **E11: DAG ablation effect**: no-DAG primary score `7887.01` versus DAG/TAM `13787.40`, but causal attribution remains confounded with TAM and calibration.
- **E12: Methodological decision**: current evidence supports “simulation framework with differentiated trajectories,” not “validated labor-market predictor.”

---

## Abstract Target

**Target length:** 190-210 words  
**Goal:** State that APEX-I introduced RSI but left six limitations unresolved: deal-size homogeneity, prior-driven weights, missing subtask mechanisms, post-hoc MVS coupling, low seed count, and weak scenario grounding. Introduce **STAM** as the APEX-II technical extension.

**Required content:**
- Problem: Presales exposure cannot be validly estimated with a single aggregate RSI trajectory.
- Method: STAM splits task weights by Enterprise/SMB, decomposes RSI across six subtasks, calibrates to BLS SOC 41-9031 and hiring/adoption proxies, and embeds condition-sensitive TAM into the survival equation.
- Results: Report cautiously: full model changes outputs substantially relative to APEX-I (`13787.40` vs `4922.41`) and ablations, but loses external RMSE to single-regime logistic (`0.021094` vs `0.00608`).
- Framing: APEX-II is a stronger simulation and diagnostic framework, not yet definitive empirical labor-market validation.

**Evidence links:** E1, E2, E3, E4, E8, E12.

---

## 1. Introduction

**Target length:** 850-950 words  
**Goal:** Motivate why SaaS sales engineering is a high-value test case for AI labor exposure: presales work combines codifiable artifacts with relationship-dependent judgment. Frame APEX-II as a direct response to Part 1’s RSI limitations.

**Paragraph plan:**
1. Explain the presales automation problem: AI copilots can accelerate RFPs, demos, discovery notes, objection handling, and POC coordination, but the exposure pattern differs by deal size and customer motion.
2. Identify the gap in APEX-I: single-motion RSI, prior-based alpha/beta weights, limited seeds, no subtask-level mechanism test, and post-hoc MVS draw.
3. Introduce STAM: a deal-size-stratified, empirically calibrated, task-coupled, TAM-aware RSI extension.
4. Contributions:
   - Enterprise/SMB conditional alpha and beta task weights.
   - Six-task RSI decomposition for augmentation-vs-replacement testing.
   - Empirical calibration to BLS, hiring proxies, and adoption scenario bands.
   - Primary survival computation with endogenous TAM and 20-seed uncertainty reporting.

**Citations to include in draft:** APEX-I, BLS SOC 41-9031, Autor task-based labor economics, Frey and Osborne automation, Webb AI exposure, Felten occupational AI exposure, Brynjolfsson augmentation framing, McKinsey AI adoption, IDC AI spending scenarios, Gartner copilot adoption surveys.

**Evidence links:** E1, E8, E9, E12.

---

## 2. Related Work

**Target length:** 650-800 words  
**Goal:** Position APEX-II against labor-exposure indices, AI adoption scenario modeling, and task-level sales engineering research.

### 2.1 AI Labor Exposure and Occupational Survival
Cover task-based labor economics, occupation-level exposure indices, and automation versus augmentation. End by stating that APEX-II differs by modeling role survival as a calibrated, time-varying RSI trajectory rather than a static exposure score.

**Evidence links:** E4, E12.

### 2.2 Presales, Sales Engineering, and Enterprise SaaS Workflows
Discuss presales as a hybrid technical-commercial role. Emphasize that Enterprise and SMB motions have different cycle lengths, stakeholder structures, proof requirements, and relationship depth. APEX-II’s split alpha/beta weights directly target this missing heterogeneity.

**Evidence links:** E8.

### 2.3 Scenario-Based AI Adoption and Market Feedback
Discuss McKinsey/IDC/Gartner-style adoption bands and how adoption scenarios influence demand, not only substitution. Clarify that APEX-II improves APEX-I by integrating condition-sensitive TAM into survival rather than drawing MVS post hoc.

**Evidence links:** E6, E10.

---

## 3. Method: STAM

**Target length:** 1200-1500 words  
**Goal:** Present a technical model, not a workflow. Keep the sigmoid-normalized RSI core from APEX-I while extending it with segmentation, calibration, task coupling, and TAM feedback.

### 3.1 Problem Formulation
Define presales segment \(s \in \{\text{Enterprise}, \text{SMB}\}\), task \(k \in \{1,\ldots,6\}\), quarter \(t\), and adoption condition \(c \in \{\text{AFC}, \text{CAB}, \text{C24}, \text{PAR}, \text{HAO}, \text{FAR}\}\). Define RSI as a sigmoid-normalized survival score:

\[
RSI_{s,c,t} = \sigma \left( \theta_0 + \sum_k \beta_{s,k} C_{s,k,t} - \sum_k \alpha_{s,k} A_{c,k,t} + \lambda TAM_{c,t} + \phi^\top Z_t \right).
\]

Explain that \(\alpha_{s,k}\) captures automation susceptibility and \(\beta_{s,k}\) captures role criticality, both split by deal size.

**Evidence links:** E8, E9.

### 3.2 Subtask-Level Decomposition
Define six subtasks: discovery, technical demonstration, POC coordination, RFP response, objection handling, and champion development. Explain the augmentation/replacement bifurcation: tasks with high codifiability and low relational dependence should show replacement pressure, while tasks with high stakeholder complexity should show augmentation.

**Evidence links:** E5, E12.

### 3.3 DAG Task Coupling
Represent task dependencies as a weighted DAG, where upstream discovery and champion development influence downstream objection handling, POC success, and demo effectiveness. Define topology contribution as a variance-decomposition term, but explicitly avoid claiming it is dominant given current R².

**Evidence links:** E5, E11.

### 3.4 Empirical Calibration
Specify calibration targets:
- BLS SOC 41-9031 employment trajectory for external occupational anchoring.
- LinkedIn-style hiring proxies for demand-side signals.
- Gartner-style copilot adoption bands for adoption timing.
- McKinsey/IDC/Gartner scenario bands for mapping AFC, CAB, C24, PAR, HAO, and FAR.

Separate calibration, validation, and test sources to avoid leakage. State that the current run reveals a key empirical tension: the richer full model underperforms a simpler logistic model on holdout RMSE.

**Evidence links:** E4, E6, E12.

### 3.5 TAM-Coupled Survival
Replace APEX-I’s seed-determined MVS draw with a condition-sensitive TAM trajectory inside the survival computation. Define TAM as a market-demand multiplier that can offset or amplify automation exposure depending on adoption condition.

**Evidence links:** E2, E10.

### 3.6 Algorithm Box
Include pseudocode for:
1. Initialize segment-specific alpha and beta.
2. Map condition to adoption/TAM scenario.
3. Compute subtask automation and criticality trajectories.
4. Propagate task effects through DAG.
5. Compute segment-conditional RSI.
6. Aggregate with uncertainty over 20 seeds.
7. Evaluate against external calibration targets and ablations.

**Evidence links:** E1, E7.

---

## 4. Experimental Design

**Target length:** 900-1100 words  
**Goal:** Explain datasets, baselines, metrics, and statistical protocol while preventing overclaiming.

### 4.1 Data and Scenario Inputs
Describe BLS SOC 41-9031, hiring-trend proxies, copilot adoption bands, and six scenario conditions. State that exact scenario bands are used as calibration priors and must be separated from holdout validation.

**Evidence links:** E4, E6.

### 4.2 Baselines
Compare against:
- APEX-I additive sigmoid.
- Single-regime logistic.
- No-DAG coupling.
- No-TAM feedback.
- Uniform topology.
- Expert priors.
- Linear displacement.

Emphasize equal calibration budget and paired-seed comparison in the revised benchmark.

**Evidence links:** E1, E3, E4, E10, E11.

### 4.3 Metrics
Define primary metric before reporting it. Recommended: normalize market-adjusted role survival by TAM scale and report units. Include final RSI, holdout employment RMSE, topology R², enterprise-SMB divergence, condition ranking stability, BCa coverage, and paired effect sizes.

**Evidence links:** E2-E8.

### 4.4 Hardware and Reproducibility
Briefly state limited GPU/CPU environment only as reproducibility context, not as a contribution. Mention Python experiments, seeds 0-19, deterministic configuration, and released scripts.

**Evidence links:** E7.

---

## 5. Results

**Target length:** 650-800 words  
**Goal:** Report quantitative findings with calibrated caution. The Results section should not claim that APEX-II is empirically superior overall.

### 5.1 Main Results
Main table should include: primary metric, normalized primary metric, final RSI, holdout RMSE, topology R², and segment divergence.

Key claims to support:
- STAM/APEX-II produces a much larger primary score than APEX-I (`13787.40` vs `4922.41`), but this may reflect TAM scale.
- Final RSI shifts from APEX-I `0.773805` to APEX-II `0.649303`, closer to single-regime `0.634293`.
- Single-regime logistic wins external employment RMSE (`0.00608` vs `0.021094`).

**Evidence links:** E2, E3, E4, E9, E12.

### 5.2 Ablation Results
Ablation table:
- Full DAG/TAM: `13787.40`
- No DAG: `7887.01`
- No TAM: `8991.60`
- Uniform topology: `8271.16`
- Linear displacement: `9217.74`
- Expert priors: `13040.19`

Interpretation: DAG and TAM materially change simulation outputs, but causal attribution remains incomplete because full model bundles several extensions.

**Evidence links:** E1, E10, E11.

### 5.3 Segment and Scenario Analysis
Report Enterprise/SMB divergence and condition ranking stability. Treat Kendall tau `1.0` as internal consistency, not proof of external validity.

**Evidence links:** E6, E8.

### 5.4 Mechanism Test
Report topology R² honestly: full-model topology R² `0.065793` is modest. The current evidence supports “task topology matters somewhat,” not “topology is the primary determinant.”

**Evidence links:** E5.

---

## 6. Discussion

**Target length:** 450-600 words  
**Goal:** Interpret the tension between richer structure and weaker holdout RMSE.

Core argument: STAM is valuable because it exposes where APEX-I was underspecified: deal-size heterogeneity, subtask mechanisms, and market feedback. However, external validation currently favors a simpler temporal model, implying that APEX-II should be framed as a structured simulation and diagnostic model until stronger empirical calibration is demonstrated.

Discuss why TAM feedback may inflate the primary metric, why scenario ordering may be mechanically imposed, and why topology effects are smaller than hypothesized. Connect this to broader AI labor literature: expressive structural models require stronger validation than static exposure scores.

**Evidence links:** E4, E5, E6, E10, E12.

---

## 7. Limitations

**Target length:** 220-300 words  
**Goal:** Put all caveats here, clearly and specifically.

Limitations to include:
- The primary metric is not yet normalized enough to support external validity claims.
- The full model loses to single-regime logistic on holdout employment RMSE.
- Seed-level outputs do not by themselves create independent empirical observations.
- Subtask-level validation remains incomplete.
- Scenario rankings may partly reflect construction assumptions.
- TAM feedback may mechanically inflate survival-value outputs.

**Evidence links:** E4, E5, E6, E7, E10, E12.

---

## 8. Conclusion

**Target length:** 150-220 words  
**Goal:** Close with a precise contribution and a restrained claim.

State that APEX-II/STAM extends APEX-I from a single aggregate RSI into a deal-size-stratified, empirically calibrated, task-coupled, TAM-aware simulation framework. The defensible conclusion is that APEX-II produces differentiated Enterprise/SMB and scenario-conditioned trajectories and reveals major sensitivity to DAG and TAM assumptions. Future work should normalize the primary estimand, retune baselines under equal calibration budgets, and validate subtask-level mechanisms against independent labor-market and workflow data.

**Evidence links:** E1, E8, E10, E12.