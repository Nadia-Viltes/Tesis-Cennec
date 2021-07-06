from bd_config import establecer_conexion

def obtener_pacientes():
    conexion = establecer_conexion()
    paciente = None
    with conexion.cursor() as cur:
        cur.execute('SELECT * from paciente')
    paciente = cur.fetchone()
    conexion.close()
    return paciente


obtener_pacientes
