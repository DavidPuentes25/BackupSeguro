from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import os
import sqlite3
import zipfile
import shutil
from datetime import datetime
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "clave_secreta_backup"

secret = pyotp.random_base32()

@app.route("/")
def home():
    return redirect(url_for("login"))

def registrar_log(usuario, evento):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO logs (usuario, evento) VALUES (?, ?)",
        (usuario, evento)
    )

    conexion.commit()
    conexion.close()

# Secreto para Google Authenticator
@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":

        usuario = request.form.get("usuario")
        password = request.form.get("password")

        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND password=?",
            (usuario, password)
        )

        user = cursor.fetchone()
        conexion.close()

        if user:
            registrar_log(usuario, "Login correcto")

            session.clear()

            session["usuario_temp"] = usuario
            session["rol_temp"] = user[3]

            return redirect("/verify")

        else:
            registrar_log(usuario, "Login fallido")
            mensaje = "Credenciales incorrectas"

    return render_template("login.html", mensaje=mensaje)

@app.route("/verify", methods=["GET", "POST"])
def verify():

    if "usuario_temp" not in session:
        return redirect(url_for("login"))

    mensaje = ""

    totp = pyotp.TOTP(secret)

    if request.method == "POST":
        codigo = request.form["codigo"]

        if totp.verify(codigo):
            registrar_log(session["usuario_temp"], "2FA correcto")

            session["usuario"] = session["usuario_temp"]
            session["rol"] = session["rol_temp"]

            session.pop("usuario_temp", None)
            session.pop("rol_temp", None)

            return redirect(url_for("dashboard"))

        else:
            registrar_log(session["usuario_temp"], "2FA fallido")
            mensaje = "Código inválido"

    uri = totp.provisioning_uri(
        name="admin@backup.com",
        issuer_name="BackupSeguro"
    )

    img = qrcode.make(uri)

    if not os.path.exists("static"):
        os.mkdir("static")

    img.save("static/qr.png")

    return render_template("verify.html", mensaje=mensaje)

@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Obtener backups
    cursor.execute("""
        SELECT id, nombre, fecha, estado
        FROM backups
        ORDER BY id DESC
        LIMIT 10
    """)

    datos_backups = cursor.fetchall()

    backups = []

    for fila in datos_backups:
        backups.append({
            "id": fila[0],
            "nombre": fila[1],
            "fecha": fila[2],
            "estado": fila[3]
        })

    # Obtener logs
    cursor.execute("""
        SELECT usuario, evento, fecha
        FROM logs
        ORDER BY id DESC
        LIMIT 10
    """)

    logs = cursor.fetchall()

    conexion.close()

    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        backups=backups,
        logs=logs
    )

@app.route("/logout")
def logout():
    if "usuario" in session:
        registrar_log(session["usuario"], "Cierre de sesión")

    session.clear()
    return redirect(url_for("login"))

@app.route("/crear_backup", methods=["GET", "POST"])
def crear_backup():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] not in ["admin", "operador"]:
        return "Acceso denegado"

    if request.method == "POST":

        area = request.form["area"]
        tipo = request.form["tipo"]

        fecha = datetime.now().strftime("%Y-%m-%d")
        nombre = f"Backup_{area}_{tipo}_{fecha}.zip"

        # Crear carpeta backups si no existe
        if not os.path.exists("backups"):
            os.mkdir("backups")

        # Rutas exactas
        if area == "Academico":
            ruta_origen = "datos/academico"
        elif area == "Financiero":
            ruta_origen = "datos/financiero"
        elif area == "RRHH":
            ruta_origen = "datos/rrhh"
        else:
            ruta_origen = "datos/investigacion"

        ruta_destino = f"backups/{nombre}"

        # Crear ZIP real
        with zipfile.ZipFile(ruta_destino, "w") as zipf:

            for carpeta, subcarpetas, archivos in os.walk(ruta_origen):
                for archivo in archivos:
                    ruta_archivo = os.path.join(carpeta, archivo)
                    zipf.write(ruta_archivo, arcname=archivo)

            # Agregar base de datos académica
            if area.lower() == "academico":
                if os.path.exists("academico.db"):
                    zipf.write("academico.db", arcname="academico.db")

        # Guardar en BD
        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO backups (nombre, fecha, estado)
            VALUES (?, ?, ?)
        """, (nombre, fecha, "Correcto"))

        conexion.commit()
        conexion.close()

        registrar_log(session["usuario"], f"Creó backup real {nombre}")

        return redirect(url_for("dashboard"))

    return render_template("crear_backup.html")

@app.route("/eliminar_backup/<int:id>")
def eliminar_backup(id):

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre FROM backups WHERE id=?", (id,))
    backup = cursor.fetchone()

    if backup:

        nombre_archivo = backup[0]

        if not os.path.exists("papelera"):
            os.mkdir("papelera")

        ruta_original = os.path.join("backups", nombre_archivo)
        ruta_nueva = os.path.join("papelera", nombre_archivo)

        if os.path.exists(ruta_original):
            shutil.move(ruta_original, ruta_nueva)

        cursor.execute("DELETE FROM backups WHERE id=?", (id,))
        conexion.commit()

        registrar_log(
            session["usuario"],
            f"Movió backup a papelera: {nombre_archivo}"
        )

    conexion.close()

    return redirect(url_for("dashboard"))

@app.route("/descargar_backup/<nombre>")
def descargar_backup(nombre):

    if "usuario" not in session:
        return redirect(url_for("login"))

    return send_from_directory(
        "backups",
        nombre,
        as_attachment=True
    )

@app.route("/nuevo_usuario", methods=["GET", "POST"])
def nuevo_usuario():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    mensaje = ""

    if request.method == "POST":

        usuario_nuevo = request.form["usuario"]
        password_nuevo = request.form["password"]
        rol_nuevo = request.form["rol"]

        try:
            conexion = sqlite3.connect("database.db")
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                (usuario_nuevo, password_nuevo, rol_nuevo)
            )

            conexion.commit()
            conexion.close()

            registrar_log(session["usuario"], f"Creó usuario {usuario_nuevo}")

            mensaje = "Usuario creado correctamente"

        except:
            mensaje = "Ese usuario ya existe"

    return render_template("nuevo_usuario.html", mensaje=mensaje)

@app.route("/papelera")
def papelera():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    archivos = []

    if os.path.exists("papelera"):
        archivos = os.listdir("papelera")

    return render_template("papelera.html", archivos=archivos)

@app.route("/restaurar_backup/<nombre>")
def restaurar_backup(nombre):

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    ruta_origen = f"papelera/{nombre}"
    ruta_destino = f"backups/{nombre}"

    if os.path.exists(ruta_origen):

        shutil.move(ruta_origen, ruta_destino)

        fecha = datetime.now().strftime("%Y-%m-%d")

        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO backups (nombre, fecha, estado)
            VALUES (?, ?, ?)
        """, (nombre, fecha, "Restaurado"))

        conexion.commit()
        conexion.close()

        registrar_log(session["usuario"], f"Restauró backup {nombre}")

    return redirect(url_for("dashboard"))
if __name__ == "__main__":
    print("Servidor iniciando...")
    app.run(debug=True, host="127.0.0.1", port=5000)

 