import streamlit as st
import requests

# Konfigurasi Halaman (Harus di baris pertama)
st.set_page_config(
    page_title="Education Readiness MLOps",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Info
st.sidebar.image("https://img.icons8.com/fluency/96/education.png", width=80)
st.sidebar.title("DevMLOps v1.0")
st.sidebar.info(
    """
    **Sistem Analisis Kesiapan Pendidikan**
    Menggunakan K-Means Clustering & MLOps Pipeline.
    """
)

# Konten Utama
st.title("🎓 Sistem Kesiapan Pendidikan Indonesia")
st.markdown("### *Data-Driven Policy Making Platform*")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
    Selamat datang di Dashboard Sistem Pendukung Keputusan Kesiapan Pendidikan.
    Sistem ini memproses data pendidikan provinsi di Indonesia untuk mengelompokkan daerah
    berdasarkan kesiapan infrastruktur TIK dan kompetensi guru.

    **Pilih Modul di Sidebar:**
    * **🏢 Dashboard Publik:** Untuk melihat peta sebaran dan profil klaster pendidikan.
    * **🧪 Data Scientist Lab:** Untuk memonitor performa model, drift, dan explainability.
    * **⚙️ Data Management:** Untuk memperbarui data dan melatih ulang model (Retraining).
    """
    )

    # Status Service Check (Backend & Mage)
    st.subheader("System Health Check")

    try:
        # Cek Backend API
        # Gunakan nama container 'backend' jika di dalam docker network
        res = requests.get("http://backend:8000/")
        if res.status_code == 200:
            st.success(f"✅ Prediction API Online: {res.json()}")
        else:
            st.error("❌ Prediction API Error")
    except:  # noqa: E722
        st.warning("⚠️ Cannot connect to Prediction API (Is Docker running?)")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3074/3074066.png", width=200)

st.markdown("---")
st.caption("Dikembangkan oleh [Nama Anda] - Tugas Akhir MLOps")
