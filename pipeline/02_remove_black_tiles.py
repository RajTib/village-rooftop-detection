import os
import shutil
from pathlib import Path
from PIL import Image, ImageStat
import argparse

parser = argparse.ArgumentParser(description="Remove black tiles")
parser.add_argument("--source_dir", required=True, help="Enter the tiles source path")
parser.add_argument("--target_dir", required=True, help="Enter the path for black tiles")

args = parser.parse_args()
source_dir = Path(args.source_dir)
target_dir = Path(args.target_dir)

# Increased threshold to catch noisy "near-black" tiles
threshold = 11.0

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

files = [f for f in os.listdir(source_dir) if f.lower().endswith('.tif')]
total_files = len(files)
moved_count = 0

print(f"Scanning {total_files} remaining files...")

for index, filename in enumerate(files):
    file_path = source_dir / filename

    try:
        with Image.open(file_path) as img:
            avg_brightness = ImageStat.Stat(img.convert('L')).mean[0]

            if avg_brightness < threshold:
                shutil.move(str(file_path), str(target_dir / filename))
                moved_count += 1

        # Simple progress update every 500 files
        if index % 500 == 0:
            percent = (index / total_files) * 100
            print(f"Progress: {percent:.1f}% | Moved so far: {moved_count}")

    except Exception:
        continue  # Skip errors like open files or corrupted headers

print(f"\nDone! Moved an additional {moved_count} images.")
print(f"If black images still remain, check their score with the diagnostic script.")
