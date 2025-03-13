import pandas as pd
import numpy as np
import os


cd = os.getcwd()  # obtenemos el path
df = pd.read_csv(f'{cd}/data/processed/dataset_paciente_final.csv')
df2 = pd.read_csv(f'{cd}/data/processed/dataset_eventos_final.csv')



df['Fecha_inicio'].fillna("frase_relleno", inplace=True)