import os
import shutil

# ================= CONFIG =================

VILLAGES = {
    "mungdanda": {
        "images": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\images\Mungdanda",
        "labels": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\labels\Mungdanda\rooftops"
    },
    "badetumnar": {
        "images": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\images\Badetumnar",
        "labels": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\labels\Badetumnar\rooftops"
    },
    "nagul": {
        "images": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\images\Nagul",
        "labels": r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\labels\Nagul\rooftops"
    }
}

OUT_IMAGES = r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\merged\utilities\images"
OUT_LABELS = r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\merged\utilities\labels"

# =========================================

os.makedirs(OUT_IMAGES, exist_ok=True)
os.makedirs(OUT_LABELS, exist_ok=True)

copied = 0
skipped = 0

for village, paths in VILLAGES.items():
    img_dir = paths["images"]
    lbl_dir = paths["labels"]

    for img_name in os.listdir(img_dir):
        if not img_name.lower().endswith((".tif", ".jpg", ".png")):
            continue

        base = os.path.splitext(img_name)[0]
        lbl_name = base + ".txt"

        img_path = os.path.join(img_dir, img_name)
        lbl_path = os.path.join(lbl_dir, lbl_name)

        if not os.path.exists(lbl_path):
            skipped += 1
            continue

        new_base = f"{village}_{base}"
        new_img = new_base + os.path.splitext(img_name)[1]
        new_lbl = new_base + ".txt"

        shutil.copy2(img_path, os.path.join(OUT_IMAGES, new_img))
        shutil.copy2(lbl_path, os.path.join(OUT_LABELS, new_lbl))

        copied += 1

print("\n================ DONE ================")
print(f"Images+labels copied : {copied}")
print(f"Skipped (no match)   : {skipped}")
print("=====================================\n")
