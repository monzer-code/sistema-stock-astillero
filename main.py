from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI(
    title="Sistema de Stock - Náutica Facu",
    description="Panel para que los empleados carguen y vean el stock del taller",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ESTA ES LA RUTA QUE MUESTRA TU PÁGINA LINDA
@app.get("/", response_class=HTMLResponse)
def leer_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/ver-stock", summary="Ver lista de materiales", tags=["Inventario"])
def obtener_stock(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

@app.post("/cargar-producto", summary="Cargar un producto nuevo", tags=["Inventario"])
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float, db: Session = Depends(get_db)):
    nuevo_prod = models.Producto(nombre=nombre, categoria=categoria, cantidad=cantidad, precio=precio)
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    return {"mensaje": "¡Cargado con éxito!", "producto": nuevo_prod}

@app.delete("/borrar-producto/{producto_id}", summary="Eliminar un producto", tags=["Inventario"])
def borrar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return {"error": "No encontré ese producto"}
    db.delete(producto)
    db.commit()
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)