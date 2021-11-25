from loguru import logger
from controllerPaciente import *
from controllerUsuario import *
from controllerRol import *
from controllerTurno import *
from controllerHCD import *
from controllerMiAgenda import *
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
        privilegios_dict[privilegio[5]] = get_modulo_by_privilegio(privilegio[5])
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
        logger.info("usuario logueado  y estos son los privilegios-> {}".format(session["privilegios"].values()))
        if("/" + current_url.split("/")[1] in session["privilegios"].values()) == False:
            logger.info("logger privilegios -> {}".format(session["privilegios"].values()))
            abort(404)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form["usuario"]
        password = request.form["password"]
        datos_usuario = obtener_datos_usuario_by_user_password(usuario, password)
        logger.info("datos usuario -> {}".format(datos_usuario))
        if datos_usuario != None:
            session["usuario_id"] = datos_usuario[0]
            logger.info("usuario_id session -> {}".format(session["usuario_id"]))
            session["usuario"] = datos_usuario[1]
            session["nombre"] = datos_usuario[2]
            session["apellido"] = datos_usuario[3]
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
    return render_template('index.html')

# MUESTRA LA LISTA DE PACIENTES Y BUSQUEDA
@app.route('/pacientes/', methods=['GET', 'POST'])
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

#Pantalla de AGREGAR PACIENTE
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

#Acción para cargar las provincias en dropdown una vez seleccionado el país
@app.route('/pacientes/provincias_dropdown/<int:id>')
def provincias_pais_dropdown(id):
    provincias = obtener_provincias_by_id_pais(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for provincia in provincias:
        options+= "<option value={}>{}</option>".format(provincia[0], provincia[1])       
    return jsonify({'htmlresponse': render_template_string(options)})

#Acción para cargar las localidades en dropdown una vez seleccionado la provincia
@app.route('/pacientes/localidades_dropdown/<int:id>')
def localidades_provincia_dropdown(id):
    localidades = obtener_localidades_by_id_provincia(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for localidad in localidades:
        options+= "<option value={}>{}</option>".format(localidad[0], localidad[1])
    return jsonify({'htmlresponse': render_template_string(options)})

#Carga los barrios del dropdown pacientes
@app.route('/pacientes/barrios_dropdown/<int:id>')
def barrios_localidad_dropdown(id):
    barrios = obtener_barrios_by_id_localidad(id)
    options = "<option value='' selected disabled>Seleccionar...</option>"
    for barrio in barrios:
        options+= "<option value={}>{}</option>".format(barrio[0], barrio[1])
    return jsonify({'htmlresponse': render_template_string(options)})

#FUNCIÓN PARA QUE GUARDE LOS DATOS DEL PACIENTE NUEVO
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
    idDomicilio = insertar_domicilio(pais, provincia, localidad, barrio, calle, altura, piso, dpto)
    idTutoria = insertar_tutor(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
    idPaciente = insertar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, idTutoria)
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
    actualizar_domicilio(pais, provincia, localidad, barrio, calle, altura, piso, dpto, idPaciente)
    actualizar_tutoria(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular,idPaciente)
    actualizar_afiliacion(financiador,nroAfiliado,idPaciente)
    actualizar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idPaciente)
    return redirect("/pacientes")

@app.route('/hcd')
def hcd():
    hcd = obtener_lista_hcd()
    data={
        'titulo': 'Historia Clínica Dígital',
        'hcd': hcd
    }
    return render_template('hcd.html', data=data)

@app.route('/hcd/ver_admision/<int:id>', methods=["GET", "POST"])
def obtener_hcd_idd(id):
    paciente_hcd = obtener_hcd_por_id(id)
    IdEspecialidad = obtener_especialidad(id)
    idPatologia = obtener_patologia()
    turnosadm = obtener_lista_turnos_admision(id)
    values={
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd,
        'especialidad': IdEspecialidad,
        'patologia': idPatologia,
        'turnosadm': turnosadm
    }
    return render_template('hcd_ver_admision.html', data=values)

@app.route('/hcd/ver_evoluciones/<int:id>', methods=["GET", "POST"])
def obtener_evolucion_id(id):
    paciente_hcd = obtener_hcd_por_id(id)
    values={
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd
    }
    return render_template('hcd_ver_evolucion.html', data=values)

#Carga los turnos admision llenando la tabla con jquery
@app.route('/hcd/agrega_turnos_admision', methods=["POST"])
def agrega_turnos_admision():
    #tomo los datos que vienen del form
    id_paciente = request.form['idPaciente']
    id_especialidad = request.form['idEspecialidad']
    cantidad = request.form['cantidad']
    id_patologia = request.form['idPatologia']
    #inserto los datos en configuracion de turno
    insertar_turnos_admision(id_paciente, id_especialidad, id_patologia, cantidad)
    #hago la consulta para obtener todos los turnos por id de paciente por especialidad
    lista_turnos = obtener_lista_turnos_admision(id_paciente)
    table = ""
    #creo una tabla con los datos de la lista de turnos y se la envío
    #a ver_HCD.html
    for turno in lista_turnos:
        table+= "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(turno[1], turno[2], turno[4])
    return jsonify({'htmlresponse': render_template_string(table)})

@app.route('/reportes')
def reportes():
    data = {
        'titulo': 'Reportes',
    }
    return render_template('reportes.html', data=data)

@app.route('/agenda')
def agenda():
    mi_agenda = obtener_lista_turno_mi_agenda()
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
    idTurno = request.form["dataTurnoId"]
    id_estado = obtener_id_estado_turno_por_estado("Atendiendo")
    return redirect("/agenda")

# Acá se abre el modal de finalizar atención
@app.route('/agenda/modal_finalizar_turno/<int:id>')
def finalizar_turno(id):
    IdTurno = obtener_turno_por_id(id)
    values = {
            'titulo': 'Finalizar atención',
            'IdTurno': IdTurno
    }
    return jsonify({'htmlresponse': render_template('mi_agenda_finalizar_atencion.html', data=values)})

# Acá se ejecuta la query para agregar un turno en estado atendido
@app.route("/agenda/finalizar_atencion", methods=["POST"])
def finalizar_atencion():
    idTurno = request.form["dataTurnoId"]
    id_estado = obtener_id_estado_turno_por_estado("Atendiendo")
    return redirect("/agenda")

@app.route('/agenda/ver_hcd/<int:id>', methods=["GET", "POST"])
def ver_hcd(id):
    paciente_hcd = obtener_hcd_por_id(id)
    historial_hcd = obtener_historial_evoluciones(id)
    values={
        'titulo': 'Historia clínica digital',
        'paciente_hcd': paciente_hcd,
        'historial': historial_hcd
    }
    return render_template('mi_agenda_ver_hcd.html', data=values)

@app.route('/agenda/guardar_detalle', methods=["GET", "POST"])
def guardar_detalle():
    inputProfesional = request.form['inputProfesional']
    InputTextareaEvoluciones = request.form['InputTextareaEvoluciones']
    inputIdHCD = request.form['inputIdHCD']
    existeEvolucion = consulta_existe_evolucion(inputIdHCD)
    if existeEvolucion == None:
        idEvolucion = insertar_evolucion(inputIdHCD)
        insertar_detalle(idEvolucion,inputProfesional,InputTextareaEvoluciones)
    else:
        insertar_detalle(existeEvolucion,inputProfesional,InputTextareaEvoluciones)
    # SI DA OK redireccionar
    return redirect("/agenda")

@app.route('/agenda/ver_historial/<int:id>', methods=["GET", "POST"])
def ver_historial(id):
    detalle_historial = obtener_detalle_historial(id)
    values={
        'titulo': 'Detalle de historia clínica',
        'detalle_historial': detalle_historial
    }
    return render_template('mi_agenda_historial.html', data=values)

# Operación para mostrar la lista de turnos
@app.route('/turnos')
def turnos():
    turno = obtener_lista_turno()
    data = {
        'titulo': 'Turnos',
        'turno': turno
    }
    return render_template('turnos.html', data=data)

# Acción para ver la pantalla de asignar turno
#aca
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

@app.route('/turnos/grabar_turno', methods=["POST"])
def grabar_turno():
    #tomo los datos que vienen del form
    print("este es mi request form")
    print(request.form)
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    #busco el id del turno asignado
    id_estado = obtener_id_estado_turno_por_estado("asignado")
    #inserto los datos en turno
    insertar_turno_asignado(id_tipo_turno, id_especialidad, id_profesional, id_paciente, fecha_turno, hora_inicio, hora_fin, id_estado)
    #Le sumo los turnos computados así continuamos con la logica de los turnos para asignar
    id_configturno = obtener_id_configuracion_turno(id_paciente,id_especialidad)
    actualizar_turnos_computados(id_paciente,id_especialidad,id_configturno)
    return redirect("/turno/")

#Acción para cargar de Profesionales en dropdown una vez seleccionada la especialidad
@app.route('/turnos/profesionales_dropdown/<int:id>')
def profesionales_especialidad_dropdown(id):
    profesionales = obtener_profesionales_especialidad(id)
    options = "<option selected disabled>Seleccionar...</option>"
    for profesional in profesionales:
        options+= "<option value={}>{} {}</option>".format(profesional[0], profesional[1], profesional[2])
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
    profesionales_filtrados = [x for x in profesionales if x[0] != id_profesional_actual]
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
    #tomo los datos que vienen del form
    id_turno_asignado = request.form['idTurnoAsignar']
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    #busco el id del turno asignado
    id_estado = obtener_id_estado_turno_por_estado("Receptado")
    #inserto los datos en turno
    update_turno_asignado(id_turno_asignado)
    insertar_turno_receptado(id_tipo_turno, id_especialidad, id_paciente, fecha_turno, hora_inicio, hora_fin, id_estado, id_profesional, id_turno_asignado)
    return redirect("/turno/")

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
    profesionales_filtrados = [x for x in profesionales if x[0] != id_profesional_actual]
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
    #tomo los datos que vienen del form
    id_turno_asignado = request.form['idTurnoAsignar']
    id_tipo_turno = request.form['tipoTurno']
    id_especialidad = request.form['nameEspecialidadDropdown']
    id_profesional = request.form['nameProfesionalDropdown']
    fecha_turno = request.form['fechaTurno']
    hora_inicio = request.form['nameHoraInicio']
    hora_fin = request.form['nameHoraFin']
    id_paciente = request.form['inputPacienteId']
    #busco el id del estado del turno en asignado
    id_estado = obtener_id_estado_turno_por_estado("Asignado")
    #inserto los datos en turno
    update_turno_reasignado(id_turno_asignado)
    insertar_turno_reasignado(id_tipo_turno, id_especialidad, id_profesional, id_paciente, fecha_turno, hora_inicio, hora_fin, id_estado, id_turno_asignado)
    return redirect("/turno/")

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
    motivoTurnosAnulados = request.form["motivoTurno"]
    ListaTurnosAnulados = request.form.getlist('lista_turnos_para_anular')
    #busco el id del estado del turno en asignado
    id_estado = obtener_id_estado_turno_por_estado("Anulado")
    for idTurnosAnulados in ListaTurnosAnulados:
        datos_turnos_para_anular = obtener_turno_por_id_asignado_anulado(idTurnosAnulados)
        insertar_anular_turno(datos_turnos_para_anular[1], datos_turnos_para_anular[2], datos_turnos_para_anular[3], datos_turnos_para_anular[4], datos_turnos_para_anular[5], datos_turnos_para_anular[6], datos_turnos_para_anular[7], id_estado, motivoTurnosAnulados, idTurnosAnulados)
        update_turno_asignado(idTurnosAnulados)
    print("estos son los turnos para anular checkeados {}".format(request.form.getlist('lista_turnos_para_anular')))
    # SI DA OK redireccionar
    return redirect("/turnos")

@app.route('/configuracion/usuarios/setear_privilegios_rol_seleccionado', methods=["POST"])
def setear_privilegios():
    #tomo los datos del rol
    id_rol = request.form['idRol']
    privilegios = obtener_privilegio_por_id_rol(id_rol)
    print("estos son los privilegios -> {}".format(privilegios))
    return jsonify({'privilegios': privilegios})

@app.route('/configuracion/rol')
def configuracion_roles():
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

'''
@app.route('/guardar_rol', methods=["POST"])
def guardar_rol():
    nombreRol = request.form["nombreRol"]
    descripcionRol = request.form["descripcionRol"]
    idPrivilegios = request.form.getlist('privilegio_nombre')
    idRol = insertar_rol(nombreRol, descripcionRol)
    for idPrivilegio in idPrivilegios:
        insertar_rol_privilegio(idRol, idPrivilegio)
    print("estos son los privilegios checkeados {}".format(request.form.getlist('privilegio_nombre')))
    # SI DA OK redireccionar
    return redirect("/rol")
'''    

@app.route('/configuracion/rol/editar_rol/<int:id>')
def editar_rol(id):
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

@app.route('/configuracion/usuarios')
def configuracion_usuarios():
    usuario = obtener_lista_usuarios()
    data = {
        'titulo': 'Configuración de usuarios',
        'usuario': usuario
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
    nombreUsuario = request.form["NombreUsuarioInput1"]
    contrasena = request.form["inputPasswordUsuario"]
    rolSeleccionado = request.form["checkRol"]
    guardar_usuario(idRecurso, nombreUsuario, contrasena, rolSeleccionado)
    # SI DA OK redireccionar
    return redirect("/usuario")

@app.route('/configuracion/usuarios/editar_usuario/<int:id>')
def editar_usuario(id):
    IdUsuario = obtener_usuario_por_id(id)
    recurso = obtener_recurso_por_id(id)
    rol = obtener_lista_roles()
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'Editar usuario',
        'IdUsuario': IdUsuario,
        'recurso': recurso,
        'rol': rol,
        'privilegios': privilegios

    }
    return render_template('usuario_editar.html', data=data)

## Acción para abrir el modal eliminar usuario
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
    return redirect("configuracion/usuarios")

if __name__ == '__main__':
    app.run(debug=True, port=5000)