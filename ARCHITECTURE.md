# AgriShield System Architecture & End-to-End Data Flow Specification

## 1. System Architecture Diagram

```mermaid
graph TD
    A["🌾 Farmer Web Interface (Responsive HTML5/Bootstrap + Mobile Camera Capture + Tamil/English Toggle)"] -->|POST Observation + Crop Image + Metadata| B["⚡ Flask Web Application Backend (app/routes.py)"]
    
    subgraph Security & Quality Pre-Triage
        B -->|1. Validate File Extension, Size & MIME| C1["🔒 Security & MIME Validator (app/routes.py)"]
        C1 -->|2. Image Quality Inspection| C2["🔍 Image Quality Service (app/services/image_quality.py)"]
        C2 -->|Quality Rejected (Blur / Darkness / Brightness / Resolution)| A
    end

    subgraph ML Screening & Explainability Pipeline
        C2 -->|Quality Passed| D["🧠 ML Disease Screening Service (app/services/predictor.py)"]
        D -->|Extract 37-dim HSV / GLCM Texture / Spot Features| E["📦 Machine Learning Model (ml/saved_model/model.pkl)"]
        E -->|Return Label + Confidence Score| D
        D -->|Generate Visual Indicators & Spot Count| F["⚡ Risk & Escalation Engine (app/services/escalation.py)"]
    end

    subgraph Risk Triage & Confidence Escalation
        F -->|High Confidence (>= 0.75) & Supported Crop| G["✅ Status: Initial Screening Result"]
        F -->|Low Confidence (< 0.70) or Unknown Disease| H["⚠️ Status: Needs Expert Review (Escalated)"]
    end

    subgraph Persistence & Audit Layer
        G --> I[("💾 SQLite Database (app/farmer_app.db)")]
        H --> I
    end

    subgraph Expert Review & Validation Workflow
        I -->|Pull Pending Escalation Queue| J["👨‍🌾 Expert Review Dashboard (app/templates/expert.html)"]
        J -->|Submit Expert Diagnosis & Notes| K["📝 Persist Expert Review & Timestamp"]
        K -->|Compute Time_To_Review = Review_Time - First_Symptom_Time| I
    end

    subgraph Analytics & Error Analysis Engine
        I --> L["📊 Real DB SLA Metrics, Review Time Distribution & Systematic Error Analysis"]
    end
```

---

## 2. End-to-End Data Flow Steps

1. **Farmer Intake & Metadata Standardized Capture**:
   - Farmer opens web app, toggles language (English / Tamil), selects crop, symptom, growth stage, general region, first symptom date, observation notes, and takes/selects photo via `<input type="file" accept="image/*" capture="environment">`.
2. **Security & Image Quality Inspection**:
   - File extension (`.jpg`, `.jpeg`, `.png`, `.webp`), MIME type, and max file size (16MB) verified.
   - Quality checks: resolution (>= 100x100), brightness (30-225 range), blur detection (Laplacian variance >= 100), and MD5 hash duplicate detection.
3. **ML Screening & Visual Feature Extraction**:
   - 37-dimensional feature extraction (HSV color histograms, mean/std channel stats, GLCM texture features, lesion spot counts).
   - Inference via trained classifier returning class probability distribution.
   - Explainability payload created with dark spot counts, GLCM contrast/homogeneity, and visual indicators.
4. **Risk Triage & Escalation Engine**:
   - High confidence (`>= 0.75`) -> `"Initial screening result"`.
   - Medium confidence (`0.70 - 0.74`) -> `"Screening result — expert confirmation recommended"`.
   - Low confidence (`< 0.70`) or unsupported crop -> `"Needs expert review"` (Escalated).
5. **Database Persistence & Status Tracker**:
   - Observation assigned unique UUID code and stored in SQLite database with status tracking history.
6. **Expert Portal & Persistent Review**:
   - Authenticated expert opens `/expert` queue, reviews full-resolution image, metadata, model screening result, and visual indicators.
   - Expert submits decision (`Confirmed`, `Corrected`, `Uncertain`) with advisory comments.
7. **SLA & Time-to-Review Calculation**:
   - Computes elapsed SLA time: `Useful_Expert_Review_Time = expert_review_completed_at - first_symptom_observed_at`.
8. **Real-Time Analytics & Systematic Error Tracking**:
   - Computes dynamic database analytics for observations by crop, status, growth stage, confidence distribution, review time distribution (average, median, min, max), and empirical error logging.
