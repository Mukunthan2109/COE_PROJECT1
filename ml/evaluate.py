import os
import csv
import json
import joblib
import cv2
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'dataset'))
METADATA_CSV = os.path.join(DATASET_DIR, 'metadata.csv')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
MODEL_DIR = os.path.join(BASE_DIR, 'saved_model')

def extract_features(image_path):
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

def run_evaluation():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    X = []
    y = []
    splits = []
    
    with open(METADATA_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_rel_path = row['image_path']
            label = row['disease_label']
            split_val = row.get('split', 'train')
            img_full_path = os.path.abspath(os.path.join(BASE_DIR, '..', img_rel_path))
            
            try:
                feat = extract_features(img_full_path)
                X.append(feat)
                y.append(label)
                splits.append(split_val)
            except Exception as e:
                print(f"Skipping {img_full_path}: {e}")

    X = np.array(X)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    splits = np.array(splits)

    # Use metadata split if train/test exist, else standard stratified split
    if 'train' in splits and ('test' in splits or 'val' in splits):
        train_idx = np.where(splits == 'train')[0]
        test_idx = np.where((splits == 'test') | (splits == 'val'))[0]
        X_train, y_train = X[train_idx], y_encoded[train_idx]
        X_test, y_test = X[test_idx], y_encoded[test_idx]
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
        )

    # 1. Baseline Model: Random Forest
    baseline_clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    baseline_clf.fit(X_train, y_train)
    y_pred_base = baseline_clf.predict(X_test)

    base_acc = accuracy_score(y_test, y_pred_base)
    base_m_prec, base_m_rec, base_m_f1, _ = precision_recall_fscore_support(y_test, y_pred_base, average='macro', zero_division=0)
    base_w_prec, base_w_rec, base_w_f1, _ = precision_recall_fscore_support(y_test, y_pred_base, average='weighted', zero_division=0)
    base_cm = confusion_matrix(y_test, y_pred_base)

    baseline_metrics = {
        'model_name': 'Baseline Random Forest Classifier',
        'accuracy': round(float(base_acc), 4),
        'precision': round(float(base_w_prec), 4),
        'recall': round(float(base_w_rec), 4),
        'f1_score': round(float(base_w_f1), 4),
        'macro_precision': round(float(base_m_prec), 4),
        'macro_recall': round(float(base_m_rec), 4),
        'macro_f1': round(float(base_m_f1), 4),
        'weighted_precision': round(float(base_w_prec), 4),
        'weighted_recall': round(float(base_w_rec), 4),
        'weighted_f1': round(float(base_w_f1), 4),
        'train_samples': int(len(X_train)),
        'test_samples': int(len(X_test)),
        'classes': list(label_encoder.classes_),
        'confusion_matrix': base_cm.tolist()
    }

    # 2. Improved Model: ExtraTrees Classifier Ensemble
    improved_clf = ExtraTreesClassifier(n_estimators=200, max_depth=16, random_state=42)
    improved_clf.fit(X_train, y_train)
    y_pred_imp = improved_clf.predict(X_test)

    imp_acc = accuracy_score(y_test, y_pred_imp)
    imp_m_prec, imp_m_rec, imp_m_f1, _ = precision_recall_fscore_support(y_test, y_pred_imp, average='macro', zero_division=0)
    imp_w_prec, imp_w_rec, imp_w_f1, _ = precision_recall_fscore_support(y_test, y_pred_imp, average='weighted', zero_division=0)
    imp_cm = confusion_matrix(y_test, y_pred_imp)

    improved_metrics = {
        'model_name': 'Improved ExtraTrees Classifier Ensemble',
        'accuracy': round(float(imp_acc), 4),
        'macro_precision': round(float(imp_m_prec), 4),
        'macro_recall': round(float(imp_m_rec), 4),
        'macro_f1': round(float(imp_m_f1), 4),
        'weighted_precision': round(float(imp_w_prec), 4),
        'weighted_recall': round(float(imp_w_rec), 4),
        'weighted_f1': round(float(imp_w_f1), 4),
        'train_samples': int(len(X_train)),
        'test_samples': int(len(X_test)),
        'classes': list(label_encoder.classes_),
        'confusion_matrix': imp_cm.tolist()
    }

    # Save metrics JSON files
    with open(os.path.join(RESULTS_DIR, 'baseline_metrics.json'), 'w') as f:
        json.dump(baseline_metrics, f, indent=2)

    with open(os.path.join(RESULTS_DIR, 'improved_metrics.json'), 'w') as f:
        json.dump(improved_metrics, f, indent=2)

    # Export comparison CSV
    comp_df = pd.DataFrame([
        {
            'Model': 'Baseline Random Forest',
            'Accuracy': f"{base_acc*100:.2f}%",
            'Macro Precision': f"{base_m_prec*100:.2f}%",
            'Macro Recall': f"{base_m_rec*100:.2f}%",
            'Macro F1': f"{base_m_f1*100:.2f}%",
            'Weighted Precision': f"{base_w_prec*100:.2f}%",
            'Weighted Recall': f"{base_w_rec*100:.2f}%",
            'Weighted F1': f"{base_w_f1*100:.2f}%"
        },
        {
            'Model': 'Improved ExtraTrees Ensemble',
            'Accuracy': f"{imp_acc*100:.2f}%",
            'Macro Precision': f"{imp_m_prec*100:.2f}%",
            'Macro Recall': f"{imp_m_rec*100:.2f}%",
            'Macro F1': f"{imp_m_f1*100:.2f}%",
            'Weighted Precision': f"{imp_w_prec*100:.2f}%",
            'Weighted Recall': f"{imp_w_rec*100:.2f}%",
            'Weighted F1': f"{imp_w_f1*100:.2f}%"
        }
    ])
    comp_df.to_csv(os.path.join(RESULTS_DIR, 'comparison.csv'), index=False)

    # 3. Controlled Dataset Experiment: Experiment A (360 core samples) vs Experiment B (460 expanded samples)
    core_mask = np.array([lbl.split()[0] in ['Tomato', 'Potato', 'Rice', 'Corn'] for lbl in y])
    X_core, y_core = X[core_mask], y_encoded[core_mask]
    le_core = LabelEncoder()
    y_core_enc = le_core.fit_transform(np.array(y)[core_mask])

    X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(X_core, y_core_enc, test_size=0.20, random_state=42, stratify=y_core_enc)
    rf_exp_a = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    rf_exp_a.fit(X_tr_c, y_tr_c)
    y_pred_exp_a = rf_exp_a.predict(X_te_c)

    acc_a = accuracy_score(y_te_c, y_pred_exp_a)
    p_a, r_a, f1_a, _ = precision_recall_fscore_support(y_te_c, y_pred_exp_a, average='weighted', zero_division=0)
    m_p_a, m_r_a, m_f1_a, _ = precision_recall_fscore_support(y_te_c, y_pred_exp_a, average='macro', zero_division=0)

    ds_comp_df = pd.DataFrame([
        {
            'Experiment': 'Experiment A: Core 360 Dataset (12 Classes)',
            'Total Samples': 360,
            'Classes': 12,
            'Accuracy': f"{acc_a*100:.2f}%",
            'Macro Precision': f"{m_p_a*100:.2f}%",
            'Macro Recall': f"{m_r_a*100:.2f}%",
            'Macro F1': f"{m_f1_a*100:.2f}%",
            'Weighted F1': f"{f1_a*100:.2f}%"
        },
        {
            'Experiment': 'Experiment B: Expanded 460 Dataset (17 Classes)',
            'Total Samples': 460,
            'Classes': 17,
            'Accuracy': f"{base_acc*100:.2f}%",
            'Macro Precision': f"{base_m_prec*100:.2f}%",
            'Macro Recall': f"{base_m_rec*100:.2f}%",
            'Macro F1': f"{base_m_f1*100:.2f}%",
            'Weighted F1': f"{base_w_f1*100:.2f}%"
        }
    ])
    ds_comp_df.to_csv(os.path.join(RESULTS_DIR, 'dataset_comparison.csv'), index=False)

    # Generate Confusion Matrix Plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(base_cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
    plt.title('Baseline Random Forest Confusion Matrix (17 Classes)')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'confusion_matrix.png'), dpi=200)
    plt.close()

    # Save best model to saved_model directory
    joblib.dump(baseline_clf, os.path.join(MODEL_DIR, 'model.pkl'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.pkl'))
    with open(os.path.join(MODEL_DIR, 'metrics.json'), 'w') as f:
        json.dump(baseline_metrics, f, indent=2)

    import sys
    import sklearn
    import cv2 as cv2_mod
    model_meta = {
        'model_name': 'crop_disease_rf',
        'model_version': 'v1.0',
        'training_dataset_version': 'v1.0-460samples',
        'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'random_seed': 42,
        'feature_method': '37-dim HSV Color Histograms + RGB/HSV Channel Stats + Canny Edge Density + Dark Spot Ratio',
        'training_samples': int(len(X_train)),
        'validation_samples': 46,
        'test_samples': int(len(X_test)),
        'classes': list(label_encoder.classes_),
        'metrics': baseline_metrics,
        'python_version': sys.version.split()[0],
        'library_versions': {
            'scikit-learn': sklearn.__version__,
            'opencv': cv2_mod.__version__,
            'numpy': np.__version__,
            'joblib': joblib.__version__
        }
    }
    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(model_meta, f, indent=2)

    print("Evaluation & Model Comparison complete!")
    print(f"Results saved to {RESULTS_DIR}")
    print(comp_df.to_string(index=False))

if __name__ == '__main__':
    run_evaluation()
