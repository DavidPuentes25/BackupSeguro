import sqlite3

conexion = sqlite3.connect("investigacion.db")
cursor = conexion.cursor()

# Tabla proyectos
cursor.execute("""
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nombre TEXT,
    estado TEXT
)
""")

# Tabla investigadores
cursor.execute("""
CREATE TABLE IF NOT EXISTS investigadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    especialidad TEXT
)
""")

# Tabla informes
cursor.execute("""
CREATE TABLE IF NOT EXISTS informes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    fecha TEXT,
    estado TEXT
)
""")

# Datos proyectos
cursor.execute("""
INSERT INTO proyectos (codigo, nombre, estado)
VALUES ('INV001', 'Smart City IoT', 'Activo')
""")

cursor.execute("""
INSERT INTO proyectos (codigo, nombre, estado)
VALUES ('INV002', 'Seguridad Digital', 'Activo')
""")

# Datos investigadores
cursor.execute("""
INSERT INTO investigadores (nombre, especialidad)
VALUES ('Laura Mendoza', 'Ciberseguridad')
""")

cursor.execute("""
INSERT INTO investigadores (nombre, especialidad)
VALUES ('Jorge Perez', 'Analitica de Datos')
""")

# Datos informes
cursor.execute("""
INSERT INTO informes (titulo, fecha, estado)
VALUES ('Informe Trimestral', '2026-04-10', 'Entregado')
""")

cursor.execute("""
INSERT INTO informes (titulo, fecha, estado)
VALUES ('Avance Proyecto INV002', '2026-04-22', 'Pendiente')
""")

conexion.commit()
conexion.close()

print("Base investigacion.db creada correctamente")