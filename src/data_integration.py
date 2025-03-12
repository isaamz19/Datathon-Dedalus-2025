import os
import pandas as pd
import csv as csv

# 1. Cargar los datasets
cd = os.getcwd()  # obtenemos el path
pacientes = pd.read_csv(f'{cd}/data/raw/cohorte_pacientes.csv')
alergias = pd.read_csv(f'{cd}/data/raw/cohorte_alegias.csv')
condiciones = pd.read_csv(f'{cd}/data/raw/cohorte_condiciones.csv') 
medicacion = pd.read_csv(f'{cd}/data/raw/cohorte_medicationes.csv')
encuentros = pd.read_csv(f'{cd}/data/raw/cohorte_encuentros.csv')
procedimientos = pd.read_csv(f'{cd}/data/raw/cohorte_procedimientos.csv')

# 2. Limpiar y preprocesar los datos
# Eliminar duplicados
df_paciente = pacientes.drop_duplicates()
df_medicacion = medicacion.drop_duplicates()
df_procedimiento = procedimientos.drop_duplicates()
df_encuentro = encuentros.drop_duplicates()
df_condicion = condiciones.drop_duplicates()
df_alergia = alergias.drop_duplicates()

#Elegir primera distribución de datos
df_1 = df_paciente[['PacienteID', 'Genero', 'Edad', 'Provincia', 'Latitud', 'Longitud']]

# Calcular la geolocalización (hospital más cercano) - Este proceso depende de tus datos y algoritmos específicos.
# Suponiendo que ya tienes la geolocalización o puedes calcularla, se añade la columna
# Aquí solo es un ejemplo ficticio, debes usar la lógica adecuada para determinar el hospital más cercano.
#df_paciente_final['Geolocalizacion'] = 'Hospital Cercano Ejemplo'

# Combinar condiciones médicas y alergias en formato de lista
df_1['Condiciones_Snomed'] = df_condicion.groupby('PacienteID')['Codigo_SNOMED'].apply(lambda x: ', '.join(map(str, x)))
df_1['Descripcion_Condiciones'] = df_condicion.groupby('PacienteID')['Descripcion'].apply(lambda x: ', '.join(x))

df_1['Alergias_Snomed'] = df_alergia.groupby('PacienteID')['Codigo_SNOMED'].apply(lambda x: ', '.join(map(str, x)))
df_1['Descripcion_Alergias'] = df_alergia.groupby('PacienteID')['Descripcion'].apply(lambda x: ', '.join(x))

# Agregar información sobre si el paciente recibe medicación, ha tenido procedimientos, encuentros

df_1['Medicacion_Actual'] = df_medicacion.groupby('PacienteID')['Nombre'].trans(lambda x: 'Sí' if len(x) > 0 else 'No')
df_1['Procedimientos_Realizados'] = df_procedimiento.groupby('PacienteID')['Descripcion'].apply(lambda x: 'Sí' if len(x) > 0 else 'No')
df_1['Encuentros_Realizados'] = df_encuentro.groupby('PacienteID')['Tipo_encuentro'].apply(lambda x: 'Sí' if len(x) > 0 else 'No')


#------------------------------------------------------------------------

#Elegir segunda distribución de datos
# Renombrar columnas para que sean consistentes
df_medicacion = df_medicacion.rename(columns={'Fecha de inicio': 'Fecha_inicio', 'Fecha de fin': 'Fecha_fin'})
df_procedimiento = df_procedimiento.rename(columns={'Fecha_inicio': 'Fecha_inicio', 'Fecha_fin': 'Fecha_fin'})
df_encuentro = df_encuentro.rename(columns={'Fecha_inicio': 'Fecha_inicio', 'Fecha_fin': 'Fecha_fin'})

# Seleccionar y normalizar las columnas
df_medicacion = df_medicacion[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Nombre', 'Dosis','Frecuencia','Vía de administración']]
df_procedimiento = df_procedimiento[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Descripcion']]
df_encuentro = df_encuentro[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Tipo_encuentro']]

# Concatenar los DataFrames
df_2 = pd.concat([df_medicacion, df_procedimiento, df_encuentro])

# Crear columnas 'Tipo_Evento' y 'Descripcion_Evento'
df_2['Tipo_Evento'] = df_2.apply(lambda row: 'Medicacion' if pd.notnull(row['Nombre']) 
                                 else ('Procedimiento' if pd.notnull(row['Descripcion']) 
                                       else 'Encuentro'), axis=1)

df_2['Descripcion_Evento'] = df_2.apply(lambda row: row['Nombre'] if pd.notnull(row['Nombre']) 
                                        else (row['Descripcion'] if pd.notnull(row['Descripcion']) 
                                              else row['Tipo_encuentro']), axis=1)

# Eliminar columnas innecesarias
df_2 = df_2[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Tipo_Evento', 'Descripcion_Evento', 'Dosis', 'Frecuencia', 'Vía de administración']]

# Ordenar por paciente y fecha
df_2 = df_2.sort_values(by=['PacienteID', 'Fecha_inicio'])

# 5. Guardar los datasets finales
df_1.to_csv(f'{cd}/data/processed/dataset_paciente_final.csv', index=False)
df_2.to_csv(f'{cd}/data/processed/dataset_eventos_final.csv', index=False)

print("Transformación y consolidación de datasets completada.")
