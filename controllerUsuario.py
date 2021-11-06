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



        