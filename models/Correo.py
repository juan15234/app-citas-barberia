import yagmail
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from conexion import obtener_conexion

class Correo:
    
    @classmethod
    def enviar_correo(cls, correo_cliente, nombre, barbero, hora, fecha, servicio_numero, token):
        
        if servicio_numero == 1:
            
            servicio = 'corte de pelo'
            
        elif servicio_numero == 2:
            
            servicio = 'afeitado de barba'
            
        elif servicio_numero == 3:
            
            servicio = 'corte de pelo y afeitado de barba'
            
        elif servicio_numero == 4:
            
            servicio = 'arreglo de barba'
        
        elif servicio_numero == 5:
            
            servicio = 'afeitado de barba y tinte'
            
        elif servicio_numero == 6:
            
            servicio = ' limpieza facial'
            
        elif servicio_numero == 7:
            
            servicio = 'corte de pelo y alizado'
            
        elif servicio_numero == 8:
            
            servicio = 'depilacion CPN cera, orejas y nariz'
        
        try:
            
            
            link = f'http://127.0.0.1:5000/editar_cita/{token}'
            
            mensaje_html = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>

                    <style>
                        .carta{{
                            background-color: rgb(63, 65, 71);
                            color: white;
                        }}

                        .carta a{{
                            color: white;
                            background-color: black;
                            border-radius: 20px;
                            padding: 5px;
                        }}
                    </style>

                </head>
                <body>
                    <h2>The Barber Factory</h2>
                    <div class="carta">
                        <p>¡Hola {nombre}!</p>
                        <p>Acabas de agendar una cita con <strong>{barbero}</strong></p>
                        <p>Fecha: <strong>{fecha}</strong></p>
                        <p>Hora: <strong>{hora}</strong></p>
                        <p>Servicio: <strong>{servicio}</strong></p>
                        <p>¿Quieres editar o eliminar la cita?, <a href="{link}">¡Preciona aqui!</a></p>
                    </div>
                </body>
                </html>
            """
            
            correo_barberia = os.getenv('CORREO_BARBERIA')
            contraseña_app = os.getenv('CONTRASENA_APP')
            
            yag = yagmail.SMTP(correo_barberia, contraseña_app)
        
            yag.send(
                to=f'{correo_cliente}',
                subject='Cita The Barber Factory',
                contents=[mensaje_html]
            )
        except Exception as e:
            print(e)
        
    @classmethod
    def enviar_recordatorio(cls):
        
        hoy = datetime.now(ZoneInfo("America/Bogota"))
        
        fecha_inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
    
        fecha_fin = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""SELECT * FROM citas WHERE fecha_hora BETWEEN %s AND %s""", (fecha_inicio, fecha_fin,))
        
        citas = cursor.fetchall()
        
        for cita in citas:
            
            nombre = cita[1]
            fecha_hora = cita[3]
            barbero_numero = int(cita[2])
            correo_cliente = cita[4]
            servicio_numero = int(cita[6])
            
            hora = fecha_hora.time()
            
            
            servicio_texto = Correo.servicio_numero_to_servicio_texto(servicio_numero)
                
            barbero = Correo.barbero_numero_to_barbero_texto(barbero_numero)

            try:

                mensaje_html = f"""
                    <!DOCTYPE html>
                    <html lang="es">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Document</title>

                        <style>
                            .carta{{
                                background-color: rgb(63, 65, 71);
                                color: white;
                            }}

                            .carta a{{
                                color: white;
                                background-color: black;
                                border-radius: 20px;
                                padding: 5px;
                            }}
                        </style>

                    </head>
                    <body>
                        <h2>The Barber Factory</h2>
                        <div class="carta">
                            <p>¡Hola {nombre}!</p>
                            <p>Recuerda que tienes una cita el dia de hoy con <strong>{barbero}</strong></p>
                            <p>Hora: <strong>{hora}</strong></p>
                            <p>Servicio: <strong>{servicio_texto}</strong></p>
                        </div>
                    </body>
                    </html>
                """

                correo_barberia = os.getenv('CORREO_BARBERIA')
                contraseña_app = os.getenv('CONTRASENA_APP')

                yag = yagmail.SMTP(correo_barberia, contraseña_app)

                yag.send(
                    to=f'{correo_cliente}',
                    subject='Recordatorio Cita The Barber Factory',
                    contents=[mensaje_html]
                )
                
            except Exception as e:
                print(e)
        
        return 'se ha enviado los recordatorios a los correos de los clientes'
    
    @classmethod
    def servicio_numero_to_servicio_texto(cls, servicio_numero):
        if servicio_numero == 1:
            
            return 'corte de pelo'
        
        elif servicio_numero == 2:
        
            return 'afeitado de barba'
        elif servicio_numero == 3:
        
            return 'corte de pelo y afeitado de barba'
        elif servicio_numero == 4:
        
            return 'arreglo de barba'
        elif servicio_numero == 5:
        
            return 'afeitado de barba y tinte'
        elif servicio_numero == 6:
        
            return ' limpieza facial'
        elif servicio_numero == 7:
        
            return 'corte de pelo y alizado'
        elif servicio_numero == 8:
        
            return 'depilacion CPN cera, orejas y nariz'
        else:
            return 'NADA'
        
    @classmethod
    def barbero_numero_to_barbero_texto(cls, barbero_numero):
        if barbero_numero == 1:

            return 'william'
        elif barbero_numero == 2:
        
            return 'ruben'
        elif barbero_numero == 3:
        
            return 'bryan'
        elif barbero_numero == 4:
        
            return 'marcos'
        elif barbero_numero == 5:
        
            return 'jhon'
        
        else:
            return 'NADA'