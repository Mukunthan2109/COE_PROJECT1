# AgriShield Deployment & Production Setup Guide

## 1. Local Environment Execution

```bash
# 1. Activate Virtual Environment
py -3 -m venv .venv
.venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Environment & Database Setup
py -3 scripts/setup_env.py

# 4. Seed Demo Data (Optional)
py -3 scripts/seed_demo.py

# 5. Launch Application
py -3 run.py
```
Open browser at: **`http://127.0.0.1:5000`**

---

## 2. Production Environment Configuration

For production deployment on Linux / WSGI environments (*e.g., Render, Railway, AWS EC2*):

### Environment Variables
Set the following environment variables:
- `FLASK_ENV=production`
- `SECRET_KEY=your_secure_random_secret_key_here`
- `DATABASE_URL=sqlite:///app/farmer_app.db` (or PostgreSQL URI)
- `PORT=5000`

### WSGI Server Execution (Gunicorn)
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 run:app
```

---

## 3. Automated Test Suite Execution
```bash
py -3 -m pytest tests/ -v
```
