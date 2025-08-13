from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

app = FastAPI(title="Semana 1 - Gestión de Tareas")

# ===========================
# MODELOS
# ===========================
class Preferencias(BaseModel):
    tema: str
    idioma: str
    zona_horaria: str

class Usuario(BaseModel):
    id: int
    nombre_usuario: str
    email: EmailStr
    nombre_completo: str
    creado_en: datetime
    preferencias: Preferencias

class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: str
    color: str
    usuario_id: int

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str
    prioridad: str
    estado: str
    categoria_id: int
    usuario_id: int
    fecha_vencimiento: date
    creado_en: datetime
    actualizado_en: datetime
    etiquetas: List[str]

# ===========================
# BASE DE DATOS EN MEMORIA
# ===========================
usuarios_db: List[Usuario] = []
categorias_db: List[Categoria] = []
tareas_db: List[Tarea] = []

# ===========================
# CRUD USUARIOS
# ===========================
@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return usuario

@app.get("/usuarios/me", response_model=Usuario)
def obtener_perfil():
    if usuarios_db:
        return usuarios_db[0]
    raise HTTPException(status_code=404, detail="No hay usuarios")

@app.put("/usuarios/me", response_model=Usuario)
def actualizar_perfil(usuario_actualizado: Usuario):
    if usuarios_db:
        usuarios_db[0] = usuario_actualizado
        return usuario_actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/me")
def eliminar_usuario():
    if usuarios_db:
        usuarios_db.pop(0)
        return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="No hay usuario para eliminar")

# ===========================
# CRUD CATEGORÍAS
# ===========================
@app.post("/categorias", response_model=Categoria)
def crear_categoria(categoria: Categoria):
    categorias_db.append(categoria)
    return categoria

@app.get("/categorias", response_model=List[Categoria])
def listar_categorias():
    return categorias_db

@app.put("/categorias/{categoria_id}", response_model=Categoria)
def actualizar_categoria(categoria_id: int, categoria_actualizada: Categoria):
    for i, categoria in enumerate(categorias_db):
        if categoria.id == categoria_id:
            categorias_db[i] = categoria_actualizada
            return categoria_actualizada
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

@app.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    for i, categoria in enumerate(categorias_db):
        if categoria.id == categoria_id:
            categorias_db.pop(i)
            return {"mensaje": "Categoría eliminada"}
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

# ===========================
# CRUD TAREAS
# ===========================
@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: Tarea):
    tareas_db.append(tarea)
    return tarea

@app.get("/tareas", response_model=List[Tarea])
def listar_tareas(estado: Optional[str] = None, prioridad: Optional[str] = None):
    resultados = tareas_db
    if estado:
        resultados = [t for t in resultados if t.estado == estado]
    if prioridad:
        resultados = [t for t in resultados if t.prioridad == prioridad]
    return resultados

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: int):
    for tarea in tareas_db:
        if tarea.id == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea):
    for i, tarea in enumerate(tareas_db):
        if tarea.id == tarea_id:
            tareas_db[i] = tarea_actualizada
            return tarea_actualizada
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    for i, tarea in enumerate(tareas_db):
        if tarea.id == tarea_id:
            tareas_db.pop(i)
            return {"mensaje": "Tarea eliminada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.patch("/tareas/{tarea_id}/estado")
def cambiar_estado(tarea_id: int, estado: str):
    for tarea in tareas_db:
        if tarea.id == tarea_id:
            tarea.estado = estado
            return {"mensaje": f"Estado cambiado a {estado}"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# ===========================
# ESTADÍSTICAS
# ===========================
@app.get("/stats/summary")
def resumen():
    return {
        "total_tareas": len(tareas_db),
        "pendientes": len([t for t in tareas_db if t.estado == "pendiente"]),
        "completadas": len([t for t in tareas_db if t.estado == "completada"])
    }

@app.get("/stats/productividad")
def productividad():
    return {"mensaje": "Estadísticas de productividad (demo)"}
