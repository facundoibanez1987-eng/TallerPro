# Importamos las herramientas que necesitamos de SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric

# Importamos la Base que utilizan nuestros modelos
from .base import Base


# Creamos la clase Servicio, que representa la tabla servicios de MySQL
class Servicio(Base):
    __tablename__ = "servicios"

    # Identificador único del servicio
    id = Column(Integer, primary_key=True)

    # Nombre del servicio
    nombre = Column(String(50), nullable=False, unique=True)

    # Descripción del servicio
    descripcion = Column(String(150))

    # Precio base del servicio
    precio_base = Column(Numeric(10, 2), nullable=False)