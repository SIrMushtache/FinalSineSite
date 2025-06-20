import streamlit as st
import numpy as np
import random
import gspread
from google.oauth2.service_account import Credentials

GSHEET_CREDENTIALS = '/mnt/data/sinewavegen-b27f10e94af8.json'
GSHEET_ID = '1X8I-b05FxHFz_fOCadtt9EKbFghJlrz77KUpDFDlzQ4'
LIMITS_SHEET = 'Limits'

def get_gsheet_client():
    creds = Credentials.from_service_account_file(
        GSHEET_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    return gc

def read_global_limits():
    gc = get_gsheet_client()
    sh = gc.open_by_key(GSHEET_ID)
    ws = sh.worksheet(LIMITS_SHEET)
    data = ws.get_all_records()
    limits = {}
    for row in data:
        key = row["key"]
        vtype = type(row["default"])
        # Support bool, int, float
        if isinstance(row["default"], str):
            if row["default"].lower() == "true":
                row["default"] = True
            elif row["default"].lower() == "false":
                row["default"] = False
            else:
                try:
                    row["default"] = float(row["default"])
                except:
                    pass
        limits[key] = {
            "min": boolify(row["min"]) if is_bool_str(row["default"]) else float(row["min"]),
            "max": boolify(row["max"]) if is_bool_str(row["default"]) else float(row["max"]),
            "default": row["default"],
        }
    return limits

def update_global_limits(new_limits):
    gc = get_gsheet_client()
    sh = gc.open_by_key(GSHEET_ID)
    ws = sh.worksheet(LIMITS_SHEET)
    values = [["key", "min", "max", "default"]]
    for key, lims in new_limits.items():
        values.append([
            key,
            lims["min"],
            lims["max"],
            lims["default"]
        ])
    ws.update('A1', values)

def boolify(x):
    if isinstance(x, bool):
        return x
    if isinstance(x, str):
        return x.lower() == "true"
    if isinstance(x, (int, float)):
        return bool(x)
    return False

def is_bool_str(x):
    return str(x).lower() in ['true', 'false']

def sine_on_circle(
    points=500,
    radius=7.0,
    amp=2.0,
    freq=5.0,
    phase=0.0,
    center_offset_amp=0.0,
    center_offset_freq=1.0,
    center_offset_phase=0.0,
    center_offset_radius=0.0,
    abs_sine=False
):
    t = np.linspace(0, 2 * np.pi, points)
    cx = center_offset_amp * np.cos(center_offset_freq * t + center_offset_phase)
    cy = center_offset_amp * np.sin(center_offset_freq * t + center_offset_phase)
    if center_offset_radius != 0:
        cx += center_offset_radius * np.cos(t)
        cy += center_offset_radius * np.sin(t)
    main_sine = np.sin(freq * t + phase)
    if abs_sine:
        main_sine = np.abs(main_sine)
    r = radius + amp * main_sine
    x = cx + r * np.cos(t)
    y = cy + r * np.sin(t)
    return x, y

def randomize_parameters(limits):
    for key, lim in limits.items():
        if isinstance(lim["default"], bool):
            st.session_state[key] = random.choice([True, False])
        elif isinstance(lim["default"], int):
            st.session_state[key] = random.randint(int(lim["min"]), int(lim["max"]))
        elif isinstance(lim["default"], float):
            st.session_state[key] = random.uniform(lim["min"], lim["max"])

def reset_parameters(limits):
    for key, lim in limits.items():
        st.session_state[key] = lim["default"]

def slider_with_text(label, key, min_value, max_value, value, step=None, format=None):
    c1, c2 = st.columns([3, 1])
    # Check int or float
    if isinstance(value, int):
        slider = c1.slider(label, min_value, max_value, value, step=step or 1, key=f"slider_{key}")
        text = c2.number_input("", min_value=min_value, max_value=max_value, value=st.session_state.get(f"slider_{key}", value), step=step or 1, key=f"num_{key}")
    else:
        slider = c1.slider(label, min_value, max_value, value, step=step or 0.01, format=format or "%.2f", key=f"slider_{key}")
        text = c2.number_input("", min_value=min_value, max_value=max_value, value=st.session_state.get(f"slider_{key}", value), step=step or 0.01, format=format or "%.2f", key=f"num_{key}")

    # Sync logic
    if st.session_state.get(f"slider_{key}") != st.session_state.get(f"num_{key}"):
        st.session_state[f"slider_{key}"] = st.session_state[f"num_{key}"]
        st.session_state[key] = st.session_state[f"num_{key}"]
    else:
        st.session_state[key] = st.session_state[f"slider_{key}"]

    return st.session_state[key]
