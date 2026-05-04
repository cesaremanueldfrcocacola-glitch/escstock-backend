# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, default=0)
