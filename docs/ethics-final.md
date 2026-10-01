# AgriShield Ethical Data Handling & Non-Surveillance Architecture

## 1. Ethical Governance Principles

AgriShield adheres strictly to non-surveillance, non-punitive, and privacy-preserving design principles tailored for smallholder farmers and food-processing procurement networks.

---

## 2. Core Ethical Commitments

### A. Non-Surveillance Design
- **No Continuous GPS Tracking**: The system does not track continuous real-time farmer location.
- **Coarse Administrative Regionalization**: Location data uses broad administrative zones (*e.g., North Zone, South Zone*).
- **No Device Fingerprinting / Personal Profiling**: User interactions are strictly limited to disease screening without passive background telemetry.

### B. Non-Punitive Farmer Protection
- **No Automated Purchasing Rejections**: Machine learning screening outputs serve as preliminary indicators for expert triage and **never** trigger automated financial or crop batch rejections.
- **No Farmer Performance Ranking**: Data is not used to score, rank, or penalize individual farmers or cooperative members.
- **No Private Data Monetization**: Images and metadata are maintained strictly within the project database for disease triage.

### C. Data Privacy & Minimization
- **Zero Personally Identifiable Information (PII)**: No facial photos, national identity numbers (Aadhaar), phone numbers, or exact residential addresses are collected.
- **Isolated Runtime Uploads**: Runtime farmer submissions are saved in `app/static/uploads/` and are isolated from the training dataset.

---

## 3. Human-in-the-Loop Expert Escalation Guarantee

Machine learning confidence scores below threshold (`< 0.70`) automatically route observations to human agricultural pathologists. Certified experts validate diagnosis before any official agronomic advisory is issued to farmers.
