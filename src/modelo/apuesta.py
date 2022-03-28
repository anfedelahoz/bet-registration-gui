import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey,Float ,column
from sqlalchemy.orm import relationship
from .declarative_base import Base
class Apuesta(Base):
    __tablename__ = 'apuesta'
    __table_args__ = {'sqlite_autoincrement': True}
    id_apuesta = Column(Integer, primary_key=True)
    carrera = Column(Integer, ForeignKey('carrera.id_carrera'))
    competidor = Column(Integer, ForeignKey('competidor.id_competidor'))
    apostador = Column(Integer, ForeignKey('apostador.id_apostador'))
    #apostador = relationship('Apostador.id_apostador', cascade='all, delete, delete-orphan')
    valor = Column(Float, nullable=True)