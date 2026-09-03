# Database Schema Documentation

The system uses an **SQLite** database managed via **SQLAlchemy ORM** (`app/farmer_app.db`).

---

## Table 1: `observations`

Stores crop observations submitted by farmers along with ML triage outputs and escalation status.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto-increment | Unique Observation Identifier |
| `crop` | VARCHAR(50) | NOT NULL | Crop type (Tomato, Potato, Chili) |
| `symptom` | VARCHAR(100) | NOT NULL | Visible symptom selected by farmer |
| `crop_stage` | VARCHAR(50) | NOT NULL | Crop growth stage (Seedling, Vegetative, Flowering, Fruiting, Harvest) |
| `location_region` | VARCHAR(100) | NOT NULL | General region/zone (e.g., North Zone, South Zone) |
| `image_path` | VARCHAR(255) | NOT NULL | Relative path to uploaded crop image |
| `observation_notes` | TEXT | NULLABLE | Optional farmer observation comments |
| `observation_timestamp` | DATETIME | NOT NULL, DEFAULT UTC | Timestamp when observation was created |
| `model_prediction` | VARCHAR(100) | NULLABLE | ML baseline predicted disease label |
| `confidence` | FLOAT | NULLABLE | ML prediction confidence score (0.0 to 1.0) |
| `explainability_notes` | TEXT | NULLABLE | Semicolon-separated visual indicators explaining prediction |
| `status` | VARCHAR(50) | NOT NULL, DEFAULT 'Needs expert review' | Workflow status ('Initial screening result', 'Needs expert review', 'Reviewed by expert') |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC | System record creation timestamp |

---

## Table 2: `expert_reviews`

Stores validation decisions, expert comments, review timestamps, and exact time-to-review calculations.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto-increment | Unique Expert Review Record ID |
| `observation_id` | INTEGER | Foreign Key (`observations.id`), NOT NULL | References parent observation |
| `expert_label` | VARCHAR(100) | NOT NULL | Confirmed or corrected disease diagnosis |
| `expert_status` | VARCHAR(50) | NOT NULL | Validation decision ('Confirmed', 'Corrected', 'Uncertain') |
| `expert_comment` | TEXT | NULLABLE | Expert advisory notes / treatment recommendations |
| `review_timestamp` | DATETIME | NOT NULL, DEFAULT UTC | Timestamp when expert submitted review |
| `time_to_review_seconds` | FLOAT | NOT NULL | Elapsed time in seconds between submission and review |

---

## Table 3: `dataset_metadata`

Tracks metadata for project-created and public crop image datasets.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto-increment | Record ID |
| `image_id` | VARCHAR(50) | UNIQUE, NOT NULL | Image accession ID (e.g., IMG_0001) |
| `image_path` | VARCHAR(255) | NOT NULL | Relative path to dataset image |
| `crop` | VARCHAR(50) | NOT NULL | Crop species |
| `symptom` | VARCHAR(100) | NOT NULL | Associated symptom category |
| `disease_label` | VARCHAR(100) | NOT NULL | Ground truth disease label |
| `location_region` | VARCHAR(100) | NOT NULL | Simulated general region |
| `crop_stage` | VARCHAR(50) | NOT NULL | Crop stage |
| `source_type` | VARCHAR(50) | NOT NULL | 'project_created' or 'public_licensed' |
| `expert_validation` | VARCHAR(50) | DEFAULT 'pending' | Ground truth validation state |
| `license_or_source_note` | VARCHAR(255) | NULLABLE | Licensing or provenance documentation |
