import os
from pathlib import Path
import rasterio
from rasterio.windows import Window
from rasterio.windows import transform as window_transform
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description="Tile raster images")

parser.add_argument("--input", required=True, help="Path to input .tif files")
parser.add_argument("--output", required=True, help="path to output tiles directory")
parser.add_argument("--tile_size", type=int, default=640)

args = parser.parse_args()

input_tif_path = Path(args.input)
output_dir_path = Path(args.output)
tile_size = args.tile_size

# 🔥 Get project root dynamically (go up from this script)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def tile_raster(input_tif, output_dir, tile_size=640):
    os.makedirs(output_dir, exist_ok=True)

    with rasterio.open(input_tif) as src:
        meta = src.meta.copy()
        width = src.width
        height = src.height

        tile_id = 0

        for y in tqdm(range(0, height, tile_size), desc="Tiling rows"):
            for x in range(0, width, tile_size):
                w = min(tile_size, width - x)
                h = min(tile_size, height - y)

                window = Window(x, y, w, h)  # type: ignore

                transform = window_transform(window, src.transform)

                meta.update({
                    "height": h,
                    "width": w,
                    "transform": transform
                })

                tile_path = os.path.join(
                    output_dir,
                    f"tile_{tile_id:06d}.tif"
                )

                with rasterio.open(tile_path, "w", **meta) as dst:
                    dst.write(src.read(window=window))

                tile_id += 1

    print(f"\n[DONE] Generated {tile_id} tiles")


# ✅ Use project-relative paths
# input_tif_path = PROJECT_ROOT / "Training_dataSet_2" / "village.tif"
# output_dir_path = PROJECT_ROOT / "dataset" / "tiles_test"

tile_raster(input_tif=str(input_tif_path), output_dir=str(output_dir_path), tile_size=tile_size)
