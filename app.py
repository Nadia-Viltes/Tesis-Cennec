from controllerPaciente import *
from controllerUsuario import *
from controllerRol import *
from controllerTurno import *
from controllerHCD import *
from controllerMiAgenda import *
from flask import Flask, render_template, render_template_string, redirect, url_for, request, jsonify

app = Flask(__name__)


# Operación para mostrar la lista
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


@app.route("/guardar_paciente", methods=["POST"])
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


@app.route('/datos_modal_agregar')
def agregar_datos():
    tipoDoc = obtener_tipoDocumento()
    pais = obtener_pais()
    provincia = obtener_provincia()
    localidad = obtener_localidad()
    barrio = obtener_barrio()
    financiador = obtener_financiador()
    values = {
        'tipoDocumento': tipoDoc,
        'pais': pais,
        'provincia': provincia,
        'localidad': localidad,
        'barrio': barrio,
        'financiador': financiador
    }
    return jsonify({'htmlresponse': render_template('agregar_paciente.html', data=values)})

@app.route('/datos_modal_editar/<int:id>')
def obtener_paciente_id(id):
    paciente = obtener_paciente_por_id(id)
    tipoDocumento = obtener_tipoDocumento()
    pais = obtener_pais()
    provincia = obtener_provincia()
    localidad = obtener_localidad()
    barrio = obtener_barrio()
    financiador = obtener_financiador()
    values = {
            'titulo': 'Editar paciente',
            'pacientes': paciente,
            'tipoDocumento': tipoDocumento,
            'pais': pais,
            'provincia': provincia,
            'localidad': localidad,
            'barrio': barrio,
            'financiador': financiador
    }
    return jsonify({'htmlresponse': render_template('editar_paciente.html', data=values)})


@app.route("/actualizar_paciente", methods=["POST"])
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


@app.route('/home')
def index(name='Home'):
    return render_template('index.html', titulo=name)



@app.route('/HCD/')
def HCD():
    hcd = obtener_lista_hcd()
    data={
        'titulo': 'Historia Clínica Dígital',
        'hcd': hcd
    }
    return render_template('HCD.html', data=data)



@app.route('/ver_HCD/<int:id>', methods=["GET", "POST"])
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
    return render_template('ver_HCD.html', data=values)


#Carga los turnos admision llenando la tabla con jquery
@app.route('/agrega_turnos_admision', methods=["POST"])
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


@app.route("/guardar_turnos_admision", methods=["POST"])
def guardar_turnos_admision():
        idPaciente_HCD = request.form["idPaciente_HCD"]
        IdEspecialidad = request.form["tipoEspecialidad"]
        idPatologia = request.form["tipoPatologia"]
        cantidad = request.form["cantidad"]
        insertar_turnos_admision(idPaciente_HCD, IdEspecialidad, idPatologia, cantidad)
        return redirect("/HCD")
    # SI DA OK redireccionar


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


# Operación para mostrar la lista de turnos
@app.route('/turno/')
def turnos():
    turno = obtener_lista_turno()
    data = {
        'titulo': 'Turnos',
        'turno': turno
    }
    return render_template('turnos.html', data=data)


# Acción para ver la pantalla de asignar turno
#aca
@app.route('/asignar_turno/<int:id>')
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

@app.route('/grabar_turno', methods=["POST"])
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
@app.route('/profesionales_dropdown/<int:id>')
def profesionales_especialidad_dropdown(id):
    profesionales = obtener_profesionales_especialidad(id)
    options = "<option selected disabled>Seleccionar...</option>"
    for profesional in profesionales:
        options+= "<option value={}>{} {}</option>".format(profesional[0], profesional[1], profesional[2])
    return jsonify({'htmlresponse': render_template_string(options)})


# Acción para ver la pantalla de seleccionar el paciente en asignar turnos
# Acción para abrir el modal para buscar un paciente
@app.route('/seleccionar_paciente', methods=['GET', 'POST'])
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



# Acción para abrir el modal de RECEPTAR turno
@app.route('/receptar_turno/<int:id_turno>')
def receptar_turno(id_turno):
    turno = obtener_turno_por_id(id_turno)
    id_paciente = turno[5]
    id_especialidad = turno[11]
    id_profesional_actual = turno[13]
    profesional_actual = [id_profesional_actual, turno[14], turno[15]]
    paciente = obtener_paciente_por_id(id_paciente)
    profesionales = obtener_profesionales_especialidad(id_especialidad)
    profesionales_filtrados = [x for x in profesionales if x[0] != id_profesional_actual]
    values = {
        'titulo': 'Receptar turno',
        'turno': turno,
        'paciente': paciente,
        'profesionales': profesionales_filtrados,
        'profesional_actual': profesional_actual
    }
    return render_template('turnos_receptar.html', data=values)



# Acción para abrir el modal de REPROGRAMAR turno
@app.route('/modal_reprogramar_turno/<int:id>')
def reprogramar_turno(id):
    turno_por_id = obtener_turno_por_id(id)
    tipoTurno = obtener_tipoTurno()
    especialidad = obtener_especialidad_turnos()
    values = {
        'titulo': 'Reprogramar turno',
        'turno_por_id': turno_por_id,
        'tipoTurno': tipoTurno,
        'especialidad': especialidad
    }
    return jsonify({'htmlresponse': render_template('turnos_reprogramar.html', data=values)})



# Acción para abrir el modal de ANULAR turno
@app.route('/modal_anular_turno/<int:id>')
def anular_turno(id):
    turno_por_id = obtener_turno_por_id(id)
    motivoTurno = obtener_motivoTurno()
    values = {
        'titulo': 'Anular turno',
        'turno_por_id': turno_por_id,
        'motivoTurno': motivoTurno
    }
    return jsonify({'htmlresponse': render_template('turnos_anular.html', data=values)})



@app.route('/rol')
def configuracion_roles():
    rol = obtener_lista_roles()
    data = {
        'titulo': 'Configuración de roles',
        'rol': rol
    }
    return render_template('roles.html', data=data)


@app.route('/modal_agregar_rol')
def agregar_rol():
    privilegios = obtener_lista_privilegios()
    data = {
        'titulo': 'agregar_rol',
        'privilegios': privilegios
    }
    return jsonify({'htmlresponse': render_template('agregar_rol.html', data=data)})


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


@app.route('/usuario')
def configuracion_usuarios():
    usuario = obtener_lista_usuarios()
    data = {
        'titulo': 'Configuración de usuarios',
        'usuario': usuario
    }
    return render_template('usuarios.html', data=data)


@app.route('/seleccionar_recurso', methods=['GET', 'POST'])
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
#aca
@app.route('/agregar_usuario/<int:id>')
def agregar_usuario(id):
    recurso = obtener_recurso_por_id(id)
    rol = obtener_lista_roles()
    privilegios = obtener_lista_privilegios()
    values = {
        'titulo': 'Crear usuario',
        'subtitulo': 'Datos de autenticación',
        'recurso': recurso,
        'rol': rol,
        'privilegios': privilegios
    }
    return render_template('usuario_agregar.html', data=values)


@app.route('/login')
def login():
    data = {
        'titulo': 'Login',
    }
    return render_template('login.html', data=data)


def pagina_no_encontrada(error):
    # return render_template('error.html'),404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)