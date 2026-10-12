# Importamos las funciones del Repository de órdenes de trabajo
from repositories.orden_trabajo_repository import (
    obtener_ordenes,
    obtener_orden_por_id,
    crear_orden,
    actualizar_orden,
    eliminar_orden
)


# Creamos una función para obtener todas las órdenes
def listar_ordenes(sesion):

    # Pedimos al Repository que consulte todas las órdenes
    ordenes = obtener_ordenes(sesion)

    # Devolvemos la lista de órdenes
    return ordenes


# Creamos una función para buscar una orden específica
def buscar_orden(sesion, orden_id):

    # Pedimos al Repository que busque la orden
    orden = obtener_orden_por_id(sesion, orden_id)

    # Devolvemos la orden encontrada
    return orden


# Creamos una función para registrar una nueva orden
def registrar_orden(
    sesion,
    vehiculo_id,
    tipo_orden,
    fecha_ingreso,
    fecha_entrega,
    tipo_servicio,
    descripcion,
    estado,
    costo
):

    # Pedimos al Repository que cree la orden
    orden = crear_orden(
        sesion,
        vehiculo_id,
        tipo_orden,
        fecha_ingreso,
        fecha_entrega,
        tipo_servicio,
        descripcion,
        estado,
        costo
    )

    # Devolvemos la orden creada
    return orden


# Creamos una función para modificar una orden existente
def modificar_orden(
    sesion,
    orden_id,
    tipo_orden,
    fecha_entrega,
    tipo_servicio,
    descripcion,
    estado,
    costo
):

    # Pedimos al Repository que actualice la orden
    orden = actualizar_orden(
        sesion,
        orden_id,
        tipo_orden,
        fecha_entrega,
        tipo_servicio,
        descripcion,
        estado,
        costo
    )

    # Devolvemos la orden actualizada
    return orden


# Creamos una función para eliminar una orden
def borrar_orden(sesion, orden_id):

    # Pedimos al Repository que elimine la orden
    orden = eliminar_orden(sesion, orden_id)

    # Devolvemos la orden eliminada
    return orden

