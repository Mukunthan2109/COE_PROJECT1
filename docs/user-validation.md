# User Usability Validation Protocol & Evaluation Template

This document provides the standardized user validation protocol and feedback collection template for evaluating the **Farmer-Friendly Disease Observation and Escalation App** with representative farmer and expert participants.

> [!IMPORTANT]
> **STATUS**: **PENDING USER VALIDATION**  
> *Note*: In accordance with academic review ethics, no fake user participants, survey scores, or user quotes have been fabricated. User validation will be conducted with actual agricultural stakeholders prior to final project submission.

---

## 1. Usability Test Tasks

Participants are asked to perform the following 6 core tasks on `http://127.0.0.1:5000`:

| Task ID | Task Description | Target System Page | Success Criteria |
|---|---|---|---|
| **T1** | **Select Language Preference** | Home / Navbar | Successfully toggle between English and Tamil interfaces. |
| **T2** | **Create Crop Observation** | `/observe` | Select crop type, visible symptom, growth stage, and general region. |
| **T3** | **Upload Crop Image** | `/observe` | Select and attach a crop leaf photo from local device. |
| **T4** | **Read Triage Result** | `/result/<id>` | Locate and read the predicted disease label and screening status. |
| **T5** | **Understand Confidence Score** | `/result/<id>` | Interpret the ML screening confidence percentage progress bar (`%`). |
| **T6** | **Understand Expert Escalation** | `/result/<id>` | Read and comprehend the escalation notice when confidence is low (`<70%`). |

---

## 2. Qualitative Usability Evaluation Questions

Following completion of the test tasks, participants answer 6 standardized usability questions (rated 1 = Strongly Disagree to 5 = Strongly Agree):

1. **Ease of Use**: Was the interface easy to navigate and understand?
2. **Label Clarity**: Were form controls and crop/symptom labels clear and unambiguous?
3. **Language Support**: Was the language (English / Tamil) natural and understandable?
4. **Explainability**: Was the prediction explanation and visual indicators list understandable?
5. **Escalation Clarity**: Was the expert review escalation message clear regarding next steps?
6. **Autonomy**: Could you complete the observation submission without technical assistance?

---

## 3. User Feedback Collection Table

*(To be populated during live stakeholder testing sessions)*

| Participant ID | Role (Farmer / Expert) | Tasks Completed (T1–T6) | Avg Rating (1–5) | Key Feedback / Comments | Testing Date |
|---|---|---|---|---|---|
| *P-01* | *Pending User Validation* | *Pending* | *Pending* | *Testing session scheduled* | *Pending* |
| *P-02* | *Pending User Validation* | *Pending* | *Pending* | *Testing session scheduled* | *Pending* |
| *P-03* | *Pending User Validation* | *Pending* | *Pending* | *Testing session scheduled* | *Pending* |
| *P-04* | *Pending User Validation* | *Pending* | *Pending* | *Testing session scheduled* | *Pending* |
| *P-05* | *Pending User Validation* | *Pending* | *Pending* | *Testing session scheduled* | *Pending* |
