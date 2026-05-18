from pathlib import Path
import json
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import LOG_DIR


from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate_model(y_test, y_pred, y_prob, model_name="model"):
    metrics = {
        "auc": roc_auc_score(y_test, y_prob),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "timestamp": datetime.now().isoformat(),
        "model_name": model_name,
    }

    return metrics


def print_metrics(metrics):
    print(f"AUC-ROC: {metrics['auc']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")

    print("\nConfusion Matrix:")
    print(metrics["confusion_matrix"])


def save_metrics(metrics, model_name="model"):
    metrics_path = LOG_DIR / f"metrics/{model_name}_metrics.json"

    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    metrics["model_name"] = model_name

    if metrics_path.exists():
        try:
            with open(metrics_path, "r") as f:
                all_metrics = json.load(f)
        except json.JSONDecodeError:
            all_metrics = []
    else:
        all_metrics = []

    all_metrics.append(metrics)

    with open(metrics_path, "w") as f:
        json.dump(all_metrics, f, indent=4)

    print("Log guardado correctamente en:", metrics_path)
