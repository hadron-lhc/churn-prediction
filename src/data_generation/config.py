TRANSITIONS = {
    "heavy_buyer": {
        "active": {
            "active": 0.92,
            "cooling_down": 0.07,
            "inactive": 0.01,
        },
        "cooling_down": {
            "active": 0.35,
            "cooling_down": 0.50,
            "inactive": 0.15,
        },
        "inactive": {
            "reactivated": 0.30,
            "inactive": 0.70,
        },
        "reactivated": {
            "active": 0.70,
            "cooling_down": 0.20,
            "inactive": 0.10,
        },
    },
    "casual_buyer": {
        "active": {
            "active": 0.80,
            "cooling_down": 0.15,
            "inactive": 0.05,
        },
        "cooling_down": {
            "active": 0.25,
            "cooling_down": 0.45,
            "inactive": 0.30,
        },
        "inactive": {
            "reactivated": 0.20,
            "inactive": 0.80,
        },
        "reactivated": {
            "active": 0.50,
            "cooling_down": 0.30,
            "inactive": 0.20,
        },
    },
    "discount_hunter": {
        "active": {
            "active": 0.70,
            "cooling_down": 0.20,
            "inactive": 0.10,
        },
        "cooling_down": {
            "active": 0.30,
            "cooling_down": 0.30,
            "inactive": 0.40,
        },
        "inactive": {
            "reactivated": 0.45,
            "inactive": 0.55,
        },
        "reactivated": {
            "active": 0.60,
            "cooling_down": 0.20,
            "inactive": 0.20,
        },
    },
    "window_shopper": {
        "active": {
            "active": 0.65,
            "cooling_down": 0.20,
            "inactive": 0.15,
        },
        "cooling_down": {
            "active": 0.10,
            "cooling_down": 0.35,
            "inactive": 0.55,
        },
        "inactive": {
            "reactivated": 0.15,
            "inactive": 0.85,
        },
        "reactivated": {
            "active": 0.35,
            "cooling_down": 0.30,
            "inactive": 0.35,
        },
    },
    "one_time_buyer": {
        "active": {
            "active": 0.20,
            "inactive": 0.80,
        },
        "cooling_down": {
            "inactive": 0.90,
            "active": 0.10,
        },
        "inactive": {
            "reactivated": 0.05,
            "inactive": 0.95,
        },
        "reactivated": {
            "active": 0.10,
            "inactive": 0.90,
        },
    },
    "loyal_customer": {
        "active": {
            "active": 0.95,
            "cooling_down": 0.04,
            "inactive": 0.01,
        },
        "cooling_down": {
            "active": 0.45,
            "cooling_down": 0.45,
            "inactive": 0.10,
        },
        "inactive": {
            "reactivated": 0.40,
            "inactive": 0.60,
        },
        "reactivated": {
            "active": 0.80,
            "cooling_down": 0.15,
            "inactive": 0.05,
        },
    },
}

PERSONAS = {
    "heavy_buyer": {
        # comportamiento base
        "login_rate": (0.65, 0.90),
        "purchase_rate": (0.35, 0.60),
        # ordenes
        "avg_days_between_orders": (2, 7),
        "avg_order_value": (80, 250),
        "items_per_order": (2, 6),
        # comportamiento comercial
        "discount_sensitivity": (0.0, 0.2),
        # engagement
        "session_length": (10, 25),
        # churn/reactivación
        "churn_risk": (0.01, 0.05),
        "reactivation_chance": (0.05, 0.15),
    },
    "casual_buyer": {
        "login_rate": (0.20, 0.50),
        "purchase_rate": (0.10, 0.30),
        "avg_days_between_orders": (15, 40),
        "avg_order_value": (40, 120),
        "items_per_order": (1, 4),
        "discount_sensitivity": (0.2, 0.5),
        "session_length": (5, 15),
        "churn_risk": (0.05, 0.15),
        "reactivation_chance": (0.15, 0.35),
    },
    "discount_hunter": {
        "login_rate": (0.30, 0.70),
        "purchase_rate": (0.05, 0.20),
        "avg_days_between_orders": (10, 35),
        "avg_order_value": (20, 70),
        "items_per_order": (1, 3),
        "discount_sensitivity": (0.70, 1.00),
        "session_length": (8, 20),
        "churn_risk": (0.10, 0.30),
        "reactivation_chance": (0.30, 0.60),
    },
    "window_shopper": {
        "login_rate": (0.40, 0.80),
        "purchase_rate": (0.01, 0.05),
        "avg_days_between_orders": (60, 180),
        "avg_order_value": (10, 40),
        "items_per_order": (1, 2),
        "discount_sensitivity": (0.30, 0.70),
        # IMPORTANTÍSIMO:
        # muchas sesiones pero poca conversión
        "session_length": (15, 40),
        "churn_risk": (0.20, 0.45),
        "reactivation_chance": (0.40, 0.70),
    },
    "one_time_buyer": {
        "login_rate": (0.05, 0.20),
        "purchase_rate": (0.03, 0.10),
        "avg_days_between_orders": (90, 365),
        "avg_order_value": (30, 100),
        "items_per_order": (1, 2),
        "discount_sensitivity": (0.20, 0.60),
        "session_length": (2, 8),
        "churn_risk": (0.40, 0.80),
        "reactivation_chance": (0.05, 0.20),
    },
    "loyal_customer": {
        "login_rate": (0.50, 0.85),
        "purchase_rate": (0.25, 0.45),
        "avg_days_between_orders": (5, 15),
        "avg_order_value": (120, 400),
        "items_per_order": (3, 8),
        "discount_sensitivity": (0.0, 0.1),
        "session_length": (12, 30),
        "churn_risk": (0.01, 0.03),
        "reactivation_chance": (0.02, 0.10),
    },
}

"""

STATES = {
    "active": {
        "login_multiplier": 1.0,
        "purchase_multiplier": 1.0,
        "session_multiplier": 1.0,
    },
    "cooling_down": {
        "login_multiplier": 0.6,
        "purchase_multiplier": 0.5,
        "session_multiplier": 0.7,
    },
    "inactive": {
        "login_multiplier": 0.1,
        "purchase_multiplier": 0.05,
        "session_multiplier": 0.2,
    },
    "reactivated": {
        "login_multiplier": 1.2,
        "purchase_multiplier": 1.3,
        "session_multiplier": 1.1,
    },
}
"""
