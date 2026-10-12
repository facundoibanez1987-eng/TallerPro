# Importamos select para realizar consultas a la base de datos
from sqlalchemy import select

# Importamos el modelo OrdenTrabajo
from models.orden_trabajo import OrdenTrabajo


# Creamos una función para obtener todas las órdenes de trabajo
def obtener_ordenes(sesion):

    # Creamos la consulta para obtener todas las órdenes
    consulta = select(OrdenTrabajo)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Convertimos el resultado en una lista de objetos OrdenTrabajo
    ordenes = resultado.scalars().all()

    # Devolvemos la lista de órdenes
    return ordenes


# Creamos una función para buscar una orden específica por su ID
def obtener_orden_por_id(sesion, orden_id):

    # Creamos la consulta buscando la orden por su ID
    consulta = select(OrdenTrabajo).where(OrdenTrabajo.id == orden_id)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Obtenemos la orden encontrada o None
    orden = resultado.scalar_one_or_none()

    # Devolvemos la orden encontrada
    return orden

# Creamos una función para registrar una nueva orden de trabajo
def crear_orden(
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

    # Creamos un objeto OrdenTrabajo con los datos recibidos
    orden = OrdenTrabajo(
        vehiculo_id=vehiculo_id,
        tipo_orden=tipo_orden,
        fecha_ingreso=fecha_ingreso,
        fecha_entrega=fecha_entrega,
        tipo_servicio=tipo_servicio,
        descripcion=descripcion,
        estado=estado,
        costo=costo
    )

    # Agregamos la orden a la sesión
    sesion.add(orden)

    # Confirmamos la operación y guardamos la orden en MySQL
    sesion.commit()

    # Devolvemos la orden creada
    return orden


# Creamos una función para actualizar una orden existente
def actualizar_orden(
    sesion,
    orden_id,
    tipo_orden,
    fecha_entrega,
    tipo_servicio,
    descripcion,
    estado,
    costo
):

    # Buscamos la orden que queremos modificar
    orden = obtener_orden_por_id(sesion, orden_id)

    # Comprobamos que la orden exista antes de modificarla
    if orden:
        orden.tipo_orden = tipo_orden
        orden.fecha_entrega = fecha_entrega
        orden.tipo_servicio = tipo_servicio
        orden.descripcion = descripcion
        orden.estado = estado
        orden.costo = costo

        # Confirmamos los cambios y los guardamos en MySQL
        sesion.commit()

    # Devolvemos la orden actualizada
    return orden


# Creamos una función para eliminar una orden
def eliminar_orden(sesion, orden_id):

    # Buscamos la orden que queremos eliminar
    orden = obtener_orden_por_id(sesion, orden_id)

    # Comprobamos que la orden exista antes de eliminarla
    if orden:
        sesion.delete(orden)

        # Confirmamos la eliminación y la guardamos en MySQL
        sesion.commit()

    # Devolvemos la orden eliminada o None si no existía
    return orden

