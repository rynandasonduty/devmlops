if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import os
import json

@data_exporter
def export_data(df: pd.DataFrame, *args, **kwargs):
    print("🚀 Memulai proses Data Drift Intelligence...")
    
    # 1. Setup Data (50:50 Split simulasi Reference vs Current)
    # Dalam production nanti, reference_data diambil dari training set lama
    split_index = int(len(df) * 0.5)
    reference_data = df.iloc[:split_index]
    current_data = df.iloc[split_index:]
    
    # 2. Setup Folder Artifacts
    ARTIFACTS_DIR = '/home/src/artifacts'
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    report_html_path = os.path.join(ARTIFACTS_DIR, 'data_drift_report.html')
    report_json_path = os.path.join(ARTIFACTS_DIR, 'data_drift_report.json')
    
    # 3. Kolom yang diabaikan (Non-Fitur)
    cols_drop = [c for c in ['provinsi', 'cluster'] if c in df.columns]
    
    # 4. Generate Report
    report = Report(metrics=[DataDriftPreset()])
    report.run(
        reference_data=reference_data.drop(columns=cols_drop, errors='ignore'), 
        current_data=current_data.drop(columns=cols_drop, errors='ignore')
    )
    
    # 5. Simpan Hasil (HTML untuk Manusia, JSON untuk Mesin)
    report.save_html(report_html_path)
    
    # Ekstrak hasil ke Dictionary Python
    result_dict = report.as_dict()
    
    # Simpan JSON
    with open(report_json_path, 'w') as f:
        json.dump(result_dict, f, indent=4)
        
    print(f"✅ Report HTML saved to: {report_html_path}")
    print(f"✅ Report JSON saved to: {report_json_path}")

    # 6. Analisa Hasil Drift (Logika Trigger)
    # Evidently JSON structure: metrics -> result -> dataset_drift (bool)
    # Kita cari metric DataDriftPreset (biasanya index 0)
    drift_share = result_dict['metrics'][0]['result']['drift_share']
    dataset_drift = result_dict['metrics'][0]['result']['dataset_drift']
    
    print(f"📊 Drift Share: {drift_share*100:.2f}%")
    print(f"⚠️ Drift Detected: {dataset_drift}")
    
    # Kembalikan Metadata ini agar bisa dipakai block selanjutnya (misal: Conditional Block)
    return {
        'drift_detected': dataset_drift,
        'drift_score': drift_share,
        'report_path': report_json_path
    }