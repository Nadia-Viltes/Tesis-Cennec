from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno():
    query = """
           SELECT tur.IdTurno, est.Nombre, tur.FechaTurno, tur.HoraDesde, tur.HoraHasta, pac.Nombre, pac.Apellido, pac.NumeroDocumento,
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


 ## Select Profesional - Lista de valores
def obtener_profesional(IdEspecialidad): 
    query = """SELECT pro.IdProfesional, rec.Nombre, rec.Apellido FROM profesional as pro, recurso as rec 
            WHERE FechaBaja is null and pro.IdEspecialidad = {};""".format(IdEspecialidad)
    conexion = get_conexion()
    profesional = None
    with conexion.cursor() as cur:
        cur.execute(query),(IdEspecialidad,)
    profesional = cur.fetchone()
    conexion.close()
    return profesional


def obtener_turno_por_id(idTurno):
    query = """SELECT est.IdEstadoTurno, est.Nombre, tur.FechaTurno, tur.HoraDesde, tur.HoraHasta, pac.Nombre, pac.Apellido, pac.NumeroDocumento, esp.Nombre, rec.Nombre
                FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp , profesional AS prof, recurso AS rec
                WHERE est.IdEstadoTurno = tur.IdEstadoTurno
                AND pac.IdPaciente = tur.IdPaciente
                AND tur.IdEspecialidad = esp.IdEspecialidad
                AND prof.idEspecialidad = esp.IdEspecialidad
                AND prof.IdRecurso = rec.IdRecurso
                AND tur.IdTurno = {}""".format(idTurno)
    conexion = get_conexion()
    id_turno = None
    with conexion.cursor() as cur:
        cur.execute(query),(idTurno,)
    id_turno = cur.fetchone()
    conexion.close()
    return id_turno