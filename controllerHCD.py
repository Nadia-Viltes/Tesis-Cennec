from config_bd import get_conexion

# query para que me muestre los datos en la lista HCD
def obtener_lista_hcd():
    query = """
           SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.NumeroDocumento, LPAD(hcd.IdHistoriaClinica, 5, '0')
            FROM paciente as pa, historiaclinica as hcd
            WHERE hcd.IdPaciente = pa.IdPaciente               
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
        cur.execute(query),(idPaciente,)
    paciente_hcd = cur.fetchone()
    conexion.close()
    return paciente_hcd

    ## Select tipo de especialidad - Lista de valores - ESTO ES PARA LA ASIGNACIÓN DE TURNOS DE ADMISIÓN
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


    ## Select tipo de patologia - Lista de valores - ESTO ES PARA LA ASIGNACIÓN DE TURNOS DE ADMISIÓN
def obtener_patologia(): 
    query = "SELECT IdTipoPatologia, Nombre FROM tipopatologia WHERE FechaBaja is null;"
    conexion = get_conexion()
    idPatologia = []
    with conexion.cursor() as cur:
        cur.execute(query)
    idPatologia = cur.fetchall()
    conexion.close()
    return idPatologia


 ## SELECT PARA VER LA CANTIDAD DE TURNOS DE ADMINISIÓN ASIGNADOS
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


 ## SELECT PARA VER LA CANTIDAD DE TURNOS DE ADMINISIÓN ASIGNADOS
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


 ## INSERTAR TURNOS DE ADMISIÓN
def insertar_turnos_admision (idPaciente_HCD, IdEspecialidad, idPatologia, cantidad):
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


 ## PARA DESAHABILITAR EL BOTON
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