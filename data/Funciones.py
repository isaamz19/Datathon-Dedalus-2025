import os
import pandas as pd
import csv as csv

cd = os.getcwd()  # obtenemos el path
# Carga de datos para que funcione desde cualquier sitio
pacientes = pd.read_csv(f'{cd}/cohorte_pacientes.csv')
alergias = pd.read_csv(f'{cd}/cohorte_alegias.csv')
condiciones = pd.read_csv(f'{cd}/cohorte_condiciones.csv') 
medicacion = pd.read_csv(f'{cd}/cohorte_medicationes.csv')
encuentros = pd.read_csv(f'{cd}/cohorte_encuentros.csv')
procedimientos = pd.read_csv(f'{cd}/cohorte_procedimientos.csv')


print(pacientes.head())
print(pacientes.describe())
print(pacientes.info())

 #Sustituir los generos por numero y provinciar por nº


