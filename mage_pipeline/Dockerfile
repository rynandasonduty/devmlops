FROM mageai/mageai:latest

# 1. Update pip
RUN pip install --upgrade pip

# 2. Install MLflow & Database
RUN pip install mlflow>=2.10.0 psycopg2-binary boto3 sqlalchemy python-dotenv

# 3. Install Data Science Libs
RUN pip install scikit-learn pandas numpy scipy openpyxl matplotlib seaborn

# 4. Install DVC
RUN pip install dvc

# 5. Install Evidently & Pydantic (Versi aman)
RUN pip install evidently>=0.4.15 pydantic>=2.0.0

# 6. Bersihkan cache
RUN pip cache purge