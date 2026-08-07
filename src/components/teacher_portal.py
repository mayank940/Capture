import streamlit as st
from src.ui.style_teacher_screen import  style_teacher_portal
from src.database.db import get_assigned_subjects, get_lectures, get_previous_lectures  
from src.components.teacher_portal_ops import upload_img_comp, detect_faces_comp, submit_frag
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

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

    lectures = get_lectures(teacher_id = teacher["teacher_id"], pending=True)
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
    st.subheader("Today's Lectures", text_alignment="center")
    lectures = get_lectures(teacher_id = teacher["teacher_id"])

    st.space()
    if lectures:
        for lecture in lectures:
            lecture_card(lecture)
    else:
        st.info("📚 No lectures scheduled by the authority for today!")

    st.space()
    st.subheader("Previous Lectures", text_alignment="center")
    st.space()

    prev_lectures = get_previous_lectures(teacher["teacher_id"])
    
    if prev_lectures:
        for lecture in prev_lectures:
            lecture_card(lecture)

def lecture_card(lecture):
    subject = lecture["subjects"]
    timestamp = datetime.fromisoformat(lecture["lec_timestamp"]).astimezone(ZoneInfo("Asia/Kolkata"))
    lec_date = timestamp.date().strftime("%d-%m-%Y")
    lec_time = timestamp.time().strftime("%H:%M")

    today = datetime.combine(
        date.today(),
        time(0, 0),
        ZoneInfo("Asia/Kolkata")
    )
    lec_status = "" 
    if lecture["is_conducted"]:
        lec_status = "✅ Completed"
    elif not lecture["is_conducted"] and timestamp <= today:
        lec_status = "❌ Not Conducted"
    elif not lecture["is_conducted"]:
        lec_status = "⏳ Attendance Pending"


    with st.container():
        st.subheader(subject["subject_name"])
        st.markdown(f"""
        <div style='margin-top:5px;'>
            <p style='color:#6B7280;'>📆  Date : <span style='font-weight:700;'>{lec_date}</span></p>
            <p style='color:#6B7280;'>🕗  Time : <span style='font-weight:700;'>{lec_time}</span></p>
            <p style='color:#6B7280;'>📓  Division : <span style='font-weight:700;'>{lecture["division"]}</span>     Subject Code : <span style='font-weight:700;'>{subject["subject_code"]}</span></p>
            <p style='color:#6B7280;'>{lec_status}</p>
        </div>
        
        """, unsafe_allow_html=True)