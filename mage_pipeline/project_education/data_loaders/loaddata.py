if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import os

@data_loader
def load_data_from_file(*args, **kwargs):
    # Pastikan file sudah dipindah ke folder root project Mage
    filepath = '/home/src/data_kesiapan_pendidikan_enriched.csv'
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan di {filepath}. Pastikan Anda sudah memindahkan file hasil generate ke folder mage_pipeline.")
        
    df = pd.read_csv(filepath)
    
    # Sedikit cleaning nama kolom agar ramah database (lowercase)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    return df

@test
def test_output(output, *args):
    assert output is not None, 'The output is undefined'