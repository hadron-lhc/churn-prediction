import pandas as pd
import numpy as np


def get_order_value(sessions):
    avg = sessions["avg_order_value"].values
    noise = np.random.normal(loc=avg, scale=avg * 0.1)

    rounded = np.round(noise, 2).astype(float)
    order_values = np.clip(rounded, 1, None)

    return order_values


def get_item_count(sessions):
    avg = sessions["items_per_order"].values
    noise = np.random.normal(loc=avg, scale=avg * 0.2)

    rounded = np.round(noise).astype(int)
    items_count = np.clip(rounded, 1, None)

    return items_count


def get_used_discount(sessions):
    random_values = np.random.rand(len(sessions))

    return random_values < sessions["discount_sensitivity"].values


def create_orders(sessions):
    order_ids = np.arange(0, len(sessions))

    order_value = get_order_value(sessions)
    items_count = get_item_count(sessions)
    used_discount = get_used_discount(sessions)

    payment_method = np.random.choice(
        ["card", "paypal", "crypto"], size=len(sessions), p=[0.7, 0.25, 0.05]
    )

    orders_df = pd.DataFrame(
        {
            "order_id": order_ids,
            "session_id": sessions["session_id"].values,
            "user_id": sessions["user_id"].values,
            "order_date": sessions["session_date"].values,
            "order_value": order_value,
            "items_count": items_count,
            "used_discount": used_discount,
            "payment_method": payment_method,
        }
    )

    return orders_df


def main():
    sessions = pd.read_csv("./data/sessions.csv")
    users = pd.read_csv("./data/simulated_users_results.csv")

    valid_sessions = sessions[sessions["converted"]]
    orders_base = valid_sessions.merge(users, on="user_id", how="left")

    orders = create_orders(orders_base)

    orders.to_csv("./data/orders.csv", index=False)

    print("Ordenes guardadas")


if __name__ == "__main__":
    np.random.seed(42)
    main()
