from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Paciente(Base):
    __tablename__ = "paciente"

    idpaciente = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    genero = Column(String)
    numero_documento = Column('NumeroDocumento', Integer)
    fecha_nacimiento = Column('FechaNacimiento', Date)

    def __init__(self, id=None, nombre=None, apellido=None, genero=None, numero_documento=None, fecha_nacimiento=None):
        self.idpaciente = id
        self.nombre = nombre
        self.apellido = apellido
        self.genero = genero
        self.numero_documento = numero_documento
        self.fecha_nacimiento = fecha_nacimiento

