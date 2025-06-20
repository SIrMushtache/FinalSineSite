import streamlit as st
from utils import read_global_limits, update_global_limits

def show_global_limits_page():
    st.title("Global Limits (Admin Only)")
    st.write("Edit and save to update all users' defaults.")

    limits = read_global_limits()
    updated_limits = {}

    for key, lims in limits.items():
        st.subheader(key)
        min_v = st.number_input(f"Min for {key}", value=lims['min'], key=f"min_{key}")
        max_v = st.number_input(f"Max for {key}", value=lims['max'], key=f"max_{key}")
        default_v = st.number_input(f"Default for {key}", value=lims['default'], key=f"default_{key}")
        updated_limits[key] = {"min": min_v, "max": max_v, "default": default_v}

    if st.button("Save All"):
        update_global_limits(updated_limits)
        st.success("Global limits updated!")
