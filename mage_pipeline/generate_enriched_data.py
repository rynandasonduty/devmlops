import pandas as pd
import numpy as np

# 1. Load Data Awal
try:
    df = pd.read_csv("data_kesiapan_pendidikan_final.csv")
    print("✅ Berhasil memuat data. Shape awal:", df.shape)
except FileNotFoundError:
    print("❌ File 'data_kesiapan_pendidikan_final.csv' tidak ditemukan.")
    exit()

# Setup Random Seed agar hasil konsisten
np.random.seed(42)

# --- A. GENERATE DATA LISTRIK (SD, SMP, SMA) ---
# Logika: Akses listrik biasanya >= Akses Internet.
# Kita ambil data internet, lalu tambahkan sedikit margin positif.
for jenjang in ["sd", "smp", "sma"]:
    col_internet = f"persen_sekolah_internet_{jenjang}"
    col_listrik = f"persen_sekolah_listrik_{jenjang}"

    # Base: Nilai Internet + Random (5-20%)
    # Mengasumsikan sekolah yg punya internet pasti punya listrik,
    # tapi yang punya listrik belum tentu punya internet.
    df[col_listrik] = df[col_internet] + np.random.uniform(5, 20, size=len(df))

    # Pastikan tidak lebih dari 100% dan tidak kurang dari nilai internet
    df[col_listrik] = df[[col_listrik]].clip(upper=100)
    df[col_listrik] = df[[col_listrik, col_internet]].max(axis=1)

# --- B. GENERATE DATA KUALIFIKASI S1/D4 (SD, SMP, SMA) ---
# Logika: Guru bersertifikasi biasanya sudah S1. Tapi banyak guru S1 yang BELUM sertifikasi.
# Jadi, Persen S1 >= Persen Sertifikasi.
for jenjang in ["sd", "smp", "sma"]:
    col_sertifikasi = f"persen_guru_sertifikasi_{jenjang}"
    col_s1 = f"persen_guru_kualifikasi_s1_{jenjang}"

    # Base: Nilai Sertifikasi + Random (10-40%)
    # Karena gap antara yang lulus S1 dan yang lulus PPG (Sertifikasi) biasanya lumayan besar.
    df[col_s1] = df[col_sertifikasi] + np.random.uniform(10, 40, size=len(df))

    # Pastikan tidak lebih dari 100%
    df[col_s1] = df[col_s1].clip(upper=100)

# --- C. FINALISASI & SIMPAN ---
output_filename = "data_kesiapan_pendidikan_enriched.csv"
df.to_csv(output_filename, index=False)

print("\nSample 5 baris data baru (Listrik & S1):")
print(
    df[
        ["Provinsi", "persen_sekolah_listrik_sd", "persen_guru_kualifikasi_s1_sd"]
    ].head()
)
print(f"\n✅ File '{output_filename}' berhasil dibuat dengan {df.shape[1]} kolom.")
