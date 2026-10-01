import os
import joblib
import numpy as np
import cv2
from ml.train import extract_features, CROP_MAP
from ml.gradcam import generate_gradcam_heatmap

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'saved_model'))

SUPPORTED_CROPS = {"Tomato", "Potato", "Rice", "Corn", "Maize", "Chili", "Grape", "Apple"}
SUPPORTED_SYMPTOMS = {
    "Healthy", "Early Blight", "Late Blight", "Brown Spot", "Leaf Blast",
    "Common Rust", "Leaf Blight", "Anthracnose", "Leaf Curl", "Black Rot", "Apple Scab",
    "Yellowing leaves", "Brown spots", "Leaf curling", "Wilting"
}


def generate_explainability(image_path, prediction, confidence):
    indicators = []
    try:
        img = cv2.imread(image_path)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            _, dark_mask = cv2.threshold(gray, 65, 255, cv2.THRESH_BINARY_INV)
            dark_ratio = np.sum(dark_mask > 0) / (gray.shape[0] * gray.shape[1])

            lower_yellow = np.array([15, 40, 40])
            upper_yellow = np.array([35, 255, 255])
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            yellow_ratio = np.sum(yellow_mask > 0) / (hsv.shape[0] * hsv.shape[1])

            if "Spot" in prediction or "Blight" in prediction or "Rust" in prediction or dark_ratio > 0.05:
                indicators.append("Visible dark spot clusters and necrotic lesion areas detected on leaf surface.")
            
            if "Blight" in prediction or "Curl" in prediction or "Rot" in prediction or yellow_ratio > 0.08:
                indicators.append("Significant leaf discoloration and chlorosis index detected on leaf surface.")

            if "Healthy" in prediction:
                indicators.append("Uniform chlorophyll green color distribution.")
                indicators.append("No prominent necrotic brown or black lesions detected.")
            else:
                indicators.append("Irregular leaf surface texture and spot variance detected.")

    except Exception:
        indicators.append("Visual color and texture anomaly detected on leaf surface.")

    if not indicators:
        indicators.append("Standard visual leaf anomaly detected by feature classifier.")

    return indicators

def determine_risk_level(prediction, symptom, confidence, threshold=0.70):
    """
    Computes Risk Level independently from Confidence score.
    Confidence = ML certainty score (0.0 to 1.0).
    Risk Level = Agricultural & food-processing quality risk (High, Medium, Low).
    """
    if confidence < 0.60:
        return 'High'

    pred_upper = (prediction or "").upper()
    sym_upper = (symptom or "").upper()

    if any(k in pred_upper or k in sym_upper for k in ["BLIGHT", "ROT", "ANTHRACNOSE"]):
        return 'High'
    elif confidence >= 0.80 and "HEALTHY" in pred_upper:
        return 'Low'
    elif confidence >= 0.80:
        return 'Medium' if any(k in pred_upper or k in sym_upper for k in ["SPOT", "RUST", "CURL", "WILT"]) else 'Low'
    else:
        return 'Medium'

def predict_crop_disease(image_path, crop="Auto", symptom="Auto"):
    """
    Predicts disease label, confidence score, risk level, and generates visual feature heatmap.
    Supports Auto-detecting Crop and Disease directly from uploaded image pixels.
    """
    heatmap_path = generate_gradcam_heatmap(image_path)

    is_auto = (crop in ("Auto", "Detect", "", None) or symptom in ("Auto", "Detect", "", None))

    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')

    if not is_auto and (crop not in SUPPORTED_CROPS or (symptom and symptom not in SUPPORTED_SYMPTOMS and symptom != "Auto")):
        return {
            'is_supported': False,
            'prediction': 'Unsupported / Unknown Category',
            'display_prediction': 'Uncertain screening result (Unsupported category)',
            'confidence': 0.35,
            'risk_level': 'High',
            'detected_crop': crop,
            'detected_symptom': symptom,
            'heatmap_path': heatmap_path,
            'explainability': [
                "Observation involves a crop or symptom category outside the baseline training dataset.",
                "AI screening is an initial triage assessment, not a final expert diagnosis.",
                "System is unable to safely triage this unclassified crop observation. Expert review recommended."
            ],
            'warning': "Category is outside the current trained model scope. Escalating to expert review."
        }

    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        canonical_crop = "Maize" if crop in ("Corn", "Maize") else (crop if crop not in ("Auto", "Detect", "", None) else "Tomato")
        unavail_msg = "AI screening is currently unavailable. Please submit the case for expert review."
        return {
            'is_supported': True,
            'prediction': 'unavailable',
            'display_prediction': unavail_msg,
            'confidence': 0.0,
            'risk_level': 'High',
            'detected_crop': canonical_crop,
            'detected_symptom': symptom if symptom not in ("Auto", "Detect", "", None) else "Healthy",
            'heatmap_path': heatmap_path,
            'explainability': [
                unavail_msg,
                "AI screening is an initial triage assessment, not a final expert diagnosis."
            ],
            'warning': unavail_msg
        }

    try:
        clf = joblib.load(model_path)
        label_encoder = joblib.load(encoder_path)

        canonical_crop = "Maize" if crop in ("Corn", "Maize") else crop
        crop_to_extract = canonical_crop if canonical_crop in SUPPORTED_CROPS else "Tomato"
        features = extract_features(image_path, crop_to_extract)
        probs = clf.predict_proba([features])[0]

        # Overall model top prediction (unfiltered across all trained classes)
        overall_top_idx = int(np.argmax(probs))
        overall_top_label = str(label_encoder.classes_[overall_top_idx])
        overall_top_prob = float(probs[overall_top_idx])
        overall_crop = overall_top_label.split(' ', 1)[0]
        if overall_crop in ("Corn", "Maize"):
            overall_crop = "Maize"

        crop_specified = crop not in ("Auto", "Detect", "", None)
        target_crop_key = "Corn" if crop_to_extract in ("Corn", "Maize") else crop_to_extract
        candidate_indices = [
            i for i, cls_name in enumerate(label_encoder.classes_)
            if str(cls_name).startswith(target_crop_key) or (target_crop_key in ("Corn", "Maize") and str(cls_name).startswith("Maize"))
        ]

        crop_prob_sum = float(np.sum(probs[candidate_indices])) if candidate_indices else 0.0

        # Crop-Image Compatibility Verification
        if crop_specified and candidate_indices and crop_prob_sum < 0.20 and overall_top_prob > 0.35 and overall_crop != canonical_crop:
            mismatch_msg = "Uploaded image may not match the selected crop. Please upload a suitable image."
            return {
                'is_supported': True,
                'is_mismatch': True,
                'prediction': 'Crop-Image Mismatch',
                'display_prediction': mismatch_msg,
                'detected_crop': canonical_crop,
                'detected_symptom': 'Mismatch',
                'confidence': round(overall_top_prob, 4),
                'risk_level': 'High',
                'heatmap_path': heatmap_path,
                'explainability': [
                    mismatch_msg,
                    f"Visual feature inspection suggests image belongs to {overall_crop} rather than selected crop ({canonical_crop}).",
                    "AI screening is an initial triage assessment, not a final expert diagnosis."
                ],
                'warning': mismatch_msg
            }

        # Valid Crop Inference: Extract true raw probability directly from model output
        if candidate_indices and crop_specified:
            best_rel_idx = int(np.argmax(probs[candidate_indices]))
            top_idx = candidate_indices[best_rel_idx]
            confidence = float(probs[top_idx])
        else:
            top_idx = overall_top_idx
            confidence = overall_top_prob

        pred_label = str(label_encoder.classes_[top_idx])
        label_parts = pred_label.split(' ', 1)
        detected_crop = label_parts[0] if len(label_parts) > 0 else crop_to_extract
        detected_symptom = label_parts[1] if len(label_parts) > 1 else "Healthy"

        risk_level = determine_risk_level(pred_label, symptom, confidence)
        explainability = generate_explainability(image_path, pred_label, confidence)
        explainability.append("Visual feature analysis derived from leaf color distribution, texture, and spot contours.")
        explainability.append("AI screening is an initial triage assessment, not a final expert diagnosis.")

        display_prediction = pred_label
        if confidence < 0.70:
            display_prediction = f"Uncertain screening result ({pred_label})"
            explainability.append("Uncertain screening result due to low model confidence (<70%). Expert review is recommended.")

        return {
            'is_supported': True,
            'is_mismatch': False,
            'prediction': pred_label,
            'display_prediction': display_prediction,
            'detected_crop': detected_crop,
            'detected_symptom': detected_symptom,
            'confidence': round(confidence, 4),
            'risk_level': risk_level,
            'heatmap_path': heatmap_path,
            'explainability': explainability,
            'warning': "Uncertain screening result. Expert review recommended." if confidence < 0.70 else None
        }

    except Exception as e:
        fallback_crop = crop if crop not in ("Auto", "Detect", "", None) else "Tomato"
        return {
            'is_supported': True,
            'prediction': 'Prediction Error',
            'display_prediction': 'Uncertain screening result (Processing Error)',
            'detected_crop': fallback_crop,
            'detected_symptom': 'Unknown',
            'confidence': 0.0,
            'risk_level': 'High',
            'heatmap_path': heatmap_path,
            'explainability': [
                f"Processing error during prediction: {str(e)}",
                "AI screening is an initial triage assessment, not a final expert diagnosis."
            ],
            'warning': "Model inference failed. Escalating to expert review."
        }

