import streamlit as st
import pandas as pd
import plotly.express as px
# Stellen Sie sicher, dass data_handling in Ihrem Repository existiert und funktioniert.
from data_handling import get_data_for_dashboard

# Konfiguration der Seite
st.set_page_config(
    page_title="IronBlow Leetify Statistiken",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- 1. DATEN ABRUFEN (mit Caching) ---
# Mit @st.cache_data wird die Funktion nur einmal ausgeführt,
# solange sich die Eingaben (oder der Funktionskörper) nicht ändern.
@st.cache_data
def load_data():
    """Lädt die Leetify-Daten einmalig und cached sie."""
    # Verwenden Sie hier Ihre Datenladefunktion
    return get_data_for_dashboard()


df_stats = load_data()

# --- VORBEREITUNG FÜR PLOTS ---
player_options = df_stats['Name'].unique().tolist()

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

# --- 2. LAYOUT UND KONTROLLEN DEFINIEREN ---

st.title("🎮 IronBlow Leetify Statistiken")
st.markdown("Ein interaktives Dashboard zur Analyse der Spielerleistungen.")
st.markdown("---")

# Kontrollbereich (Multi-Select Dropdown)
# Streamlit-Widgets geben den aktuellen Wert direkt zurück
selected_players = st.multiselect(
    "Wähle die Spieler für den Vergleich:",
    options=player_options,
    default=player_options,  # Standardwert: Alle Spieler sind ausgewählt
)

# Überprüfen, ob Spieler ausgewählt sind
if not selected_players:
    st.warning("Bitte wähle mindestens einen Spieler aus, um die Statistiken anzuzeigen.")
    st.stop()

# Filtern des Haupt-DataFrames auf die ausgewählten Spieler
df_filtered = df_stats[df_stats['Name'].isin(selected_players)].copy()

# --- 3. PLOTS GENERIEREN ---

# 1. Multi-Player Radar Chart (Haupt-Vergleich)
st.header("📊 Vergleich der Spielerleistungen (Radar Chart)")
if not df_filtered.empty:

    # Skalierung der Prozentwerte (0-1) auf 0-100
    df_scaled = df_filtered.copy()
    for col in PERCENTAGE_COLS:
        df_scaled[col] = df_scaled[col] * 100

    # Umformen des DataFrames ins Long Format (für Plotly Express)
    df_long = df_scaled.melt(
        id_vars=['Name'],
        value_vars=RADAR_METRICS,
        var_name='Metric',
        value_name='Score'
    )

    # Erzeuge das Polar (Radar)-Chart
    fig_radar = px.line_polar(
        df_long,
        r='Score',
        theta='Metric',
        color='Name',
        line_close=True,
        title="Vergleich der Spielerleistungen auf Basis der Leetify-Statistiken"
    )

    # Optische Anpassungen
    fig_radar.update_traces(fill='toself', opacity=0.5)
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        legend_title_text='Spieler'
    )

    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
st.subheader("Detailvergleiche (Bar Charts)")


# Container für die Bar Charts, um eine 2-spaltige Ansicht zu erzeugen
# Diese Spaltendefinitionen werden entfernt, um eine Einspalten-Ansicht zu erzwingen

# Funktion zum Generieren eines Bar Charts (wird mehrfach verwendet)
# Das Argument 'container' wird entfernt, da das Chart direkt in Streamlit geschrieben wird (volle Breite)
def generate_bar_chart(df, y_col, title, y_label):
    """Generiert ein Bar Chart in voller Breite."""
    fig = px.bar(
        df,
        x='Name',
        y=y_col,
        title=title,
        color=y_col,
        color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(xaxis_title="Spieler", yaxis_title=y_label)
    st.plotly_chart(fig, use_container_width=True)


# 1. Leetify Rating Vergleich
# Die Erklärung steht nun in einer separaten Zeile (volle Breite)
st.markdown(
    """
    <div style='font-size: 14px; padding: 10px 10px; background-color: #e8f0fe; border-radius: 5px; border-left: 3px solid #007bff;'>
        <strong>Erläuterung:</strong> Der Leetify Score ist ein komplexer, kontextbezogener Spieler-Rating-Wert, der speziell 
        entwickelt wurde, um den tatsächlichen Einfluss (Impact) eines Spielers auf den Ausgang 
        einer Runde oder eines Matches in CS:GO/CS2 genauer zu messen.
    </div>
    """, unsafe_allow_html=True
)

# Das Diagramm steht nun in einer eigenen Zeile (volle Breite)
generate_bar_chart(
    df_filtered,
    'Leetify_Rating',
    'Vergleich des Leetify Ratings',
    'Leetify Rating',
)

# 2. Aim Rating Vergleich
generate_bar_chart(
    df_filtered,
    'Aim_Rating',
    'Vergleich des Aim Ratings',
    'Aim Rating (Leetify Score)',
)

# 3. Utility Rating Vergleich
generate_bar_chart(
    df_filtered,
    'Utility_Rating',
    'Vergleich des Utility Ratings',
    'Utility Rating (Leetify Score)',
)

# 4. Opening Kill Success Vergleich
generate_bar_chart(
    df_filtered,
    'Opening_Kill_Success',
    'Vergleich des Opening Kill Success (Wert = Value x 1000)',
    'Opening Kill Success (Leetify Score)',
)

# 5. Positioning Rating Vergleich
generate_bar_chart(
    df_filtered,
    'Positioning_Rating',
    'Vergleich des Positioning Ratings',
    'Positioning Rating (Leetify Score)',
)

# Spezieller Fall: Clutch Percentage (wird als letztes hinzugefügt)
st.markdown("---")
st.subheader("Clutch Percentage")
st.markdown("Der Clutch Percentage ist ein entscheidender Wert für Spieler, die Runden in Unterzahl gewinnen können.")

generate_bar_chart(
    df_filtered,
    'Clutch_Percentage',
    'Vergleich des Clutch Percentage',
    'Clutch Percentage',
)

# --- ENDE DER STREAMLIT APP ---