import datetime

import streamlit as st

from database.database import *
import numpy as np
import tempfile
import cv2
from ultralytics import YOLO
from collections import Counter, defaultdict
from utils import utils
import torch
from threading import Thread
from queue import Queue

# Inisialisasi session state
if 'activity_counts' not in st.session_state:
    st.session_state.activity_counts = defaultdict(int)
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'camera_index' not in st.session_state:
    st.session_state.camera_index = 0 #Default Main Camera
@st.cache_resource
def load_model():
    model = YOLO('yoloModel/model_yolo11_v5_trained.pt')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    model.half()
    return model

frame_queue = Queue(maxsize=10)

def process_frames():
    model = load_model()
    while True:
        if not frame_queue.empty():
            frame, is_video = frame_queue.get()
            if frame_queue.qsize() > 2:
                continue

            with torch.no_grad():
                results = model.predict(
                    frame,
                    imgsz=640,
                    half=True if torch.cuda.is_available() else False,
                    device=model.device,
                    verbose=False,
                    augment=False
                )

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls)
                    label = model.bames[class_id]
                    st.session_state.activity_counts[label] += 1

            annotated_frame = results[0].plot()
            if is_video:
                st.session_state.video_frame = annotated_frame
            else:
                st.session_state.camera_frame = annotated_frame
def list_available_cameras(max_to_check=3):
    """Deteksi kamera yang tersedia"""
    available = []
    for i in range(max_to_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

def analyze_engagement():
    categories = get_activity_list()

    engaged_categories = categories['terlibat']
    not_engaged_categories = categories['tidak_terlibat']

    engaged = sum(st.session_state.activity_counts.get(activity, 0) for activity in engaged_categories)
    not_engaged = sum(st.session_state.activity_counts.get(activity, 0) for activity in not_engaged_categories)

    return {
        "engaged": engaged,
        "not_engaged": not_engaged,
        "analysis": "Terlibat" if engaged > not_engaged else "Tidak Terlibat" if engaged < not_engaged else "Seimbang"
    }

def detect_activity(image):
    model = YOLO('model_yolo11_v5_trained.pt')
    results = model.predict(image)

    detected_activities = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            label = result.names[class_id]
            detected_activities.append(label)

    activity_counts = Counter(detected_activities)
    return analyze_engagement(activity_counts)


def process_video():
    # model = YOLO('model_yolo11_trained.pt')
    model = YOLO('yoloModel/model_yolo11_v5_trained.pt')
    cap = cv2.VideoCapture(st.session_state.video_path)
    frame_window = st.empty()

    while cap.isOpened() and st.session_state.processing:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, verbose=False)
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                label = model.names[class_id]
                st.session_state.activity_counts[label] += 1

        annotated_frame = results[0].plot()
        frame_window.image(annotated_frame, channels="BGR", use_column_width=True)

    cap.release()
    st.session_state.processing = False

def process_camera(camera_index):
    model = YOLO('yoloModel/model_yolo11_v5_trained.pt')
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            st.error(f"Tidak dapat mengakses kamera dengan index {camera_index}")
            return

        frame_placeholder = st.empty()

        while cap.isOpened() and st.session_state.processing:
            ret, frame = cap.read()
            if not ret:
                st.error("Gagal mengambil frame dari kamera")
                break

            results = model.predict(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls)
                    label = model.names[class_id]
                    st.session_state.activity_counts[label] += 1

            annotated_frame = results[0].plot()
            frame_placeholder.image(annotated_frame, channels="BGR", use_column_width=True)

    finally:
        cap.release()
        st.session_state.processing = False

def show():
    st.title("📊 Analisis Keterlibatan Kelas")

    # Bagian kontrol utama
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Pengaturan Analisis")
        class_list = get_mata_kuliah()
        selected_class = st.selectbox(
            "Pilih Mata Kuliah",
            list(class_list.keys()) if class_list else ["Belum ada mata kuliah"]
        )

        # Tombol simpan
        if st.button("💾 Simpan Hasil Analisis"):
            if sum(st.session_state.activity_counts.values()) > 0:
                analysis = analyze_engagement()
                id_monitoring = utils.hash_mata_kuliah(selected_class, datetime.datetime.now())
                save_analysis_result(
                    id_monitoring=id_monitoring,
                    class_code=selected_class,
                    engaged=analysis['engaged'],
                    not_engaged=analysis['not_engaged'],
                    analysis_result=analysis['analysis']
                )
                save_detail_analysis(id_monitoring, dict(st.session_state.activity_counts))
                st.success("Data berhasil disimpan!")
                st.session_state.activity_counts = defaultdict(int)
            else:
                st.warning("Tidak ada data untuk disimpan!")

    with col2:
        st.subheader("Input Video/Kamera")
        input_type = st.radio(
            "Pilih Sumber Input:",
            ["Upload Video", "Kamera Real-Time"],
            horizontal=True
        )

        if input_type == "Upload Video":
            uploaded_file = st.file_uploader(
                "Pilih file video",
                type=["mp4", "avi", "mov"]
            )
            if uploaded_file:
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                st.session_state.video_path = tfile.name

        else:
            available_cameras = list_available_cameras()
            camera_options = {f"Kamera {i}": i for i in available_cameras}

            if not available_cameras:
                st.warning("Tidak ada kamera yang terdeteksi!")
            else:
                selected_cam = st.selectbox(
                    "Pilih Perangkat Kamera:",
                    options=list(camera_options.keys()),
                    index=0
                )
                st.session_state.camera_index = camera_options[selected_cam]

        # Kontrol pemrosesan
        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("▶️ Mulai Pemrosesan" if not st.session_state.processing else "⏸️ Sedang Memproses"):
                if not st.session_state.processing:
                    st.session_state.processing = True
                    st.session_state.activity_counts = defaultdict(int)

                    if input_type == "Upload Video" and st.session_state.video_path:
                        process_video()
                        # Thread(target=process_video, daemon=True).start()

                    elif input_type == "Kamera Real-Time":
                        process_camera(st.session_state.camera_index)
                        # Thread(target=process_camera, args=(st.session_state.camera_index,), daemon=True).start()

        with col_stop:
            if st.button("⏹️ Hentikan Pemrosesan"):
                st.session_state.processing = False

    # Tampilkan hasil real-time
    if st.session_state.processing:
        st.subheader("Hasil Real-Time")

        col_result1, col_result2 = st.columns(2)
        categories = get_activity_list()

        with col_result1:
            st.markdown("### ✅ Aktivitas Terlibat")
            if not categories['terlibat']:
                st.info("Belum ada aktivitas terlibat terdefinisi")
            else:
                for activity in categories['terlibat']:
                    count = st.session_state.activity_counts.get(activity, 0)
                    st.metric(label=activity, value=count)

        with col_result2:
            st.markdown("### ❌ Aktivitas Tidak Terlibat")
            if not categories['tidak_terlibat']:
                st.info("Belum ada aktivitas tidak terlibat terdefinisi")
            else:
                for activity in categories['tidak_terlibat']:
                    count = st.session_state.activity_counts.get(activity, 0)
                    st.metric(label=activity, value=count)

        analysis = analyze_engagement()
        st.markdown("---")
        st.markdown(f"### 🔍 Kesimpulan Keterlibatan")
        st.markdown(f"**Terlibat**: {analysis['engaged']} | **Tidak Terlibat**: {analysis['not_engaged']}")

        if analysis['analysis'] == "Terlibat":
            st.success(f"✅ KELAS TERLIBAT ({analysis['engaged']} vs {analysis['not_engaged']})")
        elif analysis['analysis'] == "Tidak Terlibat":
            st.error(f"❌ KELAS TIDAK TERLIBAT ({analysis['engaged']} vs {analysis['not_engaged']})")
        else:
            st.warning(f"⚖️ SEIMBANG ({analysis['engaged']} vs {analysis['not_engaged']})")
