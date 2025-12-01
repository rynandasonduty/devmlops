if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# --- BAGIAN INI MEMAKSA INSTALL DI DALAM BLOK ---
import subprocess
import sys
import importlib

# Cek apakah library sudah ada, jika belum, install paksa
packages = ['evidently', 'scikit-learn', 'pandas']
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"📦 Library '{package}' tidak ditemukan. Menginstall...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ '{package}' berhasil diinstall.")

# --- BARU IMPORT SETELAH PASTI TERINSTALL ---
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
    ARTIFACTS_DIR = '/home/src/artifacts'
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    report_path = os.path.join(ARTIFACTS_DIR, 'data_drift_report.html')
    
    # Drop kolom ID agar tidak dihitung drift-nya
    columns_to_drop = ['provinsi', 'cluster'] if 'cluster' in df.columns else ['provinsi']
    
    # Generate Report
    report = Report(metrics=[
        DataDriftPreset(), 
    ])
    
    report.run(
        reference_data=reference_data.drop(columns=columns_to_drop, errors='ignore'), 
        current_data=current_data.drop(columns=columns_to_drop, errors='ignore')
    )
    
    # Simpan
    report.save_html(report_path)
    
    print(f"✅ Laporan Data Drift berhasil dibuat di: {report_path}")
    
    return df