from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# Setup Path Artefak (Shared Volume dengan FastAPI)
ARTIFACTS_ROOT_DIR = "/home/src/artifacts" 
os.makedirs(ARTIFACTS_ROOT_DIR, exist_ok=True)
SCALER_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "standard_scaler.pkl")

@transformer
def transform_standardize(df: pd.DataFrame, *args, **kwargs):
    # 1. Standarisasi nama kolom
    df.columns = df.columns.str.lower().str.strip()

    # 2. Pisahkan ID (Provinsi) agar tidak ikut di-scaling
    if "provinsi" not in df.columns:
        # Fallback: cari kolom yang mengandung kata "prov"
        possible_ids = [c for c in df.columns if "prov" in c]
        if possible_ids:
            df.rename(columns={possible_ids[0]: "provinsi"}, inplace=True)
        else:
            raise ValueError(f"Kolom 'provinsi' tidak ditemukan. Kolom ada: {df.columns.tolist()}")

    province_id = df["provinsi"]
    X = df.drop(columns=["provinsi"])

    # 3. Data Cleaning (Median Imputation untuk menangani NaN/Inf)
    numeric_cols = X.select_dtypes(include=['number']).columns
    X[numeric_cols] = X[numeric_cols].replace([float("inf"), float("-inf")], float("nan"))
    X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].median())

    # 4. Fit & Transform Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X[numeric_cols])

    # 5. Simpan Scaler untuk dipakai nanti di FastAPI (PENTING!)
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ StandardScaler disimpan di: {SCALER_PATH}")

    # 6. Gabungkan kembali untuk proses selanjutnya
    df_scaled = pd.DataFrame(X_scaled, columns=numeric_cols)
    df_scaled["provinsi"] = province_id.values

    return df_scaled

@test
def test_output(output, *args) -> None:
    assert output is not None, "Output undefined"
    assert "provinsi" in output.columns, "Kolom provinsi hilang setelah transform"