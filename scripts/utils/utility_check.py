import os
import shutil

# ===== CONFIG =====
IMAGE_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\images\mungdanda\val"
LABEL_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\labels\mungdanda\utility\val"

OUT_IMG_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\images\mungdanda\utility_positive_val"
OUT_LBL_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\labels\mungdanda\utility\positives_val"
# ==================

os.makedirs(OUT_IMG_DIR, exist_ok=True)
os.makedirs(OUT_LBL_DIR, exist_ok=True)

count = 0
missing = 0

for label_file in os.listdir(LABEL_DIR):
    if not label_file.endswith(".txt"):
        continue    

    label_path = os.path.join(LABEL_DIR, label_file)

    # Skip empty labels
    if os.path.getsize(label_path) == 0:
        continue

    base = os.path.splitext(label_file)[0]

    # Find matching image (tif/tiff/jpg/png)
    image_found = False
    for ext in [".tif", ".tiff", ".jpg", ".png"]:
        img_path = os.path.join(IMAGE_DIR, base + ext)
        if os.path.exists(img_path):
            shutil.copy(img_path, os.path.join(OUT_IMG_DIR, os.path.basename(img_path)))
            image_found = True
            break

    if not image_found:
        print(f"[WARN] Image not found for {label_file}")
        missing += 1
        continue

    shutil.copy(label_path, os.path.join(OUT_LBL_DIR, label_file))
    count += 1

print(f"\n✅ Copied {count} positive samples")
print(f"⚠️ Missing images for {missing} labels")
