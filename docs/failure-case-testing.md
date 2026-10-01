# AgriShield Systematic Edge & Failure Case Validation Report

## 1. Overview & Verification Summary

This document records automated and empirical verification for 14 critical edge and failure case scenarios in the **AgriShield Crop Disease Screening & Escalation System**.

---

## 2. Complete 14 Edge Case Verification Matrix

| # | Edge Case Scenario | Test Input / Condition | System Handling & Safety Logic | Verification Status | Automated Test Function |
|---|---|---|---|---|---|
| 1 | **Blurry Image** | Out-of-focus leaf photo (Laplacian variance < 100) | Rejected in pre-triage; returns user retry prompt before ML model inference. | `PASSED` | `test_blurry_image_rejection` |
| 2 | **Very Dark Image** | Underexposed photo (Mean brightness < 30) | Rejected in pre-triage; prompts farmer for better lighting. | `PASSED` | `test_dark_image_rejection` |
| 3 | **Very Bright Image** | Overexposed photo (Mean brightness > 225) | Rejected in pre-triage; prompts farmer for shadow/shade capture. | `PASSED` | `test_image_quality.py` |
| 4 | **Low Resolution** | Image dimensions < 100x100 pixels | Rejected; requires min 100x100 resolution. | `PASSED` | `test_image_quality.py` |
| 5 | **Unsupported Crop** | Crop category outside 7 supported crops (*e.g., Dragonfruit*) | Refuses synthetic label; forces prediction to `"Unsupported Category"` and escalates to expert. | `PASSED` | `test_predict_unsupported_category_edge_case` |
| 6 | **Unknown Disease** | Symptom pattern not matching trained classes | Flags confidence < 0.70; automatically escalates to expert review queue. | `PASSED` | `test_ml_predictor.py` |
| 7 | **Low-Confidence Prediction** | Prediction confidence < 0.70 threshold | Status set to `"Needs expert review"`; warning box explains initial screening limitation. | `PASSED` | `test_low_confidence_escalation_logic_edge_case` |
| 8 | **Missing Crop Selection** | Empty crop form field submitted | HTML5 form validation and backend POST handler reject submission with HTTP 400. | `PASSED` | `test_routes.py` |
| 9 | **Missing Image Upload** | POST request without file payload | Form handler returns error flash notice: *"Please upload a valid crop image."* | `PASSED` | `test_routes.py` |
| 10 | **Invalid File Type** | File extension `.exe`, `.script`, `.html` | File validator rejects extension; prevents file saving or execution. | `PASSED` | `test_routes.py` |
| 11 | **Oversized Image File** | File size exceeding 16MB limit | Flask `MAX_CONTENT_LENGTH` returns HTTP 413 Payload Too Large. | `PASSED` | `test_routes.py` |
| 12 | **Multiple Similar Symptoms** | Checkbox selection of multiple co-occurring symptoms | Combines symptom list into metadata string without throwing parsing exception. | `PASSED` | `test_routes.py` |
| 13 | **Expert Correction** | Expert changes initial screening label to corrected diagnosis | Persistent DB update; sets status to `"Reviewed by expert"` and records review timestamp. | `PASSED` | `test_expert_review_workflow` |
| 14 | **Expert Marks Uncertain** | Expert selects decision `"Uncertain"` with advisory note | Persistent DB update; records expert comment for secondary agronomist consultation. | `PASSED` | `test_expert_review_workflow` |
