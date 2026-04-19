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

cursor.execute("""
INSERT OR IGNORE INTO backups (id, nombre, fecha, estado)
VALUES
(1,'Backup_Academico.zip','2026-04-16','Correcto'),
(2,'Backup_Finanzas.zip','2026-04-15','Correcto'),
(3,'Backup_Investigacion.zip','2026-04-14','Pendiente')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")