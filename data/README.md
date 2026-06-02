# Data folder

Put your precomputed PBMC3K CSV files here.

Expected files:

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

Do not rename the files unless you also update `app.py`.
