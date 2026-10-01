# AgriShield Dataset Documentation

## Dataset Summary

The **AgriShield Dataset** consists of **460 physical crop photos** across **17 target disease/health classes** for 7 supported agricultural crops.

| Crop | Disease / Health Class | Class Sample Count | Growth Stage |
| --- | --- | --- | --- |
| **Tomato** | Healthy Crop | 30 | Seedling |
| **Tomato** | Early Blight | 30 | Fruiting |
| **Tomato** | Late Blight | 30 | Fruiting |
| **Potato** | Healthy Crop | 30 | Vegetative |
| **Potato** | Early Blight | 30 | Vegetative |
| **Potato** | Late Blight | 30 | Flowering |
| **Rice** | Healthy Crop | 30 | Seedling |
| **Rice** | Brown Spot | 30 | Vegetative |
| **Rice** | Leaf Blast | 30 | Flowering |
| **Maize** | Healthy Crop | 30 | Vegetative |
| **Maize** | Common Rust | 30 | Flowering |
| **Maize** | Leaf Blight | 30 | Fruiting |
| **Chili** | Healthy Crop | 20 | Vegetative |
| **Chili** | Anthracnose | 20 | Fruiting |
| **Chili** | Leaf Curl | 20 | Vegetative |
| **Grape** | Black Rot | 20 | Fruiting |
| **Apple** | Apple Scab | 20 | Vegetative |

- **Total MVP Images**: `460`
- **Supported Crops**: `7`
- **Target Classes**: `17`
- **Train / Val / Test Split**: 80% Train (`368`), 10% Validation (`46`), 10% Test (`46`)
- **Random Seed**: `42` (ensures reproducible splits)

---

## Directory Structure

```text
dataset/
├── images/             # Active 460 physical crop photos matching metadata.csv
├── archive_legacy/     # Archived 80 legacy images from unreleased classes
├── metadata.csv        # Standardized CSV metadata file
└── README.md           # Dataset documentation
```

---

## Metadata Schema (`metadata.csv`)

| Column Name | Description | Example |
| --- | --- | --- |
| `image_id` | Unique image identifier | `IMG_0001` |
| `image_path` | Relative file path | `dataset/images/tomato_healthy_01.jpg` |
| `crop` | Cultivated crop name | `Tomato` |
| `symptom` | Observed visual symptom | `Healthy` |
| `disease_label` | Target model disease class | `Tomato Healthy` |
| `crop_stage` | Growth stage | `Seedling` |
| `location_region` | General region | `North Zone` |
| `source_type` | Data origin category | `project_created` |
| `source_reference` | Source note / attribution | `Project-created demo dataset` |
| `license` | License type | `CC-BY-4.0-Project-Demo` |
| `expert_validation_status` | Status | `expert_validated` or `pending_validation` |
| `split` | Dataset split assignment | `train`, `val`, `test` |

---

## Data Privacy & Ethics Policy

- **Zero Personal Data**: Contains no human faces, farmer identities, phone numbers, Aadhaar numbers, private addresses, or continuous GPS coordinates.
- **Separation of Training & Runtime Uploads**: Runtime farmer submissions (`app/static/uploads/`) are saved in runtime storage and are **never automatically appended** to the ML training set without explicit expert review and re-curation.
