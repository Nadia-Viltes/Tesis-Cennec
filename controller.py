from config_bd import get_conexion

# query para que me muestre los datos en la lista paciente
def obtener_pacientes():
    query = """
           SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.Genero, tdoc.Nombre, pa.NumeroDocumento, pa.FechaNacimiento, 
           p.Nombre, pro.Nombre, loc.Nombre, dom.calle, dom.altura, dom.piso, dom.Dpto, bar.Nombre, tu.Nombre, tu.Apellido, 
           tu.Ocupacion, tu.TelefonoFijo, tu.TelefonoCelular, fi.Nombre, afi.NumeroAfiliado, afi.FechaAlta
            FROM PACIENTE AS pa, TipoDocumento as tdoc, Domicilio AS dom, pais AS p, provincia AS pro, localidad AS loc,
            barrio AS bar, Tutoria AS tu, afiliacion afi, financiador fi
            WHERE pa.IdTipoDocumento = tdoc.IdTipoDocumento
            AND pa.IdDomicilio = dom.IdDomicilio
            AND p.IdPais = dom.IdPais
            AND pro.IdProvincia = dom.IdProvincia
            AND loc.IdLocalidad = dom.IdLocalidad
            AND bar.IdBarrio = dom.IdBarrio
            AND tu.IdTutoria = pa.idTutoria
            AND pa.IdPaciente = afi.IdPaciente
            AND fi.IdFinanciador = afi.IdFinanciador;
            """
    conexion = get_conexion()
    pacientes = []
    with conexion.cursor() as cur:
        cur.execute(query)
    pacientes = cur.fetchall()
    conexion.close()
    return pacientes

## Select tipo de documento - Lista de valores
def obtener_tipoDocumento(): 
    query = "select IdTipoDocumento, Nombre from tipodocumento where FechaBaja is null"
    conexion = get_conexion()
    tipoDocumento = []
    with conexion.cursor() as cur:
        cur.execute(query)
    tipoDocumento = cur.fetchall()
    conexion.close()
    return tipoDocumento

## Select País - Lista de valores
def obtener_pais(): 
    query = "select IdPais, Nombre from pais where FechaBaja is null"
    conexion = get_conexion()
    pais = []
    with conexion.cursor() as cur:
        cur.execute(query)
    pais = cur.fetchall()
    conexion.close()
    return pais

## Select provincia - Lista de valores
def obtener_provincia(): 
    query = "select IdProvincia, Nombre from provincia where IdPais = 1 and FechaBaja is null;"
    conexion = get_conexion()
    provincia = []
    with conexion.cursor() as cur:
        cur.execute(query)
    provincia = cur.fetchall()
    conexion.close()
    return provincia

## Select Localidad - Lista de valores
def obtener_localidad(): 
    query = "select IdLocalidad, Nombre from localidad where IdProvincia = 1 and FechaBaja is null;"
    conexion = get_conexion()
    localidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    localidad = cur.fetchall()
    conexion.close()
    return localidad

## Select Barrio - Lista de valores
def obtener_barrio(): 
    query = "select IdBarrio, Nombre from barrio where IdLocalidad = 1 and FechaBaja is null;"
    conexion = get_conexion()
    barrio = []
    with conexion.cursor() as cur:
        cur.execute(query)
    barrio = cur.fetchall()
    conexion.close()
    return barrio

## Select Financiador - Lista de valores
def obtener_financiador(): 
    query = "select IdFinanciador, Nombre from financiador where FechaBaja is null;"
    conexion = get_conexion()
    financiador = []
    with conexion.cursor() as cur:
        cur.execute(query)
    financiador = cur.fetchall()
    conexion.close()
    return financiador

## INSERTAR DOMICILIO
def insertar_domicilio (pais, provincia, localidad, barrio, calle, altura, piso, dpto):
    conexion = get_conexion()
    query = """
        INSERT INTO domicilio (IdPais, IdProvincia, IdLocalidad, IdBarrio, Calle, Altura, Piso, Dpto, FechaAlta)
        VALUES ({}, {}, {}, {}, '{}', '{}','{}', '{}', NOw())""".format(pais, provincia, localidad, barrio, calle, altura, piso, dpto)
    idDomicilio_insertado = None
    print("Insertar domicilio -> {}".format(query))
    with conexion.cursor() as cur:
        cur.execute(query)
        idDomicilio_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idDomicilio_insertado

## INSERTAR TUTOR
def insertar_tutor (nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular):
    conexion = get_conexion()
    idTutoria_insertado = None
    query = """
        INSERT INTO tutoria(Nombre, Apellido, Ocupacion, TelefonoFijo, TelefonoCelular, FechaAlta)
        VALUES ('{}', '{}', '{}', '{}', '{}', NOW())""".format(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
    print("Insertar tutor -> {}".format(query))   
    with conexion.cursor() as cur:
        cur.execute(query)
        idTutoria_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTutoria_insertado

## INSERTAR PACIENTE
def insertar_paciente (nombre, apellido, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, IdTutoria):
    conexion = get_conexion()
    query = """
        INSERT INTO paciente (Nombre, Apellido, Genero, IdTipoDocumento, NumeroDocumento, FechaNacimiento, IdDomicilio, IdTutoria, FechaAlta)
        VALUES ('{}','{}','{}',{},{},'{}',{},{}, NOW())""".format(nombre, apellido, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, IdTutoria)
    print("Este es mi insertar paciente -> {}".format(query))    
    idPaciente_insertado = None    
    with conexion.cursor() as cur:
        cur.execute(query)
        idPaciente_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idPaciente_insertado

## INSERTAR AFILIACION
def insertar_afiliacion (idPaciente, financiador, nroAfiliado, fechaAltaFinanciador):
    conexion = get_conexion()
    query = """
        INSERT INTO Afiliacion (IdPaciente, IdFinanciador, NumeroAfiliado, FechaAlta)
        VALUES ({},{},'{}','{}');""".format(idPaciente, financiador, nroAfiliado, fechaAltaFinanciador)
    print("Este es mi insertar afiliacion -> {}".format(query))       
    idAfiliacion_insertado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idAfiliacion_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idAfiliacion_insertado

def insertar_HCD (idPaciente):
    conexion = get_conexion()
    query = """
        INSERT INTO historiaclinica (IdPaciente, FechaAlta)
        VALUES ({},NOW());""".format(idPaciente)   
    idHCD_insertado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idHCD_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idHCD_insertado

def obtener_paciente_por_id(idPaciente):
    query = """
            SELECT pa.IdPaciente, pa.Nombre, pa.Apellido, pa.Genero, tdoc.IdTipoDocumento, tdoc.Nombre, pa.NumeroDocumento, pa.FechaNacimiento, p.IdPais, p.Nombre, pro.IdProvincia, pro.Nombre, 
            loc.IdLocalidad, loc.Nombre, dom.calle, dom.altura, dom.piso, dom.Dpto, bar.IdBarrio, bar.Nombre, LPAD(hcd.IdHistoriaClinica, 5, '0'), tu.Nombre, tu.Apellido, tu.Ocupacion,
            tu.TelefonoFijo, tu.TelefonoCelular, fi.IdFinanciador, fi.Nombre, afi.NumeroAfiliado
            FROM PACIENTE AS pa, TipoDocumento as tdoc, Domicilio AS dom, pais AS p, provincia AS pro, localidad AS loc,
            barrio AS bar, Tutoria AS tu, afiliacion as afi, financiador as fi, historiaclinica hcd
            WHERE pa.IdTipoDocumento = tdoc.IdTipoDocumento
            AND pa.IdDomicilio = dom.IdDomicilio
            AND p.IdPais = dom.IdPais
            AND pro.IdProvincia = dom.IdProvincia
            AND loc.IdLocalidad = dom.IdLocalidad
            AND bar.IdBarrio = dom.IdBarrio
            AND tu.IdTutoria = pa.idTutoria
            AND pa.IdPaciente = afi.IdPaciente
            AND fi.IdFinanciador = afi.IdFinanciador
            AND pa.IdPaciente = hcd.IdPaciente
            AND pa.idPaciente = {}""".format(idPaciente)
    conexion = get_conexion()
    paciente = None
    with conexion.cursor() as cur:
        cur.execute(query),(idPaciente,)
    paciente = cur.fetchone()
    conexion.close()
    return paciente


def actualizar_domicilio(pais, provincia, localidad, barrio, calle, altura, piso, dpto, idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE domicilio SET IdPais={}, IdProvincia={}, IdLocalidad={}, IdBarrio={}, calle='{}', altura='{}' piso='{}', Dpto='{}'
                        WHERE IdPaciente = {}""".format
                       (pais, provincia, localidad, barrio, calle, altura, piso, dpto, idPaciente))
    conexion.commit()
    conexion.close()

def actualizar_tutoria(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE tutoria SET Nombre = '{}', Apellido = '{}', Ocupacion = '{}', TelefonoFijo= '{}', TelefonoCelular= '{}'
                        WHERE IdPaciente = %s""".format
                       (nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular))
    conexion.commit()
    conexion.close()

def actualizar_afiliacion(financiador,nroAfiliado):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE afiliacion SET IdFinanciador ={}, NumeroAfiliado='{}' WHERE IdPaciente = {});".format
                       (financiador,nroAfiliado))
    conexion.commit()
    conexion.close()

def actualizar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento,nroDocumento, fechaNacimiento, idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE paciente SET nombre='{}'', apellido='{}', Genero='{}',IdTipoDocumento={}, NumeroDocumento={},,FechaNacimiento='{}' WHERE idPaciente = {}".format
                       (nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idPaciente))
    conexion.commit()
    conexion.close()