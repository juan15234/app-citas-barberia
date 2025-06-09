from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DATABASE_URL = os.getenv("DATABASE_URL")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    DEBUG=True
    
config={
    'development': DevelopmentConfig
}
    
