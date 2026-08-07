import streamlit as st
from src.ui.style_base_layout import style_base_layout

def style_home_screen():
    
    style_base_layout()
    st.markdown(""" 
        <style>

            .stApp div[data-testid="stColumn"]{
                background-color: var(--card_background);    
                padding: 1.5rem;
                border-radius: 1.5rem;
                box-shadow: 0 6px 8px 2px rgba(0, 0, 0, 0.3);
                transition: transform 250ms ease-in-out, box-shadow 250ms ease-in-out;
            }
                
            .stApp div[data-testid="stColumn"]:hover{
                transform: translateY(-3px);
                cursor : pointer;
                box-shadow: 0 4px 20px  rgba(0, 0, 0, 0.08);    
            }
            
            div[data-testid="stColumn"] div[data-testid="stVerticalBlock"]{
                gap: 30px;
            }
        </style>
    """, unsafe_allow_html = True)