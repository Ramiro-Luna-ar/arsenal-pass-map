import pandas as pd
import random
import os

print("Directorio actual:", os.getcwd())
players = [
    "Raya",
    "White",
    "Saliba",
    "Gabriel",
    "Zinchenko",
    "Rice",
    "Odegaard",
    "Havertz",
    "Saka",
    "Martinelli",
    "Jesus"
]

# posiciones promedio aproximadas
positions = {
    "Raya": (50,10),
    "White": (85,30),
    "Saliba": (35,25),
    "Gabriel": (65,25),
    "Zinchenko": (15,30),
    "Rice": (50,55),
    "Odegaard": (40,70),
    "Havertz": (60,70),
    "Saka": (85,90),
    "Martinelli": (15,90),
    "Jesus": (50,80)
}

passes = []

for i in range(250):  # cantidad de pases del partido

    passer = random.choice(players)
    receiver = random.choice([p for p in players if p != passer])

    x_start, y_start = positions[passer]
    x_end, y_end = positions[receiver]

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

df = pd.DataFrame(passes)

df.to_csv("data/data_passing.csv", index=False)

print("Dataset creado: data_passing.csv")