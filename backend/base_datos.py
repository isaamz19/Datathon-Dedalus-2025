import sqlite3

# Conectar a la base de datos (reemplaza 'tudb.sqlite' por el nombre de tu archivo)
conexion = sqlite3.connect("tudb.sqlite")

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Obtener nombres de tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print("Tablas disponibles:", tablas)

# Cerrar conexión
conexion.close()
