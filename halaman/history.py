import streamlit as st
from database.database import *
import plotly.express as px
import pandas as pd

def show():
    st.title("📜 History")

    # 1. Ambil data monitoring
    df_monitoring = get_monitoring_data()

    # 2. Buat display_id untuk tampilan (menggabungkan date & class_code)
    df_monitoring["display_id"] = df_monitoring.apply(
        lambda row: f"{row['date']} - {row['class_code']}", axis=1
    )

    st.write("Tabel Monitoring:")
    st.dataframe(
        df_monitoring[["date", "class_code", "display_id", "count_engage", "count_not_engage", "analysis"]],
        use_container_width=True
    )

    # 3. Mapping display_id -> id_monitoring
    display_id_to_full_id = dict(zip(df_monitoring["display_id"], df_monitoring["id_monitoring"]))

    # 4. Pilih Monitoring
    selected_display_id = st.selectbox("Pilih Monitoring", df_monitoring["display_id"].tolist())

    # 5. Jika ada pilihan, tampilkan detail analysis
    if selected_display_id:
        real_id = display_id_to_full_id[selected_display_id]
        df_detail = get_detail_monitoring(real_id)
        st.subheader(f"Detail Analysis untuk {selected_display_id}")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_detail[["activity", "activity_count"]], use_container_width=True)
        with col2:
            if not df_detail.empty:
                fig = px.pie(
                    df_detail,
                    values='activity_count',
                    names='activity',
                    title='Persentase Activity'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Tidak ada data detail untuk monitoring ini.")

    st.markdown("---")
    st.subheader("Trend Aktif & Tidak Aktif Mahasiswa Berdasarkan Mata Kuliah")

    # 6. Pilih mata kuliah untuk trend
    courses = sorted(df_monitoring["class_code"].unique())
    selected_course = st.selectbox("Pilih Mata Kuliah untuk Trend", courses)

    # 7. Filter data monitoring sesuai mata kuliah
    trend_df = df_monitoring[df_monitoring["class_code"] == selected_course].copy()

    # 8. Pastikan kolom date dalam format datetime
    trend_df["date"] = pd.to_datetime(trend_df["date"])

    # 9. Grouping dan aggregasi data berdasarkan tanggal
    trend_df = trend_df.groupby("date", as_index=False).agg({
        "count_engage": "sum",
        "count_not_engage": "sum"
    })

    # 10. Urutkan berdasarkan tanggal
    trend_df.sort_values("date", inplace=True)

    # 11. Buat kolom string untuk tanggal agar sumbu x hanya menampilkan tanggal yang ada
    trend_df["date_str"] = trend_df["date"].dt.strftime('%Y-%m-%d')

    # 12. Buat DataFrame untuk Plotly dengan melt (mengubah format wide ke long)
    plot_df = trend_df.melt(
        id_vars=["date_str"],
        value_vars=["count_engage", "count_not_engage"],
        var_name="status",
        value_name="count"
    )

    # 13. Tampilkan grafik line chart
    if not trend_df.empty:
        fig_trend = px.line(
            plot_df,
            x="date_str",
            y="count",
            color="status",
            title=f"Trend Aktif & Tidak Aktif Mahasiswa untuk {selected_course}",
            labels={
                "count": "Jumlah Mahasiswa",
                "status": "Status",
                "date_str": "Tanggal"
            }
        )

        # Atur sumbu x sebagai kategori, sehingga hanya tanggal yang ada ditampilkan
        fig_trend.update_layout(
            xaxis=dict(
                type='category'
            )
        )

        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.write("Tidak ada data trend untuk mata kuliah ini.")
