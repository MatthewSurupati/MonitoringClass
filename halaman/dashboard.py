import streamlit as st
import torch.hub

from database import *
import numpy as np
import tempfile
import cv2

def detect_activity(image):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    result = model(image)
    return result.pandas().xyxy[0]
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
                result = detect_activity(temp_file.name)

            st.subheader("Hasil Deteksi")
            st.write(result)