from personas import PERSONAS
from users import SimulatedUser
from dataclasses import asdict

import random
import pandas as pd

PERSONA_DISTRIBUTION = {
    "casual_buyer": 0.40,
    "window_shopper": 0.25,
    "one_time_buyer": 0.15,
    "discount_hunter": 0.10,
    "heavy_buyer": 0.07,
    "loyal_customer": 0.03,
}

STATE_DISTRIBUTION = {
    "active": 0.70,
    "inactive": 0.10,
    "cooling_down": 0.15,
    "reactivated": 0.04,
    "high_intent": 0.01,
}


def choose_persona():
    personas = list(PERSONA_DISTRIBUTION.keys())
    weights = list(PERSONA_DISTRIBUTION.values())
    return random.choices(personas, weights=weights, k=1)[0]


def choose_initial_state(persona):
    states = list(STATE_DISTRIBUTION.keys())
    weights = list(STATE_DISTRIBUTION.values())

    if persona == "heavy_buyer":
        weights[states.index("active")] += 0.10
        weights[states.index("inactive")] -= 0.05
        weights[states.index("cooling_down")] -= 0.05
    elif persona == "one_time_buyer":
        weights[states.index("inactive")] += 0.10
        weights[states.index("active")] -= 0.05
        weights[states.index("cooling_down")] -= 0.05
    elif persona == "discount_hunter":
        weights[states.index("cooling_down")] += 0.10
        weights[states.index("active")] -= 0.05
        weights[states.index("inactive")] -= 0.05
    elif persona == "loyal_customer":
        weights[states.index("active")] += 0.15
        weights[states.index("inactive")] -= 0.10
        weights[states.index("cooling_down")] -= 0.05
    elif persona == "window_shopper":
        weights[states.index("inactive")] += 0.05
        weights[states.index("active")] -= 0.05
    elif persona == "casual_buyer":
        pass

    # Normalizar pesos
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]

    return random.choices(states, weights=weights, k=1)[0]


def sample_range(value_range):
    return random.uniform(value_range[0], value_range[1])


def sample_attributes(persona):
    """
    Atributos to sample:

        "login_rate",
        "purchase_rate",
        "avg_days_between_orders",
        "avg_order_value",
        "items_per_order",
        "discount_sensitivity",
        "session_length",
        "churn_risk",
        "reactivation_chance",

    """
    INT_ATTRIBUTES = {"session_length", "items_per_order"}
    attributes = {}
    for attr, value_range in PERSONAS[persona].items():
        if attr in INT_ATTRIBUTES:
            attributes[attr] = int(sample_range(value_range))
        else:
            attributes[attr] = sample_range(value_range)
    return attributes


def generate_user(user_id):
    persona = choose_persona()
    attributes = sample_attributes(persona)
    user = SimulatedUser(
        user_id=user_id,
        persona=persona,
        current_state=choose_initial_state(persona),
        **attributes,
    )
    return user


def generate_users(num_users=1000):
    # Usar el objeto SimulatedUser
    users = []
    for i in range(num_users):
        user = generate_user(i)
        users.append(user)
    return users


def export_user(user):
    data = asdict(user)
    delete_keys = [
        "persona",
        "churn_risk",
        "reactivation_chance",
        "current_state",
        "purchase_rate",
        "login_rate",
    ]
    for key in delete_keys:
        del data[key]
    return data


def main():
    personas = list(PERSONA_DISTRIBUTION.keys())
    weights = list(PERSONA_DISTRIBUTION.values())
    filename = "data/simulated_users.csv"

    random.choices(personas, weights=weights, k=1)

    users = generate_users(1000)
    clean_users = []
    for user in users:
        clean_user = export_user(user)
        clean_users.append(clean_user)

    df = pd.DataFrame(clean_users)
    df.to_csv(filename, index=False)

    for user in users[:5]:  # print first 5 users
        print(user)


if __name__ == "__main__":
    random.seed(42)
    main()
