from loguru import logger
from config_bd import get_conexion

# query para que me muestre estado ASIGNADO


def obtener_estados_turnos(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*) as total, et.nombre 
            FROM turno as t, estadoturno as et
            WHERE t.IdEstadoTurno = et.IdEstadoTurno
            AND t.FechaTurno >= '{}'
            AND t.FechaTurno <= '{}'
            GROUP BY et.nombre;""".format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    reporte_turnos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    reporte_turnos = cur.fetchall()
    conexion.close()
    return reporte_turnos


def obtener_motivos_anulacion(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*), m.NombreMotivo FROM turno as t, motivo as m
            WHERE t.IdMotivoAnulado = m.IdMotivo
            AND t.FechaTurno >= '{}'
            AND t.FechaTurno <= '{}'
            GROUP BY t.IdMotivoAnulado;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    motivos_anulacion = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivos_anulacion = cur.fetchall()
    conexion.close()
    return motivos_anulacion
# query para ver el periodo de los totales


def obtener_ranking_obras_sociales(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*), fin.Nombre 
            FROM afiliacion as afi, financiador as fin
            WHERE afi.IdFinanciador = fin.IdFinanciador
            AND fin.FechaAlta >= '{}'
            AND fin.FechaAlta <= '{}'
            group by afi.IdFinanciador;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    ranking = []
    with conexion.cursor() as cur:
        cur.execute(query)
    ranking = cur.fetchall()
    conexion.close()
    return ranking


def obtener_turnos_por_especialidad(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*), e.nombre FROM turno as t, especialidad as e
            WHERE t.IdEspecialidad = e.IdEspecialidad
            AND t.FechaTurno >= '{}'
            AND t.FechaTurno <= '{}'
            AND t.FechaBaja is null
            group by t.IdEspecialidad;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    turnos_especialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turnos_especialidad = cur.fetchall()
    conexion.close()
    return turnos_especialidad


def obtener_atencion_profesional(fecha_desde, fecha_hasta):
    query = """
            select count(*), esp.nombre, tur.IdProfesional, rec.nombre, rec.apellido
            from turno as tur, especialidad as esp, profesional as prof, recurso as rec
            where tur.IdEspecialidad = esp.idEspecialidad
            and prof.IdProfesional = tur.IdProfesional
            and rec.IdRecurso = prof.IdRecurso
            and tur.idEstadoTurno = (select idEstadoTurno 
                                    from estadoturno 
                                    where LOWER(nombre) = 'Receptado')
            AND tur.FechaTurno >= '{}'
			AND tur.FechaTurno <= '{}'
            group by tur.IdEspecialidad, tur.IdProfesional
            order by esp.nombre;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    atencion_profesional = []
    with conexion.cursor() as cur:
        cur.execute(query)
    atencion_profesional = cur.fetchall()
    conexion.close()
    return atencion_profesional


def obtener_patologias_admision(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*), config.IdEspecialidad, esp.nombre, config.IdTipoPatologia, tp.nombre
            FROM configuracionturno as config, especialidad as esp, tipopatologia as tp
            WHERE config.IdEspecialidad = esp.IdEspecialidad
            AND config.IdTipoPatologia = tp.IdTipoPatologia
            AND config.FechaAlta >= '{}'
			AND config.FechaAlta <= '{}' 
            group by IdTipoPatologia;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    patologias_admision = []
    with conexion.cursor() as cur:
        cur.execute(query)
    patologias_admision = cur.fetchall()
    conexion.close()
    return patologias_admision


def obtener_altas_mensuales_por_genero():
    query = """
            SELECT count(*), genero, MONTH(FechaAlta)
            FROM paciente
            group by genero, MONTH(FechaAlta)
            ORDER BY MONTH(FechaAlta) asc;
            """
    conexion = get_conexion()
    altas_mensuales_por_genero = []
    with conexion.cursor() as cur:
        cur.execute(query)
    altas_mensuales_por_genero = cur.fetchall()
    conexion.close()
    return altas_mensuales_por_genero


def obtener_alta_paciente_por_zonas():
    query = """
            SELECT count(*), b.detalle 
            FROM paciente as p, domicilio as d, barrio as b
            WHERE p.IdDomicilio = d.IdDomicilio
            AND d.IdBarrio = b.IdBarrio
            GROUP BY b.detalle
            """
    conexion = get_conexion()
    alta_pacientes_por_zona = []
    with conexion.cursor() as cur:
        cur.execute(query)
    alta_pacientes_por_zona = cur.fetchall()
    conexion.close()
    return alta_pacientes_por_zona


def obtener_detalle_barrios():
    query = """
            select detalle from barrio
            group by detalle;
            """
    conexion = get_conexion()
    detalles_barrio = []
    with conexion.cursor() as cur:
        cur.execute(query)
    detalles_barrio = cur.fetchall()
    conexion.close()
    return detalles_barrio


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
