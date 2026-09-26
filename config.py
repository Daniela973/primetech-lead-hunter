import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'primatech-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'banco', 'leads.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAIO_PADRAO_KM = 10
    QUANTIDADE_PADRAO_LEADS = 100
