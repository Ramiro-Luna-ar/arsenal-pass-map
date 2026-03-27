import pandas as pd
import random
import os
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_players import players

passes = []

player_names = list(players.keys())

for i in range(250):  # cantidad de pases del partido

    passer = random.choice(player_names)
    receiver = random.choice([p for p in player_names if p != passer])

    x_start, y_start = players[passer]["position"]
    x_end, y_end = players[receiver]["position"]

    # agregar ruido para que no todos los pases sean iguales
    x_start += random.uniform(-7,7)
    y_start += random.uniform(-7,7)

    x_end += random.uniform(-7,7)
    y_end += random.uniform(-7,7)

    passes.append({
        "passer": passer,
        "receiver": receiver,
        "x_start": round(x_start,2),
        "y_start": round(y_start,2),
        "x_end": round(x_end,2),
        "y_end": round(y_end,2)
    })

if __name__ == "__main__":

    df = pd.DataFrame(passes)

    df.to_csv("data/data_passing.csv", index=False)

    print("Dataset creado: data_passing.csv")