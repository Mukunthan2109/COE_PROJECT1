import os
import pytest
import numpy as np
from PIL import Image
from app.services.image_quality import evaluate_image_quality

@pytest.fixture
def temp_images(tmp_path):
    # Valid image
    valid_path = str(tmp_path / "valid.jpg")
    img_arr = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(valid_path)

    # Low resolution image
    lowres_path = str(tmp_path / "lowres.jpg")
    Image.fromarray(img_arr[:50, :50]).save(lowres_path)

    # Extremely dark image
    dark_path = str(tmp_path / "dark.jpg")
    dark_arr = np.random.randint(0, 15, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(dark_arr).save(dark_path)

    # Extremely bright image
    bright_path = str(tmp_path / "bright.jpg")
    bright_arr = np.random.randint(240, 255, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(bright_arr).save(bright_path)

    # Uniform/Blurry image (zero variance)
    blur_path = str(tmp_path / "blur.jpg")
    blur_arr = np.ones((200, 200, 3), dtype=np.uint8) * 128
    Image.fromarray(blur_arr).save(blur_path)

    return {
        'valid': valid_path,
        'lowres': lowres_path,
        'dark': dark_path,
        'bright': bright_path,
        'blur': blur_path
    }

def test_valid_image_quality(temp_images):
    is_valid, msg, details = evaluate_image_quality(temp_images['valid'])
    assert is_valid is True
    assert details['reason'] == 'valid'

def test_low_resolution_rejection(temp_images):
    is_valid, msg, details = evaluate_image_quality(temp_images['lowres'])
    assert is_valid is False
    assert details['reason'] == 'resolution_too_low'
    assert "insufficient" in msg.lower()

def test_dark_image_rejection(temp_images):
    is_valid, msg, details = evaluate_image_quality(temp_images['dark'])
    assert is_valid is False
    assert details['reason'] == 'too_dark'

def test_bright_image_rejection(temp_images):
    is_valid, msg, details = evaluate_image_quality(temp_images['bright'])
    assert is_valid is False
    assert details['reason'] == 'too_bright'

def test_blurry_image_rejection(temp_images):
    is_valid, msg, details = evaluate_image_quality(temp_images['blur'])
    assert is_valid is False
    assert details['reason'] == 'blurry'

def test_corrupted_image_rejection(tmp_path):
    corrupt_path = str(tmp_path / "corrupt.jpg")
    with open(corrupt_path, "wb") as f:
        f.write(b"NOT_AN_IMAGE_HEADER_GARBAGE")
    is_valid, msg, details = evaluate_image_quality(corrupt_path)
    assert is_valid is False
    assert details['reason'] in ('processing_error', 'unreadable_file')

