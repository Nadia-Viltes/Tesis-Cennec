from flask import Flask, render_template, redirect, url_for
<<<<<<< Updated upstream
from controller import obtener_pacientes
=======
from logging import debug
import controller
from flask import request
>>>>>>> Stashed changes


app = Flask(__name__)


@app.route('/pacientes/')
def paciente():
<<<<<<< Updated upstream
    pacientes = obtener_pacientes()
    data = {
=======
    pacientes = controller.obtener_pacientes()
    data={
>>>>>>> Stashed changes
        'titulo': 'Pacientes',
        'pacientes': pacientes
    }
    return render_template('pacientes.html', data=data)


@app.route('/home/')
def index(name='Home'):
    return render_template('index.html', titulo=name)


@app.route('/HCD/')
def HCD(name='Historia clínica dígital'):
    return render_template('HCD.html', titulo=name)


@app.route('/reportes/')
def reportes():
    data = {
        'titulo': 'Reportes',
    }
    return render_template('reportes.html', data=data)


@app.route('/agenda/')
def agenda():
    data = {
        'titulo': 'Mi Agenda',
    }
    return render_template('agenda.html', data=data)


@app.route('/turno/')
def turnos():
    data = {
        'titulo': 'Turnos',
    }
    return render_template('turnos.html', data=data)


@app.route('/configuracion/')
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
