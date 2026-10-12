# Importamos Flask y render_template para trabajar con nuestras páginas HTML
from flask import Flask, render_template, request, redirect

# Importamos la función para obtener una sesión de MySQL
from conexion import obtener_sesion

# Importamos el Service que trabaja con los clientes
from services.cliente_service import (
    listar_clientes,
    registrar_cliente,
    buscar_cliente,
    modificar_cliente,
    borrar_cliente
)

# Importamos el Service que trabaja con los vehículos
from services.vehiculo_service import (
    listar_vehiculos,
    registrar_vehiculo,
    buscar_vehiculo,
    modificar_vehiculo,
    borrar_vehiculo
)

# Importamos el Service que trabaja con las órdenes
from services.orden_trabajo_service import (
    listar_ordenes,
    registrar_orden,
    buscar_orden,
    modificar_orden,
    borrar_orden
)

# Importamos el Service que trabaja con los servicios asociados a órdenes
from services.orden_servicio_service import (
    registrar_orden_servicio,
    listar_orden_servicios
)


# Importamos el Service que trabaja con los repuestos asociados a órdenes
from services.orden_repuesto_service import (
    registrar_orden_repuesto,
    listar_orden_repuestos
)

# Importamos IntegrityError para detectar errores de integridad en MySQL
from sqlalchemy.exc import IntegrityError


# Importamos el Service que trabaja con los servicios
from services.servicio_service import listar_servicios

# Importamos el Service que trabaja con los repuestos
from services.repuesto_service import listar_repuestos

# Importamos el modelo Cliente para consultar los clientes en la base de datos
from models.cliente import Cliente


# Creamos la aplicación indicando dónde están nuestros archivos CSS
app = Flask(__name__, static_folder="../frontend")




# Creamos la ruta principal de TallerPro
@app.route("/")
def inicio():

    # Abrimos una sesión para consultar la base de datos
    sesion = obtener_sesion()

    try:
        # Obtenemos los clientes registrados
        lista_clientes = listar_clientes(sesion)

        # Obtenemos los vehículos registrados
        lista_vehiculos = listar_vehiculos(sesion)

        # Obtenemos las órdenes de trabajo
        lista_ordenes = listar_ordenes(sesion)

        # Obtenemos los repuestos del inventario
        lista_repuestos = listar_repuestos(sesion)

        # Contamos los clientes registrados
        total_clientes = len(lista_clientes)

        # Contamos los vehículos registrados
        total_vehiculos = len(lista_vehiculos)

        # Contamos las órdenes que están en proceso
        ordenes_en_proceso = sum(
            1
            for orden in lista_ordenes
            if orden.estado.strip().upper() == "EN PROCESO"
        )

        # Contamos los tipos de repuestos registrados
        total_tipos_repuestos = len(lista_repuestos)

        # Ordenamos las órdenes desde la más reciente
        ordenes_recientes = sorted(
            lista_ordenes,
            key=lambda orden: orden.fecha_ingreso,
            reverse=True
        )[:5]

        # Enviamos los indicadores y las órdenes a la plantilla
        return render_template(
            "index.html",
            total_clientes=total_clientes,
            total_vehiculos=total_vehiculos,
            ordenes_en_proceso=ordenes_en_proceso,
            total_tipos_repuestos=total_tipos_repuestos,
            ordenes_recientes=ordenes_recientes
        )

    finally:
        # Cerramos la sesión incluso si ocurre un error
        sesion.close()



# Mostramos los clientes con búsqueda y paginación
@app.route("/clientes")
def clientes():

    # Abrimos una sesión con MySQL
    sesion = obtener_sesion()

    try:
        # Obtenemos el texto escrito en el buscador
        busqueda = request.args.get("buscar", "").strip()

        # Obtenemos el número de página
        pagina = request.args.get("pagina", 1, type=int)
        pagina = max(pagina, 1)

        # Definimos cuántos clientes mostramos por página
        por_pagina = 10

        # Preparamos la consulta de clientes
        consulta = sesion.query(Cliente)

        # Filtramos por nombre, apellido, DNI, teléfono o email
        if busqueda:
            from sqlalchemy import or_

            termino = f"%{busqueda}%"

            consulta = consulta.filter(
                or_(
                    Cliente.nombre.ilike(termino),
                    Cliente.apellido.ilike(termino),
                    Cliente.dni.ilike(termino),
                    Cliente.telefono.ilike(termino),
                    Cliente.email.ilike(termino)
                )
            )

        # Contamos los resultados encontrados
        total_clientes = consulta.count()

        # Calculamos la cantidad de páginas
        total_paginas = max(
            1,
            (total_clientes + por_pagina - 1) // por_pagina
        )

        # Evitamos pedir una página que no existe
        pagina = min(pagina, total_paginas)

        # Obtenemos solamente los clientes de esta página
        lista_clientes = (
            consulta
            .order_by(Cliente.apellido, Cliente.nombre)
            .offset((pagina - 1) * por_pagina)
            .limit(por_pagina)
            .all()
        )

        # Enviamos los datos a la plantilla
        return render_template(
            "clientes.html",
            clientes=lista_clientes,
            buscar=busqueda,
            pagina=pagina,
            por_pagina=por_pagina,
            total_clientes=total_clientes,
            total_paginas=total_paginas
        )

    finally:
        # Cerramos la sesión incluso si ocurre un error
        sesion.close()


# Creamos la ruta para registrar un cliente
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    # Si el formulario fue enviado
    if request.method == "POST":

        # Obtenemos los datos enviados por el formulario
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        dni = request.form["dni"].strip()
        telefono = request.form["telefono"].strip()
        email = request.form.get("email", "").strip() or None

        # Creamos una sesión con MySQL
        sesion = obtener_sesion()

        try:
            # Registramos el cliente utilizando nuestro Service
            registrar_cliente(
                sesion,
                nombre,
                apellido,
                dni,
                telefono,
                email
            )

        except ValueError as error:
            # Mostramos el error de validación en el formulario
            return render_template(
                "nuevo_cliente.html",
                error=str(error),
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                email=email or ""
            )

        except IntegrityError:
            # Deshacemos la operación si un dato único está repetido
            sesion.rollback()

            # Comprobamos si el DNI ya está registrado
            cliente_existente = (
                sesion.query(Cliente)
                .filter_by(dni=dni)
                .first()
            )

            if cliente_existente:
                mensaje_error = "Este DNI ya está registrado. Verificá el número ingresado."
            else:
                # Comprobamos si el email ya pertenece a otro cliente
                cliente_existente = (
                    sesion.query(Cliente)
                    .filter_by(email=email)
                    .first()
                ) if email else None

                if cliente_existente:
                    mensaje_error = "Este email ya está registrado."
                else:
                    mensaje_error = (
                        "No se pudo registrar el cliente. "
                        "Revisá los datos ingresados."
                    )

            # Volvemos al formulario conservando los datos ingresados
            return render_template(
                "nuevo_cliente.html",
                error=mensaje_error,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                email=email or ""
            )

        finally:
            # Cerramos la sesión
            sesion.close()

        # Volvemos a la lista de clientes si todo salió bien
        return redirect("/clientes")

    # Si simplemente entramos a la página, mostramos el formulario
    return render_template("nuevo_cliente.html")


# Creamos la ruta para editar un cliente existente
@app.route("/clientes/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar_cliente(cliente_id):

    # Abrimos una sesión con MySQL
    sesion = obtener_sesion()

    try:
        # Buscamos el cliente que queremos editar
        cliente = buscar_cliente(sesion, cliente_id)

        # Si el cliente no existe, volvemos a la lista
        if cliente is None:
            return redirect("/clientes")

        # Si enviamos el formulario, actualizamos los datos
        if request.method == "POST":

            # Obtenemos los datos enviados por el formulario
            dni = request.form["dni"].strip()
            telefono = request.form["telefono"].strip()
            email = request.form.get("email", "").strip() or None

            try:
                # Actualizamos los datos del cliente
                modificar_cliente(
                    sesion,
                    cliente_id,
                    dni,
                    telefono,
                    email
                )

            except ValueError as error:
                # Mostramos el formulario con el error de validación
                return render_template(
                    "editar_cliente.html",
                    cliente=cliente,
                    error=str(error)
                )

            except IntegrityError:
                # Deshacemos la operación si un dato único está repetido
                sesion.rollback()

                # Comprobamos si el DNI pertenece a otro cliente
                cliente_existente = (
                    sesion.query(Cliente)
                    .filter(
                        Cliente.dni == dni,
                        Cliente.id != cliente_id
                    )
                    .first()
                )

                if cliente_existente:
                    mensaje_error = "Este DNI ya está registrado por otro cliente."
                else:
                    # Comprobamos si el email pertenece a otro cliente
                    cliente_existente = (
                        sesion.query(Cliente)
                        .filter(
                            Cliente.email == email,
                            Cliente.id != cliente_id
                        )
                        .first()
                    ) if email else None

                    if cliente_existente:
                        mensaje_error = "Este email ya está registrado por otro cliente."
                    else:
                        mensaje_error = (
                            "No se pudieron guardar los cambios. "
                            "Revisá los datos ingresados."
                        )

                # Volvemos al formulario mostrando el error
                return render_template(
                    "editar_cliente.html",
                    cliente=cliente,
                    error=mensaje_error
                )

            # Si todo salió bien, volvemos a la lista
            return redirect("/clientes")

        # Mostramos el formulario con los datos actuales
        return render_template(
            "editar_cliente.html",
            cliente=cliente
        )

    finally:
        # Cerramos la sesión incluso si ocurre un error
        sesion.close()


# Creamos la ruta para eliminar un cliente
@app.route("/clientes/eliminar/<int:cliente_id>")
def eliminar_cliente(cliente_id):

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Eliminamos el cliente utilizando nuestro Service
    borrar_cliente(sesion, cliente_id)

    # Cerramos la sesión
    sesion.close()

    # Volvemos a la lista de clientes
    return redirect("/clientes")


# Creamos la ruta que muestra los vehículos registrados
@app.route("/vehiculos")
def vehiculos():

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Obtenemos los vehículos mediante nuestro Service
    lista_vehiculos = listar_vehiculos(sesion)

    # Renderizamos la página mientras la sesión todavía está abierta
    respuesta = render_template("vehiculos.html", vehiculos=lista_vehiculos)

    # Cerramos la sesión después de generar la página
    sesion.close()

    # Devolvemos la página al navegador
    return respuesta


#creamos la ruta para registrar vehículos
@app.route("/vehiculos/nuevo", methods=["GET", "POST"])
def nuevo_vehiculo():

    # Si enviamos el formulario
    if request.method == "POST":

        # Obtenemos los datos enviados por el formulario
        cliente_id = request.form["cliente_id"]
        patente = request.form["patente"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        anio = request.form["anio"]

        # Abrimos una sesión con la base de datos
        sesion = obtener_sesion()

        # Registramos el vehículo
        registrar_vehiculo(
            sesion,
            cliente_id,
            patente,
            marca,
            modelo,
            anio
        )

        # Cerramos la sesión
        sesion.close()

        # Volvemos a la lista de vehículos
        return redirect("/vehiculos")

    # Si entramos a la página por GET,
    # necesitamos obtener los clientes para mostrarlos en el select
    sesion = obtener_sesion()

    lista_clientes = listar_clientes(sesion)

    sesion.close()

    return render_template(
        "nuevo_vehiculo.html",
        clientes=lista_clientes
    )



# Creamos la ruta para editar un vehículo existente
@app.route("/vehiculos/editar/<int:vehiculo_id>", methods=["GET", "POST"])
def editar_vehiculo(vehiculo_id):

    # Abrimos una sesión con MySQL
    sesion = obtener_sesion()

    # Buscamos el vehículo que queremos editar
    vehiculo = buscar_vehiculo(sesion, vehiculo_id)

    # Si enviamos el formulario, actualizamos los datos
    if request.method == "POST":

        patente = request.form["patente"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        anio = request.form["anio"]

        modificar_vehiculo(
            sesion,
            vehiculo_id,
            patente,
            marca,
            modelo,
            anio
        )

        # Cerramos la sesión
        sesion.close()

        # Volvemos a la lista de vehículos
        return redirect("/vehiculos")

    # Cerramos la sesión después de obtener el vehículo
    sesion.close()

    # Mostramos el formulario con los datos actuales
    return render_template(
        "editar_vehiculo.html",
        vehiculo=vehiculo
    )



# Creamos la ruta para eliminar un vehículo
@app.route("/vehiculos/eliminar/<int:vehiculo_id>")
def eliminar_vehiculo(vehiculo_id):

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Eliminamos el vehículo utilizando nuestro Service
    borrar_vehiculo(sesion, vehiculo_id)

    # Cerramos la sesión
    sesion.close()

    # Volvemos a la lista de vehículos
    return redirect("/vehiculos")



# Mostramos todas las órdenes junto con sus servicios y repuestos asociados
@app.route("/ordenes")
def ordenes():

    # Abrimos una sesión con la base de datos
    sesion = obtener_sesion()

    # Obtenemos todas las órdenes de trabajo
    lista_ordenes = listar_ordenes(sesion)

    # Obtenemos los servicios asociados a las órdenes
    lista_orden_servicios = listar_orden_servicios(sesion)

    # Obtenemos el catálogo de servicios
    lista_servicios = listar_servicios(sesion)

    # Obtenemos los repuestos asociados a las órdenes
    lista_orden_repuestos = listar_orden_repuestos(sesion)

    # Obtenemos el catálogo de repuestos
    lista_repuestos = listar_repuestos(sesion)

    # Renderizamos la página y enviamos todos los datos que necesita
    respuesta = render_template(
        "ordenes.html",
        ordenes=lista_ordenes,
        orden_servicios=lista_orden_servicios,
        servicios=lista_servicios,
        orden_repuestos=lista_orden_repuestos,
        repuestos=lista_repuestos
    )

    # Cerramos la sesión con la base de datos
    sesion.close()

    # Devolvemos la página al navegador
    return respuesta


# Creamos la ruta para registrar una nueva orden de trabajo
@app.route("/ordenes/nuevo", methods=["GET", "POST"])
def nuevo_orden():

    # Si enviamos el formulario
    if request.method == "POST":

        # Obtenemos los datos enviados por el formulario
        vehiculo_id = request.form["vehiculo_id"]
        tipo_orden = request.form["tipo_orden"]
        fecha_ingreso = request.form["fecha_ingreso"]
        fecha_entrega = request.form["fecha_entrega"]
        tipo_servicio = request.form["tipo_servicio"]
        descripcion = request.form["descripcion"]
        estado = request.form["estado"]
        costo = request.form["costo"]

        # Creamos una sesión con MySQL
        sesion = obtener_sesion()

        # Registramos la orden utilizando nuestro Service
        registrar_orden(
            sesion,
            vehiculo_id,
            tipo_orden,
            fecha_ingreso,
            fecha_entrega,
            tipo_servicio,
            descripcion,
            estado,
            costo
        )

        # Cerramos la sesión
        sesion.close()

        # Volvemos a la lista de órdenes
        return redirect("/ordenes")



# Creamos la ruta para editar una orden existente
@app.route("/ordenes/editar/<int:orden_id>", methods=["GET", "POST"])
def editar_orden(orden_id):

    # Abrimos una sesión con MySQL
    sesion = obtener_sesion()

    try:
        # Buscamos la orden que queremos editar
        orden = buscar_orden(sesion, orden_id)

        # Si la orden no existe, volvemos a la lista de órdenes
        if orden is None:
            return redirect("/ordenes")

        # Si enviamos el formulario, actualizamos los datos
        if request.method == "POST":

            # Obtenemos los datos enviados por el formulario
            tipo_orden = request.form["tipo_orden"]
            fecha_entrega = request.form["fecha_entrega"] or None
            tipo_servicio = request.form["tipo_servicio"]
            descripcion = request.form["descripcion"]
            estado = request.form["estado"]
            costo = request.form["costo"]

            # Actualizamos la orden utilizando nuestro Service
            modificar_orden(
                sesion,
                orden_id,
                tipo_orden,
                fecha_entrega,
                tipo_servicio,
                descripcion,
                estado,
                costo
            )

            # Volvemos a la lista de órdenes
            return redirect("/ordenes")

        # Mostramos el formulario con los datos actuales
        return render_template(
            "editar_orden.html",
            orden=orden
        )

    finally:
        # Cerramos la sesión incluso si ocurre un error
        sesion.close()



# Creamos la ruta para consultar una orden sin modificarla
@app.route("/ordenes/<int:orden_id>")
def ver_orden(orden_id):

    # Abrimos una sesión con MySQL
    sesion = obtener_sesion()

    try:
        # Buscamos la orden solicitada
        orden = buscar_orden(sesion, orden_id)

        # Si la orden no existe, volvemos al listado
        if orden is None:
            return redirect("/ordenes")

        # Mostramos los detalles de la orden
        return render_template(
            "ver_orden.html",
            orden=orden
        )

    finally:
        # Cerramos la sesión incluso si ocurre un error
        sesion.close()



# Creamos la ruta para eliminar una orden
@app.route("/ordenes/eliminar/<int:orden_id>")
def eliminar_orden(orden_id):

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Eliminamos la orden utilizando nuestro Service
    borrar_orden(sesion, orden_id)

    # Cerramos la sesión
    sesion.close()

    # Volvemos a la lista de órdenes
    return redirect("/ordenes")


# Creamos la ruta que muestra los servicios registrados
@app.route("/servicios")
def servicios():

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Obtenemos los servicios mediante nuestro Service
    lista_servicios = listar_servicios(sesion)

    # Renderizamos la página mientras la sesión está abierta
    respuesta = render_template("servicios.html", servicios=lista_servicios)

    # Cerramos la sesión después de generar la página
    sesion.close()

    # Devolvemos la página al navegador
    return respuesta



# Creamos la ruta que muestra los repuestos registrados
@app.route("/repuestos")
def repuestos():

    # Creamos una sesión para conectarnos con MySQL
    sesion = obtener_sesion()

    # Obtenemos los repuestos mediante nuestro Service
    lista_repuestos = listar_repuestos(sesion)

    # Renderizamos la página mientras la sesión está abierta
    respuesta = render_template("repuestos.html", repuestos=lista_repuestos)

    # Cerramos la sesión después de generar la página
    sesion.close()

    # Devolvemos la página al navegador
    return respuesta


# Creamos la ruta para agregar un servicio a una orden
@app.route("/ordenes/<int:orden_id>/servicios/nuevo", methods=["GET", "POST"])
def nuevo_orden_servicio(orden_id):

    # Si enviamos el formulario
    if request.method == "POST":

        # Obtenemos los datos enviados por el formulario
        servicio_id = request.form["servicio_id"]
        cantidad = request.form["cantidad"]
        precio_unitario = request.form["precio_unitario"]

        # Creamos una sesión con MySQL
        sesion = obtener_sesion()

        # Registramos el servicio asociado a la orden
        registrar_orden_servicio(
            sesion,
            orden_id,
            servicio_id,
            cantidad,
            precio_unitario
        )

        # Cerramos la sesión
        sesion.close()

        # Volvemos a la lista de órdenes
        return redirect("/ordenes")

    # Si entramos por GET, obtenemos los servicios disponibles
    sesion = obtener_sesion()

    lista_servicios = listar_servicios(sesion)

    sesion.close()

    # Mostramos el formulario
    return render_template(
        "nuevo_orden_servicio.html",
        orden_id=orden_id,
        servicios=lista_servicios
    )


# Ruta para agregar un repuesto a una orden
@app.route("/ordenes/<int:orden_id>/repuestos/nuevo", methods=["GET", "POST"])
def nuevo_orden_repuesto(orden_id):

    sesion = obtener_sesion()

    if request.method == "POST":

        repuesto_id = request.form["repuesto_id"]
        cantidad = request.form["cantidad"]
        precio_unitario = request.form["precio_unitario"]

        registrar_orden_repuesto(
            sesion,
            orden_id,
            repuesto_id,
            cantidad,
            precio_unitario
        )

        sesion.close()

        return redirect("/ordenes")

    lista_repuestos = listar_repuestos(sesion)

    respuesta = render_template(
        "nuevo_orden_repuesto.html",
        orden_id=orden_id,
        repuestos=lista_repuestos
    )

    sesion.close()

    return respuesta

    

# Iniciamos el servidor
if __name__ == "__main__":
    app.run(debug=True, port=5001)