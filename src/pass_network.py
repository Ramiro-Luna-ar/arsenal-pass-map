import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from data.data_players import players

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/data_passing.csv")

pass_counts = (
    df
    .groupby(["passer", "receiver"])
    .size()
    .reset_index(name="pass_count")
)
max_passes = pass_counts["pass_count"].max()
pitch = Image.open("assets/cancha1.png")
fig = go.Figure()

# =========================
# DRAW PASSES (LINES)
# =========================

for _, row in pass_counts.iterrows():

    x_start, y_start = players[row["passer"]]["position"]
    x_end, y_end = players[row["receiver"]]["position"]

    width = row["pass_count"] * 1.2

    fig.add_trace(
        go.Scatter(
            x=[x_start, x_end],
            y=[y_start, y_end],
            mode="lines",
            line=dict(color="blue", width=width),
            opacity = max(0.15, row["pass_count"] / max_passes),
            hoverinfo="skip",
            showlegend=False
        )
    )

# =========================
# CALCULATE CONNECTIONS
# =========================

connection_counts = {}

for _, row in pass_counts.iterrows():

    passer = row["passer"]
    receiver = row["receiver"]
    count = row["pass_count"]

    connection_counts[passer] = connection_counts.get(passer, 0) + count
    connection_counts[receiver] = connection_counts.get(receiver, 0) + count

# =========================
# DRAW PLAYERS (NODES)
# =========================

for player, data in players.items():

    x, y = data["position"]
    number = data["number"]

    connections = connection_counts.get(player, 0)
    size = connections * 1.2

    # nodo
    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(
                size=size,
                color="red",
                line=dict(width=2, color="white")
            ),
            text=str(number),
            textposition="middle center",
            textfont=dict(color="white", size=14),
            hovertemplate=
            "<b>%{customdata[0]}</b><br>" +
            "Connections: %{customdata[1]}" +
            "<extra></extra>",
            customdata=[[player, connections]],
            showlegend=False
        )
    )

    # nombre arriba
    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y + 4],
            mode="text",
            text=player,
            textfont=dict(color="white", size=14),
            hoverinfo="skip",
            showlegend=False
        )
    )

# =========================
# LAYOUT
# =========================

fig.update_layout(

    title="Arsenal Pass Network (Simulated Data)",

    autosize=True,
    height=1000,

    plot_bgcolor="black",
    paper_bgcolor="black",

    font=dict(color="white"),

    margin=dict(l=0, r=0, t=50, b=0),

    xaxis=dict(
        range=[0, 100],
        visible=False
    ),

    yaxis=dict(
        range=[0, 100],
        visible=False,
        scaleanchor="x",
        scaleratio=1
    ),

    images=[
        dict(
            source=pitch,
            xref="x",
            yref="y",
            x=0,
            y=100,
            sizex=100,
            sizey=100,
            sizing="stretch",
            layer="below"
        )
    ]
)

# =========================
# SHOW
# =========================

fig.show()