import streamlit as st
from database.database import *
import plotly.express as px

def show():
    st.title("📜 History")

    df_monitoring = get_monitoring_data()

    df_monitoring["display_id"] = df_monitoring.apply(
        lambda row: f"{row['date']} - {row['class_code']}", axis=1
    )

    # 3. Tampilkan tabel monitoring tanpa menampilkan id hash
    st.write("Tabel Monitoring:")
    st.dataframe(df_monitoring[["date", "class_code", "display_id", "count_engage", "count_not_engage", "analysis"]], use_container_width=True)

    # 4. Mapping dari display_id ke id hash asli untuk referensi backend
    display_id_to_full_id = dict(zip(df_monitoring["display_id"], df_monitoring["id_monitoring"]))

    # 5. Buat selectbox untuk memilih monitoring berdasarkan display_id
    selected_display_id = st.selectbox("Pilih Monitoring", df_monitoring["display_id"].tolist())

    # 6. Jika ada pilihan, ambil id hash asli dan tampilkan detail analysis
    if selected_display_id:
        real_id = display_id_to_full_id[selected_display_id]
        df_detail = get_detail_monitoring(real_id)
        st.subheader(f"Detail Analysis untuk {selected_display_id}")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_detail[["activity", "activity_count"]], use_container_width=True)

        with col2:
            if not df_detail.empty:
                # Buat pie chart menggunakan Plotly Express
                fig = px.pie(
                    df_detail,
                    values='activity_count',
                    names='activity',
                    title='Persentase Activity'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Tidak ada data detail untuk monitoring ini.")