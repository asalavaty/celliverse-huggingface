---
title: CelliVerse | ClustoCell PBMC3K Demo
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

# CelliVerse | ClustoCell PBMC3K Demo

`CelliVerse` is an R package for single-cell RNA sequencing (scRNA-seq) data analysis.

This Hugging Face Space provides a lightweight, browser-based demonstration of selected CelliVerse functionality.  
For the current version, the main interactive component is a compact **ClustoCell PBMC3K mini-demo** based on precomputed outputs.

## App organization

The Space is organized as:

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

This structure allows additional CelliVerse modules to be added later as new top-level tabs while keeping the current ClustoCell PBMC3K mini-demo grouped in one place.

## What this Space demonstrates

This demo lets users interactively inspect:

- PBMC3K metadata and annotation labels
- Seurat cluster assignments
- ClustoCell major clusters
- ClustoCell subclusters
- A UMAP generated using Seurat highly variable genes
- A UMAP generated using ClustoCell-derived marker genes
- Dataset-level ClustoCell-derived positive markers
- Marker tables for ClustoCell major clusters and subclusters
- Cross-tabulations between manual annotations, Seurat clusters, and ClustoCell outputs

## Scope

This Space is intended as a lightweight and user-friendly companion to the full CelliVerse R package.

It does **not** currently run the full CelliVerse or ClustoCell pipeline live.  
Instead, it visualizes precomputed PBMC3K outputs to make the method easier to inspect and understand in the browser.

## Related resources

- GitHub: https://github.com/asalavaty/celliverse
- Documentation: https://asalavaty.github.io/celliverse/
- CRAN: https://cran.r-project.org/package=celliverse
- Author: https://asalavaty.com/

## Installation of the full R package

Install the CRAN release:

```r
install.packages("celliverse")
```

Install the development version from GitHub:

```r
install.packages("remotes")
remotes::install_github("asalavaty/celliverse", build_vignettes = TRUE)
```

## Data files expected by this Space

Place the following files in the `data/` folder:

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

## Required columns

### `pbmc3k_metadata.csv`

```text
cells
manual_annot
seurat_clusters
ClustoCell_Clusters
ClustoCell_SubClusters
```

### `pbmc3k_Seurat_HVG_umap.csv`

```text
cells
umap_1
umap_2
```

### `pbmc3k_clustoCell_Markers_umap.csv`

```text
cell
clustoCellumap_1
clustoCellumap_2
```

### `clustoCell_derived_pbmc3k_markers.csv`

```text
marker
```

### Marker files

Each cluster/subcluster marker file should contain columns such as:

```text
Feature
Gini_Score
Purity
Rank
```

## Recommended citation statement

Please cite the CelliVerse package and associated manuscript/paper when using this resource.
