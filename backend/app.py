from flask import Flask, request, jsonify
from flask_cors import CORS
from models import modelo
import pandas as pd

app = Flask(__name__)
CORS(app)

last_question = ""
last_table = None
column_name = ""
df = None
historial_conversacion = []

@app.route('/api/send-question', methods=['POST'])
def send_question():
    global last_question , historial_conversacion
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Mensaje no proporcionado"}), 400
    
    last_question = data['message']
    print(f"Pregunta recibida: {last_question}")
    return jsonify({"success": True, "message": "Pregunta recibida correctamente"})

@app.route('/api/get-bot-response', methods=['GET'])
def get_bot_response():
    global last_question, last_table, historial_conversacion
    
    if not last_question:
        return jsonify({"message": "No hay preguntas pendientes"}), 400
    
    # Aquí procesarías la pregunta y generarías una respuesta
    # Este es un ejemplo simple
    if historial_conversacion == []:
        query = modelo.preguntar_query(last_question,modelo.descripcion, None)
    else:
        query = modelo.preguntar_query(last_question,modelo.descripcion, historial_conversacion[-1]["pregunta"])
    last_table ,column_name  = modelo.abrirbasededatos(query)
    convert_last_table_to_df(last_table, column_name)
    response = modelo.preguntar_chatbot(last_question,last_table,historial_conversacion)

    historial_conversacion.append({"pregunta": last_question, "respuesta": response})

    last_question = ""
    return jsonify({"message": response})

def convert_last_table_to_df(last_table, column_name):
    # Verificar si last_table es None o está vacío
    global df
    if last_table is None or len(last_table) == 0:
        return jsonify({"error": "No hay datos en last_table"}), 400
    try:
        df = pd.DataFrame(last_table, columns=column_name)
        df = df.loc[:, ~df.columns.duplicated()]
        if 'PacienteID' in df.columns:
            df = df.drop_duplicates(subset='PacienteID', keep='first')
    except Exception as e:
        return jsonify({"error": f"Error al convertir a DataFrame: {str(e)}"}), 500
    
@app.route('/api/get-estadistic', methods=['GET'])
def get_estadistic():

    summary_data = get_summary_data()
    
    # Obtener distribución por género
    gender_data = get_gender_distribution()
    
    # Obtener distribución por edad
    age_data = get_age_distribution()

    provincia_data = get_provincias_distribution()
    
    # Devolver todos los datos en un solo objeto
    return jsonify({
        "summaryData": summary_data,
        "genderData": gender_data,
        "ageData": age_data,
        "provinciasData": provincia_data,
    })

def get_summary_data():
    # En un entorno real, esto sería una consulta SQL
    global df
    return modelo.calcular_resumen(df)

def get_gender_distribution():
    global df
    return modelo.calcular_distribucion_genero(df)
def get_age_distribution():
    # En un entorno real, esto sería una consulta SQL con CASE para agrupar por rangos de edad
    return modelo.calcular_distribucion_edad(df)
def get_provincias_distribution():
    # En un entorno real, esto sería una consulta SQL
    return modelo.calcular_distribucion_provincias(df)

if __name__ == '__main__':
    app.run(debug=True, port=5000)