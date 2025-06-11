from models.entities.Cita import Cita
import traceback
from datetime import datetime, timedelta

class CitaModel():
    
    @classmethod
    def crear_cita(cls,db,cita):
        try:
            
            cursor = db.cursor()
            sql="""SELECT * FROM citas WHERE barbero=%s AND fecha=%s AND hora=%s"""
            values=(cita.barbero, cita.fecha, cita.hora)
            cursor.execute(sql, values)
            results = cursor.fetchone()
            
            if results is None:
                sql="""INSERT INTO citas (nombre_cliente,fecha,servicio,barbero,hora) VALUES (%s,%s,%s,%s,%s)"""
                values=(cita.nombre_cliente,cita.fecha_hora, cita.servicio, cita.barbero,cita.hora)
                cursor.execute(sql, values)
                db.commit()
                
                return 'cita creada con exito'
            else:
                return 'fecha no disponible, seleccione otro horario'
        
        except Exception as ex:
            traceback.print_exc(ex)
        
    
    @classmethod
    def horas_disponibles(cls,db,fecha, barbero):
        try:
        
            cursor = db.cursor()
            sql="""SELECT TIME_FORMAT(hora, '%H:%i') FROM citas WHERE barbero=%s AND fecha=%s"""
            cursor.execute("""SELECT hora FROM citas WHERE barbero=%s AND fecha=%s""", (barbero,fecha))

            horas_ocupadas = [fila[0].strftime("%H:%M") for fila in cursor.fetchall()]

            inicio = datetime.strptime("09:00", "%H:%M")
            fin = datetime.strptime("20:00", "%H:%M")
            todas = []

            while inicio <= fin:
                hora_str = inicio.strftime("%H:%M")
                if hora_str not in horas_ocupadas:
                    todas.append(hora_str)
                inicio += timedelta(minutes=30)
            
            
            return todas
        
        except Exception as ex:
            traceback.print_exc(ex)
