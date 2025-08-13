from fastapi import FastAPI

app = FastAPI(title="Semana 1 - Sistema de Gestión de Tareas")

usuarios = []
tareas = []
categorias = []

# Usuarios
@app.post("/usuarios")
def crear_usuario(nombre_usuario: str, correo: str, nombre_completo: str):
    usuario_id = len(usuarios) + 1
    usuario = {
        "id": usuario_id,
        "nombre_usuario": nombre_usuario,
        "correo": correo,
        "nombre_completo": nombre_completo
    }
    usuarios.append(usuario)
    return {"mensaje": "Usuario creado correctamente", "usuario": usuario}

@app.get("/usuarios/yo")
def obtener_mi_perfil():
    if usuarios:
        return usuarios[0] 
    return {"mensaje": "No hay usuarios registrados"}

# Tareas
@app.post("/tareas")
def crear_tarea(titulo: str, descripcion: str, prioridad: str):
    tarea_id = len(tareas) + 1
    tarea = {
        "id": tarea_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "pendiente"
    }
    tareas.append(tarea)
    return {"mensaje": "Tarea creada", "tarea": tarea}

@app.get("/tareas")
def listar_tareas():
    return tareas

@app.put("/tareas/tarea_id")
def actualizar_tarea(tarea_id: int, titulo: str, descripcion: str, prioridad: str, estado: str):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["titulo"] = titulo
            tarea["descripcion"] = descripcion
            tarea["prioridad"] = prioridad
            tarea["estado"] = estado
            return {"mensaje": "Tarea actualizada", "tarea": tarea}
    return {"error": "Tarea no encontrada"}

@app.delete("/tareas/tarea_id")
def eliminar_tarea(tarea_id: int):
    global tareas
    tareas = [tarea for tarea in tareas if tarea["id"] != tarea_id]
    return {"mensaje": "Tarea eliminada"}

# Categorías
@app.post("/categorias")
def crear_categoria(nombre: str, descripcion: str, color: str):
    categoria_id = len(categorias) + 1
    categoria = {
        "id": categoria_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "color": color
    }
    categorias.append(categoria)
    return {"mensaje": "Categoría creada", "categoria": categoria}

@app.get("/categorias")
def listar_categorias():
    return categorias
