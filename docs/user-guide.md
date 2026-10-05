# AgriShield User Guide & Step-by-Step Workflow Walkthrough

Welcome to **AgriShield** — Early Crop Disease Observation, AI Screening, and Expert Escalation System for Food-Processing Procurement Units.

---

## 1. Starting the Application

To launch AgriShield locally on your computer:

```bash
# 1. Activate the Python virtual environment
.venv\Scripts\activate

# 2. Verify environment configuration
py -3 scripts/setup_env.py

# 3. Optional: Seed demo records for testing
py -3 scripts/seed_demo.py

# 4. Start the Flask application server
py -3 run.py
```

Open your web browser and navigate to: **`http://127.0.0.1:5000`**

---

## 2. Farmer Observation Submission

1. On the home page or navigation bar, click **"New Observation"** (`/observe`).
2. Enter your Name or Farmer ID and optional contact information.
3. Select your Crop: **Tomato**, **Potato**, **Rice**, **Maize**, **Chili**, **Grape**, or **Apple**.
4. Select the **Growth Stage** (e.g., Seedling, Vegetative, Flowering, Fruiting, Harvest).
5. Specify your general geographic **Region / District** (e.g., Coimbatore, Madurai, Salem).
6. Select observed visual symptom tags (e.g., *Brown spots*, *Yellowing*, *Wilting*).
7. Enter how many days since symptoms first appeared and optional notes.

---

## 3. Image Upload / Camera Capture

1. In the photo section of the form, tap **"Choose File"** or use your mobile device's camera.
2. Select a clear, well-focused close-up photo of the affected plant leaf, stem, or fruit.
3. Supported formats: **JPEG (`.jpg`, `.jpeg`)** and **PNG (`.png`)**. Maximum file size: **16 MB**.

---

## 4. Image-Quality Feedback & Validation Messages

AgriShield automatically inspects your photo before running disease predictions:
- **Sharp & Well-Lit Photos**: Pass immediately with an automated quality check badge.
- **Blurry Photos**: If camera shake or out-of-focus capture is detected (Laplacian variance < 100), the system displays a clear, friendly alert: *"Image appears blurry or out of focus. Please retake a clear photo for accurate screening."*
- **Dark or Overexposed Photos**: Alerts you to retake under balanced natural or shaded light.
- **Corrupted / Invalid Files**: Rejects non-image files safely without crashing or exposing technical errors.

---

## 5. Machine Learning Prediction

Once the photo passes quality checks:
1. The AI engine extracts color histograms, texture features (Haralick descriptors), and edge structures.
2. The pre-trained ensemble model compares the leaf against trained patterns across 17 target classes.
3. The screening screen displays:
   - **Identified Condition**: (e.g., *Tomato Early Blight*, *Healthy Crop*, etc.)
   - **Explainability Breakdown**: Visual symptom match summary.

---

## 6. Confidence Scoring

- Every prediction is accompanied by a transparent **Confidence Score** (e.g., `88.5%` or `54.2%`).
- High Confidence ($\ge 70\%$): Indicates strong model agreement with known reference patterns.
- Low Confidence ($< 70\%$): Highlights ambiguity or atypical symptom patterns.

---

## 7. Escalation Decision

- **Non-Surveillance & Triage Policy**: The AI is strictly an initial screening aid, not a certified final diagnosis.
- **Automatic Escalation**: If the confidence score is below **70%**, or if high-severity symptoms are flagged, the system automatically marks the observation as **Needs Expert Review** (`escalated`).
- The farmer sees a clear notice: *"This observation has been routed to our agricultural quality experts for manual diagnostic verification."*

---

## 8. Expert Review Portal

Agricultural pathologists and food-processing quality managers review cases via `/expert/dashboard`:
1. Open the **Expert Dashboard** (`/expert/dashboard`).
2. Click **"Review & Validate"** on any pending or escalated case.
3. Inspect the high-resolution photo, farmer metadata, and AI screening suggestions.
4. Input confirmed diagnosis, confidence rating, farmer treatment advisory, and raw material procurement intake decision (`ACCEPT`, `REJECT`, `QUARANTINE`, or `PRICE_DISCOUNT`).
5. Click **Submit Review**. The database updates status to `reviewed`/`resolved`.

---

## 9. Status Tracking & History

Farmers and procurement officers can track report progress via `/observations`:
- **`SUBMITTED` / `PENDING`**: Initial submission received and queued.
- **`PREDICTED`**: Automated AI screening completed.
- **`ESCALATED`**: Routed to agricultural specialist for evaluation.
- **`REVIEWED`**: Expert diagnosis and advisory recorded.
- **`RESOLVED`**: Procurement decision and farmer advisory finalized.

---

## 10. Real-Time Analytics & Regional Outbreaks

Navigate to **"Analytics"** (`/analytics`) to explore:
- **Total Intake Statistics**: Total submissions, pending reviews, and resolution rates.
- **Regional Disease Clustering**: Active **Outbreak Alerts** when $\ge 3$ similar cases emerge in the same district within 48 hours.
- **SLA Resolution Latency**: Average and median time between farmer observation submission and expert review completion.
- Note: If no records exist, the dashboard displays clean empty states (*"No data available"*) instead of fabricated dummy numbers.
