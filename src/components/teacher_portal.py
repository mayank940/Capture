import streamlit as st
from src.ui.style_teacher_screen import  style_teacher_portal
from src.database.db import get_assigned_subjects, get_lectures, get_div_students, add_attendance_logs
from src.components.teacher_portal_ops import upload_img_comp, detect_faces_comp, submit_frag
from src.pipelines.face_pipeline import detect_faces_attendance, preview_detected_faces
import numpy as np
import pandas as pd
from PIL import Image

def teacher_portal():
    style_teacher_portal()

    teacher = st.session_state["teacher_data"]
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "take_attendance"

    st.space()
    navs = st.columns(3)

    type1 = "primary" if st.session_state["nav_page"] == "take_attendance" else "secondary"
    type2 = "primary" if st.session_state["nav_page"] == "subjects" else "secondary"
    type3 = "primary" if st.session_state["nav_page"] == "lectures" else "secondary"


    if navs[0].button("Attendance", width="stretch", type = type1):
        st.session_state["nav_page"] = "take_attendance"
        st.rerun()

    if navs[1].button("Subjects", width="stretch", type=type2):
        st.session_state["nav_page"] = "subjects"
        st.rerun()

    if navs[2].button("Lectures", width="stretch", type=type3):
        st.session_state["nav_page"] = "lectures"
        st.rerun()

    st.divider()

    match st.session_state["nav_page"]:
        case "take_attendance":
            take_attendance(teacher)
        case "subjects": 
            manage_subjects(teacher)
        case "lectures":
            manage_lectures(teacher)

def take_attendance(teacher):
    st.subheader("Take Attendance", text_alignment="center")
    st.space()

    lectures = get_lectures(teacher_id = teacher["teacher_id"])
    labels = [f"{lecture["subjects"]["subject_name"]}, {lecture["subjects"]["course"]},  {lecture["division"]}" for lecture in lectures]
    options = [lecture for lecture in lectures]

    selected_lec = st.selectbox("Today's Lectures :", options, index=None, format_func= lambda x: labels[options.index(x)])

    if selected_lec:
        upload_img_comp(selected_lec)

        st.space()
        detect_btn_disabled = not bool(st.session_state["all_images"])

        if st.button("Detect Faces", type="primary", disabled=detect_btn_disabled):

            students_df = detect_faces_comp(selected_lec)
            
            submit_frag(students_df, selected_lec)
            
def manage_subjects(teacher):
    st.subheader("Assigned Subjects", text_alignment="center")
    st.space()

    teacher = st.session_state["teacher_data"]
    subjects = get_assigned_subjects(teacher["teacher_id"])

    st.space()
    if subjects:
        for subject in subjects:
            with st.container(border=True):
                st.subheader(subject["subject_name"])
                st.markdown(f""":color[Subject Code :]{{foreground="#6B7280"}}  **:color[{subject["subject_code"]}]{{foreground="#C77DFF"}}** """)
                st.markdown(f":color[Course : **{subject["course"]}**  Semester : **{subject["semester"]}**]{{foreground='#6B7280'}}")
    else:
        st.info("📖 No subjects assigned by the authority yet!")

def manage_lectures(teacher):
    st.subheader("Manage Lectures", text_alignment="center")
    lectures = get_lectures(teacher_id = teacher["teacher_id"])

    st.space()
    if lectures:
        for lecture in lectures:
            subject = lecture["subjects"]
            with st.container():
                st.subheader(subject["subject_name"])
                st.markdown(f":color[Time **{lecture["lec_timestamp"]}**    Division : **{lecture["division"]}**]{{foreground='#6B7280'}}")
                st.markdown(f":color[Subject Code : **{subject['subject_code']}**  Semester : **{subject['semester']}**  Course : **{subject['course']}**]{{foreground='#6B7280'}}")
    else:
        st.info("📚 No lectures scheduled by the authority for today!")
