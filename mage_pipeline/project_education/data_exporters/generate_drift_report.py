if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import os


@data_exporter
def export_data(df: pd.DataFrame, *args, **kwargs):
    print("🚀 Memulai proses Data Drift...")

    # Setup Data (Reference vs Current)
    # Kita ambil 50% data awal sebagai referensi, sisanya sebagai data baru
    split_index = int(len(df) * 0.5)
    reference_data = df.iloc[:split_index]
    current_data = df.iloc[split_index:]

    # Setup Folder Artifacts
    # Menggunakan path absolut container Mage
    ARTIFACTS_DIR = "/home/src/artifacts"
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    report_path = os.path.join(ARTIFACTS_DIR, "data_drift_report.html")

    # Drop kolom ID agar tidak dihitung drift-nya
    # Menyesuaikan dengan kolom yang ada di DataFrame Anda
    columns_to_drop = (
        ["provinsi", "cluster"] if "cluster" in df.columns else ["provinsi"]
    )

    # Generate Report
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    # Jalankan report dengan error ignoring untuk kolom yang mungkin tidak ada
    report.run(
        reference_data=reference_data.drop(columns=columns_to_drop, errors="ignore"),
        current_data=current_data.drop(columns=columns_to_drop, errors="ignore"),
    )

    # Simpan
    report.save_html(report_path)

    print(f"✅ Laporan Data Drift berhasil dibuat di: {report_path}")

    return df
