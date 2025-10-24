from sqlalchemy import Column, Integer, String
from database import Base

class ClienteDB(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(Integer)