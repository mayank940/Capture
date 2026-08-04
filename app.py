import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.screens.management import management_screen

def main():
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    if "is_logged_in" not in st.session_state:
        st.session_state["is_logged_in"] = False

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = "login"

    match st.session_state["user_role"]:
        case "teacher":
            teacher_screen()
        case "student":
            student_screen()
        case "authority":
            management_screen()
        case None: 
            home_screen()

main()