import mlflow
import mlflow.sklearn
import pandas as pd
import joblib
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Setup Path
ARTIFACTS_ROOT_DIR = '/home/src/artifacts'
MODEL_PATH = os.path.join(ARTIFACTS_ROOT_DIR, 'kmeans_model.pkl')

@data_exporter
def train_and_log_model(df: pd.DataFrame, *args, **kwargs):
    # Setup MLflow Tracking URI (sesuai docker-compose)
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("project_education_clustering")
    
    # Pisahkan fitur untuk training (drop provinsi)
    X = df.drop(columns=['provinsi'])
    
    # Parameter Model
    n_clusters = 3
    random_state = 42
    
    with mlflow.start_run():
        print("🚀 Memulai Training K-Means...")
        
        # 1. Train Model
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        kmeans.fit(X)
        
        # 2. Hitung Metrik Evaluasi
        labels = kmeans.labels_
        inertia = kmeans.inertia_
        silhouette = silhouette_score(X, labels)
        
        print(f"Cluster Centers:\n{kmeans.cluster_centers_}")
        print(f"Inertia: {inertia}")
        print(f"Silhouette Score: {silhouette}")
        
        # 3. Log ke MLflow
        mlflow.log_param("n_clusters", n_clusters)
        mlflow.log_metric("inertia", inertia)
        mlflow.log_metric("silhouette_score", silhouette)
        
        # Log model ke MLflow Registry
        mlflow.sklearn.log_model(kmeans, "kmeans_model")
        
        # 4. Simpan Model Lokal (untuk dimuat FastAPI nanti)
        joblib.dump(kmeans, MODEL_PATH)
        print(f"✅ Model disimpan lokal di: {MODEL_PATH}")
        
        # 5. (Opsional) Tambahkan hasil cluster ke DataFrame untuk debug
        df['cluster'] = labels
        
    return df