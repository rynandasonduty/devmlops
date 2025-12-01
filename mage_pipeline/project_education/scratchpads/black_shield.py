import sys
import subprocess
import os

print("🔄 Mereset environment ke versi Stabil Terbaru...")

# 1. Install ulang Evidently versi terbaru & Pydantic yang kompatibel
# Kita gunakan flag --upgrade --force-reinstall untuk menimpa file yang korup
pkgs = [
    "evidently>=0.7.0",  # Versi modern
    "pydantic>=2.0.0",   # Kembalikan Pydantic V2 (standar Mage baru)
    "scikit-learn",
    "pandas"
]

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + pkgs + ["--upgrade", "--force-reinstall"])
    print("✅ Instalasi Paket Selesai!")
except Exception as e:
    print(f"❌ Gagal Install: {e}")

# 2. Cek Import (Harusnya aman sekarang)
try:
    import evidently
    from evidently.report import Report
    print(f"🎉 SUKSES! Evidently v{evidently.__version__} terinstall dengan benar.")
except ImportError as e:
    print(f"⚠️ Masih error import: {e}")