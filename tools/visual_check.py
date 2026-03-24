import os
import rasterio
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

IMAGE_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\images\mungdanda\utility_positive"
LABEL_DIR = r"D:\Teams\Ardra\TechfestIITB\GeoAI\3_training\labels\mungdanda\utility\positives"
OUT_DIR   = r"D:\Teams\Ardra\TechfestIITB\GeoAI\4_output\mungdanda\utilities"

os.makedirs(OUT_DIR, exist_ok=True)

def draw_yolo_boxes(ax, labels, w, h):
    for line in labels:
        cls, cx, cy, bw, bh = map(float, line.split())

        x = (cx - bw/2) * w
        y = (cy - bh/2) * h
        bw = bw * w
        bh = bh * h

        rect = Rectangle(
            (x, y), bw, bh,
            linewidth=2, edgecolor="red", facecolor="none"
        )
        ax.add_patch(rect)

for label_file in os.listdir(LABEL_DIR):
    if not label_file.endswith(".txt"):
        continue

    img_name = label_file.replace(".txt", ".tif")
    img_path = os.path.join(IMAGE_DIR, img_name)
    label_path = os.path.join(LABEL_DIR, label_file)

    if not os.path.exists(img_path):
        continue

    with open(label_path) as f:
        lines = f.readlines()

    if len(lines) == 0:
        continue  # skip empty labels

    with rasterio.open(img_path) as ds:
        img = ds.read([1,2,3])  # RGB
        img = img.transpose(1,2,0)
        h, w, _ = img.shape

    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(img)
    draw_yolo_boxes(ax, lines, w, h)
    ax.axis("off")

    out_path = os.path.join(OUT_DIR, img_name.replace(".tif", ".png"))
    plt.savefig(out_path, bbox_inches="tight", pad_inches=0)
    plt.close()

print("Visualization complete. Check dataset/vis_debug/")
