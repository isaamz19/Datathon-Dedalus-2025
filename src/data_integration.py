import os
import pandas as pd

# 1. Cargar los datasets
cd = os.getcwd()
pacientes = pd.read_csv(f'{cd}/data/raw/cohorte_pacientes.csv')
alergias = pd.read_csv(f'{cd}/data/raw/cohorte_alegias.csv')
condiciones = pd.read_csv(f'{cd}/data/raw/cohorte_condiciones.csv') 
medicacion = pd.read_csv(f'{cd}/data/raw/cohorte_medicationes.csv')
encuentros = pd.read_csv(f'{cd}/data/raw/cohorte_encuentros.csv')
procedimientos = pd.read_csv(f'{cd}/data/raw/cohorte_procedimientos.csv')

# 2. Eliminar duplicados
pacientes = pacientes.drop_duplicates()
medicacion = medicacion.drop_duplicates()
procedimientos = procedimientos.drop_duplicates()
encuentros = encuentros.drop_duplicates()
condiciones = condiciones.drop_duplicates()
alergias = alergias.drop_duplicates()

# 3. Construir el DataFrame principal (df_1)
df_1 = pacientes[['PacienteID', 'Genero', 'Edad', 'Provincia', 'Latitud', 'Longitud']].copy()

# Combinar condiciones y alergias
condiciones_grp = condiciones.groupby('PacienteID').agg({
    'Codigo_SNOMED': lambda x: ', '.join(map(str, x)),
    'Descripcion': lambda x: ', '.join(x)
}).reset_index()

alergias_grp = alergias.groupby('PacienteID').agg({
    'Codigo_SNOMED': lambda x: ', '.join(map(str, x)),
    'Descripcion': lambda x: ', '.join(x)
}).reset_index()

# Merge para asegurar alineación correcta
df_1 = df_1.merge(condiciones_grp, on='PacienteID', how='left', suffixes=('_Condiciones', '_Alergias'))
df_1 = df_1.merge(alergias_grp, on='PacienteID', how='left', suffixes=('_Condiciones', '_Alergias'))

# Verificar si el paciente recibe medicación o ha tenido procedimientos/encuentrosNo


df_1['Medicacion_Actual'] = df_1['PacienteID'].map(medicacion.groupby('PacienteID')['Nombre'].count()).apply(lambda x: 'Sí' if x > 0 else 'No')
df_1['Procedimientos_Realizados'] = df_1['PacienteID'].map(procedimientos.groupby('PacienteID')['Descripcion'].count()).apply(lambda x: 'Sí' if x > 0 else 'No')
df_1['Encuentros_Realizados'] = df_1['PacienteID'].map(encuentros.groupby('PacienteID')['Tipo_encuentro'].count()).apply(lambda x: 'Sí' if x > 0 else 'No')

# 4. Construir el DataFrame de eventos (df_2)
medicacion = medicacion.rename(columns={'Fecha de inicio': 'Fecha_inicio', 'Fecha de fin': 'Fecha_fin'})
procedimientos = procedimientos.rename(columns={'Fecha_inicio': 'Fecha_inicio', 'Fecha_fin': 'Fecha_fin'})
encuentros = encuentros.rename(columns={'Fecha_inicio': 'Fecha_inicio', 'Fecha_fin': 'Fecha_fin'})

# Unificar eventos
df_2 = pd.concat([
    medicacion[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Nombre']].assign(Tipo_Evento='Medicacion'),
    procedimientos[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Descripcion']].assign(Tipo_Evento='Procedimiento'),
    encuentros[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Tipo_encuentro']].assign(Tipo_Evento='Encuentro')
])

df_2['Descripcion_Evento'] = df_2.apply(lambda row: row['Nombre'] if pd.notnull(row['Nombre']) 
                                        else (row['Descripcion'] if pd.notnull(row['Descripcion']) 
                                              else row['Tipo_encuentro']), axis=1)

df_2 = df_2[['PacienteID', 'Fecha_inicio', 'Fecha_fin', 'Tipo_Evento', 'Descripcion_Evento']].sort_values(by=['PacienteID', 'Fecha_inicio'])

# 5. Guardar los datasets
df_1.to_csv(f'{cd}/data/processed/dataset_paciente_final.csv', index=False)
df_2.to_csv(f'{cd}/data/processed/dataset_eventos_final.csv', index=False)

print("Transformación y consolidación de datasets completada.")
