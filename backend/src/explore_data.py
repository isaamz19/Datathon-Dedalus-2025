import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        
    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        stats = {
            'total_pacientes': len(self.df),
            'edad_promedio': round(self.df['Edad'].mean(), 1),
            'distribucion_genero': self.df['Genero'].value_counts().to_dict(),
            'distribucion_provincia': self.df['Provincia'].value_counts().to_dict()
        }
        return stats
    
    def get_age_distribution(self):
        """Retorna datos para visualizar distribución de edades"""
        bins = [0, 18, 35, 50, 65, 100]
        labels = ['0-18', '19-35', '36-50', '51-65', '66+']
        self.df['GrupoEdad'] = pd.cut(self.df['Edad'], bins=bins, labels=labels)
        
        age_dist = self.df['GrupoEdad'].value_counts().sort_index()
        
        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': 'Pacientes por grupo de edad',
                'data': age_dist.values.tolist(),
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                ]
            }]
        }
        
        return chart_data
    
    def get_geographic_distribution(self):
        """Retorna datos para visualizar distribución geográfica"""
        geo_data = self.df.groupby('Provincia').size().reset_index(name='count')
        
        return {
            'type': 'geojson',
            'data': geo_data.to_dict('records'),
            'locations': self.df[['Provincia', 'Latitud', 'Longitud']].drop_duplicates().to_dict('records')
        }