import os
import pandas as pd
import csv as csv

cd = os.getcwd()  # obtenemos el path
# Carga de datos para que funcione desde cualquier sitio
pacientes = pd.read_csv(f'{cd}/data/cohorte_pacientes.csv')
alergias = pd.read_csv(f'{cd}/data/cohorte_alegias.csv')
condiciones = pd.read_csv(f'{cd}/data/cohorte_condiciones.csv') 
medicacion = pd.read_csv(f'{cd}/data/cohorte_medicationes.csv')

encuentros = pd.read_csv(f'{cd}/data/cohorte_encuentros.csv')
procedimientos = pd.read_csv(f'{cd}/data/cohorte_procedimientos.csv')


#print(pacientes.head())
#print(pacientes.describe())
#print(pacientes.info())


print(procedimientos.head())
print(procedimientos.describe())
print(procedimientos.info())

#PacienteID: Es de tipo int y sus valores van de 1 a 30
#Fecha de inicio y fecha de fin: de tipo object, el formato es el siguiente: "YYYY-MM-DD"
#Código SNOMED: Código identificador de la descripción
#Descripción: Cadena de String que explica el procedimiento a seguir, hay 10 tipos distintos de descripción
print(procedimientos['Descripcion'].unique())

print('#------------------------------------------')

print(encuentros.head())
print(encuentros.describe())
print(encuentros.info())

print(encuentros['Tipo_encuentro'].unique())

#PacienteID: Es de tipo int y sus valores van de 1 a 30
#Tipo de encuentro:

 #Sustituir los generos por numero y provinciar por nº


