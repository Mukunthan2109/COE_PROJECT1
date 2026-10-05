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
- 🔌 **API Documentation**: [docs/API.md](docs/API.md)
- 🗄️ **Database Schema**: [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md)
- 🔒 **Security & Authentication**: [docs/SECURITY.md](docs/SECURITY.md)
- 🔬 **Systematic Error Analysis**: [docs/SYSTEMATIC_ERROR_ANALYSIS.md](docs/SYSTEMATIC_ERROR_ANALYSIS.md)
- 📋 **Review Gap Closure & Evidence Matrix**: [docs/FINAL_REVIEW_EVIDENCE.md](docs/FINAL_REVIEW_EVIDENCE.md) & [docs/review-gap-closure.md](docs/review-gap-closure.md)
- ✅ **Final Completion Matrix**: [docs/FINAL_COMPLETION_MATRIX.md](docs/FINAL_COMPLETION_MATRIX.md)
- 📊 **Dataset Methodology & Provenance**: [docs/dataset-methodology.md](docs/dataset-methodology.md), [docs/data-provenance.md](docs/data-provenance.md) & [dataset/README.md](dataset/README.md)
- 🧪 **ML Experimentation & Evaluation**: [docs/evaluation.md](docs/evaluation.md) & [EXPERIMENT.md](EXPERIMENT.md)
- ⚖️ **Ethics & Non-Surveillance Policy**: [docs/ethics-final.md](docs/ethics-final.md) & [docs/expert-validation.md](docs/expert-validation.md)
- ⚠️ **Edge & Failure Case Testing**: [docs/failure-case-testing.md](docs/failure-case-testing.md)
- 📘 **User Guide & Workflow**: [docs/user-guide.md](docs/user-guide.md)
- 👥 **User Validation Protocol**: [docs/user-validation.md](docs/user-validation.md)
- ♿ **Accessibility Validation**: [docs/accessibility-validation.md](docs/accessibility-validation.md)
- 📊 **Before vs After Experiment**: [docs/before-after-experiment.md](docs/before-after-experiment.md)
- 🚀 **Deployment Guide**: [docs/deployment.md](docs/deployment.md)

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

## 9. API Overview

AgriShield provides standard HTTP REST/HTML endpoints documented in [docs/API.md](docs/API.md):

| Endpoint | Method | Functionality |
|---|---|---|
| `GET /` | GET | Application dashboard & workflow status |
| `GET /observe` | GET | Multi-step farmer observation intake form |
| `POST /observe` | POST | Submits observation, validates image, runs ML inference & escalation |
| `GET /scan` / `POST /scan` | GET/POST | Instant single-photo camera diagnostic screening |
| `GET /observation/<id>` | GET | Detailed observation record, explainability & expert feedback |
| `GET /expert/dashboard` | GET | Agricultural expert review triage queue |
| `POST /expert/review/<id>` | POST | Submits expert diagnostic verification & procurement action |
| `GET /analytics` | GET | Real-time database analytics and spatial outbreak heatmaps |
| `GET /outbreak-alerts` | GET | Active regional disease outbreak clusters |
| `GET /batch-qa` | GET | Raw material procurement lot quality grading |
| `GET /health` | GET | Zero-auth JSON health monitor endpoint (`{"status": "ok"}`) |

---

## 10. Database Schema Overview

The database utilizes SQLite with SQLAlchemy ORM (documented in [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md)):

- **`users`**: User authentication with PBKDF2 password hashing (roles: `farmer`, `expert`, `procurement`, `admin`).
- **`observations`**: Crop type, growth stage, visual symptoms, image path, blur score, ML prediction, confidence, and escalation state.
- **`expert_reviews`**: Expert diagnosis, confidence score, treatment advice, lot intake decision (`ACCEPT`, `REJECT`, `QUARANTINE`, `PRICE_DISCOUNT`), and review duration.
- **`batch_procurements`**: Supplier batch lot tracking and acceptance risk scoring.
- **`outbreak_alerts`**: Regional spatial-temporal cluster alerts ($\ge 3$ cases within 48h).

---

## 11. Repository Structure

```text
COE_PROJECT1/
├── app/
│   ├── services/
│   │   ├── analytics_service.py   # Real SQLite database analytics & outbreak alerts
│   │   ├── batch_qa_service.py    # Food-processing batch evaluation
│   │   ├── escalation.py          # Confidence thresholding & SLA review calculation
│   │   ├── image_quality.py       # OpenCV Laplacian blur, brightness & dimension checks
│   │   └── predictor.py           # ML inference, feature extraction & explainability
│   ├── static/                    # CSS, JS, bilingual localization & uploaded photos
│   ├── templates/                 # Jinja2 templates (observe, expert, scan, analytics, 404, 500)
│   ├── config.py                  # Environment and database configuration
│   ├── models.py                  # SQLAlchemy models (User, Observation, ExpertReview, etc.)
│   ├── routes.py                  # Flask route handlers and request processing
│   └── translations.py            # Centralized bilingual English / Tamil dictionary
├── dataset/
│   ├── images/                    # 460 physical crop photos across 17 target classes
│   ├── metadata.csv               # Dataset metadata with 80/10/10 split annotations
│   └── README.md                  # Dataset methodology and distribution documentation
├── docs/                          # Comprehensive technical and scientific documentation suite
│   ├── API.md                     # REST/HTTP route specifications
│   ├── DATA_SCHEMA.md             # SQLite database schema specification
│   ├── SECURITY.md                # Security hardening and threat audit
│   ├── SYSTEMATIC_ERROR_ANALYSIS.md # Failure mode taxonomy and edge-case evaluation
│   ├── FINAL_REVIEW_EVIDENCE.md   # Machine-verifiable evidence matrix
│   ├── FINAL_COMPLETION_MATRIX.md # Review requirement completion status
│   └── PRIVACY_ETHICS.md          # Non-surveillance policy and ethical guidelines
├── ml/
│   ├── saved_model/               # Pre-trained ML model artifacts (model.pkl, metrics.json, etc.)
│   ├── train.py                   # Feature extraction and model training script
│   └── evaluate.py                # Comparative evaluation (Random Forest vs ExtraTrees)
├── scripts/
│   ├── check_dataset.py           # Dataset integrity and zero-duplicate hash verification
│   ├── seed_demo.py               # Controlled demo data seeder ([DEMO DATA] labels)
│   └── setup_env.py               # Environment initialization script
├── tests/                         # 47 automated Pytest unit tests
├── .github/workflows/tests.yml    # Continuous Integration workflow
├── Dockerfile                     # Container deployment image definition
├── docker-compose.yml             # Container orchestration
├── requirements.txt               # Python package dependencies
├── run.py                         # Application entry point
├── USER_GUIDE.md                  # 10-step beginner-friendly walkthrough
└── README.md                      # Project master documentation
```

---

## 12. Future Work & Extensibility

1. **Edge Deployment**: Quantize ML models for low-power edge inference on mobile devices without active internet connection.
2. **Independent Field Trials**: Partner with accredited agricultural extension centers to conduct multi-season validation across diverse soil and light conditions.
3. **Multi-Modal Diagnostic Enhancements**: Incorporate local weather telemetry (humidity, rainfall) into predictive risk scoring models.

---

## 13. License & Disclaimer

*AgriShield is an academic college project. Machine learning screening predictions serve as an initial triage assessment and do not replace professional agricultural expert diagnosis.*
