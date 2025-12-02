import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Education Cluster AI", page_icon="🎓", layout="wide")

# URL Backend (Ambil dari env variable atau default localhost)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# --- JUDUL & HEADER ---
st.title("🎓 Sistem Analisis Kesiapan Pendidikan AI")
st.markdown(
    """
Aplikasi ini membantu memetakan kesiapan provinsi di 
Indonesia untuk implementasi kurikulum AI 
berdasarkan data infrastruktur dan kompetensi pendidikan.
"""
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Panel Kontrol")
    st.info(
        "Pastikan backend FastAPI sudah berjalan dan model telah dilatih via Mage AI."
    )

    # Cek Status Backend
    try:
        res = requests.get(f"{BACKEND_URL}/")
        if res.status_code == 200:
            status = res.json()
            st.success("Backend: Terhubung ✅")
            st.caption(f"Model Status: {status.get('model_status', 'Unknown')}")
        else:
            st.error("Backend: Error ❌")
    except Exception:
        st.error("Backend: Offline ❌")

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(
    ["📊 Prediksi & Upload", "📈 Visualisasi Data", "📋 Profil Data"]
)

# --- TAB 1: PREDIKSI ---
with tab1:
    st.header("Upload Data Provinsi")
    st.markdown("Unggah file CSV/Excel berisi data indikator pendidikan per provinsi.")

    uploaded_file = st.file_uploader("Pilih file CSV/XLSX", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            # Baca file ke Pandas DataFrame untuk preview
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Simpan di session state agar bisa dipakai di tab lain
            st.session_state["df_uploaded"] = df

            st.subheader("Preview Data")
            st.dataframe(df.head())

            # Tombol Prediksi (Simulasi Loop ke API)
            if st.button("🚀 Analisis Klaster (Kirim ke AI)"):
                results = []
                progress_bar = st.progress(0)

                # Kita asumsikan user ingin memprediksi baris per baris
                for index, row in df.iterrows():
                    payload = {
                        "persen_sekolah_internet_sd": row.get(
                            "persen_sekolah_internet_sd", 0
                        ),
                        "persen_sekolah_internet_smp": row.get(
                            "persen_sekolah_internet_smp", 0
                        ),
                        "persen_sekolah_internet_sma": row.get(
                            "persen_sekolah_internet_sma", 0
                        ),
                        "persen_guru_sertifikasi_sd": row.get(
                            "persen_guru_sertifikasi_sd", 0
                        ),
                        "persen_guru_sertifikasi_smp": row.get(
                            "persen_guru_sertifikasi_smp", 0
                        ),
                        "persen_guru_sertifikasi_sma": row.get(
                            "persen_guru_sertifikasi_sma", 0
                        ),
                        "rasio_siswa_guru_sd": row.get("rasio_siswa_guru_sd", 0),
                        "rasio_siswa_guru_smp": row.get("rasio_siswa_guru_smp", 0),
                        "rasio_siswa_guru_sma": row.get("rasio_siswa_guru_sma", 0),
                        "rasio_siswa_komputer_sd": row.get(
                            "rasio_siswa_komputer_sd", 0
                        ),
                        "rasio_siswa_komputer_smp": row.get(
                            "rasio_siswa_komputer_smp", 0
                        ),
                        "rasio_siswa_komputer_sma": row.get(
                            "rasio_siswa_komputer_sma", 0
                        ),
                        "persen_lulus_akm_literasi": row.get(
                            "persen_lulus_akm_literasi", 0
                        ),
                        "persen_lulus_akm_numerasi": row.get(
                            "persen_lulus_akm_numerasi", 0
                        ),
                    }

                    try:
                        resp = requests.post(f"{BACKEND_URL}/predict", json=payload)
                        if resp.status_code == 200:
                            res_json = resp.json()
                            results.append(
                                {
                                    "Provinsi": row.get("Provinsi", f"Data {index}"),
                                    "Klaster": res_json["cluster_id"],
                                    "Label": res_json["label"],
                                }
                            )
                    except Exception as e:
                        st.error(f"Gagal memproses baris {index}: {e}")

                    progress_bar.progress((index + 1) / len(df))

                # Tampilkan Hasil
                if results:
                    res_df = pd.DataFrame(results)
                    st.success("Analisis Selesai!")
                    st.session_state["df_results"] = res_df  # Simpan hasil

                    # Tampilkan metrik ringkas
                    col1, col2, col3 = st.columns(3)
                    counts = res_df["Label"].value_counts()
                    col1.metric(
                        "Tinggi (Siap)", counts.get("Tinggi (High Readiness)", 0)
                    )
                    col2.metric("Sedang", counts.get("Sedang (Medium Readiness)", 0))
                    col3.metric("Rendah", counts.get("Rendah (Low Readiness)", 0))

                    st.dataframe(res_df)

        except Exception as e:
            st.error(f"Error membaca file: {e}")

# --- TAB 2: VISUALISASI ---
with tab2:
    st.header("Visualisasi Data")

    if "df_uploaded" in st.session_state:
        df = st.session_state["df_uploaded"]

        # 1. Korelasi Heatmap (Numerik saja)
        st.subheader("Korelasi Indikator")
        numeric_df = df.select_dtypes(include=["float64", "int64"])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig_corr = px.imshow(
                corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r"
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        # 2. Scatter Plot Interaktif
        st.subheader("Analisis Sebaran (Scatter Plot)")
        col_x = st.selectbox(
            "Pilih Sumbu X", df.columns, index=min(1, len(df.columns) - 1)
        )
        col_y = st.selectbox(
            "Pilih Sumbu Y", df.columns, index=min(2, len(df.columns) - 1)
        )

        # Jika hasil prediksi ada, gunakan warna berdasarkan klaster
        color_col = None
        if "df_results" in st.session_state and len(
            st.session_state["df_results"]
        ) == len(df):
            df["Klaster_Label"] = st.session_state["df_results"]["Label"].values
            color_col = "Klaster_Label"

        fig_scatter = px.scatter(
            df,
            x=col_x,
            y=col_y,
            color=color_col,
            hover_data=df.columns,
            title=f"{col_x} vs {col_y}",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        st.info("Silakan upload data di Tab 'Prediksi' terlebih dahulu.")

# --- TAB 3: PROFIL DATA ---
with tab3:
    st.header("Statistik & Kualitas Data")

    if "df_uploaded" in st.session_state:
        df = st.session_state["df_uploaded"]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Tipe Data")
            st.write(df.dtypes.astype(str))

        with col2:
            st.subheader("Missing Values")
            st.write(df.isnull().sum())

        st.subheader("Statistik Deskriptif")
        st.dataframe(df.describe())
    else:
        st.info("Silakan upload data di Tab 'Prediksi' terlebih dahulu.")
