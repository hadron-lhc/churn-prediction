from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR


def sessions_to_merge(df):
    df = df.copy()

    df["session_date"] = pd.to_datetime(df["session_date"])

    df = df.rename(columns={"session_date": "snapshot_date"})
    df = df[["user_id", "snapshot_date"]]

    active_today = (
        df.groupby(["user_id", "snapshot_date"]).size().reset_index(name="active_today")
    )

    return active_today


def orders_to_merge(df):
    df = df.copy()

    df["order_date"] = pd.to_datetime(df["order_date"])
    df = df[["user_id", "order_date"]]

    df = df.rename(columns={"order_date": "snapshot_date"})

    purchase_today = (
        df.groupby(["user_id", "snapshot_date"])
        .size()
        .reset_index(name="purchase_today")
    )

    return purchase_today


def purchases_last_30_days(df):
    """
    Cantidad de compras en los ultimos 30 dias
    por cada usuario y cada dia
    """
    df = df.copy()

    df["order_date"] = pd.to_datetime(df["order_date"])
    df = df[["user_id", "order_date"]]

    df = df.rename(columns={"order_date": "snapshot_date"})
    df = df.sort_values(["user_id", "snapshot_date"])

    df["purchase"] = 1

    purchase_last_30_days = (
        df.groupby("user_id")
        .rolling(window="30D", on="snapshot_date")["purchase"]
        .sum()
        .reset_index(name="purchase_last_30_days")
    )

    return purchase_last_30_days


def main():
    users = pd.read_csv(DATA_DIR / "raw/simulated_users.csv")
    sessions = pd.read_csv(DATA_DIR / "raw/sessions.csv")
    orders = pd.read_csv(DATA_DIR / "raw/orders.csv")

    df_users = users[["user_id"]]

    date_range = pd.date_range(start="2024-01-01", end="2026-01-01")

    df_dates = pd.DataFrame(date_range, columns=["snapshot_date"])

    df_daily = pd.merge(df_users, df_dates, how="cross")

    auxiliar_sessions = sessions_to_merge(sessions)

    auxiliar_orders = orders_to_merge(orders)

    df_daily = df_daily.merge(auxiliar_sessions, how="left").fillna(0)

    df_daily = df_daily.merge(auxiliar_orders, how="left").fillna(0)

    purchase_last_30_days = purchases_last_30_days(orders)
    df_daily = df_daily.merge(purchase_last_30_days, how="left").fillna(0)

    print(df_daily.head())


if __name__ == "__main__":
    main()
