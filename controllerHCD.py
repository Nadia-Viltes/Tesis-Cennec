from config_bd import get_conexion

# query para que me muestre los datos en la lista HCD
def obtener_lista_hcd():
    query = """
           SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0')
           FROM PACIENTE AS pa
            INNER JOIN historiaclinica as hcd
            ON pa.IdPaciente = hcd.IdPaciente               
            """
    conexion = get_conexion()
    hcd = []
    with conexion.cursor() as cur:
        cur.execute(query)
    hcd = cur.fetchall()
    conexion.close()
    return hcd

def obtener_hcd_por_id(idPaciente):
    query = """
            SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0'), fi.Nombre, afi.NumeroAfiliado
			FROM PACIENTE AS pa, afiliacion as afi, financiador as fi, historiaclinica as hcd
			WHERE pa.IdPaciente = afi.IdPaciente
			AND fi.IdFinanciador = afi.IdFinanciador
			AND pa.IdPaciente = hcd.IdPaciente
            AND pa.idPaciente = {}""".format(idPaciente)
    conexion = get_conexion()
    paciente_hcd = None
    with conexion.cursor() as cur:
        cur.execute(query),(idPaciente,)
    paciente_hcd = cur.fetchone()
    conexion.close()
    return paciente_hcd

    ## Select tipo de especialidad - Lista de valores
def obtener_especialidad(): 
    query = "SELECT IdEspecialidad, Nombre FROM especialidad WHERE FechaBaja is null;"
    conexion = get_conexion()
    IdEspecialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    IdEspecialidad = cur.fetchall()
    conexion.close()
    return IdEspecialidad

    ## Select tipo de patologia - Lista de valores
def obtener_patologia(): 
    query = "SELECT IdTipoPatologia, Nombre FROM tipopatologia WHERE FechaBaja is null;"
    conexion = get_conexion()
    idPatologia = []
    with conexion.cursor() as cur:
        cur.execute(query)
    idPatologia = cur.fetchall()
    conexion.close()
    return idPatologia

## INSERTAR TURNOS DE ADMISIÓN
def insertar_turnos_admision (idPaciente_HCD, IdEspecialidad, idPatologia, cantidad):
    conexion = get_conexion()
    query = """
        INSERT INTO configuracionturno (IdPaciente, IdEspecialidad, IdTipoPatologia, CantidadDisponibles, FechaAlta)
        VALUES ({}, {}, {}, '{}', NOw());""".format(idPaciente_HCD, IdEspecialidad, idPatologia, cantidad)
    idconfiguracion_turno = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idconfiguracion_turno = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idconfiguracion_turno