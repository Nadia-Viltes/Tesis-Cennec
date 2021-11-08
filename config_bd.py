import pymysql


def get_conexion():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='Bleda1983',
                           db='mydb')