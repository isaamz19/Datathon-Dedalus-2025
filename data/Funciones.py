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


# PACIENTES 

print(pacientes.head())
print(pacientes.describe())
print(pacientes.info())
print(pacientes['Provincia'].unique())
print(pacientes['Latitud'].unique())
print(pacientes['Longitud'].unique())

# cohorte_pacientes contiene 33 filas y 6 columnas. 
# PacienteID --> Es de tipo int64.
# Genero --> Es de tipo object (Maculino y Femenino). Mejor cambiarlos por tipos numéricos: 0 para Masculino y 1 para Femenino
# Edad --> Es de tipo int64. El mínimo son 19 años y el máximo 84. La media son 45 años y medio. El percentil 25 son 30 años, el 50 son 41 y el 75 son 62.
# Provincia --> Es de tipo object (Almería, Córdoba, Huelva, Granada, Málaga, Sevilla). Mejor cambiarlos por tipos numéricos (del 0 al 5).
# Latitud y Longitud --> Estas columnas son inútiles, pues son las mismas latitudes y longitudes para cada provincia.

# ALERGIAS

print(alergias.head())
print(alergias.describe())
print(alergias.info())
print(alergias['Descripcion'].unique())

# FATA MIRAR SI HAY GENTE SIN ALERGIAS ETC

# cohorte_alegias contiene 100 filas y 4 columnas.
# PacienteID --> Es de tipo int64. Son los mismos números que los de PacienteID de PACIENTES (no hay problemas)
# Fecha_diagnostico --> Es de tipo object (año-mes-dia). 
# Codigo_SNOMED --> Es de tipo int64. Código identificativo que dice de forma médica justo lo que hay en la columna la descripción.
# Descripcion --> Es de tipo object (cadenas de string) 
 # (['Alergia al polen' 'Alergia a los frutos secos' 'Alergia a la penicilina'
 # 'Alergia a la leche' 'Alergia a los ácaros del polvo' 'Alergia al látex'
 # 'Alergia al pelo de gato' 'Alergia a la picadura de abeja'
 # 'Alergia a la aspirina' 'Alergia a los mariscos']).




