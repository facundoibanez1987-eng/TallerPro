# Importamos las funciones del Repository de órdenes y servicios
from repositories.orden_servicio_repository import (
    obtener_orden_servicios,
    crear_orden_servicio
)


# Creamos una función para obtener las relaciones entre órdenes y servicios
def listar_orden_servicios(sesion):

    # Pedimos al Repository que consulte las relaciones
    orden_servicios = obtener_orden_servicios(sesion)

    # Devolvemos la lista
    return orden_servicios


# Creamos una función para asociar un servicio a una orden
def registrar_orden_servicio(
    sesion,
    orden_id,
    servicio_id,
    cantidad,
    precio_unitario
):

    # Pedimos al Repository que cree la relación
    orden_servicio = crear_orden_servicio(
        sesion,
        orden_id,
        servicio_id,
        cantidad,
        precio_unitario
    )

    # Devolvemos la relación creada
    return orden_servicio