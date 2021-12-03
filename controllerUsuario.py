from loguru import logger
from config_bd import get_conexion

# query para que me muestre los datos en la lista de USUARIOS


def obtener_lista_usuarios():
    query = """
           SELECT us.IdUsuario, rec.Nombre, rec.Apellido, rol.Nombre, us.Nombre
            FROM usuario as us, recurso as rec, rol as rol
            WHERE us.IdRecurso = rec.IdRecurso
            AND us.IdRol = rol.IdRol
            AND us.Nombre != lower('admin')
            AND us.fechaBaja is null
            ORDER BY us.Nombre asc;              
            """
    conexion = get_conexion()
    usuario = []
    with conexion.cursor() as cur:
        cur.execute(query)
    usuario = cur.fetchall()
    conexion.close()
    return usuario


def obtener_lista_usuarios_query(parametros):
    query = """
           SELECT us.IdUsuario, rec.Nombre, rec.Apellido, rol.Nombre, us.Nombre
            FROM usuario as us, recurso as rec, rol as rol
            WHERE us.IdRecurso = rec.IdRecurso
            AND us.IdRol = rol.IdRol
            AND us.Nombre != lower('admin')
            AND us.fechaBaja is null
            AND (LOWER(CONCAT(us.Nombre, rec.Nombre, rec.Apellido))) LIKE LOWER('{}')
            ORDER BY us.Nombre asc;              
            """.format(parametros)
    conexion = get_conexion()
    usuario = []
    with conexion.cursor() as cur:
        cur.execute(query)
    usuario = cur.fetchall()
    conexion.close()
    return usuario

# obtener usuario y contraseña


def obtener_datos_usuario_by_user_password(usuario, password):
    query = """
            SELECT us.idusuario, us.nombre, re.nombre, re.apellido, r.nombre
            FROM USUARIO AS us, RECURSO AS re, rol as r
            WHERE us.idrecurso = re.idrecurso
            AND r.IdRol = us.IdRol
            AND us.nombre = '{}'
            AND us.contraseña = '{}'
            and us.FechaBaja is null;
            """.format(usuario, password)
    conexion = get_conexion()
    nombre_usuario = None
    try:
        with conexion.cursor() as cur:
            cur.execute(query)
        nombre_usuario = cur.fetchone()
    except:
        logger.info("Ocurrio un error al obtener los datos del usuario")
    finally:
        conexion.close()
        return nombre_usuario

# query para que me muestre los datos del recurso a seleccionar


def obtener_lista_recursos():
    query = """SELECT re.IdRecurso, re.Nombre, re.Apellido, re.NumeroDocumento, tre.IdTipoRecurso, tre.Nombre,re.Legajo 
            FROM recurso as re, tiporecurso as tre
            WHERE re.IdTipoRecurso = tre.IdTipoRecurso
            AND re.IdRecurso not in (Select IdRecurso from usuario WHERE fechabaja is null)
            ORDER BY re.Nombre asc;
            """
    conexion = get_conexion()
    recursos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    recursos = cur.fetchall()
    conexion.close()
    return recursos

# busqueda dinamica de recursos por nombre o dni
# para utilizar en la busqueda


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
            AND re.IdRecurso = {};""".format(idRecurso)
    conexion = get_conexion()
    recurso_id = None
    with conexion.cursor() as cur:
        cur.execute(query)
    recurso_id = cur.fetchone()
    conexion.close()
    return recurso_id

# query para obtener recurso por ID


def obtener_recurso_por_id_usuario(id_usuario):
    query = """SELECT re.IdRecurso, re.Nombre, re.Apellido, re.NumeroDocumento, tre.IdTipoRecurso, tre.Nombre,re.Legajo 
                FROM recurso as re, tiporecurso as tre, usuario us
                WHERE re.IdTipoRecurso = tre.IdTipoRecurso
                AND us.IdRecurso = re.IdRecurso
                AND us.IdUsuario = {}
                AND us.fechabaja is null;""".format(id_usuario)
    conexion = get_conexion()
    recurso = None
    with conexion.cursor() as cur:
        cur.execute(query)
    recurso = cur.fetchone()
    conexion.close()
    return recurso

# obtener privilegios por id usuario


def obtener_privilegios_por_id_usuario(id_usuario):
    query = """
            select us.IdUsuario, us.Nombre, rol.idrol, rol.Nombre as nombre_rol, pri.IdPrivilegio, pri.Nombre as nombre_privilegio 
            from usuario as us, rol, rolprivilegio as rolpri, privilegio as pri
            where us.IdRol = rol.IdRol
            and rolpri.IdRol = rol.IdRol
            and pri.IdPrivilegio = rolpri.IdPrivilegio
            and us.IdUsuario = {}
            and us.fechabaja is null;
            """.format(id_usuario)
    conexion = get_conexion()
    privilegios = []
    with conexion.cursor() as cur:
        cur.execute(query)
    privilegios = cur.fetchall()
    conexion.close()
    return privilegios

# query para obtener los privilegios por el id rol


def obtener_privilegio_por_id_rol(id_rol):
    query = """SELECT idprivilegio FROM ROLPRIVILEGIO
               WHERE idrol = {}
               AND fechabaja is null;""".format(id_rol)
    conexion = get_conexion()
    privilegios = []
    with conexion.cursor() as cur:
        cur.execute(query)
    privilegios = cur.fetchall()
    conexion.close()
    return privilegios


# query para agregar un usuario
def guardar_usuario(idRecurso, nombreUsuario, contrasena, idRol):
    conexion = get_conexion()
    query = """INSERT INTO usuario (IdRecurso, Nombre, Contraseña, IdRol, FechaAlta) 
                VALUES({},'{}','{}',{},NOW())""".format(idRecurso, nombreUsuario, contrasena, idRol)
    nuevo_usuario = None
    with conexion.cursor() as cur:
        cur.execute(query)
        nuevo_usuario = cur.lastrowid
    conexion.commit()
    conexion.close()
    return nuevo_usuario


# query para obtener USUARIO por ID
def obtener_usuario_por_id(idRecurso):
    query = """SELECT IdUsuario, IdRecurso, Nombre, Contraseña, IdRol 
                FROM usuario 
                WHERE IdUsuario = {}
                AND fechabaja is null;""".format(idRecurso)
    conexion = get_conexion()
    usuario_id = None
    with conexion.cursor() as cur:
        cur.execute(query)
    usuario_id = cur.fetchone()
    conexion.close()
    return usuario_id


def chequear_usuario_existente_by_nombre(nombre_usuario):
    query = """
            SELECT * FROM usuario
            WHERE nombre = '{}'
            AND FechaBaja is null;
            """.format(nombre_usuario)
    logger.info("chequear nombre usuario -> {}".format(query))
    conexion = get_conexion()
    usuario_existente = None
    with conexion.cursor() as cur:
        cur.execute(query)
        usuario_existente = cur.fetchall()
    conexion.close()
    if usuario_existente != ():
        usuario_existente = True
    else:
        usuario_existente = False
    return usuario_existente


def update_rol_pass_by_id_usuario(id_rol, password, id_usuario):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE usuario 
                          SET FechaModificacion = NOW(),
                          idRol = {},
                          contraseña = {}
                          WHERE IdUsuario = {}""".format(id_rol, password, id_usuario))
    conexion.commit()
    conexion.close()

# Le asigno fecha de baja al usuario


def update_eliminar_usuario(id_usuario):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE usuario 
                          SET FechaBaja = now() 
                          WHERE IdUsuario = {} 
                          AND fechabaja is null""".format(id_usuario))
    conexion.commit()
    conexion.close()
