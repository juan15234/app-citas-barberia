from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import psycopg
from psycopg.rows import dict_row

from conexion import obtener_conexion


class CitaModel:
    
    @classmethod
    def horas_disponibles(cls, fecha, barbero):
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(row_factory=dict_row)
            
            fecha_inicio = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_fin = fecha_inicio.replace(hour=23, minute=59, second=59)
            
            cursor.execute("""SELECT fecha_hora, duracion FROM citas WHERE barbero = %s AND fecha_hora BETWEEN %s AND %s""", (barbero, fecha_inicio, fecha_fin))

            citas = cursor.fetchall()
            
            minutos_ocupados = []
            
            for fecha_hora, duracion in citas:
                
                hora = datetime.strftime(fecha_hora, "%H:%M")
                
                hora_inicio = datetime.strptime(hora, "%H:%M")
                
                for i in range(duracion):
                    bloque = (hora_inicio + timedelta(minutes=i)).strftime("%H:%M")
                    minutos_ocupados.append(bloque)
                    
                    
            inicio_mañana = datetime.strptime("10:00", "%H:%M")
            fin_mañana = datetime.strptime("11:59", "%H:%M")
            
            inicio_tarde = datetime.strptime("12:00","%H:%M")
            fin_tarde = datetime.strptime("17:59","%H:%M")
            
            inicio_noche = datetime.strptime("18:00","%H:%M")
            fin_noche = datetime.strptime("19:00","%H:%M")
                    
            minutos_ocupados = sorted(minutos_ocupados)
            bloques_ocupados = []
            bloque_actual = []

            def hora_a_minutos(hora):
                h, m = map(int, hora.split(":"))
                return h * 60 + m

            for i, hora in enumerate(minutos_ocupados):
                if datetime.strptime(hora, "%H:%M") > fin_noche:
                    break
                else:
                    if not bloque_actual:
                        bloque_actual.append(hora)
                    else:
                        hora_anterior = hora_a_minutos(bloque_actual[-1])
                        hora_actual = hora_a_minutos(hora)
                        if hora_actual == hora_anterior + 1:
                            bloque_actual.append(hora)
                        else:
                            bloques_ocupados.append(bloque_actual)
                            bloque_actual = [hora]
            if bloque_actual:
                bloques_ocupados.append(bloque_actual)
                
            
            horas_disponibles = []
            
            #BLOQUE HORARIO MAÑANA
            
            bloque_mañana = []

            while inicio_mañana <= fin_mañana:
                hora_str = inicio_mañana.strftime("%H:%M")
                if hora_str not in minutos_ocupados:
                    bloque_mañana.append(hora_str)
                inicio_mañana += timedelta(minutes=15)
                
            horas_disponibles.append(bloque_mañana)
                
            #BLOQUE HORARIO TARDE
            
            bloque_tarde = []
                
            while inicio_tarde <= fin_tarde:
                hora_str = inicio_tarde.strftime("%H:%M")
                if hora_str not in minutos_ocupados:
                    bloque_tarde.append(hora_str)
                inicio_tarde += timedelta(minutes=15)
            
            horas_disponibles.append(bloque_tarde)
            
            #BLOQUE HORARIO NOCHE
            
            bloque_noche = []
                
            while inicio_noche <= fin_noche:
                hora_str = inicio_noche.strftime("%H:%M")
                if hora_str not in minutos_ocupados:
                    bloque_noche.append(hora_str)
                inicio_noche += timedelta(minutes=15)
            
            horas_disponibles.append(bloque_noche)
                
            
            if horas_disponibles == []:
                return "no citas disponibles"
            else:
                return horas_disponibles, bloques_ocupados
        
        except Exception as e:
            print(e)
            
            
    @classmethod
    def crear_cita(cls, usuario, barbero, fecha, hora, correo_cliente, telefono_cliente, servicio_numero, duracion, token, nota_cliente):
        try:
            
            fecha_hora_obj = f'{fecha} {hora}'
            
            fecha_hora = datetime.strptime(fecha_hora_obj, '%Y-%m-%d %H:%M')
        
            if fecha_hora.replace(tzinfo=ZoneInfo("America/Bogota")) >= datetime.now(ZoneInfo("America/Bogota")):
                conexion = obtener_conexion()
                cursor = conexion.cursor(row_factory=dict_row)
                sql="""INSERT INTO citas(usuario, barbero, fecha_hora, correo_cliente, telefono_cliente, servicio_numero, duracion, token, nota_cliente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (usuario, barbero, fecha_hora, correo_cliente, str(telefono_cliente), servicio_numero, duracion, token, nota_cliente)
                cursor.execute(sql, values)
                conexion.commit()

                return "Cita creada con exito"
            
            else:
                return "Hora o fecha no disponible"
            
        except Exception as e:
            print(e)
            return e
            
    @classmethod
    def editar_cita(cls, nueva_fecha, nueva_hora, nuevo_barbero, token):
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor(row_factory=dict_row)
            cursor.execute("""SELECT * FROM citas WHERE token=%s""",(token,))
            resultado = cursor.fetchone()
            
            fecha_hora_obj = f'{nueva_fecha} {nueva_hora}'
            
            fecha_obj = datetime.strptime(fecha_hora_obj, '%Y-%m-%d %H:%M')
            
            if resultado :
                
                if fecha_obj.replace(tzinfo=ZoneInfo("America/Bogota")) >= datetime.now(ZoneInfo("America/Bogota")):
                    cursor.execute("UPDATE citas SET fecha_hora=%s, barbero=%s WHERE token=%s", (fecha_obj, nuevo_barbero, token,))
                    conexion.commit()

                    return 'Cita editada exitosamente'
                else:
                    return 'Hora o fecha no disponible'
            else:
                
                return 'cita no encontrada', 404
            
        except Exception as e:
            print(e)
        
    @classmethod
    def eliminar_citas_viejas(cls):
        
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor(row_factory=dict_row)
            cursor.execute("""DELETE FROM citas WHERE fecha_hora::date < CURRENT_DATE""")
            conexion.commit()
            
            print('citas viejas eliminadas')
            
            
        except Exception as e:
            print(e)
            
    @classmethod
    def cancelar_cita(cls, token):
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor(row_factory=dict_row)
            cursor.execute("""SELECT * FROM citas WHERE token=%s""",(token,))
            resultado = cursor.fetchone()
            
            if resultado:
                
                cursor.execute("""DELETE FROM citas WHERE token=%s""", (token,))
                conexion.commit()
                
                return 'cita cancelada exitosamente'
            
            else:
                
                return 'cita no encontrada', 404
            
        except Exception as e:
            print(e)
    
    @classmethod
    def barbero_numero(cls, barbero):
        
        
        barbero = barbero.lower()
        
        if barbero == 'william':
            barbero = 1
            return barbero
            
        elif barbero == 'ruben':
            barbero = 2
            return barbero
            
        elif barbero == 'bryan':
            barbero = 3
            return barbero
            
        elif barbero == 'marcos':
            barbero = 4
            return barbero
            
        elif barbero == 'jhon':
            barbero = 5
            return barbero
        
    @classmethod
    def servicio_numero(cls, servicio):
        if servicio == 'corte':
            servicio = 1
            duracion = 45
            return servicio, duracion
        
        elif servicio == 'afeitado_barba':
            servicio = 2
            duracion =30
            return servicio, duracion
        
        elif servicio == 'corte_barba':
            servicio = 3
            duracion = 60
            return servicio, duracion
        
        elif servicio == 'arreglo_barba':
            servicio = 4
            duracion = 30
            return servicio, duracion
        
        elif servicio == 'barba_tinte':
            servicio = 5
            duracion = 30
            return servicio, duracion
        
        elif servicio == 'limpieza_facial':
            servicio = 6
            duracion = 30
            return servicio, duracion
        
        elif servicio == 'corte_alizado':
            servicio = 7
            duracion = 45
            return servicio, duracion
        
        elif servicio == 'depilacion_cpn':
            servicio = 8
            duracion = 30
            return servicio, duracion
                
