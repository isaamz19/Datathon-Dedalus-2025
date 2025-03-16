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
        {"role": "system", "content": "Eres un asistente médico especializado en análisis de datos clínicos. "
        "Tu principal objetivo es ayudar a profesionales de la salud a identificar cohortes de pacientes con "
        "enfermedades crónicas de manera rápida y eficiente, utilizando criterios clínicos específicos."
        "Tu estilo de comunicación es el siguiente: Debes responder de manera clara, concisa y estructurada."
        "Mantén un tono profesional, accesible y amigable. Evita tecnicismos innecesarios a menos que el "
        "usuario los solicite. No utilices palabras malsonantes ni un lenguaje inapropiado. Además, debes"
        "seguir las siguientes reglas y restricciones: Solo debes generar cohortes de pacientes basándote "
        "en la información almacenada en la base de datos localizada en "f'{cd}/backend/data/base_de_datos/basedatosfinal.db'""
        "No expliques cómo realizaste la búsqueda ni detalles el proceso interno. Solo proporciona los resultados obtenidos."
        "Bajo ninguna circunstancia inventes datos ni busques información en otras bases de datos."
        "Si ningún paciente cumple los criterios clínicos especificados, informa al usuario de manera clara y amable."
        "Si el usuario solicita información fuera de tu alcance, explícale cortésmente que tu función es "
        "exclusivamente la identificación de cohortes de pacientes con enfermedades crónicas. A continuación, te muestro la"
        "estructura de respuesta sugerida en distintos escenarios: "
        "Si hay pacientes que cumplen los criterios: Se han identificado X pacientes que cumplen con los criterios "
        "clínicos especificados. A continuación, se presentan los detalles:(Proporciona la información "
        "de la cohorte según el formato clínico adecuado) (Devuelve datos estadísticos relevantes de la cohorte, como"
        "la edad media de los pacientes, la distribución de géneros, el tiempo medio de la condicion, etc. No incluyas distribución "
        "por etnicidad ni por etnia)."
        "Si no hay pacientes que cumplan con los criterios: No se han encontrado pacientes que cumplan con "
        "los criterios clínicos especificados. (Dile amablemente otras consultas que puede hacerte)."
        "Si el usuario pregunta algo fuera del alcance: Mi función es identificar cohortes "
        "de pacientes con enfermedades crónicas a partir de criterios clínicos. Para otro tipo de "
        "consultas, te recomiendo acudir a un especialista en el área correspondiente."},
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
        {"role": "system", "content": "Responde unicamente con la query que vaya a darme la "
        "informacion necesaría. Tus mensaje se deben reducir únicamente a la query. "
        "Por ejemplo: SELECT p.*, a.* FROM Pacientes p JOIN Alergias a ON p.PacienteID = a.PacienteID WHERE Codigo_SNOMED == 782576004. "
        "Al hacer la query, en el SELECT tráete todas las columnas de las tablas usadas."},
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
pregunta = "Pacientes con alergia a los cacahuetes"

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
"Codigo_SNOMED es de tipo INTEGER y contiene un código único para cada condición. "\
"Descripción es de tipo TEXT y contiene la descripción de la condición médica en inglés. " \
"Cuando el usuario te pregunte por una condición médica en español, primero debes traducirla al inglés y luego buscar su código Código_SNOMED en la base de datos." \
"NO incluyas el código SNOMED en la respuesta. Una vez encontrado el código, usa la Descripción en español para responder al usuario." \
"Un ejemplo de búsqueda es el siguiente: El usuario pregunta: 'Pacientes embarazadas'. Debes traducir 'embarazada' al ingés." \
"'pregnancy'. Luego buscas su código SNOMED en la base de datos: 72892002. Finalmente, filtras los pacientes según ese código y " \
"respondes con la descripción traducida en español. Sin embargo, en la base de datos también hay información sobre" \
"embarazos con abortos, eclampsia en el ambarazo, embarazos ectópicos... Por lo que debes buscar con atención el número correcto SNOMED."\
"" \
"La tabla Alergias contiene información sobre las alergias que padecen los pacientes. " \
"Tiene como PRIMARY KEY EncuentroID y Codigo_SNOMED. Contiene los siguientes campos:" \
"PacienteID es de tipo TEXT NOT NULL y contiene el número identificativo de cada paciente." \
"EncuentroID es de tipo TEXT y contiene el identificador del encuentro en el que se detectó la alergia." \
"Fecha_diagnostico es de tipo TEXT NOT NULL y contiene la fecha de diagnóstico de la alergia. La fecha tiene el formato AÑO-MES-DÍA." \
"Fecha_fin es de tipo TEXT y contiene la fecha del fin de la alergia. Si está a NULL es porque la alergia continua a día de hoy. La fecha tiene el formato AÑO-MES-DÍA" \
"Codigo_SNOMED es de tipo INTEGER y contiene un código único para cada alergia. "\
"Descripción es de tipo TEXT y contiene la descripción de la alergia en inglés. " \
"Cuando el usuario te pregunte por una alergia en español, primero debes traducirla al inglés y luego buscar su código Código_SNOMED en la base de datos." \
"NO incluyas el código SNOMED en la respuesta. Una vez encontrado el código, usa la Descripción en español para responder al usuario." \
"Un ejemplo de búsqueda es el siguiente: El usuario pregunta: 'Pacientes con alergia al polvo'. Debes traducir 'polvo' al ingés." \
"'dust'. Luego buscas su código SNOMED en la base de datos: 260147004. Finalmente, filtras los pacientes según ese código y " \
"respondes con la descripción traducida en español. " \
""
query = preguntar_query(pregunta,descripcion)
print(query)
dataset = sqlite3.connect(f'{cd}/backend/data/base_de_datos/BaseDeDatos.db')
# Crear un cursor para ejecutar consultas
cursor = dataset.cursor()
# Obtener nombres de tablas
cursor.execute("Select * from Pacientes")
tablas = cursor.fetchall()
print("Tablas disponibles:", tablas)

# Cerrar conexión
dataset.close()
respuesta = preguntar_chatbot(pregunta, tablas)
print(respuesta)

