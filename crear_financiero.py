import sqlite3

conexion = sqlite3.connect("financiero.db")
cursor = conexion.cursor()

# Tabla presupuesto
cursor.execute("""
CREATE TABLE IF NOT EXISTS presupuesto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area TEXT,
    valor INTEGER
)
""")

# Tabla pagos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor TEXT,
    valor INTEGER,
    fecha TEXT
)
""")

# Tabla ingresos
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto TEXT,
    valor INTEGER,
    fecha TEXT
)
""")

# Datos ejemplo presupuesto
cursor.execute("""
INSERT INTO presupuesto (area, valor)
VALUES ('Tecnologia', 25000000)
""")

cursor.execute("""
INSERT INTO presupuesto (area, valor)
VALUES ('Infraestructura', 60000000)
""")

# Datos pagos
cursor.execute("""
INSERT INTO pagos (proveedor, valor, fecha)
VALUES ('Proveedor Redes SAS', 3500000, '2026-04-15')
""")

cursor.execute("""
INSERT INTO pagos (proveedor, valor, fecha)
VALUES ('Papeleria Central', 1200000, '2026-04-18')
""")

# Datos ingresos
cursor.execute("""
INSERT INTO ingresos (concepto, valor, fecha)
VALUES ('Matriculas', 95000000, '2026-04-10')
""")

cursor.execute("""
INSERT INTO ingresos (concepto, valor, fecha)
VALUES ('Convenios', 18000000, '2026-04-20')
""")

conexion.commit()
conexion.close()

print("Base financiero.db creada correctamente")