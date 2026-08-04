import streamlit as st
from src.ui.style_base_layout import style_base_layout
import streamlit.components.v1 as components

def style_student_login_comps():
    style_base_layout()

    st.markdown("""
    <style>

    </style>

    """, unsafe_allow_html=True)

def style_student_portal():
    style_base_layout()
    st.markdown("""
    <style>

        div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"] {
            background-color : var(--card_background);
            margin-top: 1rem;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            padding: 1.25rem 1.5rem;
            border : 1px solid var(--input_border);
            border-radius: 0.8rem;
            transform: translateY(2px);
            transition: box-shadow 200ms ease-out, transform 150ms ease-out;
        }

    
        div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]:hover{
            cursor : pointer;
            box-shadow : 0 0 3px rgba(0, 0, 0, 0.2);
            transform : scale(1.02);
        }

        div[data-testid='stLayoutWrapper] > div[data-testid="stVerticalBlock"] h3 span{
            color : var(--text_primary);
            padding: 0.8rem 0 1.5rem;
        }

        div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"] div[data-testid="stMarkdown"]{
            margin-left: 5px;
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