import pandas as pd
import openai
import sqlite3
import os

#Ejemplo hehco con OPeNAI
#Nosotros debemos elegir el modelo que mejor se adapte a nuestras necesidades
#En este caso se eligió el modelo bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
#Este modelo es un modelo de lenguaje conversacional que puede ser utilizado para responder preguntas
#sobre un contexto dado. En este caso, se utiliza para responder preguntas sobre pacientes en un hospital.

def cargar_dataset(data):
    """Carga el dataset y lo convierte en una lista de textos."""
    textos = []
    for _, fila in data.iterrows():
        texto = f"Paciente {fila['PacienteID']}: Vive en {fila['Provincia']}, Alergias: {fila['Descripcion_Alergias']}, Enfermedades: {fila['Descripcion_Condiciones']}, Género: {fila['Genero']}"
        textos.append(texto)
    return textos

def buscar_info(pregunta, textos):
    """Busca todos los textos relevantes en base a la pregunta y los concatena."""
    resultados = [texto for texto in textos if any(palabra.lower() in texto.lower() for palabra in pregunta.split())]
    return "\n".join(resultados) if resultados else "No tengo información relevante en mis datos."

  
def preguntar_chatbot(pregunta, contexto):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")

    mensajes = [
        {"role": "system", "content": "Responde con una descripcion de la tabla que se te da"},
        {"role": "user", "content": f"Pregunta: {pregunta}\nContexto: {contexto}"}
    ]
    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=mensajes
    )
    return response.choices[0].message.content

def preguntar_query(pregunta, contexto):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")

    mensajes = [
        {"role": "system", "content": "Responde solo con la query que vaya a darme la informacion necesaría con nada más quiero que tus mensaje se reduzcan únicamente a la query.Ejemplo: SELECT * FROM Pacientes WHERE Alergias = 'si'"},
        {"role": "user", "content": f"Pregunta: {pregunta}\nContexto: {contexto}"}
    ]
    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=mensajes
    )
    return response.choices[0].message.content


# Cargar datos
cd = os.getcwd()
#sdata = pd.read_csv(f'{cd}/backend/data/processed/dataset_paciente_final.csv')
#textos = cargar_dataset(data)
pregunta = "¿Cuántos pacientes son de genero Femenino?"

#1º Descripción completa de nuestra base de datos
descripcion = "Tabla Pacientes con los siguientes campos: Paciente_ID	TEXT UNIQUE,Fecha_nacimiento	TEXT NOT NULL,Fecha_defuncion	TEXT, Raza	TEXT, Etnia	TEXT,Genero TEXT NOT NULL,Provincia	TEXT ,PRIMARY KEY(Paciente_ID)"
query = preguntar_query(pregunta,descripcion)
print(query)
dataset = sqlite3.connect(f'{cd}/backend/data/base_de_datos/Pacientes.db')
# Crear un cursor para ejecutar consultas
cursor = dataset.cursor()
# Obtener nombres de tablas
cursor.execute(query)
tablas = cursor.fetchall()
print("Tablas disponibles:", tablas)

# Cerrar conexión
dataset.close()
respuesta = preguntar_chatbot(pregunta, tablas)
print(respuesta)

