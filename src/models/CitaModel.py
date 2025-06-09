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
            db.commit()
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
    def view_citas(cls,db,cita):
        try:
            
            cursor = db.cursor()
            sql="""SELECT * FROM citas WHERE barbero=%s"""
            cursor.execute(sql, (cita.barbero,))
            db.commit()
            results = cursor.fetchall()
            for row in results:
                print(row)
            
            return 'todas las citas programadas'
        
        except Exception as ex:
            traceback.print_exc(ex)