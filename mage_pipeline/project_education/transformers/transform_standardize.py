from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os
# --- WAJIB: Import decorator transformer ---
from mage_ai.data_preparation.decorators import transformer 

# Tentukan path untuk menyimpan artefak scaler (digunakan oleh FastAPI)
# Menggunakan path absolut yang di-mount Docker
ARTIFACTS_ROOT_DIR = '/home/src/mage_pipeline/artifacts'
os.makedirs(ARTIFACTS_ROOT_DIR, exist_ok=True)
SCALER_PATH = os.path.join(ARTIFACTS_ROOT_DIR, 'standard_scaler.pkl')

@transformer
def transform_standardize(df: pd.DataFrame, *args, **kwargs):
    # --- Pagar Pengaman: Memastikan input adalah Pandas DataFrame yang valid ---
    if not isinstance(df, pd.DataFrame):
        # Jika Mage.ai meneruskan data sebagai list of lists/tuples, kita konversi.
        cols = [
            'provinsi', 'persen_sekolah_internet_sd', 'persen_sekolah_internet_smp', 
            'persen_sekolah_internet_sma', 'persen_guru_sertifikasi_sd', 'persen_guru_sertifikasi_smp', 
            'persen_guru_sertifikasi_sma', 'rasio_siswa_guru_sd', 'rasio_siswa_guru_smp', 
            'rasio_siswa_guru_sma', 'rasio_siswa_komputer_sd', 'rasio_siswa_komputer_smp', 
            'rasio_siswa_komputer_sma', 'persen_lulus_akm_literasi', 'persen_lulus_akm_numerasi'
        ]
        try:
            # Menggunakan copy() untuk menghindari SettingWithCopyWarning
            df_copy = pd.DataFrame(df, columns=cols).copy() 
            df = df_copy
            print("INFO: Input berhasil dikonversi ke DataFrame secara eksplisit.")
        except Exception as e:
            raise TypeError(f"Gagal mengonversi input menjadi DataFrame. Detail: {e}")

    # 1. Pisahkan ID (Provinsi) dan Fitur Numerik
    if 'provinsi' not in df.columns:
        raise ValueError("Kolom 'provinsi' tidak ditemukan. Cek output Data Loader.")

    province_id = df['provinsi']
    # Drop kolom 'provinsi' karena itu adalah ID/string
    X = df.drop(columns=['provinsi']) 
    
    # 2. Pembersihan Data (Mengisi NaN/Inf dengan Median)
    X.replace([float('inf'), float('-inf')], float('nan'), inplace=True)
    X.fillna(X.median(), inplace=True)
    
    # 3. Inisialisasi StandardScaler dan Lakukan Standardisasi (Fit & Transform)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Konversi kembali ke DataFrame dan gabungkan ID
    df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    df_scaled['provinsi'] = province_id.values
    
    # 5. Simpan StandardScaler sebagai Artefak (untuk serving FastAPI)
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ StandardScaler berhasil disimpan di: {SCALER_PATH}")

    # Output dari blok ini adalah data yang sudah di-scale
    return df_scaled
    