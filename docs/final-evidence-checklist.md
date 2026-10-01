# AgriShield Final Evidence & Verification Checklist

## 1. Required Demonstration Screenshots (20 Items)

| # | Demonstration View | URL / Location | Verification Status |
|---|---|---|---|
| 1 | **Home Landing Page** | `GET /` | `VERIFIED` |
| 2 | **Tamil Language Interface** | `GET /?lang=ta` | `VERIFIED` |
| 3 | **Farmer Observation Form** | `GET /observe` | `VERIFIED` |
| 4 | **Mobile Camera Capture Control** | `GET /observe` (`capture="environment"`) | `VERIFIED` |
| 5 | **Image Quality Rejection Alert** | `POST /observe` (Blurry image) | `VERIFIED` |
| 6 | **Instant AI Scanner** | `GET /scan` | `VERIFIED` |
| 7 | **Screening Result & Visual Indicators** | `POST /observe` (Passed image) | `VERIFIED` |
| 8 | **Low-Confidence Escalation Notice** | `GET /result/<id>` (Confidence < 0.70) | `VERIFIED` |
| 9 | **Observation Status Tracker Timeline** | `GET /status` | `VERIFIED` |
| 10 | **Expert Login Screen** | `GET /login` | `VERIFIED` |
| 11 | **Expert Review Dashboard Queue** | `GET /expert` | `VERIFIED` |
| 12 | **Expert Review Modal & Decision Input** | `GET /expert/review/<id>` | `VERIFIED` |
| 13 | **Confirmed / Corrected Status Update** | `POST /expert/review/<id>` | `VERIFIED` |
| 14 | **Time-to-Review SLA Analytics** | `GET /analytics` | `VERIFIED` |
| 15 | **Real DB Analytics Charts** | `GET /analytics` | `VERIFIED` |
| 16 | **Systematic Failure Case Handling** | `tests/test_image_quality.py` | `VERIFIED` |
| 17 | **Pytest Test Suite Execution Output** | `py -3 -m pytest tests/` | `VERIFIED` |
| 18 | **ML Model Evaluation Metrics Output** | `py -3 ml/evaluate.py` | `VERIFIED` |
| 19 | **System Architecture Diagram** | `docs/architecture.md` | `VERIFIED` |
| 20 | **GitHub Repository Repository Structure** | `https://github.com/Mukunthan2109/COE_PROJECT1` | `VERIFIED` |
