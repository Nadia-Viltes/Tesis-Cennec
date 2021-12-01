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
            AND fi.IdFinanciador = afi.IdFinanciador
            AND pa.FechaBaja is null
            ORDER BY pa.Nombre asc, pa.Apellido asc;
            """
    conexion = get_conexion()
    pacientes = []
    with conexion.cursor() as cur:
        cur.execute(query)
    pacientes = cur.fetchall()
    conexion.close()
    return pacientes

#Necesitas una query para pedirlo - BUSQUEDA
def obtener_pacientes_query(parametros):
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
            AND fi.IdFinanciador = afi.IdFinanciador
            AND (LOWER(CONCAT(pa.Nombre, pa.Apellido, pa.NumeroDocumento))) LIKE LOWER('{}')
            """.format(parametros)
    print("Esta es la consutla final {}".format(query))        
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
    pais = None
    with conexion.cursor() as cur:
        cur.execute(query)
    pais = cur.fetchone()
    conexion.close()
    return pais

## Select provincia - Lista de valores
def obtener_provincias_by_id_pais(id_pais): 
    query = "select IdProvincia, Nombre from provincia where IdPais = {} and FechaBaja is null;".format(id_pais)
    conexion = get_conexion()
    provincias = []
    with conexion.cursor() as cur:
        cur.execute(query)
    provincias = cur.fetchall()
    conexion.close()
    return provincias

## Select Localidad - Lista de valores
def obtener_localidades_by_id_provincia(id_provincia): 
    query = "select IdLocalidad, Nombre from localidad where IdProvincia = {} and FechaBaja is null;".format(id_provincia)
    conexion = get_conexion()
    localidades = []
    with conexion.cursor() as cur:
        cur.execute(query)
    localidades = cur.fetchall()
    conexion.close()
    return localidades

## Select Barrio - Lista de valores
def obtener_barrios_by_id_localidad(id_localidad): 
    query = "select IdBarrio, Nombre from barrio where IdLocalidad = {} and FechaBaja is null;".format(id_localidad)
    conexion = get_conexion()
    barrios = []
    with conexion.cursor() as cur:
        cur.execute(query)
    barrios = cur.fetchall()
    conexion.close()
    return barrios

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
        VALUES ('{}','{}','{}',{},{},'{}',{},{}, now())""".format(nombre, apellido, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, IdTutoria)
    print("Este es mi insertar paciente -> {}".format(query))    
    idPaciente_insertado = None    
    with conexion.cursor() as cur:
        cur.execute(query)
        idPaciente_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idPaciente_insertado

## INSERTAR AFILIACION
def insertar_afiliacion (idPaciente, financiador, nroAfiliado):
    conexion = get_conexion()
    query = """
        INSERT INTO Afiliacion (IdPaciente, IdFinanciador, NumeroAfiliado, FechaAlta)
        VALUES ({},{},'{}',NOW());""".format(idPaciente, financiador, nroAfiliado)
    print("Este es mi insertar afiliacion -> {}".format(query))       
    idAfiliacion_insertado = None
    with conexion.cursor() as cur:
        cur.execute(query)
        idAfiliacion_insertado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idAfiliacion_insertado

## INSERTAR NUMERO DE HISTORIA CLINICA DIGITAL
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
            AND pa.FechaBaja is null
            AND pa.idPaciente = {}""".format(idPaciente)
    conexion = get_conexion()
    paciente = None
    with conexion.cursor() as cur:
        cur.execute(query)
    paciente = cur.fetchone()
    conexion.close()
    return paciente


def actualizar_domicilio(pais, provincia, localidad, barrio, calle, altura, piso, dpto, idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE domicilio SET IdPais={}, IdProvincia={}, IdLocalidad={}, IdBarrio={}, calle='{}', altura='{}', piso='{}', Dpto='{}',FechaModificacion=NOW()
                        WHERE IdDomicilio = (select IdDomicilio from (select pa.IdDomicilio from paciente as pa, domicilio as dom Where pa.IdDomicilio = dom.IdDomicilio and pa.IdPaciente = {})AS alias_domicilio)""".format
                       (pais, provincia, localidad, barrio, calle, altura, piso, dpto, idPaciente))
    conexion.commit()
    conexion.close()

def actualizar_tutoria(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular, idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE tutoria SET Nombre = '{}', Apellido = '{}', Ocupacion = '{}', TelefonoFijo= '{}', TelefonoCelular= '{}',FechaModificacion=NOW()
                        WHERE IdTutoria = (select IdTutoria from (select pa.IdTutoria from paciente as pa, tutoria as tu Where pa.IdTutoria = tu.IdTutoria and pa.IdPaciente = {})AS alias_tutoria)""".format
                       (nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular, idPaciente))
    conexion.commit()
    conexion.close()

def actualizar_afiliacion(financiador,nroAfiliado,idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE afiliacion SET IdFinanciador ={}, NumeroAfiliado='{}', FechaModificacion=NOW() WHERE IdPaciente = {}".format
                       (financiador,nroAfiliado,idPaciente))
    conexion.commit()
    conexion.close()

def actualizar_paciente(nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idPaciente):
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE paciente SET Nombre='{}', Apellido='{}', Genero='{}',IdTipoDocumento={}, NumeroDocumento={}, FechaNacimiento='{}',FechaModificacion=NOW() 
                        WHERE IdPaciente = {}""".format
                       (nombrePaciente, apellidoPaciente, genero, tipoDocumento, nroDocumento, fechaNacimiento, idPaciente))
    conexion.commit()
    conexion.close()