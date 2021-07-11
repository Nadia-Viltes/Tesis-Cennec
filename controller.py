from config_bd import get_conexion

def obtener_pacientes():
    conexion = get_conexion()
    paciente = []
    with conexion.cursor() as cur:
        cur.execute('SELECT Nombre, Apellido, NumeroDocumento, IdTutoria from paciente')
    paciente = cur.fetchone()
    conexion.close()
    return paciente
