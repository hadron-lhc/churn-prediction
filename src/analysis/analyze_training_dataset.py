from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR


def show_info(df):
    print(df.info())
    print(df.describe())

    print(df["target_churn_30d"].value_counts(normalize=True))
    print(df.isna().sum())

    return


def show_corr(df):
    corr = df.corr(numeric_only=True)

    print(corr["target_churn_30d"].sort_values(ascending=False))

    return


def main():
    training_dataset = pd.read_parquet(DATA_DIR / "processed/training_dataset.parquet")

    # show_info(training_dataset)
    show_corr(training_dataset)


if __name__ == "__main__":
    main()
