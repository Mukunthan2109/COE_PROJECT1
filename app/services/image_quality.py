import cv2
import numpy as np
import hashlib
from PIL import Image

def compute_image_hash(image_path):
    """
    Computes SHA-256 hash of image binary data to prevent duplicate image submissions.
    """
    hasher = hashlib.sha256()
    with open(image_path, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def evaluate_image_quality(image_path, min_width=100, min_height=100, blur_threshold=40.0,
                           min_brightness=30, max_brightness=225):
    """
    Performs basic automated image quality checks:
    1. Readability & Dimensions
    2. Darkness / Underexposed check
    3. Brightness / Overexposed check
    4. Blur / Sharpness check (Laplacian variance)
    
    Returns:
        tuple: (is_valid: bool, message: str, details: dict)
    """
    try:
        # Load with PIL first to verify readability and corrupt header check
        with Image.open(image_path) as pil_img:
            pil_img.verify()
            width, height = pil_img.size
            
        if width < min_width or height < min_height:
            return (False, "Image quality is insufficient. Resolution is too low for triage. Please capture a larger crop image.", {
                'reason': 'resolution_too_low',
                'width': width,
                'height': height
            })

        # Load with OpenCV for numeric quality checks
        cv_img = cv2.imread(image_path)
        if cv_img is None:
            return (False, "Image quality is insufficient. File is unreadable or corrupted.", {
                'reason': 'unreadable_file'
            })

        # Convert to grayscale
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

        # Brightness check
        mean_brightness = np.mean(gray)
        if mean_brightness < min_brightness:
            return (False, "Image quality is insufficient. Image is extremely dark/underexposed. Please capture with better lighting.", {
                'reason': 'too_dark',
                'brightness': round(float(mean_brightness), 2)
            })

        if mean_brightness > max_brightness:
            return (False, "Image quality is insufficient. Image is extremely bright/overexposed. Please avoid direct harsh light.", {
                'reason': 'too_bright',
                'brightness': round(float(mean_brightness), 2)
            })

        # Blur check (Laplacian Variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < blur_threshold:
            return (False, "Image quality is too low for reliable AI screening. Please upload a clearer crop image.", {
                'reason': 'blurry',
                'blur_score': round(float(laplacian_var), 2)
            })

        return (True, "Image quality check passed.", {
            'reason': 'valid',
            'width': width,
            'height': height,
            'brightness': round(float(mean_brightness), 2),
            'blur_score': round(float(laplacian_var), 2)
        })

    except Exception as e:
        return (False, f"Image quality is insufficient. File is corrupted or unreadable: {str(e)}", {
            'reason': 'processing_error',
            'error': str(e)
        })

