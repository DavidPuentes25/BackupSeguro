import sqlite3

conexion = sqlite3.connect("rrhh.db")
cursor = conexion.cursor()

# Tabla empleados
cursor.execute("""
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT,
    nombre TEXT,
    cargo TEXT
)
""")

# Tabla cargos
cursor.execute("""
CREATE TABLE IF NOT EXISTS cargos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    salario INTEGER
)
""")

# Tabla vacaciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS vacaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado TEXT,
    dias INTEGER,
    estado TEXT
)
""")

# Datos empleados
cursor.execute("""
INSERT INTO empleados (documento, nombre, cargo)
VALUES ('2001', 'Pedro Lopez', 'Analista')
""")

cursor.execute("""
INSERT INTO empleados (documento, nombre, cargo)
VALUES ('2002', 'Maria Diaz', 'Coordinadora')
""")

# Datos cargos
cursor.execute("""
INSERT INTO cargos (nombre, salario)
VALUES ('Analista', 2800000)
""")

cursor.execute("""
INSERT INTO cargos (nombre, salario)
VALUES ('Coordinadora', 4200000)
""")

# Datos vacaciones
cursor.execute("""
INSERT INTO vacaciones (empleado, dias, estado)
VALUES ('Pedro Lopez', 15, 'Pendiente')
""")

cursor.execute("""
INSERT INTO vacaciones (empleado, dias, estado)
VALUES ('Maria Diaz', 10, 'Aprobado')
""")

conexion.commit()
conexion.close()

print("Base rrhh.db creada correctamente")