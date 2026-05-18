from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR

from evaluate import evaluate_model, save_metrics

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def train_and_test(train_df, test_df):
    FEATURES = [
        "purchase_last_30_days",
        "session_last_30_days",
        "days_since_last_purchase",
        "days_since_last_session",
        "purchase_ratio_7d_30d",
        "purchase_per_session_30d",
    ]

    TARGET = "target_churn_30d"

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    return X_train, X_test, y_train, y_test


def logistic_regression(X_train, X_test, y_train, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.3).astype(int)

    metrics = evaluate_model(y_test, y_pred, y_prob)

    save_metrics(metrics, model_name="logistic_regression")

    return model


def random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.3).astype(int)

    metrics = evaluate_model(y_test, y_pred, y_prob)

    save_metrics(metrics, model_name="random_forest")

    return model


def XGBoost(X_train, X_test, y_train, y_test):
    model = XGBClassifier(
        n_estimators=100,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.3).astype(int)

    metrics = evaluate_model(y_test, y_pred, y_prob)

    save_metrics(metrics, model_name="xgboost")

    return model


def main():
    df = pd.read_parquet(DATA_DIR / "processed/training_dataset.parquet")

    train_df = df[df["snapshot_date"] < "2025-10-01"]
    test_df = df[df["snapshot_date"] >= "2025-10-01"]

    X_train, X_test, y_train, y_test = train_and_test(train_df, test_df)

    logistic_regression(X_train, X_test, y_train, y_test)
    random_forest(X_train, X_test, y_train, y_test)
    XGBoost(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
