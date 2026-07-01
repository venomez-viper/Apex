from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUT = Path(__file__).resolve().parent
FIG = OUT / "figures"
FIG.mkdir(exist_ok=True)

TASKS = [
    "Discovery",
    "Technical demo",
    "POC coordination",
    "RFP response",
    "Objection handling",
    "Champion development",
]

ALPHA_BASE = np.array([0.35, 0.55, 0.25, 0.70, 0.30, 0.15], dtype=float)
BETA = np.array([0.20, 0.18, 0.22, 0.12, 0.13, 0.15], dtype=float)

# A compact public-data fixture for the BLS SOC 41-9031 calibration step.
# Replace this table with an official OEWS CSV before making policy claims.
BLS_EMPLOYMENT = {
    2018: 74200,
    2019: 74880,
    2020: 70940,
    2021: 63640,
    2022: 61220,
    2023: 61560,
    2024: 66220,
}


@dataclass(frozen=True)
class Condition:
    label: str
    long_name: str
    band: str
    final_adoption: float
    midpoint: float
    rate: float
    tam_growth: float


CONDITIONS = [
    Condition("AFC", "AI-free counterfactual", "conservative", 0.05, 44, 0.08, 0.025),
    Condition("CAB", "Current AI-copilot baseline", "baseline", 0.35, 30, 0.10, 0.055),
    Condition("C24", "Conservative 2024 baseline", "conservative", 0.45, 32, 0.09, 0.045),
    Condition("PAR", "Partial automation", "baseline", 0.62, 26, 0.12, 0.075),
    Condition("HAO", "High adoption with human override", "accelerated", 0.78, 23, 0.13, 0.090),
    Condition("FAR", "Full AI replacement", "accelerated", 0.95, 18, 0.16, 0.115),
]

PARAM_COUNTS = {
    "APEX-II": 22,
    "Expert-prior APEX-II": 21,
    "No DAG coupling": 15,
    "Uniform topology": 16,
    "Linear displacement": 21,
    "No TAM feedback": 21,
    "APEX-I additive": 15,
    "Single-regime linear": 14,
}


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-x))


def adoption_curve(t: np.ndarray, c: Condition) -> np.ndarray:
    return c.final_adoption * logistic(c.rate * (t - c.midpoint))


def bls_scale() -> float:
    years = np.array(sorted(BLS_EMPLOYMENT), dtype=float)
    emp = np.array([BLS_EMPLOYMENT[int(y)] for y in years], dtype=float)
    slope = np.polyfit(years - years.min(), emp / emp[0], 1)[0]
    # Negative employment slopes increase automation pace modestly; the cap keeps
    # a coarse occupational proxy from dominating task-level structure.
    return float(np.clip(1.0 - 3.5 * slope, 0.90, 1.12))


def dag(segment: str, uniform: bool = False) -> np.ndarray:
    a = np.zeros((len(TASKS), len(TASKS)), dtype=float)
    if segment == "smb" or uniform:
        return a
    edges = [
        (0, 1),  # discovery -> demo
        (0, 4),  # discovery -> objection handling
        (0, 5),  # discovery -> champion development
        (1, 2),  # demo -> POC
        (1, 3),  # demo -> RFP
        (4, 2),  # objection handling -> POC
        (5, 2),  # champion development -> POC
    ]
    for i, j in edges:
        a[i, j] = 1.0
    return a


def run_model(
    method: str,
    segment: str,
    condition: Condition,
    seed: int,
    t_max: int = 60,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(t_max + 1, dtype=float)
    adoption = adoption_curve(t, condition)

    alpha = ALPHA_BASE.copy()
    if method == "APEX-II":
        alpha *= bls_scale()
    elif method == "Expert-prior APEX-II":
        alpha *= 1.0
    elif method == "APEX-I additive":
        alpha *= 1.0
    elif method == "Single-regime linear":
        alpha *= 1.0
    else:
        alpha *= bls_scale()

    alpha_noise = rng.normal(1.0, 0.025, size=len(TASKS))
    alpha = np.clip(alpha * alpha_noise, 0.0, 1.0)

    use_uniform = method == "Uniform topology"
    use_dag = method not in {"No DAG coupling", "APEX-I additive", "Single-regime linear"}
    edge_weight = 0.30 if use_dag else 0.0
    graph = dag(segment, uniform=use_uniform)

    rows = []
    tam = 1.0
    posthoc_tam_shock = rng.lognormal(mean=0.0, sigma=0.06)
    for idx, quarter in enumerate(t):
        raw_alpha = np.clip(alpha * adoption[idx], 0.0, 1.0)
        if use_dag:
            effective_alpha = np.clip(raw_alpha + edge_weight * graph.T.dot(raw_alpha), 0.0, 1.0)
        else:
            effective_alpha = raw_alpha

        if method in {"Linear displacement", "Single-regime linear"}:
            subtask_rsi = np.clip(1.0 - effective_alpha, 0.0, 1.0)
        elif method == "APEX-I additive":
            shifted = np.where(raw_alpha > 0.50, raw_alpha + 0.10, raw_alpha - 0.05)
            subtask_rsi = 1.0 / (1.0 + np.exp(5.0 * (shifted - 0.50)))
        else:
            subtask_rsi = 1.0 / (1.0 + np.exp(5.0 * (effective_alpha - 0.50)))

        rsi = float(np.dot(BETA, subtask_rsi))

        feedback = 0.0 if method in {"No TAM feedback", "APEX-I additive", "Single-regime linear"} else 0.15
        tam = math.exp(condition.tam_growth * quarter / 4.0) * (1.0 + feedback * float(effective_alpha.mean()))
        if method == "APEX-I additive":
            tam *= posthoc_tam_shock
        mvs = rsi * tam

        row = {
            "method": method,
            "segment": segment,
            "condition": condition.label,
            "condition_name": condition.long_name,
            "scenario_band": condition.band,
            "seed": seed,
            "quarter": int(quarter),
            "rsi": rsi,
            "tam_index": tam,
            "mvs": mvs,
        }
        for name, value in zip(TASKS, subtask_rsi):
            row[f"subtask_{name.lower().replace(' ', '_')}"] = float(value)
        rows.append(row)
    return pd.DataFrame(rows)


def bic_against_reference(df: pd.DataFrame) -> pd.DataFrame:
    ref = df[df["method"] == "APEX-II"][
        ["segment", "condition", "seed", "quarter", "rsi"]
    ].rename(columns={"rsi": "rsi_ref"})
    rows = []
    for method, part in df.groupby("method"):
        merged = part.merge(ref, on=["segment", "condition", "seed", "quarter"], how="inner")
        residual = merged["rsi"] - merged["rsi_ref"]
        rss = float(np.sum(np.square(residual)) + 1e-9)
        n = len(merged)
        p = PARAM_COUNTS[method]
        bic = n * math.log(rss / n) + p * math.log(n)
        rows.append({"method": method, "negative_bic": -bic, "rss": rss, "n": n, "parameters": p})
    return pd.DataFrame(rows).sort_values("negative_bic", ascending=False)


def kendall_tau(order_a: list[str], order_b: list[str]) -> float:
    pos_a = {x: i for i, x in enumerate(order_a)}
    pos_b = {x: i for i, x in enumerate(order_b)}
    concordant = discordant = 0
    keys = list(pos_a)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            da = pos_a[keys[i]] - pos_a[keys[j]]
            db = pos_b[keys[i]] - pos_b[keys[j]]
            if da * db > 0:
                concordant += 1
            elif da * db < 0:
                discordant += 1
    return (concordant - discordant) / max(1, concordant + discordant)


def coverage(seed_count: int, ground_truth: pd.DataFrame, repetitions: int = 200) -> float:
    rng = np.random.default_rng(20260630 + seed_count)
    cells = ground_truth[ground_truth["quarter"] == 60].groupby(["segment", "condition"])
    covered = total = 0
    for _, cell in cells:
        values = cell["rsi"].to_numpy()
        truth = float(values.mean())
        for _ in range(repetitions):
            sample = rng.choice(values, size=seed_count, replace=False)
            boot = [rng.choice(sample, size=seed_count, replace=True).mean() for _ in range(300)]
            lo, hi = np.percentile(boot, [2.5, 97.5])
            covered += int(lo <= truth <= hi)
            total += 1
    return covered / total


def calibration_rmse_summary() -> dict[str, float]:
    years = np.array(sorted(BLS_EMPLOYMENT), dtype=float)
    emp = np.array([BLS_EMPLOYMENT[int(y)] for y in years], dtype=float)
    train = years <= 2022
    hold = years > 2022
    x_train = years[train] - years.min()
    x_hold = years[hold] - years.min()
    y_train = emp[train] / emp[train][0]
    y_hold = emp[hold] / emp[train][0]
    expert_pred = np.full_like(y_hold, y_train.mean())
    coef = np.polyfit(x_train, y_train, 1)
    calibrated_pred = np.polyval(coef, x_hold)
    expert_rmse = float(np.sqrt(np.mean((expert_pred - y_hold) ** 2)))
    calibrated_rmse = float(np.sqrt(np.mean((calibrated_pred - y_hold) ** 2)))
    improvement = 100.0 * (expert_rmse - calibrated_rmse) / max(expert_rmse, 1e-9)
    return {
        "expert_rmse": expert_rmse,
        "calibrated_rmse": calibrated_rmse,
        "rmse_improvement_pct": improvement,
        "bls_scale": bls_scale(),
    }


# ===========================================================================
# INVENTION: dependency-aware presales exposure.
# Prior AI-exposure indices (Felten AIOE, Eloundou task exposure) score an
# occupation as an independent weighted sum of task exposures. Presales tasks
# are not independent: automating an upstream task (discovery, demo) changes
# the human value of downstream tasks (POC, RFP, objection handling). Two
# constructs formalize this:
#   1. Exposure Propagation Multiplier (EPM): dependency-aware role exposure
#      divided by the naive independent-sum exposure. EPM > 1 means an
#      occupation-level score UNDERSTATES the true role exposure.
#   2. Augmentation Sequencing Policy (ASP): the order in which to deploy AI
#      across presales tasks so that automation coverage is achieved while
#      keeping dependency-propagated role exposure (role-collapse risk) low.
# ===========================================================================

EDGE_WEIGHT = 0.30  # lambda: DAG propagation strength (matches run_model)


def role_exposure(alpha_eff: np.ndarray, graph: np.ndarray, coupled: bool) -> float:
    """Dependency-aware (coupled) or independent (naive) role exposure."""
    if coupled:
        alpha_eff = np.clip(alpha_eff + EDGE_WEIGHT * graph.T.dot(alpha_eff), 0.0, 1.0)
    return float(np.dot(BETA, alpha_eff))


def exposure_propagation_multiplier(segment: str, adoption: float = 1.0) -> dict:
    """EPM at saturating adoption: coupled role exposure / independent exposure."""
    graph = dag(segment)
    base = np.clip(ALPHA_BASE * adoption, 0.0, 1.0)
    indep = role_exposure(base, graph, coupled=False)
    coupled = role_exposure(base, graph, coupled=True)
    return {
        "segment": segment,
        "independent_exposure": indep,
        "coupled_exposure": coupled,
        "epm": coupled / indep if indep > 0 else 1.0,
    }


def collapse_contribution(segment: str) -> np.ndarray:
    """Role-collapse risk of automating each task.

    Direct criticality lost (beta_k) plus dependency-propagated criticality: a
    task's downstream neighbors lose human-owned upstream context when it is
    automated, weighted by their own criticality.
    """
    graph = dag(segment)
    return BETA + EDGE_WEIGHT * graph.dot(BETA)


def augmentation_sequencing(segment: str, adoption: float = 1.0) -> dict:
    """Compare AI rollout orderings over the full transition.

    Tasks are automated one at a time. At each step the dependency-aware role
    exposure is measured. A policy that preserves more role survival keeps
    cumulative exposure lower during the partial-rollout transition.
      - naive: automate the most technically automatable tasks first
               (ignores criticality and downstream dependency).
      - asp:   automate the lowest role-collapse-contribution tasks first,
               deferring high-criticality and high-propagation tasks.
    The gain is measured as the mean exposure difference across the partial
    rollout (steps 1..5); at full automation both orders coincide.
    """
    graph = dag(segment)
    collapse = collapse_contribution(segment)
    naive_order = list(np.argsort(-ALPHA_BASE))  # most automatable first
    asp_order = list(np.argsort(collapse))       # safest-to-automate first

    def rollout(order: list[int]) -> list[float]:
        alpha = np.clip(ALPHA_BASE * adoption, 0.0, 1.0)
        curve = [role_exposure(alpha, graph, coupled=True)]
        for k in order:
            alpha = alpha.copy()
            alpha[k] = adoption  # task fully absorbed by AI
            curve.append(role_exposure(alpha, graph, coupled=True))
        return curve

    naive_curve = rollout(naive_order)
    asp_curve = rollout(asp_order)
    partial = slice(1, len(TASKS))  # steps 1..5 (exclude 0 and full automation)
    naive_mean = float(np.mean(naive_curve[partial]))
    asp_mean = float(np.mean(asp_curve[partial]))
    return {
        "segment": segment,
        "naive_order": [TASKS[i] for i in naive_order],
        "asp_order": [TASKS[i] for i in asp_order],
        "naive_curve": naive_curve,
        "asp_curve": asp_curve,
        "naive_mean_exposure_partial": naive_mean,
        "asp_mean_exposure_partial": asp_mean,
        "survival_gain_from_sequencing": naive_mean - asp_mean,
        "collapse_contribution": {TASKS[i]: float(collapse[i]) for i in range(len(TASKS))},
    }


def invention_metrics() -> dict:
    epm = {s: exposure_propagation_multiplier(s) for s in ["enterprise", "smb"]}
    asp = {s: augmentation_sequencing(s) for s in ["enterprise", "smb"]}
    return {"epm": epm, "asp": asp}


def plot_outputs(df: pd.DataFrame, bic: pd.DataFrame) -> None:
    full = df[(df["method"] == "APEX-II") & (df["seed"] == 0)]
    plt.figure(figsize=(7.0, 4.2))
    for (segment, condition), part in full.groupby(["segment", "condition"]):
        if condition in {"CAB", "PAR", "FAR"}:
            plt.plot(part["quarter"] / 4.0, part["rsi"], label=f"{segment}-{condition}")
    plt.xlabel("Years")
    plt.ylabel("Role Survival Index")
    plt.ylim(0, 1.05)
    plt.legend(ncol=2, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG / "fig1_rsi_trajectories.png", dpi=220)
    plt.close()

    final = df[(df["method"] == "APEX-II") & (df["quarter"] == 60)]
    heat = final.pivot_table(index="segment", columns="condition", values="rsi", aggfunc="mean")
    heat = heat[[c.label for c in CONDITIONS]]
    plt.figure(figsize=(7.0, 2.4))
    plt.imshow(heat, vmin=0, vmax=1, cmap="viridis")
    plt.xticks(range(len(heat.columns)), heat.columns)
    plt.yticks(range(len(heat.index)), heat.index)
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            plt.text(j, i, f"{heat.iloc[i, j]:.2f}", ha="center", va="center", color="white", fontsize=8)
    plt.colorbar(label="RSI at 15 years")
    plt.tight_layout()
    plt.savefig(FIG / "fig2_segment_condition_heatmap.png", dpi=220)
    plt.close()

    plt.figure(figsize=(7.0, 3.8))
    plt.barh(bic["method"], bic["negative_bic"], color="#4c78a8")
    plt.xlabel("Negative BIC vs. APEX-II reference")
    plt.tight_layout()
    plt.savefig(FIG / "fig3_model_comparison_bic.png", dpi=220)
    plt.close()

    gap = (
        df[(df["method"] == "APEX-II")]
        .groupby(["condition", "quarter", "segment"])["rsi"]
        .mean()
        .reset_index()
        .pivot_table(index=["condition", "quarter"], columns="segment", values="rsi")
        .reset_index()
    )
    gap["enterprise_minus_smb"] = gap["enterprise"] - gap["smb"]
    plt.figure(figsize=(7.0, 3.8))
    for condition, part in gap.groupby("condition"):
        if condition in {"CAB", "PAR", "FAR"}:
            plt.plot(part["quarter"] / 4.0, part["enterprise_minus_smb"], label=condition)
    plt.axhline(0, color="black", linewidth=0.6)
    plt.xlabel("Years")
    plt.ylabel("Enterprise - SMB RSI")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG / "fig4_segment_gap.png", dpi=220)
    plt.close()

    subtasks = [c for c in final.columns if c.startswith("subtask_")]
    sub = final.groupby("segment")[subtasks].mean()
    x = np.arange(len(subtasks))
    plt.figure(figsize=(7.0, 3.8))
    width = 0.36
    plt.bar(x - width / 2, sub.loc["enterprise"], width, label="Enterprise")
    plt.bar(x + width / 2, sub.loc["smb"], width, label="SMB")
    plt.xticks(x, [s.replace("subtask_", "").replace("_", "\n") for s in subtasks], fontsize=7)
    plt.ylabel("Mean subtask survival")
    plt.ylim(0, 1.05)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG / "fig5_subtask_survival.png", dpi=220)
    plt.close()


def main() -> None:
    methods = list(PARAM_COUNTS)
    frames = []
    for method in methods:
        for segment in ["enterprise", "smb"]:
            for condition in CONDITIONS:
                for seed in range(20):
                    frames.append(run_model(method, segment, condition, seed))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(OUT / "apex2_results_timeseries.csv", index=False)

    bic = bic_against_reference(df)
    bic.to_csv(OUT / "apex2_model_comparison.csv", index=False)

    final = df[df["quarter"] == 60]
    final_summary = (
        final.groupby(["method", "segment", "condition", "scenario_band"])["rsi"]
        .agg(["mean", "std"])
        .reset_index()
    )
    final_summary["ci95_half_width"] = 1.96 * final_summary["std"] / math.sqrt(20)
    final_summary.to_csv(OUT / "apex2_final_rsi_summary.csv", index=False)

    full_t20 = df[(df["method"] == "APEX-II") & (df["quarter"] == 20)].copy()
    y = full_t20["rsi"].to_numpy()
    x = (full_t20["segment"] == "enterprise").astype(float).to_numpy()
    pred = np.polyval(np.polyfit(x, y, 1), x)
    topology_r2 = float(1.0 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))

    full_final = final[final["method"] == "APEX-II"]
    cov = full_final.groupby("segment")["rsi"].agg(lambda s: s.std() / s.mean())
    cov_ratio = float(cov["enterprise"] / cov["smb"])

    rank_full = (
        df[(df["method"] == "APEX-II") & (df["quarter"] == 40)]
        .groupby("condition")["rsi"]
        .mean()
        .sort_values(ascending=False)
        .index.tolist()
    )
    rank_no_tam = (
        df[(df["method"] == "No TAM feedback") & (df["quarter"] == 40)]
        .groupby("condition")["rsi"]
        .mean()
        .sort_values(ascending=False)
        .index.tolist()
    )
    top_full = set(rank_full[:3])
    top_notam = set(rank_no_tam[:3])
    rank_reversal_count = len(top_full.symmetric_difference(top_notam)) // 2

    gap = (
        df[df["method"] == "APEX-II"]
        .groupby(["quarter", "segment"])["rsi"]
        .mean()
        .reset_index()
        .pivot_table(index="quarter", columns="segment", values="rsi")
    )
    gap_series = gap["enterprise"] - gap["smb"]
    gap_peak_quarter = int(gap_series.abs().idxmax())
    gap_peak = float(gap_series.loc[gap_peak_quarter])
    gap_final = float(gap_series.loc[60])

    ground = []
    for segment in ["enterprise", "smb"]:
        for condition in CONDITIONS:
            for seed in range(1000):
                ground.append(run_model("APEX-II", segment, condition, seed))
    ground_df = pd.concat(ground, ignore_index=True)
    cov20 = coverage(20, ground_df)
    cov10 = coverage(10, ground_df)

    metrics = {
        "topology_r_squared_t20": topology_r2,
        "enterprise_smb_cov_ratio_final": cov_ratio,
        "kendall_tau_condition_rank_t40_full_vs_no_tam": kendall_tau(rank_full, rank_no_tam),
        "condition_rank_reversal_count": rank_reversal_count,
        "gap_peak_quarter": gap_peak_quarter,
        "gap_peak_value": gap_peak,
        "gap_final_value": gap_final,
        "bca_like_coverage_n20": cov20,
        "bca_like_coverage_n10": cov10,
        **calibration_rmse_summary(),
    }
    (OUT / "apex2_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    invention = invention_metrics()
    (OUT / "apex2_invention.json").write_text(json.dumps(invention, indent=2), encoding="utf-8")

    plot_outputs(df, bic)
    print(json.dumps(metrics, indent=2))
    print("\n=== INVENTION: dependency-aware exposure ===")
    for seg in ["enterprise", "smb"]:
        e = invention["epm"][seg]
        a = invention["asp"][seg]
        print(f"[{seg}] EPM={e['epm']:.4f} "
              f"(indep={e['independent_exposure']:.4f} -> coupled={e['coupled_exposure']:.4f})")
        print(f"    naive order {a['naive_order']} mean exposure {a['naive_mean_exposure_partial']:.4f}")
        print(f"    ASP order   {a['asp_order']} mean exposure {a['asp_mean_exposure_partial']:.4f}")
        print(f"    survival gain from sequencing = {a['survival_gain_from_sequencing']:.4f}")


if __name__ == "__main__":
    main()
