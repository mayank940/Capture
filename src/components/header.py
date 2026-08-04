import streamlit as st
import base64

logo_path = "images/project_logo.png"
with open(logo_path, "rb")as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")

def header_home():


    st.markdown(f"""
        <div style=" display:flex; gap: 15px; align-items: center; margin-bottom: 25px;">
            <img src="data:image/png;base64,{b64_image}" style=" width:90px;" />
            <div>
                <h2>Capture</h2>
                <h3>AI Powered Attendance</h3>
            </div>        
        </div>

    """, unsafe_allow_html= True)


def header_dashboard():

    st.markdown(f"""
        <div style=" display:flex; gap: 15px; align-items: center;">
            <img src="data:image/png;base64,{b64_image}" style=" width:80px;" />
            <div>
                <h2 style=" font-size: 3.5rem;">Capture</h2>
            </div>        
        </div>

    """, unsafe_allow_html= True)