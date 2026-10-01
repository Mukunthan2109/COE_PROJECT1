# AgriShield Technical Limitations & Future Work

## Current System Limitations

While AgriShield provides an end-to-end working system for crop disease screening and expert escalation, several technical boundaries are documented for clarity:

---

## 1. Machine Learning Baseline Model

- **Dataset Size**: The baseline model is trained on a project dataset of 360 images across 12 classes (30 samples per class).
- **Feature-Based Classifier**: The feature classifier uses HSV histograms, GLCM texture, and dark spot count features with a `RandomForestClassifier`. It provides CPU-trainable initial screening triage but does not match deep learning convolutional architectures (CNNs/ResNet) trained on tens of thousands of field images.
- **Controlled Lighting Sensitivity**: Feature extraction can be sensitive to extreme lighting variations or heavy background clutter.

---

## 2. Preliminary Triage Nature

- **Initial Screening Only**: Automated predictions serve as an initial screening and prioritization tool to alert experts and flag high-risk cases. They do **not** replace certified agricultural expert diagnosis.
- **Confidence Thresholding**: Predictions with confidence `< 70%` are automatically escalated for expert review to maintain safety.

---

## 3. Scope Boundaries

- **Supported Crops**: Restricted strictly to 4 crops (**Tomato**, **Potato**, **Rice**, **Maize / Corn**).
- **Supported Disease Classes**: Restricted strictly to 12 target classes. Unsupported crops or unlisted plant diseases are automatically flagged for expert intervention.

---

## 4. Future Improvements & Roadmap

1. **Deep Learning Upgrades**: Integrate lightweight MobileNet/ResNet models when GPU resources become available.
2. **Offline Mobile PWA Sync**: Enable offline observation drafting on mobile devices with automatic sync when network connection is restored.
3. **Multi-Modal Sensor Integration**: Incorporate micro-climate soil moisture and temperature sensors to improve disease risk modeling.
