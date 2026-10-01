# AgriShield Systematic Error Analysis Report

## 1. Overview & Evaluation Methodology

This report details empirical misclassification patterns observed during model evaluation across 17 target crop-disease classes. Errors are categorized based on image quality degradation, symptom overlap, visual feature ambiguity, and class balance variations.

---

## 2. Empirical Model Error Log Table

| Case ID | Actual Label | Predicted Label | Confidence | Error Category | Root Cause Analysis | System Mitigation Strategy |
|---|---|---|---|---|---|---|
| ERR-01 | Tomato Early Blight | Tomato Late Blight | 54.2% | Disease Class Confusion | Concentric ring lesion features closely resemble late blight dark spot distribution in HSV space. | Low confidence (< 70%) automatically escalates observation to expert review queue. |
| ERR-02 | Potato Healthy | Potato Early Blight | 48.6% | Background Clutter / Shadow | Soil darkness and shadows detected as dark lesion spot contours. | Image Quality Check rejects extreme darkness; low confidence triggers expert triage. |
| ERR-03 | Chili Anthracnose | Chili Leaf Curl | 51.0% | Symptom Overlap | Advanced anthracnose fruit rot causes secondary leaf wilting similar to leaf curl. | Expert review workflow allows agronomists to correct screening diagnosis with persistent DB logging. |
| ERR-04 | Corn Leaf Blight | Corn Common Rust | 58.7% | Feature Similarity | Long necrotic blight streaks share GLCM texture dissimilarity metrics with rust pustule clusters. | Multi-symptom checkboxes provide explicit metadata context alongside visual feature vectors. |
| ERR-05 | Rice Brown Spot | Rice Leaf Blast | 62.1% | Lesion Shape Variance | Early brown spot lesions exhibit oval geometry matching leaf blast spindle spots. | Confidence thresholding (`REVIEW_THRESHOLD = 0.70`) flags ambiguous cases as *"Needs expert review"*. |
| ERR-06 | Apple Apple Scab | Grape Black Rot | 42.3% | Crop Feature Misalignment | Single-class expanded crops with dark fruit/leaf spots share color histogram peaks. | Crop selection metadata restricts candidate disease predictions strictly to selected crop category. |

---

## 3. Systematic Error Categories & Mitigations

1. **Blurry / Out-of-Focus Photos**:
   - *Cause*: Handheld camera shaking or improper lens focus.
   - *Mitigation*: Pre-triage Laplacian variance blur detection (`blur_score < 100`) immediately prompts the farmer for a clearer photo before running ML inference.
2. **Extreme Lighting Variations (Underexposed / Overexposed)**:
   - *Cause*: Direct harsh sunlight or low evening illumination.
   - *Mitigation*: Brightness thresholding (`mean_brightness < 30` or `> 225`) rejects invalid lighting conditions.
3. **Symptom Confusion & Overlapping Lesions**:
   - *Cause*: Multiple co-occurring diseases or non-pathogenic nutrient deficiencies.
   - *Mitigation*: Mandatory human-in-the-loop expert review for low-confidence (< 70%) screening outputs.
