from config_bd import get_conexion


def obtener_usuario(id):
    query = """
           SELECT Nombre FROM usuario
            WHERE fechaBaja is null
            AND lower(Nombre) like '{}';              
            """
    conexion = get_conexion()
    dato_usuario = []
    with conexion.cursor() as cur:
        cur.execute(query)
    dato_usuario = cur.fetchone()[0]
    conexion.close()
    return dato_usuario


def obtener_datos_login():
    query = """
           SELECT IdUsuario, Nombre, Contraseña FROM usuario
            WHERE fechaBaja is null
            AND lower(Nombre) like '{}';              
            """
    conexion = get_conexion()
    datos_login = []
    with conexion.cursor() as cur:
        cur.execute(query)
    datos_login = cur.fetchone()
    conexion.close()
    return datos_login