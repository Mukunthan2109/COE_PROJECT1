# Review 1 Screenshot Capture Checklist

This document provides a structured checklist for evaluators and presenters to capture visual evidence of the running **Farmer-Friendly Disease Observation and Escalation App**.

> [!NOTE]
> **MANUAL CAPTURE INSTRUCTIONS**: Ensure the local server is running (`python run.py`). Open your browser to `http://127.0.0.1:5000` and follow the URL paths below to capture high-resolution screenshots for presentation slides or documentation.

---

## Required Screenshot Checklist (12 Items)

| # | Screenshot Target | URL / Route | Target Page Elements to Capture | Capture Status |
|---|---|---|---|---|
| **1** | **Home Landing Page** | `http://127.0.0.1:5000/` | Hero banner, navigation links, quick metrics summary cards, recent submissions table. | Ready for Capture |
| **2** | **Farmer Observation Form** | `http://127.0.0.1:5000/observe` | Form dropdowns for Crop, Symptom, Growth Stage, Region, File Upload input, and Privacy notice. | Ready for Capture |
| **3** | **Image Upload Controls** | `http://127.0.0.1:5000/observe` | File picker input showing selected `.jpg`/`.png` file ready for submission. | Ready for Capture |
| **4** | **Prediction Result Page** | `http://127.0.0.1:5000/result/<id>` | Predicted disease classification label, uploaded leaf image preview, and observation metadata card. | Ready for Capture |
| **5** | **Confidence Score & Explainability** | `http://127.0.0.1:5000/result/<id>` | ML screening confidence progress bar (`%`) and bulleted explainable visual indicators list. | Ready for Capture |
| **6** | **Low-Confidence Escalation Alert** | `http://127.0.0.1:5000/result/<id>` | Yellow escalation warning box (*"System not sufficiently confident. Sent for expert review"*). | Ready for Capture |
| **7** | **Expert Dashboard Overview** | `http://127.0.0.1:5000/expert` | Pending Escalation Queue table, completed reviews audit log, and time-to-review summary metrics. | Ready for Capture |
| **8** | **Expert Validation Form** | `http://127.0.0.1:5000/expert/review/<id>` | Confirmed/corrected disease label input, validation decision dropdown (`Confirmed`/`Corrected`), and comment box. | Ready for Capture |
| **9** | **Time-to-Review Metric** | `http://127.0.0.1:5000/expert` | Analytics metric cards highlighting **Average Review Time**, **Median Review Time**, Fastest/Slowest times. | Ready for Capture |
| **10** | **Bilingual Tamil Interface** | `http://127.0.0.1:5000/observe` | Navbar language toggle set to **தமிழ்**, showing translated Tamil form labels and headings. | Ready for Capture |
| **11** | **Failure-Case Behaviour (Blurry Image)** | `http://127.0.0.1:5000/observe` | Red alert box displaying *"Image quality is insufficient. Crop image is blurry or out of focus."* | Ready for Capture |
| **12** | **Automated Test Results Output** | Terminal Execution | Terminal output showing `15 passed in 5.21s` after running `pytest tests/ -v`. | Ready for Capture |

---

## Instructions for Including Screenshots in Documentation

To save and embed captured screenshots into artifacts:
1. Save captured PNG images into `docs/screenshots/` (e.g. `docs/screenshots/01_homepage.png`).
2. Embed into markdown using: `![Homepage Screenshot](file:///c:/Users/mukun/OneDrive/Desktop/ceo/docs/screenshots/01_homepage.png)`.
