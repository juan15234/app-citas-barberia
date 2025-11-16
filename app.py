from flask import Flask, redirect, render_template, request, jsonify, session, url_for
import uuid
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from config import config
from models.CitaModel import CitaModel
from models.GoogleCalendar import GoogleCalendar
from models.Correo import Correo
from conexion import obtener_conexion

load_dotenv(dotenv_path=".env")

app = Flask(__name__)
app.config.from_object(config['development'])
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/horas-disponibles')
def horas_disponibles():
    fecha = request.args.get("fecha")
    barbero = request.args.get("barbero")
    
    barbero_numero = CitaModel.barbero_numero(barbero)
    
    horas_disponibles = CitaModel.horas_disponibles( fecha, barbero_numero)
    
    return jsonify(horas_disponibles)


#------------------------------------
@app.route('/crear_cita')
def crear_cita():
    try:
        
        nombre = request.args.get('nombre')
        correo_cliente = request.args.get('correo_cliente')
        telefono_cliente = request.args.get('telefono_cliente')
        barbero = request.args.get('barbero')
        fecha = request.args.get('fecha')
        hora = request.args.get('hora')
        servicio_numero = session.get('servicio_numero')
        duracion = session.get('duracion')
        nota_cliente = request.args.get('nota')

        barbero_numero = CitaModel.barbero_numero(barbero)

        session['nombre'] = nombre
        session['barbero'] = barbero
        session['hora'] = hora
        session['fecha'] = fecha
        session['correo_cliente'] = correo_cliente
        session['telefono_cliente'] = telefono_cliente
        session['nota_cliente'] = nota_cliente
        
        token = str(uuid.uuid4())

        crear_cita = CitaModel.crear_cita(nombre, barbero_numero, fecha, hora, correo_cliente, telefono_cliente, servicio_numero, duracion, token, nota_cliente)

        if crear_cita == 'Cita creada con exito':
            
            return jsonify({'ok': True, 'estatus': crear_cita, 'token': token, 'fecha':fecha})
        else:
            return jsonify({'ok':False, 'estatus': crear_cita, 'fecha':fecha})
        
    except Exception as e:
        print(e)


@app.route('/agendar/<servicio>')
def agendar(servicio):

    GoogleCalendar.citas_en_calendario()
    
    session['servicio'] = servicio
    
    servicio_numero, duracion = CitaModel.servicio_numero(servicio)
    session['servicio_numero'] = servicio_numero
    session['duracion'] = duracion
    return render_template("agendar.html")

@app.route('/programar_cita_calendario_y_enviar_correo')
def programar_cita_calendario_y_enviar_correo():
    
    nombre = session.get('nombre')
    servicio = session.get('servicio')
    barbero = session.get('barbero')
    duracion = session.get('duracion')
    hora = session.get('hora')
    fecha = session.get('fecha')
    correo_cliente = session.get('correo_cliente')
    servicio_numero = session.get('servicio_numero')
    telefono_cliente = session.get('telefono_cliente')
    nota_cliente = session.get('nota_cliente')
    
    token = request.args.get('token')
    
    evento = GoogleCalendar.crear_evento(nombre, servicio, barbero, correo_cliente, telefono_cliente, hora, fecha, duracion, nota_cliente)
    print(evento)
    
    enviar_correo = Correo.enviar_correo(correo_cliente, nombre, barbero, hora, fecha, servicio_numero, token)
    print(enviar_correo)
    
    guardar_eventos_en_bd = GoogleCalendar.citas_en_calendario()
    print(guardar_eventos_en_bd)
    
    session.clear()
    
    return jsonify({'evento':evento, 'enviar_correo':enviar_correo, 'guardar_eventos_en_bd':guardar_eventos_en_bd})

@app.route('/editar_cita/<token>', methods=['GET'])
def editar_cita(token):
    
    session['token'] = token
    
    
    return render_template('editar_cita.html')

@app.route('/editar_cita_backend', methods=['GET', 'POST'])
def editar_cita_backend():
    nueva_fecha = request.args.get('nueva_fecha')
    nueva_hora = request.args.get('nueva_hora')
    nuevo_barbero = request.args.get('nuevo_barbero')
    token = session.get('token')
    
    nuevo_barbero = CitaModel.barbero_numero(nuevo_barbero)
    

    cita_editada = CitaModel.editar_cita(nueva_fecha, nueva_hora, nuevo_barbero, token)
    
    evento_editado = GoogleCalendar.editar_evento(token, nuevo_barbero, nueva_hora, nueva_fecha)
    
    print(f'{cita_editada}, {evento_editado}')
    
    if cita_editada == 'cita editada exitosamente' and evento_editado == 'evento editado exitosamente':
            
        return jsonify({'ok': True, 'estatus_bd': cita_editada, 'estatus_google_calendar':evento_editado,'token': token})
    else:
        return jsonify({'ok':False, 'estatus_bd': cita_editada, 'estatus_google_calendar':evento_editado})

@app.route('/cancelar_cita_backend')
def cancelar_cita_backend():
    token = session.get('token')
    
    cita_cancelada = CitaModel.cancelar_cita(token)
    
    evento_cancelado = GoogleCalendar.eliminar_evento(token)
    
    print(f'{cita_cancelada}, {evento_cancelado}')
    
    session.clear()
    
    if cita_cancelada == 'cita cancelada exitosamente' and evento_cancelado == 'evento eliminado exitosamente':
        return jsonify({'ok': True, 'estatus_bd': cita_cancelada, 'estatus_google_calendar':evento_cancelado,'token': token})
    else:
        return jsonify({'ok':False, 'estatus_bd': cita_cancelada, 'estatus_google_calendar':evento_cancelado})

@app.route('/home')
def home():
    
    return render_template('home.html')

@app.route('/')
def main():
    return redirect(url_for('home'))


#ENVIO DE CORREOS DE RECORDATORIO DE MANERA AUTOMATICA
scheduler = BackgroundScheduler()
scheduler.add_job(Correo.enviar_recordatorio, trigger='cron', hour=9, misfire_grace_time=3600)
scheduler.add_job(CitaModel.eliminar_citas_viejas, trigger='cron', hour=9, misfire_grace_time=3600)
scheduler.start()

if __name__ == '__main__':
    app.run()
