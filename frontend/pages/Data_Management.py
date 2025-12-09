import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="Data Management", page_icon="⚙️")

st.title("⚙️ Manajemen Data & Operasional MLOps")

# --- KONFIGURASI MAGE AI ---
MAGE_HOST = "http://mage:6789"

# ID & TOKEN (Sesuai informasi dari UI Mage Anda)
TRIGGER_SCHEDULE_ID = 2
TRIGGER_TOKEN = "189557234d5e431a972f6d0926b719e9"  # Token Anda

# Path Data
TARGET_DIR = "/app/mage_data_source"
TARGET_FILE = os.path.join(TARGET_DIR, "data_kesiapan_pendidikan_final.csv")

# --- 1. DATA UPLOAD SECTION ---
st.subheader("1. 📥 Update Dataset")
uploaded_file = st.file_uploader("Upload file CSV", type="csv")

if uploaded_file is not None:
    df_new = pd.read_csv(uploaded_file)
    st.dataframe(df_new.head(3))
    if st.button("💾 Simpan ke Warehouse"):
        try:
            os.makedirs(TARGET_DIR, exist_ok=True)
            df_new.to_csv(TARGET_FILE, index=False)
            st.success("✅ Data berhasil disimpan! Siap untuk training ulang.")
        except Exception as e:
            st.error(f"Gagal menyimpan: {e}")

st.divider()

# --- 2. PIPELINE CONTROL ---
st.subheader("2. 🚀 Orchestration Control")

col1, col2 = st.columns([1, 2])
with col1:
    st.write("**Status Pipeline:**")
    try:
        res = requests.get(f"{MAGE_HOST}/api/statuses")
        if res.status_code == 200:
            st.success("🟢 Mage Engine Online")
        else:
            st.warning("🔴 Mage Engine Unreachable")
    # skip-check-connection-errors
    except:  # noqa: E722
        st.error("🔴 Connection Failed")

with col2:
    trigger_btn = st.button("▶️ Trigger Retraining Pipeline", type="primary")

if trigger_btn:
    with st.status("Menjalankan MLOps Pipeline...", expanded=True) as status:
        st.write("📡 Menghubungi Mage API...")

        # --- PERBAIKAN UTAMA DISINI ---

        # 1. Endpoint: Menggunakan 'api_trigger', bukan 'pipeline_runs' biasa
        api_url = (
            f"{MAGE_HOST}/api/pipeline_schedules/{TRIGGER_SCHEDULE_ID}/api_trigger"
        )

        # 2. Headers: Token harus masuk sini sebagai 'Bearer'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TRIGGER_TOKEN}",
        }

        # 3. Payload: Token TIDAK BOLEH ada di sini lagi
        payload = {
            "pipeline_run": {
                "variables": {
                    "triggered_by": "streamlit_dashboard"  # Opsional, untuk log
                }
            }
        }

        try:
            # Kirim Request
            res = requests.post(api_url, headers=headers, json=payload)

            if res.status_code == 200:
                st.write("✅ Request Accepted!")
                st.json(res.json())
                status.update(label="Pipeline Berhasil Dijalankan!", state="complete")
                st.balloons()
            else:
                st.error(f"❌ Gagal ({res.status_code}): {res.text}")
                status.update(label="Gagal Eksekusi", state="error")

        except Exception as e:
            st.error(f"Connection Error: {e}")
            status.update(label="Error Koneksi", state="error")

st.info(
    "Catatan: Training membutuhkan waktu 1-3 menit. Refresh halaman Dashboard Publik setelah selesai."
)
