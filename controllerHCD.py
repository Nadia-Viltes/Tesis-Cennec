from config_bd import get_conexion

# query para que me muestre los datos en la lista HCD
def obtener_hcd():
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
