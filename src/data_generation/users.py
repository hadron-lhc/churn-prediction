# src/data_generation/users.py

from dataclasses import dataclass


@dataclass
class SimulatedUser:
    user_id: int

    # oculto para simulación
    persona: str
    current_state: str

    # parámetros sampleados individualmente
    login_rate: float
    purchase_rate: float

    avg_days_between_orders: float
    avg_order_value: float
    items_per_order: float

    discount_sensitivity: float
    session_length: int

    churn_risk: float
    reactivation_chance: float

    # tracking temporal
    last_order_date: str | None = None
    last_session_date: str | None = None

    total_orders: int = 0
    total_sessions: int = 0
