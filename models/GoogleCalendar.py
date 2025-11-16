from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import uuid
import os
import json
import base64

from models.CitaModel import CitaModel
from conexion import obtener_conexion

class GoogleCalendar:

    @classmethod
    def crear_evento(cls, nombre, servicio, barbero, correo_cliente, telefono_cliente, hora, fecha, duracion, nota_cliente):
        
        try:
            
            barbero = barbero.lower()
            
            if barbero == 'william':
                colorId = '3'
            
            elif barbero == 'ruben':
                colorId = '4'
                
            elif barbero == 'bryan':
                colorId = '6'
                
            elif barbero == 'marcos':
                colorId = '1'
                
            elif barbero == 'jhon':
                colorId = '2'
            
            credentials_json = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS_BASE64')).decode('utf-8')
            info = json.loads(credentials_json)
            
            SCOPES = ['https://www.googleapis.com/auth/calendar']

            CALENDAR_ID = os.getenv('CORREO_BARBERIA')
            
            inicio_str = f'{fecha}T{hora}:00'
            fecha_ini = datetime.strptime(inicio_str, '%Y-%m-%dT%H:%M:%S')

            fecha_fin = fecha_ini + timedelta(minutes=duracion)

            credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

            service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
            

            evento = {
                'summary':f'Nombre: {nombre} Servicio: {servicio}',
                'description': f' | Barbero: {barbero} | CorreoCliente: {correo_cliente} | TelefonoCliente:  {telefono_cliente} | NotaCliente: {nota_cliente}',
                'start': {
                    'dateTime': fecha_ini.isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'end':{
                    'dateTime': fecha_fin.isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'colorId': colorId
            }

            evento = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
        except Exception as e:
            print(e)
            
    @classmethod
    def citas_en_calendario(cls):
            
        def extraer_campo(campo, texto):
            if campo in texto:
                partes = texto.split(campo + ':')
                return partes[1].split('|')[0].strip()
            return 'Desconocido'
        
        credentials_json = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS_BASE64')).decode('utf-8')
        info = json.loads(credentials_json)
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CALENDAR_ID = os.getenv('CORREO_BARBERIA')
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
        
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_results = service.events().list(calendarId=CALENDAR_ID, timeMin=now, singleEvents=True, orderBy='startTime').execute()
        events = events_results.get('items', [])
        
        for event in events:
            try:
                event_summary = event.get('summary', '')
                event_description = event.get('description', '')

                fecha_hora = datetime.fromisoformat(event['start']['dateTime'])

                usuario = extraer_campo('Nombre', event_summary)

                email = extraer_campo('CorreoCliente', event_description)
                telefono = extraer_campo('TelefonoCliente', event_description)
                nota_cliente = extraer_campo('NotaCliente', event_description)

                servicio, duracion = CitaModel.servicio_numero(extraer_campo('Servicio', event_summary))

                barbero = CitaModel.barbero_numero(extraer_campo('Barbero', event_description))

                sql="""SELECT usuario FROM citas WHERE barbero=%s AND fecha_hora=%s"""
                values = (barbero, fecha_hora)

                conexion = obtener_conexion()
                cursor = conexion.cursor()

                cursor.execute(sql, values)

                resultado = cursor.fetchone()

                token = str(uuid.uuid4())


                if resultado:
                    print('evento ya existente en bd')
                else:
                    sql="""INSERT INTO citas(usuario, barbero, fecha_hora, correo_cliente, telefono_cliente, servicio_numero, duracion, token, nota_cliente) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s)"""
                    values = (usuario, barbero, fecha_hora, email, str(telefono), servicio, duracion,  token, nota_cliente)
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()
                    cursor.execute(sql, values)
                    conexion.commit()

                    print('evento guardado en bd')
            except Exception as e:
                print(e)
        return 'citas de google calendar guardadas en base de datos'
            
            
    @classmethod
    def editar_evento(cls, token, nuevo_barbero, nueva_hora, nueva_fecha):
        
        def extraer_campo(campo, texto):
                if campo in texto:
                    partes = texto.split(campo + ':')
                    return partes[1].split('|')[0].strip()
                return 'Desconocido'
        
        credentials_json = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS_BASE64')).decode('utf-8')
        info = json.loads(credentials_json)
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        CALENDAR_ID = os.getenv('CORREO_BARBERIA')
        
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        
        
        service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)

        now = datetime.utcnow().isoformat() + 'Z'
        
        sql="""SELECT usuario FROM citas WHERE token=%s"""
        values = (token)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, values)
        
        resultado = cursor.fetchone()
        
        usuario = resultado[0]
        

        events_results = service.events().list(calendarId=CALENDAR_ID, timeMin=now, singleEvents=True, orderBy='startTime').execute()

        events = events_results.get('items', [])

        for event in events:
            
            event_summary = event.get('summary', '')
            event_description = event.get('description', '')
            
            if event_summary == f'Nombre: {usuario}':
                
                event_id = event['id']
                
                servicio = extraer_campo('servicio', event_summary)
                correo_cliente = extraer_campo('Correo_cliente', event_description)
                telefono_cliente = extraer_campo('Telefono_cliente', event_description)
                
                fecha_ini = datetime.fromisoformat(event['start']['dateTime'])
                fecha_fin = datetime.fromisoformat(event['end']['dateTime'])
                
                duracion = int((fecha_fin - fecha_ini).total_seconds() / 60)
                
                fecha_str = f'{nueva_fecha}T{nueva_hora}:00'
                
                nueva_fecha_ini = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S')
                nueva_fecha_fin = nueva_fecha_ini + timedelta(minutes=duracion)
                
                colorId = event['colorId']
                
                evento_editado = {
                        'summary':f'Nombre: {usuario} Servicio: {servicio}',
                        'description': f'Barbero: {nuevo_barbero} | Correo_cliente: {correo_cliente} | Telefonor_cliente:  {telefono_cliente}',
                        'start': {
                            'dateTime': nueva_fecha_ini.isoformat(),
                            'timeZone': 'America/Bogota',
                        },
                        'end':{
                            'dateTime': nueva_fecha_fin.isoformat(),
                            'timeZone': 'America/Bogota',
                        },
                        'colorId': colorId
                    }
                
                evento_editado = service.events().patch(calendarId=CALENDAR_ID, eventId=event_id, body=evento_editado).execute()
                print(evento_editado)
            else:
                print('evento no encontrado')
                
        return 'evento editado exitosamente'
            
    @classmethod
    def eliminar_evento(cls, token):
        
        credentials_json = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS_BASE64')).decode('utf-8')
        info = json.loads(credentials_json)
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        CALENDAR_ID = os.getenv('CORREO_BARBERIA')
        
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        
        
        service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)

        now = datetime.utcnow().isoformat() + 'Z'
        
        sql="""SELECT usuario FROM citas WHERE token=%s"""
        
        values = (token)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, values)
        
        usuario = cursor.fetchone()
        

        events_results = service.events().list(calendarId=CALENDAR_ID, timeMin=now, singleEvents=True, orderBy='startTime').execute()

        events = events_results.get('items', [])

        for event in events:
            
            event_summary = event.get('summary', '')
            
            if event_summary == f'Nombre: {usuario}':
                
                event_id = event['id']
        
                evento_eliminado = service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
                print(evento_eliminado)
                
        return 'evento eliminado exitosamente'
