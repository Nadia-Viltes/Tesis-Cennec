from loguru import logger
from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos


def obtener_lista_turno():
    query = """
           	SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), 
               DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, pac.Apellido, pac.NumeroDocumento, esp.Nombre, 
               tur.IdProfesional, r.nombre, r.apellido
				FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp, profesional as p, recurso as r
				WHERE tur.IdEstadoTurno = est.IdEstadoTurno
				AND tur.IdPaciente = pac.IdPaciente
				AND tur.IdEspecialidad = esp.IdEspecialidad
                AND tur.IdProfesional = p.IdProfesional
                AND p.IdRecurso = r.IdRecurso
				AND tur.FechaBaja is null
                order by tur.FechaTurno asc, tur.HoraDesde asc;          
            """
    conexion = get_conexion()
    turno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turno = cur.fetchall()
    conexion.close()
    return turno

    # Select tipo de turno - Lista de valores


def obtener_tipoTurno():
    query = "SELECT IdTipoTurno, Nombre FROM tipoturno WHERE FechaBaja is null;"
    conexion = get_conexion()
    tipoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    tipoTurno = cur.fetchall()
    conexion.close()
    return tipoTurno

# Select Especialidades - Lista de valores


def obtener_especialidad_turnos(id):
    query = """Select IdEspecialidad, Nombre from especialidad 
    WHERE IdEspecialidad in (Select esp.IdEspecialidad from configuracionturno as config, especialidad as esp 
    WHERE config.IdEspecialidad = esp.IdEspecialidad AND config.CantidadComputados <> config.CantidadDisponibles 
    AND config.FechaBaja is null AND config.IdPaciente = {})""".format(id)
    conexion = get_conexion()
    IdEspecialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    IdEspecialidad = cur.fetchall()
    conexion.close()
    return IdEspecialidad


# Select profesionales según especialidad - Lista de valores
def obtener_profesionales_especialidad(id):
    query = """
            SELECT pro.idprofesional, rec.nombre, rec.apellido, esp.idespecialidad, esp.nombre
            FROM profesional AS pro, recurso AS rec, especialidad AS esp
            WHERE pro.idespecialidad = esp.idespecialidad
            AND pro.idrecurso = rec.idrecurso
            AND pro.FechaBaja is null
            AND esp.IdEspecialidad = {};""".format(id)
    conexion = get_conexion()
    profesionales_especialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    profesionales_especialidad = cur.fetchall()
    conexion.close()
    return profesionales_especialidad


def obtener_turno_por_id(id_turno):
    query = """SELECT est.IdEstadoTurno, est.Nombre, tur.FechaTurno, DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, 
                pac.Apellido, pac.NumeroDocumento, tt.IdTipoTurno, tt.Nombre, tur.IdEspecialidad, esp.Nombre, prof.IdProfesional,rec.Nombre, rec.apellido, tur.IdTurno
                FROM estadoturno AS est, turno AS tur, tipoturno AS tt, paciente AS pac, especialidad AS esp , profesional AS prof,recurso AS rec
                WHERE est.IdEstadoTurno = tur.IdEstadoTurno
                AND pac.IdPaciente = tur.IdPaciente
                AND tur.IdTipoTurno = tt.IdTipoTurno
                AND tur.IdEspecialidad = esp.IdEspecialidad
                AND prof.idEspecialidad = esp.IdEspecialidad
                AND prof.IdProfesional = tur.IdProfesional
                AND prof.IdRecurso = rec.IdRecurso
                AND tur.FechaBaja is null
                AND tur.IdTurno = {}""".format(id_turno)
    conexion = get_conexion()
    id_turno = None
    with conexion.cursor() as cur:
        cur.execute(query), (id_turno)
    id_turno = cur.fetchone()
    conexion.close()
    return id_turno


def validar_tiene_detalle_evolucion_turno(id_turno):
    query = """
            select * 
            from detalleevolucion
            where idTurno = {};
            """.format(id_turno)
    logger.info("validar_tiene_detalle_evolucion_turno -> {}".format(query))
    conexion = get_conexion()
    tiene_detalle = None
    with conexion.cursor() as cur:
        cur.execute(query)
        tiene_detalle = cur.fetchall()
    conexion.close()
    if tiene_detalle != ():
        tiene_detalle = True
    else:
        tiene_detalle = False
    return tiene_detalle


def chequear_turno_atendido(id_turno):
    query = """
            select * from turno
            where idTurno = {}
            and idEstadoTurno in (Select IdEstadoTurno 
                                FROM estadoturno
                                WHERE nombre = "Atendido");
            """.format(id_turno)
    logger.info("chequar_turno_atendido -> {}".format(query))
    conexion = get_conexion()
    turno_atendido = None
    with conexion.cursor() as cur:
        cur.execute(query)
        turno_atendido = cur.fetchall()
    conexion.close()
    if turno_atendido != ():
        turno_atendido = True
    else:
        turno_atendido = False
    return turno_atendido

# Lista de valores de MOTIVOS de anulación de turnos


def obtener_motivoTurno():
    query = "SELECT IdMotivo, NombreMotivo FROM motivo WHERE FechaBaja is null;"
    conexion = get_conexion()
    motivoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivoTurno = cur.fetchall()
    conexion.close()
    return motivoTurno


def obtener_motivo_turno_by_id(id_motivo):
    query = "SELECT IdMotivo, NombreMotivo FROM motivo WHERE FechaBaja is null AND IdMotivo = {};".format(
        id_motivo)
    conexion = get_conexion()
    motivoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivoTurno = cur.fetchone()
    conexion.close()
    return motivoTurno

# Acá obtengo el ID del turno que está macheado en el app.py


def obtener_id_estado_turno_por_estado(estado):
    query = "SELECT IdEstadoTurno FROM estadoturno WHERE LOWER(Nombre) like LOWER('{}') AND FechaBaja is null".format(
        estado)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    id_estado_turno = cur.fetchone()[0]
    print("esto tiene mi fetchone -> {}".format(id_estado_turno))
    conexion.close()
    return id_estado_turno


# Agregar un nuevo turno en estado asignado:
def insertar_turno_asignado(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaAsignado, IdUsuarioAsignado, FechaAlta)
        VALUES ({},{},{},{},'{}','{}','{}',{},now(),{},now())""".format(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario)
    print("Este es mi insertar turno asignado -> {}".format(query))
    idTurno_asignado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_asignado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_asignado


def chequear_turno_existente(id_profesional, fecha_turno, hora_desde):
    query = """
            SELECT *
            FROM turno as t
            WHERE IdProfesional = {0}
            AND t.FechaTurno = '{1}'
            AND DATE_FORMAT(t.HoraDesde, '%H:%i') = '{2}'
            AND t.FechaBaja is null;
            """.format(id_profesional, fecha_turno, hora_desde)
    logger.info("chequar_turno_existente -> {}".format(query))
    conexion = get_conexion()
    turno_existente = None
    with conexion.cursor() as cur:
        cur.execute(query)
        turno_existente = cur.fetchall()
    conexion.close()
    if turno_existente != ():
        turno_existente = True
    else:
        turno_existente = False
    return turno_existente


def chequea_horario_ocupado_paciente(id_paciente, fecha_turno, hora_desde):
    query = """
            SELECT *
            FROM turno as t
            WHERE IdPaciente= {0}
            AND t.FechaTurno = '{1}'
            AND DATE_FORMAT(t.HoraDesde, '%H:%i') = '{2}'
            AND t.FechaBaja is null;   
            """.format(id_paciente, fecha_turno, hora_desde)
    logger.info("chequar_turno_existente -> {}".format(query))
    conexion = get_conexion()
    horario_ocupado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        horario_ocupado = cur.fetchall()
    conexion.close()
    if horario_ocupado != ():
        horario_ocupado = True
    else:
        horario_ocupado = False
    return horario_ocupado

# Acá obtengo el ID del turno asignado para poder actualizar los turnos computados


def obtener_id_configuracion_turno(id_paciente, id_especialidad):
    query = """
            SELECT IdconfiguracionTurno 
            FROM configuracionTurno 
            WHERE IdPaciente = {} 
            and IdEspecialidad = {} 
            AND FechaBaja is null
            AND CantidadComputados < CantidadDisponibles;""".format(id_paciente, id_especialidad)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    idConfigTurno = cur.fetchone()[0]
    conexion.close()
    return idConfigTurno


def actualizar_turnos_computados(id_configturno):
    conexion = get_conexion()
    query = """UPDATE configuracionTurno 
                SET CantidadComputados=(CantidadComputados + 1),
                FechaModificacion=NOW()
                WHERE IdconfiguracionTurno = {0};""".format(id_configturno)
    print("Este es mi insertar turnos computados -> {}".format(query))
    turnos_computados = None
    with conexion.cursor() as cur:
        cur.execute(query)
        turnos_computados = cur.lastrowid
    conexion.commit()
    conexion.close()
    return turnos_computados


# Agregar un nuevo turno en estado RECEPTADO:
def insertar_turno_receptado(tipoTurno, idEspecialidadDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaReceptado, IdUsuarioReceptado, IdProfesional, IdTurnoOriginal, FechaAlta)
        VALUES ({},{},{},'{}','{}','{}',{},now(),{},{}, {}, now())""".format(tipoTurno, idEspecialidadDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno)
    print("Este es mi insertar turno RECEPTADO -> {}".format(query))
    idTurno_receptado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_receptado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_receptado


# Acá Updateo el turno original (asignado) con la fecha de baja para que solo se vea el receptado:
def update_turno_asignado(IdTurno):
    conexion = get_conexion()
    query = """
        UPDATE turno SET FechaBaja = NOW() WHERE IdTurno = {}""".format(IdTurno)
    print("Este es mi Update en fecha de baja del asignar -> {}".format(query))
    idTurno_asignado_baja = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_asignado_baja = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_asignado_baja


# Agregar un nuevo turno en estado REASIGNADO:
def insertar_turno_reasignado(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, IdTurno, usuario):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaReasignado, IdUsuarioReasignado, TurnoReasignado, IdTurnoReasignado ,FechaAlta)
        VALUES ({},{},{},{},'{}','{}','{}',{},now(), {}, 1, {},now())""".format(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, IdTurno, usuario)
    print("Este es mi insertar turno RECEPTADO -> {}".format(query))
    idTurno_reasignado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_reasignado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_reasignado

 # Acá Updateo el turno original  con la fecha de baja para que solo se vea el reasignado:


def update_turno_reasignado(IdTurno):
    conexion = get_conexion()
    query = """
        UPDATE turno SET FechaBaja = NOW(), IdEstadoTurno = (SELECT IdEstadoTurno FROM estadoturno WHERE nombre like lower('reprogramado')) WHERE IdTurno = {}""".format(IdTurno)
    print("Este es mi Update en fecha de baja del asignar -> {}".format(query))
    idTurno_reasignado_baja = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_reasignado_baja = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_reasignado_baja

    # Listo los turnos que el paciente tiene en asignados para poder anularlos.


def obtener_lista_de_turnos_para_anular(id_paciente, id_especialidad):
    query = """
           	  SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, pac.Apellido, pac.NumeroDocumento, esp.Nombre
                FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp
                WHERE tur.IdEstadoTurno = est.IdEstadoTurno
                AND tur.IdPaciente = pac.IdPaciente
                AND tur.IdEspecialidad = esp.IdEspecialidad
                AND est.Nombre like "Asignado"
                AND tur.FechaBaja is null
                AND pac.IdPaciente = {}
                AND esp.IdEspecialidad = {};               
            """.format(id_paciente, id_especialidad)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    turnoAnular = cur.fetchall()
    conexion.close()
    return turnoAnular


# Este es el select con los datos que me trae la tupla
def obtener_turno_por_id_asignado_anulado(idTurnosAnulados):
    query = """
           	 SELECT IdTurno, IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno
                FROM turno
                WHERE FechaBaja is null
                AND IdTurno = {}""".format(idTurnosAnulados)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    turnoAnular = cur.fetchone()
    conexion.close()
    return turnoAnular

# Agregar un nuevo registro en estado ANULADO:


def insertar_anular_turno(IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, id_estado, motivoTurnosAnulados, usuario, IdTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, 
        IdEstadoTurno, FechaAnulado, IdMotivoAnulado, IdUsuarioAnulado, IdTurnoOriginal, FechaAlta, FechaBaja) 
        VALUES({},{},{},{},'{}','{}','{}',{},NOW(),{},1,{},NOW(),NOW())""".format(IdTipoTurno, IdEspecialidad, IdProfesional, IdPaciente, FechaTurno, HoraDesde, HoraHasta, id_estado, motivoTurnosAnulados, IdTurno)
    logger.info("Este es mi insertar turno anulado -> {}".format(query))
    idTurno_anulado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_anulado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_anulado


# query para que me muestre los datos en la lista de turnos
def obtener_estado_filtro():
    query = """
            SELECT idEstadoTurno, nombre
            FROM estadoturno
            WHERE FechaBaja is null
            AND nombre != lower('anulado')
            AND nombre != lower('libre')
            AND nombre != lower('reprogramado')
            """
    conexion = get_conexion()
    filtro = []
    with conexion.cursor() as cur:
        cur.execute(query)
    filtro = cur.fetchall()
    conexion.close()
    return filtro


def obtener_lista_turnos_por_estado(id_estado):
    query = """
           	SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, pac.Apellido, pac.NumeroDocumento, esp.Nombre
				FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp
				WHERE tur.IdEstadoTurno = est.IdEstadoTurno
				AND tur.IdPaciente = pac.IdPaciente
				AND tur.IdEspecialidad = esp.IdEspecialidad
                AND tur.IdEstadoTurno = {}
				AND tur.FechaBaja is null
                order by tur.FechaTurno asc, tur.HoraDesde asc;          
            """.format(id_estado)
    conexion = get_conexion()
    turno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turno = cur.fetchall()
    conexion.close()
    return turno


def obtener_lista_de_especialidades():
    query = """
           	SELECT * 
            FROM especialidad          
            """
    conexion = get_conexion()
    especialidades = []
    with conexion.cursor() as cur:
        cur.execute(query)
    especialidades = cur.fetchall()
    conexion.close()
    return especialidades
