from loguru import logger
from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno_mi_agenda(usuario):
    query = """
             SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), 
            DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente,pac.Nombre, pac.Apellido, pac.NumeroDocumento, hcd.IdHistoriaClinica, u.Nombre	
            FROM turno as tur, paciente as pac, estadoturno as est, historiaclinica as hcd, usuario as u, recurso as rec, 
            profesional as pro, especialidad as esp
            WHERE hcd.IdPaciente = pac.IdPaciente
            AND pac.IdPaciente = tur.IdPaciente
            AND tur.IdEstadoTurno = est.IdEstadoTurno
            AND tur.IdEspecialidad = esp.IdEspecialidad
            AND esp.IdEspecialidad = pro.IdEspecialidad
            AND pro.IdRecurso = rec.IdRecurso
            AND rec.IdRecurso = u.IdRecurso
            and u.IdUsuario = {}
            AND tur.FechaBaja is null
            AND (tur.IdProfesionalAsignado = pro.idProfesional OR tur.IdProfesionalReceptado = pro.idProfesional)
            order by tur.FechaTurno asc, tur.HoraDesde asc;
            """.format(usuario)
    conexion = get_conexion()
    turnoProfesional = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turnoProfesional = cur.fetchall()
    conexion.close()
    return turnoProfesional


# Query para obtener datos del usuario logueado y rellenar datos en la hcd
def obtener_datos_usuario_profesional(usuario):
    query = """
            SELECT us.IdUsuario, re.Nombre, re.Apellido, esp.Nombre, prof.IdProfesional
            FROM usuario AS us, recurso AS re, profesional as prof, especialidad as esp
            WHERE us.IdRecurso = re.IdRecurso
            AND re.IdRecurso = prof.IdRecurso
            AND prof.IdEspecialidad = esp.IdEspecialidad
            AND us.IdUsuario = {};""".format(usuario)
    conexion = get_conexion()
    usuarioProfesional = []
    with conexion.cursor() as cur:
        cur.execute(query)
    usuarioProfesional = cur.fetchone()
    conexion.close()
    return usuarioProfesional


# Query para obtener el dato del IdProfesional logueado
def obtener_id_profesional(usuario):
    query = """
            SELECT p.IdProfesional FROM usuario as us, recurso as r, profesional as p
            WHERE us.IdRecurso = r.IdRecurso
            AND r.IdRecurso = p.IdRecurso
            AND us.IdUsuario = {};""".format(usuario)
    conexion = get_conexion()
    idProfesional = []
    with conexion.cursor() as cur:
        cur.execute(query)
    idProfesional = cur.fetchone()
    conexion.close()
    return idProfesional



## Ver el ID del turno receptado:
def obtener_turno_agenda_receptado(id_turno):
    query = """SELECT IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdProfesionalReceptado, IdTurnoOriginal 
                FROM turno
                WHERE FechaBaja is null
                AND IdTurno = {}""".format(id_turno)
    conexion = get_conexion()
    agenda_receptado = None
    with conexion.cursor() as cur:
        cur.execute(query),(id_turno)
    agenda_receptado = cur.fetchone()
    conexion.close()
    return agenda_receptado

# query para obtener los datos del turno
def obtener_turno_atendiendo(idTurno):
    query = """
           SELECT IdTurno, IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, 
           FechaInicioAtencion, IdUsuarioInicioAtencion, IdTurnoOriginal
            FROM turno
            WHERE IdTurno = {}""".format(idTurno)
    conexion = get_conexion()
    idTurnoAtendiendo = []
    with conexion.cursor() as cur:
        cur.execute(query)
    idTurnoAtendiendo = cur.fetchone()
    conexion.close()
    return idTurnoAtendiendo

# query para si ya existe un detalle con ese turno
def obtener_detalle_con_turno(idTurno):
    query = """
           SELECT IdTurno FROM detalleevolucion WHERE IdTurno = {};""".format(idTurno)
    conexion = get_conexion()
    detalleTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    detalleTurno = cur.fetchone()
    conexion.close()
    return detalleTurno
    
## Agregar un nuevo turno en estado ATENDIENDO:
def insertar_turno_atendiendo(tipoTurno, idEspecialidad, idPaciente, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaInicioAtencion, IdUsuarioInicioAtencion, IdProfesionalReceptado, IdTurnoOriginal, FechaAlta,IdUsuarioAlta)
        VALUES ({},{},{},'{}','{}','{}',{},now(),{},{}, {}, now(),{})""".format(tipoTurno, idEspecialidad, idPaciente, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno,usuario)
    print("Este es mi insertar turno ATENDIENDO -> {}".format(query))    
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_atendiendo = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_atendiendo

## Agregar un nuevo turno en estado ATENDIENDO:
def insertar_turno_atendiendo(tipoTurno, idEspecialidad, idPaciente, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaFinalAtencion, IdUsuarioFinalAtencion, IdProfesionalReceptado, IdTurnoOriginal, FechaAlta,IdUsuarioAlta)
        VALUES ({},{},{},'{}','{}','{}',{},now(),{},{}, {}, now(),{})""".format(tipoTurno, idEspecialidad, idPaciente, fechaTurno, horaDesde, horaHasta, idEstadoTurno, usuario, idProfesionalDropdown, IdTurno,usuario)
    print("Este es mi insertar turno ATENDIENDO -> {}".format(query))    
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_atendido = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_atendido

# Lista de los detalles de la evolución para que se muestren en el historial.
def obtener_historial_evoluciones(id):
    query = """
           SELECT hcd.IdHistoriaClinica, hcd.IdPaciente, e.IdEvolucion, e.IdHistoriaClinica, de.IdDetalleEvolucion, de.IdEvolucion, 
           de.IdTurno, de.IdProfesional, de.ObservacionAvance, r.Nombre, r.Apellido, esp.Nombre, DATE_FORMAT(de.FechaAlta, '%d-%m-%Y')
            FROM historiaclinica as hcd, evolucion as e, detalleevolucion as de, profesional as p, especialidad as esp, recurso as r
            WHERE hcd.IdHistoriaClinica = e.IdHistoriaClinica
            AND e.IdEvolucion = de.IdEvolucion
            AND de.IdProfesional = p.IdProfesional
            AND p.IdEspecialidad = esp.IdEspecialidad
            AND p.IdRecurso = r.IdRecurso
            AND hcd.IdPaciente = {};               
            """.format(id)
    conexion = get_conexion()
    historial = []
    with conexion.cursor() as cur:
        cur.execute(query)
    historial = cur.fetchall()
    conexion.close()
    return historial

# Acá muestro el historial seleccionado
def obtener_detalle_historial(id):
    query = """
           SELECT hcd.IdHistoriaClinica, hcd.IdPaciente, e.IdEvolucion, e.IdHistoriaClinica, de.IdDetalleEvolucion, 
            de.IdEvolucion, de.IdTurno, de.IdProfesional, de.ObservacionAvance, r.Nombre, r.Apellido, esp.Nombre,
            pac.Nombre, pac.Apellido, pac.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0'), fin.Nombre, 
            afi.NumeroAfiliado, DATE_FORMAT(de.FechaAlta,"%d-%m-%Y"), DATE_FORMAT(de.FechaAlta,'%H:%i') TIMEONLY
            FROM historiaclinica as hcd, evolucion as e, detalleevolucion as de, profesional as p, especialidad as esp, 
            recurso as r, paciente as pac, financiador as fin, afiliacion as afi
            WHERE hcd.IdHistoriaClinica = e.IdHistoriaClinica
            AND e.IdEvolucion = de.IdEvolucion
            AND hcd.IdPaciente = pac.IdPaciente
            AND de.IdProfesional = p.IdProfesional
            AND p.IdEspecialidad = esp.IdEspecialidad
            AND p.IdRecurso = r.IdRecurso
            AND afi.IdPaciente = pac.IdPaciente
            AND afi.IdFinanciador = fin.IdFinanciador
            AND de.IdDetalleEvolucion = {};""".format(id)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    detalle_historial = cur.fetchone()
    conexion.close()
    return detalle_historial


## CONSULTA SI ESTÁ LA EVOLUCION
def consulta_existe_evolucion(id):
    query = """
           SELECT IdEvolucion FROM evolucion 
		   WHERE IdHistoriaClinica = {};""".format(id)
    print("Este es mi ver si existe evolucion -> {}".format(query))   
    conexion = get_conexion()
    existe_evolucion = None
    try:
        with conexion.cursor() as cur:
            cur.execute(query)
        existe_evolucion = cur.fetchone()[0]
    except:
        logger.info("Ocurrio un error obteniendo datos")
    finally:        
        conexion.close()
    return existe_evolucion


## INSERTAR EVOLUCION
def insertar_evolucion (idHCD,usuario):
    conexion = get_conexion()
    query = """
        INSERT INTO evolucion (IdHistoriaClinica, FechaAlta, IdUsuarioAlta)
        VALUES ({}, now(),{})""".format(idHCD,usuario)
    idEvolucion = None
    print("Insertar idEvolucion -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        idEvolucion = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idEvolucion



## INSERTAR DETALLE DE ESA EVOLUCION
def insertar_detalle (idEvolucion, idTurno, idProfesional, observacion, usuario):
    conexion = get_conexion()
    query = """
        INSERT INTO detalleevolucion (IdEvolucion, IdTurno, IdProfesional, ObservacionAvance, FechaAlta, IdUsuarioAlta)
		VALUES({},{},{},'{}',now(),{})""".format(idEvolucion, idTurno, idProfesional, observacion, usuario)    
    idEvolucion = None
    print("Insertar detalle -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        idEvolucion = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idEvolucion


## Operación para modificar el detall de la HCD
def actualizar_detalle(inputIdEvolucion,inputIdTurnoHis,inputProfesionalHis,InputTextareaEvolucionesHis,usuario,inputIdDetEvo):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
        UPDATE detalleevolucion SET IdEvolucion={}, IdTurno={}, IdProfesional={}, ObservacionAvance='{}',FechaModificacion=NOW(), IdUsuarioModificacion={}
        WHERE IdDetalleEvolucion = {} """.format(inputIdEvolucion,inputIdTurnoHis,inputProfesionalHis,InputTextareaEvolucionesHis,usuario,inputIdDetEvo))
    conexion.commit()
    conexion.close()