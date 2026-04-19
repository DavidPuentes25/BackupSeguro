import sqlite3

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

# Usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT,
    rol TEXT
)
""")

# Logs
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    evento TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Backups
cursor.execute("""
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado TEXT
)
""")

# Usuario admin
cursor.execute("""
INSERT INTO usuarios (usuario, password, rol)
VALUES ('admin', '1234', 'admin')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")