import random
import shutil
from pathlib import Path

# ============== CONFIG ==============
IMAGES_DIR = Path(r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\yolo_rooftop\images\test")   # or train/val
LABELS_DIR = Path(r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\yolo_rooftop\labels\test")

OUT_DIR = Path(r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\roboflow_sample")
NUM_SAMPLES = 50   # change to 15–120 as needed
SEED = 42
# ====================================

random.seed(SEED)

OUT_IMAGES = OUT_DIR / "images"
OUT_LABELS = OUT_DIR / "labels"
OUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUT_LABELS.mkdir(parents=True, exist_ok=True)

# collect images
images = [
    p for p in IMAGES_DIR.iterdir()
    if p.suffix.lower() in [".jpg", ".png", ".jpeg", ".tif"]
]

print(f"[INFO] Found {len(images)} images")

# keep only images with labels
valid_pairs = []
for img in images:
    lbl = LABELS_DIR / (img.stem + ".txt")
    if lbl.exists():
        valid_pairs.append((img, lbl))

print(f"[INFO] Valid image-label pairs: {len(valid_pairs)}")

if len(valid_pairs) < NUM_SAMPLES:
    raise RuntimeError("Not enough labeled images to sample from")

# sample
samples = random.sample(valid_pairs, NUM_SAMPLES)

# copy
for img, lbl in samples:
    shutil.copy(img, OUT_IMAGES / img.name)
    shutil.copy(lbl, OUT_LABELS / lbl.name)

print(f"\n✅ Copied {NUM_SAMPLES} samples to '{OUT_DIR}'")
print("Upload this folder directly to Roboflow.")
