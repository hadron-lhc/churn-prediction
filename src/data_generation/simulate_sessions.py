import pandas as pd
import numpy as np
import datetime


STATE_MULTIPLIERS = {
    "active": 1.0,
    "cooling_down": 0.6,
    "inactive": 0.15,
    "reactivated": 1.3,
    "high_intent": 1.6,
}


def maybe_login(login_rates, states):
    """
    Decide qué usuarios loguean hoy.

    La probabilidad real depende de:
    - login_rate base del usuario
    - estado actual del usuario
    """

    multipliers = states.map(STATE_MULTIPLIERS)

    adjusted_rates = np.clip(
        login_rates * multipliers,
        0,
        1,
    )

    random_values = np.random.rand(len(login_rates))

    return random_values < adjusted_rates


def generate_engagement(active_users):
    """
    Genera engagement coherente con el perfil del usuario.

    NO random puro:
    el usuario tiene un baseline estable
    y el día agrega variación pequeña.
    """

    num_sessions = len(active_users)

    # Variación diaria pequeña
    duration_noise = np.random.uniform(
        0.7,
        1.3,
        size=num_sessions,
    )

    durations = (active_users["session_length"].values * duration_noise).astype(int)

    durations = np.clip(durations, 1, None)

    # Pages correlaciona con duración
    browsing_noise = np.random.uniform(
        0.8,
        1.5,
        size=num_sessions,
    )

    pages_viewed = (durations * browsing_noise).astype(int)

    pages_viewed = np.clip(pages_viewed, 1, None)

    return durations, pages_viewed


def calculate_conversion_probability(active_users):
    """
    Calcula probabilidad de compra basada
    en atributos reales del usuario.
    """

    states = active_users["current_state"]
    state_multiplier = states.map(STATE_MULTIPLIERS).values

    base_probability = active_users["login_rate"].values * 0.3

    discount_boost = active_users["discount_sensitivity"].values * 0.1

    conversion_probability = base_probability + discount_boost

    conversion_probability *= state_multiplier

    conversion_probability = np.clip(
        conversion_probability,
        0,
        0.95,
    )

    return conversion_probability


def create_sessions(active_users, actual_date, session_start_id):
    """
    Genera sesiones para todos los usuarios activos del día.
    """

    num_sessions = len(active_users)

    if num_sessions == 0:
        return None

    # Session IDs incrementales
    session_ids = np.arange(
        session_start_id,
        session_start_id + num_sessions,
    )

    durations, pages_viewed = generate_engagement(active_users)

    conversion_probability = calculate_conversion_probability(active_users)

    converted = np.random.rand(num_sessions) < conversion_probability

    sessions_df = pd.DataFrame(
        {
            "session_id": session_ids,
            "user_id": active_users["user_id"].values,
            "session_date": actual_date,
            "session_duration_minutes": durations,
            "pages_viewed": pages_viewed,
            "device": active_users["device"].values,
            "traffic_source": active_users["traffic_source"].values,
            "converted": converted,
        }
    )

    return sessions_df


def main():
    users = pd.read_csv("./data/simulated_users.csv")

    num_users = len(users)

    # Preferencias persistentes del usuario
    if "device" not in users.columns:
        users["device"] = np.random.choice(
            ["mobile", "desktop"],
            size=num_users,
            p=[0.65, 0.35],
        )

    if "traffic_source" not in users.columns:
        users["traffic_source"] = np.random.choice(
            ["organic", "ad", "email"],
            size=num_users,
            p=[0.5, 0.3, 0.2],
        )

    start_date = datetime.date(2024, 1, 1)

    end_date = datetime.date(2026, 1, 1)

    actual_date = start_date

    all_sessions = []

    session_counter = 1

    while actual_date <= end_date:
        logged_in_mask = maybe_login(
            users["login_rate"],
            users["current_state"],
        )

        active_users = users[logged_in_mask]

        day_sessions = create_sessions(
            active_users=active_users,
            actual_date=actual_date,
            session_start_id=session_counter,
        )

        if day_sessions is not None:
            all_sessions.append(day_sessions)

            session_counter += len(day_sessions)

        actual_date += datetime.timedelta(days=1)

    sessions_df = pd.concat(
        all_sessions,
        ignore_index=True,
    )

    sessions_df.to_csv(
        "./data/sessions.csv",
        index=False,
    )

    print("Sessions dataset generated successfully.")


if __name__ == "__main__":
    np.random.seed(42)

    main()
