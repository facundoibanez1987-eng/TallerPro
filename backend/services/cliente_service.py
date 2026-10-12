# Importamos las funciones del Repository que necesitamos para trabajar con clientes
from repositories.cliente_repository import (
    obtener_clientes,
    obtener_cliente_por_id,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente
)

# Importamos re para validar el formato del DNI mediante expresiones regulares
import re

# Validamos que el DNI tenga entre 7 y 8 números
def validar_dni(dni):

    # Eliminamos espacios al principio y al final
    dni = dni.strip()

    # Comprobamos que solamente contenga números
    if not re.fullmatch(r"[0-9]{7,8}", dni):
        raise ValueError(
            "El DNI debe tener entre 7 y 8 números, sin puntos ni espacios."
        )

    # Devolvemos el DNI validado
    return dni

# Creamos una función para obtener todos los clientes
def listar_clientes(sesion):

    # Pedimos al Repository que consulte todos los clientes
    clientes = obtener_clientes(sesion)

    # Devolvemos la lista de clientes
    return clientes



# Creamos una función para obtener un cliente específico por su ID
def buscar_cliente(sesion, cliente_id):

    # Pedimos al Repository que busque el cliente
    cliente = obtener_cliente_por_id(sesion, cliente_id)

    # Devolvemos el cliente encontrado
    return cliente



# Creamos una función para registrar un nuevo cliente
def registrar_cliente(sesion, nombre, apellido, dni, telefono, email):

    # Validamos el DNI antes de guardar
    dni = validar_dni(dni)

    # Pedimos al Repository que cree el cliente
    cliente = crear_cliente(
        sesion,
        nombre,
        apellido,
        dni,
        telefono,
        email
    )

    # Devolvemos el cliente creado
    return cliente


# Creamos una función para actualizar los datos de un cliente
def modificar_cliente(sesion, cliente_id, dni, telefono, email):

    # Validamos el DNI antes de actualizar
    dni = validar_dni(dni)

    # Pedimos al Repository que actualice el cliente
    cliente = actualizar_cliente(
        sesion,
        cliente_id,
        dni,
        telefono,
        email
    )

    # Devolvemos el cliente actualizado
    return cliente



# Creamos una función para eliminar un cliente
def borrar_cliente(sesion, cliente_id):

    # Pedimos al Repository que elimine el cliente
    cliente = eliminar_cliente(sesion, cliente_id)

    # Devolvemos el cliente eliminado
    return cliente