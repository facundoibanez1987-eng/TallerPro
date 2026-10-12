# Importamos os para poder leer las variables de entorno
import os

# Importamos load_dotenv para cargar las variables guardadas en .env
from dotenv import load_dotenv

# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Cargamos las variables del archivo .env
load_dotenv()


# Obtenemos los datos de conexión desde las variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Construimos la URL de conexión a MySQL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Creamos el motor de conexión hacia nuestra base de datos TallerPro
engine = create_engine(DATABASE_URL)


# Creamos las sesiones que utilizaremos para trabajar con la base de datos
Session = sessionmaker(bind=engine)


# Función para obtener una nueva sesión
def obtener_sesion():
    return Session()