# Importamos las funciones del Repository de vehículos
from repositories.vehiculo_repository import (
    obtener_vehiculos,
    obtener_vehiculo_por_id,
    crear_vehiculo,
    actualizar_vehiculo,
    eliminar_vehiculo
)


# Creamos una función para obtener todos los vehículos
def listar_vehiculos(sesion):

    # Pedimos al Repository que consulte todos los vehículos
    vehiculos = obtener_vehiculos(sesion)

    # Devolvemos la lista de vehículos
    return vehiculos


# Creamos una función para obtener un vehículo específico
def buscar_vehiculo(sesion, vehiculo_id):

    # Pedimos al Repository que busque el vehículo
    vehiculo = obtener_vehiculo_por_id(sesion, vehiculo_id)

    # Devolvemos el vehículo encontrado
    return vehiculo


# Creamos una función para registrar un nuevo vehículo
def registrar_vehiculo(sesion, cliente_id, patente, marca, modelo, anio):

    # Pedimos al Repository que cree el vehículo
    vehiculo = crear_vehiculo(
        sesion,
        cliente_id,
        patente,
        marca,
        modelo,
        anio
    )

    # Devolvemos el vehículo creado
    return vehiculo


# Creamos una función para actualizar un vehículo
def modificar_vehiculo(sesion, vehiculo_id, patente, marca, modelo, anio):

    # Pedimos al Repository que actualice el vehículo
    vehiculo = actualizar_vehiculo(
        sesion,
        vehiculo_id,
        patente,
        marca,
        modelo,
        anio
    )

    # Devolvemos el vehículo actualizado
    return vehiculo


# Creamos una función para eliminar un vehículo
def borrar_vehiculo(sesion, vehiculo_id):

    # Pedimos al Repository que elimine el vehículo
    vehiculo = eliminar_vehiculo(sesion, vehiculo_id)

    # Devolvemos el vehículo eliminado
    return vehiculo