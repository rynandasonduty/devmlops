import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# Path penyimpanan Artifacts (Visualisasi akan disimpan di sini)
ARTIFACTS_DIR = "/home/src/artifacts"


@custom
def transform(df_scaled: pd.DataFrame, *args, **kwargs):
    """
    Melakukan analisis mendalam:
    1. Elbow Method (Mencari k optimal)
    2. Silhouette Score Analysis
    3. PCA Visualization (Reduksi dimensi ke 2D untuk plotting)
    Output: Menyimpan file .png ke folder artifacts
    """
    # Pisahkan kolom provinsi jika ada, karena kita hanya butuh fitur numerik untuk visualisasi
    if "provinsi" in df_scaled.columns:
        X = df_scaled.drop(columns=["provinsi"])
    else:
        X = df_scaled

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # --- 1. ELBOW METHOD & SILHOUETTE SCORE (Iterasi k=2 sampai 10) ---
    print("🔍 Menjalankan Analisis Elbow & Silhouette...")
    inertias = []
    silhouettes = []
    K_range = range(2, 10)

    for k in K_range:
        # Kita train model sementara untuk setiap k
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        silhouettes.append(silhouette_score(X, kmeans.labels_))

    # Plot Elbow Method
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, "bo-", linewidth=2, markersize=8)
    plt.xlabel("Jumlah Cluster (k)")
    plt.ylabel("Inertia (WCSS)")
    plt.title("Elbow Method untuk Menentukan k Optimal")
    plt.grid(True)
    elbow_path = os.path.join(ARTIFACTS_DIR, "elbow_method.png")
    plt.savefig(elbow_path)
    plt.close()
    print(f"✅ Grafik Elbow disimpan: {elbow_path}")

    # Plot Silhouette Score
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, silhouettes, "go-", linewidth=2, markersize=8)
    plt.xlabel("Jumlah Cluster (k)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score Analysis (Higher is Better)")
    plt.grid(True)
    sil_path = os.path.join(ARTIFACTS_DIR, "silhouette_score.png")
    plt.savefig(sil_path)
    plt.close()
    print(f"✅ Grafik Silhouette disimpan: {sil_path}")

    # --- 2. PCA VISUALIZATION (2D Projection) ---
    # Kita visualisasikan dengan asumsi k=3 (atau sesuai model default kita)
    print("🔍 Membuat Visualisasi PCA 2D...")
    k_target = 3
    kmeans_final = KMeans(n_clusters=k_target, random_state=42, n_init=10)
    labels = kmeans_final.fit_predict(X)

    # Reduksi ke 2 Dimensi menggunakan PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)

    # Buat DataFrame sementara untuk plotting
    df_pca = pd.DataFrame(data=components, columns=["PC1", "PC2"])
    df_pca["Cluster"] = labels

    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        x="PC1",
        y="PC2",
        hue="Cluster",
        data=df_pca,
        palette="viridis",
        s=100,
        alpha=0.7,
    )
    plt.title(f"Visualisasi Cluster Pendidikan (PCA 2D Projection) - k={k_target}")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(title="Cluster")

    pca_path = os.path.join(ARTIFACTS_DIR, "pca_clusters.png")
    plt.savefig(pca_path)
    plt.close()
    print(f"✅ Grafik PCA disimpan: {pca_path}")

    # Return dataframe apa adanya agar pipeline tidak putus (walaupun ini cabang akhir)
    return df_scaled


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
