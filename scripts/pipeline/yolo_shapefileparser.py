import argparse
import os
import glob

import rasterio
from shapely.geometry import shape, box
import fiona
from tqdm import tqdm


def shp_to_yolo_boxes(image_dir, shp_dir, label_out):
    os.makedirs(label_out, exist_ok=True)

    raster_files = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ]

    shp_files = glob.glob(os.path.join(shp_dir, "*.shp"))

    print(f"[INFO] Tiles found      : {len(raster_files)}")
    print(f"[INFO] Shapefiles found : {len(shp_files)}")

    if not raster_files:
        raise RuntimeError("No rasters found")
    if not shp_files:
        raise RuntimeError("No shapefiles found")

    total_boxes = 0

    for raster_name in tqdm(raster_files, desc="Processing tiles"):
        raster_path = os.path.join(image_dir, raster_name)
        label_path = os.path.join(
            label_out, os.path.splitext(raster_name)[0] + ".txt"
        )

        written = 0

        with rasterio.open(raster_path) as ds:
            width, height = ds.width, ds.height
            inv = ~ds.transform
            rb = box(*ds.bounds)

            with open(label_path, "w") as out:
                for shp in shp_files:
                    with fiona.open(shp) as src:
                        for feat in src:
                            geom = shape(feat["geometry"])
                            if geom.is_empty or not geom.intersects(rb):
                                continue

                            geom = geom.intersection(rb)
                            if geom.is_empty:
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
                            w = max(0, min(1, w))
                            h = max(0, min(1, h))

                            out.write(f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n")
                            written += 1
                            total_boxes += 1

    print("\n[SUMMARY]")
    print(f"Total boxes written : {total_boxes}")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagepath", required=True)
    parser.add_argument("--shapepath", required=True)
    parser.add_argument("--labelout", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    shp_to_yolo_boxes(opt.imagepath, opt.shapepath, opt.labelout)
