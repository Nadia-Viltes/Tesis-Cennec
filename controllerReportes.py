from loguru import logger
from config_bd import get_conexion

# query para que me muestre estado ASIGNADO


def obtener_estados_turnos():
    query = """
            SELECT count(*) as total, et.nombre 
            FROM turno as t, estadoturno as et
            WHERE t.IdEstadoTurno = et.IdEstadoTurno
            GROUP BY et.nombre;"""
    conexion = get_conexion()
    reporte_turnos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    reporte_turnos = cur.fetchall()
    conexion.close()
    return reporte_turnos


def obtener_motivos_anulacion():
    query = """
            SELECT count(*), m.NombreMotivo FROM turno as t, motivo as m
            WHERE t.IdMotivoAnulado = m.IdMotivo
            GROUP BY t.IdMotivoAnulado;
            """
    conexion = get_conexion()
    motivos_anulacion = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivos_anulacion = cur.fetchall()
    conexion.close()
    return motivos_anulacion
# query para ver el periodo de los totales


def obtener_ranking_obras_sociales():
    query = """
            SELECT count(*), fin.Nombre FROM afiliacion as afi, financiador as fin
            WHERE afi.IdFinanciador = fin.IdFinanciador
            group by afi.IdFinanciador
            """
    conexion = get_conexion()
    ranking = []
    with conexion.cursor() as cur:
        cur.execute(query)
    ranking = cur.fetchall()
    conexion.close()
    return ranking


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


def cantidad_turnos_asignados_por_mes_y_anio(mes, anio):
    query = """
            SELECT COUNT(*) FROM TURNO
            WHERE idEstadoTurno IN ( select idEstadoTurno from estadoturno where LOWER(nombre) = "asignado")
            AND DATE_FORMAT(FechaTurno, "%m") = {}
            AND DATE_FORMAT(FechaTurno, "%Y") = {};"""
    conexion = get_conexion()
    cantidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    cantidad = cur.fetchone()
    conexion.close()
    return cantidad