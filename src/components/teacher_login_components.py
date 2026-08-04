import streamlit as st
from src.ui.style_teacher_screen import style_teacher_login_comps, remove_focus
from src.database.db import check_teacher_exists, create_teacher, get_teacher_cred
import time

def teacher_register_comp():
    
    style_teacher_login_comps()
    st.header("Register your teacher profile", text_alignment="center")
    st.space()

    teacher_username = st.text_input("Username:", placeholder="E.g. mayank123").strip()
    teacher_name = st.text_input("Full name:", placeholder="E.g. Mayank Rathod").strip()
    teacher_pass = st.text_input("Password:", type="password", placeholder="Enter a new password").strip()
    teacher_pass_conf = st.text_input("Confirm password:", type="password", placeholder="Confirm your password").strip()

    remove_focus()
    st.divider()
    st.space()
    btn1, btn2 = st.columns(2, gap="medium")

    if btn1.button("Register", type="primary", width="stretch", shortcut="control+enter", icon=":material/passkey:"):
        success, message = register_teacher(teacher_username, teacher_name, teacher_pass,teacher_pass_conf)        

        if success:
             st.success(message)
             time.sleep(1)
             st.session_state["login_type"] = "login"
             st.rerun()

        else:
             st.error(message)

    if btn2.button("Login instead", type="secondary", width="stretch", icon=":material/passkey:"):
        st.session_state["login_type"] = "login"
        st.rerun()
    

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_conf):

    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_conf:
        return False, "All fields are mandatory"
    if check_teacher_exists(teacher_username):
        return False, "Username is already taken"
    if teacher_pass != teacher_pass_conf:
        return False, "password does not match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Succesfully registered, login now"
    except Exception as e:
        return False, "Unexpected error!"
    

def teacher_login_comp():

    style_teacher_login_comps()

    st.header("Login using password", text_alignment="center")
    st.space()

    teacher_username = st.text_input("Username :", placeholder="Enter your username").strip()
    teacher_password = st.text_input("Password :", placeholder="Enter your password", type="password").strip()

    remove_focus()
    st.divider()
    st.space()

    btn1, btn2 = st.columns(2)

    if btn1.button("Login",type="primary", icon=":material/passkey:", width="stretch", shortcut="control+enter"):
        response = get_teacher_cred(teacher_username, teacher_password)
        if response:
            st.success(f"logged in successfully!, welcome {response["name"]}")
            st.session_state["teacher_data"] = response
            st.session_state["is_logged_in"] = True
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password")
        

    if btn2.button("Register instead", type="secondary", icon=":material/passkey:", width="stretch"):
        st.session_state["login_type"] = "register"
        st.rerun()
