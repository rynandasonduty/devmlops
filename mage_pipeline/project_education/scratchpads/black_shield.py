import sys
import evidently

print("Versi Python:", sys.version)
print("Lokasi Library Evidently:", evidently.__file__)
print("List Path:", sys.path)

try:
    from evidently.report import Report
    print("✅ SUKSES: Import Report berhasil!")
except ImportError as e:
    print(f"❌ GAGAL: {e}")