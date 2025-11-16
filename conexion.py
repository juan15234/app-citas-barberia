import pymysql
import os

def obtener_conexion():
    
    conexion = pymysql.connect(
        user = os.getenv('USER_DB'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        database = os.getenv('DATABASE'),
        port = int(os.getenv('PORT')),
    )
    return conexion