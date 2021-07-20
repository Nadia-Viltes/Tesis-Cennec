from controllerHCD import *
from flask import Flask, render_template, redirect, url_for, request, jsonify
from controller import *

app = Flask(__name__)


# Operación para mostrar la lista
@app.route('/pacientes/')
def pacientes():
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
    fechaAltaFinanciador = request.form["fechaAltaFinanciador"]
    idDomicilio = insertar_domicilio(pais, provincia, localidad, barrio, calle, altura, piso, dpto)
    idTutoria = insertar_tutor(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
    idPaciente = insertar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, idTutoria)
    insertar_HCD(idPaciente)
    insertar_afiliacion(idPaciente, financiador, nroAfiliado, fechaAltaFinanciador)
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
    values = {
            'titulo': 'Editar paciente',
            'pacientes': paciente
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
    hcd = obtener_hcd()
    data={
        'titulo': 'Historia Clínica Dígital',
        'hcd': hcd
    }
    return render_template('HCD.html', data=data)


@app.route('/reportes')
def reportes():
    data = {
        'titulo': 'Reportes',
    }
    return render_template('reportes.html', data=data)


@app.route('/agenda')
def agenda():
    data = {
        'titulo': 'Mi Agenda',
    }
    return render_template('agenda.html', data=data)


@app.route('/turno')
def turnos():
    data = {
        'titulo': 'Turnos',
    }
    return render_template('turnos.html', data=data)


@app.route('/configuracion')
def configuracion():
    data = {
        'titulo': 'Configuración',
    }
    return render_template('configuracion.html', data=data)


def pagina_no_encontrada(error):
    # return render_template('error.html'),404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)