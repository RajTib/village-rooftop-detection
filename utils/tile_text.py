import argparse
import os
import glob

import rasterio
from rasterio.windows import bounds as window_bounds
from shapely.geometry import shape, box
import fiona


def shp_to_yolo_boxes(image_dir, shp_dir, label_out):
    os.makedirs(label_out, exist_ok=True)

    rasters = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ]

    shp_files = glob.glob(os.path.join(shp_dir, "*.shp"))

    for raster_name in rasters:
        raster_path = os.path.join(image_dir, raster_name)
        label_path = os.path.join(
            label_out, os.path.splitext(raster_name)[0] + ".txt"
        )

        with rasterio.open(raster_path) as ds:
            width, height = ds.width, ds.height
            transform = ds.transform
            inv_transform = ~transform

            # Tile bounds in world coords
            tile_bounds = box(*ds.bounds)

            written = 0

            with open(label_path, "w") as out:
                for shp in shp_files:
                    with fiona.open(shp) as src:
                        for feat in src:
                            geom = shape(feat["geometry"])
                            if geom.is_empty:
                                continue

                            # 🚨 KEY STEP: intersection test
                            if not geom.intersects(tile_bounds):
                                continue

                            # Clip geometry to tile
                            clipped = geom.intersection(tile_bounds)
                            if clipped.is_empty:
                                continue

                            minx, miny, maxx, maxy = clipped.bounds

                            # World → pixel
                            px_min, py_max = inv_transform * (minx, miny)
                            px_max, py_min = inv_transform * (maxx, maxy)

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

                            out.write(
                                f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
                            )
                            written += 1

            # Optional: remove empty label files
            if written == 0:
                os.remove(label_path)


def parse_opt():
    p = argparse.ArgumentParser()
    p.add_argument("--imagepath", required=True)
    p.add_argument("--shapepath", required=True)
    p.add_argument("--labelout", required=True)
    return p.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    shp_to_yolo_boxes(opt.imagepath, opt.shapepath, opt.labelout)
