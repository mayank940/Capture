import streamlit as st
from src.ui.style_student_screen import style_student_portal
from src.database.db import get_all_subjects, get_course_students, enroll_student, get_student, get_lectures, get_sem_subjects, get_attendance_records, get_student_logs
import pandas as pd
import numpy as np
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def student_portal():
    style_student_portal()
    st.space()
    student = st.session_state["student_data"]

    if not student["course"]:
        enrollment_comp(student)

    else:

        if "std_nav_page" not in st.session_state:
            st.session_state["std_nav_page"] = "attendance"

        type1 = "primary" if st.session_state["std_nav_page"] == "attendance" else "secondary"
        type2 = "primary" if st.session_state["std_nav_page"] == "lectures" else "secondary"
        type3 = "primary" if st.session_state["std_nav_page"] == "subjects" else "secondary"

        navs = st.columns(3)

        if navs[0].button("Attendance", type=type1, width="stretch"):
            st.session_state["std_nav_page"] = "attendance"
            st.rerun()

        if navs[1].button("Lectures", type=type2, width="stretch"):
            st.session_state["std_nav_page"] = "lectures"
            st.rerun()

        if navs[2].button("Subjets", type=type3, width="stretch"):
            st.session_state["std_nav_page"] = "subjects"
            st.rerun()

        st.divider()
        match st.session_state["std_nav_page"]:
            case "attendance":
                nav_attendance(student)
            case "lectures":
                nav_lectures(student)
            case "subjects":
                nav_subjects(student)

def enrollment_comp(student):
    st.header(f"Not enrolled in any course yet", text_alignment="center")
    st.space()
    st.subheader("Enroll now to begin your Journey!", text_alignment="center")
    st.space()

    all_subs_df = pd.DataFrame(get_all_subjects())
    courses = all_subs_df["course"].unique()
    selected_course = st.selectbox("Available Courses :", courses, index=None, placeholder="Select the Course")

    if selected_course:
        subjects_df = all_subs_df[all_subs_df["course"] == selected_course]

        with st.container(horizontal=True, horizontal_alignment="center"):
            st.markdown(f"#:color[{selected_course} has a total of {subjects_df["semester"].nunique()} Semesters and {len(subjects_df)} Subjects.]{{foreground='#6B7280'}}", text_alignment="right")

            if st.button("Show subjects" if "show_subject" not in st.session_state or not st.session_state["show_subject"] else "Hide Subjects", type="tertiary"):
                if "show_subject" not in st.session_state:
                    st.session_state["show_subject"] = False
                st.session_state["show_subject"] = not st.session_state["show_subject"]
                st.rerun()

        if "show_subject" in st.session_state and st.session_state["show_subject"]:
            st.dataframe(subjects_df)

    st.space()
    st.space()
    _, btn , _ = st.columns([16,66,18])
    if btn.button("Enroll now", type="primary", width="stretch"):
        success, message = enroll_student_py(selected_course, student["student_id"])

        if success:
            st.success(message)
            st.session_state["student_data"] = get_student(student["student_id"])[0]
            time.sleep(2)
            st.rerun()
        else:
            st.error(message)

def enroll_student_py(course, student_id):
    if not course:
        return False, "Select the course to enroll"

    enrolled_students = len(get_course_students(course))
    division = None

    if enrolled_students <= 30:
        division = "A"
    elif enrolled_students <= 60:
        division = "B"
    elif enrolled_students <= 90:
        division = "C"
    elif enrolled_students <= 120:
        division = "D"
    else:
        return False, "All seats are filled"

    try:
        enroll_student(course, division, student_id)
        return True, f"Enrolled in {course} successfully."
    except Exception as e:
        return False, "Unexpected Error!"

def nav_attendance(student):
    st.markdown("""
    <style>

    </style>

    """,unsafe_allow_html=True)

    st.subheader("Attendance Summary", text_alignment="center")
    st.space()

    logs_df = pd.DataFrame(get_attendance_records(student["student_id"]))
    logs_df["subject_name"] = logs_df["lectures"].str.get("subjects").str.get("subject_name")

    attendance = (logs_df["is_present"].sum() / len(logs_df)) * 100 

    with st.container(border=True):
        st.markdown(f":color[Overall Attendance : **{attendance:.2f} %**]{{foreground='#1F2937'}}")
        st.markdown(f":color[Total lectures : {len(logs_df)}]{{foreground='#1F2937'}}")
        st.markdown(f":color[Attended lectures : {logs_df["is_present"].sum()}]{{foreground='#1F2937'}}")
        if st.button("View Summary", type="tertiary"):
            attendance_summary(logs_df)

    st.divider()
    st.subheader("Attendance Records", text_alignment="center")
    st.space()
    attendance_records(student)

@st.fragment
def attendance_records(student):

    st.space()

    selected_date = st.date_input("Selecte Date :", max_value="today", value=None)

    subjects_df = pd.DataFrame(get_sem_subjects(student["course"], 1))
    labels = subjects_df["subject_name"].tolist()
    options = subjects_df["subject_id"].tolist()
    selected_sub = st.selectbox("Subject :", options, index=None, format_func = lambda x: labels[options.index(x)], placeholder="Select a subject")


    records_df = None
    if selected_sub and selected_date:
        records_df = pd.DataFrame(get_attendance_records(student["student_id"], selected_date, selected_sub))
    elif selected_sub:
        records_df = pd.DataFrame(get_attendance_records(student["student_id"], subject_id = selected_sub))
    elif selected_date:
        records_df = pd.DataFrame(get_attendance_records(student["student_id"], log_date=selected_date))

    if  records_df is None:
        return
    elif records_df.empty:
        st.error("No records found for the selected data")
        return

    records_df["date"] = records_df["timestamp"].apply(date_format)
    records_df["time"] = records_df["timestamp"].apply(time_format)
    records_df["display"] = records_df["is_present"].map({True : "✅" ,False : "❌"})

    records_df["subject_name"] = records_df["lectures"].str.get("subjects").str.get("subject_name")
    records_df = records_df[["subject_name", "date", "time", "display"]]

    st.dataframe(
        records_df,
        column_config={
            "subject_name" : "Subject",
            "date" : "Date",
            "time" : "Time",
            "display" : "Present"
        }
    )

@st.dialog("Attendance Summary", width="medium")
def attendance_summary(logs_df):
    st.subheader("Summary")

    total_lec= logs_df[["subject_name", "is_present"]].groupby("subject_name")["is_present"].count()
    attended_lec = logs_df[["subject_name", "is_present"]].groupby("subject_name")["is_present"].sum()
    summary_df = pd.DataFrame({"conducted" : total_lec, "attended" : attended_lec})
    summary_df = summary_df.reset_index()
    summary_df["percentage"] = round((summary_df["attended"] / summary_df["conducted"]) * 100, 2)
    st.write((summary_df))
    
def nav_lectures(student):
    st.subheader("Today's Lectures", text_alignment="center")
    st.space()

    lectures = get_lectures(student_div=student["division"], student_course = student["course"])

    for lecture in lectures:
        lec_datetime = datetime.fromisoformat(lecture["lec_timestamp"]).astimezone(ZoneInfo("Asia/Kolkata"))
        lec_time = lec_datetime.time()
        with st.container():
            st.subheader(lecture["subjects"]["subject_name"])
            st.markdown(f":color[Time : **{lec_time}**]{{foreground='#6B7280'}}")
            st.markdown(f":color[Conducted By : **{lecture["teachers"]["name"]}**]{{foreground='#6B7280'}}")

def nav_subjects(student):
    st.subheader("Manage Subjects", text_alignment="center")
    st.space()

    subjects = get_sem_subjects(student["course"], 1)

    for subject in subjects:
        with st.container():
            st.subheader(subject["subject_name"])
            st.markdown(f":color[Subject Code : **{subject["subject_code"]}**]{{foreground='#6B7280'}}")

def date_format(timestamp_str):

    timestamp = datetime.fromisoformat(timestamp_str).astimezone(ZoneInfo("Asia/Kolkata"))
    return timestamp.strftime("%d-%m-%Y")

def time_format(timestamp_str):
    timestamp = datetime.fromisoformat(timestamp_str).astimezone(ZoneInfo("Asia/Kolkata"))
    return timestamp.strftime("%H:%M")