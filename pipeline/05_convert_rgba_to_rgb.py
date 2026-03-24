import rasterio
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description="Covert 4-band images to 3-band for YOLO")
parser.add_argument("--source", required=True, help="Enter the source for images")
parser.add_argument("--destination", required=True, help="Enter the destination for images")

args = parser.parse_args()

SRC = Path(args.source)
DST = Path(args.destination)

DST.mkdir(parents=True, exist_ok=True)

tifs = list(SRC.glob("*.tif"))
print(f"[INFO] Total TIFs found: {len(tifs)}")

for tif in tqdm(tifs, desc="Converting TIF → RGB JPG"):
    with rasterio.open(tif) as src:
        img = src.read()  # (bands, H, W)

        # Take first 3 bands (RGB)
        img = img[:3]

        # Convert to HWC
        img = np.transpose(img, (1, 2, 0))

        # Normalize to uint8 if needed
        if img.dtype != np.uint8:
            max_val = img.max()
            if max_val > 0:
                img = (255 * (img / max_val)).astype(np.uint8)
            else:
                img = img.astype(np.uint8)

    out = DST / tif.with_suffix(".jpg").name
    cv2.imwrite(str(out), img)

print("✅ RGB conversion complete")
