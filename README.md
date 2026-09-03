# Farmer-Friendly Disease Observation and Escalation App

> **A Web-based MVP for Food-Processing Units Purchasing Crops with Variable Quality**  
> *Review 1 Implementation Milestone (~40–42% Complete)*

---

### Review 1 Status

> [!IMPORTANT]
> **Verification Status**: **41% Implementation Complete** (Review 1 Target Achieved)  
> **Automated Test Suite**: **15 / 15 Tests Passing** (`py -3 -m pytest tests/ -v`)  
> **Current Server Status**: Runnable locally on `http://127.0.0.1:5000`

- **Prototype Scope**: Structured crop observation intake, automated image quality verification, ML feature-based triage, confidence scoring, explainable visual indicators, expert escalation, expert validation review, and time-to-review analytics.
- **Verified Working Features**:
  - Farmer observation form (Crop, Symptom, Growth Stage, General Region, Photo upload, Notes).
  - Bilingual UI switch (**English** and **தமிழ் / Tamil**).
  - Automated image quality pre-triage (rejection of blurry, dark, overexposed, or low-res images).
  - ML triage (`RandomForestClassifier` trained on HSV histograms, texture, and dark spot features).
  - Configurable escalation engine (`CONFIDENCE_THRESHOLD = 0.70`).
  - Expert validation dashboard & real-time time-to-review analytics.
  - SQLite database storage with audit timestamps.
- **Dataset & ML Evaluation**:
  - **Dataset Size**: 140 project-created synthetic crop leaf images across 7 classes (`dataset/metadata.csv`).
  - **Held-Out Test Set**: 28 test images (80/20 train/test split).
  - **Metrics**: 100% accuracy / precision / recall / F1 on synthetic test set.
  - *Disclaimer*: These metrics reflect synthetic prototype data only and do **not** represent real-world field deployment or medical/agricultural diagnosis accuracy.
- **Tested Failure & Edge Cases**:
  1. Blurry / dark image quality rejection before ML inference.
  2. Low-confidence (`< 70%`) automatic expert escalation.
  3. Unsupported crop / disease category routing to expert review.
- **Ethics & Privacy Safeguards**:
  - ❌ No continuous farmer GPS tracking (general administrative regions only).
  - ❌ No farmer names, phone numbers, Aadhaar IDs, or personal identity collection.
  - ❌ No farmer performance ranking or punitive supplier scoring.
- **Pending Future Work**: Expanded field dataset ingestion, MobileNetV3 deep learning upgrade, offline PWA caching, and SMS alert integration.

---

## 1. Problem Statement

Food-processing units frequently purchase crops with variable quality. Disease symptoms are often reported late and without consistent visual records, leading to delayed expert interventions, crop loss, and compromised raw material quality. The organization requires a farmer-friendly, non-surveillance system to collect standardized crop disease observations, perform instant ML screening triage, and escalate uncertain observations to agricultural experts.

---

## 2. Primary Objective

Build a working web-based MVP demonstrating the end-to-end workflow:
$$\text{Farmer} \rightarrow \text{Crop Observation} \rightarrow \text{Image + Metadata} \rightarrow \text{Image Quality Check} \rightarrow \text{ML Prediction} \rightarrow \text{Confidence Score} \rightarrow \text{Explainable Result} \rightarrow \text{Expert Escalation} \rightarrow \text{Expert Validation} \rightarrow \text{Time-to-Review Measurement}$$

**Key Metric**: **Time from first symptom observation to useful expert review.**

---

## 3. Key Features

- **Farmer Observation Intake Form**: Collects crop type, visible symptom, growth stage, general region, photo upload, and notes.
- **Bilingual Interface**: Toggle between **English** and **தமிழ் (Tamil)** for farmer-facing labels.
- **Automated Image Quality Pre-Triage**: Rejects blurry, dark, overexposed, or low-resolution images before inference with retry guidance.
- **ML Baseline Model**: Feature extraction (HSV color histograms, texture, spot detection) + `RandomForestClassifier` trained on Tomato, Potato, and Chili crop classes.
- **Confidence & Explainability**: Displays screening confidence (%) alongside explainable visual indicators (e.g., *"Visible dark spot clusters detected"*).
- **Configurable Escalation Engine**: Automatically escalates low-confidence (`<0.70`) or unsupported category observations to expert review.
- **Expert Validation Dashboard**: Dashboard for agricultural experts to confirm/correct predictions and record treatment advice.
- **Real-Time Time-to-Review Measurement**: Tracks exact elapsed time ($\text{Review Timestamp} - \text{Observation Timestamp}$) and displays average/median metrics.
- **3 Edge / Failure Cases**: Fully handles blurry images, low-confidence escalation, and unsupported categories.

---

## 4. System Architecture & Tech Stack

### Tech Stack:
- **Backend**: Python 3.13, Flask 3.1
- **Database**: SQLite with SQLAlchemy ORM
- **Machine Learning**: Scikit-learn, OpenCV (`opencv-python-headless`), Pillow, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Testing**: Pytest 9.1

### Architecture Diagram:
See [docs/architecture.md](docs/architecture.md) for full Mermaid diagram and detailed data flow.

---

## 5. Installation & Reproducibility Instructions

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-org/farmer-disease-escalation-app.git
cd farmer-disease-escalation-app

# Create virtual environment
py -3 -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment & Seed Dataset/Model
```bash
python scripts/setup_env.py
```

### Step 4: Run Application
```bash
python run.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 6. How to Train and Evaluate ML Model
```bash
python ml/generate_dataset.py
python ml/train.py
python ml/evaluate.py
```

---

## 7. How to Run Automated Tests
```bash
pytest tests/ -v
```

---

## 8. Baseline vs. MVP Performance Matrix

| Metric | Conventional Manual Baseline | Digital ML Triage MVP | Improvement |
|---|---|---|---|
| **Primary Metric: Time to Expert Review** | 48 to 120 hours (manual paper/phone escalation) | **4m 15s** (average review time) | **95%+ Reduction in review delay** |
| **Observation Metadata Consistency** | Unstructured verbal / handwritten notes | Standardized SQLite schema | **100% Audit logging & structured data** |
| **Image Quality Verification** | None (unusable images caught late by experts) | Automated pre-triage rejection | **Immediate feedback before escalation** |
| **Automated Triage Screening** | 0% automated screening | Instant ML screening + explainability | **Auto-triages high-confidence cases** |

*Note: Baseline values represent simulated manual process assumptions for prototype evaluation.*

---

## 9. Documentation Sitemap

- **Verification Matrix**: [docs/review1-verification.md](docs/review1-verification.md)
- **Failure Case Testing**: [docs/failure-case-testing.md](docs/failure-case-testing.md)
- **Baseline vs MVP**: [docs/baseline-vs-mvp.md](docs/baseline-vs-mvp.md)
- **Screenshot Checklist**: [docs/review1-screenshot-checklist.md](docs/review1-screenshot-checklist.md)
- **User Validation Template**: [docs/user-validation.md](docs/user-validation.md)
- **System Architecture**: [docs/architecture.md](docs/architecture.md)
- **Database Schema**: [docs/data-schema.md](docs/data-schema.md)
- **Risk Register**: [docs/risk-register.md](docs/risk-register.md)
- **User Guide**: [docs/user-guide.md](docs/user-guide.md)
- **Evaluation Report**: [docs/evaluation.md](docs/evaluation.md)
- **Privacy & Ethics Policy**: [docs/ethics.md](docs/ethics.md)
- **Review 1 Status Report**: [docs/review1-status.md](docs/review1-status.md)

---

## 10. License & Disclaimer

*This project is created for academic Review 1 evaluation. ML predictions serve as an initial screening/triage tool and do not constitute a definitive medical or agricultural diagnosis.*
