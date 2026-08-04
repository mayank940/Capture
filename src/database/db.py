from src.database.config import supabase
import bcrypt 
from datetime import datetime, timezone, date, time
from zoneinfo import ZoneInfo

# -----------------------------------hashing----------------------------------------

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hash_pwd):
    return bcrypt.checkpw(pwd.encode(), hash_pwd.encode())



# ----------------------------------teachers table----------------------------------------------

def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"username" : username, "password" : hash_password(password), "name" : name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def get_all_teachers():
    response = supabase.table("teachers").select("*").execute()
    return response.data

def get_teacher(teacher_id):
    response = supabase.table("teachers").select("*").eq("teacher_id", teacher_id).execute()
    return response.data

def get_teacher_cred(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None



# ----------------------------------Students Table---------------------------------------

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def get_student(student_id):
    response = supabase.table("students").select("*").eq("student_id", student_id).execute()
    return response.data

def add_student(username, name, password, face_embedding):
    data = {"username" : username, "name" : name, "password" : hash_password(password), "face_embedding" : face_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def check_student_exists(username):
    response = supabase.table("students").select("username").eq("username", username).execute()
    return len(response.data) > 0

def get_student_cred(username, password):
    response = supabase.table("students").select("*").eq("username", username).execute()
    if response.data:
        student = response.data[0]
        if check_pass(password, student["password"]):
            return student
    return None

def get_course_students(course_name):
    response = supabase.table("students").select("student_id").eq("course", course_name).execute()
    return response.data

def enroll_student(course, division, student_id):
    data = {"course" : course, "division" : division, "enrolled_at" : datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()}
    response = supabase.table("students").update(data).eq("student_id", student_id).execute()
    return response

def get_course_divisions(course_name):
    response = supabase.rpc("get_course_divisions", {"p_course_name" : course_name}).execute()
    return response.data

def get_div_students(course, division):
    response = supabase.table("students").select("*").eq("course", course).eq("division", division).execute()
    return response.data




# ---------------------------------Subjects Table------------------------------------------

def check_sub_exists(sub_code):
    response = supabase.table("subjects").select("subject_code").eq("subject_code", sub_code).execute()
    return len(response.data) > 0

def add_subject(course_name, semester, sub_code, sub_name):
    data = {"course" : course_name, "semester" : semester, "subject_code" : sub_code, "subject_name" : sub_name}
    response = supabase.table("subjects").insert(data).execute()
    return response

def get_all_subjects():
    response = supabase.table("subjects").select("*").execute()
    return response.data

def get_sem_subjects(course, semester):
    response = supabase.table("subjects").select("*").eq("course", course).eq("semester", semester).execute()
    return response.data




# -----------------------Teacher Subjects Relational table-------------------------------

def is_sub_assigned(teacher_id, subject_id):
    response = supabase.table("teacher_subjects").select("*").eq("teacher_id", teacher_id).eq("subject_id", subject_id).execute()
    return len(response.data) > 0

def assign_subject(teacher_id, subject_id):
    data = {"teacher_id" : teacher_id, "subject_id" : subject_id}
    response = supabase.table("teacher_subjects").insert(data).execute()
    return response

def get_assigned_subjects(teacher_id):
    response = (
        supabase.table("subjects")
        .select("*, teacher_subjects!inner(teacher_id)")
        .eq("teacher_subjects.teacher_id", teacher_id)
        .execute()
        )
    return response.data

def get_assigned_teachers(subject_id):
    response = (
        supabase.table("teachers")
        .select("*, teacher_subjects!inner(subject_id)")
        .eq("teacher_subjects.subject_id", subject_id)
        .execute()
        )

    return response.data




# --------------------------------Lectures Table-------------------------------

def is_lec_scheduled(division, timestamp):
    response = (
        supabase
        .table("lectures")
        .select("lecture_id")
        .eq("division", division)
        .eq("lec_timestamp", timestamp.isoformat())
        .execute()
    )
    return len(response.data) > 0

def get_lectures(teacher_id = None, student_div = None, student_course= None):

    today = date.today()

    start = datetime.combine(
        today,
        time(0, 0),
        tzinfo = ZoneInfo("Asia/Kolkata")
    )

    end = datetime.combine(
        today,
        time(23, 59),
        tzinfo = ZoneInfo("Asia/Kolkata")
    )

    if teacher_id:
        response = (
            supabase
            .table("lectures")
            .select("*, subjects!inner(*)")
            .eq("teacher_id", teacher_id)
            .eq("is_conducted", False)
            .gte("lec_timestamp", start.isoformat())
            .lte("lec_timestamp", end.isoformat())
            .execute()
            )
        return response.data

    elif student_div and student_course:
        response = (
            supabase
            .table("lectures")
            .select("*, teachers!inner(name), subjects!inner(subject_name)")
            .eq("division", student_div)
            .eq("subjects.course", student_course)
            .gte("lec_timestamp", start)
            .lte("lec_timestamp", end)
            .order("lec_timestamp")
            .execute()
        )
        return response.data

def add_lecture(subject_id, teacher_id, division, timestamp):
    data = {"subject_id" : subject_id, "teacher_id" : teacher_id, "division" : division, "lec_timestamp" : timestamp.isoformat()}
    response = supabase.table("lectures").insert(data).execute()
    return response

def mark_lecture_true(lec_id):
    response = supabase.table("lectures").update({"is_conducted" : True}).eq("lecture_id", lec_id).execute()
    return response.data

def get_lecture_status(lec_id):
    response = supabase.table("lectures").select("is_conducted").eq("lecture_id", lec_id).execute()
    return response.data[0]



#--------------------------------Attendance Logs----------------------------------

def add_attendance_logs(log_data):
    response = supabase.table("attendance_logs").insert(log_data).execute()
    return response

def get_attendance_records(student_id, log_date=None, subject_id=None):

    if student_id and log_date and subject_id:

        start = datetime.combine(
            log_date,
            time(0, 0),
            tzinfo= ZoneInfo("Asia/Kolkata")
        )

        end = datetime.combine(
            log_date, 
            time(23, 59),
            tzinfo= ZoneInfo("Asia/Kolkata")
        )

        response = (
            supabase
            .table("attendance_logs")
            .select("*, lectures!inner(subjects!inner(subject_name))")
            .eq("student_id", student_id)
            .eq("lectures.subject_id", subject_id)
            .gte("timestamp", start)
            .lte("timestamp", end)
            .order("timestamp", desc=True)
            .execute()
        )

        return response.data

    elif student_id and log_date:

        start = datetime.combine(
            log_date, 
            time(0, 0),
            tzinfo= ZoneInfo("Asia/Kolkata")
        )

        end = datetime.combine(
            log_date,
            time(23, 59),
            tzinfo= ZoneInfo("Asia/Kolkata")
        )

        response = (
            supabase
            .table("attendance_logs")
            .select("*, lectures!inner(subjects!inner(subject_name))")
            .eq("student_id", student_id)
            .gte("timestamp", start)
            .lte("timestamp", end)
            .order("timestamp", desc=True)
            .execute()
        )

        return response.data


    elif student_id and subject_id:

        response = (
            supabase
            .table("attendance_logs")
            .select("*, lectures!inner(subjects!inner(subject_name))")
            .eq("student_id", student_id)
            .eq("lectures.subject_id", subject_id)
            .order("timestamp", desc=True)
            .execute()
        )

        return response.data

    elif student_id:
        response = (
            supabase
            .table("attendance_logs")
            .select("*, lectures!inner(subjects!inner(subject_name))")
            .eq("student_id", student_id)
            .order("timestamp", desc=True)
            .execute()
        )
        return response.data

def get_student_logs(student_id):
    response = (
        supabase
        .table("attendance_logs")
        .select("timestamp, is_present, lectures!inner(subjects!inner(subject_name))")
        .eq("student_id", student_id)
        .execute()
    )

    return response.data
