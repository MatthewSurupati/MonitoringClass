import streamlit as st
from database.database import *

def show():
    st.title("📚 Mata Kuliah")
    st.title("Daftar Mata Kuliah")

    # Tombol tambah mata kuliah
    if st.button("➕ Tambah Mata Kuliah"):
        st.session_state["add_mode"] = True  # Aktifkan mode tambah

    # Jika sedang menambah mata kuliah, tampilkan form
    if st.session_state.get("add_mode", False):
        with st.form("add_form"):
            new_name = st.text_input("Nama Mata Kuliah Baru", key="new_mk")
            new_code = st.text_input("Kode Mata Kuliah Baru", key="new_mk_code")
            submitted = st.form_submit_button("Simpan")

            if submitted and new_name.strip() and new_code.strip():
                add_mata_kuliah(new_code, new_name)  # Simpan ke database
                st.session_state["success_message"] = f"Mata kuliah '{new_name}' berhasil ditambahkan!"
                st.session_state["add_mode"] = False  # Keluar dari mode tambah
                st.rerun()

    classes = get_all_mata_kuliah()

    if not classes:
        st.warning("Belum ada mata kuliah yang terdaftar.")
        return

    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = None

    # Tampilkan tabel dengan tombol Edit dan Delete
    for cls in classes:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])

        with col1:
            st.text(cls["class_code"])

        with col2:
            st.text(cls["class_name"])

        with col3:
            if st.button("✏ Edit", key=f"edit_{cls['id_class']}"):
                st.session_state["edit_mode"] = cls["id_class"]
                # edit_mata_kuliah(cls["id_class"], cls["class_name"])
                st.rerun()

        with col4:
            if st.button("🗑 Delete", key=f"delete_{cls['id_class']}"):
                delete_mata_kuliah(cls["id_class"])
                st.rerun()  # Refresh halaman setelah hapus
    if st.session_state["edit_mode"] is not None:
        id_class = st.session_state["edit_mode"]
        class_to_edit = next((cls for cls in classes if cls["id_class"] == id_class), None)

        if class_to_edit:
            edit_mata_kuliah(class_to_edit["id_class"], class_to_edit["class_name"])

def edit_mata_kuliah(id_class, old_name):
    with st.form(f"edit_form_{id_class}"):
        new_name = st.text_input("Nama Mata Kuliah", value=old_name, key=f"name_{id_class}")
        submitted = st.form_submit_button("Simpan")

        if submitted and new_name.strip():
            update_mata_kuliah(id_class, new_name)
            st.session_state["success_message"] = f"Mata kuliah '{old_name}' telah diperbarui menjadi '{new_name}'."
            st.session_state["edit_mode"] = None  # Keluar dari mode edit
            st.rerun()

# Menampilkan pesan sukses setelah rerun
if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]