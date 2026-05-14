# src/data_generation/transitions.py

from pandas.core import window
from pandas.core.window import rolling
from config import TRANSITIONS
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import DATA_DIR

import random
import pandas as pd
import numpy as np


def choose_next_state(persona, current_state):
    possible_transitions = TRANSITIONS[persona][current_state]

    state = possible_transitions.keys()
    weights = possible_transitions.values()

    return random.choices(list(state), weights=list(weights))


def add_features(df):
    sessions = df.copy()

    sessions["session_date"] = pd.to_datetime(
        sessions["session_date"], errors="coerce", format="mixed"
    )

    sessions = sessions.sort_values(by=["user_id", "session_date"])

    # Dias desde ultima compra

    sessions["purchase_date_temp"] = sessions["session_date"].where(
        sessions["converted"]
    )

    sessions["last_purchase_date"] = (
        sessions.groupby("user_id")["purchase_date_temp"]
        .shift(
            1
        )  # Desplaza 1 fila para no contar el día de la compra actual como "última compra"
        .groupby(sessions["user_id"])
        .ffill()  # Rellena los NaN hacia abajo con la última fecha de compra encontrada
    )

    sessions["days_since_last_purchase"] = (
        sessions["session_date"] - sessions["last_purchase_date"]
    ).dt.days

    sessions["days_since_last_purchase"] = (
        sessions["days_since_last_purchase"].fillna(0).astype(int)
    )

    sessions = sessions.drop(columns=["purchase_date_temp"])

    # Dias desde ultimo log in
    sessions["days_since_last_login"] = (
        sessions.groupby("user_id")["session_date"].diff().dt.days.fillna(0).astype(int)
    )

    # Compras en los últimos 30 días

    sessions["session_date"] = pd.to_datetime(sessions["session_date"])

    sessions["converted"] = sessions["converted"].astype(int)

    rolling_res = (
        sessions.groupby("user_id")
        .rolling(window="30D", on="session_date")["converted"]
        .sum()
    )

    sessions["last_30d_purchases"] = rolling_res.to_numpy()

    sessions["prev_30d_purchases"] = sessions.groupby("user_id")[
        "last_30d_purchases"
    ].shift()

    sessions = sessions.drop(columns=["prev_30d_purchases"])

    print(sessions)

    return sessions


def main():
    users = pd.read_csv(DATA_DIR / "simulated_users.csv")
    sessions = pd.read_csv(DATA_DIR / "sessions.csv")

    sessions_featured = add_features(sessions)

    for user in users.itertuples():
        next_state = choose_next_state(user.persona, current_state=user.current_state)


if __name__ == "__main__":
    main()
