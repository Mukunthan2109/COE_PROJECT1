# AgriShield ML Experimentation & Model Baseline Log

## 1. Experiment Overview

- **Objective**: Establish an interpretable visual feature classifier for initial 12-class crop disease triage across 4 supported crops (Tomato, Potato, Rice, Maize).
- **Dataset**: 360 project-created synthetic leaf images (30 images/class).
- **Feature Matrix**: 35 visual features:
  - 8-bin Hue histogram (HSV)
  - 8-bin Saturation histogram (HSV)
  - 8-bin Value histogram (HSV)
  - RGB Mean & Std (6 features)
  - HSV Mean (3 features)
  - Canny edge density (1 feature)
  - Dark spot surface area ratio (1 feature)

---

## 2. Model Evaluation (12-Class Baseline)

- **Split**: 80% Train (`288` samples), 20% Test (`72` samples), Stratified.
- **Model**: `RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)`

| Metric | Result (12-Class Baseline) |
| --- | --- |
| **Accuracy** | `29.17%` |
| **Weighted Precision** | `28.81%` |
| **Weighted Recall** | `29.17%` |
| **Weighted F1-Score** | `28.90%` |

---

## 3. Probability Normalization & Fallback Safeguards

1. **Crop-Aware Masking**: Candidate probabilities are filtered by selected crop and normalized (`candidate_probs / candidate_probs.sum()`).
2. **Missing Model Handling**: Returns `confidence = 0.0` and `prediction = "Model unavailable"`, routing immediately to expert triage.
