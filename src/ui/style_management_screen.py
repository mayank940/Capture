import streamlit as st
from src.ui.style_base_layout import style_base_layout
from streamlit.components.v1 import components

def style_management_screen():
    style_base_layout()

    st.markdown("""
    <style>

        div[data-testid="stTextInput"] input:disabled{
            color : black;
        }

        div[data-testid="stMarkdown"] div[data-testid="stMarkdownContainer"] p{
            margin-bottom: 0.5rem;
        }

    </style>

    """, unsafe_allow_html=True)

def remove_focus():
    components.html("""
        <script>

        let eyeBtns = window.parent.document.querySelectorAll("div[data-testid='stTextInputRootElement'] button")
                    
        for (let eyeBtn of eyeBtns){
            eyeBtn.tabIndex = -1
            console.log(eyeBtn)
        }                        
        </script>

    """, height=0)