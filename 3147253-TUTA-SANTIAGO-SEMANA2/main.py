from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import asyncio

app = FastAPI(title="Semana 2 - Gestión de Proyectos")

# ===========================
# MODELOS Pydantic
# ===========================
class Usuario(BaseModel):
    id: int
    nombre: str
    email: EmailStr
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
usuarios_db: List[Usuario] = []
proyectos_db: List[Proyecto] = []
tareas_db: List[Tarea] = []
comentarios_db: List[Comentario] = []

# ===========================
# CRUD USUARIOS
# ===========================
@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario) -> Usuario:
    usuarios_db.append(usuario)
    return usuario

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios() -> List[Usuario]:
    return usuarios_db

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int) -> Usuario:
    for usuario in usuarios_db:
        if usuario.id == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{usuario_id}")
def desactivar_usuario(usuario_id: int) -> dict:
    for usuario in usuarios_db:
        if usuario.id == usuario_id:
            usuario.activo = False
            return {"mensaje": "Usuario desactivado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# ===========================
# CRUD PROYECTOS
# ===========================
@app.post("/proyectos", response_model=Proyecto)
def crear_proyecto(proyecto: Proyecto) -> Proyecto:
    proyectos_db.append(proyecto)
    return proyecto

@app.get("/proyectos", response_model=List[Proyecto])
def listar_proyectos() -> List[Proyecto]:
    return proyectos_db

# ===========================
# CRUD TAREAS
# ===========================
@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: Tarea) -> Tarea:
    tareas_db.append(tarea)
    return tarea

@app.get("/tareas", response_model=List[Tarea])
def listar_tareas() -> List[Tarea]:
    return tareas_db

# ===========================
# CRUD COMENTARIOS
# ===========================
@app.post("/comentarios", response_model=Comentario)
def crear_comentario(comentario: Comentario) -> Comentario:
    comentarios_db.append(comentario)
    return comentario

@app.get("/comentarios", response_model=List[Comentario])
def listar_comentarios() -> List[Comentario]:
    return comentarios_db

# ===========================
# ENDPOINT ASYNC EJEMPLO
# ===========================
@app.get("/simular-proceso")
async def simular_proceso() -> dict:
    await asyncio.sleep(3)  # Simula proceso largo
    return {"mensaje": "Proceso completado"}
