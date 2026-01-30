import streamlit as st
import plotly.express as px
from data_handling import get_all_aim_stats


@st.cache_data
def load_data():
    """Lädt die Leetify-Daten einmalig und cached sie."""
    # Verwenden Sie hier Ihre Datenladefunktion
    return get_all_aim_stats()


df_stats = load_data()

player_options = df_stats['Name'].unique().tolist()

RADAR_METRICS = [
    'accuracy_enemy_spotted',
    'counter_strafing_good_shots_ratio',
    'reaction_time_ms',
    'spray_accuracy',
    'preaim',
]

PERCENTAGE_COLS = []


st.title("💯Leetify Aim Statistiken")
st.markdown("---")


selected_players = st.multiselect(
    "Wähle die Spieler für den Vergleich:",
    options=player_options,
    default=player_options,
)

if not selected_players:
    st.warning("Bitte wähle mindestens einen Spieler aus, um die Statistiken anzuzeigen.")
    st.stop()

df_filtered = df_stats[df_stats['Name'].isin(selected_players)].copy()


st.header("Vergleich der Spieler Rating Leetify (Radar Chart)")
if not df_filtered.empty:

    df_scaled = df_filtered.copy()
    for col in PERCENTAGE_COLS:
        df_scaled[col] = df_scaled[col] * 100

    df_long = df_scaled.melt(
        id_vars=['Name'],
        value_vars=RADAR_METRICS,
        var_name='Metric2',
        value_name='Score'
    )

    fig_radar = px.line_polar(
        df_long,
        r='Score',
        theta='Metric2',
        color='Name',
        line_close=True,
        title="Vergleich der Spielerleistungen auf Basis der Leetify-Statistiken"
    )

    fig_radar.update_traces(fill='toself', opacity=0.5)
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        legend_title_text='Spieler'
    )

    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
st.subheader("Detailvergleiche (Bar Charts)")


def generate_bar_chart(df, y_col, title, y_label):
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


# bar charts automatisch machen
for metric in RADAR_METRICS:
    generate_bar_chart(
        df_filtered,
        metric, metric, metric
    )
