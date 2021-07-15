from config_bd import get_conexion

# query para que me muestre los datos en la lista paciente
def obtener_pacientes():
    query = """
            SELECT pa.Nombre, pa.Apellido, pa.numeroDocumento, fi.nombre, tu.Nombre, tu.Apellido
            FROM PACIENTE AS pa
            INNER JOIN Tutoria AS tu 
            ON tu.IdTutoria = pa.idTutoria
            INNER JOIN afiliacion afi
            ON pa.IdPaciente = afi.IdPaciente
            INNER JOIN financiador fi
            ON fi.IdFinanciador = afi.IdFinanciador;
            """
    conexion = get_conexion()
    paciente = []
    with conexion.cursor() as cur:
        cur.execute(query)
    paciente = cur.fetchall()
    conexion.close()
    return paciente

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
        INSERT INTO domicilio (IdPais, IdProvincia, IdLocalidad, IdBarrio, Calle, Altura, Piso, Dpto)
        VALUES ({}, {}, {}, {}, '{}', '{}','{}', '{}')""".format(pais, provincia, localidad, barrio, calle, altura, piso, dpto)
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
        INSERT INTO tutoria(Nombre, Apellido, Ocupacion, TelefonoFijo, TelefonoCelular)
        VALUES ('{}', '{}', '{}', '{}', '{}')""".format(nombreTutor, apellidoTutor, ocupacion, nroFijo, nroCelular)
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
        INSERT INTO paciente (Nombre, Apellido, Genero, IdTipoDocumento, NumeroDocumento, FechaNacimiento, IdDomicilio, IdTutoria)
        VALUES ('{}','{}','{}',{},{},'{}',{},{})""".format(nombre, apellido, genero, tipoDocumento, nroDocumento, fechaNacimiento, idDomicilio, IdTutoria)
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


