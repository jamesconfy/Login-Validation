import os
import dotenv

dotenv.load_dotenv()

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_PORT = os.environ.get('MYSQL_PORT')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = False
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'