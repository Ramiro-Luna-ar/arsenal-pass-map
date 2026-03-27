import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/data_passing.csv")

pass_counts = df["passer"].value_counts()
players = pass_counts.index.tolist()

trace_indices = {player: [] for player in players}

# =========================
# CREATE FIGURE
# =========================

fig = go.Figure()

# =========================
# LOAD PITCH
# =========================

pitch = Image.open("assets/cancha1.png")

fig.add_layout_image(
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
)

# =========================
# DRAW PASSES
# =========================

for _, row in df.iterrows():

    player = row["passer"]
    segments = 15

    x_start = row["x_start"]
    y_start = row["y_start"]
    x_end = row["x_end"]
    y_end = row["y_end"]

    for i in range(segments):

        x1 = x_start + (x_end - x_start) * (i / segments)
        y1 = y_start + (y_end - y_start) * (i / segments)

        x2 = x_start + (x_end - x_start) * ((i + 1) / segments)
        y2 = y_start + (y_end - y_start) * ((i + 1) / segments)

        r = 255
        g = int(255 * (i / segments))
        b = 0

        width = 6 - (i * 0.3)

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(width=width, color=f"rgb({r},{g},{b})"),
                opacity=0.8,
                showlegend=False,
                hoverinfo="skip"
            )
        )

        trace_indices[player].append(len(fig.data) - 1)

    # punto inicio del pase

    fig.add_trace(
        go.Scatter(
            x=[x_start],
            y=[y_start],
            mode="markers",
            marker=dict(size=10, color="red"),
            showlegend=False,
            hoverinfo="text",
            text=f'{row["passer"]} → {row["receiver"]}'
        )
    )

    trace_indices[player].append(len(fig.data) - 1)

# =========================
# MENU
# =========================

buttons = []

# botón ALL

buttons.append(
    dict(
        label="All Players",
        method="update",
        args=[
            {"visible": [True] * len(fig.data)},
            {"title": "Arsenal – Passes Started by Player"}
        ],
    )
)

# botones por jugador

for player in players:

    visible = [False] * len(fig.data)

    for idx in trace_indices[player]:
        visible[idx] = True

    n_passes = pass_counts[player]

    buttons.append(
        dict(
            label=f"{player} ({n_passes})",
            method="update",
            args=[
                {"visible": visible},
                {"title.text": f"Arsenal – Passes Started by {player} ({n_passes})"}
                ]
            
        )
    )

fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=1.05,
            y=1,
            font=dict(size=22),
            pad=dict(r=15, t=15)
        )
    ]
)

# =========================
# AXES
# =========================

fig.update_xaxes(range=[0, 100], visible=False)

fig.update_yaxes(
    range=[0, 100],
    visible=False,
    scaleanchor="x",
    scaleratio=1
)

# =========================
# LAYOUT
# =========================

fig.update_layout(
    title="Arsenal – Passes Started by Player",
    autosize=True,
    height=1000,
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    margin=dict(l=0, r=0, t=50, b=0)
)

# =========================
# SAVE
# =========================

fig.write_html("outputs/arsenal_pass_map.html")

fig.show()