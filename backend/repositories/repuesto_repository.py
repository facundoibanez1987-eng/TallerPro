# Importamos select para realizar consultas a la base de datos
from sqlalchemy import select

# Importamos el modelo Repuesto
from models.repuesto import Repuesto


# Obtenemos todos los repuestos registrados
def obtener_repuestos(sesion):

    # Creamos la consulta para obtener todos los repuestos
    consulta = select(Repuesto)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Convertimos el resultado en objetos Repuesto
    repuestos = resultado.scalars().all()

    # Devolvemos la lista de repuestos
    return repuestos