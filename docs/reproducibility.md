# AgriShield System Reproducibility & Replication Guide

## 1. Clean Clone Replication Protocol

AgriShield is designed for 100% independent replication from a fresh machine setup without external paid APIs or uncommitted local dependencies.

```bash
# Step 1: Clone Repository
git clone https://github.com/Mukunthan2109/COE_PROJECT1.git
cd COE_PROJECT1

# Step 2: Create & Activate Virtual Environment
py -3 -m venv .venv
.venv\Scripts\activate

# Step 3: Install Dependencies
pip install -r requirements.txt

# Step 4: Setup Environment & Database Schema
py -3 scripts/setup_env.py

# Step 5: Audit Dataset & Verify Zero Data Leakage
py -3 scripts/check_dataset.py

# Step 6: Seed Controlled Demo Data (Optional)
py -3 scripts/seed_demo.py

# Step 7: Run Pre-Trained ML Model Inference & Evaluation
py -3 ml/evaluate.py

# Step 8: Execute Automated Pytest Test Suite
py -3 -m pytest tests/ -v

# Step 9: Launch Application Server
py -3 run.py
```

---

## 2. Included Reproducible Model Artifacts

Pre-trained model artifacts are stored in `ml/saved_model/` and committed to the repository:
- `model.pkl`: Random Forest Classifier trained on 37-dim visual feature vectors.
- `label_encoder.pkl`: Label encoder covering all 17 crop-disease target classes.
- `metrics.json`: Evaluated accuracy, precision, recall, and F1-scores.
- `model_metadata.json`: Model version, training seed (`42`), split distribution, Python version, and library versions.

---

## 3. Automated Continuous Integration (CI)

GitHub Actions workflow [`.github/workflows/tests.yml`](file:///c:/Users/mukun/OneDrive/Desktop/ceo/.github/workflows/tests.yml) automatically runs `pytest tests/ -v` on Python 3.11 for every push and pull request.
