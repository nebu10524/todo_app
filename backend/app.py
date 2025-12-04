from flask import Flask, request, jsonify, send_from_directory  #Trae las herramientas básicas para que Flask funcione como servidor.
from flask_cors import CORS #permite comunicación entre frontend y backend
import mysql.connector#conecta Python con MySQL
import os

# ===== CONFIGURACIÓN PARA SERVIR FRONTEND =====
# Obtener la ruta absoluta de la carpeta frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Obtiene la ruta donde está app.py
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend') # Construye la ruta a la carpeta frontend

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='') #Crea el servidor web y le dice dónde están los archivos HTML/CSS/JS
CORS(app) #Permite que tu página web (frontend) pueda hablar con tu servidor (backend)

# =======================================================
# === CONEXIÓN A MySQL ===
# =======================================================
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="todo_app"
)

# =======================================================
# === FUNCIÓN AUXILIAR PARA FORMATEAR FECHAS ===
# =======================================================
def formatear_fecha(fecha):
    if fecha is None:
        return None
    return fecha.strftime("%Y-%m-%d")

# =======================================================
# === SERVIR ARCHIVOS DEL FRONTEND ===
# =======================================================
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# =======================================================
# === CRUD DE USUARIOS ===
# =======================================================

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    if not data or "usuario" not in data or "email" not in data or "password" not in data:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario FROM usuarios ORDER BY id_usuario DESC LIMIT 1")
    ultimo = cursor.fetchone()
    
    if ultimo:
        numero = int(ultimo[0][3:]) + 1
        id_usuario = f"USU{numero:03d}"
    else:
        id_usuario = "USU001"

    sql = "INSERT INTO usuarios (id_usuario, usuario, email, password) VALUES (%s, %s, %s, %s)" 
    cursor.execute(sql, (id_usuario, data["usuario"], data["email"], data["password"]))
    conexion.commit()
    cursor.close()

    return jsonify({
        "success": True,
        "message": "Usuario creado exitosamente",
        "usuario": {
            "id_usuario": id_usuario,
            "usuario": data["usuario"],
            "email": data["email"]
        }
    }), 201


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, usuario, email FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify({"success": True, "usuarios": usuarios}), 200


@app.route("/usuarios/<id>", methods=["GET"])
def obtener_usuario(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, usuario, email FROM usuarios WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    if not usuario:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
    return jsonify({"success": True, "usuario": usuario}), 200


@app.route("/usuarios/<id>", methods=["PUT"])
def actualizar_usuario(id):
    data = request.get_json()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    usuario["usuario"] = data.get("usuario", usuario["usuario"])
    usuario["email"] = data.get("email", usuario["email"])
    usuario["password"] = data.get("password", usuario["password"])

    sql = "UPDATE usuarios SET usuario=%s, email=%s, password=%s WHERE id_usuario=%s"
    cursor.execute(sql, (usuario["usuario"], usuario["email"], usuario["password"], id))
    conexion.commit()
    cursor.close()

    return jsonify({
        "success": True, 
        "message": "Usuario actualizado correctamente",
        "usuario": {
            "id_usuario": id,
            "usuario": usuario["usuario"],
            "email": usuario["email"],
            "password": usuario["password"]
        }
    }), 200


@app.route("/usuarios/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conexion.commit()
    cursor.close()
    return jsonify({"success": True, "message": "Usuario eliminado correctamente"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"success": False, "message": "Faltan credenciales"}), 400

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (data["email"], data["password"]))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario:
        return jsonify({"success": True, "message": "Login exitoso", "usuario": usuario}), 200
    else:
        return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401


# =======================================================
# === CRUD DE TAREAS ===
# =======================================================

@app.route("/tareas", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    if not data or "usuario_id" not in data or "texto" not in data:
        return jsonify({"success": False, "message": "Faltan datos (usuario_id, texto)"}), 400

    cursor = conexion.cursor()

    cursor.execute("SELECT id_tarea FROM tareas ORDER BY id_tarea DESC LIMIT 1")
    ultimo = cursor.fetchone()

    if ultimo:
        numero = int(ultimo[0][3:]) + 1
        id_tarea = f"TAR{numero:03d}"
    else:
        id_tarea = "TAR001"

    sql = """
        INSERT INTO tareas (id_tarea, usuario_id, texto, fecha, prioridad, completada)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        id_tarea,
        data["usuario_id"],
        data["texto"],
        data.get("fecha"),
        data.get("prioridad", "media"),
        bool(data.get("completada", False))
    ))
    conexion.commit()
    cursor.close()

    return jsonify({
        "success": True,
        "message": "Tarea creada exitosamente",
        "id_tarea": id_tarea
    }), 201


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    cursor.close()

    for t in tareas:
        t["completada"] = bool(t["completada"])
        t["fecha"] = formatear_fecha(t["fecha"])

    return jsonify({"success": True, "tareas": tareas}), 200


@app.route("/tareas/<id>", methods=["GET"])
def obtener_tarea(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tareas WHERE id_tarea = %s", (id,))
    tarea = cursor.fetchone()
    cursor.close()

    if not tarea:
        return jsonify({"success": False, "message": "Tarea no encontrada"}), 404

    tarea["completada"] = bool(tarea["completada"])
    tarea["fecha"] = formatear_fecha(tarea["fecha"])

    return jsonify({"success": True, "tarea": tarea}), 200


@app.route("/tareas/usuario/<usuario_id>", methods=["GET"])
def obtener_tareas_por_usuario(usuario_id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tareas WHERE usuario_id = %s", (usuario_id,))
    tareas = cursor.fetchall()
    cursor.close()

    for t in tareas:
        t["completada"] = bool(t["completada"])
        t["fecha"] = formatear_fecha(t["fecha"])

    return jsonify({"success": True, "tareas": tareas}), 200


@app.route("/tareas/<id>", methods=["PUT"])
def actualizar_tarea(id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Debe enviar datos para actualizar"}), 400

    campos = []
    valores = []

    if "texto" in data:
        campos.append("texto = %s")
        valores.append(data["texto"])
    if "fecha" in data:
        campos.append("fecha = %s")
        valores.append(data["fecha"])
    if "prioridad" in data:
        campos.append("prioridad = %s")
        valores.append(data["prioridad"])
    if "completada" in data:
        campos.append("completada = %s")
        valores.append(bool(data["completada"]))

    if not campos:
        return jsonify({"success": False, "message": "No hay campos válidos para actualizar"}), 400

    valores.append(id)
    sql = f"UPDATE tareas SET {', '.join(campos)} WHERE id_tarea = %s"

    cursor = conexion.cursor()
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()

    return jsonify({"success": True, "message": "Tarea actualizada correctamente"}), 200


@app.route("/tareas/<id>", methods=["DELETE"])
def eliminar_tarea(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE id_tarea = %s", (id,))
    conexion.commit()
    cursor.close()
    return jsonify({"success": True, "message": "Tarea eliminada correctamente"}), 200


@app.route("/tareas/usuario/<usuario_id>", methods=["DELETE"])
def eliminar_tareas_usuario(usuario_id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE usuario_id = %s", (usuario_id,))
    conexion.commit()
    cursor.close()
    return jsonify({
        "success": True,
        "message": f"Tareas del usuario {usuario_id} eliminadas correctamente"
    }), 200


# =======================================================
# === EJECUTAR SERVIDOR ===
# =======================================================
if __name__ == "__main__":
    print(f"Frontend folder: {FRONTEND_DIR}")
    print(f"Servidor corriendo en http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)