import rasterio
import geopandas as gpd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==== PATHS ====
RASTER_DIR = PROJECT_ROOT / "dataset" / "tiles_test"
SHP_PATH   = PROJECT_ROOT / "dataset" / "shapefiles"
# ============================

# 🔍 Pick first raster file
raster_files = list(RASTER_DIR.glob("*.tif"))

if not raster_files:
    raise RuntimeError("No .tif files found in tiles_test")

RASTER_PATH = raster_files[0]  # take first tile

# Read raster CRS
with rasterio.open(RASTER_PATH) as src:
    raster_crs = src.crs

# Read shapefile CRS
gdf = gpd.read_file(SHP_PATH)
shp_crs = gdf.crs

print("=== CRS CHECK ===")
print(f"Raster file     : {RASTER_PATH.name}")
print(f"Raster CRS      : {raster_crs}")
print(f"Shapefile CRS   : {shp_crs}")

if raster_crs == shp_crs:
    print("\n✅ CRS MATCHES — you are good to generate labels.")
else:
    print("\n❌ CRS MISMATCH — reproject SHP to raster CRS before proceeding.")
