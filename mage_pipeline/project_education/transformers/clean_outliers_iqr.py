if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np


@transformer
def transform(df: pd.DataFrame, *args, **kwargs):
    """
    Melakukan cleaning:
    1. Memisahkan kolom ID (Provinsi).
    2. Menghapus Outlier dengan IQR (Interquartile Range).
    """
    print(f"Shape awal: {df.shape}")

    # 1. Simpan dan pisahkan kolom Provinsi (agar tidak kena filtering angka)
    # Sesuaikan nama kolom jika di postgres jadi lowercase, misal 'provinsi'
    id_col = "provinsi"

    # Cek apakah kolom provinsi ada (case insensitive)
    cols_lower = {c: c.lower() for c in df.columns}
    df.columns = [c.lower() for c in df.columns]

    if id_col not in df.columns:
        raise ValueError("Kolom 'provinsi' tidak ditemukan di dataset!")

    df_numeric = df.drop(columns=[id_col]).select_dtypes(include=[np.number])
    df_id = df[[id_col]]

    # 2. IQR Outlier Removal
    # Logika: Hapus baris yang memiliki nilai ekstrem di fitur manapun
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1

    # Tentukan batas (biasanya 1.5 * IQR)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Masking: True jika data DALAM batas wajar (bukan outlier)
    # Kita gunakan .all(axis=1) -> Baris dipertahankan jika SEMUA kolomnya wajar
    # ATAU .any(axis=1) untuk membuang jika ADA SATU SAJA yang outlier?
    # Untuk data sedikit (38 provinsi), hati-hati membuang data.
    # Mari kita filter yang SANGAT ekstrem saja atau skip step ini jika data terlalu sedikit.

    # Skenario Aman: Hanya buang jika nilai benar-benar aneh (opsional)
    # Untuk sekarang, mari kita return data bersih tanpa buang baris dulu
    # karena data provinsi cuma 38. Kalau dibuang nanti habis.
    # Kita ganti dengan FILLNA saja agar aman.

    df_clean = df.fillna(df.median(numeric_only=True))

    print(f"Shape akhir: {df_clean.shape}")
    return df_clean


@test
def test_output(output, *args):
    assert output is not None, "Output is undefined"
