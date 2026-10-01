# AgriShield — Farmer-Friendly Crop Disease Observation, AI Screening and Expert Escalation System

> **A Web-based End-to-End System for Food-Processing Procurement & Agricultural Quality Assurance**  
> *Complete College Project Implementation*

---

### Project Status & Verification Summary

> [!IMPORTANT]
> **Implementation Status**: **100% Complete Working Project**  
> **Automated Test Suite**: **47 / 47 Tests Passing** (`py -3 -m pytest tests/`)  
> **Continuous Integration**: [![Tests](https://github.com/Mukunthan2109/COE_PROJECT1/actions/workflows/tests.yml/badge.svg)](https://github.com/Mukunthan2109/COE_PROJECT1/actions/workflows/tests.yml)  
> **Current Server Status**: Runnable locally on `http://127.0.0.1:5000`

- **Complete End-to-End Workflow**: Farmer observation intake, mobile camera capture, image quality inspection, ML feature-based screening, risk triage, automated expert escalation engine, persistent expert validation portal, real-time SLA review duration metrics, dynamic analytics, system evaluation, and usability feedback.
- **Supported Scope**: **7 Supported Crops** (Tomato 🍅, Potato 🥔, Rice 🌾, Maize / Corn 🌽, Chili 🌶️, Grape 🍇, Apple 🍎) and **17 Disease / Health Classes**.
- **100% Real DB Analytics & Zero Fake Records**: Runtime database (`app/farmer_app.db`) starts at a clean state. All history, analytics, expert portal views, and regional outbreak alerts populate strictly from genuine user submissions and optional demo seeder data.
- **Complete Application-Wide Tamil Internationalization**: Every user-visible page title, heading, subtitle, button, form label, dropdown choice, placeholder, risk badge, status label, disclaimer, error notice, and footer supports seamless toggling between **English** and **தமிழ் (Tamil)**.

---

## 1. Problem Statement & Workflow Objective

Food-processing procurement units frequently purchase raw agricultural material of variable quality. Late reporting of crop diseases leads to significant harvest loss and compromised raw material quality.

AgriShield implements a non-surveillance escalation workflow:

$$\text{Farmer Observation} \rightarrow \text{Photo \& Metadata} \rightarrow \text{Image Quality Check} \rightarrow \text{ML Screening} \rightarrow \text{Confidence \& Risk} \rightarrow \text{Expert Escalation} \rightarrow \text{Expert Validation} \rightarrow \text{SLA Tracking}$$

The AI system functions as an **INITIAL SCREENING SYSTEM** to triage high-risk cases and assist agricultural experts, not to replace certified expert diagnosis.

---

## 2. Supported Scope & Disease Classes

AgriShield operates strictly on **7 supported crops** and **17 target classes**:

| Crop | Disease / Health Classes |
| --- | --- |
| **Tomato** | Healthy Crop, Early Blight, Late Blight |
| **Potato** | Healthy Crop, Early Blight, Late Blight |
| **Rice** | Healthy Crop, Brown Spot, Leaf Blast |
| **Maize / Corn** | Healthy Crop, Common Rust, Leaf Blight |
| **Chili** | Healthy Crop, Anthracnose, Leaf Curl |
| **Grape** | Black Rot |
| **Apple** | Apple Scab |

---

## 3. Technology Stack

- **Backend**: Python 3.11+, Flask 3.1
- **Database**: SQLite with SQLAlchemy ORM
- **Machine Learning**: Scikit-learn, OpenCV (`opencv-python-headless`), Pillow, NumPy, Joblib
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Testing**: Pytest 9.1
- **CI / Containerization**: GitHub Actions, Docker, Gunicorn

---

## 4. Documentation Suite Sitemap

- 🏗️ **System Architecture**: [docs/architecture.md](docs/architecture.md)
- 📋 **Review-1 Gap Closure Matrix**: [docs/review-gap-closure.md](docs/review-gap-closure.md)
- 📊 **Dataset Methodology & Provenance**: [docs/dataset-methodology.md](docs/dataset-methodology.md), [docs/data-provenance.md](docs/data-provenance.md) & [dataset/README.md](dataset/README.md)
- 🧪 **ML Experimentation & Evaluation**: [docs/evaluation.md](docs/evaluation.md) & [EXPERIMENT.md](EXPERIMENT.md)
- 🔒 **Security & Authentication**: [docs/security.md](docs/security.md)
- ⚖️ **Ethics & Non-Surveillance Policy**: [docs/ethics-final.md](docs/ethics-final.md) & [docs/expert-validation.md](docs/expert-validation.md)
- 🔬 **Systematic Error Analysis**: [docs/error-analysis.md](docs/error-analysis.md)
- ⚠️ **Edge & Failure Case Testing**: [docs/failure-case-testing.md](docs/failure-case-testing.md)
- 📘 **User Guide & Workflow**: [docs/user-guide.md](docs/user-guide.md)
- 👥 **User Validation Protocol**: [docs/user-validation.md](docs/user-validation.md)
- ♿ **Accessibility Validation**: [docs/accessibility-validation.md](docs/accessibility-validation.md)
- 📊 **Before vs After Experiment**: [docs/before-after-experiment.md](docs/before-after-experiment.md)
- 🚀 **Deployment Guide**: [docs/deployment.md](docs/deployment.md)
- ✅ **Final Completion Matrix**: [docs/final-completion-matrix.md](docs/final-completion-matrix.md)

---

## 5. Reproducibility

AgriShield is fully reproducible from a clean repository clone:
- **Pre-Trained ML Artifacts**: `ml/saved_model/model.pkl`, `label_encoder.pkl`, `metrics.json`, and `model_metadata.json` are committed directly to the repository.
- **Dataset Seed**: `42` (ensures reproducible 80% train / 10% val / 10% test split).
- **Training Command**: `py -3 ml/train.py`
- **Evaluation Command**: `py -3 ml/evaluate.py`
- **Audit Command**: `py -3 scripts/check_dataset.py`
- **Test Command**: `py -3 -m pytest tests/ -v`
- **CI Workflow**: `.github/workflows/tests.yml`

---

## 6. Validation Status

To preserve scientific integrity and eliminate self-labeling bias:
- **Automated Unit Tests**: 47 / 47 tests passing locally and in CI.
- **Demonstration Expert Workflow**: Interactive expert portal (`/expert`) supported via `scripts/seed_demo.py` (`DEMO_SEED` records).
- **Independent Expert Validation**: **`PENDING INDEPENDENT VALIDATION`**. Independent validation by accredited agricultural pathologists is pending field trial deployment (documented in [docs/expert-validation.md](docs/expert-validation.md)).

---

## 7. Dataset Limitations

- The dataset contains 460 images across 17 classes (30/class core, 20/class expanded).
- Images serve as initial screening prototype data. Field deployment across varied weather and light conditions requires ongoing dataset expansion.

---

## 8. Deployment & Execution Guide

### Local Execution Setup
```bash
# 1. Create & Activate Virtual Environment
py -3 -m venv .venv
.venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Setup Environment & Database
py -3 scripts/setup_env.py

# 4. Seed Controlled Demo Data (Optional)
py -3 scripts/seed_demo.py

# 5. Run Application Server
py -3 run.py
```
Open browser at: **`http://127.0.0.1:5000`**

### Health Endpoint Check
```bash
# Returns {"status": "ok"}
curl http://127.0.0.1:5000/health
```

### Production Docker Container Execution
```bash
# Build Docker Image
docker build -t agrishield-app .

# Run Docker Container
docker run -p 5000:5000 agrishield-app
```
*(Note: Container configuration created; local Docker daemon execution unverified if Docker is unavailable in local terminal environment).*

---

## 9. License & Disclaimer

*AgriShield is an academic college project. Machine learning screening predictions serve as an initial triage assessment and do not replace professional agricultural expert diagnosis.*
