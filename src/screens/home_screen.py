import streamlit as st
from src.components.header import header_home
from src.ui.style_home_screen import style_home_screen

def home_screen():
    header_home()
    style_home_screen()
    
    st.header("Welcome to the capture!", text_alignment="center")
    st.subheader("Continue by logging in:", text_alignment="center")
    st.space()
    st.space()

    col1, col2 = st.columns(2, gap ="xlarge")

    with col1:
        st.header("I'm a Student")
        st.image("images/student.png", width= 100)
        if st.button("Student Login", type="primary", icon = ":material/arrow_outward:", icon_position= "right"):
            st.session_state["user_role"] = "student"
            st.rerun()

    with col2: 
        st.header("I'm a teacher")
        st.image("images/professor.png", width=100)
        if st.button("Teacher Login", type="primary", icon=":material/arrow_outward:", icon_position = "right"):
            st.session_state["user_role"] = "teacher"
            st.rerun()  

    st.space()
    with st.container(width="stretch", border=True, horizontal=True, vertical_alignment="center", horizontal_alignment="center"):
        st.image("images/authority.png", width=80)
        st.header("I'm an authorized person")
        if st.button("Login", icon=":material/arrow_outward:", type="primary"):
            st.session_state["user_role"] = "authority"
            st.rerun()
