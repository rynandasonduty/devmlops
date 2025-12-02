if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway  # Library baru
import pandas as pd
import os


@data_exporter
def export_data(df: pd.DataFrame, *args, **kwargs):
    print("🚀 Memulai Analisis Drift & Push Metrics...")

    # 1. Split Data
    split_index = int(len(df) * 0.5)
    reference_data = df.iloc[:split_index]
    current_data = df.iloc[split_index:]

    # 2. Generate Report
    cols_drop = [c for c in ["provinsi", "cluster"] if c in df.columns]
    report = Report(metrics=[DataDriftPreset()])
    report.run(
        reference_data=reference_data.drop(columns=cols_drop, errors="ignore"),
        current_data=current_data.drop(columns=cols_drop, errors="ignore"),
    )

    # 3. Simpan Artifacts
    ARTIFACTS_DIR = "/home/src/artifacts"
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    report.save_html(os.path.join(ARTIFACTS_DIR, "data_drift_report.html"))

    # 4. Ambil Nilai Drift
    result_dict = report.as_dict()
    drift_score = result_dict["metrics"][0]["result"]["drift_share"]
    drift_detected = result_dict["metrics"][0]["result"]["dataset_drift"]

    print(f"📊 Drift Score: {drift_score}")
    print(f"⚠️ Drift Detected: {drift_detected}")

    # ======================================================
    # BAGIAN BARU: Kirim ke Grafana (via Pushgateway)
    # ======================================================
    try:
        registry = CollectorRegistry()
        g = Gauge(
            "evidently_data_drift_score",
            "Data Drift Score form Evidently",
            registry=registry,
        )
        g.set(drift_score)  # Set nilai skor

        # Push ke container 'pushgateway' port 9091
        push_to_gateway("pushgateway:9091", job="mage_drift_check", registry=registry)
        print("✅ Metrics berhasil dikirim ke Prometheus Pushgateway")
    except Exception as e:
        print(f"❌ Gagal kirim metrics: {e}")

    # ======================================================
    # BAGIAN BARU: Conditional Trigger Logic
    # ======================================================
    # Jika TIDAK ada drift, kita stop pipeline di sini
    if not drift_detected:
        print("🛑 Data Stabil. Pipeline dihentikan (Tidak perlu Retraining).")
        # Melempar error 'aman' untuk menghentikan pipeline di block ini
        # Atau return False jika menggunakan Conditional Block Mage
        raise Exception("STOP_PIPELINE: No Drift Detected")

    print("✅ Drift Terdeteksi! Melanjutkan ke Training...")
    return df
