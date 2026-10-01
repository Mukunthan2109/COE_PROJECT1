import os
import csv
import hashlib

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
METADATA_CSV = os.path.join(PROJECT_ROOT, 'dataset', 'metadata.csv')

def compute_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def check_dataset_integrity():
    print("Running AgriShield Dataset Integrity & Data Leakage Audit...")
    if not os.path.exists(METADATA_CSV):
        print(f"Error: Metadata CSV not found at {METADATA_CSV}")
        return

    hashes = {}
    duplicates = []
    missing_files = []
    class_counts = {}
    split_counts = {}
    source_counts = {}

    total_rows = 0
    with open(METADATA_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            img_id = row['image_id']
            img_rel_path = row['image_path']
            disease = row['disease_label']
            split_val = row.get('split', 'unassigned')
            source_val = row.get('source_type', 'unknown')

            class_counts[disease] = class_counts.get(disease, 0) + 1
            split_counts[split_val] = split_counts.get(split_val, 0) + 1
            source_counts[source_val] = source_counts.get(source_val, 0) + 1

            full_path = os.path.join(PROJECT_ROOT, img_rel_path)
            if not os.path.exists(full_path):
                missing_files.append((img_id, img_rel_path))
            else:
                f_hash = compute_file_hash(full_path)
                if f_hash in hashes:
                    duplicates.append((img_id, hashes[f_hash], img_rel_path))
                else:
                    hashes[f_hash] = img_id

    print("\n--- DATASET AUDIT RESULTS ---")
    print(f"Total Metadata Records: {total_rows}")
    print(f"Missing Files: {len(missing_files)}")
    print(f"Duplicate Image Hashes: {len(duplicates)}")

    if duplicates:
        print("Warning: Duplicate hashes found:")
        for dup in duplicates[:5]:
            print(f"  - {dup[0]} matches {dup[1]} ({dup[2]})")

    print("\n--- SPLIT DISTRIBUTION ---")
    for s_name, s_count in split_counts.items():
        print(f"  {s_name}: {s_count}")

    print("\n--- SOURCE TYPES ---")
    for src_name, src_count in source_counts.items():
        print(f"  {src_name}: {src_count}")

    print("\n--- CLASS BALANCE SUMMARY ---")
    for cls_name, cls_count in sorted(class_counts.items()):
        print(f"  {cls_name}: {cls_count}")

if __name__ == '__main__':
    check_dataset_integrity()
