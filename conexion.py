import psycopg
import os

def obtener_conexion():
    conexion = psycopg.connect(
        user = os.getenv('USER_DB'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        database = os.getenv('DATABASE'),
        port = int(os.getenv('PORT_DB')),
    )
    return conexion
