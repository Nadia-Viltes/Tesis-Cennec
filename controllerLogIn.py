from config_bd import get_conexion
# query para que me muestre los datos en la lista de ROLES

def login_usuario_id():
    query = """
           "SELECT * FROM usuario WHERE IdUsuario
            """
    conexion = get_conexion()
    login = []
    with conexion.cursor() as cur:
        cur.execute(query)
    login = cur.fetchall()
    conexion.close()
    return login


# query para que me muestre los datos en la lista de PRIVILEGIOS
def login_pass():
    query = """
           "SELECT * FROM usuario WHERE Contraseña              
            """
    conexion = get_conexion()
    login = []
    with conexion.cursor() as cur:
        cur.execute(query)
    login = cur.fetchall()
    conexion.close()
    return login