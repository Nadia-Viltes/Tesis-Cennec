from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno():
    query = """
           SELECT est.IdEstadoTurno, est.Nombre, tur.FechaTurno, tur.HoraDesde, tur.HoraHasta, pac.Nombre, pac.Apellido, pac.NumeroDocumento,
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