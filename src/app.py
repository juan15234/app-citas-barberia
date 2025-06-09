from flask import Flask, redirect, url_for,  render_template, request, session
import mysql.connector

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
    return redirect(url_for('registro'))

@app.route('/registro',methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        
        user = User(
        nombre = request.form['nombre'],
        contraseña = request.form['contraseña'],
        email = request.form['email'],
        numero_tel = request.form['telefono']
        )
        
        registro_user = UserModel.registro(connection,user)
        print(registro_user)
        
        if registro_user == 'usuario creado con exito':
            return redirect(url_for('home'))
        else:
            mensaje = registro_user
            return render_template('registro.html', mensaje=mensaje)
    
    else:
        return render_template('registro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        
        user = (
            request.form['nombre'],
            request.form['contraseña'],
        )

        login_user = UserModel.login(connection, user)
        
        if login_user == 'usuario encontrado':
            return redirect(url_for('home'))
        else:
            mensaje = login_user
            return render_template('registro.html', mensaje=mensaje)
    
    else:
        return render_template('registro.html')
    
#---------------------home---------------------------

@app.route('/home')
def home():
    
    nombre = session['nombre']
    
    return f'Hola {nombre}'

@app.route('/citas')
def view_citas():
    
    cita = Cita(
        nombre='samuel',
        email='nose@gmail.com',
        numero_tel='3161827643',
        tipo_servicio='barba',
        barbero='marcos',
        fecha_hora='2025-06-10T14:30:00'
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
