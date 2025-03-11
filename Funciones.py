import os
import pandas as pd
import csv as csv

cd = os.getcwd()  # obtenemos el path
# Carga de datos para que funcione desde cualquier sitio
#Isa
pacientes = pd.read_csv(f'{cd}/data/cohorte_pacientes.csv')
alergias = pd.read_csv(f'{cd}/data/cohorte_alegias.csv')
#Roo
condiciones = pd.read_csv(f'{cd}/data/cohorte_condiciones.csv') 
medicacion = pd.read_csv(f'{cd}/data/cohorte_medicationes.csv')
#marus
encuentros = pd.read_csv(f'{cd}/data/cohorte_encuentros.csv')
procedimientos = pd.read_csv(f'{cd}/data/cohorte_procedimientos.csv')

#print(pacientes.head())
#print(pacientes.describe())
#print(pacientes.info())

#Patrón por emfeermedades
 #Sustituir los generos por numero y provinciar por nº

#------ Contar días de tratamiento por paciente
# Convertir las columnas de fechas a tipo datetime

condiciones["Fecha_inicio"] = pd.to_datetime(condiciones["Fecha_inicio"])
condiciones["Fecha_fin"] = pd.to_datetime(condiciones["Fecha_fin"])

# Calcular la diferencia en días y añadir una nueva columna
condiciones["Dias"] = (condiciones["Fecha_fin"] - condiciones["Fecha_inicio"]).dt.days

print(condiciones.head())
print(condiciones.describe())

#------ Contar días de tratamiento por paciente
print(medicacion.head())

# Filtrar datos del paciente con id 23
paciente_23 = pacientes[pacientes["PacienteID"] == 23]
condiciones_23 = condiciones[condiciones["PacienteID"] == 23]
medicacion_23 = medicacion[medicacion["PacienteID"] == 23]

# Mostrar datos del paciente 23
print("Datos del paciente 23:")
print(paciente_23)

# Mostrar condiciones del paciente 23
print("\nCondiciones del paciente 23:")
print(condiciones_23)

# Mostrar medicación del paciente 23
print("\nMedicación del paciente 23:")
print(medicacion_23)