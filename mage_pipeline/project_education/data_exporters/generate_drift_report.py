import pandas as pd
import os
import json
import joblib

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# --- KONFIGURASI PATH ---
ARTIFACTS_DIR = "/home/src/artifacts"
REPORT_PATH = os.path.join(ARTIFACTS_DIR, "data_drift_report.html")
METRICS_PATH = os.path.join(ARTIFACTS_DIR, "data_drift_metrics.json")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "kmeans_model.pkl")

# --- KONFIGURASI PROMETHEUS ---
# Pastikan hostname 'pushgateway' sesuai dengan docker-compose service name
PUSHGATEWAY_URL = "pushgateway:9091" 

@data_exporter
def export_data(df: pd.DataFrame, *args, **kwargs):
    """
    Melakukan pengecekan Data Drift.
    Fitur:
    1. Evidently Report (HTML/JSON)
    2. Push Metrics ke Prometheus
    3. Conditional Logic: Stop pipeline jika tidak ada drift & model sudah ada.
    """
    
    print("🚀 Memulai Analisis Drift & Quality Check...")
    
    # 1. Split Data untuk Simulasi (Reference vs Current)
    # Di production, reference diambil dari training set sebelumnya.
    # Disini kita split 50:50 dari data yang masuk.
    mid_point = len(df) // 2
    
    # Drop kolom non-fitur untuk analisis drift
    cols_drop = [c for c in ["provinsi", "cluster_id", "cluster_label"] if c in df.columns]
    
    reference_data = df.iloc[:mid_point].drop(columns=cols_drop, errors='ignore')
    current_data = df.iloc[mid_point:].drop(columns=cols_drop, errors='ignore')

    # 2. Generate Evidently Report
    # Kita pakai DataDriftPreset dan DataQualityPreset agar lengkap
    report = Report(metrics=[
        DataDriftPreset(), 
        DataQualityPreset()
    ])
    
    report.run(reference_data=reference_data, current_data=current_data)
    
    # 3. Simpan Artifacts (HTML)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    report.save_html(REPORT_PATH)
    print(f"📄 Drift Report HTML saved to: {REPORT_PATH}")

    # 4. Ambil Metrik Drift (Parsing JSON)
    result_dict = report.as_dict()
    
    try:
        # Mengambil metric Dataset Drift (True/False) dan Share (%)
        # Lokasi key bisa berbeda tergantung versi evidently, ini versi umum:
        drift_metrics = result_dict["metrics"][0]["result"]
        drift_share = drift_metrics["drift_share"]
        dataset_drift = drift_metrics["dataset_drift"]
    except (KeyError, IndexError, TypeError):
        print("⚠️ Warning: Struktur JSON Evidently berbeda, default ke No Drift.")
        drift_share = 0.0
        dataset_drift = False

    print(f"📊 Drift Score: {drift_share:.4f}")
    print(f"⚠️ Drift Detected: {dataset_drift}")

    # Simpan JSON untuk Audit Trail
    audit_data = {
        "drift_detected": bool(dataset_drift),
        "drift_score": drift_share,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(audit_data, f)

    # 5. Push Metrics ke Prometheus (Monitoring)
    try:
        registry = CollectorRegistry()
        # Gauge untuk Drift Score (0.0 - 1.0)
        g_score = Gauge("evidently_data_drift_score", "Share of drifting features", registry=registry)
        g_score.set(drift_share)
        
        # Gauge untuk Status Drift (1 = Drift, 0 = No Drift)
        g_status = Gauge("evidently_data_drift_detected", "1 if drift detected, 0 otherwise", registry=registry)
        g_status.set(1 if dataset_drift else 0)

        push_to_gateway(PUSHGATEWAY_URL, job="mage_drift_check", registry=registry)
        print(f"✅ Metrics pushed to Prometheus: {PUSHGATEWAY_URL}")
    except Exception as e:
        print(f"⚠️ Failed to push metrics (Check Pushgateway connection): {e}")

    # 6. CONDITIONAL LOGIC (CT Trigger)
    
    # A. Cek Cold Start (Apakah model sudah ada?)
    if not os.path.exists(MODEL_PATH):
        print("⚡ COLD START: Model belum ada. Melanjutkan ke Training...")
        return df # Lanjut ke blok selanjutnya
    
    # B. Cek Drift
    if dataset_drift:
        print("🔄 DRIFT DETECTED: Data berubah signifikan. Melanjutkan ke Retraining...")
        return df # Lanjut ke blok selanjutnya
        
    # C. Jika Stabil & Model Ada -> STOP
    print("🛑 STABLE: Data stabil & model sudah ada. Pipeline berhenti disini (Hemat Resource).")
    
    # Kita raise Exception khusus agar Mage menandai blok ini "Failed" atau "Cancelled"
    # dan blok setelahnya (Training) TIDAK dijalankan.
    raise Exception("PIPELINE_STOPPED: No Retraining Needed")