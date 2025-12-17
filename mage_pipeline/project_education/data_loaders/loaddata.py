if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import os


@data_loader
def load_data_from_file(*args, **kwargs):
    # DAFTAR KEMUNGKINAN LOKASI FILE
    possible_paths = [
        # 1. Lokasi Baru (Standar Dashboard Admin V2)
        "/home/src/data/raw/data_kesiapan_pendidikan_final.csv",
        # 2. Lokasi Lama (Root Folder Mage)
        "/home/src/data_kesiapan_pendidikan_final.csv",
        # 3. Lokasi Alternatif (Jika ada subfolder project)
        "/home/src/project_education/data/raw/data_kesiapan_pendidikan_final.csv",
    ]

    filepath = None

    # Cek satu per satu path yang ada
    for path in possible_paths:
        if os.path.exists(path):
            filepath = path
            print(f"✅ File ditemukan di: {filepath}")
            break

    if filepath is None:
        raise FileNotFoundError(
            "❌ File CSV tidak ditemukan di lokasi manapun:\n"
            + "\n".join(possible_paths)
            + "\n\nSOLUSI: Buka Admin Dashboard -> Upload File -> Klik 'Save CSV to Server'."
        )

    # Baca CSV
    df = pd.read_csv(filepath)

    # Standardisasi nama kolom (Lower case & underscore)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Validasi Kolom Kritis
    required_cols = ["provinsi"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Kolom wajib {required_cols} tidak ditemukan dalam CSV.")

    return df


@test
def test_output(output, *args):
    assert output is not None, "The output is undefined"
    assert len(output.columns) > 5, "Data seems corrupted, too few columns"
