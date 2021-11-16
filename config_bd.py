import pymysql


def get_conexion():
    return pymysql.connect(host='localhost',
                           user='diegoanywhere',
                           password='mysqltesis',
                           db='mydb')
