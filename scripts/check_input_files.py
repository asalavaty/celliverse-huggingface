"""
Validate CelliVerse/ClustoCell PBMC3K demo input files before uploading to GitHub/Hugging Face.

Run locally from the root of the Space folder:

python scripts/check_input_files.py
"""

from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MARKERS = DATA / "markers"

required = {
    "pbmc3k_metadata.csv": ["cells", "manual_annot", "seurat_clusters", "ClustoCell_Clusters", "ClustoCell_SubClusters"],
    "pbmc3k_Seurat_HVG_umap.csv": ["cells", "umap_1", "umap_2"],
    "pbmc3k_clustoCell_Markers_umap.csv": ["cell", "clustoCellumap_1", "clustoCellumap_2"],
    "clustoCell_derived_pbmc3k_markers.csv": ["marker"],
}

ok = True
print("\nChecking required files...\n")

for filename, columns in required.items():
    path = DATA / filename
    if not path.exists():
        print(f"❌ Missing: {path}")
        ok = False
        continue
    try:
        df = pd.read_csv(path, nrows=5)
    except Exception as e:
        print(f"❌ Could not read {path}: {e}")
        ok = False
        continue
    missing_cols = [c for c in columns if c not in df.columns]
    if missing_cols:
        print(f"❌ {filename}: missing columns {missing_cols}")
        print(f"   Found columns: {list(df.columns)}")
        ok = False
    else:
        print(f"✅ {filename}")

print("\nChecking marker files...\n")
marker_files = sorted(MARKERS.glob("*.csv"))

if not marker_files:
    print(f"❌ No marker files found in {MARKERS}")
    ok = False
else:
    print(f"✅ Found {len(marker_files)} marker files")
    for path in marker_files:
        try:
            df = pd.read_csv(path, nrows=5)
        except Exception as e:
            print(f"❌ Could not read {path.name}: {e}")
            ok = False
            continue
        expected_marker_cols = ["Feature", "Gini_Score", "Purity", "Rank"]
        missing_cols = [c for c in expected_marker_cols if c not in df.columns]
        if missing_cols:
            print(f"⚠️  {path.name}: missing expected columns {missing_cols}; app may still show it, but sorting/search may be less informative.")
        else:
            print(f"✅ {path.name}")

logo = ROOT / "assets" / "celliverse_logo.png"
if logo.exists():
    print("\n✅ Logo found: assets/celliverse_logo.png")
else:
    print("\n⚠️  Optional logo not found: assets/celliverse_logo.png")

if ok:
    print("\nAll required files passed basic validation.\n")
    sys.exit(0)
else:
    print("\nSome checks failed. Fix the issues above before uploading to GitHub/Hugging Face.\n")
    sys.exit(1)
