from flask import Flask, request, jsonify
from flask_cors import CORS
from models import modelo

app = Flask(__name__)
CORS(app)

last_question = ""

@app.route('/api/send-question', methods=['POST'])
def send_question():
    global last_question
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Mensaje no proporcionado"}), 400
    
    last_question = data['message']
    print(f"Pregunta recibida: {last_question}")
    
    return jsonify({"success": True, "message": "Pregunta recibida correctamente"})

@app.route('/api/get-bot-response', methods=['GET'])
def get_bot_response():
    global last_question
    
    if not last_question:
        return jsonify({"message": "No hay preguntas pendientes"}), 400
    
    # Aquí procesarías la pregunta y generarías una respuesta
    # Este es un ejemplo simple
    buscar_info = modelo.buscar_info(last_question, modelo.textos)
    response = modelo.preguntar_chatbot(last_question, buscar_info)
    # Limpiar la pregunta después de responder
    last_question = ""
    
    return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)