"""
CelliVerse Hugging Face Space
=============================

A lightweight Hugging Face/Gradio demo for CelliVerse with a ClustoCell PBMC3K mini-demo.

Expected data files:

data/
  pbmc3k_metadata.csv
  pbmc3k_Seurat_HVG_umap.csv
  pbmc3k_clustoCell_Markers_umap.csv
  clustoCell_derived_pbmc3k_markers.csv
  markers/
    Cluster_C1_Markers.csv
    Cluster_C2_Markers.csv
    ...
    Cluster_C5_Sub2_Markers.csv

Optional asset:

assets/
  celliverse_logo.png

Author: Adrian Salavaty
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Optional

import gradio as gr
import pandas as pd
import plotly.express as px


APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"
DATA_DIR = APP_DIR / "data"
MARKER_DIR = DATA_DIR / "markers"

LOGO_FILE = ASSETS_DIR / "celliverse_logo.png"

METADATA_FILE = DATA_DIR / "pbmc3k_metadata.csv"
SEURAT_HVG_UMAP_FILE = DATA_DIR / "pbmc3k_Seurat_HVG_umap.csv"
CLUSTOCELL_MARKER_UMAP_FILE = DATA_DIR / "pbmc3k_clustoCell_Markers_umap.csv"
DATASET_MARKERS_FILE = DATA_DIR / "clustoCell_derived_pbmc3k_markers.csv"


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize_cell_column(df: pd.DataFrame, possible_columns: list[str]) -> pd.DataFrame:
    """Standardize cell barcode column to 'cell'."""
    if df.empty:
        return df

    df = df.copy()

    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
    if unnamed_cols and "cell" not in df.columns and "cells" not in df.columns:
        df = df.rename(columns={unnamed_cols[0]: "cell"})

    for col in possible_columns:
        if col in df.columns:
            df = df.rename(columns={col: "cell"})
            break

    return df


def clean_cluster_label_from_filename(path: Path) -> str:
    stem = path.stem
    stem = stem.replace("Cluster_", "")
    stem = stem.replace("_Markers", "")
    stem = stem.replace("_Sub", "-Sub")
    return stem


def marker_file_sort_key(path: Path) -> tuple:
    label = clean_cluster_label_from_filename(path)
    numbers = [int(x) for x in re.findall(r"\d+", label)]
    return (label.startswith("C") is False, numbers, label)


metadata = normalize_cell_column(
    read_csv_if_exists(METADATA_FILE),
    possible_columns=["cells", "cell", "barcode"],
)

seurat_umap = normalize_cell_column(
    read_csv_if_exists(SEURAT_HVG_UMAP_FILE),
    possible_columns=["cells", "cell", "barcode"],
)

clustocell_umap = normalize_cell_column(
    read_csv_if_exists(CLUSTOCELL_MARKER_UMAP_FILE),
    possible_columns=["cell", "cells", "barcode"],
)

dataset_markers = read_csv_if_exists(DATASET_MARKERS_FILE)

marker_files = sorted(MARKER_DIR.glob("*.csv"), key=marker_file_sort_key)
marker_file_map = {clean_cluster_label_from_filename(path): path for path in marker_files}

REQUIRED_FILES = [
    METADATA_FILE,
    SEURAT_HVG_UMAP_FILE,
    CLUSTOCELL_MARKER_UMAP_FILE,
    DATASET_MARKERS_FILE,
]

missing_files = [str(p.relative_to(APP_DIR)) for p in REQUIRED_FILES if not p.exists()]
missing_marker_files = len(marker_files) == 0

data_ready = len(missing_files) == 0 and not missing_marker_files


def merge_umap_with_metadata(umap_df: pd.DataFrame, x_col: str, y_col: str) -> pd.DataFrame:
    if umap_df.empty or metadata.empty:
        return pd.DataFrame()
    if "cell" not in umap_df.columns or "cell" not in metadata.columns:
        return pd.DataFrame()

    merged = pd.merge(umap_df, metadata, on="cell", how="left")

    for col in ["manual_annot", "seurat_clusters", "ClustoCell_Clusters", "ClustoCell_SubClusters"]:
        if col not in merged.columns:
            merged[col] = "Not available"
        merged[col] = merged[col].astype(str)

    merged[x_col] = pd.to_numeric(merged[x_col], errors="coerce")
    merged[y_col] = pd.to_numeric(merged[y_col], errors="coerce")
    merged = merged.dropna(subset=[x_col, y_col])
    return merged


seurat_plot_df = merge_umap_with_metadata(seurat_umap, "umap_1", "umap_2")
clustocell_plot_df = merge_umap_with_metadata(
    clustocell_umap,
    "clustoCellumap_1",
    "clustoCellumap_2",
)

COLOR_OPTIONS = [
    "manual_annot",
    "seurat_clusters",
    "ClustoCell_Clusters",
    "ClustoCell_SubClusters",
]


def data_status_markdown() -> str:
    if data_ready:
        n_cells = metadata["cell"].nunique() if "cell" in metadata.columns else len(metadata)
        n_dataset_markers = len(dataset_markers)
        n_marker_tables = len(marker_files)
        return f"""
✅ **Data loaded successfully.**

- PBMC3K cells in metadata: **{n_cells:,}**
- Dataset-level ClustoCell-derived markers: **{n_dataset_markers:,}**
- Cluster/subcluster marker tables: **{n_marker_tables:,}**

This Space is ready for interactive exploration.
"""

    missing_txt = "\n".join([f"- `{x}`" for x in missing_files]) if missing_files else "- None"
    marker_txt = "- No marker CSV files found in `data/markers/`" if missing_marker_files else "- Marker files found"
    return f"""
⚠️ **The app is running, but the expected PBMC3K demo data are not fully available yet.**

Missing required files:

{missing_txt}

Marker-table status:

{marker_txt}

Please upload your CSV files to the expected locations, then restart/rebuild the Space.
"""


def make_umap_plot(umap_type: str, color_by: str, point_size: int, opacity: float):
    if umap_type == "Seurat HVG UMAP":
        df = seurat_plot_df
        x_col, y_col = "umap_1", "umap_2"
        title = "PBMC3K UMAP generated from Seurat HVGs"
    else:
        df = clustocell_plot_df
        x_col, y_col = "clustoCellumap_1", "clustoCellumap_2"
        title = "PBMC3K UMAP generated from ClustoCell-derived marker genes"

    if df.empty:
        fig = px.scatter(title="Data not available yet")
        fig.update_layout(
            annotations=[dict(
                text="Please upload the required PBMC3K CSV files.",
                showarrow=False,
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                font=dict(size=16),
            )]
        )
        return fig

    if color_by not in df.columns:
        color_by = "ClustoCell_Clusters"

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_by,
        hover_data=[
            "cell",
            "manual_annot",
            "seurat_clusters",
            "ClustoCell_Clusters",
            "ClustoCell_SubClusters",
        ],
        title=title,
    )
    fig.update_traces(marker=dict(size=point_size, opacity=opacity))
    fig.update_layout(
        height=650,
        legend_title_text=color_by,
        xaxis_title=x_col,
        yaxis_title=y_col,
    )
    return fig


def get_marker_table(marker_group: str, keyword: Optional[str], top_n: int) -> pd.DataFrame:
    if not marker_group or marker_group not in marker_file_map:
        return pd.DataFrame({"Message": ["No marker file selected or marker file not available."]})

    path = marker_file_map[marker_group]
    df = pd.read_csv(path)

    if keyword:
        keyword_lower = keyword.lower()
        text_cols = df.select_dtypes(include=["object"]).columns
        if len(text_cols) > 0:
            mask = False
            for col in text_cols:
                mask = mask | df[col].astype(str).str.lower().str.contains(keyword_lower, na=False)
            df = df[mask]

    if "Rank" in df.columns:
        df = df.sort_values("Rank", ascending=True)
    elif "Gini_Score" in df.columns:
        df = df.sort_values("Gini_Score", ascending=True)

    return df.head(top_n)


def get_dataset_markers(keyword: Optional[str], top_n: int) -> pd.DataFrame:
    if dataset_markers.empty:
        return pd.DataFrame({"Message": ["Dataset-level marker file not available."]})

    df = dataset_markers.copy()

    if keyword:
        keyword_lower = keyword.lower()
        text_cols = df.select_dtypes(include=["object"]).columns
        if len(text_cols) > 0:
            mask = False
            for col in text_cols:
                mask = mask | df[col].astype(str).str.lower().str.contains(keyword_lower, na=False)
            df = df[mask]

    return df.head(top_n)


def get_cell_count_summary(group_by: str) -> pd.DataFrame:
    if metadata.empty or group_by not in metadata.columns:
        return pd.DataFrame({"Message": ["Metadata not available or selected grouping column is missing."]})

    summary = (
        metadata
        .assign(**{group_by: metadata[group_by].astype(str)})
        .groupby(group_by, dropna=False)
        .size()
        .reset_index(name="n_cells")
        .sort_values("n_cells", ascending=False)
    )
    summary["percent"] = 100 * summary["n_cells"] / summary["n_cells"].sum()
    summary["percent"] = summary["percent"].round(2)
    return summary


def get_crosstab(row_group: str, column_group: str) -> pd.DataFrame:
    if metadata.empty or row_group not in metadata.columns or column_group not in metadata.columns:
        return pd.DataFrame({"Message": ["Metadata not available or selected columns are missing."]})

    tab = pd.crosstab(
        metadata[row_group].astype(str),
        metadata[column_group].astype(str),
        margins=True,
    )
    return tab.reset_index()


def download_current_marker_table(marker_group: str) -> Optional[str]:
    if not marker_group or marker_group not in marker_file_map:
        return None
    return str(marker_file_map[marker_group])


custom_css = """
.logo-card img {
    border-radius: 18px;
    max-height: 285px;
    object-fit: contain;
}
"""

with gr.Blocks(
    title="CelliVerse | ClustoCell PBMC3K Demo",
    theme=gr.themes.Soft(),
    css=custom_css,
) as demo:

    with gr.Tab("Overview"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown(
                    """
# CelliVerse

### An ecosystem for exploring the universe of single-cell data

`CelliVerse` is an R package for single-cell RNA-seq analysis. It provides functionality for clustering cells,
identifying markers for predefined clusters, subclustering major cell populations, discovering markers within
custom-selected subsets of cells, analyzing cluster similarity, and generating intuitive visualizations.

This Hugging Face Space currently provides a compact **ClustoCell PBMC3K mini-demo** based on
precomputed outputs. More CelliVerse functionality can be added as additional top-level tabs in the future.
"""
                )
                gr.Markdown(data_status_markdown())

            with gr.Column(scale=1, elem_classes=["logo-card"]):
                if LOGO_FILE.exists():
                    gr.Image(
                        value=str(LOGO_FILE),
                        label="CelliVerse logo",
                        show_label=False,
                        interactive=False,
                        height=285,
                    )
                else:
                    gr.Markdown("**CelliVerse logo**\n\nLogo file not found at `assets/celliverse_logo.png`.")

        gr.Markdown(
            """
## What this Space currently includes

- An interactive PBMC3K UMAP explorer
- A comparison of Seurat HVG-based and ClustoCell marker-based UMAPs
- Dataset-level ClustoCell-derived marker genes
- Major-cluster and subcluster marker tables
- Cluster summaries and cross-tabulations

## Important scope note

This Space does **not** currently run the full CelliVerse or ClustoCell pipeline live. It visualizes precomputed PBMC3K
outputs to make the method easier to inspect in the browser. For full functionality, please use the R package,
GitHub repository, and documentation.

## Links

- **GitHub:** https://github.com/asalavaty/celliverse
- **Documentation:** https://asalavaty.github.io/celliverse/
- **CRAN:** https://cran.r-project.org/package=celliverse
- **Author website:** https://asalavaty.com/
"""
        )

    with gr.Tab("ClustoCell PBMC3K"):
        gr.Markdown(
            """
# ClustoCell PBMC3K mini-demo

This section groups all current ClustoCell PBMC3K demo components. In future versions, additional CelliVerse
modules can be added as separate top-level tabs while keeping ClustoCell-specific content here.
"""
        )

        with gr.Tabs():
            with gr.Tab("UMAP explorer"):
                gr.Markdown(
                    """
## PBMC3K UMAP explorer

Use this tab to compare two precomputed PBMC3K UMAP views:

1. **Seurat HVG UMAP**: UMAP generated using Seurat highly variable genes.
2. **ClustoCell marker UMAP**: UMAP generated using the 657 dataset-level positive markers derived from ClustoCell clusters.

Both plots can be colored by manual annotations, Seurat clusters, ClustoCell clusters, or ClustoCell subclusters.
"""
                )
                with gr.Row():
                    umap_type = gr.Dropdown(
                        choices=["Seurat HVG UMAP", "ClustoCell marker UMAP"],
                        value="ClustoCell marker UMAP",
                        label="UMAP type",
                    )
                    color_by = gr.Dropdown(
                        choices=COLOR_OPTIONS,
                        value="ClustoCell_Clusters",
                        label="Color by",
                    )
                with gr.Row():
                    point_size = gr.Slider(minimum=2, maximum=10, value=5, step=1, label="Point size")
                    opacity = gr.Slider(minimum=0.2, maximum=1.0, value=0.8, step=0.1, label="Point opacity")

                plot_button = gr.Button("Generate UMAP")
                umap_plot = gr.Plot(label="Interactive UMAP")
                plot_button.click(make_umap_plot, inputs=[umap_type, color_by, point_size, opacity], outputs=umap_plot)

            with gr.Tab("Cluster/subcluster markers"):
                gr.Markdown(
                    """
## Marker explorer

This tab shows marker genes identified for ClustoCell major clusters and subclusters.

Expected marker files are placed in `data/markers/`.
"""
                )
                marker_choices = list(marker_file_map.keys())
                with gr.Row():
                    marker_group = gr.Dropdown(
                        choices=marker_choices,
                        value=marker_choices[0] if marker_choices else None,
                        label="Cluster or subcluster",
                    )
                    marker_keyword = gr.Textbox(label="Optional marker search", placeholder="Example: NKG7, CD3D, MS4A1")
                    marker_top_n = gr.Slider(minimum=5, maximum=100, value=20, step=5, label="Number of rows")

                marker_button = gr.Button("Show marker table")
                marker_output = gr.Dataframe(label="Marker table", interactive=False)
                marker_button.click(get_marker_table, inputs=[marker_group, marker_keyword, marker_top_n], outputs=marker_output)

                marker_download_button = gr.Button("Prepare selected marker CSV for download")
                marker_download = gr.File(label="Download selected marker CSV")
                marker_download_button.click(download_current_marker_table, inputs=marker_group, outputs=marker_download)

            with gr.Tab("Dataset-level markers"):
                gr.Markdown(
                    """
## Dataset-level ClustoCell-derived markers

This tab displays the set of positive marker genes derived from all ClustoCell clusters of the PBMC3K dataset.

In your current precomputed files, this corresponds to `clustoCell_derived_pbmc3k_markers.csv`.
"""
                )
                with gr.Row():
                    dataset_marker_keyword = gr.Textbox(label="Optional marker search", placeholder="Example: NKG7, GNLY, LYZ")
                    dataset_marker_top_n = gr.Slider(minimum=10, maximum=1000, value=100, step=10, label="Number of rows")

                dataset_marker_button = gr.Button("Show dataset-level markers")
                dataset_marker_output = gr.Dataframe(label="Dataset-level marker genes", interactive=False)
                dataset_marker_button.click(get_dataset_markers, inputs=[dataset_marker_keyword, dataset_marker_top_n], outputs=dataset_marker_output)

                gr.File(
                    value=str(DATASET_MARKERS_FILE) if DATASET_MARKERS_FILE.exists() else None,
                    label="Download dataset-level marker CSV",
                )

            with gr.Tab("Cluster summaries"):
                gr.Markdown(
                    """
## Cluster summaries

This tab summarizes the relationship between manual annotations, Seurat clusters,
ClustoCell major clusters, and ClustoCell subclusters.
"""
                )
                with gr.Row():
                    summary_group = gr.Dropdown(
                        choices=["manual_annot", "seurat_clusters", "ClustoCell_Clusters", "ClustoCell_SubClusters"],
                        value="ClustoCell_Clusters",
                        label="Summarize cells by",
                    )

                summary_button = gr.Button("Create cell-count summary")
                summary_output = gr.Dataframe(label="Cell-count summary", interactive=False)
                summary_button.click(get_cell_count_summary, inputs=summary_group, outputs=summary_output)

                gr.Markdown("### Cross-tabulation")
                with gr.Row():
                    row_group = gr.Dropdown(
                        choices=["manual_annot", "seurat_clusters", "ClustoCell_Clusters", "ClustoCell_SubClusters"],
                        value="ClustoCell_Clusters",
                        label="Rows",
                    )
                    column_group = gr.Dropdown(
                        choices=["manual_annot", "seurat_clusters", "ClustoCell_Clusters", "ClustoCell_SubClusters"],
                        value="manual_annot",
                        label="Columns",
                    )

                crosstab_button = gr.Button("Create cross-tabulation")
                crosstab_output = gr.Dataframe(label="Cross-tabulation", interactive=False)
                crosstab_button.click(get_crosstab, inputs=[row_group, column_group], outputs=crosstab_output)

            with gr.Tab("Reproducibility"):
                gr.Markdown(
                    """
## Reproducibility and scope

This mini-demo uses precomputed PBMC3K outputs for fast, stable, browser-based exploration.

### What this section currently does

- Displays precomputed PBMC3K UMAPs
- Shows manual annotations, Seurat clusters, ClustoCell clusters, and ClustoCell subclusters
- Displays ClustoCell-derived marker genes
- Summarizes cluster composition

### What this section does not currently do

- It does not run the full CelliVerse R package live.
- It does not run full ClustoCell clustering from raw scRNA-seq data.
- It does not process user-uploaded Seurat objects.
- It is not intended to replace the full R package, GitHub repository, documentation, or formal reproducibility scripts.

### Recommended citation statement

Please cite the CelliVerse package and associated manuscript/paper when using this resource.
"""
                )

    with gr.Tab("About"):
        gr.Markdown(
            """
# About the developer

**Adrian Salavaty** is a bioinformatician and systems biologist working across single-cell and spatial omics,
multi-omics data integration, network biology, machine learning-driven bioinformatics, and R package development.

CelliVerse was developed by Adrian Salavaty with advice from Ramyar Molania.

## Developer links

- Personal website: https://asalavaty.com/
- GitHub: https://github.com/asalavaty
- LinkedIn: https://www.linkedin.com/in/asalavaty
- CelliVerse GitHub repository: https://github.com/asalavaty/celliverse
- CelliVerse documentation: https://asalavaty.github.io/celliverse/
- CelliVerse CRAN page: https://cran.r-project.org/package=celliverse

## Contact and issues

For bugs, feature requests, and suggestions, please use the CelliVerse GitHub issues page:

https://github.com/asalavaty/celliverse/issues
"""
        )


if __name__ == "__main__":
    demo.launch()
