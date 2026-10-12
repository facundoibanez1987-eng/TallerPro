# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

# Importamos la Base que utilizan nuestros modelos
from .base import Base


# Creamos la clase OrdenTrabajo, que representa la tabla ordenes_trabajo
class OrdenTrabajo(Base):
    __tablename__ = "ordenes_trabajo"

    # Definimos el identificador único de la orden
    id = Column(Integer, primary_key=True)

    # Relacionamos la orden con el vehículo correspondiente
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)

    # Creamos la relación para acceder a los datos del vehículo desde una orden
    vehiculo = relationship("Vehiculo")

    # Definimos el tipo de orden: SERVICIO o REPARACION
    tipo_orden = Column(String(20), nullable=False)

    # Definimos la fecha en que ingresó el vehículo
    fecha_ingreso = Column(Date, nullable=False)

    # Definimos la fecha de entrega, que puede quedar vacía
    fecha_entrega = Column(Date)

    # Definimos el tipo de servicio realizado
    tipo_servicio = Column(String(50), nullable=False)

    # Definimos la descripción del trabajo
    descripcion = Column(String(100), nullable=False)

    # Definimos el estado actual de la orden
    estado = Column(String(20), nullable=False)

    # Definimos el costo total de la orden
    costo = Column(Numeric(10, 2), nullable=False)
