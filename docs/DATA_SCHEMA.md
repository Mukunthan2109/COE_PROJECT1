# AgriShield Database Schema Documentation

AgriShield uses **SQLite** (via **SQLAlchemy ORM**) for lightweight, zero-configuration database persistence.

---

## Entity-Relationship Diagram (Conceptual)

```
+--------------------+        1:N         +--------------------------+
|       User         |------------------->|       Observation        |
| (Farmer/Expert/Admin)|                  | (Crop Disease Record)    |
+--------------------+                    +--------------------------+
          |                                            |
          | 1:N                                        | 1:1
          v                                            v
+--------------------+                    +--------------------------+
|    ExpertReview    |<-------------------|       ExpertReview       |
| (Diagnostic Feedback)|                   | (Diagnostic Feedback)    |
+--------------------+                    +--------------------------+
```

---

## Data Tables & Attributes

### 1. `users` Table
Stores registered user accounts (Farmers, Quality Experts, Procurement Managers, Admins).

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `username` | String(80) | Unique, Not Null | Unique username for login |
| `email` | String(120) | Unique, Not Null | Contact email address |
| `password_hash` | String(256) | Not Null | Werkzeug generate_password_hash string |
| `role` | String(20) | Not Null, Default: 'farmer' | Role: `farmer`, `expert`, `procurement`, `admin` |
| `created_at` | DateTime | Not Null | Account creation timestamp |

---

### 2. `observations` Table
Stores disease observation reports submitted by farmers or quality control scanners.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique observation report ID |
| `farmer_name` | String(100) | Not Null | Name of reporting farmer |
| `farmer_contact` | String(50) | Nullable | Contact number or location reference |
| `crop` | String(50) | Not Null | Crop type (Tomato, Potato, Rice, Maize, Chili, Grape, Apple) |
| `growth_stage` | String(50) | Not Null | Growth stage (Seedling, Vegetative, Flowering, Fruiting, Harvest) |
| `region` | String(100) | Not Null | Geographical region / district name |
| `first_symptom_days` | Integer | Not Null, Default: 1 | Number of days symptoms have been present |
| `symptoms_json` | Text | Nullable | JSON string storing list of selected visual symptoms |
| `notes` | Text | Nullable | Additional farmer observations or text notes |
| `image_filename` | String(255) | Not Null | Filename of uploaded crop image stored on disk |
| `image_quality_passed` | Boolean | Not Null, Default: True | Flag indicating image quality check result |
| `image_blur_score` | Float | Nullable | Laplacian variance score measuring image blur |
| `predicted_disease` | String(100) | Nullable | ML model predicted class name |
| `ml_confidence` | Float | Nullable | ML prediction confidence probability (0.0 to 1.0) |
| `status` | String(30) | Not Null, Default: 'pending' | Status: `pending`, `escalated`, `reviewed`, `resolved` |
| `requires_escalation` | Boolean | Not Null, Default: False | Escalation trigger flag (set if low confidence or high severity) |
| `escalation_reason` | String(255) | Nullable | Cause for automatic escalation trigger |
| `observation_timestamp` | DateTime | Not Null | Date and time of report submission |
| `user_id` | Integer | ForeignKey('users.id'), Nullable | Associated user account ID if authenticated |

---

### 3. `expert_reviews` Table
Stores diagnostic verification, recommendations, and risk classifications submitted by agricultural experts.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique review ID |
| `observation_id` | Integer | ForeignKey('observations.id'), Unique, Not Null | Associated observation record ID |
| `expert_id` | Integer | ForeignKey('users.id'), Not Null | Expert user who completed the review |
| `confirmed_disease` | String(100) | Not Null | Expert verified disease diagnosis |
| `expert_confidence` | Float | Not Null | Expert's confidence score (0.0 - 1.0) |
| `recommended_action` | Text | Not Null | Actionable advisory for farmer treatment/containment |
| `procurement_action` | String(50) | Not Null | Decision: `ACCEPT`, `REJECT`, `QUARANTINE`, `PRICE_DISCOUNT` |
| `notes` | Text | Nullable | Additional clinical notes |
| `expert_validation_status` | String(50) | Default: 'PENDING INDEPENDENT VALIDATION' | Label ensuring zero fabricated validation claims |
| `reviewed_at` | DateTime | Not Null | Timestamp of expert review completion |

---

### 4. `batch_procurements` Table
Stores crop lot intake decisions made by food-processing procurement managers.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique batch ID |
| `batch_code` | String(50) | Unique, Not Null | Supplier batch lot identifier |
| `crop` | String(50) | Not Null | Crop species |
| `supplier_name` | String(100) | Not Null | Farmer/Cooperative supplier name |
| `quantity_kg` | Float | Not Null | Total batch weight in kilograms |
| `quality_grade` | String(20) | Not Null | Assigned grade: `GRADE_A`, `GRADE_B`, `REJECTED` |
| `accepted` | Boolean | Not Null | Lot acceptance decision flag |
| `evaluated_at` | DateTime | Not Null | Lot evaluation timestamp |

---

### 5. `outbreak_alerts` Table
Stores spatial-temporal disease outbreak clusters detected across regions.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Alert ID |
| `region` | String(100) | Not Null | Region under outbreak warning |
| `crop` | String(50) | Not Null | Affected crop |
| `disease` | String(100) | Not Null | Identified disease |
| `case_count` | Integer | Not Null | Count of observations triggering cluster threshold |
| `severity` | String(20) | Not Null | Alert level: `WARNING`, `CRITICAL` |
| `triggered_at` | DateTime | Not Null | Outbreak detection timestamp |
| `is_active` | Boolean | Default: True | Active status of alert |

---

## Database Migrations & Seeding

- Database initialized automatically via SQLAlchemy `db.create_all()`.
- Synthetic demo data seeded safely using `py -3 scripts/seed_demo.py` with explicit `[DEMO DATA]` labels.
