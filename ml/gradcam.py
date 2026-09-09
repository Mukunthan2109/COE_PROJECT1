import os
import cv2
import numpy as np

HEATMAP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'heatmaps'))

def generate_gradcam_heatmap(image_path, output_filename=None):
    """
    Generates a Grad-CAM style region heatmap highlighting potential disease spots
    and necrotic tissue on crop leaf images.
    
    Returns:
        str: Relative path to saved heatmap image ('heatmaps/filename.jpg')
    """
    os.makedirs(HEATMAP_DIR, exist_ok=True)
    if not output_filename:
        output_filename = f"heatmap_{os.path.basename(image_path)}"

    output_abs_path = os.path.join(HEATMAP_DIR, output_filename)
    relative_path = f"heatmaps/{output_filename}"

    try:
        img = cv2.imread(image_path)
        if img is None:
            return None

        h, w, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Detect dark spots & yellow halos
        _, dark_mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
        
        lower_yellow = np.array([15, 40, 40])
        upper_yellow = np.array([35, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        combined_mask = cv2.bitwise_or(dark_mask, yellow_mask)

        # Apply Gaussian Blur to create smooth heatmap intensity map
        heatmap_float = cv2.GaussianBlur(combined_mask.astype(np.float32), (31, 31), 0)
        norm_heatmap = cv2.normalize(heatmap_float, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Apply Jet ColorMap
        color_heatmap = cv2.applyColorMap(norm_heatmap, cv2.COLORMAP_JET)

        # Blend heatmap with original leaf image (60% original, 40% heatmap)
        blended = cv2.addWeighted(img, 0.65, color_heatmap, 0.35, 0)

        # Draw bounding boxes around top 3 disease contours
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

        for cnt in contours:
            if cv2.contourArea(cnt) > 80:
                x, y, bw, bh = cv2.boundingRect(cnt)
                cv2.rectangle(blended, (x, y), (x + bw, y + bh), (0, 0, 255), 2)
                cv2.putText(blended, "Disease Spot", (x, max(15, y - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

        cv2.imwrite(output_abs_path, blended)
        return relative_path

    except Exception as e:
        print(f"Error generating Grad-CAM heatmap: {e}")
        return None
