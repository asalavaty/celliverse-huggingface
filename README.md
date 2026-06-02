---
title: CelliVerse
emoji: 🧬
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
license: gpl-3.0
short_description: CelliVerse ClustoCell PBMC3K demo
tags:
  - single-cell
  - scRNA-seq
  - bioinformatics
  - gradio
  - clustocell
  - celliverse
---

# CelliVerse Hugging Face Space

[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/asalavaty/celliverse)
[![CRAN status](https://www.r-pkg.org/badges/version/celliverse?color=blue)](https://cran.r-project.org/package=celliverse)
[![License: GPL-3](https://img.shields.io/badge/License-GPL--3-blue.svg)](LICENSE)

This repository contains the source code and static demo assets for the **CelliVerse Hugging Face Space**:

**https://huggingface.co/spaces/asalavaty/celliverse**

The Space provides a lightweight, browser-based companion to the [`celliverse`](https://cran.r-project.org/package=celliverse) R package. The current version focuses on a compact **ClustoCell PBMC3K mini-demo** using precomputed outputs, making selected CelliVerse/ClustoCell results easier to inspect without installing or running the full R package locally.

---

## About CelliVerse

`CelliVerse` is an R package for single-cell RNA sequencing (scRNA-seq) data analysis. It provides functionality for clustering cells, identifying markers for predefined clusters, subclustering major cell populations, discovering markers within custom-selected subsets of cells, analyzing cluster similarity, and generating intuitive visualizations.

The full R package is available from:

- **CRAN:** https://cran.r-project.org/package=celliverse
- **GitHub:** https://github.com/asalavaty/celliverse
- **Documentation:** https://asalavaty.github.io/celliverse/

---

## About this Space

This Hugging Face Space is designed as a lightweight, interactive demonstration layer for CelliVerse. It is not intended to replace the full R package, full reproducibility scripts, or package documentation.

The current Space is organized as:

```text
Overview
ClustoCell PBMC3K
  ├── UMAP explorer
  ├── Cluster/subcluster markers
  ├── Dataset-level markers
  ├── Cluster summaries
  └── Reproducibility
About
```

---

## Current demo: ClustoCell PBMC3K

The current app uses precomputed PBMC3K outputs to demonstrate selected ClustoCell results interactively.

The demo allows users to inspect:

- PBMC3K metadata and manual annotation labels
- Seurat cluster assignments
- ClustoCell major clusters
- ClustoCell subclusters
- A UMAP generated using Seurat highly variable genes
- A UMAP generated using ClustoCell-derived marker genes
- Dataset-level ClustoCell-derived positive markers
- Marker tables for ClustoCell major clusters and subclusters
- Cross-tabulations between manual annotations, Seurat clusters, and ClustoCell outputs

---

## Scope and limitations

This Space currently uses precomputed outputs for fast and stable browser-based exploration.

It does **not** currently:

- run the full CelliVerse R package live,
- run full ClustoCell clustering from raw scRNA-seq data,
- process user-uploaded Seurat objects,
- replace the full R package workflow,
- replace the official documentation or reproducibility scripts.

For complete functionality, users should install and use the full `celliverse` R package.

---

## Repository structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   └── celliverse_logo.png
├── data/
│   ├── pbmc3k_metadata.csv
│   ├── pbmc3k_Seurat_HVG_umap.csv
│   ├── pbmc3k_clustoCell_Markers_umap.csv
│   ├── clustoCell_derived_pbmc3k_markers.csv
│   └── markers/
│       ├── Cluster_C1_Markers.csv
│       ├── Cluster_C2_Markers.csv
│       ├── ...
│       └── Cluster_C5_Sub2_Markers.csv
└── scripts/
    └── check_input_files.py
```

---

## Expected input files

The app expects the following precomputed files in the `data/` directory:

```text
data/
  pbmc3k_metadata.csv
  pbmc3k_Seurat_HVG_umap.csv
  pbmc3k_clustoCell_Markers_umap.csv
  clustoCell_derived_pbmc3k_markers.csv
  markers/
    Cluster_C1_Markers.csv
    Cluster_C2_Markers.csv
    Cluster_C3_Markers.csv
    Cluster_C4_Markers.csv
    Cluster_C5_Markers.csv
    Cluster_C1_Sub1_Markers.csv
    Cluster_C1_Sub2_Markers.csv
    Cluster_C2_Sub1_Markers.csv
    Cluster_C2_Sub2_Markers.csv
    Cluster_C3_Sub1_Markers.csv
    Cluster_C3_Sub2_Markers.csv
    Cluster_C4_Sub1_Markers.csv
    Cluster_C4_Sub2_Markers.csv
    Cluster_C4_Sub3_Markers.csv
    Cluster_C4_Sub4_Markers.csv
    Cluster_C5_Sub1_Markers.csv
    Cluster_C5_Sub2_Markers.csv
```

### Required columns

`pbmc3k_metadata.csv`

```text
cells
manual_annot
seurat_clusters
ClustoCell_Clusters
ClustoCell_SubClusters
```

`pbmc3k_Seurat_HVG_umap.csv`

```text
cells
umap_1
umap_2
```

`pbmc3k_clustoCell_Markers_umap.csv`

```text
cell
clustoCellumap_1
clustoCellumap_2
```

`clustoCell_derived_pbmc3k_markers.csv`

```text
marker
```

Cluster and subcluster marker files should contain columns such as:

```text
Feature
Gini_Score
Purity
Rank
```

---

## Local development

Create a local Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Validate the expected input files:

```bash
python scripts/check_input_files.py
```

Run the app locally:

```bash
python app.py
```

Then open the local Gradio URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

---

## Deployment

This repository is intended to sync with the public Hugging Face Space:

```text
asalavaty/celliverse
```

The Hugging Face Space configuration is defined in the YAML metadata block at the top of this `README.md` file. The app itself is launched from:

```text
app.py
```

The Space uses the Gradio SDK and is deployed as a lightweight Python application.

---

## Installing the full CelliVerse R package

Install the CRAN release:

```r
install.packages("celliverse")
```

Install the development version from GitHub:

```r
install.packages("remotes")
remotes::install_github("asalavaty/celliverse", build_vignettes = TRUE)
```

Open the package vignette from R:

```r
browseVignettes("celliverse")
```

---

## Citation

Please cite the CelliVerse package and its associated manuscript/paper when using this resource.

You can also retrieve package citation information in R:

```r
citation("celliverse")
```

---

## Developer

CelliVerse was developed by **Adrian Salavaty** with advice from **Ramyar Molania**.

Developer links:

- Website: https://asalavaty.com/
- GitHub: https://github.com/asalavaty
- LinkedIn: https://www.linkedin.com/in/asalavaty

---

## Issues and feedback

For issues, bugs, suggestions, or feature requests related to the full CelliVerse R package, please use the main CelliVerse GitHub issue tracker:

https://github.com/asalavaty/celliverse/issues

For issues specific to this Hugging Face Space, please use the issue tracker of this repository.

---

## License

This repository follows the same license as the CelliVerse R package: **GPL-3**.
