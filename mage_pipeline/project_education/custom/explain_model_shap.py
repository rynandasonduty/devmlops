import shap
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
import numpy as np

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom

# Path
ARTIFACTS_DIR = "/home/src/artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "kmeans_model.pkl")


@custom
def transform(df_result: pd.DataFrame, *args, **kwargs):
    """
    Menghasilkan SHAP Summary Plot untuk interpretasi model.
    """
    # 1. Load Model yang baru dilatih
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model belum ada. Jalankan blok training dulu.")

    model = joblib.load(MODEL_PATH)

    # 2. Siapkan Data (Hapus kolom non-fitur yang mungkin ada dari step sebelumnya)
    # Kita perlu data yang SAMA PERSIS formatnya dengan saat training
    # Biasanya 'cluster_id' dan 'cluster_label' dan 'provinsi' harus dibuang
    X = df_result.select_dtypes(include=[np.number])
    if "cluster_id" in X.columns:
        X = X.drop(columns=["cluster_id"])

    # 3. Hitung SHAP Values
    # KernelExplainer adalah metode agnostik (bisa untuk KMeans)
    # Kita pakai sample kecil (kmeans.cluster_centers_) sebagai background data agar cepat
    print("🔍 Calculating SHAP values...")
    explainer = shap.KernelExplainer(model.predict, X)

    # Hitung SHAP untuk seluruh data (ini bisa agak lama jika data besar, tapi data Anda kecil jadi aman)
    shap_values = explainer.shap_values(X)

    # 4. Generate & Save Plot
    print("📊 Generating SHAP Summary Plot...")
    plt.figure(figsize=(10, 6))

    # Summary plot tipe 'bar' lebih mudah dibaca untuk clustering multi-class
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)

    shap_path = os.path.join(ARTIFACTS_DIR, "shap_summary.png")
    plt.savefig(shap_path, bbox_inches="tight")
    plt.close()

    print(f"✅ SHAP Plot saved to: {shap_path}")

    return df_result
