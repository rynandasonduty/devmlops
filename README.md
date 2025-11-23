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
* **Data Versioning:** Melacak perubahan dataset dinamis dari PostgreSQL.
* **Automated Pipeline:** Mengotomatisasi proses ETL dan Training model.
* **Experiment Tracking:** Mencatat metrik performa model (Silhouette Score) secara terpusat.
* **Model Serving:** Menyediakan API prediksi real-time yang dapat diakses publik.
* **Monitoring:** Memantau kesehatan sistem (Latency) dan kualitas data (Data Drift).

---

## 🏗️ Architecture Design
Sistem dibangun menggunakan pendekatan *Microservices* dengan empat pilar utama:

1.  **Data Plane:** PostgreSQL (Source) + DVC (Versioning).
2.  **Experimentation Plane:** Mage.ai (Orchestrator) + MLflow (Tracking).
3.  **Serving Plane:** FastAPI (Backend) + Streamlit (Frontend).
4.  **DevOps Plane:** GitHub Actions (CI/CD) + Prometheus & Grafana (Monitoring).

*(Diagram arsitektur dapat dilihat di dokumen laporan)*

---

## 🛠️ Tech Stack

| Komponen | Teknologi | Fungsi Utama |
| :--- | :--- | :--- |
| **Database** | PostgreSQL 15 | Single Source of Truth data pendidikan. |
| **Orchestrator** | Mage.ai | Mengatur jadwal pipeline ETL & Training. |
| **ML Core** | Scikit-Learn | Algoritma K-Means Clustering. |
| **Tracking** | MLflow | Manajemen eksperimen & Model Registry. |
| **Versioning** | DVC | Pelacakan versi dataset (Snapshot). |
| **Backend** | FastAPI | REST API untuk melayani prediksi (`/predict`). |
| **Frontend** | Streamlit | Dashboard interaktif untuk pengguna. |
| **Monitoring** | Prometheus + Grafana | Monitoring kesehatan server & API. |
| **Quality** | Ruff, Black, Prettier | Standarisasi kode Python & Config. |

---

## 🚀 Getting Started

Ikuti langkah ini untuk menjalankan sistem secara lokal menggunakan Docker.

### Prerequisites
* Docker & Docker Compose
* Git

### Installation
1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username/skripsi-mlops-clustering.git](https://github.com/username/skripsi-mlops-clustering.git)
    cd skripsi-mlops-clustering
    ```

2.  **Setup Environment Variables**
    Salin contoh konfigurasi env (jika ada) atau pastikan file `.env` telah dibuat dengan kredensial database:
    ```bash
    # Contoh isi .env
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=adminpassword123
    POSTGRES_DB=education_db
    ```

3.  **Build & Run Services**
    Jalankan perintah sakti berikut untuk menyalakan seluruh infrastruktur:
    ```bash
    docker-compose up -d --build
    ```
    *(Proses ini akan memakan waktu 5-10 menit untuk download image & install library)*

4.  **Access Applications**
    Setelah sukses berjalan, akses layanan di browser:
    * **Mage.ai (Pipeline):** [http://localhost:6789](http://localhost:6789)
    * **MLflow (Tracking):** [http://localhost:5000](http://localhost:5000)
    * **Streamlit (Dashboard):** [http://localhost:8501](http://localhost:8501)
    * **FastAPI (Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Grafana (Monitoring):** [http://localhost:3000](http://localhost:3000)

---

## 🔄 Development Workflow (CI/CD)

Proyek ini menerapkan **Continuous Integration** menggunakan GitHub Actions.
* Setiap `git push` akan memicu pengecekan kualitas kode (**Ruff**) dan formatting (**Black**).
* Pastikan kode Anda lolos pengecekan sebelum merge ke branch `main`.

```bash
# Cara manual cek kualitas kode di lokal
ruff check .
black .