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


def obtener_genero_especialidades():
    query = """
            select count(*), nombre, genero
            from (select esp.Nombre, pac.Genero
                    from turno tur, especialidad esp, paciente pac
                    where tur.IdEstadoTurno in (select IdEstadoTurno 
                                                from estadoturno
                                                where nombre = "Asignado")
                    and esp.IdEspecialidad = tur.idEspecialidad
                    and tur.idPaciente = pac.idPaciente
                    group by esp.Nombre, pac.IdPaciente, pac.genero) a
            group by nombre, genero
            order by nombre, genero desc;  
            """
    conexion = get_conexion()
    genero_especialidades = []
    with conexion.cursor() as cur:
        cur.execute(query)
    genero_especialidades = cur.fetchall()
    conexion.close()
    return genero_especialidades


def obtener_horas_trabajadas_profesional(fecha_desde, fecha_hasta):
    query = """
            select re.nombre, re.apellido, format(count(*) / 2, 1) as "horas trabajadas" 
            from turno as tur, profesional pro, recurso re
            where idEstadoTurno = (select idEstadoTurno 
                                    from estadoturno
                                    where nombre = 'Receptado')
            and pro.idRecurso = re.IdRecurso
            and tur.IdProfesional = pro.Idprofesional 
            and tur.FechaAlta >= '{}'
            and tur.FechaAlta <= '{}'                       
            group by tur.idProfesional;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    horas_trabajadas = []
    with conexion.cursor() as cur:
        cur.execute(query)
    horas_trabajadas = cur.fetchall()
    conexion.close()
    return horas_trabajadas


def obtener_estado_turno_parametro_edades(fecha_desde, fecha_hasta):
    query = """
            SELECT COUNT(*) AS "Cantidad", "Primera Infancia (0-5 años)" AS "Categoria", et.Nombre
            FROM paciente as p, turno as t, estadoturno AS et
            WHERE p.IdPaciente = t.IdPaciente
            AND t.IdEstadoTurno = et.IdEstadoTurno
            AND TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 0
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 5
            AND t.FechaTurno >= '{0}'
            AND t.FechaTurno <= '{1}'
            AND t.IdEstadoTurno in (select idEstadoTurno 
						from estadoturno
						where nombre not in ('Receptado', 'Atendiendo'))
            GROUP BY t.IdEstadoTurno
            UNION
            SELECT COUNT(*) AS "Cantidad", "Infancia (6 - 11 años)" AS "Categoria", et.Nombre
            FROM paciente as p, turno as t, estadoturno as et
            WHERE p.IdPaciente = t.IdPaciente
            AND t.IdEstadoTurno = et.IdEstadoTurno
            AND TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 6
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 11
            AND t.FechaTurno >= '{0}'
            AND t.FechaTurno <= '{1}'
            AND t.IdEstadoTurno in (select idEstadoTurno 
						from estadoturno
						where nombre not in ('Receptado', 'Atendiendo'))
            GROUP BY t.IdEstadoTurno
            UNION
            SELECT COUNT(*) AS "Cantidad", "Adolescencia (12 - 18 años)" AS "Categoria", et.Nombre
            FROM paciente as p, turno as t, estadoturno as et
            WHERE p.IdPaciente = t.IdPaciente
            AND t.IdEstadoTurno = et.IdEstadoTurno
            AND TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 12
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 18
            AND t.FechaTurno >= '{0}'
            AND t.FechaTurno <= '{1}'
            AND t.IdEstadoTurno in (select idEstadoTurno 
						from estadoturno
						where nombre not in ('Receptado', 'Atendiendo'))
            GROUP BY t.IdEstadoTurno
            UNION
            SELECT COUNT(*) AS "Cantidad", "Juventud (14 - 26 años)" AS "Categoria", et.Nombre
            FROM paciente as p, turno as t, estadoturno as et
            WHERE p.IdPaciente = t.IdPaciente
            AND t.IdEstadoTurno = et.IdEstadoTurno
            AND TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 14
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 26
            AND t.FechaTurno >= '{0}'
            AND t.FechaTurno <= '{1}'
            AND t.IdEstadoTurno in (select idEstadoTurno 
						from estadoturno
						where nombre not in ('Receptado', 'Atendiendo'))
            GROUP BY t.IdEstadoTurno
            UNION
            SELECT COUNT(*) AS "Cantidad", "Adultez (27 o más años)" AS "Categoria", et.Nombre
            FROM paciente as p, turno as t, estadoturno as et
            WHERE p.IdPaciente = t.IdPaciente
            AND t.IdEstadoTurno = et.IdEstadoTurno
            AND TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 27
            AND t.FechaTurno >= '{0}'
            AND t.FechaTurno <= '{1}'
            AND t.IdEstadoTurno in (select idEstadoTurno 
						from estadoturno
						where nombre not in ('Receptado', 'Atendiendo'))
            GROUP BY t.IdEstadoTurno;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    estados_turnos_parametros_edades = []
    with conexion.cursor() as cur:
        cur.execute(query)
    estados_turnos_parametros_edades = cur.fetchall()
    conexion.close()
    return estados_turnos_parametros_edades


def obtener_ranking_de_pacientes_cantidad_turnos():
    query = """
            select sum(ctur.cantidadDisponibles), pac.nombre, pac.apellido
            from configuracionturno ctur,
            paciente pac
            where ctur.IdPaciente = pac.IdPaciente
            group by ctur.idPaciente
            limit 10;
            """
    conexion = get_conexion()
    pacientes = []
    with conexion.cursor() as cur:
        cur.execute(query)
    pacientes = cur.fetchall()
    conexion.close()
    return pacientes


def obtener_recursos(fecha_desde, fecha_hasta):
    query = """
            select rec.IdRecurso, rec.nombre, rec.apellido, trec.nombre, esp.nombre
            from recurso rec, 
            tiporecurso trec,
            profesional pro,
            especialidad esp
            where rec.idTipoRecurso = trec.idTipoRecurso
            and pro.IdRecurso = rec.IdRecurso
            and pro.IdEspecialidad = esp.idEspecialidad
            and rec.fechaalta >= '{0}'
            and rec.fechaalta <= '{1}'
            and trec.nombre <> 'sistemas'
            UNION
            select rec.IdRecurso, rec.nombre, rec.apellido, trec.nombre, "N/A"
            from recurso rec, 
            tiporecurso trec
            where rec.idTipoRecurso = trec.idTipoRecurso
            and rec.fechaalta >= '{0}'
            and rec.fechaalta <= '{1}'
            and trec.nombre not in ('sistemas', 'profesional');
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    recursos = []
    with conexion.cursor() as cur:
        cur.execute(query)
    recursos = cur.fetchall()
    conexion.close()
    return recursos


def obtener_lista_profesionales():
    query = """
            select rec.IdRecurso, rec.nombre, rec.apellido 
            from profesional pro, recurso rec
            where pro.IdRecurso = rec.idRecurso;
            """
    conexion = get_conexion()
    lista_profesionales = []
    with conexion.cursor() as cur:
        cur.execute(query)
    lista_profesionales = cur.fetchall()
    conexion.close()
    return lista_profesionales


def obtener_parametros_edades():
    query = """
            SELECT COUNT(*) AS "Cantidad", "Primera Infancia (0-5 años)" AS "Categoria" 
            FROM paciente as p
            WHERE TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 0
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 5
            UNION
            SELECT COUNT(*) AS "Cantidad", "Infancia (6 - 11 años)" AS "Categoria" 
            FROM paciente as p
            WHERE TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 6
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 11
            UNION
            SELECT COUNT(*) AS "Cantidad", "Adolescencia (12 - 18 años)" AS "Categoria" 
            FROM paciente as p
            WHERE TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 12
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 18
            UNION
            SELECT COUNT(*) AS "Cantidad", "Juventud (14 - 26 años)" AS "Categoria" 
            FROM paciente as p
            WHERE TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 14
            AND  TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) <= 26
            UNION
            SELECT COUNT(*) AS "Cantidad", "Adultez (27 o más años)" AS "Categoria" 
            FROM paciente as p
            WHERE TIMESTAMPDIFF(YEAR, p.fechaNacimiento , now()) >= 27;
            """
    conexion = get_conexion()
    parametros_edades = []
    with conexion.cursor() as cur:
        cur.execute(query)
    parametros_edades = cur.fetchall()
    conexion.close()
    return parametros_edades


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


def obtener_motivos_anulacion_especialidad(fecha_desde, fecha_hasta):
    query = """
            SELECT count(*), e.nombre, m.NombreMotivo
            FROM turno as t, especialidad as e, motivo as m
            WHERE t.IdEspecialidad = e.IdEspecialidad
            AND t.IdMotivoAnulado = m.IdMotivo
            AND t.FechaTurno >= '{}'
            AND t.FechaTurno <= '{}'
            group by t.IdEspecialidad, m.NombreMotivo;
            """.format(fecha_desde, fecha_hasta)
    conexion = get_conexion()
    motivos_anulacion_especialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivos_anulacion_especialidad = cur.fetchall()
    conexion.close()
    return motivos_anulacion_especialidad


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
            group by IdTipoPatologia
            ORDER BY esp.nombre;
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
