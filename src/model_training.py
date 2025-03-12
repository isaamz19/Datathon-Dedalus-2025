import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import os

# Configuración de rutas
DATA_PREPROCESSED_PATH = os.path.join('data', 'preprocessed')
MODELS_PATH = os.path.join('models')

# Función para cargar datos preprocesados
def cargar_datos():
    print("Cargando datos preprocesados...")
    
    train_df = pd.read_csv(os.path.join(DATA_PREPROCESSED_PATH, 'train_pacientes.csv'))
    test_df = pd.read_csv(os.path.join(DATA_PREPROCESSED_PATH, 'test_pacientes.csv'))
    
    print("¡Datos cargados correctamente!")
    return train_df, test_df

# Función para preparar los datos para el modelo
def preparar_datos(train_df, test_df):
    print("\nPreparando datos para el modelo...")
    
    # Convertir los DataFrames a un formato compatible con Hugging Face
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    
    return train_dataset, test_dataset

# Función para cargar el modelo y el tokenizador
def cargar_modelo_y_tokenizador():
    print("\nCargando modelo y tokenizador...")
    
    # Usar GPT-2 como modelo base (puedes cambiarlo por otro modelo)
    model_name = "gpt2"  # También puedes usar "distilbert-base-uncased" o "bert-base-uncased"
    tokenizador = GPT2Tokenizer.from_pretrained(model_name)
    modelo = GPT2LMHeadModel.from_pretrained(model_name)
    
    print(f"¡Modelo {model_name} cargado correctamente!")
    return tokenizador, modelo

# Función para tokenizar los datos
def tokenizar_datos(dataset, tokenizador):
    print("\nTokenizando datos...")
    
    def tokenizar(ejemplo):
        return tokenizador(ejemplo['texto'], truncation=True, padding='max_length', max_length=512)
    
    dataset_tokenizado = dataset.map(tokenizar, batched=True)
    return dataset_tokenizado

# Función para fine-tuning del modelo
def fine_tuning(modelo, train_dataset, test_dataset):
    print("\nFine-tuning del modelo...")
    
    # Configurar los argumentos de entrenamiento
    training_args = TrainingArguments(
        output_dir=os.path.join(MODELS_PATH, 'resultados'),  # Carpeta para guardar resultados
        overwrite_output_dir=True,
        num_train_epochs=3,  # Número de épocas
        per_device_train_batch_size=4,  # Tamaño del batch
        save_steps=500,  # Guardar el modelo cada 500 pasos
        save_total_limit=2,  # Mantener solo los últimos 2 modelos
        evaluation_strategy="steps",  # Evaluar cada cierto número de pasos
        eval_steps=500,  # Evaluar cada 500 pasos
        logging_dir=os.path.join(MODELS_PATH, 'logs'),  # Carpeta para logs
        logging_steps=100,  # Registrar logs cada 100 pasos
    )
    
    # Crear el Trainer
    trainer = Trainer(
        model=modelo,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )
    
    # Entrenar el modelo
    trainer.train()
    
    print("¡Fine-tuning completado!")
    return trainer

# Función para guardar el modelo
def guardar_modelo(trainer):
    print("\nGuardando el modelo...")
    
    if not os.path.exists(MODELS_PATH):
        os.makedirs(MODELS_PATH)
    
    modelo_path = os.path.join(MODELS_PATH, 'modelo_ajustado')
    trainer.save_model(modelo_path)
    
    print(f"¡Modelo guardado en {modelo_path}!")

# Función principal
def main():
    # Cargar datos preprocesados
    train_df, test_df = cargar_datos()
    
    # Preparar los datos para el modelo
    train_dataset, test_dataset = preparar_datos(train_df, test_df)
    
    # Cargar el modelo y el tokenizador
    tokenizador, modelo = cargar_modelo_y_tokenizador()
    
    # Tokenizar los datos
    train_dataset = tokenizar_datos(train_dataset, tokenizador)
    test_dataset = tokenizar_datos(test_dataset, tokenizador)
    
    # Fine-tuning del modelo
    trainer = fine_tuning(modelo, train_dataset, test_dataset)
    
    # Guardar el modelo ajustado
    guardar_modelo(trainer)

if __name__ == "__main__":
    main()