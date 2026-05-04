import csv
from io import StringIO
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Producto

router = APIRouter()

# ----------------------------------------
# 1. OBTENER TODOS LOS PRODUCTOS
# ----------------------------------------
@router.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

# ----------------------------------------
# 2. SUBIR CSV → BORRAR TODO → CARGAR NUEVO
# ----------------------------------------
@router.post("/subir_csv")
async def subir_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Borrar tabla completa
    db.query(Producto).delete()
    db.commit()

    contenido = await file.read()
    texto = contenido.decode("utf-8")

    csv_reader = csv.reader(StringIO(texto))

    for fila in csv_reader:
        if len(fila) < 3:
            continue

        codigo = fila[0].strip()
        descripcion = fila[1].strip()
        cantidad = int(fila[2].strip())

        nuevo = Producto(
            codigo=codigo,
            descripcion=descripcion,
            cantidad=cantidad
        )
        db.add(nuevo)

    db.commit()
    return {"mensaje": "CSV cargado correctamente"}

# ----------------------------------------
# 3. ACTUALIZAR CANTIDADES (SUMAR/RESTAR)
# ----------------------------------------
@router.post("/actualizar")
def actualizar(datos: dict, db: Session = Depends(get_db)):
    """
    Espera:
    {
        "codigo": "123",
        "cantidad": 5,
        "modo": "sumar" o "restar"
    }
    """

    codigo = datos["codigo"]
    cantidad = int(datos["cantidad"])
    modo = datos["modo"]

    producto = db.query(Producto).filter_by(codigo=codigo).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if modo == "sumar":
        producto.cantidad += cantidad
    elif modo == "restar":
        producto.cantidad -= cantidad

    db.commit()
    return {"mensaje": "Actualizado correctamente"}

# ----------------------------------------
# 4. EXPORTAR CSV
# ----------------------------------------
@router.get("/exportar_csv")
def exportar_csv(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()

    output = StringIO()
    writer = csv.writer(output)

    for p in productos:
        writer.writerow([p.codigo, p.descripcion, p.cantidad])

    output.seek(0)
    return output.getvalue()
