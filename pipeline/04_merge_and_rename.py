import os
import shutil
import argparse
from pathlib import Path

# ================= CONFIG =================

parser = argparse.ArgumentParser(description="Merge and Rename")
parser.add_argument("--input_root", required=True, help="Root folder containing village data")
parser.add_argument("--output_root", required=True, help="Output merged dataset folder")
parser.add_argument("--villages", nargs="+", required=True, help="List of village names")

args = parser.parse_args()

input_root = Path(args.input_root)
output_root = Path(args.output_root)
villages = args.villages

OUT_IMAGES = output_root / "images"
OUT_LABELS = output_root / "labels"

OUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUT_LABELS.mkdir(parents=True, exist_ok=True)

copied = 0
skipped = 0

for village in villages:
    img_dir = input_root / f"tiles_{village}"
    lbl_dir = input_root / f"labels_{village}"

    if not img_dir.exists() or not lbl_dir.exists():
        print(f"[WARNING] Missing folder for {village}")
        continue

    for img_path in img_dir.iterdir():
        if img_path.suffix.lower() not in [".tif", ".jpg", ".png"]:
            continue

        base = img_path.stem
        lbl_path = lbl_dir / f"{base}.txt"

        if not lbl_path.exists():
            skipped += 1
            continue

        new_base = f"{village}_{base}"
        new_img = OUT_IMAGES / f"{new_base}{img_path.suffix}"
        new_lbl = OUT_LABELS / f"{new_base}.txt"

        if new_img.exists() or new_lbl.exists():
            print(f"[SKIP] Already exists: {new_img.name}")
            continue

        shutil.copy2(img_path, new_img)
        shutil.copy2(lbl_path, new_lbl)

        copied += 1

print("\n================ DONE ================")
print(f"Images+labels copied : {copied}")
print(f"Skipped (no match)   : {skipped}")
print("=====================================\n")
