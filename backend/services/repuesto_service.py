# Importamos la función del Repository que necesitamos
from repositories.repuesto_repository import obtener_repuestos


# Creamos una función para obtener todos los repuestos
def listar_repuestos(sesion):

    # Obtenemos los repuestos mediante el Repository
    repuestos = obtener_repuestos(sesion)

    # Devolvemos la lista de repuestos
    return repuestos
