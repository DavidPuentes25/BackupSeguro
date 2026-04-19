import sqlite3

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

# Tabla usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
)
""")

# Tabla backups
cursor.execute("""
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    fecha TEXT,
    estado TEXT
)
""")

# Tabla logs
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    evento TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Usuario admin
cursor.execute("""
INSERT OR IGNORE INTO usuarios (usuario, password)
VALUES ('admin', '1234')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")