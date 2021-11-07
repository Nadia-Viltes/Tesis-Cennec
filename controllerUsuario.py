from config_bd import get_conexion

# query para que me muestre los datos en la lista de USUARIOS
def obtener_lista_usuarios():
    query = """
           SELECT us.IdUsuario, rec.Nombre, rec.Apellido, rol.Nombre, us.Nombre
            FROM usuario as us, recurso as rec, rol as rol
            WHERE us.IdRecurso = rec.IdRecurso
            AND us.IdRol = rol.IdRol
            AND us.fechaAlta is not null;              
            """
    conexion = get_conexion()
    usuario = []
    with conexion.cursor() as cur:
        cur.execute(query)
    usuario = cur.fetchall()
    conexion.close()
    return usuario

# query para que me muestre los datos del recuerso a seleccionar
def obtener_lista_recursos():
    query = """SELECT re.IdRecurso, re.Nombre, re.Apellido, re.NumeroDocumento, tre.IdTipoRecurso, tre.Nombre,re.Legajo 
            FROM recurso as re, tiporecurso as tre 
            WHERE re.IdTipoRecurso = tre.IdTipoRecurso"""
    conexion = get_conexion()
    recursos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    recursos = cur.fetchall()
    conexion.close()
    return recursos

#busqueda dinamica de recursos por nombre o dni
#para utilizar en la busqueda
def obtener_recursos_nombre_apellido_dni(valor):
    query = """SELECT re.IdRecurso, re.Nombre, re.Apellido, re.NumeroDocumento, tre.IdTipoRecurso, tre.Nombre,re.Legajo
            FROM recurso as re, tiporecurso as tre
            WHERE re.IdTipoRecurso = tre.IdTipoRecurso
            AND LOWER(CONCAT(re.nombre, re.apellido, NumeroDocumento)) like LOWER('{}')""".format(valor)    
    conexion = get_conexion()
    recursos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    recursos = cur.fetchall()
    conexion.close()
    return recursos

# query para obtener recurso por ID
def obtener_recurso_por_id(idRecurso):
    query = """SELECT re.IdRecurso, re.Nombre, re.Apellido, re.NumeroDocumento, tre.IdTipoRecurso, tre.Nombre,re.Legajo 
            FROM recurso as re, tiporecurso as tre 
            WHERE re.IdTipoRecurso = tre.IdTipoRecurso
            AND re.IdRecurso = {}""".format(idRecurso)
    conexion = get_conexion()
    recurso_id = None
    with conexion.cursor() as cur:
        cur.execute(query),(idRecurso,)
    recurso_id = cur.fetchone()
    conexion.close()
    return recurso_id

