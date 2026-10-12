# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, Numeric, ForeignKey

# Importamos la Base que utilizan nuestros modelos
from .base import Base


# Creamos el modelo OrdenRepuesto
class OrdenRepuesto(Base):

    # Indicamos qué tabla de MySQL representa este modelo
    __tablename__ = "orden_repuestos"

    # Identificador único de la relación
    id = Column(Integer, primary_key=True)

    # ID de la orden de trabajo
    orden_id = Column(
        Integer,
        ForeignKey("ordenes_trabajo.id"),
        nullable=False
    )

    # ID del repuesto utilizado
    repuesto_id = Column(
        Integer,
        ForeignKey("repuestos.id"),
        nullable=False
    )

    # Cantidad de repuestos utilizados
    cantidad = Column(Integer, nullable=False)

    # Precio del repuesto en el momento de realizar la orden
    precio_unitario = Column(Numeric(10, 2), nullable=False)