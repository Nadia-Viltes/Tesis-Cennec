from loguru import logger
from config_bd import get_conexion

# query para que me muestre estado ASIGNADO
def obtener_lista_roles():
    query = """
           SELECT IdRol, Nombre, Descripcion FROM rol 
           WHERE FechaBaja is null
           AND Nombre != lower('Administrador')
           ORDER BY nombre asc;"""
    conexion = get_conexion()
    rol = []
    with conexion.cursor() as cur:
        cur.execute(query)
    rol = cur.fetchall()
    conexion.close()
    return rol

