import streamlit as st
import pandas as pd
import os
import requests
import json
from datetime import datetime
import time
import hashlib
import shutil
from pathlib import Path
import plotly.express as px
import numpy as np
import secrets

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ENHANCED STYLING
# ==============================================================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Admin Header */
    .admin-header {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(220, 38, 38, 0.3);
        box-shadow: 0 8px 32px rgba(220, 38, 38, 0.2);
    }

    .admin-header h1 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.75rem !important;
    }

    .admin-header p {
        color: rgba(255, 255, 255, 0.8) !important;
        margin: 0.25rem 0 0 0 !important;
        font-size: 0.9rem !important;
    }

    /* Status Indicators */
    .status-online { color: #10B981; font-weight: 600; font-size: 1rem; }
    .status-offline { color: #EF4444; font-weight: 600; font-size: 1rem; }
    .status-pending { color: #F59E0B; font-weight: 600; font-size: 1rem; }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 35, 47, 0.95) 0%, rgba(26, 31, 58, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 1.25rem !important;
        border-radius: 12px;
        border-left: 4px solid #DC2626;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Log Container */
    .log-container {
        background: #0A0E27;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        color: #10B981;
        line-height: 1.6;
    }

    .log-entry {
        margin-bottom: 0.5rem;
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .log-timestamp { color: #60A5FA; font-weight: 600; }
    .log-level-info { color: #10B981; }
    .log-level-warning { color: #F59E0B; }
    .log-level-error { color: #EF4444; }

    /* Validation Box */
    .validation-box {
        background: rgba(30, 35, 47, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .validation-success { border-left: 4px solid #10B981; background: rgba(16, 185, 129, 0.1); }
    .validation-warning { border-left: 4px solid #F59E0B; background: rgba(245, 158, 11, 0.1); }
    .validation-error { border-left: 4px solid #EF4444; background: rgba(239, 68, 68, 0.1); }

    /* Progress Enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #DC2626 0%, #EF4444 100%);
    }

    /* Tabs Styling */
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
        font-size: 0.95rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white !important;
        font-weight: 600;
    }

    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(37, 99, 235, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 4px solid #F59E0B;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Table Styling */
    .dataframe { font-size: 0.9rem; }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 35, 47, 0.6);
        border: 2px dashed rgba(220, 38, 38, 0.5);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Button Enhancement */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3);
    }

    /* Divider */
    hr {
        margin: 2rem 0 !important;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(220, 38, 38, 0.3) 20%, rgba(239, 68, 68, 0.3) 80%, transparent 100%);
    }

    h1, h2, h3, h4 { color: #F3F4F6 !important; }
    p, li, span { color: #D1D5DB !important; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    /* Sidebar Styling - Konsisten */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# CONFIGURATION
# ==============================================================================
MAGE_HOST = "http://mage:6789"
TRIGGER_SCHEDULE_ID = int(os.getenv("TRIGGER_SCHEDULE_ID", "2"))
TRIGGER_TOKEN = os.getenv("TRIGGER_TOKEN", "189557234d5e431a972f6d0926b719e9")

# Paths - Shared Volume Configuration
BASE_DIR = Path("/app/mage_data_source")  # Root shared folder
DATA_RAW_DIR = BASE_DIR / "data/raw"  # Raw data storage
ARTIFACTS_DIR = BASE_DIR / "artifacts"  # Pipeline outputs


# File Paths
TARGET_FILE = DATA_RAW_DIR / "data_kesiapan_pendidikan_final.csv"
VERSION_HISTORY_FILE = DATA_RAW_DIR / "version_history.json"
API_KEYS_FILE = BASE_DIR / ".api_keys.json"
PIPELINE_LOGS_FILE = BASE_DIR / "pipeline_logs.json"

# Ensure directories exist
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

# Admin Password (ENV VAR or default)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# ==============================================================================
# STANDARD SIDEBAR (Tambahkan ini di Dashboard_Publik.py dan Data_Management.py)
# ==============================================================================
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
    st.caption("© Andiar Rinanda Agastya")


# ==============================================================================
# AUTHENTICATION
# ==============================================================================
def check_admin_access():
    """Simple admin authentication"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown(
            """
        <div class='admin-header'>
            <h1>🔒 Admin Access Required</h1>
            <p>Please authenticate to access the management panel</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Enter Admin Password", type="password")

            if st.button("🔓 Login", type="primary", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.login_time = datetime.now()
                    st.session_state.user = "admin"
                    st.success("✅ Authentication successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")

        st.info("💡 Hint: Default password is 'admin123' (change in production!)")
        st.stop()


check_admin_access()


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================
def get_file_hash(file_path):
    """Calculate MD5 hash of file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def save_version_metadata(filename, user, df_info, file_hash):
    """Save upload history with versioning"""
    try:
        if VERSION_HISTORY_FILE.exists():
            with open(VERSION_HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []

        version_num = len(history) + 1
        version_file = DATA_RAW_DIR / f"data_v{version_num}.csv"

        # Copy current file to versioned backup
        if TARGET_FILE.exists():
            shutil.copy(TARGET_FILE, version_file)

        history.append(
            {
                "version": version_num,
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "user": user,
                "rows": df_info["rows"],
                "columns": df_info["columns"],
                "file_hash": file_hash,
                "file_path": str(version_file),
                "is_active": True,
            }
        )

        # Mark previous versions as inactive
        for h in history[:-1]:
            h["is_active"] = False

        with open(VERSION_HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

        return version_num

    except Exception as e:
        st.error(f"Failed to save version: {e}")
        return None


def load_version_history():
    """Load version history"""
    if VERSION_HISTORY_FILE.exists():
        with open(VERSION_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def rollback_version(version_num):
    """Rollback to specific version"""
    try:
        history = load_version_history()
        target_version = next((v for v in history if v["version"] == version_num), None)

        if target_version and Path(target_version["file_path"]).exists():
            # Copy versioned file to active
            shutil.copy(target_version["file_path"], TARGET_FILE)

            # Update active status
            for v in history:
                v["is_active"] = v["version"] == version_num

            with open(VERSION_HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)

            return True
        return False
    except Exception as e:
        st.error(f"Rollback failed: {e}")
        return False


def validate_dataframe(df):
    """Comprehensive data validation specific to Education Readiness Data"""
    issues = {"errors": [], "warnings": [], "info": []}

    # 1. Check required columns
    required_cols = ["Provinsi"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        issues["errors"].append(f"Missing required columns: {', '.join(missing)}")

    # 2. Check essential numeric columns presence
    essential_metrics = [
        "persen_sekolah_internet_sd",
        "persen_sekolah_internet_smp",
        "persen_guru_sertifikasi_sd",
        "rasio_siswa_guru_sd",
        "persen_lulus_akm_literasi",
        "persen_lulus_akm_numerasi",
    ]
    missing_metrics = [c for c in essential_metrics if c not in df.columns]
    if missing_metrics:
        issues["warnings"].append(
            f"Missing recommended metrics: {', '.join(missing_metrics)}"
        )

    # 3. Check data types and ranges
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if "persen" in col.lower():
            if df[col].max() > 100:
                issues["warnings"].append(f"Column '{col}' has values > 100%")
            if df[col].min() < 0:
                issues["errors"].append(f"Column '{col}' has negative values")

    # 4. Check for duplicates
    if "Provinsi" in df.columns:
        dups = df["Provinsi"].duplicated().sum()
        if dups > 0:
            issues["errors"].append(f"Found {dups} duplicate entries in 'Provinsi'")

    # 5. Row count validation
    if len(df) < 10:
        issues["warnings"].append(f"Dataset seems too small ({len(df)} rows)")

    return issues


def get_mage_status():
    """Check Mage engine status"""
    try:
        res = requests.get(f"{MAGE_HOST}/api/statuses", timeout=5)
        if res.status_code == 200:
            return {"status": "online", "code": 200}
        else:
            return {"status": "error", "code": res.status_code}
    except requests.exceptions.RequestException:
        return {"status": "offline", "code": 0}


def trigger_pipeline(variables=None):
    """Trigger Mage pipeline execution"""
    api_url = f"{MAGE_HOST}/api/pipeline_schedules/{TRIGGER_SCHEDULE_ID}/api_trigger"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TRIGGER_TOKEN}",
    }

    payload = {"pipeline_run": {"variables": variables or {}}}

    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=10)
        return res
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None


def get_pipeline_status(run_id):
    """Fetch pipeline run status"""
    try:
        res = requests.get(
            f"{MAGE_HOST}/api/pipeline_runs/{run_id}",
            headers={"Authorization": f"Bearer {TRIGGER_TOKEN}"},
            timeout=5,
        )
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None


def save_pipeline_log(run_id, status, details):
    """Save pipeline execution log"""
    try:
        if PIPELINE_LOGS_FILE.exists():
            with open(PIPELINE_LOGS_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(
            {
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "details": details,
                "user": st.session_state.get("user", "unknown"),
            }
        )

        # Keep only last 100 logs
        logs = logs[-100:]

        with open(PIPELINE_LOGS_FILE, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"Failed to save log: {e}")


def load_pipeline_logs():
    """Load pipeline logs"""
    if PIPELINE_LOGS_FILE.exists():
        with open(PIPELINE_LOGS_FILE, "r") as f:
            return json.load(f)
    return []


def generate_data_profile(df):
    """Generate comprehensive data profile"""
    profile = {
        "basic_stats": {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            "duplicates": df.duplicated().sum(),
        },
        "column_types": df.dtypes.astype(str).value_counts().to_dict(),
        "missing_data": df.isnull().sum().to_dict(),
        "numeric_stats": {},
    }

    # Numeric column statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        profile["numeric_stats"][col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "q25": float(df[col].quantile(0.25)),
            "q75": float(df[col].quantile(0.75)),
        }

    return profile


def load_api_keys():
    """Load API keys configuration"""
    if API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    return {"keys": []}


def save_api_key(key_name, key_value, description):
    """Save new API key"""
    keys_data = load_api_keys()

    keys_data["keys"].append(
        {
            "name": key_name,
            "key": key_value,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "created_by": st.session_state.get("user", "unknown"),
            "is_active": True,
        }
    )

    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys_data, f, indent=2)


def rotate_api_key(key_name, new_key_value):
    """Rotate existing API key"""
    keys_data = load_api_keys()

    for key in keys_data["keys"]:
        if key["name"] == key_name:
            key["key"] = new_key_value
            key["rotated_at"] = datetime.now().isoformat()
            break

    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys_data, f, indent=2)


def list_artifacts():
    """List all available artifacts from Shared Volume"""
    artifacts = []

    if ARTIFACTS_DIR.exists():
        for file in ARTIFACTS_DIR.glob("*"):
            if file.is_file():
                artifacts.append(
                    {
                        "name": file.name,
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(file.stat().st_mtime),
                        "path": str(file),
                    }
                )

    return sorted(artifacts, key=lambda x: x["modified"], reverse=True)


def load_cluster_comparison():
    """Load cluster metadata for comparison"""
    metadata_path = ARTIFACTS_DIR / "cluster_metadata.json"

    if metadata_path.exists():
        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except:
            return None
    return None


# ==============================================================================
# HEADER
# ==============================================================================
st.markdown(
    f"""
<div class='admin-header'>
    <h1>⚙️ Admin Dashboard - Data and Pipeline Management</h1>
    <p>👤 User: {st.session_state.user} | 🕐 Login: {st.session_state.login_time.strftime('%H:%M:%S')}</p>
</div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# QUICK STATS DASHBOARD
# ==============================================================================
st.subheader("📊 System Overview")

col1, col2, col3, col4, col5 = st.columns(5)

# Last Upload
history = load_version_history()
if history:
    last_upload = history[-1]
    last_upload_time = datetime.fromisoformat(last_upload["timestamp"])
    time_diff = datetime.now() - last_upload_time
    days_ago = time_diff.days
    hours_ago = time_diff.seconds // 3600

    if days_ago > 0:
        delta_text = f"{days_ago}d ago"
    else:
        delta_text = f"{hours_ago}h ago"

    with col1:
        st.metric(
            "Last Upload",
            last_upload_time.strftime("%Y-%m-%d"),
            delta_text,
            delta_color="off",
        )
else:
    with col1:
        st.metric("Last Upload", "No data", "Never")

# Pipeline Status
mage_status = get_mage_status()
with col2:
    if mage_status["status"] == "online":
        st.metric("Pipeline", "🟢 Ready", "Online")
    else:
        st.metric("Pipeline", "🔴 Down", "Offline", delta_color="inverse")

# Data Version
with col3:
    current_version = f"v{len(history)}" if history else "v0"
    st.metric("Data Version", current_version, f"{len(history)} total")

# Cluster Model
cluster_meta = load_cluster_comparison()
if cluster_meta:
    with col4:
        sil_score = cluster_meta.get("silhouette_score", 0)
        st.metric("Model Score", f"{sil_score:.3f}", "Silhouette")

    with col5:
        n_clusters = cluster_meta.get("n_clusters", 0)
        st.metric("Clusters", n_clusters, "Active")
else:
    with col4:
        st.metric("Model Score", "N/A", "Not trained")
    with col5:
        st.metric("Clusters", "N/A", "Not trained")

st.divider()

# ==============================================================================
# MAIN TABS
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📥 Data Upload",
        "🚀 Pipeline Control",
        "📊 Monitoring",
        "📋 Version History",
        "📈 Data Profiling",
        "🔑 API Keys",
        "📦 Artifacts",
    ]
)

# ==============================================================================
# TAB 1: DATA UPLOAD & VALIDATION (REVISED)
# ==============================================================================
with tab1:
    st.subheader("📥 Data Upload & Synchronization")

    st.markdown(
        """
        <div class='info-box'>
            <strong>ℹ️ Workflow Update Data:</strong><br>
            1. <strong>Upload CSV:</strong> File akan divalidasi dan disimpan ke server.<br>
            2. <strong>Update Database:</strong> Tekan tombol 'Update Database' untuk menjalankan pipeline seeding ke PostgreSQL.<br>
            3. <strong>Retrain Model:</strong> Setelah database update, pindah ke Tab Pipeline Control untuk melatih ulang model.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Single File Upload
    st.markdown("#### 📘 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Pilih file CSV terbaru", type="csv", help="Format: CSV UTF-8"
    )

    if uploaded_file is not None:
        try:
            df_new = pd.read_csv(uploaded_file)

            # Preview & Stats Container
            col_preview, col_stats = st.columns([2, 1])
            with col_preview:
                st.markdown("##### 📊 Data Preview")
                st.dataframe(df_new.head(5), use_container_width=True)
            with col_stats:
                st.markdown("##### 📈 Quick Stats")
                st.write(f"**Rows:** {len(df_new):,}")
                st.write(f"**Cols:** {len(df_new.columns)}")
                if "Provinsi" in df_new.columns:
                    st.success("✅ Kolom 'Provinsi' ditemukan")
                else:
                    st.error("❌ Kolom 'Provinsi' hilang!")

            # Validation Logic
            issues = validate_dataframe(df_new)

            # Tampilkan Error/Warning jika ada
            if issues["errors"]:
                for err in issues["errors"]:
                    st.error(err)

            # Logic Tombol Save
            st.divider()
            can_save = len(issues["errors"]) == 0

            if can_save:
                col_btn1, col_btn2 = st.columns(2)

                # TOMBOL 1: HANYA SAVE CSV
                with col_btn1:
                    if st.button(
                        "💾 1. Save CSV to Server",
                        type="primary",
                        use_container_width=True,
                    ):
                        try:
                            # Save file ke Shared Volume
                            df_new.to_csv(TARGET_FILE, index=False)

                            # Log Versioning
                            file_hash = get_file_hash(TARGET_FILE)
                            version = save_version_metadata(
                                uploaded_file.name,
                                st.session_state.user,
                                {"rows": len(df_new), "columns": len(df_new.columns)},
                                file_hash,
                            )
                            st.success(f"✅ File tersimpan di Server (v{version})")
                            st.info(f"Path: `{TARGET_FILE}`")

                        except Exception as e:
                            st.error(f"Gagal menyimpan: {e}")

                # TOMBOL 2: TRIGGER PIPELINE SEEDING (Sesuai Endpoint Anda)
                with col_btn2:
                    if st.button(
                        "🚀 Update Database (Run Seeding)",
                        type="secondary",
                        use_container_width=True,
                    ):
                        with st.spinner(
                            "Menjalankan Pipeline ETL (CSV -> Postgres)..."
                        ):
                            try:
                                # KONFIGURASI API MAGE (SESUAI PERMINTAAN ANDA)
                                # Gunakan nama service docker 'mage' bukan 'localhost' karena antar container
                                MAGE_API_URL = "http://mage:6789/api/pipeline_schedules/3/api_trigger"
                                MAGE_TOKEN = (
                                    "de8a9d9750d34badb5d7fdea04519247"  # Token Anda
                                )

                                headers = {
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {MAGE_TOKEN}",
                                }

                                # Payload (Opsional, tapi bagus untuk logging di Mage)
                                payload = {
                                    "pipeline_run": {
                                        "variables": {
                                            "source": "admin_dashboard",
                                            "action": "seeding_database",
                                        }
                                    }
                                }

                                # Request ke Mage
                                response = requests.post(
                                    MAGE_API_URL,
                                    headers=headers,
                                    json=payload,
                                    timeout=10,
                                )

                                if response.status_code == 200:
                                    run_data = response.json()
                                    run_id = run_data.get("pipeline_run", {}).get(
                                        "id", "Unknown"
                                    )
                                    st.success(f"✅ Pipeline Berjalan! Run ID: {run_id}")
                                    st.caption(
                                        "Cek status detail di Tab 'Pipeline Control' atau Mage UI."
                                    )
                                    st.balloons()
                                else:
                                    st.error(f"❌ Gagal Trigger: {response.status_code}")
                                    st.code(response.text)

                            except Exception as e:
                                st.error(f"❌ Koneksi Error: {str(e)}")
                                st.info("Pastikan container Mage berjalan.")

            else:
                st.error("🚫 Perbaiki error validasi di atas sebelum menyimpan.")

        except Exception as e:
            st.error(f"Error membaca file: {e}")

    # Multi-File Upload
    st.markdown("---")
    st.markdown("#### 📚 Batch Upload (Multi-File)")

    uploaded_files = st.file_uploader(
        "Upload multiple CSV files",
        type="csv",
        accept_multiple_files=True,
        help="Select multiple CSV files for batch processing",
    )

    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} files selected")

        if st.button("🔄 Process All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Processing: {file.name}...")

                try:
                    df = pd.read_csv(file)
                    issues = validate_dataframe(df)

                    if len(issues["errors"]) == 0:
                        # Save with incremental naming
                        output_name = f"batch_{idx+1}_{file.name}"
                        output_path = DATA_RAW_DIR / output_name
                        df.to_csv(output_path, index=False)

                        st.success(f"✅ {file.name} → Saved")
                    else:
                        st.error(f"❌ {file.name} → Validation failed")

                except Exception as e:
                    st.error(f"❌ {file.name} → Error: {e}")

                progress_bar.progress((idx + 1) / len(uploaded_files))

            status_text.text("✅ Batch processing complete!")

# ==============================================================================
# TAB 2: PIPELINE CONTROL
# ==============================================================================
with tab2:
    st.subheader("🚀 Pipeline Orchestration Control")
    col_status, col_trigger = st.columns([1, 2])

    with col_status:
        st.markdown("#### System Status")

        mage_status = get_mage_status()

        if mage_status["status"] == "online":
            st.markdown(
                """
            <div class='success-box'>
                <strong class='status-online'>🟢 Mage Engine: ONLINE</strong><br>
                <span style='color: #9CA3AF; font-size: 0.85rem;'>Ready to accept pipeline requests</span>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
            <div class='validation-box validation-error'>
                <strong class='status-offline'>🔴 Mage Engine: OFFLINE</strong><br>
                <span style='color: #9CA3AF; font-size: 0.85rem;'>Cannot connect to orchestration service</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown("#### Quick Info")
        st.markdown(
            f"""
        - **Host:** `{MAGE_HOST}`
        - **Schedule ID:** `{TRIGGER_SCHEDULE_ID}`
        - **Token:** `{TRIGGER_TOKEN[:8]}...`
        """
        )

    with col_trigger:
        st.markdown("#### Manual Pipeline Trigger")

        st.markdown(
            """
        <div class='info-box'>
            <strong>ℹ️ Pipeline Stages:</strong><br>
            1. Data Loading & Preprocessing<br>
            2. Feature Engineering<br>
            3. Clustering with KMeans<br>
            4. Model Evaluation & SHAP Analysis<br>
            5. Results Export & Artifacts Generation<br>
            <br>
            <strong>⏱️ Estimated Duration:</strong> 2-5 minutes
        </div>
        """,
            unsafe_allow_html=True,
        )

        trigger_reason = st.text_input(
            "Trigger Reason (Optional)", placeholder="e.g., New data uploaded"
        )

        if st.button(
            "▶️ Trigger Pipeline Now", type="primary", use_container_width=True
        ):
            with st.status("🚀 Starting Pipeline Execution...", expanded=True) as status:
                st.write("📡 Connecting to Mage API...")

                # 1. Trigger Pipeline
                variables = {
                    "triggered_by": st.session_state.user,
                    "trigger_time": datetime.now().isoformat(),
                    "reason": trigger_reason or "Manual trigger",
                    "overwrite_db": True,
                }

                res = trigger_pipeline(variables)

                if res and res.status_code == 200:
                    run_data = res.json()
                    run_id = run_data.get("pipeline_run", {}).get("id")

                    if run_id:
                        st.write(f"✅ Pipeline Triggered! Run ID: `{run_id}`")
                        save_pipeline_log(run_id, "triggered", variables)

                        # 2. Polling Loop with Timeout
                        st.write("⏳ Waiting for completion (Timeout: 300s)...")
                        progress_bar = st.progress(0)

                        max_retries = 60  # 5 minutes timeout
                        is_completed = False

                        for i in range(max_retries):
                            time.sleep(5)

                            try:
                                status_res = requests.get(
                                    f"{MAGE_HOST}/api/pipeline_runs/{run_id}",
                                    headers={
                                        "Authorization": f"Bearer {TRIGGER_TOKEN}"
                                    },
                                    timeout=5,
                                )

                                if status_res.status_code == 200:
                                    current_status = (
                                        status_res.json()
                                        .get("pipeline_run", {})
                                        .get("status")
                                    )
                                    st.write(
                                        f"🔹 Status: **{current_status}** (Time: {i*5}s)"
                                    )

                                    # Fake progress for UX
                                    progress_bar.progress(min((i + 1) * 2, 95))

                                    if current_status == "completed":
                                        progress_bar.progress(100)
                                        status.update(
                                            label="✅ Pipeline Success!",
                                            state="complete",
                                        )
                                        st.success("Pipeline finished! Data updated.")
                                        st.balloons()
                                        is_completed = True
                                        save_pipeline_log(
                                            run_id, "completed", {"duration": i * 5}
                                        )
                                        time.sleep(2)
                                        st.rerun()
                                        break

                                    elif current_status in ["failed", "cancelled"]:
                                        status.update(
                                            label="❌ Pipeline Failed", state="error"
                                        )
                                        st.error("Pipeline execution failed.")
                                        save_pipeline_log(
                                            run_id,
                                            "failed",
                                            {"final_status": current_status},
                                        )
                                        is_completed = True
                                        break
                            except Exception as e:
                                st.warning(f"⚠️ Connection glitch: {str(e)}")

                        if not is_completed:
                            status.update(label="⏱️ Timeout", state="error")
                            st.error("Pipeline timed out. Check Mage UI.")
                    else:
                        status.update(label="❌ No Run ID", state="error")
                else:
                    status.update(label="❌ Trigger Failed", state="error")
                    st.error(f"API Error: {res.status_code if res else 'No Response'}")

        st.markdown("---")

        st.markdown(
            """
        <div class='warning-box'>
            <strong>⚠️ Important Notes:</strong><br>
            • Only trigger after uploading new data<br>
            • Do not trigger multiple times simultaneously<br>
            • Check monitoring tab for real-time progress<br>
            • Artifacts will be updated after completion
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==============================================================================
# TAB 3: MONITORING & LOGS
# ==============================================================================
with tab3:
    st.subheader("📊 Real-time Monitoring & Logs")
    # Pipeline Logs
    st.markdown("#### 📋 Recent Pipeline Executions")

    logs = load_pipeline_logs()

    if logs:
        df_logs = pd.DataFrame(logs)
        df_logs["timestamp"] = pd.to_datetime(df_logs["timestamp"])
        df_logs = df_logs.sort_values("timestamp", ascending=False)

        # Display as table
        st.dataframe(
            df_logs[["timestamp", "run_id", "status", "user", "details"]].head(20),
            use_container_width=True,
            height=300,
        )

        # Visualization
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("##### Status Distribution")

            status_counts = df_logs["status"].value_counts()

            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color=status_counts.index,
                color_discrete_map={
                    "completed": "#10B981",
                    "failed": "#EF4444",
                    "triggered": "#F59E0B",
                },
                hole=0.5,
            )

            fig_status.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", size=12),
                height=300,
            )

            st.plotly_chart(fig_status, use_container_width=True)

        with col_chart2:
            st.markdown("##### Executions Over Time")

            df_logs["date"] = df_logs["timestamp"].dt.date
            daily_counts = df_logs.groupby("date").size().reset_index(name="count")

            fig_timeline = px.line(
                daily_counts,
                x="date",
                y="count",
                markers=True,
                line_shape="spline",
            )

            fig_timeline.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", size=12),
                height=300,
                xaxis_title="Date",
                yaxis_title="Executions",
            )

            st.plotly_chart(fig_timeline, use_container_width=True)

    else:
        st.info("📭 No pipeline logs found")

    st.markdown("---")

    # System Logs Viewer
    st.markdown("#### 🔍 Detailed Log Viewer")

    if logs:
        selected_log = st.selectbox(
            "Select log entry",
            range(len(logs)),
            format_func=lambda x: f"{logs[x]['timestamp']} - {logs[x]['run_id']} - {logs[x]['status']}",
        )

        if selected_log is not None:
            log_entry = logs[selected_log]

            st.markdown(
                f"""
            <div class='log-container'>
                <div class='log-entry'>
                    <span class='log-timestamp'>[{log_entry['timestamp']}]</span>
                    <span class='log-level-info'> INFO </span>
                    <span>Run ID: {log_entry['run_id']}</span>
                </div>
                <div class='log-entry'>
                    <span class='log-timestamp'>[{log_entry['timestamp']}]</span>
                    <span class='log-level-info'> INFO </span>
                    <span>Status: {log_entry['status'].upper()}</span>
                </div>
                <div class='log-entry'>
                    <span class='log-timestamp'>[{log_entry['timestamp']}]</span>
                    <span class='log-level-info'> INFO </span>
                    <span>User: {log_entry['user']}</span>
                </div>
                <div class='log-entry'>
                    <span class='log-timestamp'>[{log_entry['timestamp']}]</span>
                    <span class='log-level-info'> INFO </span>
                    <span>Details: {json.dumps(log_entry['details'], indent=2)}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

# ==============================================================================
# TAB 4: VERSION HISTORY & ROLLBACK
# ==============================================================================
with tab4:
    st.subheader("📜 Data Version History")
    history = load_version_history()

    if history:
        st.markdown(f"#### Total Versions: {len(history)}")

        # Display history table
        df_history = pd.DataFrame(history)
        df_history["timestamp"] = pd.to_datetime(df_history["timestamp"])

        # Format for display
        display_df = df_history[
            ["version", "timestamp", "filename", "user", "rows", "columns", "is_active"]
        ].copy()
        display_df["timestamp"] = display_df["timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        st.dataframe(display_df, use_container_width=True, height=400)

        # Rollback Section
        st.markdown("---")
        st.markdown("#### ⏮️ Version Rollback")

        st.markdown(
            """
        <div class='warning-box'>
            <strong>⚠️ Warning:</strong><br>
            Rolling back will replace the current active data with the selected version.
            This action will create a new version entry but preserve the old data.
        </div>
        """,
            unsafe_allow_html=True,
        )

        col_select, col_action = st.columns([2, 1])

        with col_select:
            inactive_versions = [v for v in history if not v["is_active"]]

            if inactive_versions:
                selected_version = st.selectbox(
                    "Select version to rollback",
                    [v["version"] for v in inactive_versions],
                    format_func=lambda x: f"v{x} - {next(v['timestamp'] for v in history if v['version'] == x)} - {next(v['filename'] for v in history if v['version'] == x)}",
                )

                selected_data = next(
                    v for v in history if v["version"] == selected_version
                )

                st.markdown(
                    f"""
                **Version Details:**
                - **Uploaded:** {selected_data['timestamp']}
                - **File:** {selected_data['filename']}
                - **User:** {selected_data['user']}
                - **Rows:** {selected_data['rows']:,}
                - **Columns:** {selected_data['columns']}
                """
                )
            else:
                st.info("No inactive versions available for rollback")
                selected_version = None

        with col_action:
            if selected_version:
                st.markdown("<br><br>", unsafe_allow_html=True)

                if st.button(
                    f"⏮️ Rollback to v{selected_version}",
                    type="primary",
                    use_container_width=True,
                ):
                    with st.spinner("Rolling back..."):
                        success = rollback_version(selected_version)

                        if success:
                            st.success(
                                f"✅ Successfully rolled back to version v{selected_version}!"
                            )
                            st.balloons()

                            # Log the rollback
                            save_pipeline_log(
                                f"rollback_v{selected_version}",
                                "rollback",
                                {
                                    "target_version": selected_version,
                                    "user": st.session_state.user,
                                },
                            )

                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Rollback failed!")

        # Version Comparison
        st.markdown("---")
        st.markdown("#### 🔄 Version Comparison")

        if len(history) >= 2:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                version1 = st.selectbox(
                    "Version 1",
                    [v["version"] for v in history],
                    format_func=lambda x: f"v{x}",
                    key="v1",
                )

            with col_v2:
                version2 = st.selectbox(
                    "Version 2",
                    [v["version"] for v in history],
                    format_func=lambda x: f"v{x}",
                    key="v2",
                )

            if version1 != version2:
                v1_data = next(v for v in history if v["version"] == version1)
                v2_data = next(v for v in history if v["version"] == version2)

                comp_col1, comp_col2, comp_col3 = st.columns(3)

                with comp_col1:
                    rows_diff = v2_data["rows"] - v1_data["rows"]
                    st.metric(
                        "Rows Change",
                        v2_data["rows"],
                        f"{rows_diff:+d}",
                        delta_color="normal",
                    )

                with comp_col2:
                    cols_diff = v2_data["columns"] - v1_data["columns"]
                    st.metric(
                        "Columns Change",
                        v2_data["columns"],
                        f"{cols_diff:+d}",
                        delta_color="normal",
                    )

                with comp_col3:
                    time_diff = datetime.fromisoformat(
                        v2_data["timestamp"]
                    ) - datetime.fromisoformat(v1_data["timestamp"])
                    st.metric(
                        "Time Difference", f"{time_diff.days}d", "Between versions"
                    )

    else:
        st.info("📭 No version history available. Upload data to create first version.")

# ==============================================================================
# TAB 5: DATA PROFILING
# ==============================================================================
with tab5:
    st.subheader("📈 Advanced Data Profiling & Analysis")
    if TARGET_FILE.exists():
        try:
            df = pd.read_csv(TARGET_FILE)

            # Generate profile
            with st.spinner("Generating data profile..."):
                profile = generate_data_profile(df)

            # Basic Stats
            st.markdown("#### 📊 Basic Statistics")

            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

            with col_stat1:
                st.metric("Total Rows", f"{profile['basic_stats']['rows']:,}")

            with col_stat2:
                st.metric("Total Columns", profile["basic_stats"]["columns"])

            with col_stat3:
                st.metric("Memory Usage", profile["basic_stats"]["memory_usage"])

            with col_stat4:
                st.metric("Duplicates", profile["basic_stats"]["duplicates"])

            st.markdown("---")

            # Column Types Distribution
            st.markdown("#### 🔤 Column Type Distribution")

            col_types_df = pd.DataFrame(
                list(profile["column_types"].items()), columns=["Type", "Count"]
            )

            fig_types = px.bar(
                col_types_df,
                x="Type",
                y="Count",
                color="Type",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )

            fig_types.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", size=12),
                height=300,
                showlegend=False,
            )

            st.plotly_chart(fig_types, use_container_width=True)

            st.markdown("---")

            # Missing Data Analysis
            st.markdown("#### 🕳️ Missing Data Analysis")

            missing_df = pd.DataFrame(
                list(profile["missing_data"].items()),
                columns=["Column", "Missing Count"],
            )
            missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values(
                "Missing Count", ascending=False
            )

            if len(missing_df) > 0:
                missing_df["Missing %"] = (
                    missing_df["Missing Count"] / profile["basic_stats"]["rows"] * 100
                ).round(2)

                fig_missing = px.bar(
                    missing_df.head(15),
                    x="Missing Count",
                    y="Column",
                    orientation="h",
                    color="Missing %",
                    color_continuous_scale="Reds",
                )

                fig_missing.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=12),
                    height=400,
                )

                st.plotly_chart(fig_missing, use_container_width=True)

            else:
                st.success("✅ No missing data detected!")

            st.markdown("---")

            # Numeric Statistics
            st.markdown("#### 📉 Numeric Column Statistics")

            if profile["numeric_stats"]:
                # Select column to analyze
                numeric_cols = list(profile["numeric_stats"].keys())
                selected_col = st.selectbox(
                    "Select column for detailed analysis", numeric_cols
                )

                if selected_col:
                    stats = profile["numeric_stats"][selected_col]

                    col_det1, col_det2, col_det3, col_det4 = st.columns(4)

                    with col_det1:
                        st.metric("Mean", f"{stats['mean']:.2f}")
                        st.metric("Median", f"{stats['median']:.2f}")

                    with col_det2:
                        st.metric("Std Dev", f"{stats['std']:.2f}")
                        st.metric("Min", f"{stats['min']:.2f}")

                    with col_det3:
                        st.metric("Max", f"{stats['max']:.2f}")
                        st.metric("Q1 (25%)", f"{stats['q25']:.2f}")

                    with col_det4:
                        st.metric("Q3 (75%)", f"{stats['q75']:.2f}")
                        iqr = stats["q75"] - stats["q25"]
                        st.metric("IQR", f"{iqr:.2f}")

                    # Distribution plot
                    st.markdown("##### Distribution Plot")

                    fig_dist = px.histogram(
                        df,
                        x=selected_col,
                        nbins=30,
                        marginal="box",
                        color_discrete_sequence=["#DC2626"],
                    )

                    fig_dist.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white", size=12),
                        height=400,
                    )

                    st.plotly_chart(fig_dist, use_container_width=True)

                    # Outlier Detection
                    st.markdown("##### 🔍 Outlier Detection (IQR Method)")

                    lower_bound = stats["q25"] - 1.5 * iqr
                    upper_bound = stats["q75"] + 1.5 * iqr

                    outliers = df[
                        (df[selected_col] < lower_bound)
                        | (df[selected_col] > upper_bound)
                    ]

                    if len(outliers) > 0:
                        st.warning(
                            f"⚠️ Found {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)"
                        )

                        st.markdown(f"**Lower Bound:** {lower_bound:.2f}")
                        st.markdown(f"**Upper Bound:** {upper_bound:.2f}")

                        st.dataframe(
                            (
                                outliers[["Provinsi", selected_col]].head(10)
                                if "Provinsi" in df.columns
                                else outliers.head(10)
                            ),
                            use_container_width=True,
                        )
                    else:
                        st.success("✅ No outliers detected using IQR method")

            else:
                st.info("No numeric columns found in dataset")

            st.markdown("---")

            # Correlation Heatmap
            st.markdown("#### 🔗 Correlation Matrix")

            numeric_df = df.select_dtypes(include=[np.number])

            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr()

                fig_corr = px.imshow(
                    corr_matrix,
                    labels=dict(color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    color_continuous_scale="RdBu_r",
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                )

                fig_corr.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=10),
                    height=600,
                )

                st.plotly_chart(fig_corr, use_container_width=True)

                # Top correlations
                st.markdown("##### 🔝 Top Positive Correlations")

                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i + 1, len(corr_matrix.columns)):
                        corr_pairs.append(
                            {
                                "Variable 1": corr_matrix.columns[i],
                                "Variable 2": corr_matrix.columns[j],
                                "Correlation": corr_matrix.iloc[i, j],
                            }
                        )

                corr_df = pd.DataFrame(corr_pairs).sort_values(
                    "Correlation", ascending=False, key=abs
                )

                st.dataframe(
                    corr_df.head(10).style.format({"Correlation": "{:.3f}"}),
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")

    else:
        st.info("📭 No data file found. Please upload data first.")

# ==============================================================================
# TAB 6: API KEY MANAGEMENT
# ==============================================================================
with tab6:
    st.subheader("🔑 API Key Management")

    st.markdown(
        """
    <div class='warning-box'>
        <strong>⚠️ Security Notice:</strong><br>
        API keys are stored locally and should be rotated regularly.
        Never share keys or commit them to version control.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load existing keys
    keys_data = load_api_keys()

    # Display existing keys
    st.markdown("#### 🔐 Active API Keys")
    if keys_data["keys"]:
        for idx, key in enumerate(keys_data["keys"]):
            if key.get("is_active", True):
                with st.expander(
                    f"🔑 {key['name']} - Created: {key['created_at'][:10]}"
                ):
                    col_key1, col_key2 = st.columns([3, 1])
                    with col_key1:
                        st.markdown(f"**Description:** {key['description']}")
                        st.markdown(f"**Created by:** {key['created_by']}")
                        # Masked key display
                        masked_key = f"{key['key'][:8]}...{key['key'][-8:]}"
                        st.code(masked_key, language="text")
                        if "rotated_at" in key:
                            st.markdown(f"**Last Rotated:** {key['rotated_at'][:10]}")
                    with col_key2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        # Rotate button
                        if st.button(
                            "🔄 Rotate", key=f"rotate_{idx}", use_container_width=True
                        ):
                            new_key = secrets.token_urlsafe(32)
                            rotate_api_key(key["name"], new_key)
                            st.success(f"✅ Key rotated for {key['name']}")
                            time.sleep(1)
                            st.rerun()
    else:
        st.info("📭 No API keys configured")

    st.markdown("---")

    # Add new key form
    st.markdown("#### ➕ Add New API Key")
    with st.form("add_key_form"):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            key_name = st.text_input("Key Name", placeholder="e.g., Production API")
        with col_form2:
            key_description = st.text_input(
                "Description", placeholder="e.g., Used for production deployment"
            )

        generate_auto = st.checkbox("Auto-generate secure key", value=True)

        if not generate_auto:
            key_value = st.text_input(
                "Key Value", type="password", placeholder="Enter custom key"
            )
        else:
            key_value = None

        submitted = st.form_submit_button("💾 Save API Key")

        if submitted:
            if not key_name or not key_description:
                st.error("❌ Key Name and Description are required!")
            else:
                if generate_auto:
                    # Generate a secure 32-byte URL-safe token
                    final_key_value = secrets.token_urlsafe(32)
                else:
                    final_key_value = key_value

                if final_key_value:
                    save_api_key(key_name, final_key_value, key_description)
                    st.success(f"✅ API Key '{key_name}' created successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Key value cannot be empty!")

# ==============================================================================
# TAB 7: ARTIFACTS MANAGEMENT
# ==============================================================================
with tab7:
    st.subheader("📦 Artifacts & Downloads")

    st.markdown(
        """
    <div class='info-box'>
        <strong>ℹ️ Artifacts Information:</strong><br>
        These are files generated by the pipeline (e.g., models, processed datasets, reports).
        You can download them for local analysis.
    </div>
    """,
        unsafe_allow_html=True,
    )

    artifacts = list_artifacts()

    if artifacts:
        # Create a display dataframe for cleaner UI
        art_data = []
        for art in artifacts:
            art_data.append(
                {
                    "Filename": art["name"],
                    "Size (KB)": f"{art['size']/1024:.2f}",
                    "Last Modified": art["modified"].strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        df_artifacts = pd.DataFrame(art_data)
        st.dataframe(df_artifacts, use_container_width=True)

        st.markdown("#### 📥 Download Artifacts")

        # Grid layout for download buttons
        cols = st.columns(3)
        for idx, art in enumerate(artifacts):
            with cols[idx % 3]:
                with open(art["path"], "rb") as f:
                    file_data = f.read()

                st.download_button(
                    label=f"⬇️ {art['name']}",
                    data=file_data,
                    file_name=art["name"],
                    mime="application/octet-stream",
                    key=f"dl_{idx}",
                    use_container_width=True,
                )
    else:
        st.info("📭 No artifacts found. Run the pipeline to generate outputs.")

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
