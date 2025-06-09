from .entities.User import User
from flask import session
import traceback

class UserModel():
    
    @classmethod
    def registro(cls, db, user):
        
        
        #revisar si los datos ya estan en uso
        cursor = db.cursor()
        sql = """SELECT * FROM usuarios WHERE nombre=%s OR email=%s OR numero_tel=%s"""
        values=(user.nombre,user.email,user.numero_tel)
        cursor.execute(sql,values)
        db.commit()
        results = cursor.fetchone()
        cursor.close()
        
        if results is None:
            
            #encriptar la contraseña
            hashed_password = User.generar_hashed_password(user.contraseña)
        
            print(user.nombre + ' ' + user.contraseña + ' ' + user.email + ' ' + user.numero_tel)

            try:
                cursor = db.cursor()
                sql = """INSERT INTO usuarios (nombre,contraseña,email,numero_tel) VALUES (%s,%s,%s,%s)"""
                values = (user.nombre, hashed_password, user.email, user.numero_tel)
                cursor.execute(sql,values)
                db.commit()
                cursor.close()
                
                session['nombre']=user.nombre
                session['email']=user.email
                session['numero_tel']=user.numero_tel
                
                return 'usuario creado con exito'
            except Exception as ex:
                print(ex)
                traceback.print_exc()
        else:
            return 'nombre de usuario, email o numero de telefono en uso, ingrese otros datos'
            
    @classmethod
    def login(cls,db,user):
        try:
            
            #revisar si el usuario existe
            cursor = db.cursor()
            sql = """SELECT * FROM usuarios WHERE nombre=%s"""
            values = (user[0],)
            cursor.execute(sql,values)
            db.commit()
            results = cursor.fetchone()
            cursor.close()

            if results is None:
                
                return 'usuario no encontrado'
            
            else:
                
                #guardar datos obtenidos de la base de datos
                id, nombre_db, contraseña_db, email_db, numero_tel_db = results
                
                session['nombre']=nombre_db
                session['email']=email_db
                session['numero_tel']=numero_tel_db
                
                #revisar si la contraseña es la misma que en la base de datos
                correct_password = User.revisar_hashed_password(contraseña_db, user[1])
                
                if correct_password:
                    return 'usuario encontrado'
                else:
                    return 'contraseña incorrecta'
                
                
                
        except Exception as ex:
            print(ex)
            traceback.print_exc()