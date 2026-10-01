# AgriShield Testing & Quality Assurance Guide

## Automated Test Suite Overview

AgriShield includes an automated test suite built with **Pytest** covering unit models, services, routes, escalation rules, image quality validation, ML prediction pipelines, and bilingual translations.

---

## 1. Running the Automated Tests

Execute the test suite using Python:

```bash
py -3 -m pytest tests/ -v
```

### Test Suite Execution Summary
- **Local Test Execution**: `py -3 -m pytest tests/ -v`
- **CI Test Execution**: GitHub Actions (`.github/workflows/tests.yml`)
- **Total Tests**: `46`
- **Pass Rate**: `100%` (`46 / 46 PASSED`)
- **Execution Time**: `~12.5s`

---

## 2. Test File Breakdown

| Test File | Focus Area | Key Assertions Covered |
| --- | --- | --- |
| `tests/test_auth.py` | Authentication & Roles | User registration, password hashing verification, login session, logout |
| `tests/test_image_quality.py` | Image Quality & Hash | Valid image verification, corrupted file rejection, size limits, MD5 hashing |
| `tests/test_ml_predictor.py` | Machine Learning | Feature extraction vector length, 17-class prediction output across 7 crops, candidate masking |
| `tests/test_escalation.py` | Escalation Logic & SLA | Threshold trigger (`<0.70`), status assignment, review time calculation |
| `tests/test_routes.py` | HTTP Routes & Views | GET/POST routes, farmer intake, instant scanner, expert workflow, history, evaluation |
| `tests/test_outbreak_alerts.py` | Outbreak Alert Logic | Regional threshold triggers (>= 3 cases in 48h), empty DB alert suppression |
| `tests/test_batch_qa.py` | Quality Assurance Services | Batch QA procurement status, quality compliance scoring |
| `tests/test_final_system_qa.py` | System QA & Security | Password hashing, file extension rejection, bilingual keys, unauthorized redirects |

---

## 3. Manual Testing Checklist

- [x] **Empty Database Startup**: GET `/history` returns `"No observations submitted yet."`
- [x] **Farmer Intake Submission**: Upload real crop photo -> UUID saving in `uploads/` -> ML prediction output.
- [x] **Duplicate Hash Detection**: Re-uploading same photo triggers warning redirect to existing Observation ID.
- [x] **Low-Confidence Escalation**: Confidence `< 70%` updates status to `Needs expert review`.
- [x] **Expert Lightbox & Validation**: Expert views uploaded photo in full resolution and submits diagnosis.
- [x] **Language Switching**: Toggle between English and Tamil across all 16 views with 100% translation coverage.
