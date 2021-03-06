from config_bd import get_conexion

# query para que me muestre los datos en la lista HCD


def obtener_lista_hcd():
    query = """
           SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0')
            FROM paciente as pa, historiaclinica as hcd
            WHERE hcd.IdPaciente = pa.IdPaciente
            AND pa.fechabaja is null
            ORDER BY pa.Nombre, pa.Apellido;               
            """
    conexion = get_conexion()
    hcd = []
    with conexion.cursor() as cur:
        cur.execute(query)
    hcd = cur.fetchall()
    conexion.close()
    return hcd


def obtener_lista_hcd_query(parametros):
    query = """
            SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0')
            FROM paciente as pa, historiaclinica as hcd
            WHERE hcd.IdPaciente = pa.IdPaciente
            AND pa.fechabaja is null
            AND (LOWER(CONCAT(pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0')))) LIKE LOWER('{}')
            ORDER BY pa.Nombre, pa.Apellido;              
            """.format(parametros)
    conexion = get_conexion()
    hcd = []
    with conexion.cursor() as cur:
        cur.execute(query)
    hcd = cur.fetchall()
    conexion.close()
    return hcd


def obtener_hcd_por_id(idPaciente):
    query = """
            SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0'), fi.Nombre, 
            afi.NumeroAfiliado, hcd.IdHistoriaClinica
			FROM PACIENTE AS pa, historiaclinica as hcd, afiliacion as afi, financiador as fi
			WHERE pa.IdPaciente = afi.IdPaciente
			AND fi.IdFinanciador = afi.IdFinanciador
			AND pa.IdPaciente = hcd.IdPaciente
            AND pa.IdPaciente = {}""".format(idPaciente)
    conexion = get_conexion()
    paciente_hcd = None
    with conexion.cursor() as cur:
        cur.execute(query), (idPaciente,)
    paciente_hcd = cur.fetchone()
    conexion.close()
    return paciente_hcd

    # Select tipo de especialidad - Lista de valores - ESTO ES PARA LA ASIGNACI??N DE TURNOS DE ADMISI??N


def obtener_especialidad(id):
    query = """Select IdEspecialidad, Nombre from especialidad WHERE IdEspecialidad not in 
            (Select esp.IdEspecialidad from configuracionturno as config, especialidad as esp 
            WHERE config.IdEspecialidad = esp.IdEspecialidad AND config.CantidadComputados <> config.CantidadDisponibles
            AND config.FechaBaja is null AND config.IdPaciente = {})""".format(id)
    conexion = get_conexion()
    IdEspecialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    IdEspecialidad = cur.fetchall()
    conexion.close()
    return IdEspecialidad

    # Select tipo de patologia - Lista de valores - ESTO ES PARA LA ASIGNACI??N DE TURNOS DE ADMISI??N


def obtener_patologia_por_especialidad_id(id_especialidad):
    query = """SELECT IdTipoPatologia, Nombre 
               FROM tipopatologia 
               WHERE idEspecialidad = {}
               AND FechaBaja is null;""".format(id_especialidad)
    conexion = get_conexion()
    patologias = []
    with conexion.cursor() as cur:
        cur.execute(query)
    patologias = cur.fetchall()
    conexion.close()
    return patologias

 # SELECT PARA VER LA CANTIDAD DE TURNOS DE ADMINISI??N ASIGNADOS


def obtener_lista_turnos_admision(idPaciente):
    query = """
           SELECT config.IdConfiguracionTurno, config.CantidadDisponibles, config.CantidadComputados, espe.IdEspecialidad, espe.Nombre
            FROM configuracionturno as config, especialidad as espe
            WHERE config.IdEspecialidad = espe.IdEspecialidad
            AND config.FechaBaja is null
            AND config.IdPaciente = {}""".format(idPaciente)
    conexion = get_conexion()
    turnosadm = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turnosadm = cur.fetchall()
    conexion.close()
    return turnosadm


def chequear_turnos_adminision_disponibles(id_paciente):
    query = """
            SELECT IFNULL(SUM(cantidadDisponibles) - SUM(CantidadComputados), 0) 
            FROM configuracionturno
            WHERE idpaciente = {}
            AND fechabaja is null;
            """.format(id_paciente)
    conexion = get_conexion()
    chequea_turno_admision = False
    with conexion.cursor() as cur:
        cur.execute(query)
        chequea_turno_admision = cur.fetchone()
    conexion.close()
    if chequea_turno_admision[0] != 0:
        chequea_turno_admision = True
    else:
        chequea_turno_admision = False
    return chequea_turno_admision

 # SELECT PARA VER LA CANTIDAD DE TURNOS DE ADMINISI??N ASIGNADOS


def agrupamos_lista_turnos_admision(idPaciente):
    query = """
           SELECT config.IdConfiguracionTurno, sum(config.CantidadDisponibles), sum(config.CantidadComputados), espe.IdEspecialidad, espe.Nombre
            FROM configuracionturno as config, especialidad as espe
            WHERE config.IdEspecialidad = espe.IdEspecialidad
            AND config.FechaBaja is null
            AND config.IdPaciente = {}
            GROUP BY espe.IdEspecialidad""".format(idPaciente)
    conexion = get_conexion()
    grupo_turnosadm = []
    with conexion.cursor() as cur:
        cur.execute(query)
    grupo_turnosadm = cur.fetchall()
    conexion.close()
    return grupo_turnosadm

 # INSERTAR TURNOS DE ADMISI??N


def insertar_turnos_admision(idPaciente_HCD, IdEspecialidad, idPatologia, cantidad):
    conexion = get_conexion()
    query = """
        INSERT INTO configuracionturno (IdPaciente, IdEspecialidad, IdTipoPatologia, CantidadDisponibles, CantidadComputados, FechaAlta)
        VALUES ({}, {}, {}, '{}',0, NOw());""".format(idPaciente_HCD, IdEspecialidad, idPatologia, cantidad)
    idconfiguracion_turno = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idconfiguracion_turno = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idconfiguracion_turno


def update_baja_turno_admision(dataTurnoAdmId):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE configuracionturno SET FechaBaja = NOW() 
                        WHERE IdConfiguracionTurno = {}""".format(dataTurnoAdmId))
    conexion.commit()
    conexion.close()

 # PARA DESAHABILITAR EL BOTON


def boton_turno_adm(idConfigT):
    query = """
           SELECT config.IdConfiguracionTurno
            FROM configuracionturno as config, especialidad as espe
            WHERE config.IdEspecialidad = espe.IdEspecialidad
            AND config.FechaBaja is null
            AND config.IdConfiguracionTurno= {}""".format(idConfigT)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    boton = cur.fetchone()
    conexion.close()
    return boton
