import streamlit as st
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout
from src.ui.style_management_screen import style_management_screen
from src.components.authority_portal_ops import subject_comp, teachers_comp, lectures_comp
import time

def management_screen():
    style_management_screen()

    if "auth_nav_page" not in st.session_state:
        st.session_state["auth_nav_page"] = "subject"

    col_ratio = [67, 33] if st.session_state["is_logged_in"] else [57, 43]
    col1, col2 = st.columns(col_ratio, vertical_alignment="bottom")

    with col1:
        header_dashboard()

    back_text = "Log Out" if st.session_state["is_logged_in"] else"Go to Home screen"
    if col2.button(back_text, type="tertiary", shortcut="control+backspace"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_role"] = None
        st.rerun()

    type1 = "primary" if st.session_state["auth_nav_page"] == "subject" else "secondary"
    type2 = "primary" if st.session_state["auth_nav_page"] == "teachers" else "secondary"
    type3 = "primary" if st.session_state["auth_nav_page"] == "lectures" else "secondary"

    st.space("medium")
    navs = st.columns(3)

    if navs[0].button("Subjects", type=type1, width="stretch"):
        st.session_state["auth_nav_page"] = "subject"
        st.rerun()

    if navs[1].button("Teachers", type=type2, width="stretch"):
        st.session_state["auth_nav_page"] = "teachers"
        st.rerun()

    if navs[2].button("Lectures", type=type3, width="stretch"):
        st.session_state["auth_nav_page"] = "lectures"
        st.rerun()

    st.divider()

    match st.session_state["auth_nav_page"]:
        case "subject":
            subject_comp()
        case "teachers":
            teachers_comp()
        case "lectures":
            lectures_comp()

def verify_admin():

    if st.session_state["is_logged_in"]:
        management_screen()
    else:

        style_base_layout()
        col1, col2 = st.columns([57, 43], vertical_alignment="bottom")

        with col1:
            header_dashboard()

        if col2.button("Go back to Home", type="tertiary", shortcut="control+backspace"):
            st.session_state["user_role"] = None
            st.rerun()

        st.divider()

        st.space()
        st.header("Enter authority verification password", text_alignment="center")
        st.space("medium")
        authority_pass = "37002461"


        password = st.text_input("password", type="password", placeholder="Enter password", label_visibility="hidden")

        if password:
            if password == authority_pass:
                st.session_state["is_logged_in"] = True
                st.success("Welcome to the admin's page")
                time.sleep(2)
                st.rerun()
            else:
                st.space()
                st.error("Incorrect password")
