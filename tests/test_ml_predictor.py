import os
import pytest
import numpy as np
from PIL import Image
from app.services.predictor import predict_crop_disease

@pytest.fixture
def sample_leaf_image(tmp_path):
    img_path = str(tmp_path / "test_leaf.jpg")
    img_arr = np.random.randint(40, 180, (256, 256, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(img_path)
    return img_path

@pytest.mark.parametrize("crop_name", ["Tomato", "Potato", "Rice", "Maize", "Chili", "Grape", "Apple"])
def test_predict_supported_crops(sample_leaf_image, crop_name):
    """
    Tests that all 7 supported crops (Tomato, Potato, Rice, Maize, Chili, Grape, Apple)
    are recognized as supported and generate valid ML prediction & confidence outputs.
    """
    result = predict_crop_disease(sample_leaf_image, crop=crop_name, symptom="Auto")
    assert result['is_supported'] is True
    assert 'prediction' in result
    assert isinstance(result['confidence'], float)
    assert len(result['explainability']) > 0

def test_predict_unsupported_category_edge_case(sample_leaf_image):
    """
    Edge Case: Crop outside the 7 supported crops
    Expected: System flags unsupported category, returns low confidence, and prompts escalation.
    """
    result = predict_crop_disease(sample_leaf_image, crop="DragonFruit", symptom="Unknown Blister")
    assert result['is_supported'] is False
    assert result['prediction'] == 'Unsupported / Unknown Category'
    assert result['confidence'] < 0.70
    assert result['warning'] is not None

def test_predict_model_missing_fallback(sample_leaf_image, monkeypatch):
    import app.services.predictor as pred_module
    monkeypatch.setattr(pred_module, 'MODEL_DIR', '/non_existent_model_dir_xyz')
    result = predict_crop_disease(sample_leaf_image, crop="Tomato", symptom="Healthy")
    assert result['prediction'] in ('unavailable', 'Model unavailable')
    assert result['confidence'] == 0.0
    assert result['risk_level'] == 'High'
    assert 'unavailable' in result['warning'].lower()

