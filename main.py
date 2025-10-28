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


#Modelo de datos para la creacion de clientes
class ClienteCreate(BaseModel):
    nombre: str
    email: str
    telefono: int

# Modelo de datos de los clientes utilizando Pydantic
class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: int

    class Config:
        orm_model = True

# Modelo de datos de los proveedores
class Proveedores(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: int
    id_legal: str


#Crear la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Servir archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clientes_UI", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})

@app.get("/proveedores_UI", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("proveedores.html", {"request": request})



#Obtener Lista de Clientes
@app.get("/clientes", response_model=List[Cliente])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(models.ClienteDB).all()

#Obtener Lista de Proveedores
@app.get("/proveedores", response_model=List[Proveedores])
def get_proveedores(db: Session = Depends(get_db)):
    return db.query(models.ProveedorDB).all()



# Crear un cliente
@app.post("/clientes", status_code=201)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.ClienteDB(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Crear un proveedor
@app.post("/proveedores", status_code=201)
def create_proveedor(proveedor: Proveedores, db: Session = Depends(get_db)):
    db_proveedor = models.ProveedorDB(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor



# Eliminar un cliente
@app.delete("/clientes/{id}")
def delete_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == id). first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado"}

# Eliminar un Proveedor
@app.delete("/proveedores/{id}")
def delete_proveedor(id: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.ProveedorDB).filter(models.ProveedorDB.id == id). first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()
    return {"message": "Proveedor eliminado"}

#Actualizar un cliente
@app.put("/clientes/{id}")
def update_cliente(id: int, cliente: Cliente, db: Session = Depends(get_db)):
    cliente_db = db.query(models.ClienteDB).filter(models.ClienteDB.id == id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente_db.nombre = cliente.nombre
    cliente_db.email = cliente.email
    cliente_db.telefono = cliente.telefono
    db.commit()
    return {"message": "Cliente actualizado"}

#Actualizar un Proveedor
@app.put("/proveedores/{id}")
def update_proveedor(id: int, proveedor: Proveedores, db: Session = Depends(get_db)):
    proveedor_db = db.query(models.ProveedorDB).filter(models.ProveedorDB.id == id).first()
    if not proveedor_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    proveedor_db.nombre = proveedor.nombre
    proveedor_db.email = proveedor.email
    proveedor_db.telefono = proveedor.telefono
    proveedor_db.id_legal = proveedor.id_legal
    db.commit()
    return {"message": "Proveedor actualizado"}