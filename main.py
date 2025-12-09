import streamlit as st

rating_page = st.Page("rating.py", title="IB Leetify Rating", icon="📉")
duell_page = st.Page("duell_stats.py", title="IB Leetify Trade Rating", icon="🤼")
trade_page = st.Page("trade_stats.py", title="IB Leetify Trade Rating", icon="🔄")
flash_page = st.Page("flash_stats.py", title="IB Leetify Flash Stats", icon="👨‍🦯")
he_page = st.Page("he_stats.py", title="IB Leetify HE Stats", icon="💥")


pg = st.navigation([rating_page, duell_page, trade_page, flash_page, he_page])
st.set_page_config(page_title="Iron Blow Schwanzvergleich", page_icon=":material/edit:")




pg.run()
