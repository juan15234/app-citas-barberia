from flask import Flask, redirect, url_for,  render_template, request, session
import mysql.connector
import os

from config import config

from models.UserModel import UserModel
from models.entities.User import User

from models.CitaModel import CitaModel
from models.entities.Cita import Cita

app = Flask(__name__)
app.config.from_object(config['development'])

connection = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    return redirect(url_for('home'))
#---------------------home---------------------------

@app.route('/home')
def home():
    return render_template('home.html)

@app.route('/citas')
def view_citas():
    
    cita = Cita(
        nombre= request.form['nombre'],
        email=request.form['email'],
        numero_tel=request.form['telefono'],
        tipo_servicio=request.form['servicio'],
        barbero=request.form['barbero'],
        fecha=request.form['fecha'],
        hora=request.form['hora']
    )
    
    citas = CitaModel.view_citas(connection,cita)
    
    return f'{citas}'

@app.route('/crear_cita')
def crear_cita():
    
    cita = Cita(
        nombre_cliente='samuel',
        servicio='corte',
        barbero='marcos',
        fecha_hora='2025-06-10T16:30:00'
    )
    
    citas =  CitaModel.crear_cita(connection,cita)
    
    return f'{citas}'
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=int(os.environ.get("MYSQLPORT", 5000)), debug=True)
