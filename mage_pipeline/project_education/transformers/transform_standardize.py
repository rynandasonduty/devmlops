from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# Setup Path Artefak
ARTIFACTS_ROOT_DIR = "/home/src/artifacts"  # Simpan di folder artifacts yang ter-mount
os.makedirs(ARTIFACTS_ROOT_DIR, exist_ok=True)
SCALER_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "standard_scaler.pkl")


@transformer
def transform_standardize(df: pd.DataFrame, *args, **kwargs):
    # 1. Pastikan nama kolom huruf kecil semua biar aman
    df.columns = df.columns.str.lower()

    # 2. Pisahkan ID (Provinsi)
    if "provinsi" not in df.columns:
        raise ValueError("Kolom 'provinsi' tidak ditemukan. Cek output Data Loader.")

    province_id = df["provinsi"]
    X = df.drop(columns=["provinsi"])

    # 3. Pembersihan Data (Median Imputation)
    X.replace([float("inf"), float("-inf")], float("nan"), inplace=True)
    X.fillna(X.median(), inplace=True)

    # 4. Fit & Transform Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Simpan Scaler untuk dipakai nanti di FastAPI
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ StandardScaler disimpan di: {SCALER_PATH}")

    # 6. Gabungkan kembali
    df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    df_scaled["provinsi"] = province_id.values

    return df_scaled


@test
def test_output(output, *args) -> None:
    assert output is not None, "Output undefined"
    assert "provinsi" in output.columns, "Kolom provinsi hilang"
