import os

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER', 'admin')}:{os.getenv('DB_PASS', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'bookstore')}"
SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey-prod-2025')
SQLALCHEMY_TRACK_MODIFICATIONS = False

