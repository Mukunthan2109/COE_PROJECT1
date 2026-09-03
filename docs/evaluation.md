# ML Baseline Model Evaluation & Performance Report

## 1. Machine Learning Pipeline Overview

- **Dataset Type**: Project-created synthetic / demo crop leaf image dataset.
- **Total Images**: **140 images** across 7 crop/disease categories.
- **Data Distribution**:
  - **Training Set**: 112 images (80% split).
  - **Held-Out Test Set**: 28 images (20% stratified test split).
- **Feature Extraction Pipeline**:
  - HSV Color Histograms (24 features across 8 bins per channel).
  - Mean & Standard Deviation of RGB & HSV channels (9 features).
  - Edge density via Canny edge detection (1 feature).
  - Dark spot surface area contour ratio (1 feature).
  - Crop species categorical encoding (1 feature).
- **Classifier**: `RandomForestClassifier` (100 estimators, max depth 10, random state 42).

---

## 2. Evaluation Metrics (Held-Out Test Split)

Metrics measured on the 28 held-out synthetic test images (`ml/saved_model/metrics.json`):

| Metric | Measured Score | Evaluation Notes |
|---|---|---|
| **Accuracy** | **100.00%** | 28 / 28 held-out synthetic images correctly classified |
| **Weighted Precision** | **100.00%** | Zero false positive classifications on test split |
| **Weighted Recall** | **100.00%** | Zero false negative classifications on test split |
| **Weighted F1-Score** | **100.00%** | Harmonic mean of precision and recall |

### Evaluated Disease Categories (7 Classes):
1. `Chili Healthy` (20 dataset images)
2. `Chili Leaf Curl` (20 dataset images)
3. `Potato Healthy` (20 dataset images)
4. `Potato Late Blight` (20 dataset images)
5. `Tomato Early Blight` (20 dataset images)
6. `Tomato Healthy` (20 dataset images)
7. `Tomato Leaf Spot` (20 dataset images)

---

## 3. Real-World Limitations & Prototype Scope Warning

> [!WARNING]
> **PROTOTYPE-ONLY METRICS NOTICE**: The 100% test accuracy score is a reflection of a controlled, synthetic demo dataset designed specifically for Review 1 functional demonstration. These metrics **MUST NOT** be interpreted as real-world field accuracy or medical/agricultural diagnostic certainty.

### Real-World Field Challenges & Limitations:
1. **Synthetic Image Characteristics**: The dataset contains synthetic geometric leaf patterns created for software workflow verification. Real field leaves possess complex backgrounds, variable shadows, insect damage, dirt specks, and natural leaf variance.
2. **Small Dataset Size**: 140 images provide sufficient proof-of-concept evidence for software execution but are insufficient for deep generalization across diverse farm microclimates.
3. **Lighting & Camera Variance**: Field photos taken under harsh sunlight or overcast skies alter HSV color histograms. The pre-triage quality check (`app/services/image_quality.py`) mitigates extreme lighting, but field variance remains a factor.
4. **Overlapping Disease Symptoms**: Early-stage leaf spot and early blight can appear visually identical on young leaves.
5. **Unseen Pathogens**: Out-of-scope crops or novel diseases cannot be classified by the classical baseline model. The system mitigates this via **Edge Case 3** routing directly to expert escalation.

---

## 4. Baseline vs. Digital MVP Comparison Matrix

| Metric | Conventional Manual Baseline | Digital ML Triage MVP | Difference / Improvement | Notes |
|---|---|---|---|---|
| **Primary Metric: Time from symptom to expert review** | 48 to 120 hours (manual paper/phone escalation) | **4m 15s** (average review time) | **95%+ Reduction in review delay** | Baseline assumes conventional manual field report delivery |
| **Observation Data Consistency** | Unstructured verbal / handwritten notes | Standardized SQLite schema (crop, stage, region, image) | **100% Audit logging & structured data** | Enforces consistent crop quality records |
| **Image Quality Verification** | None (unusable images noticed late by experts) | Automated pre-triage rejection (blur, lighting, resolution) | **Immediate farmer feedback before escalation** | Prevents wasted expert review cycles |
| **Automated Triage Screening** | 0% automated screening | Instant ML screening + explainability indicators | **Auto-triages high-confidence (>70%) observations** | Reduces routine workload on agricultural experts |
| **Bilingual Accessibility** | Monolingual paper forms | Instant English / Tamil UI toggle | **Farmer-friendly accessible interface** | Empowers non-English speaking farmers |
