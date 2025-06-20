import streamlit as st
from page_generator import show_generator_page
from page_gallery import show_gallery_page
from page_local_limits import show_local_limits_page
from page_global_limits import show_global_limits_page
from page_batch_upload import show_batch_upload_page

st.set_page_config(page_title="Sinewave Generator", layout="wide")

PAGES = {
    "Generator": show_generator_page,
    "Gallery": show_gallery_page,
    "Local Limits": show_local_limits_page,
    "Global Limits": show_global_limits_page,
    "Batch Uploader": show_batch_upload_page,
}

PASSWORD = "your_password_here"  # Change this!

def password_protected_page(show_page_func, page_name):
    if "auth" not in st.session_state:
        st.session_state.auth = {}
    if page_name not in st.session_state.auth:
        pwd = st.text_input(f"Enter password to access '{page_name}'", type="password")
        if st.button("Login", key=f"login_{page_name}"):
            if pwd == PASSWORD:
                st.session_state.auth[page_name] = True
                st.success("Access granted.")
                st.experimental_rerun()
            else:
                st.error("Incorrect password")
        return
    show_page_func()

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection in ["Global Limits", "Batch Uploader"]:
    password_protected_page(PAGES[selection], selection)
else:
    PAGES[selection]()
