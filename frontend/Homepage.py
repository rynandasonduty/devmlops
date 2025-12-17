import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Homepage",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. MASTER CSS (Cyberpunk/Dark Theme)
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Headlines */
    h1, h2, h3 {
        color: #F3F4F6;
        font-weight: 800;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Navigation Links */
    div[data-testid="stPageLink-NavLink"] {
        background: transparent;
        border-radius: 8px;
        transition: all 0.3s ease;
        margin-bottom: 5px;
    }
    div[data-testid="stPageLink-NavLink"]:hover {
        background: rgba(0, 217, 255, 0.1);
        transform: translateX(5px);
        border-left: 3px solid #00D9FF;
    }

    /* Hero Text */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00D9FF 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    /* Custom Cards for Goals */
    .goal-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00D9FF;
        padding: 1.5rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
    }

    /* External Link Buttons */
    .stLinkButton > a {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #E5E7EB !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        width: 100%;
        text-align: left !important;
        transition: all 0.3s ease;
    }
    .stLinkButton > a:hover {
        border-color: #00D9FF !important;
        color: #00D9FF !important;
        background-color: rgba(0, 217, 255, 0.1) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Helper Function untuk Render Mermaid
def mermaid(code: str, height=600):
    html_code = f"""
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
    </script>
    <div class="mermaid">
        {code}
    </div>
    """
    components.html(html_code, height=height, scrolling=True)


# 3. SIDEBAR STANDARD
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ External Tools")
    st.link_button(
        "📦 MLflow Registry",
        "http://localhost:5000",
        help="Monitor eksperimen dan model versioning",
    )
    st.link_button(
        "📈 Grafana Monitor",
        "http://localhost:3000",
        help="Dashboard monitoring infrastruktur & drift",
    )

    st.divider()
    st.caption("© 2025 DevMLOps Project")

# 4. HERO SECTION & MAP
col_hero_text, col_hero_img = st.columns([1.5, 2])

with col_hero_text:
    st.markdown(
        '<div class="hero-title">Sistem Cerdas<br>Kesiapan Pendidikan</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 20px;">
    Platform analisis strategis berbasis <b>AI & MLOps</b> untuk pemetaan dan akselerasi
    kurikulum digital di seluruh provinsi Indonesia.
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 Mulai Analisis Data", type="primary"):
        st.switch_page("pages/User_Dashboard.py")

with col_hero_img:
    # Menampilkan Peta Indonesia (Gambar Visual)
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_map_of_Indonesia.svg",
        caption="Cakupan Analisis Nasional (34+ Provinsi)",
        use_container_width=True,
    )

st.markdown("---")

# 5. LATAR BELAKANG & TUJUAN
st.subheader("🎯 Latar Belakang & Ruang Lingkup")

col_bg, col_goals = st.columns([1, 1], gap="large")

with col_bg:
    st.markdown("### 🏢 Tujuan Bisnis")
    st.markdown(
        """
    <div class="goal-card">
    Kementerian Pendidikan/Dinas Pendidikan ingin meluncurkan <b>kurikulum berbasis kecerdasan buatan (AI)</b> secara nasional.
    Namun, implementasi seragam akan gagal karena perbedaan drastis pada <b>infrastruktur</b> (ketersediaan komputer & internet)
    dan <b>SDM</b> (guru tersertifikasi & literasi dasar) antar provinsi.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Tujuan Teknis")
    st.markdown(
        """
    <div class="goal-card" style="border-left-color: #A855F7;">
    Membangun pipeline otomatis <b>(CI/CD/CT)</b> yang meminimalisir intervensi manual dan kesalahan manusia
    dalam proses pengolahan data pendidikan hingga deployment model.
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_goals:
    st.markdown("### 🧠 Tujuan Model (Clustering)")
    st.markdown(
        "Mengidentifikasi kelompok-kelompok homogen (Klaster) provinsi berdasarkan indikator kesiapan:"
    )

    st.info(
        "**Klaster 0 (Tinggi)**\nProvinsi yang siap menerapkan kurikulum AI penuh (misal: Jawa, Bali, Sumatera Utara)."
    )
    st.warning(
        "**Klaster 1 (Menengah)**\nProvinsi yang perlu dukungan fasilitas dasar dan pelatihan guru intensif."
    )
    st.error(
        "**Klaster 2 (Rendah)**\nProvinsi yang perlu fokus pada Literasi, Numerasi, dan pemenuhan sarana dasar (misal: Papua)."
    )

st.markdown("---")

# 6. ARSITEKTUR SISTEM GLOBAL (Mermaid Diagram)
st.subheader("🏗️ Arsitektur Sistem Global")
st.markdown("Sistem dibangun di atas **4 Pilar Arsitektur** yang saling menopang:")

# Mermaid Code Definition
mermaid_code = """
graph TB
    subgraph Data["🗄️ DATA & ORCHESTRATION"]
        PostgreSQL[("PostgreSQL 15")]
        Mage["🔄 Mage.ai<br/>ETL Pipeline"]
    end

    subgraph Experiment["📝 EXPERIMENTATION & VERSIONING"]
        DVC["📦 DVC<br/>Data Version Control"]
        MLflow["📊 MLflow<br/>Experiment Tracking"]
        RemoteStorage[("☁️ Remote Storage<br/>AWS S3")]
    end

    subgraph Training["🧠 MACHINE LEARNING"]
        ScikitLearn["🔬 Scikit-Learn<br/>K-Means"]
        Pipeline["⚙️ Training Pipeline<br/>K=2,3,4,5,6"]
        Visualization["📈 Matplotlib<br/>Elbow Method"]
    end

    subgraph Serving["🚀 SERVING & APPLICATION"]
        FastAPI["⚡ FastAPI<br/>REST API"]
        Streamlit["🎨 Streamlit<br/>Dashboard"]
    end

    subgraph CI["🔄 CI/CD AUTOMATION"]
        Git["📌 Git<br/>Local VCS"]
        GitHub["🌐 GitHub<br/>Remote Repo"]
        Actions["🤖 GitHub Actions<br/>CI/CD Pipeline"]
    end

    subgraph Infrastructure["🏗️ INFRASTRUCTURE"]
        Docker["📦 Docker<br/>Container"]
        Compose["🎭 Docker Compose<br/>Orchestrator"]
        EC2["💻 AWS EC2<br/>Server"]
    end

    subgraph Monitoring["👁️ MONITORING & ALERTS"]
        Prometheus["📊 Prometheus<br/>Metrics"]
        Grafana["📉 Grafana<br/>Dashboard"]
        Evidently["⚠️ Evidently AI<br/>Drift Detection"]
    end

    %% DATA EXTRACTION & LOADING
    PostgreSQL -->|📤 Extract| Mage
    Mage -->|🔄 Transform & Load| Pipeline

    %% VERSIONING FLOW
    Pipeline -->|💾 Snapshot| DVC
    DVC -->|📤 Upload| RemoteStorage

    %% TRAINING & TRACKING
    Pipeline -->|🔬 Train Models| ScikitLearn
    ScikitLearn -->|📊 Generate| Visualization
    Pipeline -->|📝 Log Metrics| MLflow
    Visualization -->|📸 Store| MLflow

    %% MODEL SERVING
    MLflow -->|🏆 Champion Model| FastAPI
    FastAPI -->|📡 API Endpoint| Streamlit

    %% CI/CD PIPELINE
    Git -->|💾 Commit| GitHub
    GitHub -->|🔔 Trigger| Actions
    Actions -->|✅ Test & Build| Docker
    Docker -->|🔗 Compose| Compose

    %% DEPLOYMENT
    Compose -->|🚀 Deploy| EC2
    EC2 -->|🏃 Run| FastAPI
    EC2 -->|🏃 Run| Mage

    %% MONITORING FEEDBACK
    FastAPI -->|📊 Send Metrics| Prometheus
    PostgreSQL -->|📋 Sample Data| Evidently
    Evidently -->|⚠️ Detect Drift| Prometheus
    Prometheus -->|📊 Visualize| Grafana
    Grafana -->|🔔 Alert| Mage
    Mage -->|🔄 Retrain| Pipeline

    %% SECURITY
    Actions -->|🔐 SSH Keys| EC2

    %% Minimalist Styling
    classDef minimal fill:#f5f5f5,stroke:#333,stroke-width:1px,color:#000
    classDef header fill:#e8e8e8,stroke:#333,stroke-width:2px,color:#000
    classDef process fill:#fafafa,stroke:#666,stroke-width:1px,color:#000
    classDef data fill:#f0f0f0,stroke:#555,stroke-width:1px,color:#000
    classDef highlight fill:#f9f9f9,stroke:#333,stroke-width:1.5px,color:#000

    class Data,Experiment,Training,Serving,CI,Infrastructure,Monitoring header
    class PostgreSQL,RemoteStorage,EC2 data
    class Pipeline,FastAPI,Mage,Grafana highlight
    class DVC,MLflow,Docker,Compose,Actions,Git,GitHub,Prometheus,Evidently,ScikitLearn,Visualization,Streamlit minimal
"""

# Render Diagram
with st.container():
    mermaid(mermaid_code, height=850)

# ==============================================================================
# FOOTER
# ==============================================================================
st.divider()
footer_cols = st.columns([2, 1, 1])
with footer_cols[0]:
    st.markdown(
        """
        <div style='color: #6B7280; font-size: 0.875rem; line-height: 1.6;'>
            <strong style='color: #9CA3AF; display: block; margin-bottom: 0.5rem;'>Executive Dashboard for Kurikulum AI</strong>
            Data Sources: Portal Data Pendidikan<br>
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
            Streamlit • Plotly • ML Flow • FastAPI • Mage AI
        </div>
        """,
        unsafe_allow_html=True,
    )
with footer_cols[2]:
    st.markdown(
        """
        <div style='color: #6B7280; font-size: 0.875rem; text-align: right; line-height: 1.6;'>
            <strong style='color: #9CA3AF; display: block; margin-bottom: 0.5rem;'>Support</strong>
            📧 rynanda1202@gmail.com<br>
            🌐 @thenamesagastya
        </div>
        """,
        unsafe_allow_html=True,
    )
st.caption(
    "© 2025 Andiar Rinanda Agastya. Built with ❤️ for Machine Learning Technology Final Project"
)
