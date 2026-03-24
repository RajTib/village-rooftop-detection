import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm


# ================= CONFIG =================
DIR_PATH = Path(__file__).resolve().parents[2]
IMAGES_ALL = DIR_PATH / "dataset" / "tiles_rgb"
LABELS_ALL = DIR_PATH / "dataset" / "labels_raw"

OUT_ROOT = DIR_PATH / "dataset"

TRAIN_RATIO = 0.7
VAL_RATIO   = 0.2
TEST_RATIO  = 0.1

SEED = 42
# ==========================================

random.seed(SEED)

images_all = Path(IMAGES_ALL)
labels_all = Path(LABELS_ALL)
out_root   = Path(OUT_ROOT)

# Sanity checks
if not images_all.exists():
    raise RuntimeError(f"Images folder not found: {images_all}")

if not labels_all.exists():
    raise RuntimeError(f"Labels folder not found: {labels_all}")

print("[INFO] Images folder :", images_all.resolve())
print("[INFO] Labels folder :", labels_all.resolve())

# Create output dirs
for split in ["train", "val", "test"]:
    (out_root / "images" / split).mkdir(parents=True, exist_ok=True)
    (out_root / "labels" / split).mkdir(parents=True, exist_ok=True)

# Collect images (NOW WITH .tif SUPPORT)
images = sorted([
    p for p in images_all.iterdir()
    if p.is_file() and p.suffix.lower() in [".jpg", ".png", ".jpeg", ".tif", ".tiff"]
])

print(f"[INFO] Total images found: {len(images)}")

if len(images) == 0:
    raise RuntimeError("No images found. Check path or extensions.")

# Shuffle
random.shuffle(images)

n_total = len(images)
n_train = int(n_total * TRAIN_RATIO)
n_val   = int(n_total * VAL_RATIO)

splits = {
    "train": images[:n_train],
    "val":   images[n_train:n_train + n_val],
    "test":  images[n_train + n_val:]
}

# Copy files with progress bars
for split, imgs in splits.items():
    print(f"\n[INFO] Copying {split} split ({len(imgs)} images)")
    copied = 0
    skipped = 0

    for img_path in tqdm(imgs, desc=f"{split}"):
        label_path = labels_all / (img_path.stem + ".txt")

        if not label_path.exists():
            skipped += 1
            continue

        shutil.copy(img_path, out_root / "images" / split / img_path.name)
        shutil.copy(label_path, out_root / "labels" / split / label_path.name)
        copied += 1

    print(f"[DONE] {split}: copied={copied}, skipped(no label)={skipped}")

print("\n✅ Dataset split complete")
