# Importamos las funciones del Repository de órdenes y repuestos
from repositories.orden_repuesto_repository import (
    obtener_orden_repuestos,
    crear_orden_repuesto
)


# Creamos una función para obtener las relaciones entre órdenes y repuestos
def listar_orden_repuestos(sesion):

    # Pedimos al Repository que consulte las relaciones
    orden_repuestos = obtener_orden_repuestos(sesion)

    # Devolvemos la lista
    return orden_repuestos


# Creamos una función para asociar un repuesto a una orden
def registrar_orden_repuesto(
    sesion,
    orden_id,
    repuesto_id,
    cantidad,
    precio_unitario
):

    # Pedimos al Repository que cree la relación
    orden_repuesto = crear_orden_repuesto(
        sesion,
        orden_id,
        repuesto_id,
        cantidad,
        precio_unitario
    )

    # Devolvemos la relación creada
    return orden_repuesto