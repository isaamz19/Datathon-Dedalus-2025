import sqlite3
import os

cd = os.getcwd()
# Conectar a la base de datos (reemplaza 'tudb.sqlite' por el nombre de tu archivo)
conexion = sqlite3.connect(f'{cd}/backend/data/base_de_datos/Pacientes.db')

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Obtener nombres de tablas
cursor.execute("SELECT Raza FROM Pacientes where Raza == 'asian';")
tablas = cursor.fetchall()
print("Tablas disponibles:", tablas)


# Cerrar conexión
conexion.close()
