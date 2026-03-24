import os
import shutil
import random
from pathlib import Path

# ============ CONFIG ============
SRC_ROOT = Path(r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\yolo_rooftop")
DST_ROOT = Path(r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset")

TOTAL_IMAGES = 300        # change to 200–500 if needed
SEED = 42
# ================================

random.seed(SEED)

splits = ["train", "val", "test"]

# Create output dirs
for split in splits:
    (DST_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
    (DST_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)

# Collect all image paths with split info
all_images = []

for split in splits:
    img_dir = SRC_ROOT / "images" / split
    lbl_dir = SRC_ROOT / "labels" / split

    for img in img_dir.iterdir():
        if img.suffix.lower() not in [".jpg", ".png", ".jpeg"]:
            continue

        lbl = lbl_dir / (img.stem + ".txt")
        if not lbl.exists():
            continue  # safety

        all_images.append((split, img, lbl))

print(f"[INFO] Total available image-label pairs: {len(all_images)}")

# Sample
sampled = random.sample(
    all_images,
    min(TOTAL_IMAGES, len(all_images))
)

# Copy
counts = {s: 0 for s in splits}

for split, img, lbl in sampled:
    shutil.copy(img, DST_ROOT / "images" / split / img.name)
    shutil.copy(lbl, DST_ROOT / "labels" / split / lbl.name)
    counts[split] += 1

print("\n[DONE] Roboflow sample created")
for s in splits:
    print(f"  {s}: {counts[s]} images")
