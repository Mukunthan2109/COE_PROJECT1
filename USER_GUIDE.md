# AgriShield User Guide & Workflow Walkthrough

Welcome to **AgriShield** — Early Crop Disease Observation, AI Screening, and Expert Escalation System.

---

## 1. System Navigation

The application navigation bar includes:
- **Home**: Overview of the escalation workflow and system status.
- **New Observation**: Step-by-step form for farmers to submit crop health photos.
- **Instant AI Scanner**: Quick diagnostic analysis tool for immediate photo screening.
- **History**: Farmer observation history table with filters and detailed views.
- **Expert Portal**: Portal for agricultural experts to review escalated cases.
- **Analytics**: Real-time management metrics, charts, and regional outbreak alerts.
- **System Evaluation**: Dynamic machine learning performance metrics.
- **Feedback**: Usability feedback submission page.
- **Language Switcher**: Toggle between **English** and **தமிழ் (Tamil)** at any time.

---

## 2. Farmer Observation Submission Workflow

1. Navigate to **New Observation** (`/observe`).
2. **Step 1: Upload Photo**: Select or capture a clear photo of the plant leaf or stem (max 5MB, JPG/PNG/WEBP).
3. **Step 2: Select Crop**: Choose from the supported crops (**Tomato**, **Potato**, **Rice**, **Maize / Corn**).
4. **Step 3: Select Growth Stage**: Choose growth stage (**Seedling**, **Vegetative**, **Flowering**, **Fruiting**, **Harvest**).
5. **Step 4: Select Visible Symptoms**: Choose observed visual signs (e.g., *Yellowing leaves*, *Brown spots*, *Wilting*).
6. **Step 5: Location & Timing**: Enter approximate region and first symptom datetime.
7. Click **Submit Observation for Screening**.
8. View **Screening Result**: Inspect predicted disease, confidence level (%), risk level, visual explainability notes, and escalation status.

---

## 3. Expert Review & Escalation Workflow

1. Observations with screening confidence `< 70%` or high risk are automatically escalated to **Needs expert review**.
2. Agricultural experts log in and navigate to **Expert Portal** (`/expert`).
3. Click **Review & Validate** on any pending case.
4. View the **actual uploaded crop photo** (click image for full-size lightbox viewer), intake metadata, and AI screening notes.
5. Select expert validation status (**Validated (Confirmed)**, **Not Confirmed**, or **Needs More Information**).
6. Enter confirmed expert diagnosis and treatment advice.
7. Submit validation — the system automatically calculates exact SLA review duration (`time_to_review_seconds`).

---

## 4. Language Toggling

Click the **language button** in the top navigation bar to switch between **English** and **தமிழ் (Tamil)**. Language preferences persist across page navigation.
