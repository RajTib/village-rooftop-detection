import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Validate Labels")
parser.add_argument("--label_dir", required=True, help="Enter the directory containing lables")

args = parser.parse_args()

LABEL_DIR = Path(args.label_dir)

total_files = 0
empty_files = 0
non_empty_files = 0
total_boxes = 0
examples = []

for fname in os.listdir(LABEL_DIR):
    if not fname.endswith(".txt"):
        continue

    total_files += 1
    path = os.path.join(LABEL_DIR, fname)

    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if len(lines) == 0:
        empty_files += 1
    else:
        non_empty_files += 1
        total_boxes += len(lines)
        if len(examples) < 10:
            examples.append((fname, len(lines)))

print("=== LABEL CHECK REPORT ===")
print(f"Total label files      : {total_files}")
print(f"Empty label files      : {empty_files}")
print(f"Non-empty label files  : {non_empty_files}")
print(f"Total bounding boxes   : {total_boxes}")

print("\nSample files with boxes:")
for f, c in examples:
    print(f"  {f} -> {c} boxes")
