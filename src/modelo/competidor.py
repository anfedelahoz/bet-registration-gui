import enum

from sqlalchemy import Column, Float, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .declarative_base import Base

 
 
class Competidor(Base):
    __tablename__ = 'competidor'
    __table_args__ = {'sqlite_autoincrement': True}
    id_competidor = Column(Integer, primary_key=True)
    nombre = Column(String)
    carrera = Column(Integer, ForeignKey('carrera.id_carrera'))
    probabilidad = Column(Float)