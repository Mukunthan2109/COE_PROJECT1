import os
import sys
import joblib
import numpy as np
from ml.train import extract_features

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'saved_model'))

def predict_single_image(image_path, crop_name="Tomato"):
    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')

    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        return {
            'error': f"Model files not found in {MODEL_DIR}. Please run `python ml/train.py` first."
        }

    clf = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)

    try:
        features = extract_features(image_path, crop_name)
        probs = clf.predict_proba([features])[0]
        top_idx = int(np.argmax(probs))
        prediction = str(label_encoder.classes_[top_idx])
        confidence = float(probs[top_idx])

        return {
            'crop': crop_name,
            'prediction': prediction,
            'confidence': confidence,
            'all_probabilities': {
                cls: round(float(p), 4) for cls, p in zip(label_encoder.classes_, probs)
            }
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ml/predict.py <path_to_image> [crop_name]")
        sys.exit(1)
        
    img_p = sys.argv[1]
    crp = sys.argv[2] if len(sys.argv) > 2 else "Tomato"
    res = predict_single_image(img_p, crp)
    print("Prediction Result:", res)
