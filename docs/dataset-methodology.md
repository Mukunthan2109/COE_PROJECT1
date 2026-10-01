# AgriShield Dataset Methodology Document

## 1. Overview & Scope

The AgriShield dataset is designed for training and evaluating an initial machine learning screening model for early crop disease detection across **7 supported agricultural crops** (Tomato, Potato, Rice, Maize, Chili, Grape, Apple) and **17 target disease/health classes**.

---

## 2. Image Collection & Ethical Standards

- **Ethical Safeguards**: No facial images, farmer personal identifiers, phone numbers, location tracking, or private metadata are collected or stored in the dataset.
- **Image Licensing**: All 460 images are project-created or licensed under CC-BY-4.0 open educational use.
- **Image Preprocessing**: Images are validated for non-zero file size, standard RGB orientation, and stored in standard `.jpg` format.

---

## 3. Stratified Train / Validation / Test Split Strategy

To prevent data leakage and guarantee that test evaluation results accurately reflect held-out generalization, images were split using a fixed random seed (`random_state=42`) with class stratification:

- **Train Set (80%)**: `368` images (24 samples per core crop class, 16 per expanded crop class)
- **Validation Set (10%)**: `46` images (3 samples per core crop class, 2 per expanded crop class)
- **Test Set (10%)**: `46` images (3 samples per core crop class, 2 per expanded crop class)

---

## 4. Class Balance & Distribution Summary

```text
Class Name               Total Samples    Train Split    Val Split    Test Split
--------------------------------------------------------------------------------
Tomato Healthy                30              24             3            3
Tomato Early Blight           30              24             3            3
Tomato Late Blight            30              24             3            3
Potato Healthy                30              24             3            3
Potato Early Blight           30              24             3            3
Potato Late Blight            30              24             3            3
Rice Healthy                  30              24             3            3
Rice Brown Spot               30              24             3            3
Rice Leaf Blast               30              24             3            3
Corn Healthy                  30              24             3            3
Corn Common Rust              30              24             3            3
Corn Leaf Blight              30              24             3            3
Chili Healthy                 20              16             2            2
Chili Anthracnose             20              16             2            2
Chili Leaf Curl               20              16             2            2
Grape Black Rot               20              16             2            2
Apple Apple Scab              20              16             2            2
--------------------------------------------------------------------------------
TOTAL                        460             368            46           46
```

---

## 5. Distinction Between Model Labels & Expert Validation

- **`disease_label`**: The assigned target disease class label used for training supervised machine learning algorithms.
- **`expert_validation_status`**: Indicates whether an expert agricultural pathologist has explicitly validated the visual observation (`expert_validated`) or if the record is pending validation (`pending_validation`).

---

## 6. Dataset Limitations & Prototype Disclosure

1. **Sample Size**: 460 total images represent a prototype-level dataset suitable for academic demonstration and feature screening baseline evaluation.
2. **Environmental Variance**: Field images captured under extreme sunlight, torrential rain, or heavy leaf occlusions require expanded dataset collection prior to commercial deployment.
3. **Screening Purpose**: The dataset and model serve as initial screening triage tools to highlight suspicious cases for expert escalation, not for automated financial crop rejection.
