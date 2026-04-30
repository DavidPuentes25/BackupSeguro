import sqlite3

conexion = sqlite3.connect("academico.db")
cursor = conexion.cursor()

# Tabla estudiantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT,
    nombre TEXT,
    carrera TEXT,
    semestre INTEGER
)
""")

# Tabla materias
cursor.execute("""
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    creditos INTEGER
)
""")

# Tabla notas
cursor.execute("""
CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante TEXT,
    materia TEXT,
    nota REAL
)
""")

# Insertar estudiantes
cursor.execute("""
INSERT INTO estudiantes (documento, nombre, carrera, semestre)
VALUES ('1001', 'Ana Torres', 'Ingenieria', 4)
""")

cursor.execute("""
INSERT INTO estudiantes (documento, nombre, carrera, semestre)
VALUES ('1002', 'Carlos Ruiz', 'Contaduria', 6)
""")

# Insertar materias
cursor.execute("""
INSERT INTO materias (nombre, creditos)
VALUES ('Bases de Datos', 3)
""")

cursor.execute("""
INSERT INTO materias (nombre, creditos)
VALUES ('Programacion', 4)
""")

# Insertar notas
cursor.execute("""
INSERT INTO notas (estudiante, materia, nota)
VALUES ('Ana Torres', 'Bases de Datos', 4.5)
""")

cursor.execute("""
INSERT INTO notas (estudiante, materia, nota)
VALUES ('Carlos Ruiz', 'Programacion', 4.1)
""")

conexion.commit()
conexion.close()

print("Base academico.db creada correctamente")