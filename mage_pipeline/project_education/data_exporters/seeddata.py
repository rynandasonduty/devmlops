if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
import os

@data_exporter
def export_data_to_postgres(df, **kwargs):
    """
    Exports data to a Postgres database table.
    """
    table_name = 'education_features'
    schema_name = 'public'  # Specify the name of the schema to export data to
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # if_exists='replace' akan menghapus tabel lama jika ada dan membuat baru
        # Ini aman untuk seeding awal.
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,
            if_exists='replace',  
        )
    
    return df