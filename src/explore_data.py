import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de rutas
DATA_FINAL_PATH = os.path.join('data', 'final')
REPORTS_PATH = os.path.join('reports')

# Función para cargar datos combinados
def cargar_datos():
    print("Cargando datos combinados...")
    
    df_alergias = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'alergias_combinado.csv'))
    df_enfermedades = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'enfermedades_combinado.csv'))
    df_pacientes = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'pacientes_combinado.csv'))
    
    print("¡Datos cargados correctamente!")
    return df_alergias, df_enfermedades, df_pacientes

# Función para estadísticas descriptivas
def estadisticas_descriptivas(df, nombre_dataset):
    print(f"\nEstadísticas descriptivas para {nombre_dataset}:")
    print(df.describe())
    
    if 'Edad' in df.columns:
        print("\nDistribución de edades:")
        print(df['Edad'].value_counts().head())

# Función para visualizaciones
def visualizaciones(df, nombre_dataset):
    print(f"\nGenerando visualizaciones para {nombre_dataset}...")
    
    # Crear carpeta de reportes si no existe
    if not os.path.exists(REPORTS_PATH):
        os.makedirs(REPORTS_PATH)
    
    # Distribución de edades (si existe la columna)
    if 'Edad' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Edad'], bins=30, kde=True)
        plt.title(f'Distribución de Edades en {nombre_dataset}')
        plt.xlabel('Edad')
        plt.ylabel('Frecuencia')
        plt.savefig(os.path.join(REPORTS_PATH, f'distribucion_edad_{nombre_dataset}.png'))
        plt.close()
    
    # Distribución de género (si existe la columna)
    if 'Genero' in df.columns:
        plt.figure(figsize=(6, 4))
        sns.countplot(data=df, x='Genero')
        plt.title(f'Distribución de Género en {nombre_dataset}')
        plt.savefig(os.path.join(REPORTS_PATH, f'distribucion_genero_{nombre_dataset}.png'))
        plt.close()

# Función para detectar valores atípicos
def detectar_valores_atipicos(df, nombre_dataset):
    print(f"\nDetectando valores atípicos en {nombre_dataset}...")
    
    if 'Edad' in df.columns:
        Q1 = df['Edad'].quantile(0.25)
        Q3 = df['Edad'].quantile(0.75)
        IQR = Q3 - Q1
        
        # Definir límites para valores atípicos
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Filtrar valores atípicos
        outliers = df[(df['Edad'] < lower_bound) | (df['Edad'] > upper_bound)]
        print(f"Número de valores atípicos en 'Edad': {len(outliers)}")
        
        if len(outliers) > 0:
            print(outliers.head())

# Función para analizar correlaciones
def analizar_correlaciones(df, nombre_dataset):
    print(f"\nAnalizando correlaciones en {nombre_dataset}...")
    
    if 'Edad' in df.columns and 'Genero' in df.columns:
        # Convertir género a valores numéricos
        df['Genero_num'] = df['Genero'].map({'Masculino': 0, 'Femenino': 1})
        
        # Calcular matriz de correlación
        correlacion = df[['Edad', 'Genero_num']].corr()
        print("Matriz de correlación:")
        print(correlacion)
        
        # Visualizar matriz de correlación
        plt.figure(figsize=(6, 4))
        sns.heatmap(correlacion, annot=True, cmap='coolwarm')
        plt.title(f'Matriz de Correlación en {nombre_dataset}')
        plt.savefig(os.path.join(REPORTS_PATH, f'correlacion_{nombre_dataset}.png'))
        plt.close()

# Función principal
def main():
    # Cargar datos combinados
    df_alergias, df_enfermedades, df_pacientes = cargar_datos()
    
    # Análisis de pacientes
    estadisticas_descriptivas(df_pacientes, 'pacientes')
    visualizaciones(df_pacientes, 'pacientes')
    detectar_valores_atipicos(df_pacientes, 'pacientes')
    analizar_correlaciones(df_pacientes, 'pacientes')
    
    # Análisis de alergias
    estadisticas_descriptivas(df_alergias, 'alergias')
    visualizaciones(df_alergias, 'alergias')
    
    # Análisis de enfermedades crónicas
    estadisticas_descriptivas(df_enfermedades, 'enfermedades')
    visualizaciones(df_enfermedades, 'enfermedades')
    
    print("\n¡Análisis exploratorio completado! Los reportes se han guardado en /reports.")

if __name__ == "__main__":
    main()