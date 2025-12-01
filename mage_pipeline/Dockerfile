FROM mageai/mageai:latest

# 1. Update pip
RUN pip install --upgrade pip

# 2. Install MLflow (FIX: Pakai == untuk memaksa versi 2.14.0)
# Ini akan meng-uninstall versi bawaan image dan memasang versi yang benar
RUN pip install mlflow==2.14.0 psycopg2-binary boto3 sqlalchemy python-dotenv

# 3. Install Data Science Libs
RUN pip install scikit-learn pandas numpy scipy openpyxl matplotlib seaborn

# 4. Install DVC
RUN pip install dvc

# 5. Install Evidently & Pydantic
# Versi evidently>=0.4.15 aman karena tidak konflik dengan server
RUN pip install evidently==0.6.0 pydantic==2.6.0

# 6. Bersihkan cache
RUN pip cache purge