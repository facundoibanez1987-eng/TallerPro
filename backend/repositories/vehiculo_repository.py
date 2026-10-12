# Importamos select para realizar consultas a la base de datos
from sqlalchemy import select

# Importamos el modelo Vehiculo para trabajar con los vehículos
from models.vehiculo import Vehiculo


# Creamos una función para obtener todos los vehículos
def obtener_vehiculos(sesion):

    # Creamos la consulta para obtener todos los vehículos
    consulta = select(Vehiculo)

    # Ejecutamos la consulta utilizando la sesión recibida
    resultado = sesion.execute(consulta)

    # Convertimos el resultado en una lista de objetos Vehiculo
    vehiculos = resultado.scalars().all()

    # Devolvemos la lista de vehículos
    return vehiculos


# Creamos una función para buscar un vehículo específico por su ID
def obtener_vehiculo_por_id(sesion, vehiculo_id):

    # Creamos la consulta buscando el vehículo por su ID
    consulta = select(Vehiculo).where(Vehiculo.id == vehiculo_id)

    # Ejecutamos la consulta
    resultado = sesion.execute(consulta)

    # Obtenemos el vehículo encontrado o None
    vehiculo = resultado.scalar_one_or_none()

    # Devolvemos el vehículo encontrado
    return vehiculo

# Creamos una función para registrar un nuevo vehículo
def crear_vehiculo(sesion, cliente_id, patente, marca, modelo, anio):

    # Creamos un objeto Vehiculo con los datos recibidos
    vehiculo = Vehiculo(
        cliente_id=cliente_id,
        patente=patente,
        marca=marca,
        modelo=modelo,
        anio=anio
    )

    # Agregamos el vehículo a la sesión
    sesion.add(vehiculo)

    # Confirmamos la operación y guardamos el vehículo en MySQL
    sesion.commit()

    # Devolvemos el vehículo creado
    return vehiculo


# Creamos una función para actualizar los datos de un vehículo
def actualizar_vehiculo(sesion, vehiculo_id, patente, marca, modelo, anio):

    # Buscamos el vehículo que queremos modificar
    vehiculo = obtener_vehiculo_por_id(sesion, vehiculo_id)

    # Comprobamos que el vehículo exista antes de modificarlo
    if vehiculo:
        vehiculo.patente = patente
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        vehiculo.anio = anio

        # Confirmamos los cambios y los guardamos en MySQL
        sesion.commit()

    # Devolvemos el vehículo actualizado
    return vehiculo


# Creamos una función para eliminar un vehículo
def eliminar_vehiculo(sesion, vehiculo_id):

    # Buscamos el vehículo que queremos eliminar
    vehiculo = obtener_vehiculo_por_id(sesion, vehiculo_id)

    # Comprobamos que el vehículo exista antes de eliminarlo
    if vehiculo:
        sesion.delete(vehiculo)

        # Confirmamos la eliminación y la guardamos en MySQL
        sesion.commit()

    # Devolvemos el vehículo eliminado o None si no existía
    return vehiculo