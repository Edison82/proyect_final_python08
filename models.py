from sqlalchemy import Column, Integer, String
from database import Base

class ClienteDB(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(Integer)

class ProveedorDB(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(Integer)
    id_legal = Column(String, index=True)