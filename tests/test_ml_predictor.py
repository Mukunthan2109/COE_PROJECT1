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

def test_predict_supported_category(sample_leaf_image):
    result = predict_crop_disease(sample_leaf_image, crop="Tomato", symptom="Leaf Spot")
    assert result['is_supported'] is True
    assert 'prediction' in result
    assert isinstance(result['confidence'], float)
    assert len(result['explainability']) > 0

def test_predict_unsupported_category_edge_case(sample_leaf_image):
    """
    Edge Case 3: Crop or disease category outside the supported dataset
    Expected: System flags unsupported category, returns low confidence, and prompts escalation.
    """
    result = predict_crop_disease(sample_leaf_image, crop="DragonFruit", symptom="Unknown Blister")
    assert result['is_supported'] is False
    assert result['prediction'] == 'Unsupported / Unknown Category'
    assert result['confidence'] < 0.70
    assert result['warning'] is not None
