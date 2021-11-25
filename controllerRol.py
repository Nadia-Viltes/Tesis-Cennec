from config_bd import get_conexion

# query para que me muestre los datos en la lista de ROLES
def obtener_lista_roles():
    query = """
           SELECT IdRol, Nombre, Descripcion FROM rol 
           WHERE FechaBaja is null;              
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
           WHERE FechaBaja is null;              
            """
    conexion = get_conexion()
    privilegios = []
    with conexion.cursor() as cur:
        cur.execute(query)
    privilegios = cur.fetchall()
    conexion.close()
    return privilegios


# Acá inserto primero el rol para obtener el id
def insertar_rol (nombreRol,descripcionRol):
    conexion = get_conexion()
    query = """
        INSERT INTO rol(Nombre, Descripcion, FechaAlta) 
        VALUES ('{}','{}', NOW());""".format(nombreRol,descripcionRol)  
    rol_id = None
    print("ESTE ES MI INSERTAR ROL -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        rol_id = cur.lastrowid
    conexion.commit()
    conexion.close()
    return rol_id


# Acá inserto los privilegios que le asigné a ese rol
def insertar_rol_privilegio (idRol, idPrivilegio):
    conexion = get_conexion()
    query = """
        INSERT INTO rolprivilegio (IdRol, IdPrivilegio, FechaAlta) 
        VALUES ({},{},NOW());""".format(idRol, idPrivilegio)
    rol_privilegio = None
    print("ESTE ES MI INSERTAR ROL/PRIVILEGIO -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        rol_privilegio = cur.lastrowid
    conexion.commit()
    conexion.close()
    return rol_privilegio

# query para obtener rol por ID
def obtener_id_rol(idRol):
    query = """
           SELECT IdRol, Nombre, Descripcion FROM rol 
           WHERE FechaBaja is null
           AND IdRol = {}""".format(idRol)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    rol_id = cur.fetchone()
    conexion.close()
    return rol_id


# Le asigno fecha de baja al rol
def update_eliminar_rol(id_rol):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE rol SET FechaBaja = now() WHERE IdRol = {}""".format
                       (id_rol))
    conexion.commit()
    conexion.close()


# Le asigno fecha de baja a los privilegios del rol que se dio de baja
def update_eliminar_rolprivilegio(id_rol):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE rolprivilegio SET FechaBaja = now() WHERE IdRol = {}""".format
                       (id_rol))
    conexion.commit()
    conexion.close()