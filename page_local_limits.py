import streamlit as st
from utils import read_global_limits

def get_local_limits():
    return read_global_limits()

def show_local_limits_page():
    st.title("Local Limits")
    limits = get_local_limits()
    st.write("Current session limits (copied from global limits):")
    for key, lims in limits.items():
        st.write(f"**{key}**: min={lims['min']}, max={lims['max']}, default={lims['default']}")
