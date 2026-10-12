# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import select

# Importamos nuestro modelo OrdenRepuesto
from models.orden_repuesto import OrdenRepuesto


# Creamos una función para obtener todos los repuestos asociados a órdenes
def obtener_orden_repuestos(sesion):

    # Creamos la consulta
    consulta = select(OrdenRepuesto)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Obtenemos los objetos OrdenRepuesto
    orden_repuestos = resultado.scalars().all()

    # Devolvemos la lista
    return orden_repuestos


# Creamos una función para asociar un repuesto a una orden
def crear_orden_repuesto(
    sesion,
    orden_id,
    repuesto_id,
    cantidad,
    precio_unitario
):

    # Creamos la relación entre la orden y el repuesto
    orden_repuesto = OrdenRepuesto(
        orden_id=orden_id,
        repuesto_id=repuesto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario
    )

    # Agregamos la relación a la sesión
    sesion.add(orden_repuesto)

    # Guardamos los cambios en MySQL
    sesion.commit()

    # Devolvemos la relación creada
    return orden_repuesto