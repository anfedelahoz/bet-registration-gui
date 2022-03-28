import enum
from sqlalchemy import Column, Float, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .declarative_base import Base
 
 
class Apostador(Base):
    __tablename__ = 'apostador'
    __table_args__ = {'sqlite_autoincrement': True}
    id_apostador = Column(Integer, primary_key=True)
    nombre = Column(String)   