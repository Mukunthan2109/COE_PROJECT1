# AgriShield Dataset Data Provenance Report

## 1. Overview & Provenance Philosophy

Data provenance documents the origin, licensing, metadata attributes, and ethical lineage of every image included in the AgriShield dataset. All 460 images are project-created or licensed under open educational terms without farmer PII or surveillance data.

---

## 2. Dataset Provenance & Licensing Matrix

| Image Source / Batch | Sample Count | Source Type | License Type | Usage Scope | Validation Status |
|---|---|---|---|---|---|
| **Core Crop Set (Tomato, Potato, Rice, Maize)** | 360 | `PROJECT_CREATED` | CC-BY-4.0 Open Educational | Baseline ML Feature Training & Triage Evaluation | `PENDING_VALIDATION` (Curator Labeled) |
| **Expanded Crop Set (Chili, Grape, Apple)** | 100 | `PROJECT_CREATED` | CC-BY-4.0 Open Educational | Multi-crop Expansion Screening | `PENDING_VALIDATION` (Curator Labeled) |
| **Total Active Dataset** | **460** | `PROJECT_CREATED` | **CC-BY-4.0** | **17-Class Screening Classifier** | **`PENDING_VALIDATION`** |

---

## 3. Data Leakage Prevention

- **Hash Verification**: `scripts/check_dataset.py` verifies zero duplicate MD5 image hashes across the dataset.
- **Stratified Split**: Images are divided into 80% Train (`368`), 10% Validation (`46`), and 10% Test (`46`) using fixed random seed (`random_state=42`). No single image source or near-duplicate file appears across both training and held-out test splits.
