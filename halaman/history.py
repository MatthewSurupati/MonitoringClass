import streamlit as st
from database.database import *

def show():
    st.title("📜 History")

    df_monitoring = get_monitoring_data()

    st.write("Klik pada baris untuk mendapatkan detail Analysis")
    selected_row = st.dataframe(df_monitoring, use_container_width=True)

    id_monitoring = st.selectbox('Pilih Monitoring ID', df_monitoring['id_monitoring'].tolist())

    if id_monitoring:
        df_detail = get_detail_monitoring(id_monitoring)
        st.subheader(f"Detail Analysis Monitoring ID: {id_monitoring}")
        st.dataframe(df_detail, use_container_width=True)
