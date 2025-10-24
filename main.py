from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo de datos de los clientes utilizando Pydantic
class Cliente(BaseModel):
    id: str
    nombre: str
    email: str
    telefono: int

    class Config:
        orm_model = True

#Datos simulados
clientes = [
    Cliente(id="1", nombre="Carlos", email="carlos12@gmail.com", telefono=3234345566),
    Cliente(id="2", nombre="Andres", email="Andres22@gmail.com", telefono=3123324567),
]

#Crear la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Servir archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clientes", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})

#Obtener Lista de Clientes
@app.get("/clientes", response_model=List[Cliente])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(models.ClienteDB).all()

# Crear un cliente
@app.post("/clientes", status_code=201)
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = models.ClienteDB(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return {"message": "Cliente Creado"}

# Eliminar un cliente
@app.delete("/clientes/{id}")
def delete_cliente(id: str, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == id). first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado"}

#Actualizar un cliente
@app.put("/clientes/{id}")
def update_cliente(id: str, cliente: Cliente, db: Session = Depends(get_db)):
    cliente_db = db.query(models.ClienteDB).filter(models.ClienteDB.id == id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente_db.nombre = cliente.nombre
    cliente_db.email = cliente.email
    cliente_db.telefono = cliente.telefono
    db.commit()
    return {"message": "Cliente actualizado"}