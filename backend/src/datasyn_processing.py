import os
import pandas as pd
##from googletrans import Translator

# Inicializamos el traductor
##translator = Translator()

def translate_text(text, src='en', dest='es'):
    try:
        translation = translator.translate(text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"Error al traducir '{text}': {e}")
        return text


##from deep_translator import GoogleTranslator

def translate_text_medical(text, src='en', dest='es'):
    """
    Traduce el texto de inglés a español usando GoogleTranslator.
    Se recomienda sustituirlo o complementarlo con una solución especializada en terminología médica.
    """
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        print(f"Error al traducir '{text}': {e}")
        return text

def translate_columns_in_csv(file_path, columns):
    """
    Lee el CSV en file_path, traduce las columnas especificadas y sobrescribe el archivo.
    """
    df = pd.read_csv(file_path)
    for col in columns:
        if col in df.columns:
            # Se traduce solo si el valor no es nulo
            df[col] = df[col].apply(lambda x: translate_text_medical(x) if pd.notnull(x) else x)
        else:
            print(f"Columna '{col}' no encontrada en {file_path}")
    df.to_csv(file_path, index=False)
    print(f"Archivo traducido (sobrescrito) guardado en: {file_path}")

def post_process_translation():
    base_processed = "backend/data/processed/Synthesia/"
    
    # Diccionario con nombre de archivo y columnas a traducir
    files_to_translate = {
        "allergies_procesado.csv": ["descripcion"],
        "conditions_procesado.csv": ["descripcion"],
        "encounters_procesado.csv": ["descripcion", "razondescripcion"],
        "imaging_studies_procesado.csv": ["bodysite_description", "sop_description"],
        "immunizations_procesado.csv": ["description"],
        "medications_procesado.csv": ["descripcion"],
        "observations_procesado.csv": ["descripcion"],
        "patientes_procesado.csv": ["raza", "etnia"],
        "procedures_procesado.csv": ["descripcion", "razondescripcion"]
    }
    
    for file_name, cols in files_to_translate.items():
        file_path = os.path.join(base_processed, file_name)
        translate_columns_in_csv(file_path, cols)


# Diccionario para mapear estados de EE. UU. a provincias españolas (ejemplo)
us_to_es = {
    "Alabama": "Andalucía",
    "Alaska": "Galicia",
    "Arizona": "Aragón",
    "Arkansas": "Extremadura",
    "California": "Cataluña",
    "Colorado": "Castilla y León",
    "Connecticut": "Cantabria",
    "Delaware": "Comunidad Valenciana",
    "Florida": "Murcia",
    "Georgia": "País Vasco",
    "Hawaii": "Islas Canarias",
    "Idaho": "La Rioja",
    "Illinois": "Madrid",
    "Indiana": "Asturias",
    "Iowa": "Navarra",
    "Kansas": "Baleares",
    "Kentucky": "Andalucía",
    "Louisiana": "Cataluña",
    "Maine": "Galicia",
    "Maryland": "Valencia",
    "Massachusetts": "Castilla-La Mancha",
    "Michigan": "Castilla y León",
    "Minnesota": "Aragón",
    "Mississippi": "Extremadura",
    "Missouri": "Cantabria",
    "Montana": "Murcia",
    "Nebraska": "País Vasco",
    "Nevada": "La Rioja",
    "New Hampshire": "Madrid",
    "New Jersey": "Asturias",
    "New Mexico": "Navarra",
    "New York": "Baleares",
    "North Carolina": "Andalucía",
    "North Dakota": "Cataluña",
    "Ohio": "Galicia",
    "Oklahoma": "Valencia",
    "Oregon": "Castilla-La Mancha",
    "Pennsylvania": "Castilla y León",
    "Rhode Island": "Aragón",
    "South Carolina": "Extremadura",
    "South Dakota": "Cantabria",
    "Tennessee": "Murcia",
    "Texas": "País Vasco",
    "Utah": "La Rioja",
    "Vermont": "Madrid",
    "Virginia": "Asturias",
    "Washington": "Navarra",
    "West Virginia": "Baleares",
    "Wisconsin": "Andalucía",
    "Wyoming": "Cataluña"
}

gender_to_gender = {
    "F":"Femenino",
    "M":"Masculino"
}

def map_state_to_province(state):
    """Mapea el estado de EE. UU. a una provincia española usando el diccionario."""
    return us_to_es.get(state, state)

def map_gender(gender):
    return gender_to_gender.get(gender, gender)
    
def process_patients(input_path, output_path):
    """
    Procesa el CSV de pacientes (patientes.csv) extrayendo:
      - Id, BIRTHDATE, DEATHDATE, RACE, ETHNICITY, GENDER y STATE.
    Renombra las columnas a: id, birthdate, deathdate, raza, etnia, género y provincia,
    y mapea el estado a una provincia española.
    """
    df = pd.read_csv(input_path)
    df = df[['Id', 'BIRTHDATE', 'DEATHDATE', 'RACE', 'ETHNICITY', 'GENDER', 'STATE']]
    df.rename(columns={
        'Id': 'id',
        'BIRTHDATE': 'birthdate',
        'DEATHDATE': 'deathdate',
        'RACE': 'raza',
        'ETHNICITY': 'etnia',
        'GENDER': 'género',
        'STATE': 'provincia'
    }, inplace=True)
    df['provincia'] = df['provincia'].apply(map_state_to_province)
    df['género'] = df['género'].apply(map_gender)
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def process_allergies(input_path, output_path):
    """
    Procesa el CSV de alergias (allergies.csv) extrayendo:
      - PATIENT, START, STOP, ENCOUNTER, CODE y DESCRIPTION.
    Renombra las columnas y traduce la descripción al español.
    """
    df = pd.read_csv(input_path)
    df = df[['PATIENT', 'START', 'STOP', 'ENCOUNTER', 'CODE', 'DESCRIPTION']]
    df.rename(columns={
        'PATIENT': 'paciente',
        'START': 'start',
        'STOP': 'stop',
        'ENCOUNTER': 'encuentro_id',
        'CODE': 'codigo',
        'DESCRIPTION': 'descripcion'
    }, inplace=True)
    ##df['descripcion'] = df['descripcion'].apply(lambda x: translate_text(x))
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")


def process_conditions(input_path, output_path):
    df = pd.read_csv(input_path)
    # Seleccionamos las columnas que nos interesan, según el header real
    df = df[['PATIENT', 'START', 'STOP', 'CODE', 'DESCRIPTION']]
    df.rename(columns={
        'PATIENT': 'paciente',
        'START': 'fecha_inicio',
        'STOP': 'fecha_fin',
        'CODE': 'codigo_snomed',
        'DESCRIPTION': 'descripcion'
    }, inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")


def process_encounters(input_path, output_path):
    """
    Procesa el CSV de encuentros (encounters.csv) extrayendo:
      - Id, START, STOP, ENCOUNTERCLASS, CODE, DESCRIPTION, REASONCODE y REASONDESCRIPTION.
    Renombra las columnas a: id, fecha_inicio, fecha_fin, tipo_encuentro, codigo_encuentro,
    descripcion, razoncodigo y razondescripcion.
    """
    df = pd.read_csv(input_path)
    df = df[['Id', 'START', 'STOP', 'ENCOUNTERCLASS', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION']]
    df.rename(columns={
        'Id': 'id',
        'START': 'fecha_inicio',
        'STOP': 'fecha_fin',
        'ENCOUNTERCLASS': 'tipo_encuentro',
        'CODE': 'codigo_encuentro',
        'DESCRIPTION': 'descripcion',
        'REASONCODE': 'razoncodigo',
        'REASONDESCRIPTION': 'razondescripcion'
    }, inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def process_imaging_studies(input_path, output_path):
    """
    Procesa el CSV de estudios de imagen (imaging_studies.csv) extrayendo:
      - Id, DATE, PATIENT, ENCOUNTER, BODYSITE_CODE, BODYSITE_DESCRIPTION,
        MODALITY_DESCRIPTION, PROCEDURE_CODE y SOP_DESCRIPTION.
    Renombra las columnas a: id, fecha, paciente, encuentro, bodysite_code,
    bodysite_description, modality_description, procedure_code y sop_description.
    """
    df = pd.read_csv(input_path)
    df = df[['Id', 'DATE', 'PATIENT', 'ENCOUNTER', 'BODYSITE_CODE', 'BODYSITE_DESCRIPTION',
             'MODALITY_DESCRIPTION', 'PROCEDURE_CODE', 'SOP_DESCRIPTION']]
    df.rename(columns={
        'Id': 'id',
        'DATE': 'fecha',
        'PATIENT': 'paciente',
        'ENCOUNTER': 'encuentro',
        'BODYSITE_CODE': 'bodysite_code',
        'BODYSITE_DESCRIPTION': 'bodysite_description',
        'MODALITY_DESCRIPTION': 'modality_description',
        'PROCEDURE_CODE': 'procedure_code',
        'SOP_DESCRIPTION': 'sop_description'
    }, inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def extract_administration_route(text):
    """
    Extrae la vía de administración a partir de palabras clave en el texto.
    Si encuentra 'oral', 'inhalation', etc., retorna su equivalente en español.
    """
    keywords = {
        'oral': 'oral',
        'inhalation': 'inhalación',
        'inhaler':'inhalación',
        'intravenous': 'intravenosa',
        'subcutaneous': 'subcutánea',
        'topical': 'tópica',
        'implant': 'implante',
        'injection':'inyección',
        'syringe':'inyección',
        'injectable':'inyección',
        'intrauterine':'intrauterino',
        'transdermal':'inyección',
        'day pack':'oral'
    }
    text_lower = text.lower()
    for key, value in keywords.items():
        if key in text_lower:
            return value
    return ""

def process_medications(input_path, output_path):
    """
    Procesa el CSV de medicaciones (medications.csv) extrayendo:
      - START, STOP, PATIENT, ENCOUNTER, CODE, DESCRIPTION y DISPENSES.
    Renombra las columnas a: start, stop, paciente, encuentro, codigo, descripcion y frecuencia.
    Traduce la descripción, extrae la vía de administración (buscando palabras clave)
    y la agrega en una columna 'via_administracion'.
    """
    df = pd.read_csv(input_path)
    df = df[['START', 'STOP', 'PATIENT', 'ENCOUNTER', 'CODE', 'DESCRIPTION', 'DISPENSES']]
    df.rename(columns={
        'START': 'start',
        'STOP': 'stop',
        'PATIENT': 'paciente',
        'ENCOUNTER': 'encuentro',
        'CODE': 'codigo',
        'DESCRIPTION': 'descripcion',
        'DISPENSES': 'frecuencia'
    }, inplace=True)
    ##df['descripcion'] = df['descripcion'].apply(lambda x: translate_text(x))
    df['via_administracion'] = df['descripcion'].apply(lambda x: extract_administration_route(x))
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def process_observations(input_path, output_path):
    """
    Procesa el CSV de observaciones (observations.csv) conservando todas las columnas:
      DATE, PATIENT, ENCOUNTER, CATEGORY, CODE, DESCRIPTION, VALUE, UNITS y TYPE.
    Renombra las columnas a: fecha, paciente, encuentro, categoria, codigo,
    descripcion, valor, unidades y tipo.
    Traduce los campos de texto: categoria, descripcion y tipo.
    """
    df = pd.read_csv(input_path)
    df.rename(columns={
        'DATE': 'fecha',
        'PATIENT': 'paciente',
        'ENCOUNTER': 'encuentro',
        'CATEGORY': 'categoria',
        'CODE': 'codigo',
        'DESCRIPTION': 'descripcion',
        'VALUE': 'valor',
        'UNITS': 'unidades',
        'TYPE': 'tipo'
    }, inplace=True)
    ##df['categoria'] = df['categoria'].apply(lambda x: translate_text(x))
    ##df['descripcion'] = df['descripcion'].apply(lambda x: translate_text(x))
    ##df['tipo'] = df['tipo'].apply(lambda x: translate_text(x))
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def process_procedures(input_path, output_path):
    """
    Procesa el CSV de procedimientos (procedures.csv) extrayendo:
      - START, STOP, PATIENT, ENCOUNTER, SYSTEM, CODE, DESCRIPTION, REASONCODE y REASONDESCRIPTION.
    Se descarta BASE_COST.
    Renombra las columnas a: start, stop, paciente, encuentro, sistema, codigo, descripcion,
    razoncodigo y razondescripcion.
    Traduce los campos 'descripcion' y 'razondescripcion'.
    """
    df = pd.read_csv(input_path)
    df = df[['START', 'STOP', 'PATIENT', 'ENCOUNTER', 'SYSTEM', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION']]
    df.rename(columns={
        'START': 'start',
        'STOP': 'stop',
        'PATIENT': 'paciente',
        'ENCOUNTER': 'encuentro',
        'SYSTEM': 'sistema',
        'CODE': 'codigo',
        'DESCRIPTION': 'descripcion',
        'REASONCODE': 'razoncodigo',
        'REASONDESCRIPTION': 'razondescripcion'
    }, inplace=True)
    ##df['descripcion'] = df['descripcion'].apply(lambda x: translate_text(x))
    ##df['razondescripcion'] = df['razondescripcion'].apply(lambda x: translate_text(x))
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def process_immunizations(input_path, output_path):
    """
    Procesa el CSV de inmunizaciones (immunizations.csv).
    No se especifica transformación, por lo que se realiza un guardado simple
    con renombrado a minúsculas en las columnas.
    """
    df = pd.read_csv(input_path)
    df.columns = [col.lower() for col in df.columns]
    df.to_csv(output_path, index=False)
    print(f"Archivo procesado guardado en: {output_path}")

def main():
    base_raw = "backend/data/raw/Synthesia/"
    base_processed = "backend/data/processed/Synthesia/"
    os.makedirs(base_processed, exist_ok=True)
    
    process_patients(os.path.join(base_raw, "patients.csv"),
                     os.path.join(base_processed, "patientes_procesado.csv"))
    process_allergies(os.path.join(base_raw, "allergies.csv"),
                      os.path.join(base_processed, "allergies_procesado.csv"))
    process_conditions(os.path.join(base_raw, "conditions.csv"),
                       os.path.join(base_processed, "conditions_procesado.csv"))
    process_encounters(os.path.join(base_raw, "encounters.csv"),
                       os.path.join(base_processed, "encounters_procesado.csv"))
    process_imaging_studies(os.path.join(base_raw, "imaging_studies.csv"),
                            os.path.join(base_processed, "imaging_studies_procesado.csv"))
    process_medications(os.path.join(base_raw, "medications.csv"),
                        os.path.join(base_processed, "medications_procesado.csv"))
    ##process_observations(os.path.join(base_raw, "observations.csv"),
                         ##os.path.join(base_processed, "observations_procesado.csv"))
    process_procedures(os.path.join(base_raw, "procedures.csv"),
                       os.path.join(base_processed, "procedures_procesado.csv"))
    process_immunizations(os.path.join(base_raw, "immunizations.csv"),
                          os.path.join(base_processed, "immunizations_procesado.csv"))

if __name__ == "__main__":
    main()
    ##post_process_translation()
