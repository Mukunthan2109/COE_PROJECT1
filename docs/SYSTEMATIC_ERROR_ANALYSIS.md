# Systematic Error Analysis & Model Reliability Report

This report documents empirical failure mode taxonomy, edge case handling, image quality validation thresholds, and confidence calibration in **AgriShield**.

---

## 1. Primary Image Quality Failure Modes

AgriShield integrates an automated pre-screening module (`app/services/image_quality.py`) using **OpenCV Laplacian Variance** to evaluate uploaded crop images prior to ML model inference.

### Failure Category Taxonomy

| Category | Root Cause | Detection Metric | Resolution Strategy |
|---|---|---|---|
| **Severe Motion/Focus Blur** | Camera shake or incorrect focus | Laplacian Variance < 100.0 | Reject upload & prompt farmer to retake photo |
| **Low Contrast / Under-exposure** | Poor lighting or nighttime capture | Mean Luminance < 40 | Escalated for review with low lighting flag |
| **Over-exposure / Glare** | Direct sunlight on reflective leaf surfaces | Standard Deviation < 15 | Reject image & prompt for shaded photo |
| **Out-of-Frame / Off-Crop** | Background clutter or non-leaf surface | Class Probability Entropy > 1.8 | Mark model prediction as Low Confidence |
| **Multiple Symptom Overlap** | Co-infection of multiple pathotypes | Top-2 Class Margin < 0.15 | Trigger automatic Expert Escalation |

---

## 2. ML Model Confusion Analysis

Model performance was evaluated on a held-out test split of 460 physical crop photos across 17 target classes.

### Primary Confusion Pairs Identified
1. **Tomato Early Blight vs. Late Blight**: Early stage lesions exhibit similar concentric rings on leaves under sub-optimal camera resolution.
2. **Potato Early Blight vs. Healthy Potato**: Isolated early spots on otherwise green foliage may produce borderline confidence scores (~0.62).
3. **Maize Common Rust vs. Northern Leaf Blight**: Distinguishing pustule geometry requires close-up macro lens photos.

---

## 3. Fallback & Safe Degradation Workflow

```
[Uploaded Image]
       │
       ▼
Image Quality Check ─── (Fails: Blur < 100.0) ───► [Reject Image with Friendly UI Guidance]
       │
       │ (Passes Quality Threshold)
       ▼
ML Model Inference
       │
       ├── (Confidence >= 0.70) ──► [Direct Result Displayed + Advisory]
       │
       └── (Confidence < 0.70)  ──► [Flagged for Escalation] ──► [Expert Dashboard Review]
```

---

## 4. Empirical Evaluation Metrics Summary

- **Total Physical Field Photos**: 460 verified images (0 duplicate MD5 hashes).
- **Random Forest Baseline Accuracy**: 84.78%
- **ExtraTrees Ensemble Accuracy**: 89.13%
- **Confidence Escalation Threshold**: 70.0%
- **System Automated Unit Test Coverage**: 47 passing tests out of 47 executed.
