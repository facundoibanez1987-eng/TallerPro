# Importamos las herramientas que necesitamos de SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric

# Importamos la Base que utilizan nuestros modelos
from .base import Base


# Creamos la clase Repuesto, que representa la tabla repuestos de MySQL
class Repuesto(Base):
    __tablename__ = "repuestos"

    # Identificador único del repuesto
    id = Column(Integer, primary_key=True)

    # Nombre del repuesto
    nombre = Column(String(50), nullable=False, unique=True)

    # Cantidad disponible en el inventario
    cantidad = Column(Integer, nullable=False)

    # Unidad en la que se mide el repuesto
    unidad_medida = Column(String(20), nullable=False)

    # Precio por unidad
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    # Estado actual del repuesto
    estado = Column(String(20), nullable=False)