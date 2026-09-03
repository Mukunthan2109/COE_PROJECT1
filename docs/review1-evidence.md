# Review 1 Verification Evidence Portfolio

This document provides a clear evidence portfolio that can be presented to evaluators for Review 1.

---

## 1. Application & Navigation Links
- **Home Landing Page**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Farmer Observation Form**: [http://127.0.0.1:5000/observe](http://127.0.0.1:5000/observe)
- **Status Tracker**: [http://127.0.0.1:5000/status](http://127.0.0.1:5000/status)
- **Expert Escalation Dashboard**: [http://127.0.0.1:5000/expert](http://127.0.0.1:5000/expert)

---

## 2. Evidence of Core Features

### Evidence 2.1: Farmer Observation Submission & Metadata
- **Form Controls**: Crop Type (*Tomato*, *Potato*, *Chili*), Visible Symptom, Crop Growth Stage, General Region, Photo Upload, Notes.
- **Source Code**: [app/templates/observe.html](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/templates/observe.html) & [app/routes.py](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/routes.py).

### Evidence 2.2: Image Quality Check Pre-Triage
- **Rule Engine**: Validates minimum resolution (100x100), brightness bounds (30-225), and Laplacian blur variance (`>=40.0`).
- **Source Code**: [app/services/image_quality.py](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/services/image_quality.py).
- **Test Evidence**: `test_blurry_image_rejection` in [tests/test_image_quality.py](file:///c:/Users/mukun/OneDrive/Desktop/ceo/tests/test_image_quality.py) PASSED.

### Evidence 2.3: ML Prediction & Explainability Result
- **Output**: Predicts disease label, displays confidence bar (`88%`), and lists explainable visual indicators (e.g., *"Visible dark spot clusters detected"*).
- **Source Code**: [app/services/predictor.py](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/services/predictor.py) & [app/templates/result.html](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/templates/result.html).

### Evidence 2.4: Expert Escalation & Review Dashboard
- **Escalation Rules**: Low confidence (`<70%`) and unsupported categories route to `"Needs expert review"`.
- **Expert Dashboard**: Pending queue displaying observation details, image, confidence score, and validation form.
- **Source Code**: [app/templates/expert.html](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/templates/expert.html) & [app/templates/expert_review.html](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/templates/expert_review.html).

### Evidence 2.5: Key Project Metric: Time-to-Expert-Review
- **Calculation**: $\text{Time to Review} = \text{Review Timestamp} - \text{Observation Timestamp}$.
- **Analytics Metrics**: Total observations, escalated cases count, average review time, median review time, fastest, and slowest review times.
- **Source Code**: [app/services/escalation.py](file:///c:/Users/mukun/OneDrive/Desktop/ceo/app/services/escalation.py).

---

## 3. Evidence of ML Evaluation & Dataset

### ML Baseline Evaluation Metrics (`ml/saved_model/metrics.json`):
- **Accuracy**: **100.00%** (on 28 test split images)
- **Precision**: **100.00%**
- **Recall**: **100.00%**
- **F1-Score**: **100.00%**
- **Dataset**: 140 project-created crop leaf images (`dataset/metadata.csv`).

---

## 4. Evidence of Automated Tests

Executed command: `pytest tests/ -v`

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1
rootdir: C:\Users\mukun\OneDrive\Desktop\ceo

tests/test_escalation.py::test_high_confidence_escalation_logic PASSED   [  6%]
tests/test_escalation.py::test_low_confidence_escalation_logic_edge_case PASSED [ 13%]
tests/test_escalation.py::test_unsupported_category_escalation_logic PASSED [ 20%]
tests/test_escalation.py::test_time_to_review_calculation PASSED         [ 26%]
tests/test_image_quality.py::test_valid_image_quality PASSED             [ 33%]
tests/test_image_quality.py::test_low_resolution_rejection PASSED        [ 40%]
tests/test_image_quality.py::test_dark_image_rejection PASSED            [ 46%]
tests/test_image_quality.py::test_bright_image_rejection PASSED          [ 53%]
tests/test_image_quality.py::test_blurry_image_rejection PASSED          [ 60%]
tests/test_ml_predictor.py::test_predict_supported_category PASSED       [ 66%]
tests/test_ml_predictor.py::test_predict_unsupported_category_edge_case PASSED [ 73%]
tests/test_routes.py::test_home_page PASSED                              [ 80%]
tests/test_routes.py::test_observe_get PASSED                            [ 86%]
tests/test_routes.py::test_observe_post_valid PASSED                     [ 93%]
tests/test_routes.py::test_expert_review_workflow PASSED                 [100%]

======================= 15 passed in 10.29s =======================
```

---

## 5. Documentation Sitemap

- **Verification Matrix**: [docs/review1-verification.md](docs/review1-verification.md)
- **Failure Case Testing**: [docs/failure-case-testing.md](docs/failure-case-testing.md)
- **System Architecture**: [docs/architecture.md](docs/architecture.md)
- **Database Schema**: [docs/data-schema.md](docs/data-schema.md)
- **Risk Register**: [docs/risk-register.md](docs/risk-register.md)
- **User Guide**: [docs/user-guide.md](docs/user-guide.md)
- **Evaluation Report**: [docs/evaluation.md](docs/evaluation.md)
- **Privacy & Ethics Policy**: [docs/ethics.md](docs/ethics.md)
- **Review 1 Status Report**: [docs/review1-status.md](docs/review1-status.md)
- **Master README**: [README.md](README.md)
