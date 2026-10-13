# TallerPro 🔧

**Sistema de gestión para talleres mecánicos**, desarrollado con Python, Flask, SQLAlchemy y MySQL.

TallerPro es una aplicación web orientada a facilitar la administración de clientes, vehículos y órdenes de trabajo de un taller mecánico, mediante una interfaz sencilla y organizada.

## 🚀 Funcionalidades

- **Gestión de clientes:** registro, edición y búsqueda de clientes.
- **Búsqueda por DNI:** permite localizar clientes por su documento y otros datos.
- **Gestión de vehículos:** administración de la información de los vehículos.
- **Órdenes de trabajo:** creación, consulta y edición de órdenes.
- **Panel principal:** acceso a las principales secciones del sistema.
- **Base de datos relacional:** almacenamiento de información mediante MySQL y SQLAlchemy.
- **Interfaz web:** páginas HTML con estilos CSS.

## 🛠️ Tecnologías utilizadas

- Python
- Flask
- SQLAlchemy
- MySQL
- HTML5
- CSS3
- Git y GitHub

## 📁 Estructura del proyecto

```text
TallerPro/
├── backend/          # Aplicación y lógica del sistema
├── database/         # Esquema de la base de datos
│   └── tallerpro.sql
├── frontend/         # Archivos de interfaz y estilos
├── tests/            # Directorio para pruebas
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/facundoibanez1987-eng/TallerPro.git
cd TallerPro
```

### 2. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para instalar las dependencias del proyecto de forma aislada.

```bash
python -m venv .venv
```

En Windows, activar el entorno virtual con PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

Es necesario tener MySQL instalado y en funcionamiento.

Crear una base de datos llamada `TallerPro`:

```sql
CREATE DATABASE TallerPro;
```

**Importar la estructura de las tablas:**

Desde MySQL Workbench, utilizar la opción de importación de un archivo SQL y seleccionar:

```text
database/tallerpro.sql
```

Importar este archivo en la base de datos `TallerPro` recién creada. El archivo contiene instrucciones para eliminar y volver a crear tablas, por lo que no debe ejecutarse sobre una base que contenga información que se quiera conservar.

Crear un archivo `.env` en la carpeta principal del proyecto con las siguientes variables, utilizando los valores correspondientes a la instalación local de MySQL:

```dotenv
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=TallerPro
```

**Importante:** el archivo `.env` contiene credenciales locales y no debe subirse a GitHub.

### 4. Iniciar la aplicación

Desde la carpeta principal del proyecto, ejecutar:

```bash
python backend/app.py
```

Luego abrir el navegador en:

http://127.0.0.1:5001/

## 🎯 Objetivo del proyecto

Este proyecto forma parte de mi formación en desarrollo Full Stack y tiene como objetivo aplicar conocimientos de programación, desarrollo web, bases de datos y control de versiones en una aplicación práctica.

## 👨‍💻 Autor

Desarrollado por **Facundo Ibáñez**.

[Ver repositorio en GitHub](https://github.com/facundoibanez1987-eng/TallerPro)