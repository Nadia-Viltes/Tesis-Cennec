from loguru import logger
from datetime import date
from controllerHome import obtener_lista_cumple
from controllerPaciente import *
from controllerReportes import *
from controllerUsuario import *
from controllerRol import *
from controllerTurno import *
from controllerHCD import *
from controllerMiAgenda import *
import json
from flask import Flask, render_template, render_template_string, redirect, url_for, request, jsonify, session, abort

app = Flask(__name__)
app.secret_key = "cennec_tesis"


def get_modulo_by_privilegio(privilegio):
    permisos = {
        "acceso_modulo_turno": "/turnos",
        "acceso_modulo_mi_agenda": "/agenda",
        "acceso_modulo_pacientes": "/pacientes",
        "acceso_modulo_historia_clinica_digital": "/hcd",
        "acceso_modulo_reportes": "/reportes",
        "acceso_modulo_configuraciones": "/configuracion"
    }
    return permisos[privilegio]


def asignar_modulo_a_la_session(id_usuario):
    privilegios = obtener_privilegios_por_id_usuario(id_usuario)
    privilegios_dict = {}
    for privilegio in privilegios:
        logger.info("privilegio[5] -> {}".format(privilegio[5]))
        privilegios_dict[privilegio[5]
                         ] = get_modulo_by_privilegio(privilegio[5])
    logger.info("privilegios_dict recien creado-> {}".format(privilegios_dict))
    session["privilegios"] = privilegios_dict


@app.errorhandler(404)
def page_not_found(error):
    logger.info("url -> {}".format(request.path))
    if "usuario" not in session:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("index"))


@app.before_request
def before_request():
    current_url = request.path
    if "usuario" not in session and "/login" not in current_url and "/static/" not in current_url:
        return redirect(url_for("login"))
    if "usuario" in session and "/login" not in current_url and "/static" not in current_url and "/home" not in current_url and "/logout" not in current_url:
        logger.info(
            "usuario logueado  y estos son los privilegios-> {}".format(session["privilegios"].values()))
        if("/" + current_url.split("/")[1] in session["privilegios"].values()) == False:
            logger.info(
                "logger privilegios -> {}".format(session["privilegios"].values()))
            abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form["usuario"]
        password = request.form["password"]
        datos_usuario = obtener_datos_usuario_by_user_password(
            usuario, password)
        logger.info("datos usuario -> {}".format(datos_usuario))
        if datos_usuario != None:
            session["usuario_id"] = datos_usuario[0]
            logger.info(
                "usuario_id session -> {}".format(session["usuario_id"]))
            session["usuario"] = datos_usuario[1]
            session["nombre"] = datos_usuario[2]
            session["apellido"] = datos_usuario[3]
            session["nombre_rol"] = datos_usuario[4]
            asignar_modulo_a_la_session(session["usuario_id"])
            return redirect(url_for("index"))
        else:
            return render_template("login.html", data="invalid")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/home')
def index(name='Home'):
    nombreSession = session["nombre"]
    apellidoSession = session["apellido"]
    cumple = obtener_lista_cumple()
    data = {
        'nombreSession': nombreSession,
        'apellidoSession': apellidoSession,
        'cumple': cumple
    }
    return render_template('index.html', data=data)

# MUESTRA LA LISTA DE PACIENTES Y BUSQUEDA


@app.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
    pacientes = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        parametros = '%' + '%'.join(parametros.split()) + '%'
        pacientes = obtener_pacientes_query(parametros)
    else:
        pacientes = obtener_pacientes()
    data = {
        'titulo': 'Pacientes',
        'pacientes': pacientes
    }
    return render_template('pacientes.html', data=data)

# Pantalla de AGREGAR PACIENTE


@app.route('/pacientes/agregar_paciente')
def agregar_paciente():
    tipoDoc = obtener_tipoDocumento()
    pais = obtener_pais()
    financiador = obtener_financiador()
    data = {
        'titulo': 'Agregar paciente',
        'tipoDocumento': tipoDoc,
        'pais': pais,
        'financiador': financiador
    }
    return render_template('pacientes_agregar.html', data=data)

# Chequea que no exista mismo numero de financiador


@app.route('/pacientes/chequear_financiador', methods=["POST"])
def chequear_financiador():
    financiador_id = request.form["financiador_id"]
    numero_afiliado = request.form["numero_afiliado"]
    chequea = chequear_financiador_nro_afiliado(
        financiador_id, numero_afiliado)
    return jsonify({'chequea': chequea})

# Chequea que el DNI no exista en la base


@app.route('/pacientes/chequear_documento', methods=["POST"])
def chequear_documento():
    documento = request.form["documento"]
    chequea = chequear_documento_existente(documento)
    return jsonify({'chequea': chequea})

# Acción para cargar las provincias en dropdown una vez seleccionado el país


@app.route('/pacientes/provincias_dropdown/<int:id>')
def provincias_pais_dropdown(id):
    provincias = obtener_provincias_by_id_pais(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for provincia in provincias:
        options += "<option value={}>{}</option>".format(
            provincia[0], provincia[1])
    return jsonify({'htmlresponse': render_template_string(options)})

# Acción para cargar las localidades en dropdown una vez seleccionado la provincia


@app.route('/pacientes/localidades_dropdown/<int:id>')
def localidades_provincia_dropdown(id):
    localidades = obtener_localidades_by_id_provincia(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for localidad in localidades:
        options += "<option value={}>{}</option>".format(
            localidad[0], localidad[1])
    return jsonify({'htmlresponse': render_template_string(options)})

# Carga los barrios del dropdown pacientes


@app.route('/pacientes/barrios_dropdown/<int:id>')
def barrios_localidad_dropdown(id):
    barrios = obtener_barrios_by_id_localidad(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for barrio in barrios:
        options += "<option value={}>{}</option>".format(barrio[0], barrio[1])
    return jsonify({'htmlresponse': render_template_string(options)})

# FUNCIÓN PARA QUE GUARDE LOS DATOS DEL PACIENTE NUEVO


@app.route("/pacientes/guardar_paciente", methods=["POST"])
def guardar_paciente():
    nombrePaciente = request.form["nombrePaciente"]
    apellidoPaciente = request.form["apellidoPaciente"]
    genero = request.form["genero"]
    tipoDocumento = request.form["tipoDocumento"]
    nroDocumento = request.form["nroDocumento"]
    fechaNacimiento = request.form["fechaNacimiento"]
    pais = request.form["pais"]
    provincia = request.form["provincia"]
    localidad = request.form["localidad"]
    calle = request.form["calle"]
    altura = request.form["altura"]
    piso = request.form["piso"]
    dpto = request.form["dpto"]
    barrio = request.form["barrio"]
    nombreTutor = request.form["nombreTutor"]
    apellidoTutor = request.form["apellidoTutor"]
    ocupacion = request.form["ocupacion"]
    nroCelular = request.form["nroCelular"]
    nroFijo = request.form["nroFijo"]
    financiador = request.form["financiador"]
    nroAfiliado = request.form["nroAfiliado"]
    idDomicilio = insertar_domicilio(
        pais, provincia, localidad, barrio, calle, altura, piso, dpto)
    idTutoria = insertar_tutor(
        nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
    idPaciente = insertar_paciente(nombrePaciente, apellidoPaciente, genero,
                                   tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, idTutoria)
    insertar_HCD(idPaciente)
    insertar_afiliacion(idPaciente, financiador, nroAfiliado)
    # SI DA OK redireccionar
    return redirect("/pacientes")

# pantalla de EDITAR PACIENTE


@app.route('/pacientes/editar_paciente/<int:id>')
def obtener_paciente_id(id):
    paciente = obtener_paciente_por_id(id)
    tipoDocumento = obtener_tipoDocumento()
    pais = obtener_pais()
    provincias = obtener_provincias_by_id_pais(pais[0])
    logger.info("provincias -> {}".format(provincias))
    localidades = obtener_localidades_by_id_provincia(paciente[10])
    logger.info("localidades -> {}".format(localidades))
    barrios = obtener_barrios_by_id_localidad(paciente[12])
    logger.info("barrios -> {}".format(barrios))
    financiador = obtener_financiador()
    data = {
        'titulo': 'Editar paciente',
        'pacientes': paciente,
        'tipoDocumento': tipoDocumento,
        'pais': pais,
        'provincias': provincias,
        'localidades': localidades,
        'barrios': barrios,
        'financiador': financiador
    }
    return render_template("pacientes_editar.html", data=data)

# Acción para guardar las actualizaciones del editar PACIENTE


@app.route("/pacientes/actualizar_paciente", methods=["POST"])
def actualizar_pacientes():
    idPaciente = request.form["idPaciente"]
    nombrePaciente = request.form["nombrePaciente"]
    apellidoPaciente = request.form["apellidoPaciente"]
    genero = request.form["genero"]
    tipoDocumento = request.form["tipoDocumento"]
    nroDocumento = request.form["nroDocumento"]
    fechaNacimiento = request.form["fechaNacimiento"]
    pais = request.form["pais"]
    provincia = request.form["provincia"]
    localidad = request.form["localidad"]
    calle = request.form["calle"]
    altura = request.form["altura"]
    piso = request.form["piso"]
    dpto = request.form["dpto"]
    barrio = request.form["barrio"]
    nombreTutor = request.form["nombreTutor"]
    apellidoTutor = request.form["apellidoTutor"]
    ocupacion = request.form["ocupacion"]
    nroCelular = request.form["nroCelular"]
    nroFijo = request.form["nroFijo"]
    financiador = request.form["financiador"]
    nroAfiliado = request.form["nroAfiliado"]
    actualizar_domicilio(pais, provincia, localidad, barrio,
                         calle, altura, piso, dpto, idPaciente)
    actualizar_tutoria(nombreTutor, apellidoTutor, ocupacion,
                       nroFijo, nroCelular, idPaciente)
    actualizar_afiliacion(financiador, nroAfiliado, idPaciente)
    actualizar_paciente(nombrePaciente, apellidoPaciente, genero,
                        tipoDocumento, nroDocumento, fechaNacimiento, idPaciente)
    return redirect("/pacientes")


@app.route('/hcd', methods=['GET', 'POST'])
def hcd():
    hcd = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        parametros = '%' + '%'.join(parametros.split()) + '%'
        hcd = obtener_lista_hcd_query(parametros)
    else:
        hcd = obtener_lista_hcd()
    data = {
        'titulo': 'Historia Clínica Dígital',
        'hcd': hcd
    }
    return render_template('hcd.html', data=data)


@app.route('/hcd/ver_admision/<int:id>', methods=["GET", "POST"])
def obtener_hcd_idd(id):
    paciente_hcd = obtener_hcd_por_id(id)
    IdEspecialidad = obtener_especialidad(id)
    turnosadm = obtener_lista_turnos_admision(id)
    values = {
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd,
        'especialidad': IdEspecialidad,
        'turnosadm': turnosadm
    }
    return render_template('hcd_ver_admision.html', data=values)


@app.route('/hcd/ver_admision/carga_patologia_especialidad/<int:id>')
def patologia_especialidad(id):
    patologias = obtener_patologia_por_especialidad_id(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for patologia in patologias:
        options += "<option value={}>{}</option>".format(
            patologia[0], patologia[1])
    return jsonify({'htmlresponse': render_template_string(options)})

# Acá se abre el modal de eliminar turno de admisión


@app.route('/hcd/modal_eliminar_turno_admision/<int:id>')
def modal_eliminar_turno_admision(id):
    boton = boton_turno_adm(id)
    values = {
        'titulo': 'Eliminar turno admisión',
        'boton': boton
    }
    return jsonify({'htmlresponse': render_template('hcd_ver_admision_eliminar_turno.html', data=values)})

# Acá se ejecuta la query para eliminar el turno de admisión


@app.route("/hcd/eliminar_turno_admision/", methods=["POST"])
def eliminar_turno_admision():
    dataTurnoAdmId = request.form["dataTurnoAdmId"]
    update_baja_turno_admision(dataTurnoAdmId)
    return redirect("/hcd")


@app.route('/hcd/ver_evoluciones/<int:id>', methods=["POST", "GET"])
def obtener_evolucion_id(id):
    paciente_hcd = obtener_hcd_por_id(id)
    historial_hcd = obtener_historial_evoluciones(id)
    usuario = session["usuario_id"]
    usuario_profesional = obtener_datos_usuario_profesional(usuario)
    values = {
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd,
        'historial': historial_hcd,
        'usuarioProfesional': usuario_profesional
    }
    return render_template('hcd_ver_evolucion.html', data=values)


@app.route('/hcd/modal/ver_historial/<int:id>')
def ver_historial_hcd(id):
    # historial_hcd -> modificarlo para que obtenga el detalle
    detalle_historial = obtener_detalle_historial(id)
    usuarioprof = session["usuario_id"]
    values = {
        'titulo': 'Detalle de historia clínica',
        'detalle_historial': detalle_historial,
        'usuarioprof': usuarioprof
    }
    return jsonify({'htmlresponse': render_template('hcd_ver_historial.html', data=values)})

# Carga los turnos admision llenando la tabla con jquery


@app.route('/hcd/agrega_turnos_admision', methods=["POST"])
def agrega_turnos_admision():
    # tomo los datos que vienen del form
    id_paciente = request.form['idPaciente']
    id_especialidad = request.form['idEspecialidad']
    cantidad = request.form['cantidad']
    id_patologia = request.form['idPatologia']
    # inserto los datos en configuracion de turno
    insertar_turnos_admision(
        id_paciente, id_especialidad, id_patologia, cantidad)
    # hago la consulta para obtener todos los turnos por id de paciente por especialidad
    lista_turnos = obtener_lista_turnos_admision(id_paciente)
    logger.info("Esta es la lista de turnos admisión -> {}".format(lista_turnos))
    table = ""
    # creo una tabla con los datos de la lista de turnos y se la envío
    # a ver_HCD.html
    for turno in lista_turnos:
        boton = ""
        if turno[2] > 0:
            boton = """<td><button type="button" class="btn btn-danger" name="button_eliminar_turAdm" id={} disabled>Eliminar</button></td>""".format(
                turno[0])
        else:
            boton = """<td><button type="button" class="btn btn-danger" name="button_eliminar_turAdm" id={}>Eliminar</button></td>""".format(
                turno[0])
        table += """<tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    {}
                    </tr>""".format(
            turno[1], turno[2], turno[4], boton)
    return jsonify({'htmlresponse': render_template_string(table)})


@app.route('/agenda')
def agenda():
    usuario = session["usuario_id"]
    mi_agenda = None
    if validar_usuario_admin(session["usuario"]):
        mi_agenda = obtener_lista_turno_mi_agenda_adm()
    else:
        mi_agenda = obtener_lista_turno_mi_agenda(usuario)
    data = {
        'titulo': 'Mi Agenda',
        'turnoprof': mi_agenda
    }
    return render_template('mi_agenda.html', data=data)

# Acá se abre el modal de iniciar atención


@app.route('/agenda/modal_iniciar_turno/<int:id>')
def Iniciar_turno(id):
    IdTurno = obtener_turno_por_id(id)
    values = {
        'titulo': 'Iniciar atención',
        'IdTurno': IdTurno
    }
    return jsonify({'htmlresponse': render_template('mi_agenda_inicio_atencion.html', data=values)})

# Acá se ejecuta la query para agregar un turno en estado atendiendos


@app.route("/agenda/iniciar_atencion", methods=["POST"])
def iniciar_atencion():
    usuario = session["usuario_id"]
    idTurno = request.form["dataTurnoId"]
    idTurno_receptar = obtener_turno_agenda_receptado(idTurno)
    id_estado = obtener_id_estado_turno_por_estado("Atendiendo")
    insertar_turno_atendiendo(idTurno_receptar[0], idTurno_receptar[1], idTurno_receptar[2], idTurno_receptar[3],
                              idTurno_receptar[4], idTurno_receptar[5], id_estado, usuario, idTurno_receptar[6], idTurno_receptar[7])
    update_turno_asignado(idTurno)
    return redirect("/agenda")

# Acá se abre el modal de finalizar atención


@app.route('/agenda/modal_finalizar_turno/<int:id>')
def finalizar_turno(id):
    tiene_detalle = validar_tiene_detalle_evolucion_turno(id)
    values = {
        'titulo': 'Finalizar atención',
        'IdTurno': id,
        'tiene_detalle': tiene_detalle
    }
    return jsonify({'htmlresponse': render_template('mi_agenda_finalizar_atencion.html', data=values)})

# Acá se ejecuta la query para agregar un turno en estado atendido


@app.route("/agenda/finalizar_atencion", methods=["POST"])
def finalizar_atencion():
    usuario = session["usuario_id"]
    idTurno = request.form["dataTurnoId"]
    idTurno_atendiendo = obtener_turno_agenda_receptado(idTurno)
    id_estado = obtener_id_estado_turno_por_estado("Atendido")
    insertar_turno_atendido(idTurno_atendiendo[0], idTurno_atendiendo[1], idTurno_atendiendo[2], idTurno_atendiendo[3],
                            idTurno_atendiendo[4], idTurno_atendiendo[5], id_estado, usuario, idTurno_atendiendo[6], idTurno_atendiendo[7])
    update_turno_asignado(idTurno)
    return redirect("/agenda")


@app.route('/agenda/ver_hcd/paciente/<int:idpaciente>/turno/<int:idturno>', methods=["GET", "POST"])
def ver_hcd(idpaciente, idturno):
    paciente_hcd = obtener_hcd_por_id(idpaciente)
    historial_hcd = obtener_historial_evoluciones(idpaciente)
    turnoId = obtener_turno_atendiendo(idturno)
    detalleTurno = obtener_detalle_con_turno(idturno)
    tiene_detalle = validar_tiene_detalle_evolucion_turno(idturno)
    usuario = session["usuario_id"]
    usuario_profesional = obtener_datos_usuario_profesional(usuario)
    values = {
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd,
        'historial': historial_hcd,
        'usuarioProfesional': usuario_profesional,
        'turno_id': turnoId,
        'detalleTurno': detalleTurno,
        'tiene_detalle': tiene_detalle
    }
    return render_template('mi_agenda_ver_hcd.html', data=values)


@app.route('/agenda/guardar_detalle', methods=["GET", "POST"])
def guardar_detalle():
    usuario = session["usuario_id"]
    inputProfesional = request.form['inputProfesional']
    InputTextareaEvoluciones = request.form['InputTextareaEvoluciones']
    inputIdHCD = request.form['inputIdHCD']
    evolucion = consulta_existe_evolucion(inputIdHCD)
    inputIdTurno = request.form['inputIdTurno']
    if evolucion == None:
        idEvolucion = insertar_evolucion(inputIdHCD, usuario)
        insertar_detalle(idEvolucion, inputIdTurno,
                         inputProfesional, InputTextareaEvoluciones, usuario)
    else:
        insertar_detalle(evolucion, inputIdTurno,
                         inputProfesional, InputTextareaEvoluciones, usuario)
    # SI DA OK redireccionar
    return redirect("/agenda")


@app.route('/agenda/ver_historial/<int:id>')
def ver_historial(id):
    detalle_historial = obtener_detalle_historial(id)
    usuario = session["usuario_id"]
    usuarioprof = obtener_id_profesional(usuario)
    values = {
        'titulo': 'Detalle de historia clínica',
        'detalle_historial': detalle_historial,
        'usuarioprof': usuarioprof
    }
    return jsonify({'htmlresponse': render_template('mi_agenda_historial.html', data=values)})

# Operación para editar el detalle


@app.route('/agenda/editar_detalle', methods=["POST"])
def editar_detalle():
    usuario = session["usuario_id"]
    inputIdDetEvo = request.form['inputIdDetEvo']
    inputIdEvolucion = request.form['inputIdEvolucion']
    inputIdTurnoHis = request.form['inputIdTurnoHis']
    inputProfesionalHis = request.form['inputProfesionalHis']
    InputTextareaEvolucionesHis = request.form['InputTextareaEvolucionesHis']
    actualizar_detalle(inputIdEvolucion, inputIdTurnoHis, inputProfesionalHis,
                       InputTextareaEvolucionesHis, usuario, inputIdDetEvo)
    # SI DA OK redireccionar
    return redirect("/agenda")

# Operación para mostrar la lista de turnos


@app.route('/turnos', methods=["GET", "POST"])
def turnos():
    turnos = None
    estado = None
    if request.method == 'POST':
        estado = request.form['estadosSelect']
        turnos = obtener_lista_turnos_por_estado(
            estado) if estado != "todos" else obtener_lista_turno()
    else:
        turnos = obtener_lista_turno()
    filtro = obtener_estado_filtro()
    data = {
        'titulo': 'Turnos',
        'turnos': turnos,
        'filtro': filtro,
        'estado_seleccionado': estado
    }
    return render_template('turnos.html', data=data)

# Acción para ver la pantalla de asignar turno
# aca


@app.route('/turnos/asignar_turno/<int:id>')
def asignar_turno(id):
    paciente = obtener_paciente_por_id(id)
    tipoTurno = obtener_tipoTurno()
    especialidad = obtener_especialidad_turnos(id)
    turnosadm = obtener_lista_turnos_admision(id)
    values = {
        'titulo': 'Asignar turno',
        'subtitulo': 'Seleccionar turno',
        'paciente': paciente,
        'tipoTurno': tipoTurno,
        'especialidad': especialidad,
        'turnosadm': turnosadm
    }
    return render_template('turnos_asignar.html', data=values)


@app.route('/turnos/chequear_disponibilidad', methods=["POST"])
def chequear_disponibilidad_turno():
    logger.info("ingreso a chequear disponibilidad")
    logger.info(
        "request profesionalId -> {}".format(request.form['profesionalId']))
    logger.info("request fechaTurno -> {}".format(request.form['fechaTurno']))
    logger.info("request horaInicio -> {}".format(request.form['horaInicio']))
    id_paciente = request.form['pacienteId']
    id_profesional = request.form['profesionalId']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['horaInicio']
    horario_paciente_ocupado = chequea_horario_ocupado_paciente(
        id_paciente, fecha_turno, hora_inicio)
    horario_profesional_ocupado = chequear_turno_existente(
        id_profesional, fecha_turno, hora_inicio)
    values = {
        "horario_profesional_ocupado": horario_profesional_ocupado,
        "horario_paciente_ocupado": horario_paciente_ocupado
    }
    return jsonify({'values': values})


@app.route('/turnos/grabar_turno', methods=["POST"])
def grabar_turno():
    usuario = session["usuario_id"]
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    # busco el id del turno asignado
    id_estado = obtener_id_estado_turno_por_estado("asignado")
    # inserto los datos en turno
    insertar_turno_asignado(id_tipo_turno, id_especialidad, id_profesional,
                            id_paciente, fecha_turno, hora_inicio, hora_fin, id_estado, usuario)
    # Le sumo los turnos computados así continuamos con la logica de los turnos para asignar
    id_configturno = obtener_id_configuracion_turno(
        id_paciente, id_especialidad)
    actualizar_turnos_computados(id_configturno)
    return redirect("/turnos")

# Acción para cargar de Profesionales en dropdown una vez seleccionada la especialidad


@app.route('/turnos/profesionales_dropdown/<int:id>')
def profesionales_especialidad_dropdown(id):
    profesionales = obtener_profesionales_especialidad(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for profesional in profesionales:
        options += "<option value={}>{} {}</option>".format(
            profesional[0], profesional[1], profesional[2])
    return jsonify({'htmlresponse': render_template_string(options)})

# Acción para ver la pantalla de seleccionar el paciente en asignar turnos
# Acción para abrir el modal para buscar un paciente


@app.route('/turnos/seleccionar_paciente', methods=['GET', 'POST'])
def buscar_paciente():
    pacientes = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        pacientes = obtener_pacientes_query(parametros)
    else:
        pacientes = obtener_pacientes()
    values = {
        'titulo': 'Asignar turno',
        'subtitulo': 'Seleccionar paciente',
        'pacientes': pacientes
    }
    return render_template('turnos_seleccionar_paciente.html', data=values)

# Acción para ver la pantalla de RECEPTAR turno


@app.route('/turnos/receptar_turno/<int:id_turno>')
def receptar_turno(id_turno):
    turno = obtener_turno_por_id(id_turno)
    id_paciente = turno[5]
    id_especialidad = turno[11]
    id_profesional_actual = turno[13]
    profesional_actual = [id_profesional_actual, turno[14], turno[15]]
    paciente = obtener_paciente_por_id(id_paciente)
    profesionales = obtener_profesionales_especialidad(id_especialidad)
    profesionales_filtrados = [
        x for x in profesionales if x[0] != id_profesional_actual]
    data = {
        'titulo': 'Receptar turno',
        'turno': turno,
        'paciente': paciente,
        'profesionales': profesionales_filtrados,
        'profesional_actual': profesional_actual
    }
    return render_template('turnos_receptar.html', data=data)


@app.route('/turnos/grabar_turno_receptado', methods=["POST"])
def grabar_turno_receptado():
    # tomo los datos que vienen del form
    usuario = session["usuario_id"]
    id_turno_asignado = request.form['idTurnoAsignar']
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    # busco el id del turno asignado
    id_estado = obtener_id_estado_turno_por_estado("Receptado")
    # inserto los datos en turno
    update_turno_asignado(id_turno_asignado)
    insertar_turno_receptado(id_tipo_turno, id_especialidad, id_paciente, fecha_turno,
                             hora_inicio, hora_fin, id_estado, usuario, id_profesional, id_turno_asignado)
    return redirect("/turnos")

# Acción para ver la pantalla de REPROGRAMAR turno


@app.route('/turnos/reprogramar_turno/<int:id_turno>')
def reprogramar_turno(id_turno):
    turno = obtener_turno_por_id(id_turno)
    id_paciente = turno[5]
    id_especialidad = turno[11]
    id_profesional_actual = turno[13]
    profesional_actual = [id_profesional_actual, turno[14], turno[15]]
    paciente = obtener_paciente_por_id(id_paciente)
    profesionales = obtener_profesionales_especialidad(id_especialidad)
    profesionales_filtrados = [
        x for x in profesionales if x[0] != id_profesional_actual]
    data = {
        'titulo': 'Reprogramar turno',
        'turno': turno,
        'paciente': paciente,
        'profesionales': profesionales_filtrados,
        'profesional_actual': profesional_actual
    }
    return render_template('turnos_reprogramar.html', data=data)


@app.route('/turnos/grabar_turno_reprogramado', methods=["POST"])
def grabar_turno_reprogramado():
    # tomo los datos que vienen del form
    usuario = session["usuario_id"]
    id_turno_asignado = request.form['idTurnoAsignar']
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    # busco el id del estado del turno en asignado
    id_estado = obtener_id_estado_turno_por_estado("Asignado")
    # inserto los datos en turno
    update_turno_reasignado(id_turno_asignado)
    insertar_turno_reasignado(id_tipo_turno, id_especialidad, id_profesional, id_paciente,
                              fecha_turno, hora_inicio, hora_fin, id_estado, id_turno_asignado, usuario)
    return redirect("/turnos")

# Acción para abrir el modal de ANULAR turno


@app.route('/turnos/anular_turno/<int:id_turno>')
def anular_turno(id_turno):
    turno = obtener_turno_por_id(id_turno)
    id_paciente = turno[5]
    paciente = obtener_paciente_por_id(id_paciente)
    turnos_para_anular = obtener_lista_de_turnos_para_anular(id_paciente)
    motivo_turno = obtener_motivoTurno()
    data = {
        'titulo': 'Reprogramar turno',
        'turno': turno,
        'paciente': paciente,
        'turnos_para_anular': turnos_para_anular,
        'motivoTurno': motivo_turno
    }
    return render_template('turnos_anular.html', data=data)


@app.route('/turnos/guardar_anular_turnos', methods=["POST"])
def guardar_anular_turnos():
    usuario = session["usuario_id"]
    motivoTurnosAnulados = request.form["motivoTurno"]
    listaTurnosAnulados = request.form.getlist('lista_turnos_para_anular')
    # busco el id del estado del turno en asignado
    id_estado = obtener_id_estado_turno_por_estado("Anulado")
    for idTurnosAnulados in listaTurnosAnulados:
        datos_turnos_para_anular = obtener_turno_por_id_asignado_anulado(
            idTurnosAnulados)
        insertar_anular_turno(datos_turnos_para_anular[1], datos_turnos_para_anular[2], datos_turnos_para_anular[3], datos_turnos_para_anular[4],
                              datos_turnos_para_anular[5], datos_turnos_para_anular[6], datos_turnos_para_anular[7], id_estado, motivoTurnosAnulados, usuario, idTurnosAnulados)
        update_turno_asignado(idTurnosAnulados)
    print("estos son los turnos para anular checkeados {}".format(
        request.form.getlist('lista_turnos_para_anular')))
    # SI DA OK redireccionar
    return redirect("/turnos")


@app.route('/configuracion/usuarios_rol/setear_privilegios_rol_seleccionado', methods=["POST"])
def setear_privilegios():
    # tomo los datos del rol
    id_rol = request.form['idRol']
    privilegios = obtener_privilegio_por_id_rol(id_rol)
    print("estos son los privilegios -> {}".format(privilegios))
    return jsonify({'privilegios': privilegios})


@app.route("/configuracion/usuarios/chequear_usuario_existente", methods=["POST"])
def chequear_usuario():
    nombre_usuario = request.form['nombre_usuario']
    chequea = chequear_usuario_existente_by_nombre(nombre_usuario)
    return jsonify({'chequea': chequea})


@app.route('/configuracion/rol', methods=['GET', 'POST'])
def configuracion_roles():
    rol = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        parametros = '%' + '%'.join(parametros.split()) + '%'
        rol = obtener_roles_query(parametros)
    else:
        rol = obtener_lista_roles()
    data = {
        'titulo': 'Configuración de roles',
        'rol': rol
    }
    return render_template('rol.html', data=data)


@app.route('/configuracion/agregar_rol')
def agregar_rol():
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'Agregar rol',
        'privilegios': privilegios
    }
    return render_template('rol_agregar.html', data=data)


@app.route('/configuracion/rol/guardar_rol', methods=["POST"])
def guardar_rol():
    nombreRol = request.form["nombreRol"]
    descripcionRol = request.form["descripcionRol"]
    idPrivilegios = request.form.getlist('privilegio_nombre')
    idRol = insertar_rol(nombreRol, descripcionRol)
    for idPrivilegio in idPrivilegios:
        insertar_rol_privilegio(idRol, idPrivilegio)
    logger.info("estos son los privilegios checkeados {}".format(
        request.form.getlist('privilegio_nombre')))
    # SI DA OK redireccionar
    return redirect("/configuracion/rol")


@app.route('/configuracion/rol/editar_rol/<int:id>', methods=["GET", "POST"])
def editar_rol(id):
    if request.method == 'POST':
        nombre_rol = request.form["nombreRol"]
        descripcion_rol = request.form["descripcionRol"]
        id_privilegios = request.form.getlist('privilegio_nombre')
        update_nombre_descripcion_rol_by_id_rol(
            id, nombre_rol, descripcion_rol)
        update_eliminar_rolprivilegio(id)
        for id_privilegio in id_privilegios:
            insertar_rol_privilegio(id, id_privilegio)
        return redirect("/configuracion/rol")
    IdRol = obtener_id_rol(id)
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'Editar rol',
        'IdRol': IdRol,
        'privilegios': privilegios
    }
    return render_template('rol_editar.html', data=data)

# Acá se abre el modal de eliminar rol


@app.route('/configuracion/rol/modal_eliminar_rol/<int:id>')
def eliminar_rol_id(id):
    IdRol = obtener_id_rol(id)
    privilegios = obtener_lista_privilegios()
    values = {
        'titulo': 'Eliminar rol',
        'IdRol': IdRol,
        'privilegios': privilegios
    }
    return jsonify({'htmlresponse': render_template('rol_eliminar.html', data=values)})

# Acá se ejecuta la query para dar de baja el rol


@app.route("/configuracion/rol/delete_rol", methods=["POST"])
def delete_rol():
    idRol = request.form["dataRolId"]
    update_eliminar_rol(idRol)
    update_eliminar_rolprivilegio(idRol)
    return redirect("/configuracion/rol")


@app.route('/configuracion/usuarios', methods=['GET', 'POST'])
def configuracion_usuarios():
    usuarios = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        parametros = '%' + '%'.join(parametros.split()) + '%'
        usuarios = obtener_lista_usuarios_query(parametros)
    else:
        usuarios = obtener_lista_usuarios()
    data = {
        'titulo': 'Configuración de usuarios',
        'usuario': usuarios
    }
    return render_template('usuarios.html', data=data)


@app.route('/configuracion/usuarios/seleccionar_recurso', methods=['GET', 'POST'])
def seleccionar_recurso():
    recursos = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        parametros = '%' + '%'.join(parametros.split()) + '%'
        recursos = obtener_recursos_nombre_apellido_dni(parametros)
    else:
        recursos = obtener_lista_recursos()
    data = {
        'titulo': 'Crear usuario',
        'subtitulo': 'Seleccionar recurso',
        'recursos': recursos
    }
    return render_template('usuarios_seleccionar_recurso.html', data=data)

# Acción para ver la pantalla de agregar usuario


@app.route('/configuracion/usuarios/agregar_usuario/<int:id>')
def agregar_usuario(id):
    recurso = obtener_recurso_por_id(id)
    rol = obtener_lista_roles()
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'Crear usuario',
        'subtitulo': 'Datos de autenticación',
        'recurso': recurso,
        'rol': rol,
        'privilegios': privilegios
    }
    return render_template('usuario_agregar.html', data=data)

# Acción para guardar el usuario


@app.route('/configuracion/usuarios/grabar_usuario', methods=["POST"])
def grabar_usuario():
    idRecurso = request.form["inputRecursoId"]
    nombreUsuario = request.form["NombreUsuarioInput"]
    contrasena = request.form["inputPasswordUsuario"]
    rolSeleccionado = request.form["checkRol"]
    guardar_usuario(idRecurso, nombreUsuario, contrasena, rolSeleccionado)
    # SI DA OK redireccionar
    return redirect("/configuracion/usuarios")


@app.route('/configuracion/usuarios/editar_usuario/<int:id>', methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == 'POST':
        password = request.form["inputPasswordUsuario"]
        rol_seleccionado = request.form["checkRol"]
        update_rol_pass_by_id_usuario(rol_seleccionado, password, id)
        return redirect("/configuracion/usuarios")
    usuario = obtener_usuario_por_id(id)
    recurso = obtener_recurso_por_id_usuario(id)
    roles = obtener_lista_roles()
    rol_seleccionado = obtener_rol_by_usuario_id(id)
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'Editar usuario',
        'usuario': usuario,
        'recurso': recurso,
        'roles': roles,
        'privilegios': privilegios,
        'rol_seleccionado': rol_seleccionado
    }
    return render_template('usuario_editar.html', data=data)

# Acción para abrir el modal eliminar usuario


@app.route('/configuracion/usuarios/modal_eliminar_usuario/<int:id>')
def eliminar_usuario_id(id):
    IdUsuario = obtener_usuario_por_id(id)
    values = {
        'titulo': 'Eliminar usuario',
        'IdUsuario': IdUsuario
    }
    return jsonify({'htmlresponse': render_template('usuario_eliminar.html', data=values)})


@app.route("/configuracion/usuarios/delete_usuario", methods=["POST"])
def delete_usuario():
    idUsuario = request.form["dataUsuarioId"]
    update_eliminar_usuario(idUsuario)
    return redirect("/configuracion/usuarios")


@app.route('/reportes')
def reportes():
    data = {
        'titulo': 'Reportes',
    }
    return render_template('reportes.html', data=data)


@app.route('/reportes/estados_turnos', methods=["GET", "POST"])
def reportes_estados_turnos():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    estados_turnos = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        estados_turnos = obtener_estados_turnos(fecha_desde, fecha_hasta)
    else:
        estados_turnos = obtener_estados_turnos(fecha_desde, fecha_hasta)
    valores_columnas = []
    nombre_columnas = []
    totales = 0
    for estados_turno in estados_turnos:
        totales += estados_turno[0]
        valores_columnas.append(estados_turno[0])
        nombre_columnas.append(estados_turno[1])
    periodos_turnos = obtener_periodos()
    data = {
        'titulo': 'Estados de turnos',
        'estados_turnos': estados_turnos,
        'periodos_turnos': periodos_turnos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombres_columnas': json.dumps(nombre_columnas, ensure_ascii=False),
        'valores_columnas': valores_columnas,
        'total': totales
    }
    return render_template('reportes_estados_turnos.html', data=data)


@app.route('/reportes/motivos_anulacion_turnos', methods=["GET", "POST"])
def reportes_movitos_anulacion_turnos():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    motivos_anulacion = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        motivos_anulacion = obtener_motivos_anulacion(fecha_desde, fecha_hasta)
    else:
        motivos_anulacion = obtener_motivos_anulacion(fecha_desde, fecha_hasta)
    valores_categorias = []
    nombre_categorias = []
    totales = 0
    for motivo_anulacion in motivos_anulacion:
        totales += motivo_anulacion[0]
        valores_categorias.append(motivo_anulacion[0])
        nombre_categorias.append(motivo_anulacion[1])
    data = {
        'titulo': 'Motivos Anulacion',
        'motivos_anulacion_turnos': motivos_anulacion,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': valores_categorias,
        'total': totales
    }
    return render_template('reportes_motivo_anulacion.html', data=data)


@app.route('/reportes/ranking_obras_sociales', methods=["GET", "POST"])
def reportes_ranking_obras_sociales():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    ranking_obras_sociales = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        ranking_obras_sociales = obtener_ranking_obras_sociales(
            fecha_desde, fecha_hasta)
    else:
        ranking_obras_sociales = obtener_ranking_obras_sociales(
            fecha_desde, fecha_hasta)
    valores_categorias = []
    nombre_categorias = []
    totales = 0
    for ranking in ranking_obras_sociales:
        totales += ranking[0]
        valores_categorias.append(ranking[0])
        nombre_categorias.append(ranking[1])
    data = {
        'titulo': 'Ranking Obras Sociales',
        'ranking_obras_sociales': ranking_obras_sociales,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': valores_categorias,
        'total': totales
    }
    return render_template('reportes_ranking_obra_social.html', data=data)


@app.route('/reportes/obtener_turnos_especialidad', methods=["GET", "POST"])
def reportes_turnos_especialidad():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    turnos_especialidad = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        turnos_especialidad = obtener_turnos_por_especialidad(
            fecha_desde, fecha_hasta)
    else:
        turnos_especialidad = obtener_turnos_por_especialidad(
            fecha_desde, fecha_hasta)
    valores_categorias = []
    nombre_categorias = []
    totales = 0
    for turnos in turnos_especialidad:
        totales += turnos[0]
        valores_categorias.append(turnos[0])
        nombre_categorias.append(turnos[1])
    data = {
        'titulo': 'Turnos por especialidad',
        'turnos_especialidad': turnos_especialidad,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': valores_categorias,
        'total': totales
    }
    return render_template('reportes_atencion_especialidad.html', data=data)


@app.route('/reportes/atencion_profesional', methods=["GET", "POST"])
def reportes_atencion_profesional():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    atencion_profesional = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        atencion_profesional = obtener_atencion_profesional(
            fecha_desde, fecha_hasta)
    else:
        atencion_profesional = obtener_atencion_profesional(
            fecha_desde, fecha_hasta)
    nombre_categorias = []
    totales = 0
    for atencion in atencion_profesional:
        totales += atencion[0]
        nombre_categorias.append(atencion[1])
    nombre_categorias = list(dict.fromkeys(nombre_categorias))
    data = {
        'titulo': 'Atencion Profesional',
        'atencion_profesional': atencion_profesional,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': json.dumps(atencion_profesional, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_atencion_profesional.html', data=data)


@app.route('/reportes/patologias_admision', methods=["GET", "POST"])
def reportes_patologias_admision():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    patologias_admision = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        patologias_admision = obtener_patologias_admision(
            fecha_desde, fecha_hasta)
    else:
        patologias_admision = obtener_patologias_admision(
            fecha_desde, fecha_hasta)
    nombre_categorias = []
    totales = 0
    for patologia in patologias_admision:
        totales += patologia[0]
        nombre_categorias.append(patologia[2])
    nombre_categorias = list(dict.fromkeys(nombre_categorias))
    data = {
        'titulo': 'Patologias Admisión',
        'patologias_admision': patologias_admision,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': json.dumps(patologias_admision, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_patologias_admision.html', data=data)


@app.route('/reportes/altas_mensuales_pacientes')
def reportes_altas_mensuales_pacientes():
    altas_mensuales_genero = obtener_altas_mensuales_por_genero()
    valores_categorias = []
    nombre_categorias = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    totales = 0
    for altas in altas_mensuales_genero:
        totales += altas[0]
        valores_categorias.append(altas[0])
    data = {
        'titulo': 'Altas Mensuales de Pacientes',
        'altas_mensuales_genero': altas_mensuales_genero,
        'meses': nombre_categorias,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': json.dumps(altas_mensuales_genero, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_altas_mensuales_pacientes.html', data=data)


@app.route('/reportes/alta_pacientes_zona')
def reportes_pacientes_zonas():
    alta_pacientes_por_zona = obtener_alta_paciente_por_zonas()
    valores_categorias = []
    nombre_categorias = obtener_detalle_barrios()
    totales = 0
    for altas in alta_pacientes_por_zona:
        totales += altas[0]
        valores_categorias.append(altas[0])
    data = {
        'titulo': 'Altas de Pacientes por Zona',
        'alta_pacientes_por_zona': alta_pacientes_por_zona,
        'nombre_categorias': json.dumps(nombre_categorias, ensure_ascii=False),
        'valores_categorias': json.dumps(alta_pacientes_por_zona, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_altas_pacientes_zonas.html', data=data)


@app.route('/reportes/parametros_edades', methods=["GET", "POST"])
def reportes_parametros_edades():
    parametros_edades = obtener_parametros_edades()
    valores_columnas = []
    nombre_columnas = []
    totales = 0
    for parametros in parametros_edades:
        totales += parametros[0]
        valores_columnas.append(parametros[0])
        nombre_columnas.append(parametros[1])
    data = {
        'titulo': 'Parametros por Edades',
        'parametros_edades': parametros_edades,
        'nombres_columnas': json.dumps(nombre_columnas, ensure_ascii=False),
        'valores_columnas': valores_columnas,
        'total': totales
    }
    return render_template('reportes_parametros_edades.html', data=data)


@app.route('/reportes/genero_especialidades', methods=["GET", "POST"])
def reportes_genero_especialidades():
    genero_especialidades = obtener_genero_especialidades()
    nombre_columnas = []
    for especialidades in obtener_lista_de_especialidades():
        nombre_columnas.append(especialidades[1])
    totales = 0
    for generos in genero_especialidades:
        totales += generos[0]
    data = {
        'titulo': 'Generos por Especialidad',
        'genero_especialidades': genero_especialidades,
        'nombres_columnas': json.dumps(nombre_columnas, ensure_ascii=False),
        'valores_columnas': json.dumps(genero_especialidades, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_genero_especialidades.html', data=data)


@app.route('/reportes/horas_trabajadas_profesional', methods=["GET", "POST"])
def reportes_horas_trabajadas_profesional():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    horas_trabajadas = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        horas_trabajadas = obtener_horas_trabajadas_profesional(
            fecha_desde, fecha_hasta)
    else:
        horas_trabajadas = obtener_horas_trabajadas_profesional(
            fecha_desde, fecha_hasta)
    nombres_columnas = []
    for profesionales in obtener_lista_profesionales():
        nombres_columnas.append("{} {}".format(
            profesionales[1], profesionales[2]))
    totales = 0
    for horas in horas_trabajadas:
        totales += float(horas[2])
    data = {
        'titulo': 'Horas Trabajadas por profesional',
        'horas_trabajadas': horas_trabajadas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombres_columnas': json.dumps(nombres_columnas, ensure_ascii=False),
        'valores_columnas': json.dumps(horas_trabajadas, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_horas_trabajadas_profesional.html', data=data)


@app.route('/reportes/reportes_estado_parametro_edades', methods=["GET", "POST"])
def reportes_estado_parametro_edades():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    estado_parametros_edades = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        estado_parametros_edades = obtener_estado_turno_parametro_edades(
            fecha_desde, fecha_hasta)
    else:
        estado_parametros_edades = obtener_estado_turno_parametro_edades(
            fecha_desde, fecha_hasta)
    nombres_columnas = ["Primera Infancia (0-5 años)", "Infancia (6 - 11 años)",
                        "Adolescencia (12 - 18 años)", "Juventud (14 - 26 años)", "Adultez (27 o más años)"]
    data = {
        'titulo': 'Estado de Turnos por Parámetro de Edades',
        'estado_parametros_edades': estado_parametros_edades,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombres_columnas': json.dumps(nombres_columnas, ensure_ascii=False),
        'valores_columnas': json.dumps(estado_parametros_edades, ensure_ascii=False)
    }
    return render_template('reportes_estado_parametros_edades.html', data=data)


@app.route('/reportes/reportes_motivos_anulacion_especialidad', methods=["GET", "POST"])
def reportes_motivos_anulacion_especialidad():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    motivos_anulacion_especialidad = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        motivos_anulacion_especialidad = obtener_motivos_anulacion_especialidad(
            fecha_desde, fecha_hasta)
    else:
        motivos_anulacion_especialidad = obtener_motivos_anulacion_especialidad(
            fecha_desde, fecha_hasta)
    nombre_columnas = []
    totales = 0
    for motivos in motivos_anulacion_especialidad:
        totales += motivos[0]
    for especialidades in obtener_lista_de_especialidades():
        nombre_columnas.append(especialidades[1])
    data = {
        'titulo': 'Motivo anulación por especialidad',
        'motivos_anulacion_especialidad': motivos_anulacion_especialidad,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nombres_columnas': json.dumps(nombre_columnas, ensure_ascii=False),
        'valores_columnas': json.dumps(motivos_anulacion_especialidad, ensure_ascii=False),
        'total': totales
    }
    return render_template('reportes_motivo_anulacion_especialidad.html', data=data)


@app.route('/reportes/ranking_pacientes_atenciones', methods=["GET", "POST"])
def reportes_ranking_pacientes_atenciones():
    nombres_columnas = []
    valores_columnas = []
    ranking_pacientes_atenciones = obtener_ranking_de_pacientes_cantidad_turnos()
    totales = 0
    for pacientes in ranking_pacientes_atenciones:
        nombres_columnas.append("{} {}".format(
            pacientes[1], pacientes[2]))
        valores_columnas.append(int(pacientes[0]))
        totales += pacientes[0]
    data = {
        'titulo': 'Ranking de pacientes por cantidad de turnos de admisión',
        'ranking_pacientes_atenciones': ranking_pacientes_atenciones,
        'nombres_columnas': json.dumps(nombres_columnas, ensure_ascii=False),
        'valores_columnas': valores_columnas,
        'total': totales
    }
    return render_template('reportes_pacientes_cantidad_turnos.html', data=data)


@app.route('/reportes/reporte_tipo_recursos', methods=["GET", "POST"])
def reportes_tipo_recursos():
    fecha_desde = '2021-01-01'
    fecha_hasta = '2021-12-31'
    reporte_tipo_recursos = None
    if request.method == 'POST':
        fecha_desde = request.form["fechaDesde"]
        fecha_hasta = request.form["fechaHasta"]
        reporte_tipo_recursos = obtener_recursos(
            fecha_desde, fecha_hasta)
    else:
        reporte_tipo_recursos = obtener_recursos(
            fecha_desde, fecha_hasta)
    data = {
        'titulo': 'Listado de Recursos por Tipo',
        'reporte_tipo_recursos': reporte_tipo_recursos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    }
    return render_template('reportes_tipo_recursos.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
