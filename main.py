import streamlit as st

rating_page = st.Page("rating.py", title="Leetify Rating", icon="📉")
aim_page = st.Page("aim_stats.py", title="Leetify Aim Rating", icon="💯")
duell_page = st.Page("duell_stats.py", title="Leetify Duell Rating", icon="🤼")
trade_page = st.Page("trade_stats.py", title="Leetify Trade Rating", icon="🔄")
flash_page = st.Page("flash_stats.py", title="Leetify Flash Stats", icon="👨‍🦯")
he_page = st.Page("he_stats.py", title="IB Leetify HE Stats", icon="💥")


pg = st.navigation([rating_page, aim_page, duell_page, trade_page, flash_page, he_page])
st.set_page_config(page_title="CS2 Schwanzvergleich dataDate: 30.01.2026 16:00", page_icon=":material/edit:")




pg.run()
