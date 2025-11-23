import streamlit as st
import requests
import os

# Ambil URL Backend dari Environment Variable (Sesuai Docker Compose)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🎓 Dashboard Kesiapan Pendidikan (DevMLOps)")

st.sidebar.header("Status Sistem")
if st.sidebar.button("Cek Koneksi API"):
    try:
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 200:
            st.sidebar.success("Backend Terhubung! ✅")
            st.sidebar.json(response.json())
        else:
            st.sidebar.error(f"Error: {response.status_code}")
    except Exception as e:
        st.sidebar.error(f"Gagal terkoneksi: {e}")

st.write("Selamat datang di sistem analisis klaster pendidikan.")