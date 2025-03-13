import pandas as pd
import openai
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
        texto = f"Paciente {fila['PacienteID']}: Vive en {fila['Provincia']}, Alergias: {fila['Descripcion_Alergias']}, Enfermedades: {fila['Descripcion_Condiciones']}"
        textos.append(texto)
    return textos

def buscar_info(pregunta, textos):
    """Busca el texto más relevante en base a la pregunta (búsqueda simple)."""
    for texto in textos:
        if any(palabra.lower() in texto.lower() for palabra in pregunta.split()):
            return texto
    return "No tengo información relevante en mis datos."

def preguntar_chatbot(pregunta, contexto):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")

    mensajes = [
        {"role": "system", "content": "Responde solo con base en el contexto proporcionado."},
        {"role": "user", "content": f"Pregunta: {pregunta}\nContexto: {contexto}"}
    ]
    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=mensajes
    )
    return response.choices[0].message.content

# Cargar datos
cd = os.getcwd()
data = pd.read_csv(f'{cd}/backend/data/processed/dataset_paciente_final.csv')
textos = cargar_dataset(data)

# Simulación de pregunta del usuario
pregunta_usuario = "¿Cuántos pacientes tienen alergías?"
contexto = buscar_info(pregunta_usuario, textos)
respuesta = preguntar_chatbot(pregunta_usuario, contexto)
print(respuesta)
