import pymysql

def establecer_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='admin',
                                db='mydb')