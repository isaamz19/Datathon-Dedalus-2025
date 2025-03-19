import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sqlite3

"""# Lista de archivos CSV en el directorio
archivos_csv = [
    "cohorte_alegias.csv",
    "cohorte_condiciones.csv",
    "cohorte_encuentros.csv",
    "cohorte_medicationes.csv",
    "cohorte_pacientes.csv",
    "cohorte_procedimientos.csv"
]

# Cargar los datos
ruta_base = "c:/Users/isabe/OneDrive/Escritorio/Datathon-Dedalus-2025/backend/data/raw/"
dataframes = {archivo: pd.read_csv(os.path.join(ruta_base, archivo)) for archivo in archivos_csv}

# Explorar los datos
for nombre, df in dataframes.items():
    print(f"Datos de {nombre}:")
    print(df.head(), "\n")

# Cargar el CSV
archivo = "cohorte_pacientes.csv"
df = pd.read_csv(os.path.join(ruta_base, archivo))

# Configurar el tamaño de la figura
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Análisis de Pacientes", fontsize=16, fontweight='bold')

# 1. Histograma de edades
sns.histplot(df["Edad"], bins=20, kde=True, ax=axes[0, 0], color="royalblue")
axes[0, 0].set_title("Distribución de Edades", fontsize=12)
axes[0, 0].set_ylabel("Cantidad")

# 2. Conteo de Género con etiquetas
ax1 = sns.countplot(x=df["Genero"], ax=axes[0, 1], palette="pastel")
axes[0, 1].set_title("Distribución de Género", fontsize=12)
axes[0, 1].set_ylabel("Cantidad")
axes[0, 1].set_yticks([])

# Agregar etiquetas con los valores exactos
for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height())}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# 3. Pacientes por Provincia
ax2 = sns.countplot(y=df["Provincia"], order=df["Provincia"].value_counts().index, ax=axes[1, 0], palette="coolwarm")
axes[1, 0].set_title("Pacientes por Provincia", fontsize=12)
axes[1, 0].set_ylabel("Provincia")

# Ajustar etiquetas para evitar solapamiento
axes[1, 0].tick_params(axis='y', labelsize=8)

# 4. Mapa de dispersión (Latitud vs Longitud)
sns.scatterplot(x=df["Longitud"], y=df["Latitud"], ax=axes[1, 1], alpha=0.5, color="green")
axes[1, 1].set_title("Distribución Geográfica", fontsize=12)
axes[1, 1].set_xlabel("Longitud")
axes[1, 1].set_ylabel("Latitud")

# Ajustar diseño
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show() 

"""

"""# Conectar a la base de datos
cd = os.getcwd()
conn = sqlite3.connect(f'{cd}/backend/data/base_de_datos/BaseDeDatos.db')

# Leer una tabla en un DataFrame de pandas
df = pd.read_sql_query("SELECT * FROM Pacientes", conn)

# Convertir fechas a formato datetime (si aún no lo hiciste)
df["Fecha_nacimiento"] = pd.to_datetime(df["Fecha_nacimiento"], errors="coerce")
df["Fecha_muerte"] = pd.to_datetime(df["Fecha_muerte"], errors="coerce")

# Configurar el tamaño de la figura
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Análisis de Pacientes", fontsize=16, fontweight='bold')

# 1. Histograma de edades
df["Edad"] = df["Edad"].astype(str).str.extract("(\d+)")  # Extrae solo los números
df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")   # Convierte a número
binsnum = [0, 18, 35, 50, 65, 100]  # Ejemplo: niños, jóvenes, adultos, mayores
sns.histplot(df["Edad"], bins=binsnum, kde=True, ax=axes[0, 0], color="royalblue")
axes[0, 0].set_title("Distribución de Edades", fontsize=12)
axes[0, 0].set_ylabel("Cantidad")
# Ajustar las etiquetas del eje X para que sean más legibles
tick_positions = [(binsnum[i] + binsnum[i + 1]) / 2 for i in range(len(binsnum) - 1)]
axes[0, 0].set_xticks(tick_positions)  # Poner ticks en los centros de los rangos
labels = ["0-18", "19-35", "36-50", "51-65", "66-100"]
axes[0, 0].set_xticklabels(labels)  # Asignar etiquetas a los bins

# 2. Conteo de Género con etiquetas
ax1 = sns.countplot(x=df["Genero"], ax=axes[0, 1], palette="pastel")
axes[0, 1].set_title("Distribución de Género", fontsize=12)
axes[0, 1].set_ylabel("Cantidad")
axes[0, 1].set_yticks([])

# Agregar etiquetas con los valores exactos
for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height())}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# 3. Pacientes por Provincia
ax2 = sns.countplot(y=df["Provincia"], order=df["Provincia"].value_counts().index, ax=axes[1, 0], palette="coolwarm")
axes[1, 0].set_title("Pacientes por Provincia", fontsize=12)
axes[1, 0].set_ylabel("Provincia")

# 4. Pacientes por razas

ax3 = sns.countplot(x=df["Raza"], ax=axes[1, 1], palette="pastel")
axes[1, 1].set_title("Distribución de Razas", fontsize=12)
axes[1, 1].set_ylabel("Cantidad")
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
axes[1, 1].set_yticks([])

# Agregar etiquetas con los valores exactos
for p in ax3.patches:
    ax3.annotate(f'{int(p.get_height())}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Ajustar el diseño
plt.tight_layout()

# Mostrar la figura
plt.show()

# Cerrar la conexión
conn.close() """

"""# Cargar el CSV
# Conectar a la base de datos
cd = os.getcwd()
conn = sqlite3.connect(f'{cd}/backend/data/base_de_datos/BaseDeDatos.db')

# Leer una tabla en un DataFrame de pandas
df = pd.read_sql_query("SELECT * FROM Condiciones", conn) """


ruta_base = "c:/Users/isabe/OneDrive/Escritorio/Datathon-Dedalus-2025/backend/data/raw/"
archivo = "cohorte_condiciones.csv"
df = pd.read_csv(os.path.join(ruta_base, archivo))

# Convertir fechas a formato datetime (si aún no lo hiciste)
df["Fecha_inicio"] = pd.to_datetime(df["Fecha_inicio"], errors="coerce")
df["Fecha_fin"] = pd.to_datetime(df["Fecha_fin"], errors="coerce")

# Crear una nueva columna con la duración de los procedimientos
df["Duracion_dias"] = (df["Fecha_fin"] - df["Fecha_inicio"]).dt.days

# Configurar la figura con 4 gráficos
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Análisis de Condiciones", fontsize=16, fontweight='bold')

# 1. Duración de los procedimientos (boxplot)
sns.boxplot(x=df["Duracion_dias"], ax=axes[0, 0], color="lightcoral")
axes[0, 0].set_title("Duración de Condiciones (en días)", fontsize=12)
axes[0, 0].set_xlabel("Días de Duración")
axes[0, 0].set_yticks([])  # Ocultar números en el eje Y

# 2. Procedimientos más comunes (top 10)
desc_frecuencia = df["Condicion"].value_counts()
top_10 = desc_frecuencia.head(10)
sns.barplot(x=top_10.values, y=top_10.index, ax=axes[0, 1], palette="coolwarm")
axes[0, 1].set_title("Condiciones", fontsize=12)
axes[0, 1].set_xlabel("Cantidad")
axes[0, 1].set_ylabel("Condición")
print(df["Condicion"].unique())

# 3. Cantidad de procedimientos por paciente
procedimientos_por_paciente = df["PacienteID"].value_counts()
sns.histplot(procedimientos_por_paciente, bins=20, kde=True, ax=axes[1, 0], color="green")
axes[1, 0].set_title("Distribución de Condiciones por Paciente", fontsize=12)
axes[1, 0].set_xlabel("Cantidad de Condiciones")
axes[1, 0].set_ylabel("Número de Pacientes")

# 4. Espacio vacío en (1,1)
"""desc_frecuencia = df["Razon_descripcion"].fillna("Desconocido").value_counts()
desc_frecuencia = desc_frecuencia[desc_frecuencia.index != "Desconocido"]
top_10 = desc_frecuencia.head(10)
sns.barplot(x=top_10.values, y=top_10.index, ax=axes[1, 1], palette="coolwarm")
axes[1, 1].set_title("Razón del procedimiento", fontsize=12)
axes[1, 1].set_xlabel("Cantidad")
axes[1, 1].set_ylabel("Razon")
print(df["Razon_descripcion"].unique()) """

axes[1, 1].axis("off")  # ⬅ Oculta completamente el subplot

# Ajustar diseño
plt.tight_layout()
plt.show()
# conn.close()