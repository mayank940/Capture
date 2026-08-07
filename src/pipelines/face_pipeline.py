import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from src.database.db import get_all_students
from insightface.app import FaceAnalysis
import numpy as np
import cv2

@st.cache_resource
def load_face_models():

    app = FaceAnalysis(
        name="buffalo_l",
        providers = ["CPUExecutionProvider"]
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    return app


def get_face_embeddings(images_np):
    app = load_face_models()
    embeddings = []
    for img in images_np:
        faces = app.get(img)

        for face in faces:
            embedding = face.normed_embedding
            embeddings.append(embedding)

    return embeddings

def check_difference(embeddings):
    first_n_emb = []
    similarity_threshold = 0.6
    for i, embedding in enumerate(embeddings):
        if i == 0:
            first_n_emb.append(embedding)
            continue

        mean_emb = np.mean(first_n_emb, axis=0)
        similarity_score = cosine_similarity(mean_emb.reshape(1, -1), embedding.reshape(1, -1))[0][0]
        if similarity_score < similarity_threshold:
            return True
        first_n_emb.append(embedding)
    return False


def detect_faces(images_np, students = None):

    embeddings = get_face_embeddings(images_np)
    if not students:
        students = get_all_students()
    detected_students = []
    similarity_threshold = 0.6

    for i, embedding in enumerate(embeddings):
        best_score = -1
        best_match = None
        for student in students:
            stored_emb = np.array(student["face_embedding"])
            mean = np.mean(stored_emb if len(stored_emb.shape) > 1 else [stored_emb], axis =0) 
            similarity_score = cosine_similarity(embedding.reshape(1, -1), mean.reshape(1, -1) )[0][0]
            if similarity_score > best_score:
                best_score = similarity_score
                best_match = student

        
        if best_score > similarity_threshold:
            best_match["is_registered"] = True
        else:
            best_match["is_registered"] = False

        best_match["best_score"] = best_score
        detected_students.append(best_match.copy())

    detected_students.sort(key = lambda x : x["best_score"], reverse=True)
    return detected_students

def detect_faces_attendance(images_np, students):

    embeddings = get_face_embeddings(images_np)

    similarity_threshold = 0.6

    for student in students:
        best_score = -1
        stored_embedding = np.array(student["face_embedding"])
        mean_emb = np.mean(stored_embedding if len(stored_embedding.shape) > 1 else [stored_embedding], axis=0)
        mean_emb /= np.linalg.norm(mean_emb)

        for embedding in embeddings:
            similarity_score = cosine_similarity(mean_emb.reshape(1, -1), embedding.reshape(1, -1))[0][0]
            if similarity_score > best_score:
                best_score = similarity_score


        student["best_score"] = round(best_score*100, 2)
        if best_score > similarity_threshold:
            student["is_present"] = True
        else:
            student["is_present"] = False


        student.pop("face_embedding", None)
        student.pop("username", None)
        student.pop("password", None)
        student.pop("course", None)
        student.pop("division", None)
        student.pop("enrolled_at", None)

def preview_detected_faces(images_np, students):
    app = load_face_models()

    display_imgs = images_np.copy()
    similarity_threshold = 0.6

    for i, img in enumerate(images_np):
        faces = app.get(img)

        for face in faces:
            face_emb = face.normed_embedding
            best_score = -1
            best_match = None

            for student in students:
                embedding = np.array(student["face_embedding"])
                mean = np.mean(embedding if len(embedding.shape) > 1 else [embedding], axis = 0)

                similarity_score = cosine_similarity(face_emb.reshape(1, -1), np.array(mean).reshape(1, -1))[0][0]
                if similarity_score > best_score:
                    best_score = similarity_score
                    best_match = student

            x1, y1, x2, y2 = map(int, face["bbox"])
            w = x2 - x1
            if best_score > similarity_threshold:
                color = (0, 255, 0)
                text = f"{best_match["name"]} {best_score:.2f}" 
            else:
                color = (255, 0, 0)
                text = "unknown"
                
            cv2.rectangle(display_imgs[i], (x1, y1), (x2, y2), color, 5)
            cv2.rectangle(display_imgs[i], (x1, y1-int(w*0.2)), (x1+w, y1), (0, 0, 0), -1)

            cv2.putText(
                display_imgs[i], 
                text, 
                (x1, y1-int(w*0.05)),
                cv2.FONT_HERSHEY_SIMPLEX,
                (w / 315),
                color,
                4
            )

    return display_imgs