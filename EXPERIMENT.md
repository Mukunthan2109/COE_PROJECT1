# AgriShield ML Experimentation & Model Training Report

## Objective

Develop an open, reproducible, local CPU-trainable machine learning feature classifier for early crop disease screening across 7 supported crops and 17 target disease/health classes.

---

## 1. Supported Crop & Class Scope

The machine learning model operates strictly on **7 crops** and **17 target classes**:

1. **Tomato**: Healthy Crop, Early Blight, Late Blight
2. **Potato**: Healthy Crop, Early Blight, Late Blight
3. **Rice**: Healthy Crop, Brown Spot, Leaf Blast
4. **Maize / Corn**: Healthy Crop, Common Rust, Leaf Blight
5. **Chili**: Healthy Crop, Anthracnose, Leaf Curl
6. **Grape**: Black Rot
7. **Apple**: Apple Scab

---

## 2. Dataset Pipeline & Reproducibility

- **Dataset Path**: `dataset/images/`
- **Metadata File**: `dataset/metadata.csv` (460 total samples across 17 classes)
- **Train / Test Split**: 80% Train (`368` samples), 20% Test (`92` samples)
- **Random Seed**: `42` (ensures reproducible splits across training runs)

---

## 3. Feature Extraction Pipeline (`ml/features.py`)

Each crop leaf image undergoes feature vector extraction:
1. **HSV Color Histograms**: 8 bins for Hue, 8 bins for Saturation, 8 bins for Value (24 dimensions).
2. **Color Statistics**: Mean and standard deviation across HSV channels (6 dimensions).
3. **Texture Features**: Gray-Level Co-occurrence Matrix (GLCM) contrast, dissimilarity, homogeneity, energy, and correlation (5 dimensions).
4. **Lesion & Dark Spot Count**: Adaptive thresholding and contour analysis detecting spot clusters (2 dimensions).

---

## 4. Model Training (`ml/train.py`)

- **Classifier**: `RandomForestClassifier(n_estimators=100, random_state=42)`
- **Artifacts Saved**: `ml/saved_model/model.pkl`, `ml/saved_model/label_encoder.pkl`, and `ml/saved_model/metrics.json`
- **Dynamic Evaluation Results**:
  - **Accuracy**: `32.61%`
  - **Weighted Precision**: `30.66%`
  - **Weighted Recall**: `32.61%`
  - **Weighted F1-Score**: `30.47%`

> [!NOTE]
> Evaluation results are dynamically calculated from the held-out test set and serve as an initial baseline for prototype evaluation. Screening predictions are preliminary indicators and do not replace professional agricultural diagnosis.
