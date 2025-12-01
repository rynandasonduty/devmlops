import io
import pandas as pd
import requests
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Load data dari file CSV lokal (yang sudah dipindah ke folder mage_pipeline)
    dan export ke PostgreSQL.
    """
    
    # 1. Baca File CSV
    # Asumsi: File ada di root project mage (/home/src/)
    filepath = '/home/src/data_kesiapan_pendidikan_final.csv'
    
    if not path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan di {filepath}. Pastikan file sudah dipindah ke folder mage_pipeline.")

    df = pd.read_csv(filepath)
    print(f"✅ Berhasil load CSV. Shape: {df.shape}")
    print(f"Kolom: {df.columns.tolist()}")

    # 2. Export ke PostgreSQL
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    schema_name = 'public'
    table_name = 'education_data_final'  # Nama tabel di DB

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Jangan masukkan index pandas sebagai kolom
            if_exists='replace',  # 'replace' akan menghapus tabel lama jika ada dan buat baru
        )
    
    print(f"✅ Data berhasil diexport ke tabel: {schema_name}.{table_name}")
    
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert len(output.index) >= 10, 'Data terlalu sedikit, mungkin gagal load.'