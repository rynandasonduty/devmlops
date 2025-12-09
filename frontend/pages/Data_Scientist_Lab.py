import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- NEW: METADATA INSIGHT ---
METADATA_PATH = "/app/artifacts/cluster_metadata.json"

st.subheader("🏷️ Model Interpretation Status")

if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    # Tampilkan sebagai kartu informasi
    cols = st.columns(len(metadata))
    for i, (cluster_id, label) in enumerate(metadata.items()):
        with cols[i]:
            st.success(f"**Cluster {cluster_id}**\n\n📌 {label}")
else:
    st.warning(
        "⚠️ Metadata label belum tersedia. Model mungkin belum dilatih dengan versi terbaru."
    )

st.divider()

st.set_page_config(page_title="Data Scientist Lab", page_icon="🧪", layout="wide")

st.title("🧪 Laboratorium AI & Eksperimen")
st.markdown(
    "Monitoring performa model, deteksi drift, dan interpretasi (Explainability)."
)

# Path Artifacts
ARTIFACTS_DIR = "/app/artifacts"

# Cek apakah folder ada
if not os.path.exists(ARTIFACTS_DIR):
    st.error(
        f"⚠️ Folder Artifacts tidak ditemukan di {ARTIFACTS_DIR}. Pastikan volume Docker terpasang."
    )
    st.stop()

# --- TABS NAVIGASI ---
tab1, tab2, tab3 = st.tabs(
    ["📈 Training Metrics", "🔍 Model Explainability (SHAP)", "⚠️ Data Drift Monitor"]
)

# TAB 1: HASIL TRAINING (Elbow, Silhouette, PCA)
with tab1:
    st.header("Evaluasi Training Terakhir")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Elbow Method")
        if os.path.exists(f"{ARTIFACTS_DIR}/elbow_method.png"):
            st.image(
                f"{ARTIFACTS_DIR}/elbow_method.png",
                caption="Mencari k optimal (Inertia)",
            )
        else:
            st.warning("Grafik Elbow belum tersedia.")

    with col2:
        st.subheader("Silhouette Score")
        if os.path.exists(f"{ARTIFACTS_DIR}/silhouette_score.png"):
            st.image(
                f"{ARTIFACTS_DIR}/silhouette_score.png",
                caption="Kualitas Klaster (Separasi)",
            )
        else:
            st.warning("Grafik Silhouette belum tersedia.")

    st.divider()
    st.subheader("Visualisasi Klaster (PCA 2D)")
    if os.path.exists(f"{ARTIFACTS_DIR}/pca_clusters.png"):
        st.image(
            f"{ARTIFACTS_DIR}/pca_clusters.png",
            use_column_width=True,
            caption="Proyeksi Data 2 Dimensi",
        )

# TAB 2: EXPLAINABILITY (SHAP)
with tab2:
    st.header("Interpretasi Model (Why?)")
    st.write("Fitur apa yang paling berpengaruh dalam menentukan klaster suatu daerah?")

    if os.path.exists(f"{ARTIFACTS_DIR}/shap_summary.png"):
        st.image(f"{ARTIFACTS_DIR}/shap_summary.png", use_column_width=True)
        st.caption(
            "Grafik di atas menunjukkan Feature Importance berdasarkan SHAP Values."
        )
    else:
        st.warning(
            "Grafik SHAP belum tersedia. Pastikan pipeline `explain_model_shap` sukses."
        )

# TAB 3: DRIFT MONITORING (Evidently HTML)
with tab3:
    st.header("Data Drift & Quality Check")

    drift_file = f"{ARTIFACTS_DIR}/data_drift_report.html"

    if os.path.exists(drift_file):
        st.success("✅ Laporan Evidently ditemukan. Menampilkan report...")

        # Baca file HTML
        with open(drift_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Tampilkan HTML di Streamlit
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.error(
            "❌ Laporan Data Drift tidak ditemukan. Jalankan pipeline stage drift_report."
        )
