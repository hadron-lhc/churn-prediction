from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR


def build_churn_target(df, horizon_days=30):
    df = df.copy()
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

    df = df.sort_values(["user_id", "snapshot_date"])

    future_sum = df.groupby("user_id", group_keys=False).apply(
        lambda x: (
            x.iloc[::-1]
            .rolling(window=f"{horizon_days}D", on="snapshot_date")["purchase_today"]
            .sum()
            .iloc[::-1]
        ),
        include_groups=False,
    )

    future_sum = future_sum.iloc[::-1].values

    future_sum = future_sum - df["purchase_today"]

    df["target_churn_30d"] = (future_sum == 0).astype(int)

    return df


def main():
    base_df = pd.read_csv(DATA_DIR / "processed/daily_users.csv")

    df_target = build_churn_target(base_df)

    df_target.to_parquet(DATA_DIR / "processed/training_dataset.parquet")

    print("Dataset de entrenamiento guardado en data/processed")


if __name__ == "__main__":
    main()
