# ana_test.py
import streamlit as st
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API anahtarını al
api_key = os.getenv("GEMINI_API_KEY", "")

st.title("Bitki Doktoru - Test")

st.write(f"API anahtarı var mı: {'Evet' if api_key else 'Hayır'}")

st.write("Bu basit bir Streamlit testi.")

if st.button("Tıkla"):
    st.success("Buton çalışıyor!")