from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DATABASE_URL = os.getenv("MYSQL_PUBLIC_URL")
    MYSQL_HOST = os.getenv("MYSQLHOST")
    MYSQL_PORT = int(os.getenv("MYSQLPORT"))
    MYSQL_USER = os.getenv("MYSQLUSER")
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DATABASE")
    DEBUG=True
    
config={
    'development': DevelopmentConfig
}
    

