# src/data_loader.py

def get_carpentry_data():
    """
    Retorna los escenarios, probabilidades y parámetros técnicos
    basados en las diapositivas de David Pozo (Higle, 2005).
    """
    # Escenarios de demanda (Escritorios, Mesas, Sillas)
    scenarios = {
        'Low':    {'d': 50,  't': 20,  'c': 200},
        'Medium': {'d': 150, 't': 110, 'c': 225},
        'High':   {'d': 250, 't': 250, 'c': 500}
    }
    
    # Probabilidades (0.3, 0.4, 0.3)
    probs = {
        'Low': 0.3,
        'Medium': 0.4,
        'High': 0.3
    }
    
    return scenarios, probs


def get_technical_params():
    """
    Retorna los coeficientes técnicos del modelo de carpintería.
    """
    params = {
        'prices': {'d': 60.0, 't': 40.0, 'c': 10.0},
        'costs': {'l': 2.0, 'f': 4.0, 'p': 5.2},
        'resources': {
            'l': {'d': 8.0, 't': 6.0, 'c': 1.0},
            'f': {'d': 4.0, 't': 2.0, 'c': 1.5},
            'p': {'d': 2.0, 't': 1.5, 'c': 0.5}
        }
    }
    return params