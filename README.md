# 🎓 Education Readiness Clustering - End-to-End MLOps

[![Mage.ai](https://img.shields.io/badge/Orchestration-Mage.ai-blue)](https://mage.ai)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow-orange)](https://mlflow.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)](https://streamlit.io)
[![DVC](https://img.shields.io/badge/Data-DVC-purple)](https://dvc.org)
[![Docker](https://img.shields.io/badge/Infrastructure-Docker-blue)](https://docker.com)

## 📋 Overview
Sistem ini adalah implementasi **DevMLOps (Development + ML + Operations)** untuk melakukan analisis klastering kesiapan pendidikan provinsi di Indonesia. Proyek ini tidak hanya fokus pada pemodelan Machine Learning, tetapi juga pada pembangunan infrastruktur otomatis yang tangguh, *reproducible*, dan siap produksi.

### 🎯 Tujuan
* **Data Versioning:** Melacak perubahan dataset dinamis dari PostgreSQL menggunakan **DVC**.
* **Automated Pipeline:** Mengotomatisasi proses ETL dan Training model dengan **Mage.ai**.
* **Experiment Tracking:** Mencatat metrik performa model (Silhouette Score) dan artefak secara terpusat dengan **MLflow**.
* **Model Serving:** Menyediakan API prediksi real-time yang cepat dan standar menggunakan **FastAPI**.
* **Monitoring:** Memantau kesehatan sistem (Latency/Throughput) dengan **Prometheus & Grafana** serta kualitas data (Data Drift) menggunakan **Evidently AI**.

---

## 🏗️ Architecture Design
Sistem dibangun menggunakan pendekatan *Microservices* dengan empat pilar utama:

1.  **Data Plane:** PostgreSQL (Source of Truth) + DVC (Versioning).
2.  **Experimentation Plane:** Mage.ai (Orchestrator) + MLflow (Tracking).
3.  **Serving Plane:** FastAPI (Backend) + Streamlit (Frontend).
4.  **DevOps Plane:** GitHub Actions (CI/CD) + Prometheus & Grafana (Monitoring).

*(Diagram arsitektur dapat dilihat di dokumen laporan)*

---

## 🛠️ Tech Stack

| Kategori | Teknologi | Fungsi Utama |
| :--- | :--- | :--- |
| **Database** | **PostgreSQL 15** | Single Source of Truth penyimpanan data pendidikan. |
| **Orchestrator** | **Mage.ai** | Mengatur jadwal pipeline: Extract (SQL) -> Transform (Python) -> Train. |
| **ML Core** | **Scikit-Learn** | Library utama algoritma K-Means Clustering. |
| **Tracking** | **MLflow** | Manajemen eksperimen, pencatatan metrik, dan Model Registry. |
| **Versioning** | **DVC** | Pelacakan versi dataset besar (Snapshotting) yang terintegrasi dengan Git. |
| **Backend** | **FastAPI** | REST API asynchronous untuk melayani prediksi (`/predict`). |
| **Frontend** | **Streamlit** | Dashboard interaktif untuk visualisasi klaster bagi pengguna. |
| **Monitoring (Sys)** | **Prometheus + Grafana** | Monitoring kesehatan server, latency API, dan penggunaan resource. |
| **Monitoring (ML)** | **Evidently AI** | Deteksi otomatis Data Drift dan degradasi model. |
| **Quality** | **Ruff, Black, Prettier** | Standardisasi kode Python dan konfigurasi (Linting & Formatting). |
| **Infra** | **Docker** | Kontainerisasi seluruh layanan agar konsisten di semua environment. |

---

## 🚀 Getting Started

Ikuti langkah ini untuk menjalankan sistem secara lokal menggunakan Docker.

### Prerequisites
* Docker Desktop & Docker Compose
* Git
* Python 3.9+ (Optional, untuk dev tools lokal)

### Installation
1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username/skripsi-mlops-clustering.git](https://github.com/username/skripsi-mlops-clustering.git)
    cd skripsi-mlops-clustering
    ```

2.  **Setup Environment Variables**
    Buat file `.env` di root folder dan isi dengan kredensial database (pastikan sesuai dengan `docker-compose.yml`):
    ```env
    # Database Credentials
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=adminpassword123
    POSTGRES_DB=education_db

    # (Optional) AWS Credentials for DVC Remote
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_REGION=ap-southeast-1
    ```

3.  **Build & Run Services**
    Jalankan perintah sakti berikut untuk membangun dan menyalakan seluruh infrastruktur:
    ```bash
    docker-compose up -d --build
    ```
    *(Proses ini akan memakan waktu 5-15 menit untuk download image & install library)*

4.  **Access Applications**
    Setelah sukses berjalan, akses layanan di browser:
    * **Mage.ai (Pipeline):** [http://localhost:6789](http://localhost:6789)
    * **MLflow (Tracking):** [http://localhost:5000](http://localhost:5000)
    * **Streamlit (Dashboard):** [http://localhost:8501](http://localhost:8501)
    * **FastAPI (Swagger Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Grafana (Monitoring):** [http://localhost:3000](http://localhost:3000) (Login: admin/admin)
    * **Prometheus (Metrics):** [http://localhost:9090](http://localhost:9090)

---

## 🔄 Development Workflow (CI/CD)

Proyek ini menerapkan **Continuous Integration** menggunakan GitHub Actions untuk menjamin kualitas kode.

### Local Development
Sebelum melakukan commit, pastikan kode Anda bersih dan standar:

1.  **Linting (Mencari Bug):**
    ```bash
    ruff check .
    ```
2.  **Formatting (Merapikan Kode):**
    ```bash
    black .
    ```

### CI Pipeline
Setiap `git push` ke branch `main` akan memicu pipeline otomatis yang melakukan:
1.  Pengecekan kualitas kode (Linting).
2.  Unit Testing dengan `pytest`.
3.  Build test Docker image.

---

## 👨‍💻 Author
**A.R Agastya**
*Sistem Informasi - ITS*