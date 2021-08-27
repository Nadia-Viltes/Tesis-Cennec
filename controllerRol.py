from config_bd import get_conexion

# query para que me muestre los datos en la lista de ROLES
def obtener_lista_roles():
    query = """
           SELECT IdRol, Nombre, Descripcion FROM rol 
           WHERE FechaAlta is not null              
            """
    conexion = get_conexion()
    rol = []
    with conexion.cursor() as cur:
        cur.execute(query)
    rol = cur.fetchall()
    conexion.close()
    return rol

# query para que me muestre los datos en la lista de PRIVILEGIOS
def obtener_lista_privilegios():
    query = """
           SELECT IdPrivilegio, Nombre, Descripcion FROM privilegio 
           WHERE FechaAlta is not null;              
            """
    conexion = get_conexion()
    privilegios = []
    with conexion.cursor() as cur:
        cur.execute(query)
    privilegios = cur.fetchall()
    conexion.close()
    return privilegios