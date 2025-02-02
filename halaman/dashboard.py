import streamlit as st

from database.database import *
import numpy as np
import tempfile
import cv2
from ultralytics import YOLO
from collections import Counter

def analyze_engagement(activity_counts):
    engaged_categories = ['Raising Hand', 'Writing', 'Looking Forward']
    not_engaged_categories = ['Sleeping', 'Playing Handphone', 'Turning Around']

    engaged = sum(activity_counts.get(activity, 0) for activity in engaged_categories)
    not_engaged = sum(activity_counts.get(activity, 0) for activity in not_engaged_categories)

    if engaged > not_engaged:
        analysis = "Terlibat"
    elif engaged < not_engaged:
        analysis = "Tidak Terlibat"
    else:
        analysis = "Seimbang"

    return {
        "engaged": engaged,
        "not_engaged": not_engaged,
        "analysis": analysis,
        "details": activity_counts
    }

def detect_activity(image):
    model = YOLO('model_yolo11_trained.pt')
    results = model.predict(image)
    activity_data = {}
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            label = model.names[class_id]
            if label not in activity_data:
                activity_data[label] = {"count": 0, "total_confidence": 0.0}

            activity_data[label]['count'] += 1
            activity_data[label]['total_confidence'] += confidence

        activity_summary = []
        for activity, data in activity_data.items():
            avg_confidence = data["total_confidence"] / data["count"]
            activity_summary.append({
                "activity": activity,
                "count": data["count"],
                "avg_confidence": avg_confidence
            })

        detected_activities = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                label = result.names[class_id]
                detected_activities.append(label)

        activity_counts = Counter(detected_activities)
    return analyze_engagement(activity_counts)

def show():
    st.title("🏠 Dashboard")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Pilih Mata Kuliah")
        class_list = get_mata_kuliah()

        if not class_list:
            st.warning("Belum ada mata kuliah tersedia.")
            return

        selected_class = st.selectbox("Mata Kuliah", list(class_list.keys()))

    with col2:
        st.subheader("Upload Gambar / Kamera")

        option = st.radio("Pilih Input:", ["Upload Image", "Gunakan Kamera"], horizontal=True)

        uploaded_file = None
        image = None

        if option == "Upload Image":
            uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])

            if uploaded_file is not None:
                image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        elif option == "Gunakan Kamera":
            camera_image = st.camera_input("Ambil Gambar")

            if camera_image is not None:
                image = np.array(bytearray(camera_image.read()), dtype=np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if image is not None:
            st.image(image, caption="Gambar yang diunggah", use_column_width=True)

            # Simpan sementara untuk analisis
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                cv2.imwrite(temp_file.name, image)
                results = detect_activity(temp_file.name)

                if results:
                    st.subheader("Hasil Deteksi")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Kategori Terlibat:**")
                        st.write(f"- Raising Hand: {results['details'].get('Raising Hand', 0)}")
                        st.write(f"- Writing: {results['details'].get('Writing', 0)}")
                        st.write(f"- Looking Forward: {results['details'].get('Looking Forward', 0)}")
                        st.markdown(f"**Total Terlibat:** {results['engaged']}")

                    with col2:
                        st.markdown("**Kategori Tidak Terlibat:**")
                        st.write(f"- Sleeping: {results['details'].get('Sleeping', 0)}")
                        st.write(f"- Playing Handphone: {results['details'].get('Playing Handphone', 0)}")
                        st.write(f"- Turning Around: {results['details'].get('Turning Around', 0)}")
                        st.markdown(f"**Total Tidak Terlibat:** {results['not_engaged']}")

                    st.subheader("Hasil Analisis Keterlibatan:")
                    if results['engaged'] == 0 and results['not_engaged'] == 0:
                        st.warning("Tidak ada aktivitas terdeteksi")
                    else:
                        engagement_status = results['analysis']
                        if engagement_status == "Terlibat":
                            st.success(
                                f"✅ KELAS TERLIBAT (Total: {results['engaged']} vs {results['not_engaged']})")
                        elif engagement_status == "Tidak Terlibat":
                            st.error(
                                f"❌ KELAS TIDAK TERLIBAT (Total: {results['engaged']} vs {results['not_engaged']})")
                        else:
                            st.warning(
                                f"⚖️ SEIMBANG (Total: {results['engaged']} vs {results['not_engaged']})")
                    # for entry in results:
                    #     st.write(
                    #         f"- **{entry['activity']}**: {entry['count']} orang (Keyakinan rata-rata: {entry['avg_confidence']:.2f})")

                else:
                    st.warning("Tidak ada kegiatan terdeteksi")