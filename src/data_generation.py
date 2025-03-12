import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime, timedelta

# Configuración de rutas
DATA_PROCESSED_PATH = os.path.join('data', 'processed')
DATA_FINAL_PATH = os.path.join('data', 'final')

# Inicializar Faker para datos demográficos
fake = Faker('es_ES')  # Configura Faker para datos en español