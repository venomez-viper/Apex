"""Generate validation figures for the APEX-II / STAM paper.

The script reads committed experiment outputs and writes publication-ready PNG
figures into ``figures/``. It is intentionally small and deterministic so the
paper figures can be regenerated during review.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
EXP_DIR = ROOT / "experiments"

CONDITION_ORDER = ["AFC", "C24", "CAB", "PAR", "HAO", "FAR"]
METHOD_ORDER = [
    "APEX-II",
    "APEX-I additive",
    "No DAG coupling",
    "No TAM feedback",
    "Expert-prior APEX-II",
    "Single-regime linear",
]


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.7,
        }
    )


def final_rsi_by_condition(summary: pd.DataFrame) -> None:
    df = summary[summary["method"].isin(METHOD_ORDER)].copy()
    grouped = (
        df.groupby(["method", "condition"], as_index=False)
        .agg(mean=("mean", "mean"), ci95=("ci95_half_width", "mean"))
    )

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    palette = {
        "APEX-II": "#2f5d8c",
        "APEX-I additive": "#8c3f2f",
        "No DAG coupling": "#6a8c2f",
        "No TAM feedback": "#7b4f9f",
        "Expert-prior APEX-II": "#c07c2f",
        "Single-regime linear": "#444444",
    }

    x = np.arange(len(CONDITION_ORDER))
    for method in METHOD_ORDER:
        part = grouped[grouped["method"] == method].set_index("condition")
        y = part.reindex(CONDITION_ORDER)["mean"].to_numpy()
        err = part.reindex(CONDITION_ORDER)["ci95"].to_numpy()
        ax.plot(x, y, marker="o", linewidth=2, label=method, color=palette[method])
        ax.fill_between(x, y - err, y + err, color=palette[method], alpha=0.12)

    ax.set_xticks(x)
    ax.set_xticklabels(CONDITION_ORDER)
    ax.set_ylabel("Final RSI")
    ax.set_xlabel("Adoption condition")
    ax.set_title("Final RSI by adoption condition")
    upper = float(np.nanmax(grouped["mean"] + grouped["ci95"]))
    ax.set_ylim(0.45, min(1.02, upper + 0.035))
    ax.legend(ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "final_rsi_by_condition.png")
    plt.close(fig)


def segment_gap_by_condition(summary: pd.DataFrame) -> None:
    df = summary[summary["method"] == "APEX-II"].copy()
    pivot = df.pivot_table(index="condition", columns="segment", values="mean", aggfunc="mean")
    pivot = pivot.reindex(CONDITION_ORDER)
    gap = pivot["enterprise"] - pivot["smb"]

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    colors = ["#2f5d8c" if value >= 0 else "#8c3f2f" for value in gap]
    ax.bar(CONDITION_ORDER, gap, color=colors)
    ax.axhline(0, color="#222222", linewidth=1)
    ax.set_ylabel("Enterprise minus SMB final RSI")
    ax.set_xlabel("Adoption condition")
    ax.set_title("Segment divergence under full APEX-II")
    for idx, value in enumerate(gap):
        ax.text(idx, value + (0.003 if value >= 0 else -0.006), f"{value:.3f}", ha="center", va="bottom" if value >= 0 else "top", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "segment_gap_by_condition.png")
    plt.close(fig)


def subtask_survival_profile(timeseries: pd.DataFrame) -> None:
    subtask_cols = [
        "subtask_discovery",
        "subtask_technical_demo",
        "subtask_poc_coordination",
        "subtask_rfp_response",
        "subtask_objection_handling",
        "subtask_champion_development",
    ]
    labels = ["Discovery", "Demo", "POC", "RFP", "Objection", "Champion"]
    final_q = int(timeseries["quarter"].max())
    df = timeseries[(timeseries["method"] == "APEX-II") & (timeseries["quarter"] == final_q)]
    matrix = (
        df.groupby("condition")[subtask_cols]
        .mean()
        .reindex(CONDITION_ORDER)
        .to_numpy()
    )

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    image = ax.imshow(matrix, aspect="auto", cmap="viridis", vmin=0.45, vmax=0.94)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(CONDITION_ORDER)))
    ax.set_yticklabels(CONDITION_ORDER)
    ax.set_title(f"Subtask survival profile at quarter {final_q}")
    ax.set_xlabel("Presales subtask")
    ax.set_ylabel("Adoption condition")
    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Mean subtask RSI")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "subtask_survival_profile.png")
    plt.close(fig)


def coverage_and_calibration(metrics: dict[str, float]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))

    coverage_labels = ["10 seeds", "20 seeds"]
    coverage_values = [
        metrics["bca_like_coverage_n10"],
        metrics["bca_like_coverage_n20"],
    ]
    axes[0].bar(coverage_labels, coverage_values, color=["#8c3f2f", "#2f5d8c"])
    axes[0].axhline(0.95, color="#333333", linestyle="--", linewidth=1, label="0.95 target")
    axes[0].set_ylim(0.80, 1.00)
    axes[0].set_ylabel("Coverage")
    axes[0].set_title("Seed-count coverage check")
    axes[0].legend(frameon=False)
    for idx, value in enumerate(coverage_values):
        axes[0].text(idx, value + 0.006, f"{value:.3f}", ha="center", fontsize=8)

    rmse_labels = ["Expert priors", "Calibrated fixture"]
    rmse_values = [metrics["expert_rmse"], metrics["calibrated_rmse"]]
    axes[1].bar(rmse_labels, rmse_values, color=["#c07c2f", "#7b4f9f"])
    axes[1].set_ylabel("RMSE")
    axes[1].set_title("Calibration stress test")
    for idx, value in enumerate(rmse_values):
        axes[1].text(idx, value + 0.003, f"{value:.3f}", ha="center", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "coverage_and_calibration.png")
    plt.close(fig)


def bic_model_ranking(comparison: pd.DataFrame) -> None:
    df = comparison.sort_values("negative_bic", ascending=True).copy()
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    y = np.arange(len(df))
    ax.barh(y, df["negative_bic"], color="#2f5d8c")
    ax.set_yticks(y)
    ax.set_yticklabels(df["method"])
    ax.set_xlabel("Negative BIC")
    ax.set_title("Model ranking by negative BIC")
    for idx, value in enumerate(df["negative_bic"]):
        ax.text(value, idx, f" {value:.0f}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "bic_model_ranking.png")
    plt.close(fig)


def main() -> None:
    _style()
    FIG_DIR.mkdir(exist_ok=True)

    summary = pd.read_csv(EXP_DIR / "apex2_final_rsi_summary.csv")
    timeseries = pd.read_csv(EXP_DIR / "apex2_results_timeseries.csv")
    comparison = pd.read_csv(EXP_DIR / "apex2_model_comparison.csv")
    metrics = json.loads((EXP_DIR / "apex2_metrics.json").read_text(encoding="utf-8"))

    final_rsi_by_condition(summary)
    segment_gap_by_condition(summary)
    subtask_survival_profile(timeseries)
    coverage_and_calibration(metrics)
    bic_model_ranking(comparison)


if __name__ == "__main__":
    main()
