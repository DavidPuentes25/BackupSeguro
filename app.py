from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import os
import sqlite3

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
            session.pop("usuario_temp", None)

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
        backups=backups,
        logs=logs
    )

@app.route("/logout")
def logout():
    if "usuario" in session:
        registrar_log(session["usuario"], "Cierre de sesión")

    session.clear()
    return redirect(url_for("login"))

@app.route("/crear_backup")
def crear_backup():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO backups (nombre, fecha, estado)
        VALUES ('Backup_Nuevo.zip', date('now'), 'Correcto')
    """)

    conexion.commit()
    conexion.close()

    registrar_log(session["usuario"], "Backup creado")

    return redirect(url_for("dashboard"))


@app.route("/eliminar_backup/<int:id>")
def eliminar_backup(id):

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM backups WHERE id=?", (id,))

    conexion.commit()
    conexion.close()

    registrar_log(session["usuario"], f"Backup eliminado ID {id}")

    return redirect(url_for("dashboard"))

@app.route("/nuevo_usuario", methods=["GET", "POST"])
def nuevo_usuario():

    if "usuario" not in session:
        return redirect(url_for("login"))

    mensaje = ""

    if request.method == "POST":

        usuario_nuevo = request.form["usuario"]
        password_nuevo = request.form["password"]

        try:
            conexion = sqlite3.connect("database.db")
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
                (usuario_nuevo, password_nuevo)
            )

            conexion.commit()
            conexion.close()

            registrar_log(session["usuario"], f"Creó usuario {usuario_nuevo}")

            mensaje = "Usuario creado correctamente"

        except:
            mensaje = "Ese usuario ya existe"

    return render_template("nuevo_usuario.html", mensaje=mensaje)

if __name__ == "__main__":
    print("Servidor iniciando...")
    app.run(debug=True, host="127.0.0.1", port=5000)

 