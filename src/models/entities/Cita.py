from datetime import datetime

class Cita():
    
    def __init__(self,nombre_cliente,servicio, barbero, fecha_hora):
        self.nombre_cliente=nombre_cliente
        self.servicio=servicio
        self.barbero=barbero
        self.fecha_hora=fecha_hora