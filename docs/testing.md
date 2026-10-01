# AgriShield Testing & Automated Verification Document

## 1. Automated Test Suite Overview

AgriShield includes an automated test suite built with **Pytest** covering user authentication, image quality validation, ML predictor pipelines, escalation logic, HTTP views, outbreak alerts, quality assurance services, and security controls.

---

## 2. Test Execution Commands

### Local Execution Command
```bash
py -3 -m pytest tests/ -v
```

### Continuous Integration (CI) Execution
GitHub Actions workflow configured in `.github/workflows/tests.yml`:
- Trigger: `push` and `pull_request` on `main`/`master`
- Environment: `ubuntu-latest` (Python 3.11)
- CI Command: `python -m pytest tests/ -v`

---

## 3. Test Suite Execution Summary

- **Total Automated Tests**: `46`
- **Pass Rate**: **`100%` (`46 / 46 PASSED`)**
- **Execution Time**: `~12.5s`

---

## 4. Test Module Breakdown

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
