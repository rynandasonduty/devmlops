import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager


# --- 1. Definisi Schema Input (14 Fitur) ---
class ProvinceFeatures(BaseModel):
    # Tidak perlu input 'Provinsi' (nama) karena tidak masuk ke model
    persen_sekolah_internet_sd: float
    persen_sekolah_internet_smp: float
    persen_sekolah_internet_sma: float
    persen_guru_sertifikasi_sd: float
    persen_guru_sertifikasi_smp: float
    persen_guru_sertifikasi_sma: float
    rasio_siswa_guru_sd: float
    rasio_siswa_guru_smp: float
    rasio_siswa_guru_sma: float
    rasio_siswa_komputer_sd: float
    rasio_siswa_komputer_smp: float
    rasio_siswa_komputer_sma: float
    persen_lulus_akm_literasi: float
    persen_lulus_akm_numerasi: float


# --- 2. Global Variables untuk Model ---
ml_models = {}


# --- 3. Lifespan (Load Model saat Startup) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model saat aplikasi mulai
    model_path = "/app/artifacts/kmeans_model.pkl"
    scaler_path = "/app/artifacts/standard_scaler.pkl"

    try:
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            ml_models["kmeans"] = joblib.load(model_path)
            ml_models["scaler"] = joblib.load(scaler_path)
            print(f"✅ Model loaded successfully from {model_path}")
        else:
            print(
                "⚠️ Warning: Model artifacts not found. Please run Mage pipeline first."
            )
    except Exception as e:
        print(f"❌ Error loading models: {e}")

    yield
    # (Code after yield runs on shutdown - clean up if needed)
    ml_models.clear()


app = FastAPI(title="Education Cluster API", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


# --- 4. Helper: Mapping Cluster ID ke Label ---
def get_cluster_label(cluster_id):
    # BERDASARKAN HASIL TRAINING ANDA (Interpreted from Cluster Centers):
    # Cluster 1 (Centroid Positif ~0.7) -> Kesiapan TINGGI
    # Cluster 0 (Centroid Negatif Infrastruktur ~-2.0) -> Kesiapan RENDAH
    # Cluster 2 (Centroid ~-0.5) -> Kesiapan SEDANG
    # (Anda bisa sesuaikan mapping ini nanti jika label tertukar di Frontend)
    mapping = {
        1: "Tinggi (High Readiness)",
        2: "Sedang (Medium Readiness)",
        0: "Rendah (Low Readiness)",
    }
    return mapping.get(cluster_id, "Unknown")


# --- 5. Endpoints ---
@app.get("/")
def read_root():
    model_status = "Loaded" if "kmeans" in ml_models else "Not Loaded"
    return {"status": "active", "model_status": model_status}


@app.post("/predict")
def predict_cluster(features: ProvinceFeatures):
    if "kmeans" not in ml_models or "scaler" not in ml_models:
        raise HTTPException(
            status_code=503, detail="Model belum siap. Jalankan pipeline training dulu."
        )

    try:
        # 1. Konversi Input ke DataFrame (sesuai urutan training)
        input_data = pd.DataFrame(
            [features.dict().values()], columns=features.dict().keys()
        )

        # 2. Standardisasi Data (pakai scaler yang sama dengan training)
        scaled_data = ml_models["scaler"].transform(input_data)

        # 3. Prediksi
        cluster_id = ml_models["kmeans"].predict(scaled_data)[0]
        label = get_cluster_label(cluster_id)

        return {
            "cluster_id": int(cluster_id),
            "label": label,
            "message": "Prediksi berhasil",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
