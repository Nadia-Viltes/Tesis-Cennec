from logging import debug
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/pacientes')
def home():
    return render_template('pacientes.html')

@app.route('/HCD')
def agregar_paciente():
    return render_template('HCD.html')


if __name__ == '__main__':
    app.run(debug=True)