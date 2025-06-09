from werkzeug.security import check_password_hash, generate_password_hash

class User:
    
    def __init__(self,nombre,contraseña,email,numero_tel):
        self.nombre=nombre
        self.contraseña=contraseña
        self.email=email
        self.numero_tel=numero_tel
        
    @classmethod
    def revisar_hashed_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    @classmethod
    def generar_hashed_password(cls, password):
        return generate_password_hash(password)
        