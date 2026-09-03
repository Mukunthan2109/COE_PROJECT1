# Failure and Edge Case Testing Document

This document records empirical test runs for the three required failure and edge case scenarios in the **Farmer-Friendly Disease Observation and Escalation App**.

---

## Failure Case 1: Blurry / Poor Quality Image Upload

- **Scenario**: A farmer submits an out-of-focus or low-quality crop leaf image.
- **Input**:
  - Image: Uniform low-variance image file (`tests/test_image_quality.py` sample blur fixture).
  - Crop: Tomato
  - Symptom: Leaf Spot
  - Region: North Zone
- **Expected Behaviour**:
  - Image quality check service (`app/services/image_quality.py`) flags Laplacian variance below threshold (`< 40.0`).
  - Pre-triage rejects the image before ML inference.
  - User receives clear, non-technical feedback: *"Image quality is insufficient. Please capture a clearer crop image."*
  - User is offered an opportunity to re-upload without losing form metadata.
- **Actual Behaviour**:
  - `evaluate_image_quality()` computed Laplacian variance = 0.00.
  - Returned `is_valid = False`, `reason = 'blurry'`.
  - Flash warning displayed: *"Image quality is insufficient. Crop image is blurry or out of focus. Please capture a clearer crop image."*
- **Result**: **PASS** (Verified via `test_blurry_image_rejection` in `tests/test_image_quality.py`).

---

## Failure Case 2: Low-Confidence Prediction Escalation

- **Scenario**: An ambiguous image yields an ML model confidence score below the threshold (`< 0.70`).
- **Input**:
  - Crop: Tomato
  - Symptom: Leaf Spot
  - Image: Ambiguous dark spot pattern yielding prediction confidence = 0.62.
- **Expected Behaviour**:
  - Predictor identifies confidence `0.62 < CONFIDENCE_THRESHOLD (0.70)`.
  - System avoids presenting prediction as certainty.
  - Status automatically assigned to `"Needs expert review"`.
  - Observation routes directly to the Expert Dashboard queue.
  - User interface displays: *"The system is not sufficiently confident. This observation has been sent for expert review."*
- **Actual Behaviour**:
  - `determine_escalation(0.62, threshold=0.70)` returned `'Needs expert review'`.
  - Status recorded in SQLite DB as `'Needs expert review'`.
  - Displayed warning box on result page and added item to expert queue.
- **Result**: **PASS** (Verified via `test_low_confidence_escalation_logic_edge_case` in `tests/test_escalation.py`).

---

## Failure Case 3: Unsupported / Unknown Crop or Disease Category

- **Scenario**: A farmer submits a crop or symptom outside the supported training dataset scope (e.g. DragonFruit or Unknown Anomaly).
- **Input**:
  - Crop: "Other / Unknown" or "DragonFruit"
  - Symptom: "Unknown Anomaly"
- **Expected Behaviour**:
  - System detects category is outside supported set (`{"Tomato", "Potato", "Chili"}`).
  - Refuses to force a wrong disease label.
  - Sets prediction label to `"Unsupported / Unknown Category"`.
  - Sets confidence to low baseline (`0.35`).
  - Status automatically assigned to `"Needs expert review"`.
  - UI displays: *"Observation involves a crop or symptom category outside the baseline training dataset. System is unable to safely triage this unclassified crop observation."*
- **Actual Behaviour**:
  - `predict_crop_disease()` flagged `is_supported = False`.
  - Status set to `'Needs expert review'`.
  - Observation successfully routed to expert review queue.
- **Result**: **PASS** (Verified via `test_predict_unsupported_category_edge_case` in `tests/test_ml_predictor.py`).

---

## Summary of Failure Case Execution

| Test Case | Target Scenario | Automated Test Function | Execution Result |
|---|---|---|---|
| **Case 1** | Blurry / Dark / Low-res Image | `test_blurry_image_rejection`, `test_dark_image_rejection` | **PASSED** |
| **Case 2** | Low Confidence Escalation | `test_low_confidence_escalation_logic_edge_case` | **PASSED** |
| **Case 3** | Unsupported Category | `test_predict_unsupported_category_edge_case` | **PASSED** |
