import os
import csv
import json
import joblib
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'dataset'))
METADATA_CSV = os.path.join(DATASET_DIR, 'metadata.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'saved_model')

CROP_MAP = {
    "Tomato": 0, "Potato": 1, "Chili": 2, "Corn": 3,
    "Rice": 4, "Wheat": 5, "Apple": 6, "Grape": 7, "Cotton": 8
}

def extract_features(image_path, crop_name=None):
    """
    Extracts interpretable visual features from crop leaf images:
    - HSV Color Histograms (24 features)
    - RGB & HSV Stats (9 features)
    - Canny Edge density (1 feature)
    - Dark spot area ratio (1 feature)
    Note: Label and crop_code leakage removed for strict ML evaluation.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
        
    img = cv2.resize(img, (128, 128))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h_hist = cv2.calcHist([hsv], [0], None, [8], [0, 180]).flatten()
    s_hist = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()
    v_hist = cv2.calcHist([hsv], [2], None, [8], [0, 256]).flatten()
    
    h_hist /= (np.sum(h_hist) + 1e-6)
    s_hist /= (np.sum(s_hist) + 1e-6)
    v_hist /= (np.sum(v_hist) + 1e-6)

    mean_rgb = np.mean(img, axis=(0, 1))
    std_rgb = np.std(img, axis=(0, 1))
    mean_hsv = np.mean(hsv, axis=(0, 1))
    
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (128 * 128)

    _, dark_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
    dark_spot_ratio = np.sum(dark_mask > 0) / (128 * 128)

    features = np.hstack([
        h_hist, s_hist, v_hist,
        mean_rgb, std_rgb, mean_hsv,
        [edge_density, dark_spot_ratio]
    ])
    return features

def train_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    if not os.path.exists(METADATA_CSV):
        raise FileNotFoundError(f"Metadata CSV not found at {METADATA_CSV}. Run generate_dataset.py first.")

    X = []
    y = []
    
    print("Loading dataset and extracting features across 9 crops...")
    with open(METADATA_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_rel_path = row['image_path']
            crop = row['crop']
            label = row['disease_label']
            img_full_path = os.path.abspath(os.path.join(BASE_DIR, '..', img_rel_path))
            
            try:
                feat = extract_features(img_full_path, crop)
                X.append(feat)
                y.append(label)
            except Exception as e:
                print(f"Skipping {img_full_path}: {e}")

    X = np.array(X)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print(f"Extracted {len(X)} samples with {X.shape[1]} features across {len(label_encoder.classes_)} classes.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
    )

    clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'f1_score': round(float(f1), 4),
        'classes': list(label_encoder.classes_),
        'confusion_matrix': cm,
        'train_samples': len(X_train),
        'test_samples': len(X_test)
    }

    print("\n--- ML Baseline Evaluation Report ---")
    print(f"Accuracy:  {metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {metrics['precision'] * 100:.2f}%")
    print(f"Recall:    {metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:  {metrics['f1_score'] * 100:.2f}%")

    joblib.dump(clf, os.path.join(MODEL_DIR, 'model.pkl'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.pkl'))
    with open(os.path.join(MODEL_DIR, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved model & artifacts to {MODEL_DIR}")
    return metrics

if __name__ == '__main__':
    train_model()
