import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from database.database import login, get_all_mata_kuliah
import halaman.dashboard as dashboard
import halaman.history as history
import halaman.mata_kuliah as mata_kuliah

# Konfigurasi cookies manager
cookies = EncryptedCookieManager(prefix="myapp_", password="adminprilly")
if not cookies.ready():
    st.stop()

# Fungsi logout
def logout():
    cookies["logged_in"] = ""
    cookies["username"] = ""
    cookies.save()
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# Fungsi login
def handle_login(username, password):
    user = login(username, password)  # Validasi dari database
    if user:
        cookies["logged_in"] = "True"
        cookies["username"] = username
        cookies.save()
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login berhasil!")
        st.rerun()
    else:
        st.error("Username atau password salah.")

# Restore session state dari cookies
if "logged_in" not in st.session_state:
    st.session_state.logged_in = cookies.get("logged_in", False) == "True"
if "username" not in st.session_state:
    st.session_state.username = cookies.get("username", None)

# Menggunakan CSS untuk sidebar
with open("styles.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Sidebar
# st.sidebar.markdown("<div class='sidebar'>", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.sidebar.markdown(f"<p class='welcome'>Selamat datang, {st.session_state.username}!</p>", unsafe_allow_html=True)

    # Navigasi manual tanpa radio button
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("📜 History"):
        st.session_state.page = "History"
    if st.sidebar.button("📚 Mata Kuliah"):
        st.session_state.page = "Mata Kuliah"
    if st.sidebar.button("🚪 Logout"):
        logout()

    # Menampilkan halaman sesuai pilihan
    page = st.session_state.get("page", "Dashboard")
    if page == "Dashboard":
        dashboard.show()
    elif page == "History":
        history.show()
    elif page == "Mata Kuliah":
        mata_kuliah.show()

else:
    with st.sidebar.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            handle_login(username, password)

    st.sidebar.info("Silakan login untuk mengakses menu.")

st.sidebar.markdown("</div>", unsafe_allow_html=True)