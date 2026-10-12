# Importamos la función del Repository que necesitamos
from repositories.servicio_repository import obtener_servicios


# Creamos una función para obtener todos los servicios
def listar_servicios(sesion):

    # Obtenemos los servicios mediante el Repository
    servicios = obtener_servicios(sesion)

    # Devolvemos la lista de servicios
    return servicios