import streamlit as st
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout
from src.ui.style_management_screen import style_management_screen
from src.components.authority_portal_ops import subject_comp, teachers_comp, lectures_comp

def management_screen():
    style_management_screen()

    if "auth_nav_page" not in st.session_state:
        st.session_state["auth_nav_page"] = "subject"

    col1, col2 = st.columns(2, vertical_alignment="bottom")

    with col1:
        header_dashboard()

    if col2.button("Go to Home screen", type="tertiary", shortcut="control+backspace"):
        st.session_state["user_role"] = None
        st.rerun()

    type1 = "primary" if st.session_state["auth_nav_page"] == "subject" else "secondary"
    type2 = "primary" if st.session_state["auth_nav_page"] == "teachers" else "secondary"
    type3 = "primary" if st.session_state["auth_nav_page"] == "lectures" else "secondary"

    st.space()
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