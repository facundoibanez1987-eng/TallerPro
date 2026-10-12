# Importamos las herramientas que necesitamos de SQLAlchemy
from sqlalchemy import Column, Integer, String

# Importamos la Base que creamos para nuestros modelos
from .base import Base


# Definimos el nombre de la tabla que este modelo representa en MySQL
class Cliente(Base):
    __tablename__ = "clientes"

    # Definimos el identificador único del cliente
    id = Column(Integer, primary_key=True)

    # Definimos el nombre del cliente
    nombre = Column(String(50), nullable=False)

    # Definimos el apellido del cliente
    apellido = Column(String(50), nullable=False)

    # Definimos el DNI del cliente
    dni = Column(String(8), unique=True, nullable=True)

    # Definimos el teléfono del cliente
    telefono = Column(String(20), nullable=False)

    # Definimos el email del cliente
    email = Column(String(100), unique=True)
