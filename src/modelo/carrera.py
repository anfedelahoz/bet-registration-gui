import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, column
from sqlalchemy.orm import relationship

from .declarative_base import Base


class TipoCarrera(enum.Enum):
    F1 = 1
    ATLETISMO = 2
    NATACION = 3


class Carrera(Base):
    __tablename__ = 'carrera'
    __table_args__ = {'sqlite_autoincrement': True}
    id_carrera = Column(Integer, primary_key=True)
    titulo = Column(String)
    abierta = Column(Boolean, nullable=False,default=1)
    ganador = Column(Integer, nullable=True)
    competidores = relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas= relationship('Apuesta', cascade='all, delete, delete-orphan')
