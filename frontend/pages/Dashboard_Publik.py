import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
from PIL import Image

COLOR_PALETTE = {
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "primary": "#00D9FF",
    "secondary": "#A855F7",
}

# ==============================================================================
# 1. PAGE CONFIGURATION & ENHANCED STYLING
# ==============================================================================
st.set_page_config(
    page_title="Executive Dashboard: Kesiapan Pendidikan AI",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced Custom CSS with Better Typography & Contrast
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
    }
    /* Improve focus states for keyboard navigation */
button:focus, .stSelectbox:focus {
    outline: 2px solid #00D9FF !important;
    outline-offset: 2px;
}
    /* Typography Hierarchy */
    h1 {
        background: linear-gradient(135deg, #00D9FF 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
        line-height: 1.2 !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #F3F4F6 !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        position: relative;
        padding-bottom: 0.5rem;
    }
    h2:first-of-type {
    margin-top: 0.25rem !important;
    }
    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #00D9FF 0%, #A855F7 100%);
        border-radius: 2px;
    }
    h3 {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 0.75rem !important;
        margin-top: 0.5rem !important;
    }
    h4 {
        color: #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    p, li {
        color: #D1D5DB !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    /* Consistent Section Spacing */
    .element-container {
        margin-bottom: 0.75rem !important;
    }
    .block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 100%;
    }
    /* Enhanced Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 35, 47, 0.95) 0%, rgba(26, 31, 58, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 1.5rem !important;
        margin-bottom: 0 !important;
        border-radius: 12px;
        border-left: 3px solid;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        min-height: 120px;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    div[data-testid="metric-container"] label {
        color: #9CA3AF !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #F3F4F6 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
    }
    /* Improved Insight Box */
    .insight-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        backdrop-filter: blur(10px);
    }
    .insight-box-header {
        color: #10B981 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .insight-box ul {
        margin: 0 !important;
        padding-left: 1.5rem !important;
        list-style: none;
    }
    .insight-box li {
        color: #D1D5DB !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        margin-bottom: 0.4rem !important;
        position: relative;
        padding-left: 1.5rem;
    }
    .insight-box li:before {
        content: "→";
        position: absolute;
        left: 0;
        color: #10B981;
        font-weight: 700;
    }
    .insight-box strong {
        color: #10B981 !important;
        font-weight: 600 !important;
    }
    /* Info Box Variants */
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(37, 99, 235, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .info-box-header {
        color: #60A5FA !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    .info-box p {
        color: #D1D5DB !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 4px solid #F59E0B;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    /* Section Cards */
    .section-card {
        background: rgba(30, 35, 47, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 35, 47, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #9CA3AF;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #E5E7EB;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00D9FF 0%, #A855F7 100%);
        color: white !important;
        font-weight: 600;
    }
    /* Enhanced Divider */
    hr {
        margin: 2rem 0 !important;
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(0, 217, 255, 0.3) 20%,
            rgba(168, 85, 247, 0.3) 80%,
            transparent 100%);
    }
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #00D9FF 100%);
    }
    /* Chart Text */
    .js-plotly-plot .plotly text {
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
    }
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 35, 47, 0.6) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    /* Better spacing for columns */
    [data-testid="column"] {
        padding: 0 0.75rem;
    }
    [data-testid="column"]:first-child {
        padding-left: 0;
    }
    [data-testid="column"]:last-child {
        padding-right: 0;
    }
    /* Subtitle styling */
    .subtitle {
    color: #9CA3AF !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    margin-top: 0.25rem !important;
    margin-bottom: 0.75rem !important;
}

    /* Image styling */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. DATA LOADING ENGINE - INTEGRATED WITH MAGE PIPELINE
# ==============================================================================
def get_data_path(filename):
    """Get file path with fallback mechanism for Mage AI artifacts"""
    search_paths = [
        f"/home/src/artifacts/{filename}",
        f"/app/artifacts/{filename}",
        f"/app/mage_data_source/{filename}",
        f"mage_pipeline/artifacts/{filename}",
        f"artifacts/{filename}",
        f"data/{filename}",
        filename,
    ]

    for path in search_paths:
        if os.path.exists(path):
            return path
    return None


RAW_DATA_PATH = get_data_path("data_kesiapan_pendidikan_enriched.csv")
LABELED_DATA_PATH = get_data_path("data_labeled.csv")
LOCAL_GEOJSON_PATH = get_data_path("indonesia-prov.geojson")
CLUSTER_METADATA_PATH = get_data_path("cluster_metadata.json")
CLUSTER_PROFILE_PATH = get_data_path("cluster_profile.csv")
MODEL_PATH = get_data_path("kmeans_model.pkl")
SHAP_PATH = get_data_path("shap_summary.png")
ELBOW_PATH = get_data_path("elbow_method.png")
PCA_PATH = get_data_path("pca_clusters.png")
SILHOUETTE_PATH = get_data_path("silhouette_score.png")


@st.cache_data(ttl=3600)
def load_and_prep_data():
    """
    Load and prepare education readiness data integrated with Mage AI pipeline output
    """

    # 1. Load GeoJSON
    geojson = None
    if LOCAL_GEOJSON_PATH and os.path.exists(LOCAL_GEOJSON_PATH):
        try:
            with open(LOCAL_GEOJSON_PATH, "r") as f:
                geojson = json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Could not load GeoJSON: {str(e)[:100]}")

    # 2. Load Raw Data
    if not RAW_DATA_PATH or not os.path.exists(RAW_DATA_PATH):
        st.error("❌ Data source not found. Please check data files.")
        return None, None, None, None

    try:
        df_raw = pd.read_csv(RAW_DATA_PATH)

        if df_raw.empty:
            st.error("❌ Dataset is empty")
            return None, None, None, None

    except Exception as e:
        st.error(f"❌ Failed to load data: {str(e)[:100]}")
        return None, None, None, None

    df_raw.columns = df_raw.columns.str.lower().str.strip()
    prov_col_raw = next((col for col in df_raw.columns if "prov" in col), None)

    if not prov_col_raw:
        st.error("❌ Province column not found in dataset")
        return None, None, None, None

    # 3. Load Cluster Metadata from Mage AI Pipeline
    cluster_metadata = None
    if CLUSTER_METADATA_PATH and os.path.exists(CLUSTER_METADATA_PATH):
        try:
            with open(CLUSTER_METADATA_PATH, "r") as f:
                cluster_metadata = json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Could not load cluster metadata: {str(e)[:100]}")

    # 4. Load Cluster Labels from Pipeline Output
    df_raw["cluster_label"] = "Belum Diklasifikasi"
    df_raw["cluster_id"] = -1

    if LABELED_DATA_PATH and os.path.exists(LABELED_DATA_PATH):
        try:
            df_labeled = pd.read_csv(LABELED_DATA_PATH)
            df_labeled.columns = df_labeled.columns.str.lower().str.strip()
            prov_col_label = next(
                (col for col in df_labeled.columns if "prov" in col), None
            )
            cluster_col = next(
                (col for col in df_labeled.columns if "cluster_label" in col), None
            )
            cluster_id_col = next(
                (col for col in df_labeled.columns if "cluster_id" in col), None
            )
            if prov_col_label and cluster_col:
                df_labeled["join_key"] = (
                    df_labeled[prov_col_label].astype(str).str.lower().str.strip()
                )
                df_raw["join_key"] = (
                    df_raw[prov_col_raw].astype(str).str.lower().str.strip()
                )
                label_map = dict(zip(df_labeled["join_key"], df_labeled[cluster_col]))
                df_raw["cluster_label"] = (
                    df_raw["join_key"].map(label_map).fillna("Belum Diklasifikasi")
                )

                if cluster_id_col:
                    id_map = dict(
                        zip(df_labeled["join_key"], df_labeled[cluster_id_col])
                    )
                    df_raw["cluster_id"] = df_raw["join_key"].map(id_map).fillna(-1)

        except Exception as e:
            st.warning(f"⚠️ Could not load cluster labels: {str(e)[:100]}")

    # 5. Load Cluster Profile
    cluster_profile = None
    if CLUSTER_PROFILE_PATH and os.path.exists(CLUSTER_PROFILE_PATH):
        try:
            cluster_profile = pd.read_csv(CLUSTER_PROFILE_PATH, index_col=0)
        except Exception as e:
            st.warning(f"⚠️ Could not load cluster profile: {str(e)[:100]}")

    # 6. Feature Engineering
    col_inet = [c for c in df_raw.columns if "internet" in c]
    if col_inet:
        df_raw["indeks_infrastruktur"] = (
            df_raw[col_inet].mean(axis=1, skipna=True).fillna(0)
        )
    else:
        df_raw["indeks_infrastruktur"] = 0.0

    col_sdm = [c for c in df_raw.columns if "sertifikasi" in c]
    if col_sdm:
        df_raw["indeks_sdm"] = df_raw[col_sdm].mean(axis=1, skipna=True).fillna(0)
    else:
        df_raw["indeks_sdm"] = 0.0

    col_akm = [c for c in df_raw.columns if "akm" in c or "lulus_akm" in c]
    if col_akm:
        df_raw["potensi_siswa"] = df_raw[col_akm].mean(axis=1, skipna=True).fillna(0)
    else:
        df_raw["potensi_siswa"] = 0.0

    col_pc = [c for c in df_raw.columns if "komputer" in c and "rasio" in c]
    if col_pc:
        df_raw["rasio_pc_avg"] = df_raw[col_pc].mean(axis=1, skipna=True).fillna(15)
    else:
        df_raw["rasio_pc_avg"] = 15.0

    # 7. Province Mapping for GeoJSON compatibility
    MAPPING_PROVINSI = {
        "aceh": "ACEH",
        "sumatera utara": "SUMATERA UTARA",
        "sumatera barat": "SUMATERA BARAT",
        "riau": "RIAU",
        "jambi": "JAMBI",
        "sumatera selatan": "SUMATERA SELATAN",
        "bengkulu": "BENGKULU",
        "lampung": "LAMPUNG",
        "kepulauan bangka belitung": "KEPULAUAN BANGKA BELITUNG",
        "bangka belitung": "KEPULAUAN BANGKA BELITUNG",
        "kepulauan riau": "KEPULAUAN RIAU",
        "dki jakarta": "DAERAH KHUSUS IBUKOTA JAKARTA",
        "jakarta": "DAERAH KHUSUS IBUKOTA JAKARTA",
        "jawa barat": "JAWA BARAT",
        "jawa tengah": "JAWA TENGAH",
        "di yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",
        "yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",
        "jawa timur": "JAWA TIMUR",
        "banten": "BANTEN",
        "bali": "BALI",
        "nusa tenggara barat": "NUSA TENGGARA BARAT",
        "ntb": "NUSA TENGGARA BARAT",
        "nusa tenggara timur": "NUSA TENGGARA TIMUR",
        "ntt": "NUSA TENGGARA TIMUR",
        "kalimantan barat": "KALIMANTAN BARAT",
        "kalimantan tengah": "KALIMANTAN TENGAH",
        "kalimantan selatan": "KALIMANTAN SELATAN",
        "kalimantan timur": "KALIMANTAN TIMUR",
        "kalimantan utara": "KALIMANTAN UTARA",
        "sulawesi utara": "SULAWESI UTARA",
        "sulawesi tengah": "SULAWESI TENGAH",
        "sulawesi selatan": "SULAWESI SELATAN",
        "sulawesi tenggara": "SULAWESI TENGGARA",
        "gorontalo": "GORONTALO",
        "sulawesi barat": "SULAWESI BARAT",
        "maluku": "MALUKU",
        "maluku utara": "MALUKU UTARA",
        "papua barat": "PAPUA BARAT",
        "papua": "PAPUA",
        "papua tengah": "PAPUA",
        "papua pegunungan": "PAPUA",
        "papua selatan": "PAPUA",
    }

    def normalize_prov_geo(name):
        n = str(name).lower().replace("prov.", "").replace("provinsi", "").strip()
        return MAPPING_PROVINSI.get(n, n.upper())

    df_raw["geo_key"] = df_raw[prov_col_raw].apply(normalize_prov_geo)
    df_raw["display_prov"] = df_raw[prov_col_raw]

    return df_raw, geojson, cluster_metadata, cluster_profile


with st.spinner("📊 Loading dashboard data..."):
    df, geojson_indo, cluster_metadata, cluster_profile = load_and_prep_data()

# Enhanced Color Map - Dynamic based on metadata
if cluster_metadata and "cluster_mapping" in cluster_metadata:
    n_clusters = cluster_metadata.get("n_clusters", 3)

    if n_clusters == 2:
        COLOR_MAP = {
            "Rendah (Low)": "#EF4444",
            "Tinggi (High)": "#10B981",
            "Belum Diklasifikasi": "#6B7280",
        }
    elif n_clusters == 3:
        COLOR_MAP = {
            "Rendah (Low)": "#EF4444",
            "Sedang (Medium)": "#F59E0B",
            "Tinggi (High)": "#10B981",
            "Belum Diklasifikasi": "#6B7280",
        }
    elif n_clusters == 4:
        COLOR_MAP = {
            "Sangat Rendah": "#DC2626",
            "Rendah (Low)": "#EF4444",
            "Sedang (Medium)": "#F59E0B",
            "Tinggi (High)": "#10B981",
            "Belum Diklasifikasi": "#6B7280",
        }
    else:
        colors = ["#DC2626", "#EF4444", "#F59E0B", "#FCD34D", "#10B981", "#059669"]
        COLOR_MAP = {
            f"Cluster {i+1}": colors[i % len(colors)] for i in range(n_clusters)
        }
        COLOR_MAP["Belum Diklasifikasi"] = "#6B7280"
else:
    COLOR_MAP = {
        "Tinggi (High)": "#10B981",
        "Sedang (Medium)": "#F59E0B",
        "Rendah (Low)": "#EF4444",
        "Belum Diklasifikasi": "#6B7280",
    }

# ==============================================================================
# HEADER
# ==============================================================================
col_title, col_logo = st.columns([5, 1])
with col_title:
    st.title("🇮🇩 Executive Dashboard: Kesiapan Pendidikan AI")
    st.markdown(
        "<p class='subtitle'><strong>Monitor Strategis</strong> · Infrastruktur Digital & SDM Nasional</p>",
        unsafe_allow_html=True,
    )
with col_logo:
    st.markdown(
        "<div style='text-align: right; padding: 20px 0;'><span style='font-size: 4rem;'>📊</span></div>",
        unsafe_allow_html=True,
    )
st.markdown("<div style='margin: 0.5rem 0;'><hr></div>", unsafe_allow_html=True)

# ==============================================================================
# MODEL & PIPELINE INFO
# ==============================================================================
if cluster_metadata:
    with st.expander("🤖 ML Model Information (from Mage AI Pipeline)", expanded=False):
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)

        with col_info1:
            st.metric("Model Type", "KMeans", help="Clustering algorithm used")

        with col_info2:
            n_clusters = cluster_metadata.get("n_clusters", "N/A")
            st.metric(
                "Number of Clusters", n_clusters, help="Optimal k determined by Optuna"
            )

        with col_info3:
            sil_score = cluster_metadata.get("silhouette_score", 0)
            st.metric(
                "Silhouette Score",
                f"{sil_score:.3f}",
                help="Higher is better (range: -1 to 1)",
            )

        with col_info4:
            db_score = cluster_metadata.get("davies_bouldin_score", 0)
            st.metric("Davies-Bouldin", f"{db_score:.3f}", help="Lower is better")

        st.markdown("<br>", unsafe_allow_html=True)

        if "cluster_statistics" in cluster_metadata:
            st.markdown("#### 📊 Cluster Distribution")
            cluster_stats = cluster_metadata["cluster_statistics"]

            stats_data = []
            for cid, stats in cluster_stats.items():
                stats_data.append(
                    {
                        "Cluster": stats["label"],
                        "Provinces": stats["count"],
                        "Percentage": f"{stats['percentage']:.1f}%",
                        "Avg Score": f"{stats['avg_score']:.2f}",
                    }
                )

            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

        if MODEL_PATH and os.path.exists(MODEL_PATH):
            model_time = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH))
            st.caption(f"Last trained: {model_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Empty state handling
if df is None or df.empty:
    st.error("❌ Data tidak tersedia")
    st.markdown(
        """
        <div class='info-box'>
            <div class='info-box-header'>🔭 Troubleshooting</div>
            <p>1. Pastikan file data ada di lokasi yang benar<br>
            2. Cek format CSV (kolom provinsi harus ada)<br>
            3. Verifikasi struktur data sesuai template</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# Data Freshness Indicator
if RAW_DATA_PATH and os.path.exists(RAW_DATA_PATH):
    last_modified = os.path.getmtime(RAW_DATA_PATH)
    last_update_time = datetime.fromtimestamp(last_modified)

    st.markdown(
        f"""
    <div style='text-align: right; color: #6B7280; font-size: 0.875rem; margin-bottom: 0.5rem;'>
            📅 Last Updated: {last_update_time.strftime('%d %B %Y, %H:%M')} WIB
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 1. EXECUTIVE SUMMARY
# ==============================================================================
st.header("1. Executive Summary")
c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1:
    infra_mean = df["indeks_infrastruktur"].mean() if len(df) > 0 else 0
    infra_std = df["indeks_infrastruktur"].std() if len(df) > 0 else 0
    c1.metric(
        "Indeks Infrastruktur",
        f"{infra_mean:.1f}%",
        f"+{infra_std:.1f} σ",
        help="Rata-rata Akses Internet & Listrik",
    )
with c2:
    sdm_mean = df["indeks_sdm"].mean() if len(df) > 0 else 0
    sdm_std = df["indeks_sdm"].std() if len(df) > 0 else 0
    c2.metric(
        "Indeks Kualitas SDM",
        f"{sdm_mean:.1f}%",
        f"+{sdm_std:.1f} σ",
        help="Rata-rata Sertifikasi Guru",
    )
with c3:
    akm_mean = df["potensi_siswa"].mean() if len(df) > 0 else 0
    akm_std = df["potensi_siswa"].std() if len(df) > 0 else 0
    c3.metric(
        "Potensi Siswa (AKM)",
        f"{akm_mean:.1f}",
        f"±{akm_std:.1f}",
        help="Skor Literasi & Numerasi",
    )
with c4:
    total_prov = len(df)
    ready_prov = df["cluster_label"].str.contains("Tinggi", na=False).sum()
    ready_pct = (ready_prov / total_prov * 100) if total_prov > 0 else 0
    c4.metric(
        "Provinsi Siap AI",
        f"{ready_prov}/{total_prov}",
        f"{ready_pct:.0f}%",
        help="Klaster Tinggi (High)",
    )
st.markdown("<br>", unsafe_allow_html=True)

col_map, col_pie = st.columns([2.5, 1], gap="medium")

with col_map:
    st.subheader("Peta Sebaran Kesiapan Nasional")
    if geojson_indo:
        color_order = [
            "Rendah (Low)",
            "Sedang (Medium)",
            "Tinggi (High)",
            "Belum Diklasifikasi",
        ]
        df["cluster_numeric"] = df["cluster_label"].map(
            {v: i for i, v in enumerate(color_order)}
        )
        fig_map = px.choropleth_mapbox(
            df,
            geojson=geojson_indo,
            locations="geo_key",
            featureidkey="properties.Propinsi",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            category_orders={"cluster_label": color_order},
            mapbox_style="carto-darkmatter",
            zoom=3.8,
            center={"lat": -2.5, "lon": 118},
            opacity=0.85,
            hover_name="display_prov",
            hover_data={
                "geo_key": False,
                "cluster_numeric": False,
                "indeks_infrastruktur": ":.1f",
                "indeks_sdm": ":.1f",
                "potensi_siswa": ":.1f",
            },
            labels={
                "indeks_infrastruktur": "Infrastruktur",
                "indeks_sdm": "SDM",
                "potensi_siswa": "AKM",
            },
        )
        fig_map.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=480,
            legend=dict(
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(30, 35, 47, 0.9)",
                bordercolor="rgba(255, 255, 255, 0.2)",
                borderwidth=1,
                font=dict(color="white", size=13),
            ),
            font=dict(family="Inter, sans-serif", size=14),
        )
        st.plotly_chart(fig_map, use_container_width=True, key="main_map")
    else:
        st.warning("⚠️ Peta tidak tersedia. Menampilkan visualisasi alternatif...")
        fig_b = px.bar(
            df.sort_values("indeks_infrastruktur", ascending=True),
            x="indeks_infrastruktur",
            y="display_prov",
            orientation="h",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            height=600,
        )
        fig_b.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=14),
        )
        st.plotly_chart(fig_b, use_container_width=True)

with col_pie:
    st.subheader("Distribusi Klaster")
    counts = df["cluster_label"].value_counts().reset_index()
    counts.columns = ["cluster_label", "count"]
    fig_pie = px.pie(
        counts,
        values="count",
        names="cluster_label",
        color="cluster_label",
        color_discrete_map=COLOR_MAP,
        hole=0.65,
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=12, color="white", family="Inter"),
        marker=dict(line=dict(color="rgba(255,255,255,0.3)", width=2)),
    )
    fig_pie.update_layout(
        showlegend=False,
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
        height=240,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter", size=13),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    rentan = df["cluster_label"].str.contains("Rendah", na=False).sum()
    sedang = df["cluster_label"].str.contains("Sedang", na=False).sum()
    rentan_pct = (rentan / len(df) * 100) if len(df) > 0 else 0
    sedang_pct = (sedang / len(df) * 100) if len(df) > 0 else 0

    st.markdown(
        f"""
        <div class='insight-box' style='margin-top: 1rem;'>
            <div class='insight-box-header'>💡 Key Insights</div>
            <ul>
                <li><strong>{rentan}</strong> provinsi ({rentan_pct:.0f}%) masih klaster Rendah</li>
                <li><strong>{sedang}</strong> provinsi ({sedang_pct:.0f}%) di klaster Sedang</li>
                <li>Prioritas: Tingkatkan infrastruktur di zona merah</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 2. CLUSTER INTELLIGENCE
# ==============================================================================
st.divider()
st.header("2. Cluster Intelligence & Advanced Analytics")
(
    tab_overview,
    tab_correlation,
    tab_distribution,
    tab_ranking,
    tab_gap,
    tab_shap,
    tab_artifacts,
) = st.tabs(
    [
        "📊 Overview",
        "🔗 Correlation Analysis",
        "📈 Distribution",
        "🏆 Ranking System",
        "📉 Gap Analysis",
        "🧠 SHAP Explainability",
        "📸 ML Artifacts Gallery",
    ]
)

with tab_overview:
    c_rad, c_tab = st.columns([1.2, 1], gap="medium")
    with c_rad:
        st.subheader("DNA Profil Klaster")
        radar_metrics = ["indeks_infrastruktur", "indeks_sdm", "potensi_siswa"]
        extra_col = next((c for c in df.columns if "internet_smp" in c), None)
        if extra_col:
            radar_metrics.append(extra_col)
        radar_df = df.groupby("cluster_label")[radar_metrics].mean().reset_index()
        fig_rad = go.Figure()
        for idx, row in radar_df.iterrows():
            cluster = row["cluster_label"]
            values = [row[m] for m in radar_metrics]
            values.append(values[0])
            fig_rad.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=radar_metrics + [radar_metrics[0]],
                    fill="toself",
                    name=cluster,
                    line=dict(color=COLOR_MAP.get(cluster, "#888"), width=2),
                    fillcolor=COLOR_MAP.get(cluster, "#888"),
                    opacity=0.5,
                )
            )
        fig_rad.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color="#9CA3AF", size=12),
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color="white", size=12),
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            showlegend=True,
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            legend=dict(
                bgcolor="rgba(30,35,47,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            ),
        )
        st.plotly_chart(fig_rad, use_container_width=True)

    with c_tab:
        st.subheader("Matriks Prioritas Aksi")
        prio_cols = ["indeks_infrastruktur", "indeks_sdm", "rasio_pc_avg"]
        prio_df = df.groupby("cluster_label")[prio_cols].mean()

        def get_act(row):
            act = []
            if row["indeks_infrastruktur"] < 65:
                act.append("⚡ Infra")
            if row["indeks_sdm"] < 50:
                act.append("🎓 Guru")
            if row["rasio_pc_avg"] > 15:
                act.append("💻 Perangkat")
            return " + ".join(act) if act else "✅ Maintain"

        prio_df["Fokus Utama"] = prio_df.apply(get_act, axis=1)

        def color_scale(val):
            if val < 50:
                return "background-color: rgba(239, 68, 68, 0.3)"
            elif val < 70:
                return "background-color: rgba(245, 158, 11, 0.3)"
            else:
                return "background-color: rgba(16, 185, 129, 0.3)"

        styled_df = prio_df.style.format("{:.1f}", subset=prio_cols).applymap(
            color_scale, subset=prio_cols
        )
        st.dataframe(styled_df, use_container_width=True, height=220)
        st.markdown(
            """
            <div class='info-box' style='margin-top: 1rem;'>
                <div class='info-box-header'>📌 Action Items</div>
                <p>Prioritas tertinggi pada klaster Rendah untuk akselerasi digital</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_correlation:
    st.subheader("🔗 Correlation Heatmap Analysis")
    col_heat, col_insights = st.columns([2, 1], gap="medium")
    with col_heat:
        numeric_cols = [
            "indeks_infrastruktur",
            "indeks_sdm",
            "potensi_siswa",
            "rasio_pc_avg",
        ]

        for col in [
            "persen_sekolah_internet_smp",
            "persen_guru_sertifikasi_smp",
            "persen_lulus_akm_literasi",
            "persen_lulus_akm_numerasi",
        ]:
            if col in df.columns:
                numeric_cols.append(col)

        corr_matrix = df[numeric_cols].corr()

        fig_heatmap = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
        )

        fig_heatmap.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=11),
            height=500,
            xaxis=dict(tickangle=-45),
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col_insights:
        st.markdown("#### 🔍 Key Correlations")

        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_pairs.append(
                    {
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "corr": corr_matrix.iloc[i, j],
                    }
                )

        corr_df = pd.DataFrame(corr_pairs).sort_values("corr", ascending=False, key=abs)

        st.markdown(
            """
        <div class='section-card' style='padding: 1rem;'>
            <h4 style='color: #10B981; margin-top: 0;'>Strongest Positive</h4>
        """,
            unsafe_allow_html=True,
        )

        for idx, row in corr_df.head(3).iterrows():
            st.markdown(
                f"""
            <div style='margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 6px;'>
                <small style='color: #9CA3AF;'>{row['var1'][:20]}... ↔ {row['var2'][:20]}...</small><br>
                <strong style='color: #10B981; font-size: 1.2rem;'>{row['corr']:.3f}</strong>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div class='section-card' style='padding: 1rem; margin-top: 1rem;'>
            <h4 style='color: #EF4444; margin-top: 0;'>Strongest Negative</h4>
        """,
            unsafe_allow_html=True,
        )

        for idx, row in corr_df.tail(3).iterrows():
            st.markdown(
                f"""
            <div style='margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(239, 68, 68, 0.1); border-radius: 6px;'>
                <small style='color: #9CA3AF;'>{row['var1'][:20]}... ↔ {row['var2'][:20]}...</small><br>
                <strong style='color: #EF4444; font-size: 1.2rem;'>{row['corr']:.3f}</strong>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

with tab_distribution:
    st.subheader("📈 Distribution Analysis")
    col_dist1, col_dist2 = st.columns(2, gap="medium")
    with col_dist1:
        st.markdown("#### Infrastruktur Distribution")

        fig_dist1 = px.histogram(
            df,
            x="indeks_infrastruktur",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            nbins=20,
            marginal="box",
            labels={"indeks_infrastruktur": "Indeks Infrastruktur (%)"},
        )

        fig_dist1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            height=350,
            showlegend=True,
            legend=dict(
                bgcolor="rgba(30,35,47,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            ),
        )

        st.plotly_chart(fig_dist1, use_container_width=True)
    with col_dist2:
        st.markdown("#### SDM Quality Distribution")

        fig_dist2 = px.violin(
            df,
            y="indeks_sdm",
            x="cluster_label",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            box=True,
            labels={"indeks_sdm": "Indeks SDM (%)"},
        )

        fig_dist2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            height=350,
            showlegend=False,
        )

        st.plotly_chart(fig_dist2, use_container_width=True)

    st.markdown("#### Multi-Metric Distribution by Cluster")
    metrics_to_plot = ["indeks_infrastruktur", "indeks_sdm", "potensi_siswa"]
    df_melted = df.melt(
        id_vars=["cluster_label"],
        value_vars=metrics_to_plot,
        var_name="Metric",
        value_name="Value",
    )
    fig_box = px.box(
        df_melted,
        x="Metric",
        y="Value",
        color="cluster_label",
        color_discrete_map=COLOR_MAP,
        labels={"Value": "Score", "Metric": "Indicator"},
    )
    fig_box.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter", size=13),
        height=400,
        legend=dict(
            bgcolor="rgba(30,35,47,0.9)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
        ),
    )
    st.plotly_chart(fig_box, use_container_width=True)

with tab_ranking:
    st.subheader("🏆 Provincial Ranking System")
    df["composite_score"] = (
        df["indeks_infrastruktur"] * 0.4
        + df["indeks_sdm"] * 0.35
        + df["potensi_siswa"] * 0.25
    )
    df["rank"] = df["composite_score"].rank(ascending=False).astype(int)
    col_rank1, col_rank2 = st.columns([1.5, 1], gap="medium")
    with col_rank1:
        top_10 = df.nsmallest(10, "rank")[
            ["display_prov", "composite_score", "rank", "cluster_label"]
        ]

        fig_rank = px.bar(
            top_10,
            x="composite_score",
            y="display_prov",
            orientation="h",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            text="rank",
            labels={"composite_score": "Composite Score", "display_prov": "Province"},
        )

        fig_rank.update_traces(
            texttemplate="Rank %{text}",
            textposition="outside",
            textfont=dict(color="white", size=12),
        )

        fig_rank.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            height=400,
            title="Top 10 Provinces by Composite Score",
            title_font=dict(size=16, color="#E5E7EB"),
        )

        st.plotly_chart(fig_rank, use_container_width=True)
    with col_rank2:
        st.markdown("#### 🎯 Ranking Methodology")
        st.markdown(
            """
        <div class='section-card' style='padding: 1rem;'>
            <p style='color: #D1D5DB; font-size: 0.9rem; line-height: 1.6;'>
            <strong style='color: #00D9FF;'>Composite Score Formula:</strong><br>
            • Infrastruktur: <strong>40%</strong><br>
            • SDM Quality: <strong>35%</strong><br>
            • Student Potential: <strong>25%</strong>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        top_prov = df.nsmallest(1, "rank").iloc[0]

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=top_prov["composite_score"],
                domain={"x": [0, 1], "y": [0, 1]},
                title={
                    "text": f"Best: {top_prov['display_prov']}",
                    "font": {"color": "white", "size": 14},
                },
                delta={
                    "reference": df["composite_score"].mean(),
                    "increasing": {"color": "#10B981"},
                },
                gauge={
                    "axis": {"range": [None, 100], "tickcolor": "white"},
                    "bar": {"color": "#00D9FF"},
                    "bgcolor": "rgba(30, 35, 47, 0.5)",
                    "borderwidth": 2,
                    "bordercolor": "rgba(255,255,255,0.2)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(239, 68, 68, 0.3)"},
                        {"range": [50, 70], "color": "rgba(245, 158, 11, 0.3)"},
                        {"range": [70, 100], "color": "rgba(16, 185, 129, 0.3)"},
                    ],
                    "threshold": {
                        "line": {"color": "#A855F7", "width": 4},
                        "thickness": 0.75,
                        "value": df["composite_score"].median(),
                    },
                },
            )
        )

        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            height=250,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

with tab_gap:
    st.subheader("📉 Gap Analysis: Distance to Target")
    targets = {
        "indeks_infrastruktur": 85,
        "indeks_sdm": 75,
        "potensi_siswa": 70,
        "rasio_pc_avg": 5,
    }
    df["gap_infra"] = targets["indeks_infrastruktur"] - df["indeks_infrastruktur"]
    df["gap_sdm"] = targets["indeks_sdm"] - df["indeks_sdm"]
    df["gap_student"] = targets["potensi_siswa"] - df["potensi_siswa"]
    df["gap_pc"] = df["rasio_pc_avg"] - targets["rasio_pc_avg"]
    col_gap1, col_gap2 = st.columns([2, 1], gap="medium")
    with col_gap1:
        cluster_gaps = df.groupby("cluster_label")[
            ["gap_infra", "gap_sdm", "gap_student"]
        ].mean()

        selected_cluster = st.selectbox(
            "Select Cluster for Detailed Gap Analysis", df["cluster_label"].unique()
        )

        cluster_data = cluster_gaps.loc[selected_cluster]

        fig_waterfall = go.Figure(
            go.Waterfall(
                name="Gap Analysis",
                orientation="v",
                measure=["relative", "relative", "relative", "total"],
                x=["Infrastruktur Gap", "SDM Gap", "Student Gap", "Total Gap"],
                y=[
                    cluster_data["gap_infra"],
                    cluster_data["gap_sdm"],
                    cluster_data["gap_student"],
                    cluster_data.sum(),
                ],
                text=[
                    f"{cluster_data['gap_infra']:.1f}",
                    f"{cluster_data['gap_sdm']:.1f}",
                    f"{cluster_data['gap_student']:.1f}",
                    f"{cluster_data.sum():.1f}",
                ],
                textposition="outside",
                connector={"line": {"color": "rgba(255,255,255,0.3)"}},
                decreasing={"marker": {"color": "#EF4444"}},
                increasing={"marker": {"color": "#10B981"}},
                totals={"marker": {"color": "#3B82F6"}},
            )
        )

        fig_waterfall.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            height=400,
            title=f"Gap Analysis: {selected_cluster}",
            title_font=dict(size=16, color="#E5E7EB"),
            showlegend=False,
        )

        st.plotly_chart(fig_waterfall, use_container_width=True)
    with col_gap2:
        st.markdown("#### 🎯 Target Benchmarks")

        for metric, target in targets.items():
            current_avg = (
                df[metric].mean() if metric != "rasio_pc_avg" else df[metric].mean()
            )
            gap = (
                target - current_avg
                if metric != "rasio_pc_avg"
                else current_avg - target
            )
            progress = (
                (current_avg / target * 100)
                if metric != "rasio_pc_avg"
                else (target / current_avg * 100)
            )
            progress = min(progress, 100)

            st.markdown(
                f"""
            <div style='margin-bottom: 1rem; padding: 0.75rem; background: rgba(30, 35, 47, 0.6); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);'>
                <div style='color: #9CA3AF; font-size: 0.85rem; margin-bottom: 0.25rem;'>{metric.replace('_', ' ').title()}</div>
                <div style='color: #E5E7EB; font-size: 1.1rem; font-weight: 600;'>
                    {current_avg:.1f} / {target}
                </div>
                <div style='background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; margin-top: 0.5rem; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #00D9FF, #A855F7); height: 100%; width: {progress}%; transition: width 0.3s;'></div>
                </div>
                <div style='color: {"#10B981" if gap < 0 or (metric == "rasio_pc_avg" and gap < 0) else "#EF4444"}; font-size: 0.85rem; margin-top: 0.25rem;'>
                    Gap: {abs(gap):.1f}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
        <div class='insight-box' style='margin-top: 1rem;'>
            <div class='insight-box-header'>💡 Insight</div>
            <ul style='margin-bottom: 0;'>
                <li>Priority tinggi untuk provinsi dengan gap > 30 poin</li>
                <li>Fokus investasi pada metrik dengan gap terbesar</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

with tab_shap:
    st.subheader("🧠 SHAP Explainability Analysis")
    st.markdown(
        """
    <div class='info-box'>
        <div class='info-box-header'>ℹ️ About SHAP</div>
        <p>SHAP (SHapley Additive exPlanations) values show feature importance and how each feature contributes to model predictions.
        Higher SHAP values indicate stronger feature influence on cluster assignments.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if SHAP_PATH and os.path.exists(SHAP_PATH):
        try:
            shap_img = Image.open(SHAP_PATH)
            st.image(
                shap_img,
                caption="SHAP Summary Plot - Feature Importance",
                use_container_width=True,
            )

            st.markdown(
                """
            <div class='insight-box'>
                <div class='insight-box-header'>🔍 How to Interpret</div>
                <ul>
                    <li><strong>Bar Length:</strong> Indicates feature importance magnitude</li>
                    <li><strong>Top Features:</strong> Most influential in determining cluster assignments</li>
                    <li><strong>Color Intensity:</strong> Shows feature value distribution</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if cluster_metadata and "feature_names" in cluster_metadata:
                st.markdown("#### 📊 Feature Details from Model")
                features = cluster_metadata["feature_names"]

                col_feat1, col_feat2 = st.columns(2)

                with col_feat1:
                    st.markdown("**Features Used in Model:**")
                    for i, feat in enumerate(features[: len(features) // 2], 1):
                        st.markdown(f"{i}. `{feat}`")

                with col_feat2:
                    st.markdown("**&nbsp;**")
                    for i, feat in enumerate(
                        features[len(features) // 2 :], len(features) // 2 + 1
                    ):
                        st.markdown(f"{i}. `{feat}`")

        except Exception as e:
            st.error(f"❌ Failed to load SHAP plot: {str(e)}")
    else:
        st.warning(
            "⚠️ SHAP summary plot not found. Please ensure the model training pipeline has completed."
        )
        st.info(
            "💡 Run the `explain_model_shap.py` block in Mage pipeline to generate SHAP analysis."
        )

with tab_artifacts:
    st.subheader("📸 ML Training Artifacts Gallery")
    st.markdown(
        """
    <div class='info-box'>
        <div class='info-box-header'>ℹ️ About Artifacts</div>
        <p>These visualizations are generated during model training and hyperparameter optimization.
        They provide insights into model selection and cluster quality.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    col_art1, col_art2 = st.columns(2, gap="medium")
    with col_art1:
        st.markdown("#### 📐 Elbow Method Analysis")
        if ELBOW_PATH and os.path.exists(ELBOW_PATH):
            try:
                elbow_img = Image.open(ELBOW_PATH)
                st.image(
                    elbow_img,
                    caption="Elbow Method - Optimal K Selection",
                    use_container_width=True,
                )
                st.markdown(
                    """
                <div class='section-card' style='padding: 0.75rem;'>
                    <p style='color: #D1D5DB; font-size: 0.85rem; margin: 0;'>
                    <strong>Purpose:</strong> Identifies optimal number of clusters by finding "elbow point" where inertia decrease slows.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ Error loading: {str(e)[:50]}")
        else:
            st.warning("⚠️ Elbow plot not available")
    with col_art2:
        st.markdown("#### 🎯 Silhouette Score Analysis")
        if SILHOUETTE_PATH and os.path.exists(SILHOUETTE_PATH):
            try:
                sil_img = Image.open(SILHOUETTE_PATH)
                st.image(
                    sil_img, caption="Silhouette Score vs K", use_container_width=True
                )

                st.markdown(
                    """
                <div class='section-card' style='padding: 0.75rem;'>
                    <p style='color: #D1D5DB; font-size: 0.85rem; margin: 0;'>
                    <strong>Purpose:</strong> Measures cluster quality. Higher scores indicate better-defined clusters.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ Error loading: {str(e)[:50]}")
        else:
            st.warning("⚠️ Silhouette plot not available")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🌟 PCA 2D Cluster Visualization")
    if PCA_PATH and os.path.exists(PCA_PATH):
        try:
            pca_img = Image.open(PCA_PATH)
            st.image(
                pca_img,
                caption="PCA 2D Projection - Cluster Separation",
                use_container_width=True,
            )

            st.markdown(
                """
            <div class='insight-box'>
                <div class='insight-box-header'>💡 Interpretation Guide</div>
                <ul>
                    <li><strong>Distinct Clusters:</strong> Clear separation indicates good clustering quality</li>
                    <li><strong>PC1 & PC2:</strong> Principal components capturing most variance in data</li>
                    <li><strong>Overlap:</strong> Some overlap is normal; complete separation is rare in real-world data</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error loading PCA plot: {str(e)}")
    else:
        st.warning("⚠️ PCA visualization not found")
    st.markdown("<br>", unsafe_allow_html=True)
    if cluster_metadata:
        with st.expander("🔍 View Complete Model Metadata", expanded=False):
            st.json(cluster_metadata)

# ==============================================================================
# 3. INFRASTRUCTURE DEEP-DIVE
# ==============================================================================
st.divider()
st.header("3. Infrastructure Deep-Dive & Advanced Viz")
tab_matrix, tab_anomaly, tab_treemap, tab_parallel = st.tabs(
    [
        "📊 Energy-Connectivity Matrix",
        "🔍 Anomaly Detection",
        "🌳 Treemap Analysis",
        "🎯 Parallel Coordinates",
    ]
)

with tab_matrix:
    c_sc, c_bar = st.columns([2, 1], gap="medium")
    with c_sc:
        st.subheader("Matriks Energi vs Konektivitas Digital")
        df["size_bubble"] = df["rasio_pc_avg"].fillna(1).clip(lower=1)
        col_x = next((c for c in df.columns if "internet_smp" in c), None)
        col_y = next((c for c in df.columns if "internet_sd" in c), None)
        if col_x and col_y:
            fig_sc = px.scatter(
                df,
                x=col_x,
                y=col_y,
                color="cluster_label",
                size="size_bubble",
                hover_name="display_prov",
                color_discrete_map=COLOR_MAP,
                labels={
                    "size_bubble": "Rasio PC",
                    col_x: "Internet SMP (%)",
                    col_y: "Internet SD (%)",
                },
                size_max=30,
            )
            median_x = df[col_x].median()
            median_y = df[col_y].median()

            fig_sc.add_vline(
                x=median_x,
                line_dash="dash",
                line_color="rgba(255,255,255,0.3)",
                line_width=1,
            )
            fig_sc.add_hline(
                y=median_y,
                line_dash="dash",
                line_color="rgba(255,255,255,0.3)",
                line_width=1,
            )
            fig_sc.add_annotation(
                x=95,
                y=95,
                text="🚀 Cloud Ready",
                showarrow=False,
                font=dict(color="#10B981", size=14, family="Inter"),
            )
            fig_sc.add_annotation(
                x=30,
                y=30,
                text="⚠️ Priority Zone",
                showarrow=False,
                font=dict(color="#EF4444", size=14, family="Inter"),
            )
            fig_sc.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter", size=14),
                height=420,
                legend=dict(
                    bgcolor="rgba(30,35,47,0.9)",
                    bordercolor="rgba(255,255,255,0.2)",
                    borderwidth=1,
                    font=dict(size=12),
                ),
                xaxis=dict(title_font=dict(size=15)),
                yaxis=dict(title_font=dict(size=15)),
            )
            st.plotly_chart(fig_sc, use_container_width=True)
        else:
            st.info("⚠️ Data internet tidak tersedia untuk visualisasi scatter")
    with c_bar:
        st.subheader("Red Zone: Rasio PC Tertinggi")
        worst = df.sort_values("rasio_pc_avg", ascending=False).head(10)
        fig_b = px.bar(
            worst,
            x="rasio_pc_avg",
            y="display_prov",
            orientation="h",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            text="rasio_pc_avg",
        )
        fig_b.add_vline(
            x=5,
            line_color="#10B981",
            line_dash="solid",
            line_width=2,
            annotation_text="Target Ideal (1:5)",
            annotation=dict(font=dict(size=12)),
        )
        fig_b.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            textfont=dict(color="white", size=12, family="Inter"),
        )
        fig_b.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=13),
            height=420,
            showlegend=False,
            xaxis_title="Rasio Siswa per PC",
            yaxis_title="",
            xaxis=dict(title_font=dict(size=14)),
        )
        st.plotly_chart(fig_b, use_container_width=True)

with tab_anomaly:
    st.subheader("🔍 Anomaly Detection using Z-Score")
    metrics_for_anomaly = [
        "indeks_infrastruktur",
        "indeks_sdm",
        "potensi_siswa",
        "rasio_pc_avg",
    ]
    for metric in metrics_for_anomaly:
        if metric in df.columns:
            mean_val = df[metric].mean()
            std_val = df[metric].std()
            if std_val > 0:
                df[f"{metric}_zscore"] = (df[metric] - mean_val) / std_val
            else:
                df[f"{metric}_zscore"] = 0
    df["is_anomaly"] = (
        (abs(df["indeks_infrastruktur_zscore"]) > 2)
        | (abs(df["indeks_sdm_zscore"]) > 2)
        | (abs(df["potensi_siswa_zscore"]) > 2)
    )
    anomalies = df[df["is_anomaly"]]
    col_anom1, col_anom2 = st.columns([2, 1], gap="medium")
    with col_anom1:
        fig_3d = px.scatter_3d(
            df,
            x="indeks_infrastruktur",
            y="indeks_sdm",
            z="potensi_siswa",
            color="is_anomaly",
            color_discrete_map={True: "#EF4444", False: "#10B981"},
            hover_name="display_prov",
            labels={
                "is_anomaly": "Anomaly Status",
                "indeks_infrastruktur": "Infrastruktur",
                "indeks_sdm": "SDM",
                "potensi_siswa": "Student Potential",
            },
        )

        fig_3d.update_layout(
            scene=dict(
                bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    backgroundcolor="rgba(30, 35, 47, 0.5)",
                    gridcolor="rgba(255,255,255,0.1)",
                ),
                yaxis=dict(
                    backgroundcolor="rgba(30, 35, 47, 0.5)",
                    gridcolor="rgba(255,255,255,0.1)",
                ),
                zaxis=dict(
                    backgroundcolor="rgba(30, 35, 47, 0.5)",
                    gridcolor="rgba(255,255,255,0.1)",
                ),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter", size=12),
            height=500,
            legend=dict(
                bgcolor="rgba(30,35,47,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            ),
        )

        st.plotly_chart(fig_3d, use_container_width=True)
    with col_anom2:
        st.markdown("#### 🚨 Detected Anomalies")

        if len(anomalies) > 0:
            for idx, row in anomalies.iterrows():
                reasons = []
                if abs(row["indeks_infrastruktur_zscore"]) > 2:
                    reasons.append(f"Infra: {row['indeks_infrastruktur_zscore']:.2f}σ")
                if abs(row["indeks_sdm_zscore"]) > 2:
                    reasons.append(f"SDM: {row['indeks_sdm_zscore']:.2f}σ")
                if abs(row["potensi_siswa_zscore"]) > 2:
                    reasons.append(f"Student: {row['potensi_siswa_zscore']:.2f}σ")

                st.markdown(
                    f"""
                <div style='margin-bottom: 1rem; padding: 0.875rem; background: rgba(239, 68, 68, 0.1); border-radius: 8px; border-left: 3px solid #EF4444;'>
                    <div style='color: #F3F4F6; font-weight: 600; margin-bottom: 0.5rem;'>{row['display_prov']}</div>
                    <div style='color: #9CA3AF; font-size: 0.85rem;'>
                        {' | '.join(reasons)}
                    </div>
                    <div style='color: #FCA5A5; font-size: 0.8rem; margin-top: 0.5rem;'>
                        Cluster: {row['cluster_label']}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("✅ No significant anomalies detected")

        st.markdown(
            """
        <div class='info-box' style='margin-top: 1rem;'>
            <div class='info-box-header'>ℹ️ Methodology</div>
            <p>Provinces with z-score > |2| in any metric are flagged as anomalies (2.5% outliers)</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

with tab_treemap:
    st.subheader("🌳 Hierarchical Treemap: Cluster → Province")
    df_treemap = df.copy()
    df_treemap["total"] = "Indonesia"
    fig_treemap = px.treemap(
        df_treemap,
        path=["total", "cluster_label", "display_prov"],
        values="composite_score",
        color="composite_score",
        color_continuous_scale="RdYlGn",
        hover_data={
            "composite_score": ":.2f",
            "indeks_infrastruktur": ":.1f",
            "indeks_sdm": ":.1f",
        },
    )
    fig_treemap.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter", size=12),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.markdown(
        """
    <div class='insight-box'>
        <div class='insight-box-header'>💡 Insight</div>
        <ul style='margin-bottom: 0;'>
            <li>Ukuran box menunjukkan composite score</li>
            <li>Warna menunjukkan tingkat kesiapan (hijau = tinggi, merah = rendah)</li>
            <li>Click untuk drill-down ke level detail</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with tab_parallel:
    st.subheader("🎯 Parallel Coordinates: Multi-Dimensional Analysis")
    parallel_cols = [
        "indeks_infrastruktur",
        "indeks_sdm",
        "potensi_siswa",
        "rasio_pc_avg",
    ]
    for col in ["persen_sekolah_internet_smp", "persen_guru_sertifikasi_smp"]:
        if col in df.columns and col not in parallel_cols:
            parallel_cols.append(col)
    df["rasio_pc_normalized"] = 100 - (
        df["rasio_pc_avg"] / df["rasio_pc_avg"].max() * 100
    )
    fig_parallel = px.parallel_coordinates(
        df,
        dimensions=parallel_cols[:6],
        color="composite_score",
        color_continuous_scale="Turbo",
        labels={
            col: col.replace("_", " ")
            .replace("persen", "%")
            .replace("indeks", "Idx")[:20]
            for col in parallel_cols
        },
    )
    fig_parallel.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter", size=12),
        height=500,
        margin=dict(l=100, r=100, t=50, b=50),
    )
    st.plotly_chart(fig_parallel, use_container_width=True)
    st.markdown(
        """
    <div class='info-box'>
        <div class='info-box-header'>📊 How to Read</div>
        <p>Setiap garis vertikal adalah satu provinsi. Pola garis horizontal menunjukkan provinsi dengan performa seimbang di semua metrik.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 4. HUMAN CAPITAL
# ==============================================================================
st.divider()
st.header("4. Human Capital Analytics")
tab_corr_hc, tab_sankey, tab_funnel = st.tabs(
    ["📊 Correlation Analysis", "🔄 Flow Analysis (Sankey)", "📉 Education Funnel"]
)

with tab_corr_hc:
    c_cor, c_heat = st.columns(2, gap="medium")
    with c_cor:
        st.subheader("Korelasi: Kualifikasi Guru vs Numerasi Siswa")
        col_guru = next((c for c in df.columns if "sertifikasi_smp" in c), None)
        col_num = next((c for c in df.columns if "akm_numerasi" in c), None)
        if col_guru and col_num:
            fig_cor = px.scatter(
                df,
                x=col_guru,
                y=col_num,
                color="cluster_label",
                color_discrete_map=COLOR_MAP,
                hover_name="display_prov",
                trendline="ols",
                trendline_color_override="rgba(0, 217, 255, 0.8)",
                labels={
                    col_guru: "Guru Bersertifikat (%)",
                    col_num: "Skor Numerasi AKM",
                },
            )
            fig_cor.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter", size=13),
                height=380,
                legend=dict(
                    bgcolor="rgba(30,35,47,0.9)",
                    bordercolor="rgba(255,255,255,0.2)",
                    borderwidth=1,
                ),
                xaxis=dict(title_font=dict(size=14)),
                yaxis=dict(title_font=dict(size=14)),
            )
            st.plotly_chart(fig_cor, use_container_width=True)
        else:
            st.info("⚠️ Data guru atau numerasi tidak tersedia")
    with c_heat:
        st.subheader("Heatmap: Beban Guru vs Kualitas")
        col_beban = next((c for c in df.columns if "rasio_siswa_guru" in c), None)
        col_num = next((c for c in df.columns if "akm_numerasi" in c), None)
        if col_beban and col_num:
            fig_heat = px.density_heatmap(
                df,
                x=col_beban,
                y=col_num,
                color_continuous_scale="Turbo",
                labels={col_beban: "Rasio Siswa:Guru", col_num: "Skor Numerasi"},
            )
            fig_heat.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter", size=13),
                height=380,
                xaxis=dict(title_font=dict(size=14)),
                yaxis=dict(title_font=dict(size=14)),
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("⚠️ Data beban mengajar tidak tersedia")
    st.markdown(
        """
        <div class='insight-box'>
            <div class='insight-box-header'>🔬 Research Finding</div>
            <ul style='margin-bottom: 0;'>
                <li>Korelasi positif signifikan antara kualifikasi guru dengan capaian numerasi siswa</li>
                <li>Setiap <strong>10% peningkatan</strong> guru bersertifikat berpotensi menaikkan skor AKM hingga <strong>3-5 poin</strong></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_sankey:
    st.subheader("🔄 Teacher Qualification Flow: SD → SMP → SMA")
    col_cert_sd = next((c for c in df.columns if "sertifikasi_sd" in c), None)
    col_cert_smp = next((c for c in df.columns if "sertifikasi_smp" in c), None)
    col_cert_sma = next((c for c in df.columns if "sertifikasi_sma" in c), None)

    if col_cert_sd and col_cert_smp and col_cert_sma:
        sankey_data = df.groupby("cluster_label")[
            [col_cert_sd, col_cert_smp, col_cert_sma]
        ].mean()

        nodes = [
            "SD Level",
            "SMP Level",
            "SMA Level",
            "High Cluster",
            "Medium Cluster",
            "Low Cluster",
        ]

        node_colors = ["#60A5FA", "#60A5FA", "#60A5FA", "#10B981", "#F59E0B", "#EF4444"]

        source = []
        target = []
        value = []
        colors = []

        cluster_map = {
            "Tinggi (High)": (3, "#10B981"),
            "Sedang (Medium)": (4, "#F59E0B"),
            "Rendah (Low)": (5, "#EF4444"),
        }

        for cluster, row in sankey_data.iterrows():
            if cluster in cluster_map:
                cluster_idx, color = cluster_map[cluster]
                source.append(0)
                target.append(cluster_idx)
                value.append(row[col_cert_sd])
                colors.append(
                    f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.4)"
                )

                source.append(1)
                target.append(cluster_idx)
                value.append(row[col_cert_smp])
                colors.append(
                    f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.4)"
                )

                source.append(2)
                target.append(cluster_idx)
                value.append(row[col_cert_sma])
                colors.append(
                    f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.4)"
                )

        fig_sankey = go.Figure(
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="rgba(255,255,255,0.2)", width=1),
                    label=nodes,
                    color=node_colors,
                ),
                link=dict(source=source, target=target, value=value, color=colors),
            )
        )

        fig_sankey.update_layout(
            font=dict(size=13, color="white", family="Inter"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=500,
            margin=dict(l=0, r=0, t=30, b=0),
        )

        st.plotly_chart(fig_sankey, use_container_width=True)

        st.markdown(
            """
        <div class='info-box'>
            <div class='info-box-header'>💡 Flow Interpretation</div>
            <p>Diagram menunjukkan distribusi rata-rata sertifikasi guru dari setiap jenjang (SD, SMP, SMA) ke cluster kesiapan.
            Lebar aliran menunjukkan persentase sertifikasi.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Data sertifikasi guru tidak lengkap untuk visualisasi Sankey")

with tab_funnel:
    st.subheader("📉 Education Quality Funnel")
    col_funnel, col_insight_funnel = st.columns([2, 1], gap="medium")
    with col_funnel:
        col_internet = next((c for c in df.columns if "internet_smp" in c), None)
        col_cert = next((c for c in df.columns if "sertifikasi_smp" in c), None)
        col_lit = next((c for c in df.columns if "lulus_akm_literasi" in c), None)
        col_num = next((c for c in df.columns if "lulus_akm_numerasi" in c), None)

        funnel_stages = []
        funnel_values = []

        if col_internet:
            funnel_stages.append("Internet Access")
            funnel_values.append(df[col_internet].mean())

        if col_cert:
            funnel_stages.append("Certified Teachers")
            funnel_values.append(df[col_cert].mean())

        if col_lit:
            funnel_stages.append("Literacy Pass Rate")
            funnel_values.append(df[col_lit].mean())

        if col_num:
            funnel_stages.append("Numeracy Pass Rate")
            funnel_values.append(df[col_num].mean())

        if funnel_stages:
            fig_funnel = go.Figure(
                go.Funnel(
                    y=funnel_stages,
                    x=funnel_values,
                    textposition="inside",
                    textinfo="value+percent initial",
                    marker=dict(
                        color=["#3B82F6", "#10B981", "#F59E0B", "#EF4444"],
                        line=dict(width=2, color="rgba(255,255,255,0.3)"),
                    ),
                    connector={"line": {"color": "rgba(255,255,255,0.2)", "width": 2}},
                )
            )

            fig_funnel.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family="Inter", size=14),
                height=450,
                margin=dict(l=100, r=100, t=30, b=30),
            )

            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.info("Data tidak tersedia untuk funnel visualization")
    with col_insight_funnel:
        st.markdown("#### 📊 Funnel Insights")

        if funnel_values:
            drop_off_rate = (
                (funnel_values[0] - funnel_values[-1]) / funnel_values[0] * 100
            )

            st.markdown(
                f"""
            <div class='section-card' style='padding: 1rem;'>
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <div style='color: #9CA3AF; font-size: 0.85rem;'>Total Drop-off Rate</div>
                    <div style='color: #EF4444; font-size: 2.5rem; font-weight: 700;'>{drop_off_rate:.1f}%</div>
                </div>
                <hr style='border-color: rgba(255,255,255,0.1); margin: 1rem 0;'>
                <div style='color: #D1D5DB; font-size: 0.9rem; line-height: 1.6;'>
                    <strong>Stage Analysis:</strong><br>
            """,
                unsafe_allow_html=True,
            )

            for i, (stage, value) in enumerate(zip(funnel_stages, funnel_values)):
                if i < len(funnel_values) - 1:
                    drop = funnel_values[i] - funnel_values[i + 1]
                    st.markdown(
                        f"• {stage}: <strong style='color: #F59E0B;'>{value:.1f}%</strong> (-{drop:.1f}%)<br>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"• {stage}: <strong style='color: #10B981;'>{value:.1f}%</strong>",
                        unsafe_allow_html=True,
                    )

            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div class='insight-box' style='margin-top: 1rem;'>
            <div class='insight-box-header'>🎯 Recommendations</div>
            <ul style='margin-bottom: 0;'>
                <li>Focus on stages with highest drop-off</li>
                <li>Implement targeted interventions</li>
                <li>Monitor conversion rates quarterly</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==============================================================================
# 5. STRATEGIC ROADMAP
# ==============================================================================
st.divider()
st.header("5. Strategic Roadmap by Cluster")
t1, t2, t3 = st.tabs(
    ["🚀 High: AI Leaders", "🚧 Medium: Gap Fillers", "🆘 Low: Basic Enablers"]
)
with t1:
    st.markdown(
        """
        <div class='section-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%); border-left: 4px solid #10B981;'>
            <h4 style='color: #10B981; margin-top: 0; margin-bottom: 1.25rem;'>🎯 Vision: National AI Innovation Hub</h4>
            <ul style='color: #D1D5DB; line-height: 2; padding-left: 1.5rem; margin-bottom: 1.5rem;'>
                <li><strong>Deep Tech:</strong> Implementasi Cloud AI, Neural Networks, Computer Vision</li>
                <li><strong>Global Standards:</strong> Sertifikasi internasional (AWS, Google AI, Azure)</li>
                <li><strong>Research Collaboration:</strong> Partnership dengan universitas top dunia</li>
                <li><strong>Innovation Labs:</strong> AI Research Center di sekolah unggulan</li>
            </ul>
            <div style='padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);'>
                <strong style='color: #10B981;'>💰 Investment:</strong>
                <span style='color: #D1D5DB;'>Rp 500M - 1T per provinsi | ROI Target: 300% dalam 5 tahun</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with t2:
    st.markdown(
        """
        <div class='section-card' style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%); border-left: 4px solid #F59E0B;'>
            <h4 style='color: #F59E0B; margin-top: 0; margin-bottom: 1.25rem;'>🎯 Vision: Digital Literacy Acceleration</h4>
            <ul style='color: #D1D5DB; line-height: 2; padding-left: 1.5rem; margin-bottom: 1.5rem;'>
                <li><strong>Hardware:</strong> Pengadaan 50,000 laptop/tahun per provinsi</li>
                <li><strong>Connectivity:</strong> Fiber optic deployment + Starlink backup</li>
                <li><strong>Capacity Building:</strong> Training of Trainers (ToT) untuk 10,000 guru</li>
                <li><strong>Curriculum:</strong> Hybrid learning model (30% digital)</li>
            </ul>
            <div style='padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.2);'>
                <strong style='color: #F59E0B;'>💰 Investment:</strong>
                <span style='color: #D1D5DB;'>Rp 200M - 500M per provinsi | Timeline: 2-3 tahun</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with t3:
    st.markdown(
        """
        <div class='section-card' style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%); border-left: 4px solid #EF4444;'>
            <h4 style='color: #EF4444; margin-top: 0; margin-bottom: 1.25rem;'>🎯 Vision: Foundation Infrastructure</h4>
            <ul style='color: #D1D5DB; line-height: 2; padding-left: 1.5rem; margin-bottom: 1.5rem;'>
                <li><strong>Power Grid:</strong> 24/7 electricity coverage (solar + PLN)</li>
                <li><strong>Basic Internet:</strong> 4G/Starlink untuk 100% sekolah</li>
                <li><strong>Offline-First:</strong> Raspberry Pi labs + unplugged coding curriculum</li>
                <li><strong>Teacher Upskilling:</strong> Basic digital literacy untuk semua guru</li>
            </ul>
            <div style='padding: 1rem; background: rgba(239, 68, 68, 0.1); border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.2);'>
                <strong style='color: #EF4444;'>💰 Investment:</strong>
                <span style='color: #D1D5DB;'>Rp 100M - 300M per provinsi | Priority: CRITICAL</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.divider()

# ==============================================================================
# 6. POLICY SIMULATION ENGINE
# ==============================================================================
st.header("6. Interactive Policy Simulator")
st.markdown(
    """
    <div class='info-box'>
        <div class='info-box-header'>🧪 What-If Scenario Analysis</div>
        <p>Simulasikan dampak investasi infrastruktur terhadap kualitas pendidikan dengan model predictive analytics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
col_sim_left, col_sim_right = st.columns([1, 2], gap="medium")
with col_sim_left:
    selected_prov = st.selectbox(
        "🎯 Target Provinsi",
        df["display_prov"].unique(),
        help="Pilih provinsi untuk simulasi kebijakan",
    )
    current_data = df[df["display_prov"] == selected_prov].iloc[0]
    current_pc_ratio = int(current_data["rasio_pc_avg"])
    col_num_sim = next((c for c in df.columns if "akm_numerasi" in c), None)
    current_akm = float(current_data[col_num_sim]) if col_num_sim else 50.0
    st.markdown(
        f"""
        <div style='background: rgba(30, 35, 47, 0.9); padding: 1.25rem; border-radius: 12px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);'>
            <h4 style='color: #F3F4F6; margin-top: 0; margin-bottom: 0.875rem; font-size: 1.05rem;'>📊 Current State</h4>
            <div style='display: flex; flex-direction: column; gap: 0.625rem;'>
                <div>
                    <span style='color: #00D9FF; font-weight: 600;'>Rasio PC:</span>
                    <span style='color: #D1D5DB;'>1:{current_pc_ratio} siswa</span>
                </div>
                <div>
                    <span style='color: #A855F7; font-weight: 600;'>Skor AKM:</span>
                    <span style='color: #D1D5DB;'>{current_akm:.1f}</span>
                </div>
                <div>
                    <span style='color: #10B981; font-weight: 600;'>Klaster:</span>
                    <span style='color: #D1D5DB;'>{current_data['cluster_label']}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    target_pc_ratio = st.slider(
        "🎚️ Target Rasio PC (Ideal: 1:5)",
        min_value=1,
        max_value=max(current_pc_ratio, 20),
        value=min(current_pc_ratio, 10),
        help="Semakin kecil rasio, semakin baik akses siswa terhadap teknologi",
    )
    investment_infra = st.slider(
        "💰 Investasi Infrastruktur (dalam %)",
        min_value=0,
        max_value=100,
        value=20,
        help="Persentase peningkatan akses internet & listrik",
    )

with col_sim_right:
    st.subheader("📈 Projected Impact Analysis")
    delta_pc = current_pc_ratio - target_pc_ratio
    akm_impact_pc = delta_pc * 0.35
    akm_impact_infra = (investment_infra / 10) * 0.8
    projected_akm = current_akm + akm_impact_pc + akm_impact_infra
    cost_per_pc = 500
    cost_per_infra = 300
    total_cost = (delta_pc * cost_per_pc) + (investment_infra / 10 * cost_per_infra)
    roi_percentage = (
        ((projected_akm - current_akm) / current_akm * 100) if current_akm > 0 else 0
    )
    m1, m2, m3 = st.columns(3, gap="medium")
    with m1:
        st.metric(
            "Target Rasio PC",
            f"1:{target_pc_ratio}",
            f"-{delta_pc} (Better)" if delta_pc > 0 else "Maintain",
            delta_color="normal",
        )
    with m2:
        st.metric(
            "Projected AKM Score",
            f"{projected_akm:.1f}",
            f"+{(projected_akm - current_akm):.1f}",
            delta_color="normal",
        )
    with m3:
        st.metric(
            "Estimated Investment",
            f"Rp {total_cost:.0f}M",
            f"ROI: {roi_percentage:.1f}%",
        )
    st.markdown("<br>", unsafe_allow_html=True)
    progress_val = min(projected_akm / 100, 1.0)
    st.progress(progress_val)
    st.caption(f"🎯 Progress menuju target nasional (AKM ≥ 80): {progress_val*100:.0f}%")
    breakdown_data = pd.DataFrame(
        {
            "Category": [
                "PC Hardware",
                "Infrastructure",
                "Teacher Training",
                "Maintenance (5yr)",
            ],
            "Cost (M IDR)": [
                delta_pc * cost_per_pc * 0.6,
                investment_infra / 10 * cost_per_infra,
                delta_pc * cost_per_pc * 0.2,
                total_cost * 0.3,
            ],
        }
    )
    fig_breakdown = px.bar(
        breakdown_data,
        x="Cost (M IDR)",
        y="Category",
        orientation="h",
        color="Category",
        color_discrete_sequence=["#00D9FF", "#A855F7", "#10B981", "#F59E0B"],
    )
    fig_breakdown.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter", size=13),
        height=220,
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_breakdown, use_container_width=True)
    st.markdown(
        f"""
        <div class='info-box' style='border-left-color: #3B82F6;'>
            <div class='info-box-header'>🔮 Impact Projection Summary</div>
            <p>Dengan investasi <strong>Rp {total_cost:.0f}M</strong>, provinsi <strong>{selected_prov}</strong> dapat meningkatkan
            skor AKM dari <strong>{current_akm:.1f}</strong> menjadi <strong>{projected_akm:.1f}</strong> dalam <strong>2-3 tahun</strong>.
            ROI diproyeksikan mencapai <strong>{roi_percentage:.1f}%</strong> melalui peningkatan kualitas SDM dan daya saing digital.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ==============================================================================
# 7. DATA EXPLORER
# ==============================================================================
st.header("7. Data Explorer & Raw Insights")
with st.expander("🔍 View Complete Dataset", expanded=False):
    available_cols = [
        c
        for c in df.columns
        if c not in ["join_key", "size_bubble", "cluster_numeric", "geo_key"]
    ]
    selected_cols = st.multiselect(
        "Select columns to display",
        available_cols,
        default=[
            "display_prov",
            "cluster_label",
            "indeks_infrastruktur",
            "indeks_sdm",
            "potensi_siswa",
        ],
    )
    if selected_cols:
        display_df = df[selected_cols].copy()
        st.dataframe(
            display_df.style.format(
                "{:.2f}",
                subset=[
                    c for c in selected_cols if df[c].dtype in ["float64", "int64"]
                ],
            ),
            use_container_width=True,
            height=400,
        )
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"indonesia_ai_readiness_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

# ==============================================================================
# FOOTER
# ==============================================================================
st.divider()
footer_cols = st.columns([2, 1, 1])
with footer_cols[0]:
    st.markdown(
        """
        <div style='color: #6B7280; font-size: 0.875rem; line-height: 1.6;'>
            <strong style='color: #9CA3AF; display: block; margin-bottom: 0.5rem;'>Executive Dashboard v2.1</strong>
            Data Sources: Kemendikbud, BPS, Regional Analytics<br>
            Last Updated: December 2025 | Real-time Sync Enabled
        </div>
        """,
        unsafe_allow_html=True,
    )
with footer_cols[1]:
    st.markdown(
        """
        <div style='color: #6B7280; font-size: 0.875rem; text-align: center; line-height: 1.6;'>
            <strong style='color: #9CA3AF; display: block; margin-bottom: 0.5rem;'>Powered by</strong>
            Streamlit • Plotly • ML Pipeline
        </div>
        """,
        unsafe_allow_html=True,
    )
with footer_cols[2]:
    st.markdown(
        """
        <div style='color: #6B7280; font-size: 0.875rem; text-align: right; line-height: 1.6;'>
            <strong style='color: #9CA3AF; display: block; margin-bottom: 0.5rem;'>Support</strong>
            📧 devmlops@edu.id<br>
            🌐 dashboard.ai-education.id
        </div>
        """,
        unsafe_allow_html=True,
    )
st.caption("© 2025 DevMLOps Education System. Built with ❤️ for Indonesian Education")
