# AgriShield Review 1 Final Comprehensive Report

## 1. Executive Summary

The **AgriShield** system is a web-based MVP designed for food-processing units purchasing crops with variable quality. The system provides a farmer-friendly observation intake workflow, automated image quality screening, ML feature-based triage, normalized confidence scoring, expert escalation engine, expert validation portal, and real-time SLA review duration measurement.

---

## 2. Final Standardized Scope

- **Supported Crops**: `Tomato`, `Potato`, `Rice`, `Maize` (4 crops).
- **Disease & Health Classes**: 12 target classes (3 classes per crop).
- **Runtime Database**: Starts 100% empty (0 observations, 0 expert reviews, 0 outbreak alerts).
- **Test Suite**: 34 / 34 automated unit tests passing (`py -3 -m pytest tests/ -v`).

---

## 3. Machine Learning Baseline & Evaluation

- **Dataset**: 360 project-created synthetic crop leaf images (30 images per class across 12 classes).
- **Train / Test Split**: 80% Train (`288` samples), 20% Test (`72` samples).
- **Classifier**: Random Forest Classifier trained on visual HSV histograms, RGB/HSV statistics, edge density, and dark spot surface ratios.
- **Evaluation Metrics (12-Class)**:
  - **Accuracy**: `29.17%`
  - **Weighted Precision**: `28.81%`
  - **Weighted Recall**: `29.17%`
  - **Weighted F1-Score**: `28.90%`

*Disclaimer*: These baseline metrics reflect synthetic prototype data and serve as an initial triage tool, not a final medical/agricultural diagnosis. Expert validation is required for uncertain cases.

---

## 4. Key Hardened Architectural Features

1. **Crop-Aware Probability Normalization**: Candidate class probabilities for the selected crop are isolated and normalized (`candidate_probs / candidate_probs.sum()`) to provide crop-specific confidence.
2. **Model-Missing Fallback**: If model artifacts are missing, the system returns `confidence = 0.0`, `prediction = "Model unavailable"`, `risk_level = "High"`, and escalates to expert review.
3. **Empty-State Database**: History, Expert Portal, and Analytics display clean empty-state messages when zero runtime submissions exist. Outbreak alerts trigger ONLY when real observations satisfy the cluster threshold (>= 3 cases in 48h).
4. **Bilingual UI Support**: Centralized translation dictionary supporting seamless switching between **English** and **தமிழ் (Tamil)** across all pages and alerts.
