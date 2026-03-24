import os
import rasterio
from shapely.geometry import shape, box
import fiona
from tqdm import tqdm
from pathlib import Path

DIR_PATH = Path(__file__).resolve().parents[2]

IMG_DIR = DIR_PATH / "dataset" / "tiles_test"
SHAPEFILE_DIR = DIR_PATH / "dataset" / "shapefiles"
LABELS_DIR = DIR_PATH / "dataset" / "labels_raw"

def shp_to_yolo_boxes(
    image_dir,
    shp_path,
    label_out,
    class_mapper
):
    os.makedirs(label_out, exist_ok=True)

    raster_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ])

    if not raster_files:
        raise RuntimeError("No raster tiles found")

    with fiona.open(shp_path) as src:
        features = list(src)
        shp_crs = src.crs

    print("\n================ START ================")
    print(f"[INFO] Raster tiles found  : {len(raster_files)}")
    print(f"[INFO] SHP features loaded : {len(features)}")
    print(f"[INFO] SHP CRS             : {shp_crs}")

    if not features:
        raise RuntimeError("Shapefile has ZERO features")

    print("[INFO] SHP fields          :", features[0]["properties"].keys())

    total_written = 0
    tiles_with_boxes = 0

    for raster_name in tqdm(raster_files, desc="Processing tiles"):
        raster_path = os.path.join(image_dir, raster_name)
        label_path = os.path.join(
            label_out, os.path.splitext(raster_name)[0] + ".txt"
        )

        written_this_tile = 0

        with rasterio.open(raster_path) as ds:
            width, height = ds.width, ds.height
            inv = ~ds.transform
            tile_bounds = box(*ds.bounds)

            with open(label_path, "w") as out:
                for feat in features:
                    geom = shape(feat["geometry"])
                    if geom.is_empty or not geom.intersects(tile_bounds):
                        continue

                    geom = geom.intersection(tile_bounds)
                    if geom.is_empty:
                        continue

                    class_id = class_mapper(feat)
                    if class_id is None:
                        continue

                    minx, miny, maxx, maxy = geom.bounds

                    px_min, py_max = inv * (minx, miny)
                    px_max, py_min = inv * (maxx, maxy)

                    xmin = px_min / width
                    xmax = px_max / width
                    ymin = py_min / height
                    ymax = py_max / height

                    cx = (xmin + xmax) / 2
                    cy = (ymin + ymax) / 2
                    w = xmax - xmin
                    h = ymax - ymin

                    if w <= 0 or h <= 0:
                        continue

                    cx = max(0, min(1, cx))
                    cy = max(0, min(1, cy))
                    w  = max(0, min(1, w))
                    h  = max(0, min(1, h))

                    out.write(
                        f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
                    )

                    written_this_tile += 1
                    total_written += 1

        if written_this_tile > 0:
            tiles_with_boxes += 1

    print("\n================ SUMMARY ================")
    print(f"[SUMMARY] Total boxes written     : {total_written}")
    print(f"[SUMMARY] Tiles with rooftops    : {tiles_with_boxes}")
    print("========================================\n")


# ---------- CLASS MAPPERS ----------

def rooftop_class_mapper(feat):
    try:
        rt = int(feat["properties"]["Roof_type"])
    except Exception:
        return None

    if rt == 1:
        return 0  # RCC
    elif rt == 2:
        return 1  # Tiled
    elif rt == 3:
        return 2  # Tin
    elif rt == 4:
        return 3  # Others
    else:
        return None


def utility_class_mapper(feat):
    return 0


# ---------- RUN ----------

shp_to_yolo_boxes(
    image_dir=IMG_DIR,
    shp_path=SHAPEFILE_DIR,
    label_out=LABELS_DIR,
    class_mapper=rooftop_class_mapper
)
