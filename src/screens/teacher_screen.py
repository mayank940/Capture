import streamlit as st
from src.components.header import header_dashboard
from src.components.teacher_login_components import teacher_register_comp, teacher_login_comp
from src.components.teacher_portal import teacher_portal

def teacher_screen():

    col1, col2 = st.columns([0.68, 0.32] if st.session_state["is_logged_in"] else [58,42], vertical_alignment="bottom")

    with col1:
        header_dashboard()

    with col2:
        if st.button("Log out" if st.session_state["is_logged_in"] else "Go back to Home", shortcut="control+backspace", type="tertiary"):
            st.session_state["user_role"] = None
            st.session_state["is_logged_in"] = False
            st.session_state["login_type"] = "login"
            if "is_camera" in st.session_state:
                st.session_state["is_camera"] = False
            if "all_images" in st.session_state:
                st.session_state["all_images"] = []
            st.rerun()

    if st.session_state["is_logged_in"]:
        teacher_portal()
    else:
        match st.session_state["login_type"]:
            case "login":
                teacher_login_comp()
            case "register":
                teacher_register_comp()