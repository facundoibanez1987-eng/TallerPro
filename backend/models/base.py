# Importamos la clase base que SQLAlchemy utiliza para crear nuestros modelos
from sqlalchemy.orm import DeclarativeBase

# Creamos la Base que van a utilizar todos nuestros modelos
class Base(DeclarativeBase):
    pass