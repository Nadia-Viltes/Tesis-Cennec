from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno_mi_agenda():
    query = """SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), 
            DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente,pac.Nombre, pac.Apellido, pac.NumeroDocumento, hcd.IdHistoriaClinica	
            FROM turno as tur, paciente as pac, estadoturno as est, historiaclinica as hcd
            WHERE tur.IdPaciente = pac.IdPaciente
            AND pac.IdPaciente = hcd.IdPaciente
            AND est.IdEstadoTurno = tur.IdEstadoTurno
            AND tur.IdProfesionalReceptado = 1;              
            """
    conexion = get_conexion()
    turnoProfesional = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turnoProfesional = cur.fetchall()
    conexion.close()
    return turnoProfesional


## Agregar un nuevo turno en estado ATENDIENDO:
def insertar_turno_atendiendo(tipoTurno, idEspecialidadDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, idProfesionalDropdown, IdTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaInicioAtencion, IdUsuarioInicioAtencion, IdProfesionalReceptado, IdTurnoOriginal, FechaAlta)
        VALUES ({},{},{},'{}','{}','{}',{},now(),1,{}, {}, now())""".format(tipoTurno, idEspecialidadDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno, idProfesionalDropdown, IdTurno)
    print("Este es mi insertar turno ATENDIENDO -> {}".format(query))    
    idTurno_atendiendo = None    
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_atendiendo = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_atendiendo

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
    with conexion.cursor() as cur:
        cur.execute(query)
    existe_evolucion = cur.fetchone()[0]
    conexion.close()
    return existe_evolucion


## INSERTAR EVOLUCION
def insertar_evolucion (idHCD):
    conexion = get_conexion()
    query = """
        INSERT INTO evolucion (IdHistoriaClinica, FechaAlta)
        VALUES ({}, now())""".format(idHCD)
    idEvolucion = None
    print("Insertar idEvolucion -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        idEvolucion = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idEvolucion



## INSERTAR DETALLE DE ESA EVOLUCION
def insertar_detalle (idEvolucion,idProfesional,observacion):
    conexion = get_conexion()
    query = """
        INSERT INTO detalleevolucion (IdEvolucion, IdTurno, IdProfesional, ObservacionAvance, FechaAlta)
		VALUES({},{},{},'{}',now())""".format(idEvolucion,idProfesional,observacion)
    idEvolucion = None
    print("Insertar detalle -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        idEvolucion = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idEvolucion