import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils import sine_on_circle, slider_with_text, randomize_parameters, reset_parameters
from page_local_limits import get_local_limits

def show_generator_page():
    st.title("Sine on a Circle Generator")
    lims = get_local_limits()

    lims["abs_sine"] = {"min": False, "max": True, "default": False}
    lims["enable_center_wobble"] = {"min": False, "max": True, "default": True}

    for key, lim in lims.items():
        if key not in st.session_state:
            st.session_state[key] = lim["default"]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Randomize All"):
            randomize_parameters(lims)
            st.experimental_rerun()
    with col2:
        if st.button("🔄 Reset All"):
            reset_parameters(lims)
            st.experimental_rerun()

    st.sidebar.header("General")
    points = slider_with_text("Points", "points", int(lims["points"]["min"]), int(lims["points"]["max"]), int(st.session_state["points"]), step=1)
    copies = slider_with_text("Copies", "copies", int(lims["copies"]["min"]), int(lims["copies"]["max"]), int(st.session_state["copies"]), step=1)

    st.sidebar.markdown("### Main Wave")
    freq = slider_with_text("Frequency", "freq", lims["freq"]["min"], lims["freq"]["max"], st.session_state["freq"], step=0.01, format="%.2f")
    freq_offset = slider_with_text("Frequency Offset", "freq_offset", lims["freq_offset"]["min"], lims["freq_offset"]["max"], st.session_state["freq_offset"], step=0.01, format="%.2f")
    amp = slider_with_text("Amplitude", "amp", lims["amp"]["min"], lims["amp"]["max"], st.session_state["amp"], step=0.01, format="%.2f")
    amp_offset = slider_with_text("Amplitude Offset", "amp_offset", lims["amp_offset"]["min"], lims["amp_offset"]["max"], st.session_state["amp_offset"], step=0.01, format="%.2f")
    radius = slider_with_text("Radius", "radius", lims["radius"]["min"], lims["radius"]["max"], st.session_state["radius"], step=0.01, format="%.2f")
    radius_offset = slider_with_text("Radius Offset", "radius_offset", lims["radius_offset"]["min"], lims["radius_offset"]["max"], st.session_state["radius_offset"], step=0.01, format="%.2f")
    phase = slider_with_text("Phase", "phase", lims["phase"]["min"], lims["phase"]["max"], st.session_state["phase"], step=0.01, format="%.2f")
    phase_offset = slider_with_text("Phase Offset", "phase_offset", lims["phase_offset"]["min"], lims["phase_offset"]["max"], st.session_state["phase_offset"], step=0.01, format="%.2f")

    st.sidebar.markdown("### Center Offset")
    center_freq = slider_with_text("Center Frequency", "center_freq", lims["center_freq"]["min"], lims["center_freq"]["max"], st.session_state["center_freq"], step=0.01, format="%.2f")
    center_freq_offset = slider_with_text("Center Frequency Offset", "center_freq_offset", lims["center_freq_offset"]["min"], lims["center_freq_offset"]["max"], st.session_state["center_freq_offset"], step=0.01, format="%.2f")
    center_amp = slider_with_text("Center Amplitude", "center_amp", lims["center_amp"]["min"], lims["center_amp"]["max"], st.session_state["center_amp"], step=0.01, format="%.2f")
    center_amp_offset = slider_with_text("Center Amplitude Offset", "center_amp_offset", lims["center_amp_offset"]["min"], lims["center_amp_offset"]["max"], st.session_state["center_amp_offset"], step=0.01, format="%.2f")
    center_radius = slider_with_text("Center Radius", "center_radius", lims["center_radius"]["min"], lims["center_radius"]["max"], st.session_state["center_radius"], step=0.01, format="%.2f")
    center_radius_offset = slider_with_text("Center Radius Offset", "center_radius_offset", lims["center_radius_offset"]["min"], lims["center_radius_offset"]["max"], st.session_state["center_radius_offset"], step=0.01, format="%.2f")
    center_phase = slider_with_text("Center Phase", "center_phase", lims["center_phase"]["min"], lims["center_phase"]["max"], st.session_state["center_phase"], step=0.01, format="%.2f")
    center_phase_offset = slider_with_text("Center Phase Offset", "center_phase_offset", lims["center_phase_offset"]["min"], lims["center_phase_offset"]["max"], st.session_state["center_phase_offset"], step=0.01, format="%.2f")

    abs_sine = st.sidebar.checkbox("Absolute Sine", value=st.session_state["abs_sine"], key="abs_sine")
    enable_center = st.sidebar.checkbox("Enable Center Wobble", value=st.session_state["enable_center_wobble"], key="enable_center_wobble")

    fig, ax = plt.subplots(figsize=(6, 6))
    for i in range(copies):
        main_freq = freq + freq_offset * i
        main_amp = amp + amp_offset * i
        main_radius = radius + radius_offset * i
        main_phase = phase + phase_offset * i
        if enable_center:
            cent_freq = center_freq + center_freq_offset * i
            cent_amp = center_amp + center_amp_offset * i
            cent_radius = center_radius + center_radius_offset * i
            cent_phase = center_phase + center_phase_offset * i
        else:
            cent_freq = 0.0
            cent_amp = 0.0
            cent_radius = 0.0
            cent_phase = 0.0
        x, y = sine_on_circle(
            points=points,
            radius=main_radius,
            amp=main_amp,
            freq=main_freq,
            phase=main_phase,
            center_offset_amp=cent_amp,
            center_offset_freq=cent_freq,
            center_offset_phase=cent_phase,
            center_offset_radius=cent_radius,
            abs_sine=abs_sine
        )
        ax.plot(x, y, alpha=0.7, lw=2)
    ax.set_aspect('equal')
    ax.axis("off")
    st.pyplot(fig)
