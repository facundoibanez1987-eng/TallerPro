# Importamos select para realizar consultas a la base de datos
from sqlalchemy import select

# Importamos el modelo Servicio
from models.servicio import Servicio


# Obtenemos todos los servicios registrados
def obtener_servicios(sesion):

    # Creamos la consulta para obtener todos los servicios
    consulta = select(Servicio)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Convertimos el resultado en objetos Servicio
    servicios = resultado.scalars().all()

    # Devolvemos la lista de servicios
    return servicios