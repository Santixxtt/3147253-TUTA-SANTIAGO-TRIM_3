from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import asyncio

app = FastAPI(title="Semana 2 - Sistema de Gestión de Proyectos")

# ===========================
# MODELOS Pydantic
# ===========================
class Usuario(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    activo: bool = True

class Proyecto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    propietario_id: int

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    prioridad: str
    estado: str = "pendiente"
    proyecto_id: int

class Comentario(BaseModel):
    id: int
    contenido: str
    autor_id: int
    tarea_id: int

# ===========================
# DATOS EN MEMORIA
# ===========================
usuarios: List[Usuario] = []
proyectos: List[Proyecto] = []
tareas: List[Tarea] = []
comentarios: List[Comentario] = []

# ===========================
# CRUD USUARIOS
# ===========================
@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return usuario

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    for u in usuarios:
        if u.id == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    global usuarios
    usuarios = [u for u in usuarios if u.id != usuario_id]
    return {"mensaje": "Usuario eliminado"}

# ===========================
# CRUD PROYECTOS
# ===========================
@app.post("/proyectos", response_model=Proyecto)
def crear_proyecto(proyecto: Proyecto):
    proyectos.append(proyecto)
    return proyecto

@app.get("/proyectos", response_model=List[Proyecto])
def listar_proyectos():
    return proyectos

# ===========================
# CRUD TAREAS
# ===========================
@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: Tarea):
    tareas.append(tarea)
    return tarea

@app.get("/tareas", response_model=List[Tarea])
def listar_tareas():
    return tareas

# ===========================
# CRUD COMENTARIOS
# ===========================
@app.post("/comentarios", response_model=Comentario)
def crear_comentario(comentario: Comentario):
    comentarios.append(comentario)
    return comentario

@app.get("/comentarios", response_model=List[Comentario])
def listar_comentarios():
    return comentarios

# ===========================
# ENDPOINT ASYNC EJEMPLO
# ===========================
@app.get("/backup")
async def hacer_backup():
    await asyncio.sleep(2)  # Simula proceso largo
    return {"mensaje": "Backup completado"}
