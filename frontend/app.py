import streamlit as st
import requests
import os
import json

# Setup halaman
st.set_page_config(page_title="Prediksi Klaster Pendidikan", layout="wide")

# Judul dan Deskripsi
st.title("🎓 Sistem Klasterisasi Kesiapan Pendidikan")
st.markdown("""
Aplikasi ini menggunakan Machine Learning (K-Means) untuk mengelompokkan provinsi 
berdasarkan indikator infrastruktur, guru, dan hasil AKM.
""")

# URL Backend (diambil dari env docker-compose atau default localhost)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# --- FORM INPUT ---
with st.form("prediction_form"):
    st.header("📝 Input Data Pendidikan")
    
    # Kita bagi input menjadi 3 kolom agar rapi
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌐 Akses Internet (%)")
        p_inet_sd = st.number_input("SD Internet", 0.0, 100.0, 80.0)
        p_inet_smp = st.number_input("SMP Internet", 0.0, 100.0, 85.0)
        p_inet_sma = st.number_input("SMA Internet", 0.0, 100.0, 90.0)

        st.subheader("📊 Hasil AKM (%)")
        p_akm_lit = st.number_input("Lulus AKM Literasi", 0.0, 100.0, 50.0)
        p_akm_num = st.number_input("Lulus AKM Numerasi", 0.0, 100.0, 40.0)

    with col2:
        st.subheader("insentif Guru Sertifikasi (%)")
        p_guru_sd = st.number_input("Guru SD Sertifikasi", 0.0, 100.0, 40.0)
        p_guru_smp = st.number_input("Guru SMP Sertifikasi", 0.0, 100.0, 45.0)
        p_guru_sma = st.number_input("Guru SMA Sertifikasi", 0.0, 100.0, 50.0)

    with col3:
        st.subheader("👥 Rasio Siswa : Guru")
        r_guru_sd = st.number_input("Rasio Siswa/Guru SD", 0.0, 100.0, 15.0)
        r_guru_smp = st.number_input("Rasio Siswa/Guru SMP", 0.0, 100.0, 12.0)
        r_guru_sma = st.number_input("Rasio Siswa/Guru SMA", 0.0, 100.0, 10.0)

        st.subheader("💻 Rasio Siswa : Komputer")
        r_komp_sd = st.number_input("Rasio Siswa/Komputer SD", 0.0, 100.0, 5.0)
        r_komp_smp = st.number_input("Rasio Siswa/Komputer SMP", 0.0, 100.0, 3.0)
        r_komp_sma = st.number_input("Rasio Siswa/Komputer SMA", 0.0, 100.0, 2.0)

    # Tombol Submit
    submitted = st.form_submit_button("🔍 Prediksi Klaster")

# --- LOGIKA PREDIKSI ---
if submitted:
    # 1. Susun Payload JSON (Sesuai Schema Backend)
    payload = {
        "persen_sekolah_internet_sd": p_inet_sd,
        "persen_sekolah_internet_smp": p_inet_smp,
        "persen_sekolah_internet_sma": p_inet_sma,
        "persen_guru_sertifikasi_sd": p_guru_sd,
        "persen_guru_sertifikasi_smp": p_guru_smp,
        "persen_guru_sertifikasi_sma": p_guru_sma,
        "rasio_siswa_guru_sd": r_guru_sd,
        "rasio_siswa_guru_smp": r_guru_smp,
        "rasio_siswa_guru_sma": r_guru_sma,
        "rasio_siswa_komputer_sd": r_komp_sd,
        "rasio_siswa_komputer_smp": r_komp_smp,
        "rasio_siswa_komputer_sma": r_komp_sma,
        "persen_lulus_akm_literasi": p_akm_lit,
        "persen_lulus_akm_numerasi": p_akm_num
    }

    # 2. Kirim Request ke Backend
    try:
        with st.spinner("Sedang menganalisis data..."):
            response = requests.post(f"{BACKEND_URL}/predict", json=payload)
            
        if response.status_code == 200:
            result = response.json()
            label = result['label']
            cluster_id = result['cluster_id']
            
            # Tampilkan Hasil dengan Warna Menarik
            st.success("✅ Prediksi Selesai!")
            
            # Logic warna berdasarkan hasil (Hardcoded untuk contoh K=3)
            if "Tinggi" in label:
                st.metric(label="Hasil Klaster", value=label, delta="Sangat Baik")
                st.balloons()
            elif "Sedang" in label:
                st.metric(label="Hasil Klaster", value=label, delta="Cukup", delta_color="off")
            else:
                st.metric(label="Hasil Klaster", value=label, delta="-Perlu Perhatian", delta_color="inverse")
                
            st.info(f"Data ini masuk ke dalam Cluster ID: {cluster_id}")
            
        else:
            st.error(f"Gagal memprediksi. Error: {response.text}")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan koneksi ke Backend: {e}")
        st.warning("Pastikan container 'backend' sudah berjalan.")