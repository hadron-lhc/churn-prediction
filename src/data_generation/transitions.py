# src/data_generation/transitions.py

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
    },
    "one_time_buyer": {
        "active": {
            "active": 0.20,
            "inactive": 0.80,
        },
        "inactive": {
            "reactivated": 0.05,
            "inactive": 0.95,
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
    },
}
