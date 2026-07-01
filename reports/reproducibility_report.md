# Reproducibility Report

## Repository State

The repository keeps a polished artifact structure:

- `paper/` for IEEE paper source and PDF.
- `experiments/` for executable code and result tables.
- `figures/` for paper figures.
- `reports/` for human-readable reports and raw pipeline evidence.

## Running the Experiment

The main script is:

```bash
python experiments/apex2_simulation.py
```

The committed output files are already included, so a reader can inspect the
results without rerunning the simulation.

## Rebuilding the Paper

From the repository root:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
bibtex paper
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The paper uses IEEEtran conference mode and reads figures from `../figures/`.

## Key Files for Audit

| Purpose | File |
| --- | --- |
| Pipeline checkpoint | `reports/pipeline/checkpoint.json` |
| Stage 12 run output | `reports/pipeline/stage12_runs/results.json` |
| Stage 14 analysis | `reports/pipeline/stage14_analysis/analysis.md` |
| Stage 14 summary JSON | `reports/pipeline/stage14_analysis/experiment_summary.json` |
| Stage 20 quality report | `reports/pipeline/stage20_quality/quality_report.json` |
| Fabrication flags | `reports/pipeline/stage20_quality/fabrication_flags.json` |

## Reproducibility Boundary

The repository contains the code and generated artifacts. Full environment
reconstruction may still require installing the Python packages used by the
simulation environment. The paper claims are therefore tied to the committed
outputs and not to hidden or proprietary data.
