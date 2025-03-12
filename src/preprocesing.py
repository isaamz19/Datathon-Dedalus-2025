import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import os

# Configuración de rutas
DATA_FINAL_PATH = os.path.join('data', 'final')
DATA_PREPROCESSED_PATH = os.path.join('data', 'preprocessed')

# Función para cargar datos combinados
def cargar_datos():
    print("Cargando datos combinados...")
    
    df_pacientes = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'pacientes_combinado.csv'))
    df_alergias = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'alergias_combinado.csv'))
    df_enfermedades = pd.read_csv(os.path.join(DATA_FINAL_PATH, 'enfermedades_combinado.csv'))
    
    print("¡Datos cargados correctamente!")
    return df_pacientes, df_alergias, df_enfermedades

# Función para codificar variables categóricas
def codificar_categoricas(df):
    print("\nCodificando variables categóricas...")
    
    # Codificar género (Masculino: 0, Femenino: 1)
    if 'Genero' in df.columns:
        df['Genero'] = df['Genero'].map({'Masculino': 0, 'Femenino': 1})
    
    # Codificar provincia usando One-Hot Encoding
    if 'Provincia' in df.columns:
        encoder = OneHotEncoder(sparse=False, drop='first')
        provincia_encoded = encoder.fit_transform(df[['Provincia']])
        provincia_encoded_df = pd.DataFrame(provincia_encoded, columns=encoder.get_feature_names_out(['Provincia']))
        df = pd.concat([df, provincia_encoded_df], axis=1)
        df = df.drop('Provincia', axis=1)
    
    return df

# Función para normalizar variables numéricas
def normalizar_numericas(df):
    print("\nNormalizando variables numéricas...")
    
    # Normalizar edad
    if 'Edad' in df.columns:
        scaler = StandardScaler()
        df['Edad'] = scaler.fit_transform(df[['Edad']])
    
    return df

# Función para dividir los datos en entrenamiento y prueba
def dividir_datos(df):
    print("\nDividiendo datos en conjuntos de entrenamiento y prueba...")
    
    # Dividir los datos (80% entrenamiento, 20% prueba)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    print(f"Tamaño del conjunto de entrenamiento: {len(train_df)}")
    print(f"Tamaño del conjunto de prueba: {len(test_df)}")
    
    return train_df, test_df

# Función principal
def main():
    # Cargar datos combinados
    df_pacientes, df_alergias, df_enfermedades = cargar_datos()
    
    # Preprocesar datos de pacientes
    df_pacientes = codificar_categoricas(df_pacientes)
    df_pacientes = normalizar_numericas(df_pacientes)
    
    # Dividir datos de pacientes en entrenamiento y prueba
    train_pacientes, test_pacientes = dividir_datos(df_pacientes)
    
    # Guardar datos preprocesados
    if not os.path.exists(DATA_PREPROCESSED_PATH):
        os.makedirs(DATA_PREPROCESSED_PATH)
    
    train_pacientes.to_csv(os.path.join(DATA_PREPROCESSED_PATH, 'train_pacientes.csv'), index=False)
    test_pacientes.to_csv(os.path.join(DATA_PREPROCESSED_PATH, 'test_pacientes.csv'), index=False)
    
    print("\n¡Preprocesamiento completado! Los datos preprocesados se han guardado en /data/preprocessed.")

if __name__ == "__main__":
    main()