import streamlit as st
from src.ui.style_student_screen import style_student_login_comps, remove_focus
from src.database.db import add_student, check_student_exists, get_student_cred
from src.pipelines.face_pipeline import get_face_embeddings, detect_faces
from PIL import Image
import numpy as np
import time

def student_login_comp():
    style_student_login_comps()

    if "is_camera" not in st.session_state:
        st.session_state["is_camera"] = False

    st.header("Login using Password", text_alignment="center")
    st.space()

    std_username = st.text_input("Username :", placeholder="Enter your username")
    std_password = st.text_input("Password :", type="password", placeholder="Enter your password")
    std_image = None
    remove_focus()

    cam_text = "Close camera" if st.session_state["is_camera"] else "Login using FaceId"
    cam_icon = ":material/close:" if st.session_state["is_camera"] else ":material/add_a_photo:"
    if st.button(cam_text, type="secondary", width="stretch", icon=cam_icon, key="camera_btn"):
        st.session_state["is_camera"] = not st.session_state["is_camera"]
        st.rerun()

    if st.session_state["is_camera"]:
        std_image = st.camera_input("Position your face in the center")

    st.divider()

    btn1, btn2 = st.columns(2, gap="medium")

    if btn1.button("Login", shortcut="control+enter", type="primary", width="stretch", icon=":material/passkey:"):
        st.session_state["is_camera"] = False
        success, message, student = login_student(std_username, std_password, std_image)
        if success:
            st.session_state["is_logged_in"] = True
            st.session_state["student_data"] = student
            st.space()
            st.success(message, icon=":material/check_circle:")
            time.sleep(1)
            st.rerun()
        else:
            st.space()
            st.error(message, icon=":material/error:")

    if btn2.button("Register instead",type="secondary", width="stretch", icon=":material/passkey:"):
       st.session_state["is_camera"] = False
       st.session_state["login_type"] = "register"
       st.rerun()

def login_student(username, password, face_img = None):

    if not username and not password and not face_img:
        return False, "Please enter your username & password. or Log in via FaceID", None

    if face_img:
        image_np = np.array(Image.open(face_img))
        response = detect_faces([image_np])

        if response[0]["is_registered"]:
            return True, "Logged in successfully using FaceId", response[0]
        elif username and password:
            student = get_student_cred(username, password)
            if student:
                return True, "Logged in Succesfully", student
            else:
                return False, "Invalid Username or password", student
        else:
            st.write(response[0]["best_score"], response[0]["name"])
            return False, "Unknown person detected!", None
    else:
        student = get_student_cred(username, password)
        if student:
            return True, "Logged in Successfully", student
        else:
            return False, "Invalid username or password", student

def student_register_comp():
    style_student_login_comps()

    if "is_camera" not in st.session_state:
        st.session_state["is_camera"] = False

    if "all_images" not in st.session_state:
        st.session_state["all_images"] = []

    st.header("Register your student profile", text_alignment="center")
    st.space()

    std_username = st.text_input("Username :", placeholder="Enter a unique username")
    std_name = st.text_input("Full Name :", placeholder="Enter your full name")
    std_password = st.text_input("Password :", type="password", placeholder="Enter a new password")
    std_password_conf = st.text_input("Confirm Password :", type="password", placeholder="Confirm your password")
    st.file_uploader("Choose image:", type="image", max_upload_size=15, accept_multiple_files=True, key = "reg_image")
    remove_focus()

    if st.session_state["reg_image"]:
        if st.button("Add images", type="secondary"):
            add_image()

    cam_text = "Close camera" if st.session_state["is_camera"] else "Take a picture"
    cam_icon = ":material/close:" if st.session_state["is_camera"] else ":material/add_a_photo:"    
    if st.button(cam_text, type="secondary", icon=cam_icon, width="stretch"):
        st.session_state["is_camera"] = not st.session_state["is_camera"]
        st.rerun()
    st.info("Tip : Upload atleast 🖼️ 4-5 images in different conditions for better results", icon=":material/info:")

    if st.session_state["is_camera"]:
        camera_img = st.camera_input("Position your face in the center:")
        if st.button("Add image", type="secondary"):
            st.session_state["all_images"].append(camera_img) if camera_img else st.error("Please click photo first", icon=":material/error:")

    if st.session_state["all_images"]:
        st.subheader("Selected Images:")

        st.space()
        cols = st.columns(4)
        for i, img in enumerate(st.session_state["all_images"]):
            cols[i%4].image(img, width="content")

        st.space()
        if st.button("Clear all images", type="tertiary"):
            st.session_state["all_images"] = []
            st.rerun()

    st.divider()

    btn1, btn2 = st.columns(2, gap="medium")

    if btn1.button("Register", type="primary", shortcut="control+enter", width="stretch"):
        st.session_state["is_camera"] = False
        success, message = register_student(std_username, std_name, std_password, std_password_conf, st.session_state["all_images"])
        if success:
            st.session_state["all_images"] = []
            st.space()
            st.success(message, icon=":material/check_circle:")
            st.session_state["login_type"] = "login"
            time.sleep(1)
            st.rerun()
        else:
            st.space()
            st.error(message, icon=":material/error:")

    if btn2.button("Login instead", type="secondary", width="stretch"):
       st.session_state["all_images"] = []
       st.session_state["is_camera"] = False
       st.session_state["login_type"] = "login"
       st.rerun()

def register_student(std_username, std_name, std_password, std_password_conf, std_imgs):

    std_info = [std_username, std_name, std_password, std_password_conf, std_imgs]
    std_info = list(map(bool, std_info))

    if False in std_info:
        return False, "All fields are mandatory!"
    elif check_student_exists(std_username):
        return False, "Username already exists"
    elif std_password != std_password_conf:
        return False, "Password does not match"

    image_np = [np.array(Image.open(img)) for img in std_imgs]
    embeddings = get_face_embeddings(image_np)
    embeddings = [emb.tolist() for emb in embeddings]

    if len(embeddings) < 1:
        return False, "Upload the image where face is clearly visible"
    elif len(embeddings) > len(image_np):
        return False, "Upload the image where only your face is visible"

    try:
        add_student(std_username, std_name, std_password, embeddings)
        return True, "Successfully Registerd!"
    except Exception as e:
        return False, e

def add_image():
    new_images = st.session_state["reg_image"]
    for img in new_images:
        st.session_state["all_images"].append(img)
    return 
