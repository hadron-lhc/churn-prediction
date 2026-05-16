from pathlib import Path
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR


def sessions_to_merge(df):
    df["session_date"] = pd.to_datetime(df["session_date"])
    df = df.rename(columns={"session_date": "snapshot_date"})
    df = df[["user_id", "snapshot_date"]]

    active_today = (
        df.groupby(["user_id", "snapshot_date"]).size().reset_index(name="active_today")
    )

    return active_today


def orders_to_merge(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df = df.rename(columns={"order_date": "snapshot_date"})
    df = df[["user_id", "snapshot_date"]]

    purchase_today = (
        df.groupby(["user_id", "snapshot_date"])
        .size()
        .reset_index(name="purchase_today")
    )

    return purchase_today


def purchases_last_K_days(df, k):
    """
    Cantidad de compras en los ultimos k dias
    por cada usuario y cada dia
    """
    df = df.copy()
    days = f"{k}D"

    df[f"purchase_last_{k}_days"] = (
        df.groupby("user_id")
        .rolling(window=days, on="snapshot_date")["purchase_today"]
        .sum()
        .values.astype(int)
    )

    return df


def sessions_last_K_days(df, k):
    """
    Cantidad de sesiones
    por usuario los ultimos
    K dias
    """

    df = df.copy()
    days = f"{k}D"

    df[f"session_last_{k}_days"] = (
        df.groupby("user_id")
        .rolling(window=days, on="snapshot_date")["active_today"]
        .sum()
        .values.astype(int)
    )

    return df


def days_since_last_purchase_func(df):
    df = df.copy()
    df["last_purchase_date"] = df["snapshot_date"].where(df["purchase_today"] > 0)
    df["last_purchase_date"] = df.groupby("user_id")["last_purchase_date"].ffill()
    df["days_since_last_purchase"] = (
        df["snapshot_date"] - df["last_purchase_date"]
    ).dt.days

    df["days_since_last_purchase"] = (
        df["days_since_last_purchase"].fillna(-1).astype(int)
    )

    return df.drop(columns=["last_purchase_date"])


def days_since_last_session_func(df):
    df = df.copy()
    df["last_session_date"] = df["snapshot_date"].where(df["active_today"] > 0)
    df["last_session_date"] = df.groupby("user_id")["last_session_date"].ffill()

    df["days_since_last_session"] = (
        df["snapshot_date"] - df["last_session_date"]
    ).dt.days

    df["days_since_last_session"] = df["days_since_last_session"].fillna(-1).astype(int)

    return df.drop(columns=["last_session_date"])


def purchase_ratio(df):
    df = df.copy()
    df["purchase_ratio_7d_30d"] = np.where(
        df["purchase_last_30_days"] > 0,
        df["purchase_last_7_days"] / df["purchase_last_30_days"],
        0,
    )

    return df


def get_new_df(users, sessions, orders):
    df_users = users[["user_id"]]

    date_range = pd.date_range(start="2024-01-01", end="2026-01-01")
    df_dates = pd.DataFrame(date_range, columns=["snapshot_date"])

    df_daily = pd.merge(df_users, df_dates, how="cross").reset_index(drop=True)

    df_daily["snapshot_date"] = pd.to_datetime(df_daily["snapshot_date"])

    auxiliar_sessions = sessions_to_merge(sessions)
    auxiliar_orders = orders_to_merge(orders)

    df_daily = df_daily.merge(
        auxiliar_sessions, how="left", on=["user_id", "snapshot_date"]
    )
    df_daily = df_daily.merge(
        auxiliar_orders, how="left", on=["user_id", "snapshot_date"]
    )

    df_daily = df_daily.sort_values(["user_id", "snapshot_date"])

    return df_daily


def add_features(df_daily):
    df_daily = df_daily.sort_values(["user_id", "snapshot_date"])

    df_daily["active_today"] = df_daily["active_today"].fillna(0).astype(int)
    df_daily["purchase_today"] = df_daily["purchase_today"].fillna(0).astype(int)

    df_daily = purchases_last_K_days(df_daily, 7)
    df_daily = purchases_last_K_days(df_daily, 30)

    df_daily = sessions_last_K_days(df_daily, 7)
    df_daily = sessions_last_K_days(df_daily, 30)

    df_daily = days_since_last_purchase_func(df_daily)
    df_daily = days_since_last_session_func(df_daily)

    df_daily = purchase_ratio(df_daily)

    df_daily = df_daily.sort_values(["user_id", "snapshot_date"])

    return df_daily


def main():
    users = pd.read_csv(DATA_DIR / "raw/simulated_users.csv")
    sessions = pd.read_csv(DATA_DIR / "raw/sessions.csv")
    orders = pd.read_csv(DATA_DIR / "raw/orders.csv")

    df_daily = get_new_df(users, sessions, orders)
    df_daily = add_features(df_daily)

    print(df_daily)


if __name__ == "__main__":
    main()
