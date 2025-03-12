import os
import pandas as pd
import csv as csv

# 1. Cargar los datasets
cd = os.getcwd()  # obtenemos el path
df_1 = pd.read_csv(f'{cd}/data/processed/dataset_paciente_final.csv')
df_2 = pd.read_csv(f'{cd}/data/processed/dataset_eventos_final.csv')

def remove_duplicates(cell):
    if pd.notna(cell):
        unique_values = list(set(cell.split(', ')))
        return ', '.join(unique_values)
    return cell  

df_1['Codigo_SNOMED_Condiciones'] = df_1['Codigo_SNOMED_Condiciones'].apply(remove_duplicates)
df_1['Descripcion_Condiciones'] = df_1['Descripcion_Condiciones'].apply(remove_duplicates)
df_1['Codigo_SNOMED_Alergias'] = df_1['Codigo_SNOMED_Alergias'].apply(remove_duplicates)
df_1['Descripcion_Alergias'] = df_1['Descripcion_Alergias'].apply(remove_duplicates)

#------------------------------------------------------



# 5. Guardar los datasets finales
df_1.to_csv(f'{cd}/data/processed/dataset_paciente_final.csv', index=False)
df_2.to_csv(f'{cd}/data/processed/dataset_eventos_final.csv', index=False)

print("Limpieza de datasets completada.")
