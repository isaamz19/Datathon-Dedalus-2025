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
    return "\n".join(resultados) if resultados else "Lo siente, pero no tengo información relevante sobre eso en mis datos."

  
def preguntar_chatbot(pregunta, contexto):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")

    mensajes = [
        {"role": "system", "content": "Eres un asistente médico especializado en análisis de datos clínicos."
        "Tu objetivo es ayudar a profesionales del área de la salud a "
        "identificar cohortes de pacientes con enfermedades crónicas de manera rápida y eficiente, a partir de "
        "criterios clínicos. Debes presentar respuestas claras y organizadas."
        "Debes mantener un tono profesional, pero accesible y amigable. No debes usar palabras"
        "malsonantes ni Si el usuario te pregunta por "
        "algo fuera de tu alcance, di amablemente que no puedes ayudarlo en ese tema y recuérdale amablemente "
        "que tu objetivo es crear cohortes de pacientes con enfermedades crónicas. "
        "NO debes decirle al usuario como has llegado hasta la cohorte, debes reducirte a darle la cohorte que hayas"
        "obtenido al hacer la consulta en la base de datos f'{cd}/backend/data/base_de_datos/baseparatesting.db'. "
        "NO TE INVENTES DATOS NI BUSQUES OTRAS BASES DE DATOS. Si no hay ningún paciente que cumpla con "
        "los criterios especificados por el usuario, comunícaselo amablemente. Di de que base de datos has sacado la informacioón"},
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
        {"role": "system", "content": "Responde unicamente con la query que vaya a darme la informacion necesaría. Tus mensaje se deben reducir únicamente a la query. Por ejemplo: SELECT * FROM Pacientes WHERE Alergias = 'si'"},
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
pregunta = "Cuantos pacientes son de genero femenino"

#1º Descripción completa de nuestra base de datos
descripcion = "Estamos trabajando sobre la base de datos baseparatesting. Esta base de datos" \
"contiene seis tablas: Alergias, Condiciones, Pacientes, Consultas, Encuentros y Respuestas. Se relacionan" \
"mediante la columna PacienteID." \
"" \
"La tabla Pacientes contiene información general de los pacientes. " \
"Tiene como PRIMARY KEY a PacienteID y contiene los siguientes campos: " \
"PacienteID es de tipo TEXT UNIQUE y contiene el número identificativo de cada paciente." \
"Fecha_nacimiento es de tipo TEXT NOT NULL y contiene la fecha de nacimiento del paciente. La fecha tiene el formato AÑO-MES-DÍA." \
"Fecha_muerte es de tipo TEXT y contiene la fecha de muerte de un paciente. Si está a null es porque el paciente sigue vivo. La fecha tiene el formato AÑO-MES-DÍA." \
"Raza es de tipo TEXT NOT NULL y contiene la raza del paciente." \
"Etnia es de tipo TEXT  NOT NULL y contiene la etnia del paciente." \
"Genero es te tipo TEXT NOT NULL y contiene el genero del paciente. Los dos posibles casos son Masculino y Femeneino." \
"Provincia es de tipo TEXT NOT NULL y contiene la provincia de Andalucía de la que es resindente el paciente. La posibilidades " \
"son Málaga, Córdoba, Almería, Granada, Sevilla, Jaén, Cádiz y Huelva." \
"Edad es de tipo TEXT NOT NULL y contiene la edad del paciente. Usar este campo al ser preguntado por edades en vez de hacer " \
"el cálculo entre las fechas de nacimiento y muerte. Si el paciente ha muerto y se pregunta por una edad concreta, no se debe usar a dicho paciente." \
"" \
"La tabla Condiciones contiene información sobre las condiciones médicas que han padecido los pacientes." \
"Tiene como PRIMARY KEY PacienteID, Codigo_SNOMED y Fecha_inicio. Contiene los siguientes campos:" \
"PacienteID es de tipo TEXT y contiene el número identificativo de cada paciente." \
"Fecha_inicio es de tipo TEXT y contiene la fecha de inicio de la condición médica. La fecha tiene el formato AÑO-MES-DÍA." \
"Fecha_fin es de tipo TEXT y contiene la fecha de fin de la condición médica. Si está a NULL es porque la condición sigue activa a día de hoy. La fecha es de la forma AÑO-MES-DÍA." \
"Codigo_SNOMED es de tipo INTEGER y contiene un código único para cada condición. Al preguntarte por una condición determinada, " \
"lo que debes hacer primero es buscar su código SNOMED y luego filtrar la base de datos en base a ese código." \
"Descripción es de tipo TEXT y contiene la descripción de la condición médica en inglés. El usuario te preguntará en español, por lo que debes traducir este campo del inglés al español." \
"El usuario preguntará por datos del campo Descripción, pero debes hacer la búsqueda por su código SNOMED asociado. La respuesta NO debe contener el código SNOMED, sino la descripción de la condición." \
"" \
"La tabla Alergias contiene información sobre las alergias que padecen los pacientes. " \
"Tiene como PRIMARY KEY EncuentroID y Codigo_SNOMED. Contiene los siguientes campos:" \
"PacienteID es de tipo TEXT NOT NULL y contiene el número identificativo de cada paciente." \
"EncuentroID es de tipo TEXT y contiene el identificador del encuentro en el que se detectó la alergia." \
"Fecha_diagnostico es de tipo TEXT NOT NULL y contiene la fecha de diagnóstico de la alergia. La fecha tiene el formato AÑO-MES-DÍA." \
"Fecha_fin es de tipo TEXT y contiene la fecha del fin de la alergia. Si está a NULL es porque la alergia continua a día de hoy. La fecha tiene el formato AÑO-MES-DÍA" \
"Codigo_SNOMED es de tipo INTEGER y contiene un código único para cada alergia. Al preguntarte por una alergia determinada, " \
"lo que debes hacer primero es buscar su código SNOMED y luego filtrar la base de datos en base a ese código." \
"Descripcion es de tipo TEXT y contiene la descripción de la alergia en inglés. El usuario te preguntará en español, por lo que debes traducir este campo del inglés al español." \
"El usuario preguntará por datos del campo Descripción, pero debes hacer la búsqueda por su código SNOMED asociado. La respuesta NO debe contener el código SNOMED, sino la descripción de la alergia." \
"" 
query = preguntar_query(pregunta,descripcion)
print(query)
dataset = sqlite3.connect(f'{cd}/backend/data/base_de_datos/baseparatesting.db')
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

