import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib
import json
import os
import optuna
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# --- KONFIGURASI PATH ---
ARTIFACTS_ROOT_DIR = "/home/src/artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "kmeans_model.pkl")
METADATA_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "cluster_metadata.json")


# --- FUNGSI OPTIMASI ---
def objective(trial, X):
    # Search Space: Kita cari k antara 3 sampai 5
    n_clusters = trial.suggest_int("n_clusters", 3, 5)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    score = silhouette_score(X, labels)
    return score


@data_exporter
def train_and_log_model(df: pd.DataFrame, *args, **kwargs):
    # 1. Setup MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("project_education_clustering")

    # 2. Persiapan Data (Drop ID Provinsi)
    if "provinsi" in df.columns:
        df["provinsi"]
        X = df.drop(columns=["provinsi"])
    else:
        # Fallback jika tidak ada kolom provinsi
        X = df.select_dtypes(include=[np.number])
        pd.Series(index=df.index, data=["Unknown"] * len(df))

    print(f"🚀 Memulai Hyperparameter Tuning dengan Optuna (Data shape: {X.shape})...")

    # 3. Jalankan Optuna untuk mencari k terbaik
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, X), n_trials=10)

    best_k = study.best_params["n_clusters"]
    best_score = study.best_value
    print(f"✅ Best Params: k={best_k} | Best Silhouette: {best_score:.4f}")

    # 4. Training Ulang dengan Parameter Terbaik (Final Model)
    with mlflow.start_run(run_name="Best_KMeans_Model"):
        kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        kmeans_final.fit(X)
        labels = kmeans_final.labels_

        # Log Metrics & Params
        mlflow.log_param("n_clusters", best_k)
        mlflow.log_metric("silhouette_score", best_score)
        mlflow.log_metric("inertia", kmeans_final.inertia_)

        # Log Model ke Registry
        mlflow.sklearn.log_model(kmeans_final, "kmeans_education_model")

        # --- 5. LOGIKA PENAMAAN CLUSTER DINAMIS (Anti-Label Switching) ---
        cluster_centers = kmeans_final.cluster_centers_
        # Hitung skor rata-rata tiap centroid
        centroid_scores = cluster_centers.mean(axis=1)

        # Buat mapping: Index Cluster -> Rank (0 terendah, dst)
        sorted_indices = np.argsort(centroid_scores)

        label_names = ["Rendah (Low)", "Sedang (Medium)", "Tinggi (High)"]
        if best_k > 3:
            label_names = [f"Level {i+1}" for i in range(best_k)]

        cluster_mapping = {}
        for rank, original_id in enumerate(sorted_indices):
            cluster_mapping[int(original_id)] = label_names[rank]

        print("🏷️ Cluster Interpretation (Mapping):", cluster_mapping)

        # 6. Simpan Artifacts Fisik (Model & Metadata)
        # FIX: Menggunakan variabel yang benar ARTIFACTS_ROOT_DIR
        os.makedirs(ARTIFACTS_ROOT_DIR, exist_ok=True)
        joblib.dump(kmeans_final, MODEL_PATH)

        with open(METADATA_PATH, "w") as f:
            json.dump(cluster_mapping, f)

        print(f"✅ Model disimpan: {MODEL_PATH}")
        print(f"✅ Metadata disimpan: {METADATA_PATH}")

    # Kembalikan dataframe dengan hasil prediksi
    df_result = df.copy()
    df_result["cluster_id"] = labels
    df_result["cluster_label"] = df_result["cluster_id"].map(cluster_mapping)

    # Menggabungkan fitur dengan label untuk dihitung rata-ratanya
    df_profile = X.copy()
    df_profile["cluster_label"] = labels
    df_profile["cluster_label"] = df_profile["cluster_label"].map(cluster_mapping)

    # Hitung rata-rata per cluster
    cluster_stats = df_profile.groupby("cluster_label").mean()

    # Simpan ke CSV
    PROFILE_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "cluster_profile.csv")
    cluster_stats.to_csv(PROFILE_PATH)
    print(f"✅ Cluster Profile disimpan: {PROFILE_PATH}")

    return df_result
