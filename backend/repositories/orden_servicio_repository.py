# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import select

# Importamos nuestro modelo OrdenServicio
from models.orden_servicio import OrdenServicio


# Creamos una función para obtener todos los servicios asociados a órdenes
def obtener_orden_servicios(sesion):

    # Creamos la consulta
    consulta = select(OrdenServicio)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Obtenemos los objetos OrdenServicio
    orden_servicios = resultado.scalars().all()

    # Devolvemos la lista
    return orden_servicios


# Creamos una función para asociar un servicio a una orden
def crear_orden_servicio(
    sesion,
    orden_id,
    servicio_id,
    cantidad,
    precio_unitario
):

    # Creamos la relación entre la orden y el servicio
    orden_servicio = OrdenServicio(
        orden_id=orden_id,
        servicio_id=servicio_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario
    )

    # Agregamos la relación a la sesión
    sesion.add(orden_servicio)

    # Guardamos los cambios en MySQL
    sesion.commit()

    # Devolvemos la relación creada
    return orden_servicio