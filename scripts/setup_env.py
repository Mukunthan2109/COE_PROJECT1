import os
import sys
import shutil
from datetime import datetime, timedelta

# Add parent dir to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.models import db, User, Observation, ExpertReview, BatchProcurement, OutbreakAlert, DatasetMetadata
from ml.generate_dataset import main as generate_dataset
from ml.train import train_model

def setup_environment():
    print("==================================================")
    print("   SETTING UP 100% FULL PROJECT ENVIRONMENT      ")
    print("==================================================")

    # 1. Generate Expanded Dataset (9 crops, 18 categories)
    generate_dataset()

    # 2. Train Model
    train_model()

    # 3. Initialize Flask DB and seed default users & records
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed Users
        if User.query.count() == 0:
            print("Seeding default system users (Farmer, Expert, QA Manager)...")
            farmer_user = User(username="farmer1", email="farmer1@agri.org", role="farmer", region="North Zone")
            farmer_user.set_password("password123")

            expert_user = User(username="expert1", email="expert1@agri.org", role="expert", region="South Zone")
            expert_user.set_password("password123")

            qa_user = User(username="qamanager1", email="qa1@foodproc.com", role="qa_manager", region="Central Region")
            qa_user.set_password("password123")

            db.session.add_all([farmer_user, expert_user, qa_user])
            db.session.commit()
            print("Seeded default system users (farmer1, expert1, qamanager1)!")

    print("\n100% Full Environment Setup Complete (Zero seeded runtime observations)!")

if __name__ == '__main__':
    setup_environment()
