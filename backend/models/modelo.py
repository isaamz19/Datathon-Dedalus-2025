import pandas as pd
import openai
import sqlite3
import os
import app as app


#Datos para calcular las estadisticas
def calcular_resumen(tabla):
    """Calcula el resumen de pacientes."""
    if 'PacienteID' not in tabla.columns:
        raise ValueError("La columna 'PacienteID' no existe en la tabla.")
    numero = tabla['PacienteID'].nunique()
    return {
        "totalPatients": int(numero)  # Asegurarnos de que sea un entero
    }

def calcular_distribucion_genero(tabla):
    """ Calcula la distribución de género. """
    gender_counts = tabla['Genero'].value_counts(normalize=True) * 100
    return [{"name": genero, "value": round(valor, 2)} for genero, valor in gender_counts.items()]

def calcular_distribucion_provincias(tabla):
    """ Calcula la distribución por provincias. """
    province_counts = tabla['Provincia'].value_counts(normalize=True) * 100
    return [{"name": provincia, "value": round(valor, 2)} for provincia, valor in province_counts.items()]

def calcular_distribucion_edad(tabla):
    # Eliminar los caracteres no numéricos y convertir la columna 'Edad' en números
    tabla['Edad'] = tabla['Edad'].str.extract('(\d+)').astype(float)
    
    # Eliminar filas con NaN (si alguna edad no pudo ser convertida)
    tabla = tabla.dropna(subset=['Edad'])
    
    # Definir los bins y etiquetas
    bins = [0, 18, 25, 40, 70, 100]  # Rango de edades
    labels = ['<= 18', '19-25', '26-40', '41-70', '> 70']  # Etiquetas para los bins
    
    # Aplicar pd.cut para categorizar las edades
    tabla['Rango Edad'] = pd.cut(tabla['Edad'], bins=bins, labels=labels, right=False)

    # Contar la cantidad de personas por cada rango de edad
    age_distribution = tabla['Rango Edad'].value_counts().sort_index()

    # Suponiendo que hay una columna 'Fecha_muerte' para identificar los fallecidos
    # Filtrar los fallecidos (si la columna 'Fecha_muerte' está presente y tiene valores)
    fallecidos_count = tabla[tabla['Fecha_muerte'].notnull()].shape[0]

    # Construir la lista final con la distribución de edades
    result = [
        {"name": "<= 18", "value": int(age_distribution.get('<= 18', 0))},
        {"name": "19-25", "value": int(age_distribution.get('19-25', 0))},
        {"name": "26-40", "value": int(age_distribution.get('26-40', 0))},
        {"name": "41-70", "value": int(age_distribution.get('41-70', 0))},
        {"name": "> 70", "value": int(age_distribution.get('> 70', 0))},
        {"name": "Fallecidos", "value": int(fallecidos_count)}
    ]
    return result

def preguntar_chatbot(pregunta, contexto, historial_conversacion, num):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")
    
    historial = "\n".join(
        [f"Usuario: {item['pregunta']}\nAsistente: {item['respuesta']}" for item in historial_conversacion if item["respuesta"]]
    )

    mensajes = [
        {"role": "system", "content": "Eres un asistente médico especializado en análisis de datos clínicos. "
        "Tu principal objetivo es ayudar a profesionales de la salud a identificar cohortes de pacientes con "
        "enfermedades crónicas de manera rápida y eficiente, utilizando criterios clínicos específicos."
        "Tu estilo de comunicación es el siguiente: Debes responder de manera clara, concisa y estructurada."
        "Mantén un tono profesional, accesible y amigable. Evita tecnicismos innecesarios a menos que el "
        "usuario los solicite. No utilices palabras malsonantes ni un lenguaje inapropiado. Además, debes"
        "seguir las siguientes reglas y restricciones: Solo debes generar cohortes de pacientes basándote "
        "en la información almacenada en la tabla que se te proporciona."
        "No expliques cómo realizaste la búsqueda ni detalles del proceso interno. Solo proporciona los resultados obtenidos."
        "Bajo ninguna circunstancia inventes datos ni busques información en otras bases de datos."
        "Si la tabla que se te proporciona está vacía, informa al usuario de manera clara y amable de que no tienes datos para responder a esa pregunta."
        "La respuesta concreta que debes dar es: En estos momentos no hay pacientes en nuestra base de datos que cumplan los requisitos que propone. Por favor, introduzca otra consulta."
        "Si el usuario solicita información fuera de tu alcance, explícale cortésmente que tu función es "
        "exclusivamente la identificación de cohortes de pacientes con enfermedades crónicas. A continuación, te muestro la"
        "estructura de respuesta sugerida en distintos escenarios: "
        "Si hay pacientes que cumplen los criterios: Se han identificado exitosamente"
        f"{num}"
        " pacientes que cumplen con los criterios clínicos especificados. A continuación, se presentan los detalles:"
        "(Proporciona la información de la cohorte según el formato clínico adecuado)."
        "No debes contestar con la información específica de cada paciente, sólo con estadísticas generales del conjunto que no sean ni el numero de pacientes , ni estadisticas de la edad ni el genero, ni la provincia."
        "Además, si el usuario lo especifica, puedes recomendarle un par de acciones que se pueden hacer sobre ese conjunto de pacientes dependiendo de las características"
        "comunes de los pacientes. Por ejemplo, puedes recomendarle meterlos en un plan de medicina preventiva."
        "Si el usuario pregunta algo fuera del alcance: Mi función es identificar cohortes "
        "de pacientes con enfermedades crónicas a partir de criterios clínicos. Para otro tipo de "
        "consultas, te recomiendo acudir a un especialista en el área correspondiente."
        "Por otro lado si la pregunta no es acerca de ninguna tabla en concreto sino de la conversación previa que habeis mantenido, aquí puedes acceder a toda la información sobre la conversación previa: "
        f"{historial}"},
        {"role": "user", "content": f"Pregunta: {pregunta}\nTabla: {contexto}"}
    ]
    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=mensajes
    )
    return response.choices[0].message.content

def preguntar_query(pregunta, contexto,pregunta_anterior):
    """Envía la pregunta con el contexto relevante a litellm."""
    client = openai.OpenAI(api_key="sk-P_a0RaVeWsY5R46N1ACKIQ", base_url="https://litellm.dccp.pbu.dedalus.com")
    
    if pregunta_anterior is None:
        pregunta_anterior = 'No hay contexto por el momento.'

    mensajes = [
        {"role": "system", "content": "Genera consultas SQL precisas alineadas con la intención del usuario."
        "Devuelve declaraciones SQL sin explicaciones ni comentarios."
        "Prefija todas las columnas seleccionadas o contadas con el nombre de la tabla y envuélvelas entre comillas dobles."
        "No uses marcadores de posición (por ejemplo, nombre_de_tabla, nombre_de_columna)."
        "Asume una base de datos SQLite y evita funciones no disponibles en ella."
        "Prefiere soluciones simples con llamadas mínimas a funciones o condiciones booleanas redundantes.No uses alias de tabla."
        "Al comparar cadenas, conviértelas a minúsculas usando LOWER() y identifica las coincidencias con LIKE '%palabra%'."
        "Por ejemplo: SELECT p.*, a.* FROM Pacientes p JOIN Alergias a ON p.PacienteID = a.PacienteID WHERE p.Edad = 'X años' AND a.Descripcion = 'Alergia al polen'."
        "Al hacer la query, en el SELECT tráete todas las columnas de las tablas usadas."
        "Esta es la pregunta anterior que se te hizo el caso es que si te pide ango de lo anterior fijate aquí para construir la quary si se necesita contexto."
        f"{pregunta_anterior}"},
        {"role": "user", "content": f"Pregunta: {pregunta}\nContexto: {contexto}"}
    ]

    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-haiku-20240307-v1:0",
        messages=mensajes
    )
    return response.choices[0].message.content


#1º Descripción completa de nuestra base de datos
descripcion = "Estamos trabajando sobre una base de datos que" \
"contiene siete tablas cuyos nombres son Alergias, Condiciones, Pacientes, Inmunizaciones, Medicacion, Procedimientos y Encuentros. Se relacionan" \
"mediante la columna PacienteID y EncuentroID." \
"" \
"La tabla Pacientes contiene información general de los pacientes. " \
"Tiene como PRIMARY KEY a PacienteID y contiene las siguientes columnas: " \
"PacienteID es de tipo TEXT UNIQUE." \
"Fecha_nacimiento es de tipo TEXT NOT NULL. La fecha tiene el formato AÑO-MES-DÍA (YYYY-MM-DD) como por ejemplo 2014-06-10." \
"Fecha_muerte es de tipo TEXT. Si está a NULL es porque el paciente sigue vivo. La fecha tiene el formato AÑO-MES-DÍA (YYYY-MM-DD) como por ejemplo 2014-06-10." \
"Raza es de tipo TEXT NOT NULL. Los 6 valores distintos que contiene son Blanco/Caucásico, Asiático, Negro/Afrodescendiente" \
"Nativo de Hawái, Otra raza y Indígena/Nativo Americano." \
"Genero es te tipo TEXT NOT NULL. Los casos son Masculino y Femenino." \
"Provincia es de tipo TEXT NOT NULL. Los posibles casos son Málaga, Córdoba, Almería, Granada, Sevilla, Jaén, " \
"Cádiz y Huelva." \
"Edad es de tipo TEXT NOT NULL. Los casos posibles son X años, X meses, X semanas y X días."\
"" \
"La tabla Condiciones contiene información sobre las condiciones médicas que han padecido los pacientes." \
"Tiene como PRIMARY KEY PacienteID, Codigo_SNOMED y Fecha_inicio. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT." \
"Fecha_inicio es de tipo TEXT. La fecha tiene el formato AÑO-MES-DÍA (YYYY-MM-DD) como por ejemplo 2014-06-10." \
"Fecha_fin es de tipo TEXT. Si está a NULL es porque la condición sigue activa a día de hoy. La fecha es de la forma AÑO-MES-DÍA(YYYY-MM-DD) como por ejemplo 2014-06-10." \
"Codigo_SNOMED es de tipo INTEGER. "\
"Condicion es de tipo TEXT. Los posibles casos son: Revisión de medicación pendiente, Pérdida de dientes, Educación superior recibida, Hipertensión, Índice de masa corporal 30+ - obesidad, Prediabetes, Síndrome metabólico X, Empleo a tiempo completo, Empleo a tiempo parcial, Estrés, Comportamiento de consumo de alcohol no saludable, Gingivitis, Sinusitis viral, Enfermedad gingival, Caries dental primaria, Faringitis estreptocócica, Bronquitis, Osteoartritis de cadera, Desempleado, Contacto social limitado, Empaste dental flojo, Empaste dental fracturado, Participación en actividad de riesgo, Educado hasta nivel de secundaria, Embarazo normal, Faringitis viral aguda, No en la fuerza laboral, Aislamiento social, Lesión por quemadura, Quemadura de espesor parcial, Vivienda insatisfactoria, Falta de acceso al transporte, Anemia, Problema de transporte, Historial de ligadura de trompas, Dolor crónico, Dolor crónico en el cuello, Informes de violencia en el entorno, Pólipo de colon, Aborto espontáneo en el primer trimestre, Aborto espontáneo completo, Pólipo rectal recurrente, Historial de aborto espontáneo en embarazo previo, Hiperlipidemia, Víctima de abuso de pareja íntima, Infección dental, Trastorno del sueño, Síndrome de apnea obstructiva del sueño, Enfermedad cardíaca isquémica, Hallazgos anormales en imágenes diagnósticas del corazón y circulación coronaria, Abuso de drogas, Dolor lumbar crónico, Fibromialgia, Sinusitis crónica, Insuficiencia mitral, Fractura de brazo, Fractura de clavícula, Alzheimer, Neoplasia maligna de colon, Esguince, Esguince de tobillo, Asma infantil, Infección urinaria recurrente, Otitis media, Fractura de antebrazo, Migraña, Molares impactados, Índice de masa corporal 40+ - obesidad severa, Sin hogar, Tiene antecedentes penales, Enfermedad sospechada causada por el coronavirus SARS-CoV-2, Dolor de cabeza, Tos, Fatiga, Fiebre, Pérdida del gusto, Gripe, Neumonía, Hipoxemia, Dificultad respiratoria, Abuso dependiente de drogas, Ansiedad severa (pánico), Óvulo inviable, Empaste dental con filtración, Infarto de miocardio, Infarto de miocardio sin elevación del segmento ST, Historial de infarto de miocardio, Osteoartritis de rodilla, Refugiado, Resorción del proceso alveolar debido a trauma dental, Empaste dental perdido, Enfermedad renal crónica etapa 1, Trastorno renal debido a diabetes mellitus, Enfermedad renal crónica etapa 2, Microalbuminuria debido a diabetes mellitus tipo 2, Esguince de muñeca, Enfermedad renal crónica etapa 3, Proteinuria debido a diabetes mellitus tipo 2, Alveolitis de la mandíbula, Torus palatino, Sinusitis bacteriana aguda, Enfisema pulmonar, Falleció en hospicio, Cistitis infecciosa aguda, Esterilización solicitada, Laceración - lesión, Laceración de mano, Herida por arma de fuego, Herida por bala, Sólo recibió educación primaria, Sepsis, Lesión cerebral traumática o no traumática, Meningomielocele, Malformación de Chiari tipo II, Deformidad congénita del pie, Hidrocefalia, Alergia a la proteína de látex de Hevea brasiliensis, Enfermedad infecciosa del tracto urinario, Úlcera por presión, Fibrilación auricular, Sinusitis, Fractura de tobillo, Diabetes tipo 2, Hiperglucemia, Hipertrigliceridemia, Laceración facial, Embolia pulmonar aguda, Lesión de rodilla, Lesión del ligamento colateral medial de la rodilla, Lesión cerebral por conmoción, Conmoción sin pérdida de conciencia, Osteoporosis, Ruptura de apéndice, Apendicitis, Antecedentes de apendicectomía, Trastorno convulsivo, Antecedentes de convulsiones, Lesión de cuello, Lesión por latigazo cervical, Disnea, Sibilancias, Insuficiencia respiratoria aguda, Fractura cerrada de cadera, Trastorno inflamatorio por aumento de los niveles de urato en sangre, Neuropatía debido a diabetes mellitus tipo 2, Hallazgo de esputo, Laceración de antebrazo, Pre-eclampsia, Rinitis alérgica perenne con variación estacional, Eclampsia en el embarazo, Náusea, Vómitos, Sepsis causada por virus, Shock séptico, Síndrome de dificultad respiratoria aguda, Dolor muscular, Dolor articular, Servicio militar, Bronquitis crónica obstructiva, Apnea del sueño, Enfermedad renal crónica etapa 4, Esperando trasplante de riñón, Antecedentes de bypass coronario, Enfermedad infecciosa bacteriana, Embarazo tubárico, Conmoción con pérdida de conciencia, Enfermedad renal terminal, Antecedentes de trasplante renal, Neoplasia maligna superpuesta de colon, Dolor de garganta, Epilepsia, Fractura subluxación de muñeca, Fracaso y rechazo de trasplante renal, Fractura de costilla, Luxación traumática de la articulación temporomandibular, Infección por virus de inmunodeficiencia humana, Hepatitis C crónica, Cáncer de pulmón sospechado, Cáncer de pulmón no microcítico, Cáncer de próstata sospechado, Neoplasia de próstata, Carcinoma in situ de próstata, Carcinoma de pulmón de células pequeñas, Retinopatía debido a diabetes mellitus tipo 2 y Asma"\
"" \
"La tabla Alergias contiene información sobre las alergias que padecen los pacientes. " \
"Tiene como PRIMARY KEY EncuentroID y Codigo_SNOMED. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT NOT NULL." \
"EncuentroID es de tipo TEXT." \
"Fecha_diagnostico es de tipo TEXT NOT NULL. La fecha tiene el formato AÑO-MES-DÍA (YYYY-MM-DD) como por ejemplo 2014-06-10." \
"Codigo_SNOMED es de tipo INTEGER. "\
"Descripcion es de tipo TEXT. Los posibles valores son:  Alergia a los ácaros del polvo, Alergia al polen, Alergia a la aspirina, Alergia al moho, Alergia al cacahuete, Alergia a la penicilina, Alergia al trigo, Alergia al pelo de gato, Alergia al látex, Alergia a los mariscos, Alergia al pescado, Alergia a los frutos secos, Alergia al huevo, Alergia a la picadura de abeja y Alergia al ibuprofeno." \
"" \
"La tabla Encuentros contiene información sobre las asistencia de los pacientes a algún encuentro médico. " \
"Tiene como PRIMARY KEY EncuentroID. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT NOT NULL." \
"EncuentroID es de tipo TEXT." \
"Fecha_inicio es de tipo TEXT NOT NULL. La fecha tiene el formato AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Fecha_fin es de tipo TEXT NOT NULL. La fecha es de la forma AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Codigo_encuentro es de tipo INTEGER NOT NULL. " \
"Tipo_encuentro es de tipo TEXT. Los posibles valores son: Atención primaria, Hospital (Si te dicen persona que haya ideo al hospital y nada más se refiere a esto si te da alguna mas informacion ya ves cual es más adecuada entre las otras opciones), Urgencia, Hospicio, Casa y Virtual."\
"Descripcion es de tipo TEXT. Los posibles valores son: Visita del niño sano, Consulta por problema, Examen general del paciente, Consulta para chequeo, Visita postnatal, Consulta por síntoma, Consulta de seguimiento, Administración de vacuna para producir inmunidad activa, Consulta para tratamiento, Visita prenatal inicial, Visita prenatal, Clínica de atención urgente, Procedimiento de encuentro con paciente, Admisión en sala de emergencia, Admisión hospitalaria, Admisión al departamento de cirugía, Admisión hospitalaria por emergencia obstétrica, Visita domiciliaria, Seguimiento de asma, Admisión en hospicio, Admisión hospitalaria de emergencia por asma, Visita al consultorio, Tratamiento de emergencia, Admisión hospitalaria de emergencia, Admisión hospitalaria para aislamiento, Rehabilitación y desintoxicación de drogas, Evaluación y manejo de paciente domiciliario o en hogar de reposo, Visita de seguimiento postoperatorio, Admisión al departamento de cirugía torácica, Certificación de defunción, Consulta iniciada por el paciente, Admisión ortopédica no urgente, Entrevista psiquiátrica inicial con evaluación del estado mental, Visita de seguimiento, Traslado de paciente a unidad de cuidados intensivos, Admisión a sala hospitalaria, Admisión a unidad de cuidados intensivos, Admisión al departamento de trasplante quirúrgico, Consulta telefónica, Evaluación inicial de trastorno alérgico, Procedimiento ambulatorio, Evaluación de seguimiento de trastorno alérgico, Admisión al departamento de oncología clínica, Reevaluación periódica y manejo de individuo sano, Vigilancia de detección, Consulta de telemedicina con paciente, Servicio de ginecología, Trastorno de estrés postraumático, Visita al médico con evaluación y/o manejo, Traslado a unidad de transición, Consulta por videotelefonía, Discusión sobre tratamiento, Visita de paciente a departamento de emergencia, Coordinación preoperatoria, Procedimiento quirúrgico y Consulta indirecta." \
"" \
"La tabla Inmunizaciones contiene información sobre las inmunizaciones/vacunaciones recibidas por los pacientes. " \
"Tiene como PRIMARY KEY EncuentroID y Codigo. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT NOT NULL." \
"EncuentroID es de tipo TEXT." \
"Fecha es de tipo TEXT NOT NULL. La fecha tiene el formato AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Codigo es de tipo INTEGER. " \
"Descripcion es de tipo TEXT. Los posibles valores son: Influenza estacional inyectable sin conservante, Vacuna contra el herpes zóster viva, Td (adulto) 5 Lf toxoide tetánico sin conservante adsorbido, Hepatitis A pediátrico/adolescente 2 dosis, Varicela, Polio inactivada (IPV), DTPa, Triple viral (SRP), HPV cuadrivalente, Vacuna meningocócica MCV4P, COVID-19 mRNA LNP-S PF 100 mcg/0.5mL o 50 mcg/0.25mL, Hepatitis B adulto, Vacuna COVID-19 vector-nr rS-Ad26 PF 0.5 mL, Hepatitis B adolescente o pediátrico, Hib (PRP-OMP), Rotavirus monovalente, Vacuna conjugada neumocócica PCV 13, COVID-19 mRNA LNP-S PF 30 mcg/0.3 mL, Vacuna neumocócica polisacárida 23 valente, Hepatitis A adulto, Vacuna toxoide tetánico, toxoide diftérico reducido y tos ferina acelular adsorbida." \
"" \
"La tabla Medicacion contiene información sobre los medicamentos tomados por los pacientes. " \
"Tiene como PRIMARY KEY Fecha_inicio, Fecha_fin, EncuentroID y Codigo. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT NOT NULL." \
"EncuentroID es de tipo TEXT." \
"Fecha_inicio es de tipo TEXT. La fecha tiene el formato AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Fecha_fin es de tipo TEXT. La fecha es de la forma AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Codigo es de tipo INTEGER. " \
"Via_de_administracion es de tipo TEXT. Los posibles valores son: oral, intrauterino, implante, inyección, inhalación y tópica." \
"Frecuencia es de tipo TEXT. Los posibles valores a tener en cuenta incluyen una descripción de su toma entre paréntesis, la cual se debe tener en cuenta: 1 vez al día (dosis matutina), 1 vez al día (con o sin alimentos), Aplicar 1-2 veces al día (uso dental nocturno), 4 veces al día (cada 6 horas), Cada 4-6 horas (máx 4 g/día), 2 veces al día con comida, Cada 6-8 horas (no exceder 4 dosis en 24 horas), 1 vez al día (antihistamínico no sedante), Uso en emergencias (1 dosis, repetir a los 5-15 minutos si es necesario), 1 tableta diaria (anticonceptivo oral combinado), 1 tableta diaria (anticonceptivo, misma hora cada día), 1 tableta diaria (anticonceptivo con estrógeno y progestina), Aplicación única (efectivo hasta 6 años), 2 veces al día (cada 12 horas, con alimentos), Cada 4-6 horas (dolor moderado-severo; máx 4 g de paracetamol/día), 1 vez al día (control de presión arterial), 3 veces al día, Aplicación única (efectivo hasta 3 años), 1 inyección cada 3 meses (anticonceptivo), 1 vez al día (control de presión/frecuencia cardíaca), 1-2 pulsaciones cada 5 minutos (máx 3 dosis en 15 min), Cada 6 horas (dolor severo; máx 4 g de paracetamol/día), Cada 12 horas (no triturar), 2-4 inhalaciones cada 4-6 horas (crisis asmática), Cada 4-6 horas (dolor moderado), 2 veces al día (Alzheimer, con las comidas), Según protocolo de quimioterapia (dosis variable), Infusión cada 2 semanas (ciclo oncológico), 1 vez al día (demencia, por la mañana), 2 inhalaciones diarias (prevención de asma), Nebulizar cada 4-6 horas (uso agudo), 3 veces al día (cada 8 horas, infecciones bacterianas), Cada 6-8 horas (máx 1200 mg/día), 1 parche cada 72 horas (dolor crónico), 1 tableta diaria (anticonceptivo extendido), 1 tableta diaria (anticonceptivo de progestágeno solo), Cada 6 horas (dolor moderado), 1 vez al día (antiagregante plaquetario), 1 vez al día (noche, colesterol), 1 inyección diaria (profilaxis trombosis), Cada 6-8 horas (máx 4 g/día), 1 tableta diaria (anticonceptivo progestínico), Cada 4-6 horas (pediátrico, ajustar por peso), 1 vez al día (dolor/antiinflamatorio), Cada 4-6 horas (dolor agudo, hospitalario), Infusión continua (angioplastia), 1 vez al día (síndrome coronario agudo), 1 vez al día (prevención cardiovascular), 1 vez al día (noche, hipercolesterolemia), 1 vez al día (hipertensión), 1 inyección mensual (déficit de B12), 3 veces al día (cada 8 horas, con alimentos), 1 tableta diaria (anticonceptivo combinado), 1 tableta diaria (anticonceptivo oral), Cada 6-8 horas (infecciones graves), 2 infusiones diarias (ajustar por niveles séricos), Infusión continua (shock séptico/hipotensión), 1 vez al día (control de frecuencia cardíaca), 1 vez al día (noche, alto riesgo cardiovascular), 1 vez al día (fallo cardíaco/hipertensión), Cada 6-8 horas (máx 3200 mg/día), 1 vez al día (en ayunas, con vitamina C), 3 veces al día (arritmias/angina), 1 vez al día (ajustar según INR), 1 vez al día (monitorear niveles séricos), Cada 4-6 horas (dolor leve-moderado), 1 vez al día (diabetes tipo 2, con cena), 1 inyección diaria (tratamiento trombosis), 1 vez a la semana (osteoporosis, en ayunas), 2 veces al día (epilepsia/neuralgia), 2 inhalaciones cada 4-6 horas (crisis asmática), Cada 3-4 horas (dolor agudo, uso hospitalario), Aplicación única (efectivo hasta 5 años), Aplicar 1-2 veces al día (dermatitis), 1 vez al día (alergias estacionales), 2 veces al día (cada 12 horas), 1 vez al día durante 3-5 días, 1 parche semanal (cambiar cada 7 días), 1 vez al día (pediátrico), Dosis única (intubación quirúrgica), Uso en quirófano (concentración ajustada), Infusión continua (anestesia general), Cada 8 horas (infecciones graves), 1 inyección diaria (ajustar por niveles séricos), 2 inhalaciones diarias (asma), 1 vez al día (antihistamínico - OBSOLETO por riesgo cardíaco), 2 veces al día (infecciones bacterianas), Infusión única (ictus isquémico agudo/protocolo específico), 1 vez al día (VIH), 2-3 veces al día (ansiedad/epilepsia), 2-4 veces al día (ansiedad/espasmos), Infusión cada 3 semanas (cáncer), Uso en quirófano (concentración ajustada por anestesiólogo), Dosis única (anestesia general de corta duración), 1 vez al día durante 3-5 días (ciclo de quimioterapia), 2 veces al día con alimentos (dolor/antiinflamatorio), 1 vez al día (depresión/neuropatía diabética), 4 veces al día (infecciones bacterianas), Cada 4-6 horas (máx 4 g de paracetamol/día), Infusión continua (dolor postoperatorio intenso), 2 veces al día (dolor neuropático), 2 veces al día (infecciones respiratorias), 1-2 veces al día (edema/insuficiencia cardíaca), Dosis única o dividida (urgencias hospitalarias), 1-2 veces al día (TDAH, por la mañana), 1 vez al día (en ayunas, hipotiroidismo), Dosis según necesidad (ansiedad/espasmos), 1 vez al día (mañana, enfermedades inflamatorias), 1 inhalación diaria (fibrosis quística), 3 veces al día (con las comidas), 2 infusiones diarias (infecciones graves), 2 veces al día (síndrome coronario agudo), 2 veces al día (arritmias/hipertensión), 2 veces al día (dosis inicial), 1 vez al día (fallo cardíaco), 1 vez al día (demencia), 1 vez al día (prevención de trombosis), 1 vez al día (dependencia a opioides), 2 veces al día (insuficiencia cardíaca), 1 parche diario (terapia de reemplazo de nicotina), Infusión continua (según requerimiento clínico) y Cada 4-6 horas (dolor severo, uso hospitalario)." \
"Descripcion es de tipo TEXT. Los posibles valores son: Hidroclorotiazida 25 MG Tableta Oral, Amlodipino 2.5 MG Tableta Oral, Fluoruro de sodio 0.0272 MG/MG Gel Oral, Penicilina V Potasio 250 MG Tableta Oral, Paracetamol 325 MG Tableta Oral, Naproxeno sódico 220 MG Tableta Oral, Paracetamol 21.7 MG/ML / Bromhidrato de dextrometorfano 1 MG/ML / Succinato de doxilamina 0.417 MG/ML Solución Oral, Hidrocloruro de fexofenadina 30 MG Tableta Oral, Epinefrina 1 MG/ML Auto-Inyector 0.3 ML, Liletta 52 MG Sistema Intrauterino, Cefuroxima 250 MG Tableta Oral, Paracetamol 325 MG / Bitartrato de hidrocodona 7.5 MG Tableta Oral, Lisinopril 10 MG Tableta Oral, Simvastatina 10 MG Tableta Oral, Amoxicilina 250 MG / Clavulanato 125 MG Tableta Oral, Etonogestrel 68 MG Implante, 1 ML Acetato de medroxiprogesterona 150 MG/ML Inyección, Metoprolol succinato 100 MG Tableta Oral de Liberación Prolongada 24 Horas, Nitroglicerina 0.4 MG/ACTUACIÓN Spray Mucosal, Paracetamol 325 MG / Hidrocloruro de oxicodona 10 MG Tableta Oral [Percocet], Bitartrato de hidrocodona 10 MG Cápsula Oral de Liberación Prolongada 12 Horas, Albuterol 0.83 MG/ML Solución para Inhalación, Paracetamol 300 MG / Bitartrato de hidrocodona 5 MG Tableta Oral, Galantamina 4 MG Tableta Oral, Leucovorina 100 MG Inyección, Oxaliplatino 5 MG/ML Inyección 10 ML, Clorhidrato de donepezilo 10 MG / Clorhidrato de memantina 28 MG Cápsula Oral de Liberación Prolongada 24 Horas, Fluticasona propionato 0.044 MG/ACTUACIÓN Inhalador de Dosis Medida [Flovent], Albuterol 0.21 MG/ML Solución para Inhalación, Mirena 52 MG Sistema Intrauterino, Amoxicilina 500 MG Tableta Oral, Ibuprofeno 100 MG Tableta Oral, Fentanilo 0.025 MG/HR Sistema Transdérmico 72 Horas, Paracetamol 325 MG / Hidrocloruro de oxicodona 5 MG Tableta Oral, Hidrocloruro de oxicodona 15 MG Tableta Oral de Liberación Prolongada 12 Horas (Con Prevención de Abuso), Clopidogrel 75 MG Tableta Oral, Simvastatina 20 MG Tableta Oral, Jeringa Precargada con Enoxaparina Sódica 100 MG/ML 0.4 ML, Paracetamol 500 MG Tableta Oral, Paracetamol 160 MG Tableta Masticable, Aspirina 325 MG Tableta Oral, Sulfato de morfina 1 MG/ML Inyección 2 ML, Bivalirudina 5 MG/ML Inyección 50 ML, Prasugrel 10 MG Tableta Oral, Aspirina 81 MG Tableta Oral, Atorvastatina 40 MG Tableta Oral, Lisinopril 40 MG Tableta Oral, Vitamina B12 5 MG/ML Solución Inyectable, Amoxicilina 250 MG Cápsula Oral, Fluticasona propionato 0.25 MG/ACTUACIÓN / Salmeterol 0.05 MG/ACTUACIÓN Inhalador de Polvo Seco, Albuterol 5 MG/ML Solución para Inhalación, Nitrofurantoína macrocristales 25 MG / Nitrofurantoína monohidrato 75 MG Cápsula Oral, Piperacilina 2000 MG / Tazobactam 250 MG Inyección, Vancomicina 5 MG/ML Inyección 150 ML, Norepinefrina 1 MG/ML Inyección 4 ML, Metoprolol succinato 50 MG Tableta Oral de Liberación Prolongada 24 Horas, Atorvastatina 80 MG Tableta Oral, Ramipril 10 MG Cápsula Oral, Ibuprofeno 400 MG Tableta Oral [Ibu], Sulfato Ferroso 325 MG Tableta Oral, Verapamilo clorhidrato 80 MG Tableta Oral, Warfarina Sódica 5 MG Tableta Oral, Digoxina 0.125 MG Tableta Oral, Ibuprofeno 200 MG Tableta Oral, Medroxiprogesterona Acetato 150 MG/ML Inyección 1 ML, Metformina clorhidrato 500 MG Tableta Oral de Liberación Prolongada 24 Horas, Jeringa Precargada con Enoxaparina Sódica 150 MG/ML 1 ML, Ácido Acetlsalicílico 10 MG Tableta Oral, Carbamazepina 20 MG/ML Suspensión Oral [Tegretol], Albuterol 0.09 MG/ACTUACIÓN Inhalador de Dosis Medida [NDA020503], Meperidina Clorhidrato 50 MG Tableta Oral, Kyleena 19.5 MG Sistema Intrauterino, Hidrocortisona 10 MG/ML Crema Tópica, Loratadina 10 MG Tableta Oral, Doxiciclina Hiclato 100 MG, Azitromicina 250 MG, Penicilina V Potásica 500 MG Tableta Oral, Etinilestradiol 0.00146 MG/HR / Norelgestromina 0.00625 MG/HR Sistema Transdérmico 168 Horas, Loratadina 5 MG Tableta Masticable, Tramadol Clorhidrato 50 MG Tableta Oral, Rocuronio Bromuro 10 MG/ML Solución Inyectable, Sevoflurano 1000 MG/ML Solución para Inhalación, Remifentanilo 2 MG Inyección, Vancomicina 1000 MG Inyección, Piperacilina 4000 MG / Tazobactam 500 MG Inyección, Paracetamol 325 MG Tableta Oral [Tylenol], Montelukast 10 mg Tableta Oral, Paroxetina 20 mg Tableta Oral, Tacrolimus 5 MG/ML Inyección 1 ML, Sertralina 50 mg Tableta Oral, Budesónido 0.125 MG/ML Suspensión para Inhalación [Pulmicort], Astemizol 10 MG Tableta Oral, Espironolactona 25 mg Tableta Oral, Ciprofloxacino 500 MG Tableta Oral, Metotrexato 2.5 mg Tableta Oral, Alteplasa 100 MG Inyección, Adalimumab 40 mg/0.8 mL Inyección Subcutánea, Dolutegravir 50 MG Tableta Oral, Pravastatina 20 mg Tableta Oral, Omeprazol 20 mg Cápsula Oral, Clonazepam 0.25 MG Tableta Oral, Diazepam 5 MG Tableta Oral, Amoxicilina 500 MG / Clavulánico 125 MG Tableta Oral, Docetaxel 20 MG/ML Inyección 1 ML, Domperidona 10 mg Tableta Oral, Desflurano 1000 MG/ML Solución para Inhalación, Alfentanilo 0.5 MG/ML Inyección 10 ML, Etopósido 100 MG Inyección, Albuterol 0.09 MG/ACTUAT Inhalador Dosificado [Ventolin] 200 ACTUACIONES, Naproxeno 500 MG Tableta Oral, Duloxetina 20 MG Cápsula Oral de Liberación Prolongada, Cefalexina 500 MG Tableta Oral, Levetiracetam 500 mg Tableta Oral, Paracetamol 300 MG / Fosfato de Codeína 15 MG Tableta Oral, Albuterol 0.09 MG/ACTUAT Inhalador Dosificado [ProAir] 200 ACTUACIONES, Propranolol 40 mg Tableta Oral, Sufentanilo 0.05 MG/ML Inyección 5 ML, Metoprolol Succinate 25 MG Tableta Oral de Liberación Prolongada 24 Horas, Escitalopram 10 mg Tableta Oral, Hidroclorotiazida 25 MG / Losartán Potásico 100 MG Tableta Oral, Pregabalina 100 MG Cápsula Oral, Albuterol 0.417 MG/ML Solución para Inhalación, Aspirina 81 MG Cápsula Oral, Betametasona 0.1 mg Tableta Oral, Cefpodoxima 200 MG Tableta Oral, Furosemida 40 MG Tableta Oral, Furosemida 10 MG/ML Inyección 10 ML, Stosterona enantato 250 mg/mL Inyección Intramuscular, Metilfenidato Hidrocloruro 20 MG Tableta Oral, Levotiroxina Sódica 0.075 MG Tableta Oral, Losartán Potásico 25 MG Tableta Oral, Diazepam 5 MG/ML Solución Inyectable, Fluticasona Propionato 0.11 MG/ACTUAT Inhalador Dosificado [Flovent] 120 ACTUACIONES, Prednisona 5 MG Tableta Oral, Ciprofloxacino 250 MG Tableta Oral, Pancreatina 600 MG Tableta Oral, Ciprofloxacino 10 MG/ML Inyección 20 ML, Ticagrelor 90 MG Tableta Oral, Enalapril 2.5 MG Tableta Oral, Metoprolol Tartrato 50 MG Tableta Oral, Metoprolol Tartrato 25 MG Tableta Oral, Atorvastatina 10 MG Tableta Oral, Ramipril 5 MG Cápsula Oral, Beclometasona Dipropionato 0.04 MG/ACTUAT Inhalador Dosificado Activado por Respiración [Qvar] 120 ACTUACIONES, Memantina Hidrocloruro 2 MG/ML Solución Oral, Clopidogrel 300 MG Tableta Oral, Enalapril Maleato 10 MG Tableta Oral, Buprenorfina 2 MG / Naloxona 0.5 MG Tableta Sublingual, Carvedilol 25 MG Tableta Oral, Lisopril 20 MG Tableta Oral, Naltrexona clorhidrato 50 MG Tableta Oral, Nicotina 7 MG/Día Sistema Transdérmico 24HR, Cloruro de Sodio 9 MG/ML Solución Inyectable y 1 ML Sulfato de Morfina 5 MG/ML Inyección.." \
"Dosis es de tipo TEXT. Los posibles valores son: 25 MG, 2.5 MG, 0.0272 MG/MG, 250 MG, 325 MG, 220 MG, 21.7 MG/ML, 30 MG, 1 MG/ML, 52 MG, 10 MG, 68 MG, 150 MG/ML, 100 MG, 0.4 MG/ACTUACIÓN, 0.83 MG/ML, 300 MG, 4 MG, 5 MG/ML, 0.044 MG/ACTUACIÓN, 0.21 MG/ML, 500 MG, 0.025 MG/HR, 15 MG, 75 MG, 20 MG, 100 MG/ML, 160 MG, 81 MG, 40 MG, 0.25 MG/ACTUACIÓN, 2000 MG, 50 MG, 80 MG, 400 MG, 5 MG, 0.125 MG, 200 MG, 20 MG/ML, 0.09 MG/ACTUACIÓN, 19.5 MG, 10 MG/ML, 0.00146 MG/HR, 1000 MG/ML, 2 MG, 1000 MG, 4000 MG, 10 mg, 20 mg, 50 mg, 0.125 MG/ML, 25 mg, 2.5 mg, 40 mg/0.8, 0.25 MG, 0.5 MG/ML, 0.09 MG/ACTUAT, 500 mg, 40 mg, 0.05 MG/ML, 0.417 MG/ML, 0.1 mg, 250 mg/mL, 0.075 MG, 0.11 MG/ACTUAT, 600 MG, 90 MG, 0.04 MG/ACTUAT, 2 MG/ML, 7 MG/Día, 9 MG/ML" \
"" \
"La tabla Procedimientos contiene información sobre los procedimientos realizados a los pacientes. " \
"Tiene como PRIMARY KEY Fecha_inicio, EncuentroID y Codigo_SNOMED. Contiene las siguientes columnas:" \
"PacienteID es de tipo TEXT NOT NULL." \
"EncuentroID es de tipo TEXT." \
"Fecha_inicio es de tipo TEXT. La fecha tiene el formato AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Fecha_fin es de tipo TEXT. La fecha es de la forma AÑO-MES-DÍATHORA:MINUTO:SEGUNDOZ (YYYY-MM-DDTHH:MM:SSZ) como por ejemplo 2014-06-10T12:34:06Z." \
"Codigo_SNOMED es de tipo INTEGER. " \
"Descripcion es de tipo TEXT. Los posibles valores son: Reconciliación de medicación, Procedimiento de examen físico, Detección de depresión, Evaluación de necesidades de atención social y de salud, Detección de abuso doméstico, Evaluación del consumo de sustancias, Evaluación utilizando el Alcohol Use Disorders Identification Test - Consumo, Referencia del paciente para atención dental, Consulta dental e informe, Atención dental, Eliminación de placa y cálculo supragingival de todos los dientes utilizando instrumento dental, Eliminación de placa y cálculo subgingival de todos los dientes utilizando instrumento dental, Radiografía dental de tipo mordida, Examen de encías, Tratamiento dental con flúor, Educación sobre salud bucal, Procedimiento quirúrgico dental, Aplicación dental de medicamento desensibilizante, Borrar, Cuidado postoperatorio para procedimiento dental, Restauración del diente con cobertura de todas las cúspides usando material de relleno dental, Tomar impresión oral o dental, Colocación de dentadura, Medición de la función respiratoria, Evaluación de ansiedad, Aplicación de material de relleno dental compuesto a la dentina del diente tras fractura dental, Prueba estándar de embarazo, Ecografía para viabilidad fetal, Evaluación de altura del fondo uterino, Auscultación del corazón fetal, Tipificación de grupo sanguíneo, Medición de antígeno de superficie de Hepatitis B, Prueba de antígeno del virus de la inmunodeficiencia humana (VIH), Prueba de antígeno de Chlamydia, Prueba de título de infección por gonorrea, Prueba de título infeccioso de sífilis, Cultivo de orina, Prueba de detección de orina para diabetes, Prueba de detección de rubéola, Medición de anticuerpos del virus varicela-zóster, Prueba de proteínas en orina, Detección de aneuploidía cromosómica en muestra de líquido amniótico prenatal usando técnica de hibridación fluorescente in situ, Estudio de anatomía fetal, Prueba de alfa-fetoproteína - antenatal, Cultivo de garganta, Inserción de dispositivo anticonceptivo intrauterino, Detección de abuso de sustancias, Detección de depresión usando el cuestionario de salud del paciente de nueve ítems, Vacunación contra la gripe, Detección de glucosa en orina, Nacimiento prematuro de recién nacido, Historia y examen físico, Evaluación inicial del paciente, Desarrollo de plan de atención individualizado, Atención de enfermería/supervisión complementaria, Procedimiento de fisioterapia, Atención de servicios profesionales/auxiliares, Evaluación previa al alta, Alta hospitalaria, Retiro de dispositivo anticonceptivo intrauterino, Detección de anticuerpos RhD en el embarazo, Inmunización pasiva, Ensayo de antígeno del grupo B de Streptococcus pneumoniae, Episiotomía, Cesárea, Colonoscopia, Polipectomía rectal, Reemplazo de dispositivo anticonceptivo intrauterino, Inducción médica del parto, Parto, Inserción de anticonceptivo subcutáneo, Anestesia epidural, Retiro de anticonceptivo subcutáneo, Inyección intramuscular, Parto instrumentado, Extracción de muela, Radiografía de clavícula, Escáner de densidad ósea, Procedimiento de certificación, Notificaciones, Cuidados paliativos, Cribado de sangre oculta en heces, Resección parcial del colon, Cuidados postoperatorios, Quimioterapia combinada con radioterapia, Orientación anticipatoria, Radiografía de húmero, Inmovilización ósea, Examen de esputo, Educación sobre riesgos para la salud, Interpretación de frotis de sangre periférica, Revisión de sistemas, Examen general breve, Extracción de muela del juicio, Derivación al servicio de cardiología, Consulta para tratamiento, Angiografía de arteria coronaria, Manejo postoperatorio de anestesia, Cateterismo cardíaco, Mascarilla facial, Radiografía de tórax, Administración de oxígeno por mascarilla, Colocación del sujeto en posición prono, Terapia de rehabilitación, Evaluación del estado cardíaco con dispositivo de monitoreo, Procedimiento electrocardiográfico, Prueba de laboratorio, Evaluación diagnóstica, Evaluación de riesgos, Ecocardiografía transtorácica, Injerto de defecto óseo periodontal, Terapia ocupacional, Terapia del habla y lenguaje, Recopilación de información, Procedimiento de alveólo dental, Exéresis de torus palatino maxilar, Espirometría, Rehabilitación pulmonar, Transplante de pulmón, Observación cercana, Toma de historia clínica, Discusión sobre signos y síntomas, Procedimiento de evaluación, Discusión sobre el embarazo, Recolección de muestra de orina, Análisis de orina con referencia a microscopía y cultivo, Terapia antibiótica, Educación sobre esterilización, Ligadura bilateral de trompas de falopio, Sutura de herida, Resucitación con líquidos intravenosos, Traslado a unidad de transición, Ingreso a la unidad de cuidados intensivos, Examen neurológico, Examen físico del sistema musculoesquelético, Reparación de mielomeningocele, Exteriorización endoscópica del tercer ventrículo, Cauterización del plexo coroideo, Estudios urodinámicos, Ultrasonografía Doppler de la vena renal, Tomografía computarizada de la cabeza, Resonancia magnética de la columna vertebral, Prueba manual de la función muscular, Cardioversión con corriente continua, Radiografía simple de la región del tobillo, Asesoramiento para la interrupción del embarazo, Interrupción inducida del embarazo, Cuidado post interrupción del embarazo, Radiografía simple de la región de la rodilla, Manipulación quirúrgica de la articulación de la rodilla, Evaluación de regímenes de cuidado, Terapia de movimiento, Cirugía de apendicitis, Electroencefalograma, Referencia a servicio, Radiografía simple de pelvis, Ventilación artificial, Desconexión de ventilación asistida mecánicamente, Referencia a clínica de apnea del sueño, Titulación de presión positiva continua en las vías respiratorias, Diálisis renal, Referencia a cirujano de trasplantes, Referencia a servicio de cirugía cardíaca, Pruebas prequirúrgicas, Ecocardiografía, Notificación del plan de tratamiento, Programación, Inserción de catéter en arteria, Administración de anestesia para procedimiento, Intubación, Cateterización pulmonar con catéter Swan-Ganz, Preparación del paciente para el procedimiento, Canulación, Operación de bypass cardiopulmonar, Colocación de pinza de cruzamiento aórtico y Resonancia magnética cerebral." \
"Razon_descripcion es de tipo TEXT. Los posibles valores son: Gingivitis, Derivación del paciente para atención dental, Enfermedad gingival, Caries dentales primarias, Pérdida de dientes, Bronquitis aguda, Relleno dental flojo, Relleno dental fracturado, Embarazo normal, Faringitis viral aguda, Pólipo rectal recurrente, Aborto espontáneo completo, Infección dental, Trastorno del sueño, Fractura de clavícula, Pólipo de colon, Neoplasia maligna de colon, Faringitis estreptocócica, Fractura de antebrazo, Involucramiento en actividad de riesgo, Enfermedad isquémica del corazón, Hallazgos anormales en imágenes diagnósticas del corazón y circulación coronaria, Enfermedad sospechada causada por el coronavirus 2 de síndrome respiratorio agudo severo, Hipoxemia, Abuso de drogas dependiente, Óvulo huero, Relleno dental con fuga, Infarto de miocardio sin elevación del segmento ST agudo, Resorción del proceso alveolar debido a trauma dental, Relleno dental perdido, Alveolitis de la mandíbula, Torus palatino, Enfisema pulmonar, Esterilización solicitada, Historia de ligadura de trompas, Laceración de la mano, Sepsis, Shock séptico, Meningomielocele, Hidrocefalia, Fibrilación auricular, Fractura de tobillo, Laceración facial, Lesión del ligamento colateral medial de la rodilla, Apendicitis, Fractura cerrada de cadera, Laceración de antebrazo, Síndrome de dificultad respiratoria aguda, Bronquitis crónica obstructiva, Enfermedad renal crónica estadio 4, En espera de trasplante de riñón, Historia de injerto de derivación de arteria coronaria, Embarazo tubárico, Enfermedad renal en etapa terminal, Historia de trasplante renal, Neoplasia maligna superpuesta de colon, Fractura subluxación de muñeca, Fractura de costilla, Luxación traumática de la articulación temporomandibular, Infección por el virus de inmunodeficiencia humana, Cáncer de pulmón sospechado, Carcinoma de pulmón de células no pequeñas en estadio TNM 1, Neoplasia de próstata, Neoplasia maligna primaria de células pequeñas de pulmón en estadio TNM 1, Laceración de pie, Neoplasia maligna de mama, Complicación durante el embarazo, Estenosis de la válvula aórtica, Historia de reemplazo de válvula aórtica, Torus mandibular, Insuficiencia cardíaca congestiva crónica, Regurgitación de la válvula aórtica, Laceración de muslo, Trastorno por déficit de atención en niños, Feto con anomalía cromosómica, Fibrosis quística, Sepsis causada por Pseudomonas, Enfermedad causada por el coronavirus 2 del síndrome respiratorio agudo severo, Depresión mayor episodio único, Ruptura del tendón rotuliano, Quemadura de espesor total, Asma infantil, Anquiloglosia, Fractura de mandíbula, Infarto agudo de miocardio con elevación del segmento ST, Abuso de opioides, En espera de trasplante de médula ósea, Historia de trasplante autólogo de médula ósea, Lesión del ligamento cruzado anterior, Lesión del tendón del manguito rotador del hombro, Trastorno de estrés postraumático, Herida de bala, Salivación excesiva, Historia de trasplante de células madre periféricas y Neoplasia maligna metastásica en colon." \
""

cd = os.getcwd()
def abrirbasededatos(query):
    dataset = sqlite3.connect(f'{cd}/backend/data/base_de_datos/BaseDeDatos.db')
    # Crear un cursor para ejecutar consultas
    cursor = dataset.cursor()
    # Obtener nombres de tablas
    cursor.execute(query)
    tablas = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    # Mostrar resultados con nombres de columnas
    print("-------------------------------------",column_names)
    # Cerrar conexión
    dataset.close()
    return tablas,column_names