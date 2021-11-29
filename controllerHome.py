from config_bd import get_conexion

# query para ver cumpleaños
def obtener_lista_cumple():
    query = """
           SELECT Nombre, Apellido, date_format(fechaNacimiento,'%d/%m'), date_format(now(),'%d/%m') 
           FROM paciente WHERE date_format(fechaNacimiento,'%d/%m') = date_format(now(),'%d/%m');             
            """
    conexion = get_conexion()
    cumple = []
    with conexion.cursor() as cur:
        cur.execute(query)
    cumple = cur.fetchall()
    conexion.close()
    return cumple


