# Importamos las herramientas que necesitamos de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

# Importamos relationship para relacionar el vehículo con su cliente
from sqlalchemy.orm import relationship

# Importamos la Base que utilizan nuestros modelos
from .base import Base

# Importamos el modelo Cliente para establecer la relación
from .cliente import Cliente

# Creamos la clase Vehiculo, que representa la tabla vehiculos de MySQL
class Vehiculo(Base):
    __tablename__ = "vehiculos"

    # Definimos el identificador único del vehículo
    id = Column(Integer, primary_key=True)

    # Relacionamos el vehículo con el cliente propietario
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relacionamos el vehículo con el cliente propietario
    cliente = relationship("Cliente")

    # Definimos la patente del vehículo
    patente = Column(String(10), unique=True, nullable=False)

    # Definimos la marca del vehículo
    marca = Column(String(50), nullable=False)

    # Definimos el modelo del vehículo
    modelo = Column(String(50), nullable=False)

    # Definimos el año del vehículo
    anio = Column(Integer, nullable=False)

