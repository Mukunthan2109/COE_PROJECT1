# Privacy, Non-Surveillance & Ethics Policy

The **Farmer-Friendly Disease Observation and Escalation App** is engineered with strict ethical guidelines to safeguard farmer autonomy, prevent surveillance creep, and ensure non-punitive quality management in food-processing supply chains.

---

## 1. Explicit Exclusions & Non-Surveillance Safeguards

The application explicitly **DOES NOT** collect, store, or process any of the following sensitive data types:

- ❌ **NO Farmer Identity**: No farmer names, usernames, or government ID numbers (Aadhaar, PAN, voter ID) are requested or stored.
- ❌ **NO Phone Numbers**: Contact phone numbers or mobile device IMEI identifiers are completely excluded.
- ❌ **NO Exact Personal Addresses**: No precise street addresses, plot numbers, or residential coordinates are requested.
- ❌ **NO Continuous GPS Tracking**: The app does **not** access device location APIs or track real-time farmer movement.
- ❌ **NO Farmer Ranking / Performance Scoring**: Data is never used to rank farmers, grade supplier competence, or generate performance leaderboards.
- ❌ **NO Punitive Scoring / Procurement Penalties**: Observations are strictly diagnostic tools to assist crop health, never mechanisms to penalize suppliers or trigger financial deductions.

---

## 2. Actual Data Fields Collected

To verify full transparency, the following table lists **every data field** collected by the application in the SQLite database (`app/models.py`):

| Data Field Name | Table | Purpose & Privacy Justification | Identifiable? |
|---|---|---|---|
| `crop` | `observations` | Crop species (Tomato, Potato, Chili) for ML model selection | **NO** |
| `symptom` | `observations` | Observed visual symptom (Leaf Spot, Blight, etc.) for triage | **NO** |
| `crop_stage` | `observations` | Growth stage (Vegetative, Flowering, etc.) for context | **NO** |
| `location_region` | `observations` | Broad administrative zone (e.g., North Zone) for regional disease tracking | **NO** (General region only) |
| `image_path` | `observations` | Relative file path to uploaded crop leaf photo | **NO** (Crop leaves only) |
| `observation_notes` | `observations` | Optional text notes regarding crop symptoms | **NO** |
| `observation_timestamp` | `observations` | UTC timestamp to compute Time-to-Review SLA metrics | **NO** |
| `model_prediction` | `observations` | ML screening classification result | **NO** |
| `confidence` | `observations` | ML screening confidence percentage (`0.0` to `1.0`) | **NO** |
| `status` | `observations` | Workflow state ('Initial screening result', 'Needs expert review') | **NO** |
| `expert_label` | `expert_reviews` | Expert confirmed or corrected disease label | **NO** |
| `expert_status` | `expert_reviews` | Validation decision ('Confirmed', 'Corrected', 'Uncertain') | **NO** |
| `expert_comment` | `expert_reviews` | Advisory treatment comments from agricultural expert | **NO** |
| `review_timestamp` | `expert_reviews` | UTC timestamp when expert submitted review | **NO** |
| `time_to_review_seconds` | `expert_reviews` | Elapsed time in seconds between submission and expert review | **NO** |

---

## 3. Non-Identifiable Image Policy

- All submitted crop images are verified by automated quality checks.
- Photos must focus exclusively on crop leaves, stems, or fruits.
- Photos containing human faces or identifiable personal property are excluded from dataset training and public presentation.

---

## 4. Ethical Model Disclaimer

- Machine learning predictions are explicitly labeled:
  > **“This result is an initial screening/triage result, not a definitive expert diagnosis.”**
- Machine learning predictions are never presented as authoritative truth, ensuring human agricultural experts retain final decision authority on all escalated cases.
