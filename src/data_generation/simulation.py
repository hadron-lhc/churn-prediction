# src/data_generation/simulation.py

"""
FLUJO GENERAL DEL SIMULADOR

for each simulated day:

    for each user:

        1. actualizar estado
        2. decidir login
        3. generar sesión
        4. generar eventos
        5. decidir compra
        6. generar orden
        7. actualizar historial
"""

from personas import PERSONAS
from states import STATES
from transitions import TRANSITIONS
