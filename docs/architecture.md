# System Architecture & Data Flow Specification

## 1. System Architecture Diagram

```mermaid
graph TD
    A["🌾 Farmer / User Interface (Responsive HTML/CSS/JS + English/Tamil Toggle)"] -->|POST Observation + Image| B["⚡ Flask Web Application Backend (app/routes.py)"]
    
    subgraph Pre-Triage Verification
        B -->|1. Validate File & Format| C["🔍 Image Quality Check Service (app/services/image_quality.py)"]
        C -->|Quality Rejected (Blur/Dark/Bright)| A
    end

    subgraph ML Triage Pipeline
        C -->|Quality Passed| D["🧠 ML Feature Classifier (app/services/predictor.py)"]
        D -->|Extract HSV/Texture/Color Features| E["📦 Trained RandomForest Classifier (ml/saved_model/model.pkl)"]
        E -->|Return Label + Confidence Score| D
        D -->|Generate Explainable Visual Indicators| F["⚡ Escalation Engine (app/services/escalation.py)"]
    end

    subgraph Escalation & Decision Engine
        F -->|Confidence >= 70% & Supported| G["✅ Status: Initial Screening Result"]
        F -->|Confidence < 70% or Unsupported| H["⚠️ Status: Needs Expert Review (Escalated)"]
    end

    subgraph Data Persistence
        G --> I[("💾 SQLite Database (app/farmer_app.db)")]
        H --> I
    end

    subgraph Expert Escalation & Audit Workflow
        I -->|Pull Pending Queue| J["👨‍🌾 Expert Review Dashboard (app/templates/expert.html)"]
        J -->|Submit Expert Diagnosis & Timestamp| K["📝 Record Expert Validation & Time-to-Review"]
        K -->|Calculate: Time_To_Review = Review_Time - Submission_Time| I
    end

    subgraph Analytics Engine
        I --> L["📊 Real-Time Time-to-Review Analytics & Baseline Matrix"]
    end
```

---

## 2. End-to-End Data Flow Steps

1. **Observation Creation**: Farmer selects crop type, visible symptom, crop growth stage, general region, uploads crop leaf image, and adds optional observation notes.
2. **Form & Upload Validation**: Flask validates required inputs and checks file extensions (`.jpg`, `.png`, `.webp`).
3. **Automated Image Quality Inspection**:
   - Checks image resolution (min 100x100 pixels).
   - Evaluates mean brightness (detecting underexposed `<30` or overexposed `>225` photos).
   - Computes Laplacian variance to catch out-of-focus / blurry photos.
   - If quality fails -> Returns user-friendly retry message (*"Image quality is insufficient. Please capture a clearer crop image."*).
4. **Machine Learning Triage & Explainability**:
   - Feature extraction: HSV color histograms, mean RGB/HSV stats, edge density, and dark spot area ratios.
   - Inference via `RandomForestClassifier`.
   - Generates human-understandable visual indicators explaining the screening rationale.
5. **Confidence & Escalation Decisioning**:
   - Configurable threshold `CONFIDENCE_THRESHOLD = 0.70`.
   - If confidence >= 0.70 and category is supported -> Assigned status `"Initial screening result"`.
   - If confidence < 0.70 or category is unknown -> Assigned status `"Needs expert review"`.
6. **Database Persistence**: Observation record stored in SQLite database.
7. **Expert Dashboard Queue**: Escalated observations appear in the pending queue for agricultural experts.
8. **Expert Validation & Time-to-Review Measurement**:
   - Expert views observation image, screening prediction, and visual indicators.
   - Expert submits confirmed/corrected diagnosis, status (`Confirmed`, `Corrected`, `Uncertain`), and advisory comments.
   - System records `review_timestamp` and computes exact elapsed time:
     `time_to_review_seconds = review_timestamp - observation_timestamp`.
9. **Analytics Aggregation**: Updates total observations, escalated cases count, average/median review time, fastest/slowest review time, and baseline comparison.
