import os
import json

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'saved_model'))
METRICS_JSON = os.path.join(MODEL_DIR, 'metrics.json')

def print_evaluation_report():
    if not os.path.exists(METRICS_JSON):
        print(f"Metrics file not found at {METRICS_JSON}. Please run train.py first.")
        return

    with open(METRICS_JSON, 'r') as f:
        metrics = json.load(f)

    print("==================================================")
    print("      ML BASELINE MODEL EVALUATION REPORT        ")
    print("==================================================")
    print(f"Train Samples: {metrics.get('train_samples')}")
    print(f"Test Samples:  {metrics.get('test_samples')}")
    print(f"Accuracy:      {metrics['accuracy'] * 100:.2f}%")
    print(f"Precision:     {metrics['precision'] * 100:.2f}%")
    print(f"Recall:        {metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:      {metrics['f1_score'] * 100:.2f}%")
    print("--------------------------------------------------")
    print("Classes Evaluated:")
    for cls in metrics['classes']:
        print(f" - {cls}")
    print("--------------------------------------------------")
    print("Confusion Matrix:")
    cm = metrics['confusion_matrix']
    for row in cm:
        print("  ", row)
    print("==================================================")

if __name__ == '__main__':
    print_evaluation_report()
