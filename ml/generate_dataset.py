import os
import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
IMAGES_DIR = os.path.join(DATASET_DIR, 'images')
METADATA_CSV = os.path.join(DATASET_DIR, 'metadata.csv')

# Supported scope
CROP_DISEASES = [
    ("Tomato", "Healthy", "Tomato Healthy", "Seedling"),
    ("Tomato", "Leaf Spot", "Tomato Leaf Spot", "Vegetative"),
    ("Tomato", "Early Blight", "Tomato Early Blight", "Fruiting"),
    ("Potato", "Healthy", "Potato Healthy", "Vegetative"),
    ("Potato", "Late Blight", "Potato Late Blight", "Flowering"),
    ("Chili", "Healthy", "Chili Healthy", "Flowering"),
    ("Chili", "Leaf Curl", "Chili Leaf Curl", "Fruiting"),
]

REGIONS = ["North Zone", "South Zone", "Central Region", "East District", "West Valley"]

def draw_leaf_base(draw, size, leaf_color, stem_color):
    w, h = size
    # Draw leaf contour (ellipse/polygon hybrid)
    leaf_shape = [
        (w * 0.5, h * 0.1),
        (w * 0.85, h * 0.4),
        (w * 0.75, h * 0.8),
        (w * 0.5, h * 0.95),
        (w * 0.25, h * 0.8),
        (w * 0.15, h * 0.4),
    ]
    draw.polygon(leaf_shape, fill=leaf_color, outline=(20, 80, 20))
    # Draw central vein
    draw.line([(w * 0.5, h * 0.15), (w * 0.5, h * 0.9)], fill=stem_color, width=4)
    # Draw side veins
    for y_factor in [0.3, 0.45, 0.6, 0.75]:
        draw.line([(w * 0.5, h * y_factor), (w * 0.75, h * (y_factor + 0.08))], fill=stem_color, width=2)
        draw.line([(w * 0.5, h * y_factor), (w * 0.25, h * (y_factor + 0.08))], fill=stem_color, width=2)

def generate_crop_image(crop, disease, size=(256, 256), seed=0):
    np.random.seed(seed)
    w, h = size
    
    # Background - neutral soil/bench background
    bg_color = (210 + np.random.randint(-10, 10), 195 + np.random.randint(-10, 10), 180 + np.random.randint(-10, 10))
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    if disease == "Healthy":
        leaf_color = (40 + np.random.randint(-10, 10), 160 + np.random.randint(-15, 15), 40 + np.random.randint(-10, 10))
        stem_color = (80, 200, 80)
        draw_leaf_base(draw, size, leaf_color, stem_color)

    elif disease == "Leaf Spot":
        leaf_color = (50 + np.random.randint(-10, 10), 150 + np.random.randint(-15, 15), 35 + np.random.randint(-10, 10))
        stem_color = (70, 180, 70)
        draw_leaf_base(draw, size, leaf_color, stem_color)
        # Add multiple dark spots
        num_spots = np.random.randint(12, 25)
        for _ in range(num_spots):
            cx = np.random.randint(int(w * 0.25), int(w * 0.75))
            cy = np.random.randint(int(h * 0.2), int(h * 0.8))
            r = np.random.randint(4, 12)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 20, 10), outline=(60, 40, 20))

    elif disease == "Early Blight":
        leaf_color = (80 + np.random.randint(-10, 10), 140 + np.random.randint(-15, 15), 30 + np.random.randint(-10, 10))
        stem_color = (90, 160, 60)
        draw_leaf_base(draw, size, leaf_color, stem_color)
        # Add concentric brown lesions with yellow halo
        num_lesions = np.random.randint(4, 9)
        for _ in range(num_lesions):
            cx = np.random.randint(int(w * 0.3), int(w * 0.7))
            cy = np.random.randint(int(h * 0.25), int(h * 0.75))
            r_halo = np.random.randint(16, 26)
            r_core = np.random.randint(8, 14)
            # Yellow halo
            draw.ellipse([cx - r_halo, cy - r_halo, cx + r_halo, cy + r_halo], fill=(210, 190, 40))
            # Brown core
            draw.ellipse([cx - r_core, cy - r_core, cx + r_core, cy + r_core], fill=(70, 40, 20))

    elif disease == "Late Blight":
        leaf_color = (60 + np.random.randint(-10, 10), 130 + np.random.randint(-15, 15), 35 + np.random.randint(-10, 10))
        stem_color = (60, 140, 50)
        draw_leaf_base(draw, size, leaf_color, stem_color)
        # Large dark brown water-soaked necrotic patches
        for _ in range(np.random.randint(2, 5)):
            px = np.random.randint(int(w * 0.25), int(w * 0.65))
            py = np.random.randint(int(h * 0.25), int(h * 0.65))
            pw = np.random.randint(30, 60)
            ph = np.random.randint(30, 60)
            draw.ellipse([px, py, px + pw, py + ph], fill=(45, 30, 20))

    elif disease == "Leaf Curl":
        # Yellowish distorted leaf
        leaf_color = (160 + np.random.randint(-15, 15), 170 + np.random.randint(-15, 15), 40 + np.random.randint(-10, 10))
        stem_color = (180, 190, 60)
        draw_leaf_base(draw, size, leaf_color, stem_color)
        # Add wrinkled texture lines
        for _ in range(15):
            x1 = np.random.randint(int(w * 0.2), int(w * 0.8))
            y1 = np.random.randint(int(h * 0.2), int(h * 0.8))
            draw.arc([x1, y1, x1 + 30, y1 + 30], start=0, end=180, fill=(120, 130, 30), width=2)

    # Slight Gaussian blur to make shapes natural
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return img

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    metadata_rows = []
    image_counter = 1

    print("Generating demo crop leaf dataset...")
    for crop, symptom, disease_label, stage in CROP_DISEASES:
        # Generate 20 images per class
        for i in range(20):
            img_id = f"IMG_{image_counter:04d}"
            filename = f"{crop.lower()}_{symptom.lower().replace(' ', '_')}_{i+1:02d}.jpg"
            rel_path = os.path.join('dataset', 'images', filename)
            abs_path = os.path.join(IMAGES_DIR, filename)

            img = generate_crop_image(crop, symptom, seed=image_counter * 7 + i)
            img.save(abs_path, quality=90)

            region = REGIONS[i % len(REGIONS)]
            metadata_rows.append({
                'image_id': img_id,
                'image_path': rel_path,
                'crop': crop,
                'symptom': symptom,
                'disease_label': disease_label,
                'location_region': region,
                'crop_stage': stage,
                'source_type': 'project_created',
                'expert_validation': 'verified' if i < 15 else 'pending',
                'license_or_source_note': 'Project-created synthetic/demo dataset for Review 1 MVP evaluation'
            })
            image_counter += 1

    # Write metadata.csv
    fieldnames = ['image_id', 'image_path', 'crop', 'symptom', 'disease_label',
                  'location_region', 'crop_stage', 'source_type', 'expert_validation', 'license_or_source_note']
    with open(METADATA_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)

    print(f"Successfully generated {len(metadata_rows)} demo images in {IMAGES_DIR}")
    print(f"Metadata saved to {METADATA_CSV}")

if __name__ == '__main__':
    main()
