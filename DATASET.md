# AgriShield Dataset Documentation

## Dataset Summary

The **AgriShield MVP** dataset consists of **460 images** across **17 disease/health classes** for 7 supported crops:

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
- **Classes**: `17` (30 samples per 4 core crops, 20 samples per 3 expanded crops)
- **Train / Test Split**: 80% Train (`368` samples), 20% Test (`92` samples)

---

## Data Structure & Archiving

- `dataset/images/` — Contains strictly the 460 active MVP images matching `dataset/metadata.csv`.
- `dataset/metadata.csv` — Standardized CSV metadata mapping image IDs, paths, crops, symptoms, regions, and stages.
- `dataset/archive_legacy/` — Contains 80 archived legacy image files from unreleased/unsupported classes (*Corn Northern Leaf Blight*, *Rice Bacterial Blight*, *Tomato Leaf Spot*, *Wheat Healthy*). Excluded from model training and evaluation.

---

## Separation of Training Data & Runtime Uploads

- **Training Dataset** (`dataset/images/`): Used exclusively for feature classifier training and evaluation.
- **Runtime Uploads** (`app/static/uploads/`): Real images captured and submitted by farmers during runtime. Runtime uploads are **never automatically added** to the training set.
