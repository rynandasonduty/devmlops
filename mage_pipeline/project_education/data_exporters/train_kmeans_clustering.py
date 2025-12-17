import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib
import json
import os
import optuna
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# --- KONFIGURASI PATH ---
ARTIFACTS_ROOT_DIR = "/home/src/artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "kmeans_model.pkl")
METADATA_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "cluster_metadata.json")


# --- FUNGSI OPTIMASI ---
def objective(trial, X):
    """Optuna objective function untuk mencari k optimal"""
    n_clusters = trial.suggest_int("n_clusters", 2, 6)  # Extended range

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Silhouette score (higher is better)
    sil_score = silhouette_score(X, labels)

    # Davies-Bouldin score (lower is better, we negate for maximization)
    db_score = davies_bouldin_score(X, labels)

    # Combined metric: prioritize silhouette but penalize high DB score
    combined_score = sil_score - (0.3 * db_score)

    return combined_score


@data_exporter
def train_and_log_model(df: pd.DataFrame, *args, **kwargs):
    """
    Training KMeans dengan hyperparameter tuning & dynamic cluster labeling
    """
    # 1. Setup MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("project_education_clustering")

    # 2. Persiapan Data (Drop ID Provinsi)
    province_col = None
    if "provinsi" in df.columns:
        province_col = df["provinsi"].copy()  # FIX: Proper assignment
        X = df.drop(columns=["provinsi"])
    else:
        # Fallback jika tidak ada kolom provinsi
        X = df.select_dtypes(include=[np.number])
        province_col = pd.Series(
            index=df.index, data=[f"Province_{i}" for i in range(len(df))]
        )

    print(f"🚀 Memulai Hyperparameter Tuning dengan Optuna (Data shape: {X.shape})...")

    # 3. Jalankan Optuna untuk mencari k terbaik
    study = optuna.create_study(direction="maximize")
    study.optimize(
        lambda trial: objective(trial, X), n_trials=15, show_progress_bar=True
    )

    best_k = study.best_params["n_clusters"]
    best_score = study.best_value
    print(f"✅ Best Params: k={best_k} | Best Combined Score: {best_score:.4f}")

    # 4. Training Ulang dengan Parameter Terbaik (Final Model)
    with mlflow.start_run(run_name=f"KMeans_k{best_k}_Final"):
        kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        kmeans_final.fit(X)
        labels = kmeans_final.labels_

        # Calculate all metrics
        sil_score = silhouette_score(X, labels)
        db_score = davies_bouldin_score(X, labels)

        # Log Metrics & Params
        mlflow.log_param("n_clusters", best_k)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("silhouette_score", sil_score)
        mlflow.log_metric("davies_bouldin_score", db_score)
        mlflow.log_metric("inertia", kmeans_final.inertia_)
        mlflow.log_metric("combined_score", best_score)

        # Log Model ke Registry
        mlflow.sklearn.log_model(
            kmeans_final,
            "kmeans_education_model",
            registered_model_name="education_clustering_model",
        )

        # --- 5. LOGIKA PENAMAAN CLUSTER DINAMIS (Anti-Label Switching) ---
        cluster_centers = kmeans_final.cluster_centers_

        # Hitung skor rata-rata tiap centroid (composite score)
        centroid_scores = cluster_centers.mean(axis=1)

        # Buat mapping: Index Cluster -> Rank (0 terendah, dst)
        sorted_indices = np.argsort(centroid_scores)

        # Dynamic labeling based on k
        if best_k == 2:
            label_names = ["Rendah (Low)", "Tinggi (High)"]
        elif best_k == 3:
            label_names = ["Rendah (Low)", "Sedang (Medium)", "Tinggi (High)"]
        elif best_k == 4:
            label_names = [
                "Sangat Rendah",
                "Rendah (Low)",
                "Sedang (Medium)",
                "Tinggi (High)",
            ]
        else:
            label_names = [f"Cluster {i+1}" for i in range(best_k)]

        cluster_mapping = {}
        for rank, original_id in enumerate(sorted_indices):
            cluster_mapping[int(original_id)] = label_names[rank]

        print("🏷️ Cluster Interpretation (Mapping):", cluster_mapping)

        # Calculate cluster statistics for metadata
        cluster_stats = {}
        for cluster_id in range(best_k):
            cluster_mask = labels == cluster_id
            cluster_stats[int(cluster_id)] = {
                "label": cluster_mapping[int(cluster_id)],
                "count": int(cluster_mask.sum()),
                "percentage": float(cluster_mask.sum() / len(labels) * 100),
                "centroid": cluster_centers[cluster_id].tolist(),
                "avg_score": float(centroid_scores[cluster_id]),
            }

        # 6. Simpan Artifacts Fisik (Model & Metadata)
        os.makedirs(ARTIFACTS_ROOT_DIR, exist_ok=True)
        joblib.dump(kmeans_final, MODEL_PATH)

        # Enhanced metadata dengan statistics
        metadata = {
            "n_clusters": best_k,
            "silhouette_score": float(sil_score),
            "davies_bouldin_score": float(db_score),
            "inertia": float(kmeans_final.inertia_),
            "cluster_mapping": cluster_mapping,
            "cluster_statistics": cluster_stats,
            "feature_names": X.columns.tolist(),
            "timestamp": pd.Timestamp.now().isoformat(),
        }

        with open(METADATA_PATH, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Model disimpan: {MODEL_PATH}")
        print(f"✅ Metadata disimpan: {METADATA_PATH}")

    # 7. Prepare output dataframe dengan hasil prediksi
    df_result = df.copy()
    if province_col is not None:
        df_result["provinsi"] = province_col

    df_result["cluster_id"] = labels
    df_result["cluster_label"] = df_result["cluster_id"].map(cluster_mapping)

    # 8. Hitung Cluster Profile (rata-rata per cluster)
    df_profile = X.copy()
    df_profile["cluster_id"] = labels
    df_profile["cluster_label"] = df_profile["cluster_id"].map(cluster_mapping)

    # Group by cluster label dan hitung mean
    cluster_profile = (
        df_profile.groupby("cluster_label").mean().drop(columns=["cluster_id"])
    )

    # Tambahkan count
    cluster_profile["province_count"] = df_profile.groupby("cluster_label").size()

    # Simpan profile ke CSV
    PROFILE_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "cluster_profile.csv")
    cluster_profile.to_csv(PROFILE_PATH)
    print(f"✅ Cluster Profile disimpan: {PROFILE_PATH}")

    # 9. Simpan labeled data
    LABELED_DATA_PATH = os.path.join(ARTIFACTS_ROOT_DIR, "data_labeled.csv")
    df_result.to_csv(LABELED_DATA_PATH, index=False)
    print(f"✅ Labeled Data disimpan: {LABELED_DATA_PATH}")

    print("\n" + "=" * 60)
    print("📊 CLUSTER SUMMARY:")
    print("=" * 60)
    for cid, stats in cluster_stats.items():
        print(
            f"{stats['label']}: {stats['count']} provinces ({stats['percentage']:.1f}%)"
        )
    print("=" * 60 + "\n")

    return df_result
