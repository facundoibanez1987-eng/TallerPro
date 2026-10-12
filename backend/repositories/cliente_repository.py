# Importamos select para realizar consultas a la base de datos
from sqlalchemy import select

# Importamos el modelo Cliente para trabajar con los clientes
from models.cliente import Cliente


# Creamos una función para obtener todos los clientes de la base de datos
def obtener_clientes(sesion):

    # Creamos la consulta para obtener todos los clientes
    consulta = select(Cliente)

    # Ejecutamos la consulta utilizando la sesión recibida
    resultado = sesion.execute(consulta)

    # Convertimos el resultado en una lista de objetos Cliente
    clientes = resultado.scalars().all()

    # Devolvemos la lista de clientes
    return clientes


# Creamos una función para buscar un cliente específico por su ID
def obtener_cliente_por_id(sesion, cliente_id):

    # Creamos la consulta buscando el cliente cuyo ID coincida
    consulta = select(Cliente).where(Cliente.id == cliente_id)

    # Ejecutamos la consulta utilizando la sesión recibida
    resultado = sesion.execute(consulta)

    # Obtenemos el cliente encontrado o None si no existe
    cliente = resultado.scalar_one_or_none()

    # Devolvemos el cliente encontrado
    return cliente


# Creamos una función para agregar un nuevo cliente a la base de datos
def crear_cliente(sesion, nombre, apellido, dni, telefono, email):

    # Creamos un objeto Cliente con los datos recibidos
    cliente = Cliente(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        telefono=telefono,
        email=email
    )

    # Agregamos el nuevo cliente a la sesión
    sesion.add(cliente)

    # Confirmamos la operación y guardamos el cliente en MySQL
    sesion.commit()

    # Devolvemos el cliente creado
    return cliente


# Creamos una función para actualizar los datos de un cliente existente
def actualizar_cliente(sesion, cliente_id, dni, telefono, email):

    # Buscamos el cliente que queremos modificar
    cliente = obtener_cliente_por_id(sesion, cliente_id)

    # Comprobamos que el cliente exista antes de modificarlo
    if cliente:

        # Actualizamos los datos del cliente
        cliente.dni = dni
        cliente.telefono = telefono
        cliente.email = email

        # Confirmamos los cambios y los guardamos en MySQL
        sesion.commit()

    # Devolvemos el cliente actualizado
    return cliente


# Creamos una función para eliminar un cliente existente
def eliminar_cliente(sesion, cliente_id):

    # Buscamos el cliente que queremos eliminar
    cliente = obtener_cliente_por_id(sesion, cliente_id)

    # Comprobamos que el cliente exista antes de eliminarlo
    if cliente:
        sesion.delete(cliente)

        # Confirmamos la eliminación y la guardamos en MySQL
        sesion.commit()

    # Devolvemos el cliente eliminado o None si no existía
    return cliente