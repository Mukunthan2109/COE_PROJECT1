# User Guide - Farmer & Expert Workflow

Welcome to the **Farmer-Friendly Disease Observation and Escalation App**. This application connects crop producers with food-processing quality assurance teams for rapid disease triage and expert escalation.

---

## Part 1: Farmer Workflow (Submitting a Crop Observation)

### Step 1: Access the Application & Choose Language
1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Locate the **Language Toggle** in the top right navbar.
3. Click **English** or **தமிழ் (Tamil)** to switch interface labels.

### Step 2: Fill the Observation Form
1. Click **"Report Crop Observation"** on the home banner or navigation bar.
2. Select your **Crop Type** (e.g., *Tomato*, *Potato*, *Chili*).
3. Select the **Visible Symptom** observed on the leaf/crop (e.g., *Leaf Spot*, *Blight*, *Leaf Curl*, *Healthy*).
4. Select the **Crop Growth Stage** (e.g., *Vegetative*, *Flowering*, *Fruiting*).
5. Select your **General Region/Zone** (e.g., *North Zone*, *South Zone*).
6. Click **Choose File** to upload a photo of the affected crop leaf.
7. Add optional observation notes if needed.
8. Click **"Submit Crop Observation"**.

### Step 3: Image Quality Inspection & Retry
- The application automatically verifies your uploaded photo before running ML triage:
  - If the photo is **too blurry**, **too dark**, **overexposed**, or **low resolution**, an alert will appear:
    > *"Image quality is insufficient. Please capture a clearer crop image."*
  - Follow the tips (improve lighting, hold camera steady) and click submit again with a clearer image.

### Step 4: Read the Triage & Screening Result
- Once submitted, you will be taken to the **Screening Result Page**:
  - **Classification Result**: Shows predicted disease label (e.g., *Tomato Leaf Spot*).
  - **Confidence Score**: Indicates ML model confidence (e.g., *88%*).
  - **Visual Indicators**: Displays observed features (e.g., *"Visible dark spot clusters detected"*).
  - **Disclaimer**: *"This result is an initial screening/triage result, not a definitive expert diagnosis."*

### Step 5: Automatic Expert Escalation
- If the ML model confidence is below 70% or if the crop/symptom category is unknown, the application will display:
  > *"The system is not sufficiently confident. This observation has been sent for expert review."*
- You can copy your **Observation ID #** to track the status later.

---

## Part 2: Agricultural Expert Workflow (Dashboard & Validation)

### Step 1: Open Expert Dashboard
1. Click **"Expert Dashboard"** in the top navigation bar or navigate to `http://127.0.0.1:5000/expert`.
2. View the **Time-to-Expert-Review Analytics Cards**:
   - Total Observations, Escalated Cases, Reviewed Count, Average/Median Review Time, Fastest/Slowest Review Times.

### Step 2: Review Pending Escalated Cases
1. Under **"Pending Escalation Queue"**, locate the escalated observation.
2. Review the submitted crop photo, region, crop stage, ML prediction, and confidence score.
3. Click **"Validate / Review"** next to the observation.

### Step 3: Submit Expert Validation
1. Verify or update the **Confirmed / Corrected Disease Label**.
2. Select the **Decision Status**:
   - `Confirmed`: ML screening prediction was accurate.
   - `Corrected`: Updated disease label.
   - `Uncertain`: Requires physical laboratory sample testing.
3. Enter **Expert Advice / Comments** (e.g., treatment recommendations or intake batch segregation instructions).
4. Click **"Submit Review & Record Timestamp"**.

### Step 4: Time-to-Review Verification
- Upon submission, the system automatically calculates:
  `time_to_review = review_timestamp - observation_timestamp`
- The audit log updates instantly with the formatted review time (e.g., `14m 20s`).
