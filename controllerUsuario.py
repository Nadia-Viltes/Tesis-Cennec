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
