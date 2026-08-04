import streamlit as st
from src.database.db import check_sub_exists, add_subject, get_all_subjects, get_all_teachers, is_sub_assigned, assign_subject, get_assigned_subjects, get_sem_subjects, get_course_divisions, get_assigned_teachers, add_lecture, is_lec_scheduled
import pandas as pd
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def subject_comp():

    if "show_subject" not in st.session_state:
        st.session_state["show_subject"] = False

    st.subheader("Add subjects", text_alignment="center")

    course_name = st.text_input("Course Name:",placeholder="Enter course name").strip()
    semester = st.selectbox("Semester :",range(1, 9), index=None, placeholder="Select the semester")
    sub_name = st.text_input("Subject :", placeholder = "Enter name of the subject").strip()

    code = None
    if course_name and semester:
        sub_count = len(get_sem_subjects(course_name, semester))
        code = course_name + str(semester) + "0" + str((sub_count + 1))

    sub_code = st.text_input("Subject Code:", placeholder="Enter the 6 digit subject code", value = code)

    st.space()

    if st.button("Add subject",shortcut="control+enter", type="primary", width="stretch"):
        success, message = add_subject_py(course_name, semester, sub_code, sub_name)
        if success:
            st.success(message)
            time.sleep(2)
            st.rerun()
        else:
            st.error(message)

    st.divider()

    if st.button("View all subjects", type="secondary", width="stretch"):
        st.session_state["show_subject"] = True

    if st.session_state["show_subject"]:
        show_subjects()

def add_subject_py(course_name, semester, sub_code, sub_name):

    info = [course_name, semester, sub_code, sub_name]
    info = list(map(bool, info))

    if False in info:
        return False, "All fields are mandatory"
    if check_sub_exists(sub_code):
        return False, "Subject already exists!"

    try:
        add_subject(course_name, semester, sub_code, sub_name)
        return True, "Subject added successfully in the database"
    except Exception as e:
        return False, e

def show_subjects():
    subjects = get_all_subjects()

    df = pd.DataFrame(subjects)
    df.drop(columns=["subject_id"], inplace=True)

    courses = df["course"].unique().tolist()
    selected_course = st.selectbox("Select the course :", courses, index = None, placeholder="Select the Course")

    sems = df[df["course"] == selected_course]["semester"].unique().tolist()
    selected_sem = st.selectbox("Select the semester :", sems, index=None, placeholder="Select the semester")
    st.space()

    if selected_course and selected_sem:
        st.dataframe(
            df[(df["course"] == selected_course) & (df["semester"] == selected_sem)][["subject_code", "subject_name"]],
            column_config={
                "subject_code" : "Subject Code",
                "subject_name" : "Subject Name",
                "semester" : "Semester",
                "course" : "Course"
            }
        )
    elif selected_course:
        st.dataframe(
            df[df["course"] == selected_course].drop(columns=["course"]),
            column_config={
                "subject_code" : "Subject Code",
                "subject_name" : "Subject Name",
                "semester" : "Semester",
                "course" : "Course"
            }
        )
    
def teachers_comp():
    st.subheader("Assign Subjects", text_alignment="center")
    st.space()
    teachers = get_all_teachers()
    subjects_df = pd.DataFrame(get_all_subjects())

    for i, teacher in enumerate(teachers):
        teacher_sub_box(i, teacher, subjects_df)

@st.fragment
def teacher_sub_box(i, teacher, subjects_df):
        with st.container():

            sec1, sec2 = st.columns([93, 7], vertical_alignment="top")

            sec1.markdown(f"""
            <div>
                <span style="color:black; padding:0 1rem; font-size:1.25rem;">{i}</span>
                <span style="color:black;">{teacher["name"]}</span>
                <span style="color:var(--text_secondary); padding: 0 1rem;">{teacher["username"]}</span>
            </div>
            """, unsafe_allow_html=True)

            arr_icon = ":material/keyboard_arrow_up:"if f"is_teacher{i}" in st.session_state and st.session_state[f"is_teacher{i}"] else ":material/keyboard_arrow_down:"

            if sec2.button("",icon=arr_icon, key=f"teacher_sub_btn{i}"):
                if f"is_teacher{i}" not in st.session_state:
                    st.session_state[f"is_teacher{i}"] = False
                st.session_state[f"is_teacher{i}"] = not st.session_state[f"is_teacher{i}"]
                st.rerun()

            if f"is_teacher{i}" in st.session_state and st.session_state[f"is_teacher{i}"]:
                assigned_subs = pd.DataFrame(get_assigned_subjects(teacher["teacher_id"]))

                if not assigned_subs.empty:
                    sub_names = subjects_df[subjects_df["subject_id"].isin(assigned_subs["subject_id"])]["subject_name"].tolist()
                    for ind, sub_name in enumerate(sub_names):
                        st.markdown(f"""
                            <span style="margin-left:3rem;color: var(--text_secondary);">{sub_name}</span>
                        """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                        <p style="margin-left:3rem; color:var(--text_secondary);">No subjects assigned yet.</p>
                    """, unsafe_allow_html=True)

                pad, content = st.columns([2, 98])

                if content.button("Add subject", icon=":material/add_2:", type="tertiary", key=f"add_sub{i}"):
                    add_subject_dialog(subjects_df, teacher)

@st.dialog("Select the subject")
def add_subject_dialog(subjects_df, teacher):
    st.header("Select subject")

    courses = subjects_df["course"].unique().tolist()
    selected_course = st.selectbox("Course :", courses, index=None, placeholder="Select the course ")

    sems = subjects_df[subjects_df["course"] == selected_course]["semester"].unique().tolist()
    selected_sem = st.selectbox("Semester :", sems, index=None, placeholder="Select semester")

    subjects = subjects_df[(subjects_df["course"] == selected_course) & (subjects_df["semester"] == selected_sem)][["subject_id", "subject_name"]]
    labels = subjects.set_index("subject_id")["subject_name"].to_dict()
    options = subjects["subject_id"].tolist()
    selected_sub = st.selectbox("Subject :", options, format_func= lambda x: labels[x], index=None, placeholder="Select subject")

    st.space()

    if st.button(f"Assign subject to {teacher["name"]}", disabled = not(bool(selected_sub)), type="primary", width="stretch"):
        if is_sub_assigned(teacher["teacher_id"], selected_sub):
            st.error("Subject is already assigned")
        else:
            try:
                assign_subject(teacher["teacher_id"], selected_sub)
                st.success(f"Successfully assigned{subjects[subjects["subject_id"] == selected_sub].iloc[0,1]} to {teacher["name"]}.")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(e)

def lectures_comp():
    st.subheader("Arrange Lectures", text_alignment="center")
    st.space()

    subjects_df = pd.DataFrame(get_all_subjects())

    courses = subjects_df["course"].unique()
    selected_course = st.selectbox("Course", courses, index=None, placeholder="Select the course")

    semesters = subjects_df[subjects_df["course"] == selected_course]["semester"].unique()
    selected_sem = st.selectbox("Semester :", semesters, index=None, placeholder="Select semester")

    divisions = pd.DataFrame(get_course_divisions(selected_course))["division"] if selected_course else None
    selected_div = st.selectbox("Division :", divisions, index=None, placeholder="Select the division")

    subjects = subjects_df[(subjects_df["course"] == selected_course) & (subjects_df["semester"] == selected_sem)][["subject_id", "subject_name"]]
    sub_labels = subjects.set_index("subject_id")["subject_name"].to_dict()
    sub_options = subjects["subject_id"]
    selected_subject = st.selectbox("Subjects :", sub_options,format_func= lambda x: sub_labels[x], index = None, placeholder="Select Subject")

    teachers = get_assigned_teachers(selected_subject) if selected_subject else None
    options, labels = None, None
    if teachers:
        teachers = pd.DataFrame(teachers)[["teacher_id", "name"]]
        labels = teachers.set_index("teacher_id")["name"].to_dict()
        options = teachers["teacher_id"]
    selected_teacher = st.selectbox("Teachers :", options,format_func= lambda x: labels[x], index=None, placeholder="Select the teacher")

    now = datetime.now(tz=ZoneInfo("Asia/Kolkata"))
    lec_time = st.datetime_input("Date & Time :", min_value=now, value = None,  step=60).replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    st.write(lec_time)

    st.space()
    if st.button("Schedule Lecture", type="primary", width="stretch"):
        success, message = schedule_lec(selected_subject, selected_teacher, selected_div, lec_time, sub_labels)
        if success:
            st.success(message)
            time.sleep(2)
            st.rerun()
        else:
            st.error(message)

def schedule_lec(subject_id, teacher_id, division, timestamp, sub_names):
    info = [subject_id, teacher_id, division, timestamp]
    info = list(map(bool,info))

    if False in info:
        return False, "Select all the values"
    if is_lec_scheduled(division, timestamp):
        return False, f"Lecture is already scheduled for selected division {division} on {timestamp.date()} {timestamp.time()}"

    try:
        add_lecture(subject_id, teacher_id, division, timestamp)
        return True, f"Lecture of {sub_names[subject_id]} for division {division} is scheduled on {timestamp.date()} {timestamp.time()}"
    except Exception as e:
        return False, e