import streamlit as st
from src.pipelines.face_pipeline import detect_faces_attendance
from src.database.db import get_div_students, add_attendance_logs, mark_lecture_true, get_lecture_status
import numpy as np
import pandas as pd
from PIL import Image
import time

def detect_faces_comp(selected_lec):

    images_np = [np.array(Image.open(img)) for img in st.session_state["all_images"]]
    div_students = get_div_students(selected_lec["subjects"]["course"], selected_lec["division"])

    detect_faces_attendance(images_np, div_students)

    students_df = pd.DataFrame(div_students)

    return students_df

@st.fragment
def submit_frag(students_df, selected_lec):
    submit_attendance(students_df, selected_lec)




@st.dialog("Preview & Submit")
def submit_attendance(students_df, selected_lec):
    students_df = st.data_editor(
        students_df,
        column_config ={
            "student_id" : "Student ID",
            "name" : "Name",
            "best_score" : "Similarity",
            "is_present" : "Is Present"
        }, 
        disabled=["student_id", "name", "best_score"],
        hide_index=True
    )

    lec_id = selected_lec["lecture_id"]
    students_df["lecture_id"] = lec_id

    logs_data = students_df[["lecture_id", "student_id", "is_present"]].to_dict(orient="records")
    
    if st.button("Submit Attendance", type="primary", width="stretch"):
        if not get_lecture_status(lec_id)["is_conducted"]:
            try:
                add_attendance_logs(logs_data)
                st.success("Attendance data submitted Successfully!")
                mark_lecture_true(lec_id)
                st.success("Updated Lecture status to conducted")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(e)
        else:
            st.error("Lecture is already conducted")


def upload_img_comp(selected_lec):

        if "all_images" not in st.session_state:
            st.session_state["all_images"] = []

        if "is_camera" not in st.session_state:
            st.session_state["is_camera"] = False

        st.space()
        st.markdown(":color[**Choose Method :**]{foreground='#1F2937'}")
        img_cols = st.columns(3)
        with img_cols[0].popover("Upload Images", width="stretch", icon=":material/upload:"):
            selected_imgs = st.file_uploader("Upload student's images:", type="image", max_upload_size=15, accept_multiple_files=True, label_visibility="collapsed",)

            if selected_imgs:

                if st.button("Add images", type="tertiary", icon=":material/add:"):
                    for img in selected_imgs:
                        st.session_state["all_images"].append(img)
                    st.rerun()

        btn_name = "Close Camera" if st.session_state["is_camera"] else "Use Camera"
        btn_icon = ":material/close:" if st.session_state["is_camera"] else ":material/add_a_photo:" 

        if img_cols[1].button(btn_name, type="secondary", icon=btn_icon, width="stretch"):
            st.session_state["is_camera"] = not st.session_state["is_camera"]
            st.rerun()

        if img_cols[2].button("Submit Manually", type="secondary", width="stretch"):
            students_df = pd.DataFrame(get_div_students(selected_lec["subjects"]["course"], selected_lec["division"]))
            students_df["is_present"] = False
            submit_frag(students_df[["student_id", "name", "is_present"]], selected_lec)

        if "is_camera" in st.session_state and  st.session_state["is_camera"]:
            uploaded_img = st.camera_input("Click Photo")
            if st.button("Add image", type="tertiary", icon=":material/add:"):
                st.session_state["all_images"].append(uploaded_img)
                st.rerun()

        if st.session_state["all_images"]:
            st.space()
            st.subheader("Selected Images :")

            grid = st.columns(4)

            for i, selected_img in enumerate(st.session_state["all_images"]):
                grid[i%4].image(selected_img)

            if st.button("Clear all images", type="tertiary"):
                st.session_state["all_images"] = []
                st.rerun()

