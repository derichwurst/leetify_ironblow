import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_handling import get_data_for_dashboard  # Importiere das Daten-Modul

# --- 1. DATEN ABRUFEN ---
df_stats = get_data_for_dashboard()

# --- 2. DASH APP INITIALISIEREN ---
app = dash.Dash()

# --- VORBEREITUNG FÜR LAYOUT ---
player_options = [{'label': name, 'value': name} for name in df_stats['Name'].unique()]
all_players = df_stats['Name'].unique().tolist()

# Die Metriken, die im Radar Chart verglichen werden sollen
RADAR_METRICS = [
    'Aim_Rating',
    'Utility_Rating',
    'Opening_Kill_Success',
    'Clutch_Percentage',
    'Positioning_Rating',
]
# Spalten, die in Prozent (0-1) vorliegen und auf 0-100 skaliert werden müssen
PERCENTAGE_COLS = ['Clutch_Percentage']

# --- 3. LAYOUT DEFINIEREN ---

app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[

    html.H1("🎮 IronBlow Leetify Statistiken", style={'textAlign': 'center', 'color': '#007bff'}),
    html.Hr(),

    # Kontrollbereich (Multi-Select Dropdown)
    html.Div([
        html.Label("Wähle die Spieler für den Vergleich:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='player-select-multiselect',
            options=player_options,
            value=all_players,  # Standardwert: Alle Spieler sind ausgewählt
            multi=True,  # NEU: Erlaubt die Auswahl mehrerer Optionen
            clearable=False
        ),
    ], style={'width': '60%', 'margin': 'auto', 'marginBottom': '30px'}),  # Zentriert das Auswahlfeld

    # --- DASHBOARD BEREICH ---

    # 1. Multi-Player Radar Chart
    html.H2("📊 Vergleich der Spielerleistungen (Radar Chart)", style={'textAlign': 'center', 'color': '#333'}),
    html.Div([
        dcc.Graph(id='player-radar-chart')
    ], style={'width': '80%', 'margin': 'auto', 'marginBottom': '30px'}),  # Breite angepasst

    html.Hr(),

    # 1.5. BarChart (Aim Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='leetify-rating-bar-chart'),
        html.Div(
            id='leetify-rating-explanation',
            children=[
                html.P([
                    html.Strong("Erläuterung:"), " Das obere Balkendiagramm vergleicht das ",
                    html.Strong("Leetify Rating"), " der oben ausgewählten Spieler. ",
                    "Die Leetify Score ist ein komplexer, kontextbezogener Spieler-Rating-Wert, der speziell "
                    "entwickelt wurde, um den tatsächlichen Einfluss (Impact) eines Spielers auf den Ausgang "
                    "einer Runde oder eines Matches in CS:GO/CS2 genauer zu messen, als es einfache Metriken wie "
                    "Kills oder der offizielle Spiel-Score tun.",
                    "Leetify selbst beschreibt seine Bewertung als ein wirtschaftlich angepasstes, auf der "
                    "Gewinnwahrscheinlichkeit basierendes System."
                ], style={'fontSize': '14px', 'padding': '10px 20px', 'backgroundColor': '#e8f0fe',
                          'borderRadius': '5px', 'borderLeft': '3px solid #007bff'})
            ])
    ]),

    # 2. BarChart (Aim Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='aim-rating-bar-chart')
    ]),

    # 3. BarChart (Utility Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='utility-rating-bar-chart')
    ]),

    # 4. BarChart (opening Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='opening-rating-bar-chart')
    ]),

    # 5. BarChart (clutch Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='clutch-rating-bar-chart')
    ]),

    # 6. BarChart (positioning Rating Vergleich – bleibt als Zusatzansicht)
    html.Div([
        dcc.Graph(id='positioning-rating-bar-chart')
    ]),

])


# --- 4. CALLBACKS (INTERAKTIVITÄT) DEFINIEREN ---

# Callback für das Radar Chart (Multi-Spieler-Vergleich)
@app.callback(
    Output('player-radar-chart', 'figure'),
    Input('player-select-multiselect', 'value')
)
def update_radar_chart(selected_players):
    # Wenn keine Spieler ausgewählt sind, gib ein leeres Diagramm zurück
    if not selected_players:
        return {}

    # Filtern des Haupt-DataFrames auf die ausgewählten Spieler
    df_filtered = df_stats[df_stats['Name'].isin(selected_players)].copy()

    # Skalierung der Prozentwerte (0-1) auf 0-100, damit sie mit den Ratings vergleichbar sind
    for col in PERCENTAGE_COLS:
        df_filtered[col] = df_filtered[col] * 100

    # Umformen des DataFrames vom Wide Format ins Long Format (erforderlich für Plotly Express)
    df_long = df_filtered.melt(
        id_vars=['Name'],
        value_vars=RADAR_METRICS,
        var_name='Metric',
        value_name='Score'
    )

    # Erzeuge das Polar (Radar)-Chart
    fig = px.line_polar(
        df_long,
        r='Score',
        theta='Metric',
        color='Name',  # Plotly erstellt eine separate Linie pro 'Name'-Wert
        line_close=True,
        title="Vergleich der Spielerleistungen auf Basis der Leetify-Statistiken"
    )

    # Optische Anpassungen
    fig.update_traces(fill='toself', opacity=0.5)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])  # Einheitliche Skalierung 0-100
        ),
        legend_title_text='Spieler'
    )

    return fig


# Callback für das BarChart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('leetify-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart nur mit den ausgewählten Spielern
    fig = px.bar(
        df_filtered_bar,  # Verwende den gefilterten DataFrame
        x='Name',
        y='Leetify_Rating',
        title='Vergleich des Leetify Ratings der ausgewählten Spieler '
              '<br> Formel: (ct_leetify_rateing + t_leetify_rateing) / 2 ',
        color='Leetify_Rating',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Leetify Rating")
    return fig


# Callback für dasBar Chart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('aim-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart nur mit den ausgewählten Spielern
    fig = px.bar(
        df_filtered_bar,  # Verwende den gefilterten DataFrame
        x='Name',
        y='Aim_Rating',
        title='Vergleich des Aim Ratings der ausgewählten Spieler',
        color='Aim_Rating',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Aim Rating (Leetify Score)")
    return fig


# Callback für das BarChart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('utility-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart, das das Aim Rating aller Spieler vergleicht
    fig = px.bar(
        df_filtered_bar,
        x='Name',
        y='Utility_Rating',
        title='Vergleich des Utility Ratings aller Spieler',
        color='Utility_Rating',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Utility Rating (Leetify Score)")
    return fig


# Callback für das BarChart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('opening-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart, das das Aim Rating aller Spieler vergleicht
    fig = px.bar(
        df_filtered_bar,
        x='Name',
        y='Opening_Kill_Success',
        title='Vergleich des Opening_Kill_Success Ratings aller Spieler (Wert = Value x 1000)',
        color='Opening_Kill_Success',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Opening_Kill_Success Rating (Leetify Score)")
    return fig


# Callback für das BarChart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('clutch-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart, das das Aim Rating aller Spieler vergleicht
    fig = px.bar(
        df_filtered_bar,
        x='Name',
        y='Clutch_Percentage',
        title='Vergleich des Clutch_Percentage Ratings aller Spieler',
        color='Clutch_Percentage',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Clutch_Percentage Rating (Leetify Score)")
    return fig


# Callback für das BarChart (Gesamtübersicht - bleibt unverändert)
@app.callback(
    Output('positioning-rating-bar-chart', 'figure'),
    Input('player-select-multiselect', 'value')  # Abhängigkeit von der Auswahl für einen sauberen Ablauf
)
def update_bar_chart(selected_players):
    if not selected_players:
        # Rückgabe eines leeren Diagramms, falls nichts ausgewählt ist
        return {}

        # NEU: Filtern des DataFrames basierend auf der Auswahl
    df_filtered_bar = df_stats[df_stats['Name'].isin(selected_players)]

    # Erstelle ein BarChart, das das Aim Rating aller Spieler vergleicht
    fig = px.bar(
        df_filtered_bar,
        x='Name',
        y='Positioning_Rating',
        title='Vergleich des Positioning_Rating aller Spieler',
        color='Positioning_Rating',
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title="Positioning_Rating (Leetify Score)")
    return fig


# --- 5. APP STARTEN ---
if __name__ == '__main__':
#     # print("Starte Dash App...")
#     # print("Öffne http://127.0.0.1:8050/ in deinem Browser")
    app.run(debug=True)

server = app.server

