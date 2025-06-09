from models.entities.Cita import Cita
import traceback

class CitaModel():
    
    @classmethod
    def crear_cita(cls,db,cita):
        try:
            
            cursor = db.cursor()
            sql="""SELECT * FROM citas WHERE barbero=%s AND fecha_hora=%s"""
            values=(cita.barbero, cita.fecha_hora)
            cursor.execute(sql, values)
            results = cursor.fetchone()
            
            if results is None:
                sql="""INSERT INTO citas (nombre_cliente,fecha_hora,servicio,barbero) VALUES (%s,%s,%s,%s)"""
                values=(cita.nombre_cliente,cita.fecha_hora, cita.servicio, cita.barbero)
                cursor.execute(sql, values)
                db.commit()
                
                return 'cita creada con exito'
            else:
                return 'fecha no disponible, seleccione un dia distinto u otra hora'
        
        except Exception as ex:
            traceback.print_exc(ex)
        
    
    @classmethod
    def horas_disponibles(cls,db,fecha, barbero):
        try:
            
            cursor = db.cursor()
            sql="""SELECT hora FROM citas WHERE barbero=%s AND fecha=%s"""
            cursor.execute("""SELECT hora FROM citas WHERE barbero=%s AND fecha=%s"""(barbero,fecha,))

            horas_ocupadas = [fila[0].strftim("%H:%M") for fila in cursor.fetchall()]

            inicio = datetime.strptime("09:00", "%H:%M")
            fin = datetime.strftime("20:00", "%H:M")
            todas = []

            while inicio <= fin:
                hora_str = inicio.strftime("%H:%M")
                if hora_str not in horas_ocupadas:
                    todas.append(hora_str)
                inicio += timedelta(minutes=30)
            
            
            return todas
        
        except Exception as ex:
            traceback.print_exc(ex)
