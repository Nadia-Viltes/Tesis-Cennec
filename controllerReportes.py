from loguru import logger
from config_bd import get_conexion

# query para que me muestre estado ASIGNADO
def obtener_estados_turnos():
    query = """
           SELECT @rownum := @rownum + 1 AS 'rank', count(*) as total, et.nombre 
            FROM turno as t, estadoturno as et, (SELECT @rownum := 0) r
            WHERE t.IdEstadoTurno = et.IdEstadoTurno
            GROUP BY et.nombre;"""
    conexion = get_conexion()
    reporte_turnos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    reporte_turnos = cur.fetchall()
    conexion.close()
    return reporte_turnos

# query para ver el periodo de los totales
def obtener_periodos():
    query = """
           SELECT (SELECT count(*) FROM turno WHERE FechaBaja is null
            AND FechaTurno BETWEEN CURDATE() - INTERVAL 1 MONTH  AND CURDATE()) AS mes_actual, 
            (SELECT count(*) FROM turno WHERE FechaBaja is null
            AND FechaTurno BETWEEN CURDATE() - INTERVAL 2 MONTH  AND CURDATE() - INTERVAL 1 MONTH) as mes_anterior, 
            ((SELECT count(*) FROM turno WHERE FechaBaja is null
            AND FechaTurno BETWEEN CURDATE() - INTERVAL 1 MONTH  AND CURDATE()) - (SELECT count(*) 
            FROM turno WHERE FechaBaja is null
            AND FechaTurno BETWEEN CURDATE() - INTERVAL 2 MONTH  AND CURDATE() - INTERVAL 1 MONTH)) as resta"""
    conexion = get_conexion()
    periodos_turnos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    periodos_turnos = cur.fetchone()
    conexion.close()
    return periodos_turnos