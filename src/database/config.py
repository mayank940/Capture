import streamlit as st
from supabase import create_client, Client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    url,
    key
)