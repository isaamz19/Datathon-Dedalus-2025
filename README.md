# Datathon-Dedalus-2025

## 📌 Descripción
Este proyecto implementa un sistema inteligente de respuestas basado en una arquitectura modular que integra **Flask**, **React**, **SQLite** y modelos de **IA en la nube**. Permite procesar consultas de usuarios, analizar datos y generar respuestas precisas mediante inteligencia artificial.

## 🛠 Tecnologías Utilizadas

### Backend
- **Python** y **Flask** → Para manejar la lógica del servidor.
- **SQLite** → Base de datos ligera para almacenar información.

### Frontend
- **React** → Para construir una interfaz interactiva.
- **Python** → Lógica del cliente en conjunto con React.

### Procesamiento de Datos
- **Pandas** y **NumPy** → Para análisis y manipulación eficiente de datos.

### Modelos de Inteligencia Artificial
- **Cloud Haiku** → Procesamiento inicial de las consultas.
- **Cloud 3.5 SONET** → Generación de respuestas precisas.

### Prompt Engineering
- Seguimos **buenas prácticas en SQL**, asegurando consultas eficientes y alineadas con la intención del usuario.
- Nos basamos en el enfoque de **AWS RAG** para mejorar la recuperación y generación de respuestas.

## ⚙️ Arquitectura del Proyecto

1. **El usuario** envía una consulta a través del frontend.
2. **El backend (Flask/Python)** procesa la solicitud y consulta la base de datos.
3. **Cloud Haiku** ayuda en la interpretación inicial de la consulta.
4. **Procesamiento de datos** optimiza la información antes de enviarla a la IA.
5. **Cloud 3.5 SONET** genera una respuesta precisa.
6. **El frontend** muestra el resultado al usuario.

## 🚀 Instalación y Uso

### 🔧 Requisitos previos
- Python 3.x
- Node.js y npm
- Virtualenv (opcional)

### 📥 Instalación
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend
cd ../frontend
npm install
```

### ▶️ Ejecución del Proyecto
```bash
# Ejecutar backend
cd backend
flask run

# Ejecutar frontend
cd ../frontend
npm start
```
