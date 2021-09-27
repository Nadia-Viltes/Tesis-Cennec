from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno():
    query = """
           SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.Nombre, pac.Apellido, pac.NumeroDocumento,
            esp.Nombre, rec.Nombre
            FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp , profesional AS prof, recurso AS rec
            WHERE est.IdEstadoTurno = tur.IdEstadoTurno
            AND pac.IdPaciente = tur.IdPaciente
            AND tur.IdEspecialidad = esp.IdEspecialidad
            AND prof.idEspecialidad = esp.IdEspecialidad
            AND prof.IdRecurso = rec.IdRecurso;             
            """
    conexion = get_conexion()
    turno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turno = cur.fetchall()
    conexion.close()
    return turno

    ## Select tipo de turno - Lista de valores
def obtener_tipoTurno(): 
    query = "SELECT IdTipoTurno, Nombre FROM tipoturno WHERE FechaBaja is null;"
    conexion = get_conexion()
    tipoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    tipoTurno = cur.fetchall()
    conexion.close()
    return tipoTurno

## Select Especialidades - Lista de valores
def obtener_especialidad_turnos(): 
    query = "SELECT IdEspecialidad, Nombre FROM especialidad WHERE FechaBaja is null;"
    conexion = get_conexion()
    IdEspecialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    IdEspecialidad = cur.fetchall()
    conexion.close()
    return IdEspecialidad
    

def obtener_turno_por_id(id_turno):
    query = """SELECT est.IdEstadoTurno, est.Nombre, tur.FechaTurno, DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.Nombre, pac.Apellido, 
                pac.NumeroDocumento, esp.Nombre, rec.Nombre, tur.IdEspecialidad
                FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp , profesional AS prof, recurso AS rec
                WHERE est.IdEstadoTurno = tur.IdEstadoTurno
                AND pac.IdPaciente = tur.IdPaciente
                AND tur.IdEspecialidad = esp.IdEspecialidad
                AND prof.idEspecialidad = esp.IdEspecialidad
                AND prof.IdRecurso = rec.IdRecurso
                AND tur.IdTurno = {}""".format(id_turno)
    conexion = get_conexion()
    id_turno = None
    with conexion.cursor() as cur:
        cur.execute(query),(id_turno,)
    id_turno = cur.fetchone()
    conexion.close()
    return id_turno


## Lista de valores de MOTIVOS de anulación de turnos
def obtener_motivoTurno(): 
    query = "SELECT IdMotivo, NombreMotivo FROM motivo WHERE FechaBaja is null;"
    conexion = get_conexion()
    motivoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivoTurno = cur.fetchall()
    conexion.close()
    return motivoTurno