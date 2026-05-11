# src/data_generation/states.py

STATES = {
    "active": {
        "login_multiplier": 1.0,
        "purchase_multiplier": 1.0,
        "session_multiplier": 1.0,
    },
    "high_intent": {
        "login_multiplier": 1.3,
        "purchase_multiplier": 1.5,
        "session_multiplier": 1.2,
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
