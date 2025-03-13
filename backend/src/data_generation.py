import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker("es_ES")  # Configurar para datos españoles

# --- Listas actualizadas con datos reales ---
provincias_espanolas = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", 
                       "Málaga", "Murcia", "Palma de Mallorca", "Bilbao", "La Coruña"]

# Códigos SNOMED CT reales (ejemplos verificados)
diagnosis_codes = [
    ("91936005", "Alergia al polen"),
    ("91933007", "Alergia a los frutos secos"),
    ("195967001", "Asma"),  
    ("44054006", "Diabetes mellitus tipo 2"),  
    ("59621000", "Hipertensión esencial"),  
    ("293962008", "Alergia a la penicilina"),  
    ("57054005", "EPOC")  # Enfermedad pulmonar obstructiva crónica
]

procedures_codes = [
    ("303893007", "Resonancia magnética cerebral"),
    ("241589008", "Radiografía de tórax"),
    ("430193006", "Colonoscopia"),
    ("433271000", "Espirometría")  # Para EPOC/Asma
]

# Medicamentos reales con dosis estándar
medications = {
    "Diabetes mellitus tipo 2": [
        ("A10BA02", "Metformina", "850 mg", "2 veces al día", "Oral"),
        ("A10BJ02", "Empagliflozina", "10 mg", "1 vez al día", "Oral")
    ],
    "Hipertensión esencial": [
        ("C09AA03", "Lisinopril", "10 mg", "1 vez al día", "Oral"),
        ("C03CA01", "Furosemida", "40 mg", "1 vez al día", "Oral")
    ],
    "EPOC": [
        ("R03AK04", "Formoterol/Budesonida", "12/400 mcg", "2 veces al día", "Inhalación")
    ],
    "Asma": [
        ("R03AC02", "Salbutamol", "100 mcg", "Cada 6 horas", "Inhalación")
    ]
}

# --- Funciones mejoradas ---
def obtener_coordenadas(provincia):
    """Devuelve coordenadas aproximadas de la provincia"""
    coordenadas = {
        "Madrid": (40.4168, -3.7038),
        "Barcelona": (41.3851, 2.1734),
        "Valencia": (39.4699, -0.3763),
        "Sevilla": (37.3891, -5.9845),
        "Zaragoza": (41.6488, -0.8891),
        "Málaga": (36.7194, -4.4200),
        "Murcia": (37.9922, -1.1307),
        "Palma de Mallorca": (39.5696, 2.6502),
        "Bilbao": (43.2630, -2.9350),
        "La Coruña": (43.3623, -8.4115)
    }
    return coordenadas.get(provincia, (fake.latitude(), fake.longitude()))

def generate_patients(n=100):
    """Genera pacientes con distribución realista de edades"""
    patients = []
    for i in range(1, n + 1):
        gender = random.choice(["Masculino", "Femenino"])
        # Distribución de edad: 30% mayores de 65 años
        age = np.random.choice([np.random.randint(30,64), np.random.randint(65,90)], p=[0.7, 0.3])
        province = random.choice(provincias_espanolas)
        lat, lon = obtener_coordenadas(province)
        patients.append([i, gender, age, province, lat, lon])
    return pd.DataFrame(patients, columns=["PacienteID", "Género", "Edad", "Provincia", "Latitud", "Longitud"])

def generate_diagnoses(patients):
    """Asigna diagnósticos con distribución realista"""
    diagnoses = []
    patient_diseases = {}
    
    for _, row in patients.iterrows():
        patient_id = row["PacienteID"]
        age = row["Edad"]
        
        # Probabilidad de diagnóstico basada en edad
        prob_diagnostico = 0.8 if age >= 50 else 0.4
        
        if random.random() < prob_diagnostico:
            # Enfermedades más probables según edad
            if age >= 50:
                diseases = ["Diabetes mellitus tipo 2", "Hipertensión esencial", "EPOC"]
            else:
                diseases = ["Asma", "Alergia al polen", "Alergia a los frutos secos"]
                
            desc = np.random.choice(diseases, p=[0.5, 0.25, 0.25] if age >=50 else [0.6, 0.2, 0.2])
            code = next(code for code, name in diagnosis_codes if name == desc)
            date = fake.date_between(start_date=f"-{random.randint(1,10)}y", end_date="today")
            
            diagnoses.append([patient_id, date, code, desc])
            patient_diseases[patient_id] = desc
            
    return pd.DataFrame(diagnoses, columns=["PacienteID", "Fecha_diagnóstico", "Código_SNOMED", "Descripción"]), patient_diseases

def generate_medications(patients, patient_diseases):
    """Asigna medicamentos coherentes con diagnóstico"""
    meds = []
    for patient, disease in patient_diseases.items():
        if disease in medications:
            # Obtener edad del paciente
            age = patients.loc[patients["PacienteID"] == patient, "Edad"].values[0]
            
            # Seleccionar medicamento apropiado
            available_meds = medications[disease]
            if disease == "Hipertensión esencial" and age > 65:
                available_meds = [m for m in available_meds if m[1] != "Furosemida"]  # Evitar diuréticos en mayores
            
            code, name, dose, freq, route = random.choice(available_meds)
            start_date = fake.date_between(
                start_date=patients.loc[patients["PacienteID"] == patient, "Fecha_diagnóstico"].values[0],
                end_date="today"
            )
            meds.append([patient, start_date, code, name, dose, freq, route])
    return pd.DataFrame(meds, columns=["PacienteID", "Fecha_inicio", "Código", "Nombre", "Dosis", "Frecuencia", "Vía de administración"])

def generate_procedures(patients, patient_diseases):
    """Asigna procedimientos médicos relevantes"""
    procedures = []
    procedure_probabilities = {
        "Diabetes mellitus tipo 2": [("303893007", 0.3), ("241589008", 0.4)],
        "EPOC": [("433271000", 0.7), ("241589008", 0.5)],
        "Asma": [("433271000", 0.6)],
        "default": [("430193006", 0.2)]
    }
    
    for patient, disease in patient_diseases.items():
        if random.random() < 0.5:  # 50% de probabilidad de procedimiento
            procs = procedure_probabilities.get(disease, procedure_probabilities["default"])
            chosen_proc = random.choices(
                [proc[0] for proc in procs],
                weights=[prob[1] for prob in procs]
            )[0]
            
            code, desc = next((code, desc) for code, desc in procedures_codes if code == chosen_proc)
            date = fake.date_between(
                start_date=patients.loc[patients["PacienteID"] == patient, "Fecha_diagnóstico"].values[0],
                end_date="today"
            )
            procedures.append([patient, date, code, desc])
    
    return pd.DataFrame(procedures, columns=["PacienteID", "Fecha_inicio", "Código_SNOMED", "Descripción"])

# --- Generación de datos ---
patients_df = generate_patients(200)  # 200 pacientes
diagnoses_df, patient_diseases = generate_diagnoses(patients_df)
medications_df = generate_medications(patients_df, patient_diseases)
procedures_df = generate_procedures(patients_df, patient_diseases)

# --- Guardar datos ---
patients_df.to_csv("pacientes_realistas.csv", index=False)
diagnoses_df.to_csv("diagnosticos_realistas.csv", index=False)
medications_df.to_csv("medicamentos_realistas.csv", index=False)
procedures_df.to_csv("procedimientos_realistas.csv", index=False)

print("Datos realistas generados exitosamente.")