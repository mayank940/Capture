import streamlit as st
from src.components.header import header_dashboard
from src.components.student_login_components import student_login_comp, student_register_comp
from src.components.student_portal import student_portal

def student_screen():

    col1, col2 = st.columns(2, vertical_alignment="bottom", gap="medium")
    
    with col1:
        header_dashboard()

    with col2:
        if st.button("Go back to Home screen", shortcut="control+backspace", type="tertiary"):
            st.session_state["user_role"] = None
            st.session_state["is_logged_in"] = False
            st.session_state["login_type"] = "login"
            st.rerun()


    if st.session_state["is_logged_in"]:
        student_portal()
    else:
        match st.session_state["login_type"]:
            case "login":
                student_login_comp()
            case "register":
                student_register_comp()