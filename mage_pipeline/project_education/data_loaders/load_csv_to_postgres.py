import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs):

    filepath = "/home/src/data_kesiapan_pendidikan_final.csv"

    if not path.exists(filepath):
        raise FileNotFoundError(
            f"File tidak ditemukan di {filepath} Pastikan file sudah dipindah ke folder"
        )

    df = pd.read_csv(filepath)
    print(f"✅ Berhasil load CSV. Shape: {df.shape}")
    print(f"Kolom: {df.columns.tolist()}")

    # 2. Export ke PostgreSQL
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"

    schema_name = "public"
    table_name = "education_data_final"

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,
            if_exists="replace",
        )

    print(f"✅ Data berhasil diexport ke tabel: {schema_name}.{table_name}")

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert len(output.index) >= 10, "Data terlalu sedikit, mungkin gagal load."
