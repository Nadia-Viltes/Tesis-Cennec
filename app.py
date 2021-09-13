from controllerPaciente import *
from controllerUsuario import *
from controllerRol import *
from controllerTurno import *
from controllerHCD import *
from controllerMiAgenda import *
from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)


# Operación para mostrar la lista
@app.route('/pacientes/', methods=['GET', 'POST'])
def pacientes():
    pacientes = None
    if request.method == 'POST':
        parametros = request.form["buscar"]
        print("Esta es la puta query {}".format(parametros))
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
    tipoDocumento = obtener_tipoDocumento()
    pais = obtener_pais()
    provincia = obtener_provincia()
    localidad = obtener_localidad()
    barrio = obtener_barrio()
    financiador = obtener_financiador()
    values = {
        'tipoDocumento': tipoDocumento,
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
def actualizar_paciente():
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
    actualizar_domicilio(pais, provincia, localidad, calle, altura, piso, dpto, barrio, idPaciente)
    actualizar_tutoria(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
    actualizar_afiliacion(financiador,nroAfiliado)
    actualizar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento,nroDocumento, fechaNacimiento, idPaciente)
    return redirect("/pacientes")


@app.route('/home')
def index(name='Home'):
    return render_template('index.html', titulo=name)

@app.route('/HCD')
def HCD():
    hcd = obtener_lista_hcd()
    data={
        'titulo': 'Historia Clínica Dígital',
        'hcd': hcd
    }
    return render_template('HCD.html', data=data)

@app.route('/datos_modal_verHCD/<int:id>')
def obtener_hcd_id(id):
    paciente_hcd = obtener_hcd_por_id(id)
    IdEspecialidad = obtener_especialidad()
    idPatologia = obtener_patologia()
    values = {
            'titulo': 'Historia clínica dígital',
            'paciente_hcd': paciente_hcd,
            'especialidad': IdEspecialidad,
            'patologia': idPatologia
    }
    return jsonify({'htmlresponse': render_template('modal_ver_HCD.html', data=values)})

@app.route("/guardar_turnos_admision", methods=["POST"])
def guardar_turnos_admision():
        idPaciente_HCD = request.form["idPaciente_HCD"]
        IdEspecialidad = request.form["tipoEspecialidad"]
        idPatologia = request.form["tipoPatologia"]
        cantidad = request.form["cantidad"]
        insertar_turnos_admision(idPaciente_HCD, IdEspecialidad, idPatologia, cantidad)
        return redirect("/datos_modal_verHCD")
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


# Acción para abrir el modal de asignar turno
@app.route('/modal_asignar_turno')
def asignar_turno():
    tipoTurno = obtener_tipoTurno()
    especialidad = obtener_especialidad()
    #profesional = obtener_profesional(especialidad)
    value = {
        'titulo': 'Asignar turno',
        'tipoTurno': tipoTurno,
        'especialidad': especialidad
        #'profesional': profesional
    }
    return jsonify({'htmlresponse': render_template('turnos_asignar.html', data=value)})


    # Acción para abrir el modal para buscar un paciente
@app.route('/modal_buscar_paciente')
def buscar_paciente():
    value = {
        'titulo': 'Buscar paciente'
    }
    return jsonify({'htmlresponse': render_template('modal_buscar_paciente.html', data=value)})


# Acción para abrir el modal de RECEPTAR turno
@app.route('/modal_receptar_turno/<int:id_turno>')
def receptar_turno(id_turno):
    turno_id = obtener_turno_por_id(id_turno)
    value = {
        'titulo': 'Receptar turno',
        'turno_id': 'turno_id'
    }
    return jsonify({'htmlresponse': render_template('turnos_receptar.html', data=value)})


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
    print("estos son los privilegios checkeados {}".format(request.form.getlist('privilegio_nombre')))
    return redirect("/rol")


@app.route('/usuario')
def configuracion_usuarios():
    usuario = obtener_lista_usuarios()
    data = {
        'titulo': 'Configuración de usuarios',
        'usuario': usuario
    }
    return render_template('usuarios.html', data=data)


@app.route('/modal_agregar_usuario')
def agregar_usuario():
    privilegios = obtener_lista_privilegios()
    roles = obtener_lista_roles()
    values = {
        'titulo': 'agregar_rol',
        'roles': roles,
        'privilegios': privilegios
    }
    return jsonify({'htmlresponse': render_template('agregar_usuario.html', data=values)})

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